import subprocess
from tkinter import filedialog as fd

import customtkinter as ctk

from instrument.folders import get_folder_info
from instrument.instrument import get_input
from ui.get_resource_path import resource_path
from ui.test_log_window import OpenTestLog
from ui.ui_logger import LoggingButton, LoggingTopLevel
from utils.logger import autosa_logger
from utils.settings import (
    get_log_folder_path,
    get_settings_path,
    is_valid_inst_folder,
    is_valid_local_folder,
    is_valid_sweep_duration,
    read_settings_from_file,
    write_settings_to_file,
)


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
        autosa_logger.info(
            f"{band} Amplitude Correction changed to {self.corr_choice[band]}"
        )

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
    def __init__(self, parent, inst, settings_vars, settings_labels):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.inst = inst
        self.settings_vars = settings_vars
        self.settings_labels = settings_labels
        self.path_entry_widget = {}  # to store the entry widgets

        for key, val in self.settings_vars.items():
            val.trace_add(
                "write", lambda *args, v=val, k=key: self.validate_path_settings(k, v)
            )

        self.create_widgets()

    def create_widgets(self):
        self.create_primary_frame()

    def create_primary_frame(self):
        """creates and sets up the frame for the folders"""
        primary_frame = ctk.CTkFrame(self)
        primary_frame.grid(row=0, column=0, sticky="nsew")
        primary_frame.rowconfigure([0, 1, 2, 3, 4], weight=1)
        primary_frame.columnconfigure([0, 1, 2], weight=1)

        self.path_entries = []  # storing user input folders

        for r, (key, settings_var) in enumerate(self.settings_vars.items()):
            text = self.settings_labels[key] + ":"
            ctk.CTkLabel(primary_frame, text=text, justify="left").grid(
                row=r, column=0, padx=5, pady=5, sticky="w"
            )
            path_entry = ctk.CTkEntry(
                primary_frame, textvariable=settings_var, width=500
            )
            path_entry.grid(row=r, column=2, padx=5, pady=5, sticky="ew")
            self.path_entries.append(path_entry)  # collect the inputs in entry widget
            self.path_entry_widget[key] = path_entry  # entry widget

        # validate upon opening the settings window
        for key, val in self.settings_vars.items():
            self.validate_path_settings(key, val)

        LoggingButton(
            primary_frame,
            text="Browse",
            command=lambda: SettingsWindow.browse_files(
                self.master,
                self.settings_vars["-LOCAL OUT FOLDER-"],
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

    def validate_path_settings(self, key, val):
        cur_path = val.get().strip()
        entry_widget = self.path_entry_widget.get(key)

        # if entry box doesn't exist, crashes
        if not entry_widget:
            return

        if key in ["-STATE FOLDER-", "-CORR FOLDER-", "-INST OUT FOLDER-"]:
            valid = is_valid_inst_folder(self.inst, cur_path)
        elif key == "-LOCAL OUT FOLDER-":
            valid = is_valid_local_folder(cur_path)
        elif key == "-SWEEP DUR-":
            valid = is_valid_sweep_duration(cur_path)

        entry_widget.configure(border_color="gray" if valid else "red")
        if valid:
            autosa_logger.debug(f"VALID {key}: {cur_path}")
        else:
            autosa_logger.debug(f"INVALID {key}: {cur_path}")


class SettingsWindow(LoggingTopLevel):
    """opens a new window and sets it up for settings"""

    def __init__(
        self,
        parent,
        inst,
        label_color,
        frame_color,
        update_valid,
        update_output_folder,
        inst_found,
        update_state_button,
    ):
        super().__init__(parent)
        self.title("Settings")
        window_width = 1300
        window_height = 613
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure([0, 1, 2], weight=0)

        self.inst = inst
        self.label_color = label_color
        self.frame_color = frame_color
        self.inst_found = inst_found
        self.update_valid = update_valid
        self.update_output_folder = update_output_folder
        self.update_state_button = update_state_button
        self.frame_color = parent.frame_color
        self.label_color = parent.label_color
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
        frame1 = self.init_frame1()  # "Settings", settings location
        frame2 = self.init_frame2()  # tabview
        frame3 = self.init_frame3()  # update or cancel

        self.fill_header_frame1(frame1)
        self.fill_tabview_frame2(frame2)
        self.fill_button_frame3(frame3)

    def init_frame1(self):
        header_frame = ctk.CTkFrame(self, fg_color=self.label_color)
        header_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        header_frame.columnconfigure([0, 1], weight=1)
        return header_frame

    def init_frame2(self):
        self.tabview_frame = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabview_frame.grid(row=1, column=0, padx=5, pady=5, sticky="ewns")
        self.tabview_frame.columnconfigure(0, weight=1)
        self.tabview_frame.rowconfigure(0, weight=1)
        return self.tabview_frame

    def init_frame3(self):
        button_frame = ctk.CTkFrame(self, fg_color=self.label_color)
        button_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        button_frame.columnconfigure(0, weight=1)
        return button_frame

    def fill_header_frame1(self, frame1):
        settings_header_label = ctk.CTkLabel(frame1, text="Settings", font=("", 16))
        settings_header_label.grid(row=0, column=0, padx=5, sticky="w")

        test_log = LoggingButton(
            frame1,
            text="Start New Log",
            font=("", 10),
            width=16,
            height=10,
            anchor="center",
            command=self.open_test_log,
        )
        test_log.grid(row=1, column=0, padx=5, sticky="w")

        view_json_button = LoggingButton(
            frame1,
            text="Open Settings File",
            font=("", 8),
            width=16,
            height=10,
            anchor="center",
            fg_color="#979da2",
            hover_color="#676b6e",
            command=lambda: self.open_to_json(),
        )
        view_json_button.grid(row=0, column=1, padx=5, sticky="e")

        view_log_button = LoggingButton(
            frame1,
            text="View Logs",
            font=("", 8),
            width=16,
            height=10,
            anchor="center",
            fg_color="#979da2",
            hover_color="#676b6e",
            command=lambda: self.open_to_log(),
        )
        view_log_button.grid(row=1, column=1, padx=5, sticky="e")

    def fill_tabview_frame2(self, frame2):
        tab1 = frame2.add("      Primary      ")
        tab1.grid_rowconfigure(0, weight=1)
        tab1.grid_columnconfigure(0, weight=1)

        primary_frame = PrimaryFrame(
            tab1,
            self.inst,
            self.settings_vars,
            self.settings_labels,
        )
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
        save_button = LoggingButton(
            frame3,
            text="Save",
            command=lambda: self.save_settings(),
        )
        save_button.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        cancel_button = LoggingButton(frame3, text="Cancel", command=self.on_close)
        cancel_button.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def on_tab_change(self):
        current_tab = self.tabview_frame.get()
        autosa_logger.info(f'[TAB] User switched to "{current_tab.strip()}" tab.')

    def open_to_json(self):
        json_filepath = get_settings_path()
        subprocess.run(["explorer", "/select,", json_filepath])

    def open_to_log(self):
        log_folder_path = get_log_folder_path()
        subprocess.run(["explorer", log_folder_path])

    def save_settings(self):
        """write to the json file"""
        settings = {}
        for label, settings_var in self.settings_vars.items():
            settings[label] = (
                (
                    settings_var.get().lstrip("0")
                    if label == "-SWEEP DUR-"
                    else settings_var.get()
                )
                .strip()
                .replace("/", "\\")
            )

        settings["-CORR CHOICES-"] = self.corr_choice

        write_settings_to_file(settings)
        self.update_valid()
        self.update_output_folder()
        self.update_state_button()

        autosa_logger.debug("Settings saved and closed.")
        self.destroy()  # close settings window after saving

    def browse_files(parent, path_var):
        folder_path = fd.askdirectory(parent=parent)
        path_var.set(folder_path)

    def on_close(self):
        autosa_logger.debug(
            "Any settings changed in the Settings window was canceled and not saved."
        )
        self.destroy()

    def open_test_log(self):
        self.log_window = OpenTestLog(
            self, self.inst, self.inst_found, self.frame_color, self.label_color
        )
        self.log_window.wait_window()  # Block until window closes

        # Get the result
        test_log_data = getattr(self.log_window, "return_data", None)
        if test_log_data:
            get_input(test_log_data)
