import os

import customtkinter as ctk

from ui.get_resource_path import resource_path
from ui.ui_logger import LoggingButton, LoggingTopLevel
from utils.settings import read_settings_from_file


class OpenTestLog(LoggingTopLevel):
    def __init__(self, parent, inst, inst_found, frame_color, label_color):
        super().__init__(parent)
        self.title("Test Log")
        window_width = 900
        window_height = 550
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

        self.test_log_choice = ctk.StringVar()
        self.test_log_choice.set("Select From Existing")
        self.log_info_labels = {
            "Test Engineer:": "Test Engineer",
            "Test Location:": "Test Location",
            "Project Name:": "Project Name",
        }

        self.log_info_entries = {}

        self.create_widgets()

    def create_widgets(self):
        # self.grid_rowconfigure(1, weight=1)
        # self.grid_columnconfigure(0, weight=1)
        frame1 = self.init_frame1()  # choice
        self.frame2 = self.init_frame2()  # choice fill
        frame3 = self.init_frame3()  # buttons

        self.fill_dropdown_menu(frame1)
        # self.fill_choice_frame(self.frame2)
        self.fill_button_frame(frame3)

    def init_frame1(self):
        dropdown_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        dropdown_frame.grid(row=0, column=0, padx=5, pady=5, sticky="ew")
        return dropdown_frame

    def init_frame2(self):
        choice_frame = ctk.CTkScrollableFrame(self, fg_color=self.frame_color)
        choice_frame.grid(row=1, column=0, padx=5, pady=5, sticky="nsew")
        return choice_frame

    def init_frame3(self):
        button_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        button_frame.grid(row=2, column=0, padx=5, pady=5, sticky="ew")
        # button_frame.grid_columnconfigure([0, 1], weight=0)
        return button_frame

    def fill_dropdown_menu(self, frame1):
        header_label = ctk.CTkLabel(
            frame1,
            text='Choose an option below. If there are existing test logs, they will appear for you to select. If not, it will stay empty. Select "Create New Test Log" to start a new file.',
            justify="left",
            wraplength=550,
        )
        header_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.dropdown_menu = ctk.CTkOptionMenu(
            frame1,
            values=["Select From Existing", "Create New Test Log"],
            variable=self.test_log_choice,
            command=self.update_choice,
            width=160,
        )
        self.dropdown_menu.grid(row=1, column=0, padx=5, pady=5, sticky="w")

    def fill_button_frame(self, frame3):
        frame3.grid_columnconfigure(0, weight=1)  # helps push buttons to the right

        cur_btn = LoggingButton(
            frame3, text="Save/Open Selected CSV", command=self.open_cur_csv
        )
        cur_btn.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        cancel_btn = LoggingButton(
            frame3,
            text="Cancel",
            command=lambda: self.destroy(),
            fg_color="#939ba2",
            hover_color="#646a6e",
        )
        cancel_btn.grid(row=0, column=1, padx=5, pady=5, sticky="e")

    def update_choice(self, selected_choice):
        local_output_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

        for widget in self.frame2.winfo_children():
            widget.destroy()

        self.choice_label = ctk.CTkLabel(self.frame2, text="")
        self.choice_label.grid(row=0, column=0, padx=5, pady=5, sticky="nw")

        if selected_choice == "Select From Existing":
            self.choice_label.configure(text=selected_choice)
            csv_path = os.path.join(local_output_folder, "autosa_test_log.csv")
        elif selected_choice == "Create New Test Log":
            for row, (label, placeholder) in enumerate(self.log_info_labels.items()):
                ctk.CTkLabel(self.frame2, text=label).grid(
                    row=row, column=0, padx=5, pady=5, sticky="w"
                )

                entry = ctk.CTkEntry(
                    self.frame2, placeholder_text=placeholder, width=450
                )
                entry.grid(row=row, column=1, padx=5, pady=5, sticky="w")

                self.log_info_entries[label] = entry

    # dropdown:
    # - search for "autosa_test_log" with "".csv" extension in local_output_folder (it could also be autosa_test_log (1) or 2, etc)
    # --- show all in list, make selectable 1 at a time
    # --- select only 1 from existing
    # --- if none found, "No Test Logs found. Create a new Test Log."
    # --- create a new csv
    # --- entry boxes (red until filled)

    # for now, print
    # later, return all things and call in write_to_test_log()

    def open_cur_csv(self):
        print("Opening file explorer")
        self.destroy()
        # disable if no file was selected else, enable
        # if self.test_log_choice.get() == "Select From Existing", open
        # if self.test_log_choice.get() == "Create New Test Log", save
        # subprocess.run(["explorer", selected_test_log])
