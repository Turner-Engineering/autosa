import customtkinter as ctk
from tkinter import filedialog as fd
from ui.new_utils import write_json, read_json
import os

global SETTINGS_FILE_PATH
SETTINGS_FILE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "Autosa")


# TODO :
#   correction file selected -> updates dropdown, then settings saved WORKS
#   BUT when settings is opened again, the dropdown is not available, <-- TODO
#   despite the choice appearing
class CorrSettingFrame(ctk.CTkFrame):
    def __init__(self, parent, corr_var, corr_menus, corr_choice):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)

        # interaction with the entry bar for "correction files folder"
        self.corr_var = corr_var
        self.corr_var.trace_add("write", self.update_dropdown)

        # interaction with the choices in the dropdown menu
        self.corr_menus = corr_menus
        self.corr_choice = corr_choice
        self.corr_file_options = ["No Correction"]

        self.create_widgets(corr_var)

    def create_widgets(self, corr_var):
        self.get_correction_tab(corr_var)

    def get_correction_tab(self, corr_var):
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
            corr_band_menu = ctk.CTkOptionMenu(
                corr_frame, values=self.corr_file_options
            )
            corr_band_menu.set(self.corr_choice.get(f"B{b}", "No Correction"))
            corr_band_menu.grid(row=row, column=col, padx=15, pady=15, sticky="W")
            corr_band_menu.configure(
                command=lambda choice, band=f"B{b}": self.update_corr_choice(
                    band, choice
                )
            )
            self.corr_menus.append(corr_band_menu)  # Store dropdowns

        test_label = ctk.CTkLabel(corr_frame, textvariable=corr_var)
        test_label.grid(row=4, column=0, padx=15, pady=15, sticky="EW", columnspan=3)

    def update_corr_choice(self, band, choice):
        self.corr_choice[band] = choice

    def update_dropdown(self, corr_var, index, mode):
        self.corr_file_options = ["No Correction"]

        for menu in self.corr_menus:
            if self.corr_var.get() == "":
                menu.configure(state="disabled")
            else:
                menu.configure(state="normal")

        if not os.path.exists(self.corr_var.get()):
            for menu in self.corr_menus:
                menu.configure(state="disabled")
            print(f"correction folder '{self.corr_var.get()}' DOES NOT EXIST")
        elif not os.listdir(self.corr_var.get()):
            for menu in self.corr_menus:
                menu.configure(state="disabled")
            print(f"Correction folder '{self.corr_var.get()}' IS EMPTY")
        else:
            menu.configure(state="normal")

            # for each file in the found directory, check csv
            for file in os.listdir(self.corr_var.get()):
                if file.endswith(".csv"):
                    self.corr_file_options.append(file)

            for menu in self.corr_menus:
                print("FILE IS HERE!")
                menu.configure(values=self.corr_file_options)
                menu.set(
                    "No Correction"
                )  # if another file is selected, reset dropdown to "No correction"


class PrimaryFrame(ctk.CTkFrame):
    def __init__(self, parent, input_labels):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.create_widgets(input_labels)

    def create_widgets(self, input_labels):
        self.get_folder_frame(input_labels)

    def get_folder_frame(self, input_labels):
        """creates and sets up the frame for the folders"""
        prmry_frm = ctk.CTkFrame(self)
        prmry_frm.grid(row=0, column=0, sticky="EW")
        prmry_frm.rowconfigure([0, 1, 2, 3, 4], weight=1)
        prmry_frm.columnconfigure([0, 1, 2], weight=1)

        self.input = []  # storing user input files

        for r, (label, input) in enumerate(input_labels.items()):
            ctk.CTkLabel(prmry_frm, text=label, justify="left").grid(
                row=r, column=0, padx=5, pady=5, sticky="W"
            )

            path = ctk.CTkEntry(prmry_frm, textvariable=input, width=500)
            path.grid(row=r, column=2, padx=5, pady=5, sticky="EW")
            self.input.append(path)  # collect the inputs
        ctk.CTkButton(
            prmry_frm,
            text="Browse",
            command=lambda: SettingsWindow.browse_files(
                input_labels["Correction Files Folder:"]
            ),
        ).grid(row=1, column=3, padx=5, pady=5, sticky="W")

        ctk.CTkButton(
            prmry_frm,
            text="Browse",
            command=lambda: SettingsWindow.browse_files(
                input_labels["Local Output Folder:"]
            ),
        ).grid(row=3, column=3, padx=5, pady=5, sticky="W")

        ctk.CTkLabel(
            prmry_frm,
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
            data = read_json()

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
        settings_header = ctk.CTkLabel(self, text="Settings", justify="left")
        settings_header.grid(row=0, column=0, padx=5, pady=5, sticky="W")

        self.corr_menus = []
        self.input_labels = {
            "State Files Folder:": ctk.StringVar(value=state_folder),
            "Correction Files Folder:": ctk.StringVar(value=corr_folder),
            "Instrument Output Folder:": ctk.StringVar(value=inst_out_folder),
            "Local Output Folder:": ctk.StringVar(value=local_out_folder),
            "Sweep Duration:": ctk.StringVar(value=sweep_dur),
        }

        self.create_widgets()

    def create_widgets(self):
        self.get_button_frame()  # Button frame
        self.get_settings_menu_layout()

    def get_button_frame(self):
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

    def get_settings_menu_layout(self):
        tabview = ctk.CTkTabview(self)
        tabview.grid(row=1, column=0, padx=5, pady=5, sticky="EW")
        tabview.rowconfigure([0, 1, 2, 3], weight=1)

        tab1 = tabview.add("      Primary      ")
        frame = PrimaryFrame(tab1, self.input_labels)
        frame.pack(expand=1, fill="both")

        tab2 = tabview.add("      Amplitude Correction      ")
        frame = CorrSettingFrame(
            tab2,
            self.input_labels["Correction Files Folder:"],
            self.corr_menus,
            self.corr_choice,
        )
        frame.pack(expand=1, fill="both")

    def save_settings(self):
        """write to the json file"""
        json_data = {label: input.get() for label, input in self.input_labels.items()}
        json_data["Correction Choice:"] = self.corr_choice

        if not os.path.exists(SETTINGS_FILE_PATH):
            os.mkdir(SETTINGS_FILE_PATH)

        for label, input in self.input_labels.items():
            json_data[label] = input.get()

        write_json(json_data)

        self.destroy()  # close settings window after saving

    def browse_files(folder):
        folder_name = fd.askdirectory()
        folder.set(folder_name)
