import os
import subprocess

import customtkinter as ctk

from instrument.instrument import get_input, release_inst
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
from ui.warnings_window import WarningsWindow
from utils.logger import autosa_logger
from utils.settings import (
    get_autosa_version,
    read_settings_from_file,
)
from utils.warnings import WarningManager

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

        # Initialize warning manager
        self.warning_manager = WarningManager()

        # Check for warnings
        self.warning_manager.check_datetime_warning(self.inst, self.inst_name)
        self.warning_manager.check_settings_warning(self.inst)
        self.warning_manager.check_correction_warning()

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure([0, 1], weight=1)

        ctk.CTkLabel(
            self,
            text="Autosa",
            font=("", 18),
            fg_color=self.label_color,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        LoggingButton(
            self,
            text="?",
            height=24,
            width=24,
            # fg_color="#979da2",
            # hover_color="#676b6e",
            command=lambda: HelpWindow(self, self.frame_color, self.label_color),
        ).grid(row=0, column=1, sticky="e", pady=10)

        LoggingButton(
            self,
            text="Settings",
            command=lambda: self.settings_window(),
        ).grid(row=0, column=2, sticky="ne", padx=10, pady=10)

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
        self.output_folder_button.grid(row=1, column=2, sticky="ne", padx=10)

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
        self.test_log_button.grid(row=2, column=2, padx=10, sticky="ne")

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
        ).grid(row=1, column=0, sticky="w", padx=10)

        # Create warning display frame
        self.warning_frame = ctk.CTkFrame(self, fg_color=self.frame_color)
        self.warning_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=5)
        self.warning_frame.columnconfigure(0, weight=1)

        # Warning display label
        self.warning_var = ctk.StringVar()
        self.warning_label = ctk.CTkLabel(
            self.warning_frame,
            textvariable=self.warning_var,
            justify="left",
            anchor="w",
            fg_color=self.label_color,
            text_color="red",
            font=("", 12),
            height=20,
        )
        self.warning_label.grid(row=0, column=0, sticky="w", padx=0)

        # View details button (always shown)
        self.show_all_warnings_button = OutlineButton(
            self.warning_frame,
            text="See All Warnings",
            height=20,
            font=("", 10),
            command=self.open_warnings_window,
        )
        # Override colors to make it red
        self.show_all_warnings_button.configure(
            text_color="red",
            border_color="red",
            hover_color="#ffcccc",
        )
        self.show_all_warnings_button.grid(row=0, column=1, sticky="w", padx=(5, 100))

        # Update warning display
        self.update_warning_display()

    def update_warning_display(self):
        """Update the warning display based on current warnings"""
        if not self.warning_manager.has_warnings():
            self.warning_var.set("")
            self.show_all_warnings_button.grid_remove()
            return

        primary_warning = self.warning_manager.get_primary_warning()
        if primary_warning:
            warning_text = f"⚠️ {primary_warning.message}"

            # Add count of additional warnings in parentheses if there are multiple
            if self.warning_manager.has_multiple_warnings():
                extra_count = self.warning_manager.count() - 1
                warning_text += f" ({extra_count} more)"

            self.warning_var.set(warning_text)
            self.show_all_warnings_button.grid()

    def open_warnings_window(self):
        """Open the warnings popup window"""
        all_warnings = self.warning_manager.get_all_warnings()
        WarningsWindow(self, all_warnings, self.frame_color, self.label_color)

    def update_valid(self):
        """Update settings validation and refresh warning display"""
        self.warning_manager.check_datetime_warning(self.inst, self.inst_name)
        self.warning_manager.check_settings_warning(self.inst)
        self.warning_manager.check_correction_warning()
        self.update_warning_display()

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
            self, self.inst, self.inst_found, self.frame_color, self.label_color
        )
        self.log_window.wait_window()  # Block until window closes

        # Get the result
        test_log_data = getattr(self.log_window, "return_data", None)
        if test_log_data:
            get_input(test_log_data)

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
        window_height = 780
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
        menu_frame = MenuFrame(
            self,
            self.inst_found,
            self.inst,
            self.discon_btn_st,
            self.is_disconnected,
        )

        top_frame = HeaderFrame(
            self,
            self.inst_found,
            self.inst,
            self.inst_name,
            menu_frame.set_up_frame,
        )

        # use a string for "both" to match the fill="x" above
        top_frame.pack(fill="x")
        menu_frame.pack(fill="both", expand=True)

    def on_close(self):
        autosa_logger.info("User closed Autosa.")
        self.destroy()
