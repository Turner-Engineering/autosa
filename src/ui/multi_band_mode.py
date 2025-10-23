import datetime
import threading

import customtkinter as ctk

from instrument.instrument import get_run_filename, get_run_id, run_band
from ui.get_resource_path import resource_path
from ui.save_window_popups import CompletedWindow, NoRunNoteWindow
from ui.test_log_window import OpenTestLog
from ui.ui_logger import LoggingButton, LoggingTopLevel
from utils.logger import autosa_logger
from utils.settings import read_settings_from_file
from utils.test_log import get_test_logs


class ConfirmWindow(LoggingTopLevel):
    def __init__(self, parent, discon_btn_st, run_multiple_bands):
        super().__init__(parent)
        self.title("Confirm Runs")
        self.parent = parent
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.resizable(False, False)  # disable resizing
        self.transient(parent)
        self.center()  # center on screen, otherwise it will be in the top left corner

        self.frame_color = parent.frame_color
        self.label_color = parent.label_color
        self.discon_btn_st = discon_btn_st
        self.run_multiple_bands = run_multiple_bands
        self.create_widgets()

    def create_widgets(self):
        frame = self.init_frame()
        self.fill_frame(frame)

    def init_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        return frame

    def fill_frame(self, frame):
        text = self.get_confirmation_text()

        # Confirmation Text
        ctk.CTkLabel(
            frame,
            text=text,
            justify="left",
        ).grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        # Okay Button
        LoggingButton(
            frame,
            text="Okay",
            state=self.discon_btn_st,
            command=lambda: self.confirmation_callback(),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cancel Button
        LoggingButton(
            frame,
            text="Cancel",
            command=lambda: self.destroy(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        ).grid(row=1, column=1, padx=5, pady=5, sticky="e")

    def get_confirmation_text(self):
        band_range = self.parent.band_range_var.get()
        run_count = self.get_run_count(band_range)
        run_note = self.parent.run_note_var.get()
        band_ori_full = (
            "" if self.parent.ori_var.get() == "None" else self.parent.ori_var.get()
        )
        band_ori = band_ori_full[0].lower() if band_ori_full else ""
        run_id = "XYZ-AB"
        first_band = band_range[:2]
        cur_time = datetime.datetime.now().strftime("%H_%M_%S")
        sweep_dur = read_settings_from_file()["-SWEEP DUR-"]

        text = (
            "Please confirm that you would like to run bands\n"
            f"{band_range} ({run_count} runs total)\n"
            f"for {sweep_dur} seconds each\n"
            "and that the first filename should be:\n"
            f"{run_id} {run_note} {sweep_dur}s {first_band}{band_ori} {cur_time}\n"
            "(the rest will be numbered sequentially).\n"
            "The time will not be included in the checklist,\n"
            "but will be in the actual saved filename."
        )
        return text

    def get_run_count(self, band_range):
        if band_range == "B0 - B4 (monopole)":
            run_count = 5
        elif band_range == "B5 - B7 (bilogical)":
            run_count = 3
        elif band_range == "B0 - B7 (50 Ohm Term)":
            run_count = 8
        elif band_range == "B0 - B7 (Unterminated)":
            run_count = 8
        else:
            raise ValueError("Invalid band range")
        return run_count

    def confirmation_callback(self):
        # create new thread
        autosa_logger.debug(
            f"Multi Band Mode runs confirmed and started {self.parent.band_range_var.get()} runs"
        )
        self.destroy()  # close confirm window
        new_thread = threading.Thread(target=self.run_multiple_bands, daemon=True)
        new_thread.start()

    def center(self):
        # roughly center the popup
        x = self.winfo_screenwidth() // 2 - 200
        y = self.winfo_screenheight() // 2 - 300
        self.geometry("{}+{}".format(x, y))


class MultiModeFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        inst_found,
        inst,
        discon_btn_st,
        header_access,
        current_test_log,
        frame_color,
        label_color,
    ):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.discon_btn_st = discon_btn_st
        self.header_access = header_access
        self.current_test_log = current_test_log
        self.frame_color = frame_color
        self.label_color = label_color
        self.check_color = "#2d1a03"

        self.band_ranges = [
            "B0 - B4 (monopole)",
            "B5 - B7 (bilogical)",
            "B0 - B7 (50 Ohm Term)",
            "B0 - B7 (Unterminated)",
        ]

        self.bands = ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"]

        # CTK Variables
        self.band_range_var = ctk.StringVar(value=self.band_ranges[0])
        self.run_note_var = ctk.StringVar()
        self.ori_var = ctk.StringVar()

        self.band_range_var.trace_add("write", self.call_update_band_keys)
        self.update_band_keys()

        self.run_filename = None
        self.is_cancel = False
        self.saved_files = []

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()
        self.frame3 = self.init_frame3()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        frame2.columnconfigure([1], weight=1)
        frame2.rowconfigure(0, weight=1)
        return frame2

    def init_frame3(self):
        frame3 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame3.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        frame3.columnconfigure([1], weight=1)
        return frame3

    def fill_frame1(self, frame1):
        # Run Note Label
        ctk.CTkLabel(
            frame1,
            text="Run Note: ",
            fg_color=self.label_color,
            width=80,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Run Note Entry
        self.run_note_entry = ctk.CTkEntry(
            frame1,
            textvariable=self.run_note_var,
            width=300,
        )
        self.run_note_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Band Range Label
        ctk.CTkLabel(
            frame1,
            text="Band Range: ",
            fg_color=self.label_color,
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

        # Band Range Dropdown
        self.band_range_dropdown = ctk.CTkOptionMenu(
            frame1,
            values=self.band_ranges,
            variable=self.band_range_var,
            command=lambda event: self.update_ori_dropdown(),
            width=180,
        )
        self.band_range_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # Orientation Label
        ctk.CTkLabel(
            frame1,
            text="Orientation: ",
            fg_color=self.label_color,
        ).grid(row=2, column=0, padx=5, pady=5, sticky="w")

        # Orientation Dropdown
        self.ori_dropdown = ctk.CTkOptionMenu(
            frame1,
            values=["Horizontal", "Vertical"],
            variable=self.ori_var,
            command=lambda event: autosa_logger.info(
                f"{self.ori_var.get()} orientation was selected."
            ),
            width=180,
        )
        self.ori_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.update_ori_dropdown()

    def fill_frame2(self, frame2):
        # Run Button
        self.run_button = LoggingButton(
            frame2,
            text="Run Sweeps",
            command=lambda: self.check_and_run(),
        )
        self.run_button.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        # Progress Bar
        self.pbar = ctk.CTkProgressBar(frame2, height=15, corner_radius=0)
        self.pbar.set(0)  # start at 0
        self.pbar.grid(row=0, column=1, padx=10, pady=5, sticky="ew")

        # Progress Amount Label
        self.pbar_label = ctk.CTkLabel(
            frame2,
            text="0/#",
            fg_color=self.label_color,
        )
        self.pbar_label.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Cancel Button
        LoggingButton(
            frame2,
            text="Cancel",
            command=lambda: self.update_cancel_status(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="e")

    def fill_frame3(self, frame3):
        for widget in frame3.winfo_children():
            widget.destroy()

        self.band_checkbox = {}
        self.band_filenames = {}
        run_note = self.run_note_var.get()
        band_ori_full = "" if self.ori_var.get() == "None" else self.ori_var.get()
        band_ori = band_ori_full[0].lower() if band_ori_full else ""
        self.run_id_counter = None
        sweep_dur = read_settings_from_file()["-SWEEP DUR-"]

        for i, band_key in enumerate(self.band_keys):
            run_id = self.get_next_run_id()
            cur_filename = f"{run_id} {run_note} {sweep_dur}s {band_key}{band_ori}"
            self.band_filenames[band_key] = cur_filename

            check_var = ctk.BooleanVar(value=False)
            checkbox = ctk.CTkCheckBox(
                frame3,
                text=cur_filename,
                variable=check_var,
                state="disabled",
                corner_radius=3,
                border_width=1.5,
                border_color=self.check_color,
                text_color_disabled=self.check_color,
                checkbox_height=12,
                checkbox_width=12,
            )
            checkbox.grid(row=i + 1, column=0, padx=5, pady=2, sticky="w")

            self.band_checkbox[band_key] = (checkbox, check_var)

    # helps get next run_id becasue `get_run_id` will return the same ID (e.g. 622-01 run_note B0, 622-01 run_note B1)
    # only used to display
    def get_next_run_id(self):
        if self.run_id_counter is None:
            base_run_id = get_run_id(
                self.inst, read_settings_from_file()["-INST OUT FOLDER-"]
            )
            date_part, count_part = base_run_id.split("-")
            self.run_id_date = date_part
            self.run_id_counter = int(count_part)
        else:
            self.run_id_counter += 1

        return f"{self.run_id_date}-{self.run_id_counter:02}"

    def update_ori_dropdown(self):
        """disables and enables the orientation based on the selected range"""
        band_range = self.band_range_var.get()
        if band_range == "B5 - B7 (bilogical)":
            self.ori_dropdown.configure(state="normal")
            if self.ori_var.get() not in ["Horizontal", "Vertical"]:
                self.ori_dropdown.set("Horizontal")
            autosa_logger.info(f"{self.ori_var.get()} orientation was selected.")
        else:
            self.ori_dropdown.configure(state="disabled")
            self.ori_dropdown.set("None")

    def update_cancel_status(self):
        autosa_logger.info("Runs canceled.")
        self.is_cancel = True

    def call_update_band_keys(self, *args):
        self.update_band_keys()

    def update_band_keys(self):
        band_range = self.band_range_var.get()

        if band_range == "B0 - B4 (monopole)":
            self.band_keys = self.bands[:5]
        elif band_range == "B5 - B7 (bilogical)":
            self.band_keys = self.bands[5:]
        elif band_range == "B0 - B7 (50 Ohm Term)":
            self.band_keys = self.bands
            self.run_note_var.set("50 Ohm Term")
        elif band_range == "B0 - B7 (Unterminated)":
            self.band_keys = self.bands
            self.run_note_var.set("Unterminated")
        else:
            self.band_keys = []

        autosa_logger.info(f"Band Range {band_range} was selected for run.")

    def disable_buttons(self):
        self.ori_dropdown.configure(state="disabled")
        self.run_note_entry.configure(state="disabled")
        self.band_range_dropdown.configure(state="disabled")
        self.run_button.configure(state="disabled")

    def enable_buttons(self):
        self.update_ori_dropdown()
        self.run_note_entry.configure(state="normal")
        self.band_range_dropdown.configure(state="normal")
        self.run_button.configure(state="normal")

    def check_and_run(self):
        if self.run_note_var.get().strip() == "":
            autosa_logger.info("Multi Band Mode: No Run Note was entered.")
            self.disable_buttons()
            self.wait_window(NoRunNoteWindow(self))
            self.enable_buttons()
        else:
            self.disable_buttons()

            if not self.current_test_log.get("full_path"):
                self.log_window = OpenTestLog(
                    self,
                    self.inst,
                    self.inst_found,
                    self.header_access.test_log_label,
                    self.frame_color,
                    self.label_color,
                )
                self.log_window.wait_window()

                if hasattr(self.log_window, "data"):
                    self.current_test_log.clear()
                    self.current_test_log.update(
                        {
                            "full_path": self.log_window.data.get("Log Filename"),
                            "project_name": self.log_window.data.get(
                                "Project Name", "No Project Name"
                            ),
                        }
                    )
                    # Update header label to reflect new log
                    self.header_access.update_test_log_label()

            self.wait_window(
                ConfirmWindow(
                    self,
                    self.discon_btn_st,
                    self.run_multiple_bands,
                )
            )
            self.enable_buttons()

    def run_multiple_bands(self):
        self.saved_files = []
        self.disable_buttons()
        self.ori_dropdown.configure(state="disabled")
        band_ori_full = "" if self.ori_var.get() == "None" else self.ori_var.get()
        band_ori = band_ori_full[0].lower() if band_ori_full else ""
        num_bands = len(self.band_keys)
        sweep_dur = read_settings_from_file()["-SWEEP DUR-"]
        self.is_cancel = False

        # Now grid it (show it), then fill it
        self.frame3.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        self.fill_frame3(self.frame3)

        # updates progress bar to reset
        self.pbar.set(0)
        self.pbar_label.configure(text=f"0/{num_bands}")
        self.update_idletasks()

        for i in range(num_bands):
            if self.is_cancel:
                self.pbar.stop()
                break

            band_key = self.band_keys[i]
            run_note = self.run_note_var.get()

            _, self.run_filename = get_run_filename(
                self.inst, band_key, run_note, sweep_dur, band_ori
            )
            run_band(
                self.inst,
                band_key,
                self.run_filename,
                band_ori,
                run_note,
                self.current_test_log,
            )

            # Mark checkbox complete
            checkbox, check_var = self.band_checkbox[band_key]
            check_var.set(True)

            # SHOW SAVED FILES
            saved_csv = f"{self.run_filename}.csv"
            saved_png = f"{self.run_filename}.png"

            self.saved_files.append(saved_csv)
            self.saved_files.append(saved_png)
            self.update_idletasks()

            # PROGRESS BAR
            progress = (i + 1) / num_bands
            self.pbar.set(progress)
            self.pbar_label.configure(text=f"{i + 1}/{num_bands}")

            self.update_idletasks()

            self.run_filename = None

        # RUNS COMPLETE
        self.pbar.stop()
        autosa_logger.debug("Multi Band Mode: Completed and saved measurements.")
        CompletedWindow(self)
        self.band_checkbox.clear()
        self.band_filenames.clear()
        self.frame3.grid_forget()  # hide the frame after completion, .destroy() doesn't work here
        self.run_filename = None
        self.after(1, self.enable_buttons())
        self.after(1, self.update_ori_dropdown())
