import customtkinter as ctk

from ui.large_button import LargeButton


class SingleModeFrame(ctk.CTkFrame):
    def __init__(self, parent, frame_color="transparent", label_color="transparent"):
        super().__init__(parent)
        self.frame_color = frame_color
        self.label_color = label_color
        self.button_padding = 4
        self.columnconfigure(0, weight=1)

        self.run_note_var = ctk.StringVar()

        self.band_buttons = [
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

        ctk.CTkEntry(
            frame,
            textvariable=self.run_note_var,
            width=300,
        ).grid(row=0, column=1, padx=5, pady=5, sticky="w")

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
            LargeButton(
                inner_frame,
                text=band_key,
                command=cmd,
            ).grid(row=r, column=c, padx=self.button_padding, pady=self.button_padding)
