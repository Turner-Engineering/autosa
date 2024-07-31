import threading
import customtkinter as ctk
from ui.save_window_popups import CompletedWindow, PopupWindow
from utils.settings import read_settings_from_file
from ui.get_resource_path import resource_path
from instrument.instrument import (
    get_run_filename,
    run_band,
)


class ConfirmWindow(ctk.CTkToplevel):
    def __init__(self, parent, run_multiple_bands):
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
        self.run_multiple_bands = run_multiple_bands
        self.create_widgets()

    def create_widgets(self):
        frame = self.init_frame()
        self.fill_frame(frame)

    def init_frame(self):
        frame = ctk.CTkFrame(self, fg_color="transparent")
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
        ctk.CTkButton(
            frame,
            text="Okay",
            command=lambda: self.confirmation_callback(),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        # Cancel Button
        ctk.CTkButton(
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
        band_ori = (
            "" if self.parent.ori_var.get() == "None" else self.parent.ori_var.get()
        )
        sweep_dur = read_settings_from_file()["-SWEEP DUR-"]
        run_id = "XYZ-AB"

        text = (
            "Please confirm that you would like to run bands\n"
            f"{band_range} ({run_count} runs total)\n"
            f"for {sweep_dur} seconds each\n"
            "and that the first filename should be:\n"
            f"{run_id} {run_note} B0{band_ori}\n"
            "(the rest will be numbered sequentially)"
        )
        return text

    def get_run_count(self, band_range):
        if band_range == "B0 - B4 (monopole)":
            run_count = 5
        elif band_range == "B5 - B7 (bilogical)":
            run_count = 3
        elif band_range == "B0 - B7 (calibration)":
            run_count = 8
        else:
            raise ValueError("Invalid band range")
        return run_count

    def confirmation_callback(self):
        # create new thread
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
        frame_color="transparent",
        label_color="transparent",
    ):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.frame_color = frame_color
        self.label_color = label_color

        self.settings = read_settings_from_file()
        self.state_folder = read_settings_from_file()["-STATE FOLDER-"]
        self.corr_folder = read_settings_from_file()["-CORR FOLDER-"]
        self.inst_output_folder = read_settings_from_file()["-INST OUT FOLDER-"]
        self.local_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

        self.band_ranges = [
            "B0 - B4 (monopole)",
            "B5 - B7 (bilogical)",
            "B0 - B7 (calibration)",
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

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()

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
            width=180,
        )
        self.ori_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky="w")
        self.update_ori_dropdown()

    def fill_frame2(self, frame2):
        # Run Button
        self.run_button = ctk.CTkButton(
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
        ctk.CTkButton(
            frame2,
            text="Cancel",
            command=lambda: self.update_cancel_status(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        ).grid(row=0, column=3, padx=5, pady=5, sticky="e")

    def update_ori_dropdown(self):
        """disables and enables the orientation based on the selected range"""
        band_range = self.band_range_var.get()
        if band_range == "B5 - B7 (bilogical)":
            self.ori_dropdown.configure(state="normal")
            self.ori_dropdown.set("Horizontal")
        else:
            self.ori_dropdown.configure(state="disabled")
            self.ori_dropdown.set("None")

    def update_cancel_status(self):
        self.is_cancel = True

    def call_update_band_keys(self, *args):
        self.update_band_keys()

    def update_band_keys(self):
        band_range = self.band_range_var.get()

        if band_range == "B0 - B4 (monopole)":
            self.band_keys = self.bands[:5]
        elif band_range == "B5 - B7 (bilogical)":
            self.band_keys = self.bands[5:]
        elif band_range == "B0 - B7 (calibration)":
            self.band_keys = self.bands
        else:
            self.band_keys = []

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
            self.disable_buttons()
            self.wait_window(PopupWindow(self))
            self.enable_buttons()
        else:
            self.disable_buttons()
            self.wait_window(ConfirmWindow(self, self.run_multiple_bands))
            self.enable_buttons()

    def run_multiple_bands(self):
        self.disable_buttons()
        self.ori_dropdown.configure(state="disabled")
        band_ori = "" if self.ori_var.get() == "None" else self.ori_var.get()
        num_bands = len(self.band_keys)
        self.is_cancel = False

        # PROGRESS BAR
        run_times = 1 / num_bands
        prog_step = run_times

        # updates progress bar to reset
        self.pbar.set(0)
        self.pbar_label.configure(text=f"0/{num_bands}")
        self.update_idletasks()
        self.pbar.start()

        for i in range(num_bands):
            if self.is_cancel:
                self.pbar.stop()
                break

            band_key = self.band_keys[i]
            run_note = self.run_note_var.get()

            self.run_filename = get_run_filename(
                self.inst, band_key, run_note, band_ori
            )
            run_band(self.inst, band_key, self.run_filename)

            # PROGRESS BAR
            self.pbar.set(prog_step)
            self.pbar_label.configure(text=f"{i+1}/{num_bands}")

            prog_step += run_times
            self.update_idletasks()

            self.run_filename = None

        # RUNS COMPLETE
        self.pbar.stop()
        CompletedWindow(self)
        self.run_filename = None
        self.after(1, self.enable_buttons())
        self.after(1, self.update_ori_dropdown())
