from PIL import Image
import customtkinter as ctk


class ManualModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.button_padding = 5
        self.columnconfigure(0, weight=1)
        self.configure(border_width=2)
        self.create_widgets()

    def create_widgets(self):
        self.get_button_frame()
        self.get_measure_frame()
        self.get_time_frame()

    # FRAME 1: Buttons
    def get_button_frame(self):
        """1st frame is the bands B0-B7"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        button_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)

        tab1_header = ctk.CTkLabel(button_frame, text="Prepare Band:")
        tab1_header.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        band_buttons = [
            ("B0", lambda: print("B0"), 1, 0),
            ("B1", lambda: print("B1"), 1, 1),
            ("B2", lambda: print("B2"), 1, 2),
            ("B3", lambda: print("B3"), 1, 3),
            ("B4", lambda: print("B4"), 1, 4),
            ("B5", lambda: print("B5"), 2, 1),
            ("B6", lambda: print("B6"), 2, 2),
            ("B7", lambda: print("B7"), 2, 3),
        ]

        for band, cmd, r, c in band_buttons:
            band_button = ctk.CTkButton(button_frame, text=band, command=cmd)
            band_button.grid(row=r, column=c, padx=2, pady=2)

    # FRAME 2: Measurement Buttons
    def get_measure_frame(self):
        """2nd frame is the measurement buttons"""
        measurement_frame = ctk.CTkFrame(self, fg_color="transparent")
        measurement_frame.grid(row=1, column=0, padx=10, pady=10, sticky="W")

        tab1_measure_header = ctk.CTkLabel(measurement_frame, text="Record and Save:")
        tab1_measure_header.grid(row=3, column=0, padx=2, pady=2, sticky="W")

        measure_ctrl = [
            ("play-green.png", 0, lambda: print("play button")),
            ("reset-blue.png", 1, lambda: print("reset button")),
            ("save-purple.png", 2, lambda: print("save button")),
        ]

        for img, c, cmd in measure_ctrl:
            img_import = ctk.CTkImage(
                light_image=Image.open(f"./images/{img}"),
                dark_image=Image.open(f"./images/{img}"),
            )

            img_button = ctk.CTkButton(
                measurement_frame, text="", image=img_import, command=cmd
            )
            img_button.grid(row=4, column=c, padx=2, pady=2)

    # FRAME 3: Stopwatch Frame
    def get_time_frame(self):
        """3rd frame is the time and band information"""
        time_frame = ctk.CTkFrame(self, fg_color="transparent")
        time_frame.grid(row=2, column=0, padx=10, pady=10, sticky="W")

        time_frame.columnconfigure([0, 1], weight=1)

        # stopwatch + features
        stopwatch_label = ctk.CTkLabel(time_frame, text="0:00.0")
        stopwatch_label.grid(row=0, column=0, padx=2, pady=2, sticky="W")

        start_label = ctk.CTkLabel(time_frame, text="Last Start Time: ")
        start_label.grid(row=1, column=0, padx=2, pady=2, sticky="W")

        start_time = ctk.CTkLabel(time_frame, text="   [Last Start Time]")
        start_time.grid(row=1, column=1, padx=2, pady=2, sticky="W")

        band_label = ctk.CTkLabel(time_frame, text="Last Band Prepared: ")
        band_label.grid(row=2, column=0, padx=2, pady=2, sticky="W")

        band_prepped = ctk.CTkLabel(time_frame, text="   [Last Band Prepared]")
        band_prepped.grid(row=2, column=1, padx=2, pady=2, sticky="W")
