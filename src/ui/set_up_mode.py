import threading

import customtkinter as ctk

from instrument.folders import get_folder_info
from instrument.instrument import (
    get_ref_level,
    get_state_file,
    prep_band,
    set_rounded_ref_level,
    update_state,
)
from ui.get_resource_path import resource_path
from ui.ui_logger import ArrowButton, LargeButton, LoggingButton, LoggingTopLevel
from utils.logger import autosa_logger
from utils.settings import read_settings_from_file


class ConfirmStateChangePopup(LoggingTopLevel):
    def __init__(
        self,
        parent,
        update_ref_level,
        state_filename,
        warning_red,
        hover_red,
    ):
        super().__init__(parent)
        self.title("Confirm State Update")
        self.parent = parent
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.warning_red = warning_red
        self.hover_red = hover_red
        self.backgroud_gray = "#DBDBDB"
        self.configure(fg_color=self.backgroud_gray)
        self.resizable(False, False)  # disable resizing
        self.transient(parent)

        self.update_ref_level = update_ref_level
        self.state_filename = state_filename

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.backgroud_gray)
        frame1.grid(row=0, column=0, padx=10)
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.backgroud_gray)
        frame2.grid(row=1, column=0, padx=10)
        return frame2

    def fill_frame1(self, frame1):
        # Warning Symbol
        ctk.CTkLabel(
            frame1,
            text="\u26a0",
            anchor="center",
            font=("Arial", 48),
            text_color="#dc9908",
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Confirmation Text
        ctk.CTkLabel(
            frame1,
            text="Are You Sure?",
            justify="center",
            font=("", 24),
        ).grid(row=1, column=0, columnspan=2, padx=5, sticky="nsew")

        # Confirmation Text
        ctk.CTkLabel(frame1, text="This will overwrite ", font=("", 14)).grid(
            row=2, column=0, sticky="e"
        )

        ctk.CTkLabel(
            frame1, text=f"{self.state_filename}", font=("", 14, "underline")
        ).grid(row=2, column=1, sticky="w")

        ctk.CTkLabel(
            frame1,
            text="This cannot be reversed!",
            justify="center",
            font=("", 14),
        ).grid(row=3, column=0, columnspan=2, padx=5, sticky="nsew")

    def fill_frame2(self, frame2):
        # Okay Button
        LoggingButton(
            frame2,
            text="Overwrite",
            command=lambda: self.confirmation_callback(),
            anchor="center",
            fg_color=self.warning_red,
            hover_color=self.hover_red,
        ).grid(row=0, column=0, padx=5, pady=5)

        # Cancel Button
        LoggingButton(
            frame2,
            text="Cancel",
            command=lambda: self.overwrite_canceled(),
            anchor="center",
            fg_color="#939ba2",
            hover_color="#585656",
        ).grid(row=0, column=1, padx=5, pady=5)

    def confirmation_callback(self):
        # create new thread
        autosa_logger.info(f"State File {self.state_filename} overwritten.")
        self.destroy()  # close confirm window
        new_thread = threading.Thread(target=self.update_ref_level, daemon=True)
        new_thread.start()

    def overwrite_canceled(self):
        autosa_logger.info(f"State File {self.state_filename} overwrite canceled.")
        self.destroy()


class SetUpModeFrame(ctk.CTkFrame):
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
        self.inst_found = inst_found
        self.inst = inst
        self.discon_btn_st = discon_btn_st
        self.frame_color = frame_color
        self.label_color = label_color

        self.button_list = []
        self.ref_level_double_var = ctk.DoubleVar()
        self.ref_level_double_var.set(get_ref_level(self.inst))
        self.band_selected_var = ctk.StringVar()
        self.state_filename_var = ctk.StringVar()
        self.warning_red = "#8F0202"
        self.hover_red = "#350303"

        self.band_buttons = [
            ("B0", self.discon_btn_st, lambda: self.setup_files("B0"), 1, 0),
            ("B1", self.discon_btn_st, lambda: self.setup_files("B1"), 1, 1),
            ("B2", self.discon_btn_st, lambda: self.setup_files("B2"), 1, 2),
            ("B3", self.discon_btn_st, lambda: self.setup_files("B3"), 1, 3),
            ("B4", self.discon_btn_st, lambda: self.setup_files("B4"), 1, 4),
            ("B5", self.discon_btn_st, lambda: self.setup_files("B5"), 2, 1),
            ("B6", self.discon_btn_st, lambda: self.setup_files("B6"), 2, 2),
            ("B7", self.discon_btn_st, lambda: self.setup_files("B7"), 2, 3),
        ]

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()
        frame3 = self.init_frame3()
        frame4 = self.init_frame4()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)
        self.fill_frame3(frame3)
        self.fill_frame4(frame4)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        return frame2

    def init_frame3(self):
        frame3 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame3.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        frame3.columnconfigure(0, weight=1)
        return frame3

    def init_frame4(self):
        frame4 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame4.grid(row=3, column=0, padx=5, pady=5, sticky="ew")
        frame4.columnconfigure(0, weight=1)
        return frame4

    # FRAME 1: LAST BAND
    def fill_frame1(self, frame1):
        ctk.CTkLabel(
            frame1,
            text="Recall State File:",
            fg_color=self.label_color,
            width=80,
            anchor="w",
        ).grid(row=0, column=0, padx=5, pady=5, sticky="ew")

        self.last_band_prepped = ctk.CTkLabel(
            frame1,
            text="[Last State Recalled]",
            fg_color=self.label_color,
        )
        self.last_band_prepped.grid(row=0, column=1, padx=5, sticky="w")

    # FRAME 2: BAND BUTTONS
    def fill_frame2(self, frame2):
        inner_frame = ctk.CTkFrame(frame2)
        inner_frame.grid(row=0, column=0, padx=0, pady=0)

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

    # FRAME 3: EDIT STATE
    def fill_frame3(self, frame3):
        ctk.CTkLabel(
            frame3,
            text="Ref Level:",
            fg_color=self.label_color,
        ).grid(row=0, column=0, padx=5)

        # Inner Button Frame for Ref Level Controls
        ref_button_frame = ctk.CTkFrame(frame3)
        ref_button_frame.grid(row=1, column=0, pady=5)

        self.increase_ref_button = ArrowButton(
            ref_button_frame,
            text="\u25b2",
            log_label="Increase Ref Level",
            state=self.discon_btn_st,
            command=lambda: self.increse_ref_level(),
        )
        self.increase_ref_button.pack(side="left", padx=5)

        self.cur_ref_level_label = ctk.CTkLabel(
            ref_button_frame,
            text=f"{self.ref_level_double_var.get():.2f} dBm",
            text_color="black",
            width=50,
            anchor="center",
        )
        self.cur_ref_level_label.pack(side="left", padx=5)

        self.decrease_ref_button = ArrowButton(
            ref_button_frame,
            text="\u25bc",
            log_label="Decrease Ref Level",
            state=self.discon_btn_st,
            command=lambda: self.decrese_ref_level(),
        )
        self.decrease_ref_button.pack(side="left", padx=5)
        # self.match_ref_level()

    # FRAME 4: UPDATE Button
    def fill_frame4(self, frame4):
        self.update_button = LoggingButton(
            frame4,
            text="Update State",
            font=("", 16),
            fg_color=self.warning_red,
            hover_color=self.hover_red,
            width=150,
            height=50,
            command=lambda: self.confirm_window(),
        )
        self.update_button.grid(row=0, column=0, padx=5, pady=5)
        self.update_button.configure(state=self.is_state_folder_valid())

    def setup_files(self, band_key):
        self.band_selected_var.set(band_key)
        self.last_band_prepped.configure(text=band_key)
        self.state_filename_var = get_state_file(
            self.inst, read_settings_from_file()["-STATE FOLDER-"], band_key
        )
        prep_band(self.inst, self.band_selected_var.get())
        autosa_logger.debug(f"Recalled State: {self.state_filename_var}")

        updated_ref_level = get_ref_level(self.inst)
        self.ref_level_double_var.set(updated_ref_level)
        self.update_ref_level_label(updated_ref_level)

    def decrese_ref_level(self):
        self.update_autosa_ref_level()

        decresed_ref = self.ref_level_double_var.get() - 10
        decresed_ref_rounded = round(decresed_ref / 10) * 10

        self.ref_level_double_var.set(decresed_ref_rounded)
        set_rounded_ref_level(self.inst, decresed_ref_rounded)
        self.update_ref_level_label(decresed_ref_rounded)

        autosa_logger.info(f"Decreased ref level to {decresed_ref_rounded} dBm")

    def increse_ref_level(self):
        self.update_autosa_ref_level()

        increased_ref = self.ref_level_double_var.get() + 10
        incresed_ref_rounded = round(increased_ref / 10) * 10

        self.ref_level_double_var.set(incresed_ref_rounded)
        set_rounded_ref_level(self.inst, incresed_ref_rounded)
        self.update_ref_level_label(incresed_ref_rounded)

        autosa_logger.info(f"Increased ref level to {incresed_ref_rounded} dBm")

    def confirm_window(self):
        autosa_logger.debug(
            f"State File {self.state_filename_var} overwrite initiated."
        )
        self.wait_window(
            ConfirmStateChangePopup(
                self,
                self.update_ref_level,
                self.state_filename_var,
                self.warning_red,
                self.hover_red,
            )
        )

    def update_ref_level(self):
        state_folder = read_settings_from_file()["-STATE FOLDER-"]
        self.state_filename_var = get_state_file(
            self.inst, state_folder, self.band_selected_var.get()
        )
        update_state(self.inst, state_folder, self.state_filename_var)

    def update_ref_level_label(self, updated_ref_level):
        self.cur_ref_level_label.configure(text=f"{updated_ref_level:.2f} dBm")

    def is_state_folder_valid(self):
        state_folder = read_settings_from_file()["-STATE FOLDER-"]
        state_exists, _, _ = get_folder_info(self.inst, state_folder)
        return "normal" if state_exists else "disabled"

    def update_state_button(self):
        if hasattr(self, "update_button"):
            new_state = self.is_state_folder_valid()
            self.update_button.configure(state=new_state)

    def update_autosa_ref_level(self):
        # check to see if ref level on autosa matches the ref level on the instrument
        # if not, update autosa ref level to match the screens instrument
        cur_ref_level = self.ref_level_double_var.get()
        inst_ref_level = get_ref_level(self.inst)

        if cur_ref_level != inst_ref_level:
            self.ref_level_double_var.set(inst_ref_level)
            self.update_ref_level_label(inst_ref_level)

    """"
    If any changes are made to the ref level on the instrument, match_ref_level() updates it on Autosa. 
    Currently, this function cannot be used. 

    If release_inst(self.inst):
    - is used, the instrument is released every second which can interfere with testing 
      and unsure how release acts with the instrument

    - is not used but function is used, the instrument is very difficult to release 
      even with Release Tab and esc button. This is because this function updates every second.

    To use, uncomment line 261 and the function below.
    """
    #
    # def match_ref_level(self, update_time=1000):
    #     cur_ref_level = get_ref_level(self.inst)
    #     if cur_ref_level != self.ref_level_double_var.get():
    #         self.ref_level_double_var.set(cur_ref_level)
    #         self.cur_ref_level_label.configure(text=f"{cur_ref_level:.2f} dBm")

    #     release_inst(self.inst)

    #     self.after(update_time, self.match_ref_level, update_time)
