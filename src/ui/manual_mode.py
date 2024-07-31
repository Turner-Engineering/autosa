import time
import customtkinter as ctk
from PIL import Image

from ui.large_button import LargeButton
from utils.stopwatch import Stopwatch
from ui.save_window_popups import ManualSaveWindow
from ui.get_resource_path import resource_path
from utils.settings import read_settings_from_file
from instrument.instrument import (
    get_run_id,
    prep_band,
    save_trace_and_screen,
)


class ManualModeFrame(ctk.CTkFrame):
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
        self.stopwatch = Stopwatch()

        self.state_folder = read_settings_from_file()["-STATE FOLDER-"]
        self.corr_folder = read_settings_from_file()["-CORR FOLDER-"]
        self.inst_output_folder = read_settings_from_file()["-INST OUT FOLDER-"]
        self.local_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

        self.is_paused = True
        self.run_filename = None

        self.button_list = []
        self.measure_button_imgs = []
        self.pause_img = resource_path("./images/pause.png")
        self.play_img = resource_path("./images/play.png")

        self.band_buttons = [
            ("B0", lambda: self.setup_files("B0"), 1, 0),
            ("B1", lambda: self.setup_files("B1"), 1, 1),
            ("B2", lambda: self.setup_files("B2"), 1, 2),
            ("B3", lambda: self.setup_files("B3"), 1, 3),
            ("B4", lambda: self.setup_files("B4"), 1, 4),
            ("B5", lambda: self.setup_files("B5"), 2, 1),
            ("B6", lambda: self.setup_files("B6"), 2, 2),
            ("B7", lambda: self.setup_files("B7"), 2, 3),
        ]

        self.measure_buttons = [
            (self.play_img, lambda: self.cont_toggle(), "#2ecf4f", "#229c3b"),
            (
                resource_path("./images/reset.png"),
                lambda: self.reset_stopwatch(),
                "#58c4db",
                "#4396a7",
            ),
            (
                resource_path("./images/save.png"),
                lambda: self.save_trace_screen(),
                "#a165cf",
                "#794c9c",
            ),
        ]

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()
        frame3 = self.init_frame3()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)
        self.fill_frame3(frame3)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        frame1.columnconfigure(0, weight=1)
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        frame2.columnconfigure([0, 1], weight=1)
        return frame2

    def init_frame3(self):
        frame3 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame3.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        frame3.columnconfigure([0, 1], weight=1)
        return frame3

    # FRAME 1: Prepare Band Frame
    def fill_frame1(self, frame1):
        """1st frame is the bands B0-B7"""

        ctk.CTkLabel(
            frame1,
            text="Prepare Band:",
            fg_color=self.label_color,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        inner_frame = ctk.CTkFrame(frame1)
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

    # FRAME 2: Record and Save Frame
    def fill_frame2(self, frame2):
        """2nd frame is the measurement buttons"""

        ctk.CTkLabel(
            frame2,
            text="Record and Save:",
            fg_color=self.label_color,
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        button_frame = ctk.CTkFrame(frame2)
        button_frame.grid(row=1, column=0, sticky="w")

        for c, (img, cmd, fg_color, hover_color) in enumerate(self.measure_buttons):
            image = ctk.CTkImage(
                light_image=Image.open(img),
                dark_image=Image.open(img),
                size=(30, 30),
            )

            button = LargeButton(
                button_frame,
                text="",
                image=image,
                command=cmd,
                height=60,
                fg_color=fg_color,
                hover_color=hover_color,
            )
            button.grid(
                row=4, column=c, padx=self.button_padding, pady=self.button_padding
            )

            self.measure_button_imgs.append(button)

        self.time_elapased = ctk.CTkLabel(
            frame2,
            text="0.0 s",
            fg_color=self.label_color,
            font=("", 48),
        )
        self.time_elapased.grid(row=1, column=1, sticky="w")

    def fill_frame3(self, frame3):
        """3rd frame is the time and band information"""

        ctk.CTkLabel(
            frame3,
            text="Last Start Time: ",
            fg_color=self.label_color,
        ).grid(row=1, column=0, padx=5, sticky="w")

        self.last_start_time = ctk.CTkLabel(
            frame3,
            text="[Last Start Time]",
            fg_color=self.label_color,
        )
        self.last_start_time.grid(row=1, column=1, padx=5, sticky="w")

        ctk.CTkLabel(
            frame3,
            text="Last Band Prepared: ",
            fg_color=self.label_color,
        ).grid(row=2, column=0, padx=5, sticky="w")

        self.last_band_prepped = ctk.CTkLabel(
            frame3,
            text="[Last Band Prepared]",
            fg_color=self.label_color,
        )
        self.last_band_prepped.grid(row=2, column=1, padx=5, sticky="w")

    def cont_toggle(self):
        inst_status_img = self.pause_img if self.is_paused else self.play_img
        inst_status_fg_color = "#f64242" if self.is_paused else "#2ecf4f"
        inst_status_hover_color = "#c33434" if self.is_paused else "#229c3b"

        change_button_img = ctk.CTkImage(
            light_image=Image.open(inst_status_img),
            dark_image=Image.open(inst_status_img),
            size=(30, 30),
        )

        self.measure_button_imgs[0].configure(
            image=change_button_img,
            fg_color=inst_status_fg_color,
            hover_color=inst_status_hover_color,
        )

        start_time = time.strftime("%I:%M:%S %p", time.localtime(time.time()))

        if self.is_paused:
            self.inst.write(":INIT:CONT ON")
            self.last_start_time.configure(text=start_time)
            self.stopwatch.start()
            self.disable_buttons("disabled")
        else:
            self.inst.write(":INIT:CONT OFF")
            self.stopwatch.stop()
            self.disable_buttons("normal")

        self.update_stopwatch_time()
        self.is_paused = not self.is_paused

    def setup_files(self, band_key):
        self.last_band_prepped.configure(text=band_key)
        prep_band(self.inst, band_key)
        self.stopwatch.reset()

    def update_stopwatch_time(self):
        self.time_elapased.configure(text=self.stopwatch.get_time_str())
        self.after(100, self.update_stopwatch_time)

    def reset_stopwatch(self):
        self.inst.write(":INIT:REST")
        self.stopwatch.reset()

    def save_trace_screen(self):
        run_id = get_run_id(self.inst, self.inst_output_folder)
        run_file = ManualSaveWindow(
            self,
            self.run_filename,
            self.inst,
            run_id,
            self.frame_color,
            self.label_color,
        )

        self.wait_window(run_file)
        self.run_filename = run_file.get_filename()

        if self.run_filename != None:
            save_trace_and_screen(
                self.inst, self.run_filename, self.inst_output_folder, self.local_folder
            )
            run_error_message = ""

        self.run_filename = None

    def disable_buttons(self, state):
        self.measure_colors = ["#58c4db", "#a165cf"]
        invalid_color = "#8f8f8f"

        for button in self.button_list:
            button.configure(state=state)

        if self.is_paused:
            for button in self.measure_button_imgs[1:]:
                button.configure(state=state, fg_color=invalid_color)
        else:
            for i, button in enumerate(self.measure_button_imgs[1:]):
                button.configure(state=state, fg_color=self.measure_colors[i])
