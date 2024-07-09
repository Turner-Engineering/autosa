import customtkinter as ctk
from tkinter import filedialog as fd
from ui.new_utils import write_settings_to_json, read_settings_from_json
import os

global SETTINGS_FILE_PATH
SETTINGS_FILE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "Autosa")


# TODO :
#   correction file selected -> updates dropdown, then settings saved WORKS
#   BUT when settings is opened again, the dropdown is not available, <-- TODO
#   despite the choice appearing
class CorrSettingFrame(ctk.CTkFrame):
    def __init__(self, parent, corr_path_var, corr_dropdowns, corr_choice):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)

        # interaction with the entry bar for "correction files folder"
        self.corr_path_var = corr_path_var
        self.corr_path_var.trace_add("write", self.update_dropdown)

        # interaction with the choices in the dropdown menu
        self.corr_dropdowns = corr_dropdowns
        self.corr_choice = corr_choice
        self.corr_file_options = ["No Correction"]

        self.create_widgets(corr_path_var)

    def create_widgets(self, corr_var):
        self.create_correction_tab(corr_var)

    def create_correction_tab(self, corr_path_var):
        corr_frame = ctk.CTkFrame(self)
        corr_frame.grid(row=0, column=0, sticky="EW")
        corr_frame.columnconfigure([0, 1, 2, 3], weight=1)
        corr_frame.rowconfigure([0, 1, 2, 3], weight=1)

        # label's row, column
        band_labels = [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2)]
        for b, (row, col) in enumerate(band_labels):
            ctk.CTkLabel(corr_frame, text=f"B{b}").grid(
                row=row, column=col, padx=15, pady=15, sticky="E"
            )

        # row and column of the option menu
        place_menu = [(0, 1), (0, 3), (1, 1), (1, 3), (2, 1), (2, 3), (3, 1), (3, 3)]
        for b, (row, col) in enumerate(place_menu):
            corr_band_dropdown = ctk.CTkOptionMenu(
                corr_frame, values=self.corr_file_options
            )
            corr_band_dropdown.set(self.corr_choice.get(f"B{b}", "No Correction"))
            corr_band_dropdown.grid(row=row, column=col, padx=15, pady=15, sticky="W")
            corr_band_dropdown.configure(
                command=lambda choice, band=f"B{b}": self.update_corr_choice(
                    band, choice
                )
            )
            self.corr_dropdowns.append(corr_band_dropdown)  # Store dropdowns

        test_label = ctk.CTkLabel(corr_frame, textvariable=corr_path_var)
        test_label.grid(row=4, column=0, padx=15, pady=15, sticky="EW", columnspan=3)

    def update_corr_choice(self, band, choice):
        self.corr_choice[band] = choice

    def update_dropdown(self, corr_var, index, mode):
        self.corr_file_options = ["No Correction"]

        for dropdown in self.corr_dropdowns:
            if self.corr_path_var.get() == "":
                dropdown.configure(state="disabled")
            else:
                dropdown.configure(state="normal")

        if not os.path.exists(self.corr_path_var.get()):
            for dropdown in self.corr_dropdowns:
                dropdown.configure(state="disabled")
            print(f"correction folder '{self.corr_path_var.get()}' DOES NOT EXIST")
        elif not os.listdir(self.corr_path_var.get()):
            for dropdown in self.corr_dropdowns:
                dropdown.configure(state="disabled")
            print(f"Correction folder '{self.corr_path_var.get()}' IS EMPTY")
        else:
            dropdown.configure(state="normal")

            # for each file in the found directory, check csv
            for file in os.listdir(self.corr_path_var.get()):
                if file.endswith(".csv"):
                    self.corr_file_options.append(file)

            for dropdown in self.corr_dropdowns:
                print("FILE IS HERE!")
                dropdown.configure(values=self.corr_file_options)
                # if another file is selected, reset dropdown to "No correction"
                dropdown.set("No Correction")


class PrimaryFrame(ctk.CTkFrame):
    def __init__(self, parent, settings_vars):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.create_widgets(settings_vars)

    def create_widgets(self, settings_vars):
        self.create_primary_frame(settings_vars)

    def create_primary_frame(self, settings_vars):
        """creates and sets up the frame for the folders"""
        primary_frame = ctk.CTkFrame(self)
        primary_frame.grid(row=0, column=0, sticky="EW")
        primary_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)
        primary_frame.columnconfigure([0, 1, 2], weight=1)

        self.path_entries = []  # storing user input folders

        for r, (label, input) in enumerate(settings_vars.items()):
            ctk.CTkLabel(primary_frame, text=label, justify="left").grid(
                row=r, column=0, padx=5, pady=5, sticky="W"
            )

            path_entry = ctk.CTkEntry(primary_frame, textvariable=input, width=500)
            path_entry.grid(row=r, column=2, padx=5, pady=5, sticky="EW")
            self.path_entries.append(path_entry)  # collect the inputs

        ctk.CTkButton(
            primary_frame,
            text="Browse",
            command=lambda: SettingsWindow.browse_files(
                settings_vars["Correction Files Folder:"]
            ),
        ).grid(row=1, column=3, padx=5, pady=5, sticky="W")

        ctk.CTkButton(
            primary_frame,
            text="Browse",
            command=lambda: SettingsWindow.browse_files(
                settings_vars["Local Output Folder:"]
            ),
        ).grid(row=3, column=3, padx=5, pady=5, sticky="W")

        ctk.CTkLabel(
            primary_frame,
            text=(
                "The run note is the text placed after the run id and band name in filename.\n"
                'Files will be saved as "808-13 B3 [run note].csv" and "808-13 B3 [run note].png"\n'
                "This can be used for location, test type, or any other information."
            ),
            justify="left",
        ).grid(row=5, column=0, padx=5, pady=2, columnspan=3, sticky="W")


class SettingsWindow(ctk.CTkToplevel):
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

        # if folder exists:
        if os.path.exists(SETTINGS_FILE_PATH):
            data = read_settings_from_json()

            state_folder = data["State Files Folder:"]
            corr_folder = data["Correction Files Folder:"]
            inst_out_folder = data["Instrument Output Folder:"]
            local_out_folder = data["Local Output Folder:"]
            sweep_dur = data["Sweep Duration:"]
            self.corr_choice = data.get("Correction Choice:", {})
        else:
            state_folder = "D:/Users/Instrument/Desktop/State Files"
            corr_folder = "D:/Users/Instrument/Desktop/Correction Files"
            inst_out_folder = "D:/Users/Instrument/Desktop/Test Data"
            local_out_folder = ""
            sweep_dur = "5"
            self.corr_choice = {}

        # title frame
        settings_header_label = ctk.CTkLabel(self, text="Settings", justify="left")
        settings_header_label.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.corr_dropdowns = []
        self.settings_vars = {
            "State Files Folder:": ctk.StringVar(value=state_folder),
            "Correction Files Folder:": ctk.StringVar(value=corr_folder),
            "Instrument Output Folder:": ctk.StringVar(value=inst_out_folder),
            "Local Output Folder:": ctk.StringVar(value=local_out_folder),
            "Sweep Duration:": ctk.StringVar(value=sweep_dur),
        }

        self.create_widgets()

    def create_widgets(self):
        self.create_button_frame()  # Button frame
        self.create_settings_menu_layout()

    def create_button_frame(self):
        """Creates the save and cancel buttons"""
        button_frame = ctk.CTkFrame(self)
        button_frame.grid(row=3, column=0, sticky="EW")

        save_button = ctk.CTkButton(
            button_frame,
            text="Save",
            command=lambda: self.save_settings(),
        )
        save_button.grid(row=0, column=0, padx=10, pady=10, sticky="W")

        cancel_button = ctk.CTkButton(
            button_frame, text="Cancel", command=lambda: self.destroy()
        )
        cancel_button.grid(row=0, column=1, padx=10, pady=10, sticky="W")

    def create_settings_menu_layout(self):
        tabview = ctk.CTkTabview(self)
        tabview.grid(row=1, column=0, padx=5, pady=5, sticky="EW")
        tabview.rowconfigure([0, 1, 2, 3], weight=1)

        tab1 = tabview.add("      Primary      ")
        frame = PrimaryFrame(tab1, self.settings_vars)
        frame.pack(expand=1, fill="both")

        tab2 = tabview.add("      Amplitude Correction      ")
        frame = CorrSettingFrame(
            tab2,
            self.settings_vars["Correction Files Folder:"],
            self.corr_dropdowns,
            self.corr_choice,
        )
        frame.pack(expand=1, fill="both")

    def save_settings(self):
        """write to the json file"""
        json_data = {
            label: settings_var.get()
            for label, settings_var in self.settings_vars.items()
        }
        json_data["Correction Choice:"] = self.corr_choice

        if not os.path.exists(SETTINGS_FILE_PATH):
            os.mkdir(SETTINGS_FILE_PATH)

        for label, settings_var in self.settings_vars.items():
            json_data[label] = settings_var.get()

        write_settings_to_json(json_data)

        self.destroy()  # close settings window after saving

    def browse_files(path_var):
        folder_path = fd.askdirectory()
        path_var.set(folder_path)
