import customtkinter as ctk


class SingleModeFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.configure(border_width=2)
        self.create_widgets()

    def create_widgets(self):
        self.create_header_frame()
        self.create_band_button_frame()

    # FRAME 1: header and run note
    def create_header_frame(self):
        """1st frame is the header"""
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.grid(row=0, column=0, padx=10, pady=10, sticky="EW")
        header_frame.columnconfigure([0, 1], weight=1)

        tab2_label = ctk.CTkLabel(
            header_frame,
            text=(
                "Single Band Mode lets you run one band at a time.\n"
                "State files, correction files, and file names are set automatically."
            ),
            justify="left",
            anchor="w",
        )
        tab2_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        run_note_entry = ctk.CTkEntry(header_frame, placeholder_text="[run note]")
        run_note_entry.grid(row=0, column=1, padx=5, pady=5, sticky="E")

    # FRAME 2: Button Frame
    def create_band_button_frame(self):
        """2nd frame creates and sets up bands B0-B4, B5h-B7h, B5v-B7v"""
        button_frame = ctk.CTkFrame(self, fg_color="transparent")
        button_frame.grid(row=1, column=0, padx=10, pady=10, sticky="EW")
        button_frame.columnconfigure([0, 1, 2, 3, 4], weight=1)

        details_label = ctk.CTkLabel(button_frame, text="Prepare, Record, and Save:")
        details_label.grid(row=0, column=0, padx=5, pady=5, columnspan=5, sticky="W")

        band_buttons = [
            ("B0", lambda: print("B0"), 1, 0),
            ("B1", lambda: print("B1"), 1, 1),
            ("B2", lambda: print("B2"), 1, 2),
            ("B3", lambda: print("B3"), 1, 3),
            ("B4", lambda: print("B4"), 1, 4),
            ("B5h", lambda: print("B5h"), 2, 1),
            ("B6h", lambda: print("B6h"), 2, 2),
            ("B7h", lambda: print("B7h"), 2, 3),
            ("B5v", lambda: print("B5v"), 3, 1),
            ("B6v", lambda: print("B6v"), 3, 2),
            ("B7v", lambda: print("B7v"), 3, 3),
        ]

        for band_key, cmd, r, c in band_buttons:
            band_button = ctk.CTkButton(button_frame, text=band_key, command=cmd)
            band_button.grid(row=r, column=c, padx=2, pady=2)
