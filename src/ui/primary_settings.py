import customtkinter as ctk


class MainSettingFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.get_folder_frame()

    def get_folder_frame(self):
        """creates and sets up the frame for the folders"""
        primary_frame = ctk.CTkFrame(self)
        primary_frame.grid(row=0, column=0, sticky="EW")
        primary_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)
        primary_frame.columnconfigure([0, 1, 2], weight=1)

        header = ctk.CTkLabel(primary_frame, text="Folders", justify="left")
        header.grid(row=0, column=0, padx=10, pady=2, sticky="W")

        input_labels = [
            (0, "State Files Folder:", "D:/Users/Instrument/Desktop/State Files"),
            (
                1,
                "Correction Files Folder:",
                "D:/Users/Instrument/Desktop/Correction Files",
            ),
            (2, "Instrument Output Folder:", "D:/Users/Instrument/Desktop/Test Data"),
            (3, "Local Output Folder:", ""),
            (4, "Sweep Duration:", ""),
        ]

        for r, label, input in input_labels:
            folder_label = ctk.CTkLabel(primary_frame, text=label, justify="left")
            folder_label.grid(row=r, column=0, padx=5, pady=5, sticky="W")

            folder_path = ctk.CTkEntry(primary_frame, placeholder_text=input, width=500)
            folder_path.grid(row=r, column=2, padx=5, pady=5, sticky="EW")

        browse_button = ctk.CTkButton(primary_frame, text="Browse")
        browse_button.grid(row=3, column=3, padx=5, pady=5, sticky="W")

        run_note_text = ctk.CTkLabel(
            primary_frame,
            text=(
                "The run note is the text placed after the run id and band name in filename.\n"
                'Files will be saved as "808-13 B3 [run note].csv" and "808-13 B3 [run note].png"\n'
                "This can be used for location, test type, or any other information."
            ),
            justify="left",
        )
        run_note_text.grid(row=5, column=0, padx=5, pady=2, columnspan=3, sticky="W")
