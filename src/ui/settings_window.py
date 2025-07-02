import customtkinter as ctk
from tkinter import filedialog as fd
from instrument.folders import get_folder_info
from ui.get_resource_path import resource_path
from utils.settings import get_version_path, write_settings_to_file, read_settings_from_file


class CorrSettingFrame(ctk.CTkFrame):
    def __init__(self, parent, corr_path_var, corr_dropdowns, corr_choice, inst):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # interaction with the entry bar for "correction files folder"
        self.corr_path_var = corr_path_var
        self.corr_path_var.trace_add("write", self.update_dropdown)

        # interaction with the choices in the dropdown menu
        self.corr_dropdowns = corr_dropdowns
        self.corr_choice = corr_choice
        self.corr_file_options = ["No Correction"]
        self.inst = inst

        self.create_widgets()
        self.get_init_corr()

    def create_widgets(self):
        self.create_correction_tab()

    def create_correction_tab(self):
        corr_frame = ctk.CTkFrame(self)
        corr_frame.grid(row=0, column=0, sticky="nsew")
        corr_frame.columnconfigure([0, 1, 2, 3], weight=1)
        corr_frame.rowconfigure([0, 1, 2, 3], weight=1)

        # label's row, column
        band_labels = [(0, 0), (0, 2), (1, 0), (1, 2), (2, 0), (2, 2), (3, 0), (3, 2)]
        for b, (row, col) in enumerate(band_labels):
            ctk.CTkLabel(corr_frame, text=f"B{b}").grid(
                row=row, column=col, padx=15, pady=15, sticky="e"
            )

        # row and column of the option menu
        place_menu = [(0, 1), (0, 3), (1, 1), (1, 3), (2, 1), (2, 3), (3, 1), (3, 3)]
        for b, (row, col) in enumerate(place_menu):
            corr_band_dropdown = ctk.CTkOptionMenu(
                corr_frame, values=self.corr_file_options
            )
            corr_band_dropdown.set(self.corr_choice.get(f"B{b}", "No Correction"))
            corr_band_dropdown.grid(row=row, column=col, padx=15, pady=15, sticky="w")
            corr_band_dropdown.configure(
                command=lambda choice, band=f"B{b}": self.update_corr_choice(
                    band, choice
                )
            )
            self.corr_dropdowns.append(corr_band_dropdown)  # Store dropdowns

    def update_corr_choice(self, band, choice):
        self.corr_choice[band] = choice

    def update_dropdown(self, *args):
        self.corr_file_options = ["No Correction"]
        corr_exists, corr_empty, corr_filenames = get_folder_info(
            self.inst, self.corr_path_var.get()
        )

        for dropdown in self.corr_dropdowns:
            if self.corr_path_var.get() == "":
                dropdown.configure(state="disabled")
            else:
                dropdown.configure(state="normal")

        if not corr_exists or corr_empty:
            for dropdown in self.corr_dropdowns:
                dropdown.set("No Correction")
                dropdown.configure(state="disabled")
        else:
            dropdown.configure(state="normal")

            self.corr_file_options = ["No Correction"] + [
                file for file in corr_filenames if file.endswith(".csv")
            ]

            for dropdown in self.corr_dropdowns:
                dropdown.configure(values=self.corr_file_options)
                # if another file is selected, reset dropdown to "No correction"
                dropdown.set("No Correction")

    def get_init_corr(self):
        """Loads initial dropdown choices from settings if they exist."""
        corr_exists, _, corr_filenames = get_folder_info(
            self.inst, self.corr_path_var.get()
        )

        # loads the dropdown
        if self.corr_path_var.get():
            self.update_dropdown()

        # if path exists upon loading, load corr choices from settings
        if corr_exists:
            self.corr_file_options = ["No Correction"] + [
                file for file in corr_filenames if file.endswith(".csv")
            ]

            # Set the dropdown values based on corr_choice settings
            for i, dropdown in enumerate(self.corr_dropdowns):
                band = f"B{i}"
                corr_choice = self.corr_choice.get(band, "No Correction")
                if corr_choice in self.corr_file_options:
                    dropdown.set(corr_choice)
                else:
                    dropdown.set("No Correction")


class PrimaryFrame(ctk.CTkFrame):
    def __init__(self, parent, settings_vars, settings_labels):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.create_widgets(settings_vars, settings_labels)

    def create_widgets(self, settings_vars, settings_labels):
        self.create_primary_frame(settings_vars, settings_labels)

    def create_primary_frame(self, settings_vars, settings_labels):
        """creates and sets up the frame for the folders"""
        primary_frame = ctk.CTkFrame(self)
        primary_frame.grid(row=0, column=0, sticky="nsew")
        primary_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)
        primary_frame.columnconfigure([0, 1, 2], weight=1)

        self.path_entries = []  # storing user input folders

        for r, (key, settings_var) in enumerate(settings_vars.items()):
            text = settings_labels[key] + ":"
            ctk.CTkLabel(primary_frame, text=text, justify="left").grid(
                row=r, column=0, padx=5, pady=5, sticky="w"
            )
            path_entry = ctk.CTkEntry(
                primary_frame, textvariable=settings_var, width=500
            )
            path_entry.grid(row=r, column=2, padx=5, pady=5, sticky="ew")
            self.path_entries.append(path_entry)  # collect the inputs

        # ctk.CTkButton(
        #     primary_frame,
        #     text="Browse",
        #     command=lambda: SettingsWindow.browse_files(settings_vars["-CORR FOLDER-"]),
        # ).grid(row=1, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkButton(
            primary_frame,
            text="Browse",
            command=lambda: SettingsWindow.browse_files(
                self.master, settings_vars["-LOCAL OUT FOLDER-"]
            ),
        ).grid(row=3, column=3, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(
            primary_frame,
            text=(
                "The run note is the text placed after the run id and band name in filename.\n"
                'Files will be saved as "808-13 B3 [run note].csv" and "808-13 B3 [run note].png"\n'
                "This can be used for location, test type, or any other information."
            ),
            justify="left",
        ).grid(row=5, column=0, padx=5, pady=2, columnspan=3, sticky="w")


class SettingsWindow(ctk.CTkToplevel):
    """opens a new window and sets it up for settings"""

    def __init__(self, parent, inst, update_valid, inst_found, frame_color, label_color):
        super().__init__(parent)
        self.title("Settings")
        window_width = 1300
        window_height = 650
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1, 2], weight=0)
        self.inst = inst
        self.inst_found = inst_found
        self.update_valid = update_valid
        self.frame_color = frame_color
        self.label_color = label_color
        self.transient(parent)

        # if folder exists:
        settings = read_settings_from_file()
        self.corr_choice = settings.get("-CORR CHOICES-", {})

        self.settings_labels = {
            "-STATE FOLDER-": "State Files Folder",
            "-CORR FOLDER-": "Correction Files Folder",
            "-INST OUT FOLDER-": "Instrument Output Folder",
            "-LOCAL OUT FOLDER-": "Local Output Folder",
            "-SWEEP DUR-": "Sweep Duration",
        }

        self.corr_dropdowns = []
        self.settings_vars = {
            key: ctk.StringVar(value=value)
            for key, value in settings.items()
            if key != "-CORR CHOICES-"
        }

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2() # tabview
        frame3 = self.init_frame3() # update or cancel

        self.fill_header_frame1(frame1) # "Settings", settings location
        self.fill_tabview_frame2(frame2)
        self.fill_button_frame3(frame3)

    def init_frame1(self):
        header_frame = ctk.CTkFrame(self, fg_color=self.label_color)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        return header_frame

    def init_frame2(self):
        tabview_frame = ctk.CTkTabview(self)
        tabview_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ew")
        tabview_frame.columnconfigure(0, weight=1)
        tabview_frame.rowconfigure(0, weight=1)
        return tabview_frame
    
    def init_frame3(self):
        button_frame = ctk.CTkFrame(self, fg_color=self.label_color)
        button_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        return button_frame

    def fill_header_frame1(self, frame1):
        settings_header_label = ctk.CTkLabel(frame1, text="Settings")
        settings_header_label.grid(row=0, column=0, padx=5, sticky="w")

        folderpath_label = ctk.CTkLabel(frame1, text=get_version_path(), font=("", 10))
        folderpath_label.grid(row=1, column=0, padx=5, sticky="w")

    def fill_tabview_frame2(self, frame2):
        tab1 = frame2.add("      Primary      ")
        tab1.grid_rowconfigure(0, weight=1)
        tab1.grid_columnconfigure(0, weight=1)

        primary_frame = PrimaryFrame(tab1, self.settings_vars, self.settings_labels)
        primary_frame.pack(expand=True, fill="both")

        tab2 = frame2.add("      Amplitude Correction      ")
        tab2.grid_rowconfigure(0, weight=1)
        tab2.grid_columnconfigure(0, weight=1)

        corr_frame = CorrSettingFrame(
            tab2,
            self.settings_vars["-CORR FOLDER-"],
            self.corr_dropdowns,
            self.corr_choice,
            self.inst,
        )
        corr_frame.pack(expand=True, fill="both")

    def fill_button_frame3(self, frame3):
        save_button = ctk.CTkButton(
            frame3,
            text="Save",
            command=lambda: self.save_settings(),
        )
        save_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        cancel_button = ctk.CTkButton(
            frame3, text="Cancel", command=lambda: self.destroy()
        )
        cancel_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")


    def save_settings(self):
        """write to the json file"""
        settings = {}
        for label, settings_var in self.settings_vars.items():
            settings[label] = (settings_var.get().lstrip("0") if label == "-SWEEP DUR-" else settings_var.get()).strip()

        settings["-CORR CHOICES-"] = self.corr_choice

        write_settings_to_file(settings)
        self.update_valid()

        self.destroy()  # close settings window after saving

    def browse_files(parent, path_var):
        folder_path = fd.askdirectory(parent=parent)
        path_var.set(folder_path)
