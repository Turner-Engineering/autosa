import customtkinter as ctk


class CorrSettingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.columnconfigure([0, 1, 2, 3], weight=1)
        self.rowconfigure([0, 1, 2, 3], weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.get_correction_tab()

    def get_correction_tab(self):
        band_labels = [
            ("B0", 0, 0),
            ("B1", 0, 2),
            ("B2", 1, 0),
            ("B3", 1, 2),
            ("B4", 2, 0),
            ("B5", 2, 2),
            ("B6", 3, 0),
            ("B7", 3, 2),
        ]

        for band, r, c in band_labels:
            corr_label = ctk.CTkLabel(self, text=band)
            corr_label.grid(row=r, column=c, padx=10, pady=5, sticky="E")

        corr_inputs = [
            (["Option 01", "Option 02"], 0, 1),
            (["Option 03", "Option 04"], 0, 3),
            (["Option 05", "Option 06"], 1, 1),
            (["Option 07", "Option 08"], 1, 3),
            (["Option 09", "Option 10"], 2, 1),
            (["Option 11", "Option 12"], 2, 3),
            (["Option 13", "Option 14"], 3, 1),
            (["Option 15", "Option 16"], 3, 3),
        ]
        for value, r, c in corr_inputs:
            corr_band_menu = ctk.CTkOptionMenu(self, values=value)
            corr_band_menu.grid(row=r, column=c, padx=10, pady=5, sticky="W")
