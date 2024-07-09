import customtkinter as ctk
from PIL import Image

from ui.large_button import LargeButton


class ManualModeFrame(ctk.CTkFrame):
    def __init__(self, parent, frame_color="transparent", label_color="transparent"):
        super().__init__(parent)
        self.button_padding = 4
        self.frame_color = frame_color
        self.label_color = label_color
        self.parent = parent
        self.columnconfigure(0, weight=1)

        self.band_buttons = [
            ("B0", lambda: print("B0"), 1, 0),
            ("B1", lambda: print("B1"), 1, 1),
            ("B2", lambda: print("B2"), 1, 2),
            ("B3", lambda: print("B3"), 1, 3),
            ("B4", lambda: print("B4"), 1, 4),
            ("B5", lambda: print("B5"), 2, 1),
            ("B6", lambda: print("B6"), 2, 2),
            ("B7", lambda: print("B7"), 2, 3),
        ]

        self.measure_buttons = [
            # ("./images/pause.png", lambda: print("pause button"), "#f64242", "#c33434"),
            ("./images/play.png", lambda: print("play button"), "#2ecf4f", "#229c3b"),
            ("./images/reset.png", lambda: print("reset button"), "#58c4db", "#4396a7"),
            ("./images/save.png", lambda: print("save button"), "#a165cf", "#794c9c"),
        ]

        self.create_widgets()

    def create_widgets(self):
        # kind of subjective, but "get" functions should "get" something and return it
        # these functions aren't getting things, they're creating things
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
            LargeButton(
                inner_frame,
                text=band_key,
                command=cmd,
            ).grid(row=r, column=c, padx=self.button_padding, pady=self.button_padding)

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

            LargeButton(
                button_frame,
                text="",
                image=image,
                command=cmd,
                height=60,
                fg_color=fg_color,
                hover_color=hover_color,
            ).grid(row=4, column=c, padx=self.button_padding, pady=self.button_padding)

        ctk.CTkLabel(
            frame2,
            text="0.0 s",
            fg_color=self.label_color,
            font=("", 48),
        ).grid(row=1, column=1, sticky="w")

    def fill_frame3(self, frame3):
        """3rd frame is the time and band information"""

        ctk.CTkLabel(
            frame3,
            text="Last Start Time: ",
            fg_color=self.label_color,
        ).grid(row=1, column=0, padx=5, sticky="w")

        ctk.CTkLabel(
            frame3,
            text="[Last Start Time]",
            fg_color=self.label_color,
        ).grid(row=1, column=1, padx=5, sticky="w")

        ctk.CTkLabel(
            frame3,
            text="Last Band Prepared: ",
            fg_color=self.label_color,
        ).grid(row=2, column=0, padx=5, sticky="w")

        ctk.CTkLabel(
            frame3,
            text="[Last Band Prepared]",
            fg_color=self.label_color,
        ).grid(row=2, column=1, padx=5, sticky="w")
