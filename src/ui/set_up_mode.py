import threading
import customtkinter as ctk
from ui.get_resource_path import resource_path
from ui.large_button import LargeButton
from utils.settings import read_settings_from_file
from instrument.instrument import (
    get_ref_level,
    set_ref_level,
    recall_state,
    get_state_file,
    update_state,
)


class ArrowButton(ctk.CTkButton):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(
            parent,
            *args,
            **kwargs,
        )
        self.configure(
            height=30, width=30, font=("", 16), text_color="black", anchor="center"
        )


class ConfirmStateChangePopup(ctk.CTkToplevel):
    def __init__(self, parent, update_ref_level, state_filename):
        super().__init__(parent)
        self.title("Confirm State Update")
        self.parent = parent
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.window_color = "#8F0202"
        self.configure(fg_color=self.window_color)
        self.resizable(False, False)  # disable resizing
        self.transient(parent)

        self.update_ref_level = update_ref_level
        self.state_filename = state_filename

        self.create_widgets()

    def create_widgets(self):
        frame = self.init_frame()
        self.fill_frame(frame)

    def init_frame(self):
        frame = ctk.CTkFrame(self, fg_color=self.window_color)
        frame.grid(row=0, column=0, padx=10, pady=10)
        frame.columnconfigure([0, 1], weight=1)
        frame.rowconfigure([0, 1, 2], weight=1)
        return frame

    def fill_frame(self, frame):
        # Warning Symbol
        ctk.CTkLabel(
            frame,
            text="\u26a0 \u26a0 \u26a0",
            anchor="center",
            font=("Arial", 24, "bold"),
            text_color="#ffcc00",
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Confirmation Text
        ctk.CTkLabel(
            frame,
            text="Please confirm that you would like to overwrite",
            justify="center",
            font=("", 14),
            text_color="white",
        ).grid(row=1, column=0, columnspan=2, padx=5, sticky="nsew")

        ctk.CTkLabel(
            frame,
            text=f"{self.state_filename}",
            justify="center",
            font=("", 16, "bold"),
            text_color="white",
        ).grid(row=2, column=0, columnspan=2, padx=5, sticky="nsew")

        ctk.CTkLabel(
            frame,
            # text="This will overwrite the state file and cannot be reversed.",
            text="This cannot be reversed.",
            justify="center",
            font=("", 14),
            text_color="white",
        ).grid(row=3, column=0, columnspan=2, padx=5, sticky="nsew")

        # Okay Button
        ctk.CTkButton(
            frame,
            text="Overwrite",
            command=lambda: self.confirmation_callback(),
            anchor="center",
        ).grid(row=4, column=0, padx=5, pady=5)

        # Cancel Button
        ctk.CTkButton(
            frame,
            text="Cancel",
            command=lambda: self.destroy(),
            fg_color="#939ba2",
            hover_color="#646a6e",
            anchor="center",
        ).grid(row=4, column=1, padx=5, pady=5)

        # pop up a scary dialog to confirm the ref level update will overwrite the current state
        # are you sure you want to update [dropdown] state file? make the band changeable

    def confirmation_callback(self):
        # create new thread
        self.destroy()  # close confirm window
        new_thread = threading.Thread(target=self.update_ref_level, daemon=True)
        new_thread.start()


class SetUpModeFrame(ctk.CTkFrame):
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
        self.inst_found = inst_found
        self.inst = inst
        self.frame_color = frame_color
        self.label_color = label_color

        self.state_folder = read_settings_from_file()["-STATE FOLDER-"]
        self.button_list = []

        self.ref_level_double_var = ctk.DoubleVar()
        self.ref_level_double_var.set(get_ref_level(self.inst))
        self.band_selected = ctk.StringVar()
        self.state_filename = ctk.StringVar()

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

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()
        # frame3 = self.init_frame3()
        frame4 = self.init_frame4()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)
        # self.fill_frame3(frame3)
        self.fill_frame4(frame4)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        return frame2

    # def init_frame3(self):
    #     frame3 = ctk.CTkFrame(self, fg_color=self.frame_color)
    #     frame3.grid(row=2, column=0, padx=5, pady=5, sticky="w")
    #     return frame3

    def init_frame4(self):
        frame4 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame4.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
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

    # FRAME 3: EDIT STATE
    # def fill_frame3(self, frame3):
    #     ctk.CTkLabel(
    #         frame3,
    #         text="Ref Level:",
    #         fg_color=self.label_color,
    #     ).grid(row=0, column=0, padx=5, sticky="w")

    #     # Inner Button Frame for Ref Level Controls
    #     ref_button_frame = ctk.CTkFrame(frame3)
    #     ref_button_frame.grid(row=1, column=0, columnspan=3, pady=5, sticky="w")

    #     self.decrease_ref_button = ArrowButton(
    #         ref_button_frame,
    #         text="\u25BC",
    #         command=lambda: self.decrese_ref_level()
    #     )
    #     self.decrease_ref_button.pack(side="left", padx=5)

    #     self.cur_ref_level_label = ctk.CTkLabel(
    #         ref_button_frame,
    #         text=f"{self.ref_level_double_var.get():.2f} dBm",
    #         text_color="black",
    #         width=50,
    #         anchor="center"
    #     )
    #     self.cur_ref_level_label.pack(side="left", padx=5)

    #     self.increase_ref_button = ArrowButton(
    #         ref_button_frame,
    #         text="\u25B2",
    #         command=lambda: self.increse_ref_level()
    #     )
    #     self.increase_ref_button.pack(side="left", padx=5)

    # FRAME 4: UPDATE Button
    def fill_frame4(self, frame4):
        self.update_button = ctk.CTkButton(
            frame4,
            text="Update State",
            font=("", 16),
            fg_color="#A90404",
            hover_color="#5B0404",
            width=150,
            height=50,
            command=lambda: self.confirm_window(),
        )
        self.update_button.grid(row=0, column=0, padx=5, pady=5)

    def setup_files(self, band_key):
        self.band_selected = band_key
        self.last_band_prepped.configure(text=self.band_selected)
        self.update_button.configure(text=f"Update State {self.band_selected}")

        self.state_filename = get_state_file(
            self.inst, self.state_folder, self.band_selected
        )
        recall_state(self.inst, self.state_folder, self.state_filename)

        updated_ref_level = get_ref_level(self.inst)
        self.ref_level_double_var.set(updated_ref_level)
        self.cur_ref_level_label.configure(text=f"{updated_ref_level:.2f} dBm")

    def decrese_ref_level(self):
        # check to see if ref level on autosa matches the ref level on the instrument
        # if not, update autosa ref level to match the screens instrument
        cur_rev_level = self.ref_level_double_var.get()
        if cur_rev_level != get_ref_level(self.inst):
            self.ref_level_double_var.set(get_ref_level(self.inst))
            cur_rev_level = self.ref_level_double_var.get()

        decresed_ref = self.ref_level_double_var.get() - 10
        self.ref_level_double_var.set(decresed_ref)
        set_ref_level(self.inst, decresed_ref)
        self.cur_ref_level_label.configure(text=f"{decresed_ref:.2f} dBm")

    def increse_ref_level(self):
        increased_ref = self.ref_level_double_var.get() + 10
        self.ref_level_double_var.set(increased_ref)
        set_ref_level(self.inst, increased_ref)
        self.cur_ref_level_label.configure(text=f"{increased_ref:.2f} dBm")

    def confirm_window(self):
        self.wait_window(
            ConfirmStateChangePopup(self, self.update_ref_level, self.state_filename)
        )

    def update_ref_level(self):
        print(f"Updating state file {self.band_selected}...")
        self.state_filename = get_state_file(
            self.inst, self.state_folder, self.band_selected
        )
        print(f"State folder: {self.state_folder}")
        print(f"State filename: {self.state_filename}")
        print(f"saving state to {self.state_folder}/{self.state_filename}")
        update_state(self.inst, self.state_folder, self.state_filename)
