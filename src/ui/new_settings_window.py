import customtkinter as ctk
from ui.primary_settings import MainSettingFrame
from ui.corr_settings import CorrSettingFrame


class get_settings_window(ctk.CTkToplevel):
    """opens a new window and sets it up for settings"""

    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        window_width = 1400
        window_height = 600
        self.geometry(f"{window_width}x{window_height}")

        self.iconbitmap("images/autosa_logo.ico")
        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1, 2, 3], weight=1)
        self.create_widgets()

        # title frame
        settings_header = ctk.CTkLabel(self, text="Settings", justify="left")
        settings_header.grid(row=0, column=0, padx=5, pady=5, sticky="W")

    def create_widgets(self):
        self.get_button_frame()  # Button frame
        self.get_settings_menu_layout()

    def get_button_frame(self):
        """Creates the save and cancel buttons"""
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, sticky="EW")

        save_button = ctk.CTkButton(
            button_frame, text="Save", command=lambda: print("SAVED!")
        )
        save_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        cancel_button = ctk.CTkButton(
            button_frame, text="Cancel", command=lambda: self.destroy
        )
        cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    def get_settings_menu_layout(self):
        tabview = ctk.CTkTabview(self)
        tabview.grid(row=1, column=0, padx=5, pady=5, sticky="EW")
        tabview.rowconfigure([0, 1, 2, 3], weight=1)

        tab1 = tabview.add("      Primary      ")
        frame = MainSettingFrame(tab1)
        frame.pack(expand=1, fill="both")

        tab2 = tabview.add("      Amplitude Correction      ")
        frame = CorrSettingFrame(tab2)
        frame.pack(expand=1, fill="both")
