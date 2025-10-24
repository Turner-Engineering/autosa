import os
import subprocess

import customtkinter as ctk

from ui.get_resource_path import resource_path
from ui.ui_logger import LoggingButton, LoggingTopLevel, OutlineButton
from utils.logger import autosa_logger
from utils.settings import read_settings_from_file
from utils.test_log import get_project_name, get_test_logs


class ChooseActiveLog(LoggingTopLevel):
    def __init__(
        self,
        parent,
        inst,
        inst_found,
        header_frame,
        current_test_log,
        frame_color,
        label_color,
    ):
        super().__init__(parent)
        self.title("Choose Active Log")
        window_width = 700
        window_height = 300
        self.geometry(f"{window_width}x{window_height}")
        self.resizable(False, True)
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient(parent)

        self.inst = inst
        self.inst_found = inst_found
        self.header_frame = header_frame
        self.current_test_log = current_test_log
        self.frame_color = frame_color
        self.label_color = label_color

        self.test_logs = get_test_logs()
        self.test_logs_dict = [
            {"base_path": os.path.basename(log), "full_path": log}
            for log in self.test_logs
        ]

        self.log_type = None
        self.active_log_var = ctk.StringVar()  # for dropdown
        self.active_log_var.set(
            self.test_logs_dict[0]["base_path"]
        )  # default to first log

        self.create_widgets()

    def create_widgets(self):
        frame1 = self.init_frame1()
        frame2 = self.init_frame2()
        frame3 = self.init_frame3()

        self.fill_frame1(frame1)
        self.fill_frame2(frame2)
        self.fill_frame3(frame3)

    def init_frame1(self):
        frame1 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame1.grid(row=0, column=0, padx=10, sticky="ew")
        return frame1

    def init_frame2(self):
        frame2 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame2.grid(row=1, column=0, padx=10, pady=20, sticky="ew")
        return frame2

    def init_frame3(self):
        frame3 = ctk.CTkFrame(self, fg_color=self.frame_color)
        frame3.grid(row=2, column=0, padx=10, sticky="e")
        return frame3

    def fill_frame1(self, frame1):
        ctk.CTkLabel(
            frame1,
            text="Multiple test logs were found. Please choose a test log or start a new log.",
            justify="left",
            font=("", 12, "bold"),
        ).grid(row=0, column=0, padx=5, pady=5, sticky="w")

        ctk.CTkLabel(
            frame1,
            text="Autosa works best with one autosa test log in the local output folder. "
            "To avoid this prompt on the next launch please move inactive test logs to a separate folder.",
            text_color="#8F0202",
            wraplength=430,
            justify="left",
            font=("", 12, "bold"),
        ).grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def fill_frame2(self, frame2):
        ctk.CTkLabel(frame2, text="Test Log: ").grid(row=0, column=0, padx=5, pady=5)

        self.active_log_menu = ctk.CTkOptionMenu(
            frame2,
            values=[log["base_path"] for log in self.test_logs_dict],
            variable=self.active_log_var,
            width=372,
        )
        self.active_log_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

    def fill_frame3(self, frame3):
        LoggingButton(
            frame3, text="Use Selected Log", command=self.use_selected_log
        ).grid(row=0, column=1, padx=5, pady=5, sticky="e")

        OutlineButton(
            frame3, text="Open Output Folder", command=self.open_output_folder
        ).grid(row=1, column=0, padx=5, pady=5, sticky="e")

        OutlineButton(frame3, text="Start A New Log", command=self.new_test_log).grid(
            row=1, column=1, padx=5, pady=5, sticky="e"
        )

    def use_selected_log(self):
        # find the dictionary matching the selected base path
        selected_log = next(
            log
            for log in self.test_logs_dict
            if log["base_path"] == self.active_log_var.get()
        )

        self.current_test_log.clear()
        self.current_test_log.update(
            {
                "full_path": selected_log["full_path"],
                "project_name": get_project_name(selected_log["full_path"]),
            }
        )

        self.log_type = "existing_log"

        autosa_logger.info(
            f'User selected "{self.current_test_log["full_path"]}" as active log.'
        )

        self.destroy()

    def open_output_folder(self):
        """Open the local output folder in Windows Explorer"""
        try:
            local_output_path = read_settings_from_file()["-LOCAL OUT FOLDER-"]
            if local_output_path and os.path.exists(local_output_path):
                subprocess.run(["explorer", "/open,", local_output_path])
                autosa_logger.info(f"Opened output folder: {local_output_path}")
            else:
                autosa_logger.warning("Output folder path is not set or does not exist")
        except Exception as e:
            autosa_logger.error(f"Failed to open output folder: {e}")

    def new_test_log(self):
        self.log_type = "new_log"

        self.current_test_log.clear()
        self.current_test_log.update(
            {
                "full_path": None,  # Will be set after OpenTestLog
                "project_name": "New Test Log",  # Placeholder, will be updated in OpenTestLog
            }
        )

        self.destroy()
