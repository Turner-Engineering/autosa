import customtkinter as ctk
from ui.save_window_popups import CompletedWindow, PopupWindow
from ui.large_button import LargeButton
from utils.settings import read_settings_from_file
from instrument.instrument import (
    get_run_filename,
    run_band,
    save_trace_and_screen,
)


class SingleModeFrame(ctk.CTkFrame):
    def __init__(
        self,
        parent,
        inst_found,
        inst,
        frame_color="transparent",
        label_color="transparent",
    ):
        super().__init__(parent)
        self.button_padding = 4
        self.columnconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.frame_color = frame_color
        self.label_color = label_color

        self.settings = read_settings_from_file()
        self.state_folder = self.settings["-STATE FOLDER-"]
        self.corr_folder = self.settings["-CORR FOLDER-"]
        self.inst_output_folder = self.settings["-INST OUT FOLDER-"]
        self.local_folder = self.settings["-LOCAL OUT FOLDER-"]

        self.is_paused = True
        self.run_filename = None
        self.run_note_var = ctk.StringVar()

        self.button_list = []
        self.band_buttons = [
            ("B0", lambda: self.check_and_run("B0"), 1, 0),
            ("B1", lambda: self.check_and_run("B1"), 1, 1),
            ("B2", lambda: self.check_and_run("B2"), 1, 2),
            ("B3", lambda: self.check_and_run("B3"), 1, 3),
            ("B4", lambda: self.check_and_run("B4"), 1, 4),
            ("B5h", lambda: self.check_and_run("B5h"), 2, 1),
            ("B6h", lambda: self.check_and_run("B6h"), 2, 2),
            ("B7h", lambda: self.check_and_run("B7h"), 2, 3),
            ("B5v", lambda: self.check_and_run("B5v"), 3, 1),
            ("B6v", lambda: self.check_and_run("B6v"), 3, 2),
            ("B7v", lambda: self.check_and_run("B7v"), 3, 3),
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
            width=80,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.run_note_entry = ctk.CTkEntry(
            frame,
            textvariable=self.run_note_var,
            width=300,
        )
        self.run_note_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    # FRAME 2: Button Frame
    def fill_frame2(self, frame):
        ctk.CTkLabel(
            frame,
            text="Prepare, Record, and Save:",
            fg_color=self.label_color,
        ).grid(row=0, column=0, padx=5, pady=5, columnspan=5, sticky="w")

        inner_frame = ctk.CTkFrame(frame)
        inner_frame.grid(row=1, column=0, padx=0, pady=0)

        for band_key, cmd, r, c in self.band_buttons:
            button = LargeButton(
                inner_frame,
                text=band_key,
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
        if self.run_note_var.get().strip() == "":
            self.disable_buttons()
            self.wait_window(PopupWindow(self))
            self.enable_buttons()
        else:
            self.disable_buttons()
            self.after(100, lambda: self.run_single_band(band_name))

    def run_single_band(self, band_name):
        # PREPARE, RECORD, ADJUST
        band_key = band_name[:2]
        error_message = run_band(self.inst, band_key, "", save=False)

        # GET FILENAME
        run_note = self.run_note_var.get()
        self.run_filename = get_run_filename(self.inst, band_name, run_note)

        # SAVE
        if self.run_filename != None:
            save_trace_and_screen(
                self.inst, self.run_filename, self.inst_output_folder, self.local_folder
            )

        # AFTER RUN
        CompletedWindow(self)
        self.run_filename = None
        self.enable_buttons()

        return error_message
