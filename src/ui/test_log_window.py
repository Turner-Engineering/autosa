import os

import customtkinter as ctk

from ui.get_resource_path import resource_path
from ui.ui_logger import LoggingButton, LoggingTopLevel
from utils.settings import read_settings_from_file
from utils.test_log import get_latest_test_log


class OpenTestLog(LoggingTopLevel):
    def __init__(self, parent, inst, inst_found, frame_color, label_color):
        super().__init__(parent)
        self.title("Test Log")
        window_width = 900
        window_height = 400
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient(parent)

        self.inst = inst
        self.inst_found = inst_found
        self.frame_color = frame_color
        self.label_color = label_color

        self.log_info_labels = {
            "Test Engineer": "Test Engineer",
            "Project Name": "Project Name",
            "Log Filename": "Test Log Filename",  # TODO: make it project_name_autosa_test_log_date
        }
        self.entry_vars = {}
        self.return_data = {}

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()  # choice
        frame2 = self.init_frame2()  # choice fill
        frame3 = self.init_frame3()  # buttons

        self.fill_title_menu(frame1)
        self.fill_entry_frame(frame2)
        self.fill_button_frame(frame3)

    def init_frame1(self):
        dropdown_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        dropdown_frame.grid(row=0, column=0, padx=5, pady=5, sticky="new")
        return dropdown_frame

    def init_frame2(self):
        choice_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        choice_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        return choice_frame

    def init_frame3(self):
        button_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        button_frame.grid(row=3, column=0, padx=5, pady=5, sticky="sew")
        button_frame.columnconfigure(0, weight=1)
        return button_frame

    def fill_title_menu(self, frame1):
        header_label = ctk.CTkLabel(
            frame1, text="Current Test Log: ", justify="left", font=("", 11, "bold")
        )
        header_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        cur_test_log = ctk.CTkLabel(
            frame1,
            text=get_latest_test_log(),
            justify="left",
            font=("", 11),
        )
        cur_test_log.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def fill_entry_frame(self, frame2):
        ctk.CTkLabel(
            frame2, text="Create New Test Log: ", justify="left", font=("", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        for row, (label, text) in enumerate(self.log_info_labels.items()):
            ctk.CTkLabel(frame2, text=label + ":").grid(
                row=row + 1, column=0, padx=5, pady=5, sticky="w"
            )

            var = ctk.StringVar()
            var.trace_add("write", self.check_entry)
            self.entry_vars[label] = var

            entry = ctk.CTkEntry(
                frame2, textvariable=var, placeholder_text=text, width=490
            )
            entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky="w")

            self.entry_vars[label] = entry

    def fill_button_frame(self, frame3):
        self.save_btn = LoggingButton(
            frame3,
            text="Start New Log",
            state="disabled",
            command=self.save_csv,
        )
        self.save_btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        cancel_btn = LoggingButton(
            frame3,
            text="Cancel",
            command=lambda: self.destroy(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        )
        cancel_btn.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def check_entry(self, *args):
        all_filled = all(var.get().strip() for var in self.entry_vars.values())
        self.save_btn.configure(state="normal" if all_filled else "disabled")

    def save_csv(self):
        # gather to return
        data = {label: var.get().strip() for label, var in self.entry_vars.items()}
        new_filename = data["Log Filename"]
        local_out_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

        # makesure filename ends with csv
        if not new_filename.lower().endswith(".csv"):
            new_filename += ".csv"

        path = os.path.join(local_out_folder, new_filename)
        base, ext = os.path.splitext(path)
        filename = f"{base}{ext}"

        # consider filename
        i = 1
        while os.path.exists(filename):
            filename = f"{base}({i}){ext}"
            i += 1

        open(filename, "w").close()  # create but don't write

        data["Log Filename"] = filename
        self.return_data = data

        self.destroy()
