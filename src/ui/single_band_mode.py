import customtkinter as ctk

from instrument.instrument import (
    get_run_filename,
    run_band,
    save_trace_and_screen,
)
from ui.save_window_popups import NoRunNoteWindow, SBMCompletedWindow
from ui.ui_logger import LargeButton
from utils.logger import autosa_logger
from utils.settings import read_settings_from_file


class SingleModeFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        inst_found,
        inst,
        discon_btn_st,
        frame_color,
        label_color,
    ):
        super().__init__(parent)
        self.button_padding = 4
        self.columnconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.discon_btn_st = discon_btn_st
        self.frame_color = frame_color
        self.label_color = label_color

        self.is_paused = True
        self.run_filename = None
        self.run_note_var = ctk.StringVar()

        self.button_list = []
        self.band_buttons = [
            ("B0", self.discon_btn_st, lambda: self.check_and_run("B0"), 1, 0),
            ("B1", self.discon_btn_st, lambda: self.check_and_run("B1"), 1, 1),
            ("B2", self.discon_btn_st, lambda: self.check_and_run("B2"), 1, 2),
            ("B3", self.discon_btn_st, lambda: self.check_and_run("B3"), 1, 3),
            ("B4", self.discon_btn_st, lambda: self.check_and_run("B4"), 1, 4),
            ("B5h", self.discon_btn_st, lambda: self.check_and_run("B5h"), 2, 1),
            ("B6h", self.discon_btn_st, lambda: self.check_and_run("B6h"), 2, 2),
            ("B7h", self.discon_btn_st, lambda: self.check_and_run("B7h"), 2, 3),
            ("B5v", self.discon_btn_st, lambda: self.check_and_run("B5v"), 3, 1),
            ("B6v", self.discon_btn_st, lambda: self.check_and_run("B6v"), 3, 2),
            ("B7v", self.discon_btn_st, lambda: self.check_and_run("B7v"), 3, 3),
        ]

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
        frame2.columnconfigure(0, weight=1)
        return frame2

    # FRAME 1: header and run note
    def fill_frame1(self, frame):
        ctk.CTkLabel(
            frame,
            text="Run Note: ",
            fg_color=self.label_color,
            width=100,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.run_note_entry = ctk.CTkEntry(
            frame,
            textvariable=self.run_note_var,
            width=300,
        )
        self.run_note_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(
            frame,
            text="Selected Band: ",
            fg_color=self.label_color,
            width=100,
            anchor="w",
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.last_band_prepped = ctk.CTkLabel(
            frame,
            text="[Selected Band]",
            fg_color=self.label_color,
            width=300,
            anchor="w",
        )
        self.last_band_prepped.grid(row=1, column=1, padx=5, pady=5, sticky="w")

    # FRAME 2: Button Frame
    def fill_frame2(self, frame):
        ctk.CTkLabel(
            frame,
            text="Prepare, Record, and Save:",
            fg_color=self.label_color,
        ).grid(row=0, column=0, padx=5, pady=5, columnspan=5, sticky="w")

        inner_frame = ctk.CTkFrame(frame)
        inner_frame.grid(row=1, column=0, padx=0, pady=0)

        for band_key, st, cmd, r, c in self.band_buttons:
            button = LargeButton(
                inner_frame,
                text=band_key,
                state=st,
                command=cmd,
            )
            button.grid(
                row=r, column=c, padx=self.button_padding, pady=self.button_padding
            )
            self.button_list.append(button)

    def disable_buttons(self):
        for button in self.button_list:
            button.configure(state="disabled")
        self.run_note_entry.configure(state="disabled")

    def enable_buttons(self):
        for button in self.button_list:
            button.configure(state="normal")
        self.run_note_entry.configure(state="normal")

    # Functions
    def check_and_run(self, band_name):
        self.last_band_prepped.configure(text=band_name)
        if self.run_note_var.get().strip() == "":
            autosa_logger.info("Single Band Mode: No Run Note was entered.")
            self.disable_buttons()
            self.wait_window(NoRunNoteWindow(self))
            self.enable_buttons()
        else:
            self.disable_buttons()
            self.after(100, lambda: self.run_single_band(band_name))

    def run_single_band(self, band_name):
        # PREPARE, RECORD, ADJUST
        band_key = band_name[:2]
        band_ori = band_name[2] if len(band_name) == 3 else ""
        run_note = self.run_note_var.get()

        error_message = run_band(
            self.inst, band_key, "", band_ori, run_note, save=False
        )

        # GET FILENAME
        settings = read_settings_from_file()
        sweep_dur = settings["-SWEEP DUR-"]
        _, self.run_filename = get_run_filename(
            self.inst, band_name, run_note, sweep_dur
        )

        inst_output_folder = settings["-INST OUT FOLDER-"]
        local_folder = settings["-LOCAL OUT FOLDER-"]

        # SAVE
        if self.run_filename is not None:
            save_trace_and_screen(
                self.inst,
                self.run_filename,
                inst_output_folder,
                local_folder,
                band_name,
                run_note,
                sweep_dur,
            )

        # AFTER RUN
        SBMCompletedWindow(self, band_name, self.run_filename)
        self.run_filename = None
        self.enable_buttons()

        return error_message
