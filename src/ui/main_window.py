import os
import subprocess

import customtkinter as ctk

from instrument.instrument import compare_datetime, release_inst
from ui.get_resource_path import resource_path
from ui.help_window import HelpWindow
from ui.manual_mode import ManualModeFrame
from ui.multi_band_mode import MultiModeFrame
from ui.release_mode import ReleaseMode
from ui.set_up_mode import SetUpModeFrame
from ui.settings_window import SettingsWindow
from ui.single_band_mode import SingleModeFrame
from ui.test_log_window import OpenTestLog
from ui.ui_logger import LoggingButton, OutlineButton
from utils.logger import autosa_logger
from utils.settings import (
    get_autosa_version,
    is_settings_valid,
    read_settings_from_file,
)
from utils.test_log import get_latest_test_log, get_test_log_project

ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.5)


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent, inst_found, inst, inst_name, set_up_frame):
        super().__init__(parent)
        self.inst_found = inst_found
        self.inst_name = inst_name
        self.inst = inst
        self.set_up_frame = set_up_frame

        self.frame_color = parent.frame_color
        self.label_color = parent.label_color
        self.configure(fg_color=self.frame_color, bg_color=self.frame_color)
        self.columnconfigure(0, weight=1)

        self.dt_diff, self.dt_check = compare_datetime(self.inst, self.inst_name)
        self.dt_check_text = (
            ""
            if self.dt_check
            else f"⚠️ Instrument and laptop datetime differ by {self.dt_diff}"
        )
        self.dt_check_color = "green" if self.dt_check else "red"
        self.dt_match_var = ctk.StringVar()
        self.dt_match_var.set(value=self.dt_check_text)

        self.valid_settings_label = ctk.CTkLabel(self)
        self.settings_error_var = ctk.StringVar()
        self.settings_error_color = None
        self.update_valid()

        self.create_widgets()

    def create_widgets(self):
        ctk.CTkLabel(
            self,
            text="Autosa",
            font=("", 18),
            fg_color=self.label_color,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        ctk.CTkLabel(
            self,
            text="Project Name: ",
            font=("", 12),
            fg_color=self.label_color,
        ).grid(row=0, column=1, sticky="w", pady=10)

        self.test_log_label = ctk.CTkLabel(
            self,
            text=get_test_log_project(),
            font=("", 12),
            fg_color=self.label_color,
        )
        self.test_log_label.grid(row=0, column=2, sticky="ew", padx=(0, 10), pady=10)

        LoggingButton(
            self,
            text="?",
            height=24,
            width=24,
            # fg_color="#979da2",
            # hover_color="#676b6e",
            command=lambda: HelpWindow(self, self.frame_color, self.label_color),
        ).grid(row=0, column=3, sticky="e", pady=10)

        LoggingButton(
            self,
            text="Settings",
            command=lambda: self.settings_window(),
        ).grid(row=0, column=4, sticky="ne", padx=10, pady=10)

        self.output_folder_button = OutlineButton(
            self,
            # text="📁 Open Output Folder",
            text="Open Output Folder",
            height=10,
            font=("", 10),
            state="normal"
            if os.path.exists(read_settings_from_file()["-LOCAL OUT FOLDER-"])
            else "disabled",
            command=lambda: self.open_output_folder(),
        )
        self.output_folder_button.grid(row=1, column=4, sticky="ne", padx=10)

        self.test_log_button = OutlineButton(
            self,
            # text="➕ Start New Test Log",
            text="Start New Test Log",
            font=("", 10),
            height=10,
            state="normal"
            if os.path.exists(read_settings_from_file()["-LOCAL OUT FOLDER-"])
            else "disabled",
            command=lambda: self.test_log_window(),
        )
        self.test_log_button.grid(row=2, column=4, padx=10, sticky="ne")

        inst_found_var = ctk.StringVar(
            value=(
                f"✅ {self.inst_name} Detected - " + str(self.inst)
                if self.inst_found
                else "❌ No Instrument Detected - Ensure the instrument is on and connected via USB-B to USB-A."
            )
        )
        inst_found_color = "green" if self.inst_found else "red"

        ctk.CTkLabel(
            self,
            textvariable=inst_found_var,
            text_color=inst_found_color,
            justify="left",
            anchor="w",
            fg_color=self.label_color,
            font=("", 12),
            height=20,
        ).grid(row=1, column=0, sticky="w", padx=10, columnspan=4)

        ctk.CTkLabel(
            self,
            textvariable=self.dt_match_var,
            text_color=self.dt_check_color,
            justify="left",
            anchor="w",
            fg_color=self.label_color,
            font=("", 12),
            height=20,
        ).grid(row=2, column=0, sticky="w", padx=10, columnspan=4)

        self.valid_settings_label = ctk.CTkLabel(
            self,
            textvariable=self.settings_error_var,
            text_color=self.settings_error_color,
            justify="left",
            anchor="w",
            fg_color=self.label_color,
            font=("", 12),
            height=20,
        )
        self.valid_settings_label.grid(row=2, column=0, sticky="w", padx=10)

    def update_test_log_label(self):
        self.test_log_label.configure(text=get_test_log_project())

    def is_valid_settings(self):
        is_valid = is_settings_valid(self.inst)
        return is_valid

    def update_valid(self):
        is_valid = self.is_valid_settings()
        self.settings_error_var.set(
            value=(
                ""
                if is_valid
                else "❌ Settings Invalid. Please change settings.                "
            )
        )
        self.settings_error_color = "green" if is_valid else "red"
        self.valid_settings_label.configure(text_color=self.settings_error_color)

    def update_output_folder(self):
        # get file paths of output folders
        local_output_path = read_settings_from_file()["-LOCAL OUT FOLDER-"]

        if os.path.exists(local_output_path):
            # on click, open both folders in explorer
            self.output_folder_button.configure(state="normal")
            self.test_log_button.configure(state="normal")
        else:
            self.output_folder_button.configure(state="disabled")
            self.test_log_button.configure(state="disabled")

    def open_output_folder(self):
        subprocess.run(
            ["explorer", "/open,", read_settings_from_file()["-LOCAL OUT FOLDER-"]]
        )

    def test_log_window(self):
        self.log_window = OpenTestLog(
            self,
            self.inst,
            self.inst_found,
            self.test_log_label,
            self.frame_color,
            self.label_color,
        )
        self.log_window.wait_window()  # Block until window closes

    def settings_window(self):
        SettingsWindow(
            self,
            self.inst,
            self.label_color,
            self.frame_color,
            self.update_valid,
            self.update_output_folder,
            self.inst_found,
            self.set_up_frame.update_state_button,
        )


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, inst_found, inst, discon_btn_st, is_disconnected):
        super().__init__(parent)
        self.header_access = None
        self.columnconfigure(0, weight=1)  # format to center
        self.rowconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.discon_btn_st = discon_btn_st
        self.is_disconnected = is_disconnected
        self.frame_color = parent.frame_color
        self.label_color = parent.label_color

        self.create_widgets()

    def create_widgets(self):
        """sets the structure for the different modes"""
        self.tabview = ctk.CTkTabview(self, command=self.on_tab_change)
        self.tabview.grid(row=0, column=0, padx=0, pady=0, sticky="ewns")
        self.tabview.configure(border_width=2)

        # tab formatting
        tab1 = self.tabview.add("      Manual Mode      ")
        frame = ManualModeFrame(
            tab1,
            self.inst_found,
            self.inst,
            self.discon_btn_st,
            self.header_access,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")

        tab2 = self.tabview.add("      Single Band Mode      ")
        frame = SingleModeFrame(
            tab2,
            self.inst_found,
            self.inst,
            self.discon_btn_st,
            self.header_access,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")

        tab3 = self.tabview.add("      Multi Band Mode      ")
        frame = MultiModeFrame(
            tab3,
            self.inst_found,
            self.inst,
            self.discon_btn_st,
            self.header_access,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")

        self.set_up_tab_label = "      Set Up Mode     "
        tab4 = self.tabview.add(self.set_up_tab_label)
        self.set_up_frame = SetUpModeFrame(
            tab4,
            self.inst_found,
            self.inst,
            self.discon_btn_st,
            self.frame_color,
            self.label_color,
        )
        frame = self.set_up_frame
        frame.pack(expand=1, fill="both")

        self.release_tab_label = "      Release Mode      "
        tab5 = self.tabview.add(self.release_tab_label)
        frame = ReleaseMode(
            tab5,
            self.inst_found,
            self.inst,
            self.is_disconnected,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")

    def on_tab_change(self):
        current_tab = self.tabview.get()
        autosa_logger.info(f'[TAB] User switched to "{current_tab.strip()}" tab.')
        if (current_tab == self.release_tab_label) and (not self.is_disconnected):
            release_inst(self.inst)


class MainApp(ctk.CTk):
    # Window creation
    def __init__(self, inst, inst_found, inst_name):
        super().__init__()
        self.title(f"Autosa {get_autosa_version()}")
        window_width = 1170
        window_height = 760
        self.geometry(f"{window_width}x{window_height}")
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.inst = inst
        self.inst_found = inst_found
        self.inst_name = inst_name
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        # self.debug = True
        self.debug = False
        if self.debug:
            self.frame_color = "pink"
            self.label_color = "white"
            autosa_logger.info("Debug Mode entered.")
        else:
            self.frame_color = "transparent"
            self.label_color = "transparent"

        self.is_disconnected = True if self.inst is None else False
        self.discon_btn_st = "disabled" if self.is_disconnected else "normal"

        self.create_widgets()

    def create_widgets(self):
        """sets up the window to have the header and the mode window"""
        self.menu_frame = MenuFrame(
            self,
            self.inst_found,
            self.inst,
            self.discon_btn_st,
            self.is_disconnected,
        )

        self.top_frame = HeaderFrame(
            self,
            self.inst_found,
            self.inst,
            self.inst_name,
            # self.menu_frame.set_up_frame,
            None,
        )
        self.top_frame.set_up_frame = self.menu_frame.set_up_frame
        self.menu_frame.header_access = self.top_frame

        self.menu_frame.create_widgets()

        # use a string for "both" to match the fill="x" above
        self.top_frame.pack(fill="x")
        self.menu_frame.pack(fill="both", expand=True)

    def on_close(self):
        autosa_logger.info("User closed Autosa.")
        self.destroy()
