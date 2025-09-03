import datetime
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
        window_height = 340
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, False)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.transient(parent)

        self.inst = inst
        self.inst_found = inst_found
        self.frame_color = frame_color
        self.label_color = label_color
        self.cur_date = datetime.datetime.now().strftime("%Y_%m_%d")

        self.log_info_labels = [
            "Test Engineer",
            "Project Name",
            "Log Filename",
        ]
        self.entry_vars = {}
        self.return_data = {}
        self.filename_var = ctk.StringVar()
        self.filename_var.set(f"autosa_test_log_{self.cur_date}.csv")

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
        dropdown_frame.grid(row=0, column=0, padx=5, sticky="sew")
        return dropdown_frame

    def init_frame2(self):
        choice_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        choice_frame.grid(row=1, column=0, padx=5, sticky="nsew")
        return choice_frame

    def init_frame3(self):
        button_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        button_frame.grid(row=3, column=0, padx=5, sticky="sew")
        button_frame.columnconfigure(0, weight=1)
        return button_frame

    def fill_title_menu(self, frame1):
        header_label = ctk.CTkLabel(
            frame1, text="Current Test Log: ", justify="left", font=("", 11, "bold")
        )
        header_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        cur_test_log = ctk.CTkLabel(
            frame1,
            text=get_latest_test_log()[1],
            justify="left",
            font=("", 11),
        )
        cur_test_log.grid(row=0, column=1, padx=5, pady=5, sticky="w")

    def fill_entry_frame(self, frame2):
        ctk.CTkLabel(
            frame2, text="Create New Test Log: ", justify="left", font=("", 12, "bold")
        ).grid(row=0, column=0, columnspan=2, padx=5, pady=5, sticky="w")

        for row, label in enumerate(self.log_info_labels):
            ctk.CTkLabel(frame2, text=label + ":").grid(
                row=row + 1, column=0, padx=5, pady=5, sticky="w"
            )

            if label == "Log Filename":
                filename_label = ctk.CTkLabel(frame2, textvariable=self.filename_var)
                filename_label.grid(row=row + 1, column=1, padx=5, pady=5, sticky="w")
            else:
                var = ctk.StringVar()
                var.trace_add("write", self.create_filename)
                self.entry_vars[label] = var

                entry = ctk.CTkEntry(frame2, textvariable=var, width=490)
                entry.grid(row=row + 1, column=1, padx=5, pady=5, sticky="w")

                self.entry_vars[label] = entry

    def fill_button_frame(self, frame3):
        self.save_btn = LoggingButton(
            frame3,
            text="Start New Log",
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

    def create_filename(self, *args):
        project_name = self.entry_vars["Project Name"].get().strip()
        project_name = project_name.replace(" ", "_")  # replace spaces with underscores
        if not project_name:
            project_name = f"autosa_test_log_{self.cur_date}.csv"
            self.filename_var.set(project_name)
        else:
            project_name = f"autosa_test_log_{project_name}_{self.cur_date}.csv"
            self.filename_var.set(project_name)

    def save_csv(self):
        # gather to return
        data = {label: var.get().strip() for label, var in self.entry_vars.items()}
        data["Log Filename"] = self.filename_var.get().strip()
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
