import webbrowser

import customtkinter as ctk

from ui.get_resource_path import resource_path
from utils.settings import get_autosa_version


class HelpWindow(ctk.CTkToplevel):
    def __init__(self, parent, frame_color, label_color):
        super().__init__(parent)
        self.title("Help")
        self.logo = resource_path("images/help.ico")
        self.after(200, lambda: self.iconbitmap(self.logo))
        self.transient(parent)
        self.window_width = 800
        self.window_height = 600
        self.geometry(f"{self.window_width}x{self.window_height}")
        self.resizable(False, False)

        self.frame_color = frame_color
        self.label_color = label_color

        self.padx = 5
        self.header_pady = (12, 0)
        self.subheader_pady = (5, 0)
        self.body_pady = (3, 5)

        self.header_font = ("Arial", 12, "bold")
        self.subheader_font = ("Arial", 10, "bold")
        self.body_font = ("Arial", 10)

        self.create_widgets(get_autosa_version())

    def create_widgets(self, autosa_version):
        """main scrollable frame"""
        main_scroll_frame = ctk.CTkScrollableFrame(self)
        main_scroll_frame.pack(expand=True, fill="both")

        """dynamically create frames based on content structure"""
        content_data = self.get_content_data(autosa_version)
        row = 0

        for section_key, section_data in content_data.items():
            frame = self.init_frame(main_scroll_frame, row)
            self.fill_frame_dynamically(frame, section_data)
            row += 1

    def init_frame(self, main_scroll_frame, row):
        about_frame = ctk.CTkFrame(main_scroll_frame, fg_color=self.frame_color)
        about_frame.grid(row=row, column=0, padx=self.padx, pady=0, sticky="ew")
        return about_frame

    def create_header(self, parent_frame, text, row=0):
        """Creates a header label with consistent styling"""
        return ctk.CTkLabel(
            parent_frame,
            text=text,
            font=self.header_font,
            height=0,
        ).grid(row=row, column=0, padx=self.padx, pady=self.header_pady, sticky="nw")

    def create_subheader(self, parent_frame, text, row):
        """Creates a subheader label with consistent styling"""
        return ctk.CTkLabel(
            parent_frame,
            text=text,
            font=self.subheader_font,
            height=0,
        ).grid(row=row, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")

    def create_body_text(self, parent_frame, text, row):
        """Creates a body text label with consistent styling"""
        return ctk.CTkLabel(
            parent_frame,
            text=text,
            font=self.body_font,
            height=0,
            justify="left",
            wraplength=490,
        ).grid(row=row, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

    def create_clickable_link(self, parent_frame, text, url, row):
        """Creates a clickable link label"""
        link_label = ctk.CTkLabel(
            parent_frame,
            text=text,
            font=self.body_font,
            height=0,
            justify="left",
            text_color="blue",
            cursor="hand2",
        )
        link_label.grid(
            row=row, column=0, padx=self.padx, pady=self.body_pady, sticky="nw"
        )

        def open_link(event):
            webbrowser.open(url)

        link_label.bind("<Button-1>", open_link)
        return link_label

    def get_content_data(self, autosa_version):
        """Returns all text content in a structured format"""
        return {
            "connection": {
                "title": "How do I connect Autosa to the Instrument?",
                "content": (
                    "To connect Autosa to the instrument, please ensure that:\n"
                    "1. The instrument is plugged in to power and turned on.\n"
                    "2. The instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable.\n"
                    "3. Autosa is launched after the instrument is fully on."
                ),
            },
            "no_instrument_detected": {
                "title": 'How do I fix "No Instrument Detected"?',
                "content": (
                    "1. Ensure that either the instrument or the emulator is fully turned on and running.\n"
                    "2. Relaunch Autosa."
                ),
            },
            "settings_invalid": {
                "title": 'How do I fix "Settings Invalid?"',
                "content": (
                    '"Settings Invalid" means one or more of the settings are not valid and must be corrected before measurements can be taken. '
                    "To fix this, follow these steps:\n"
                    "1. Ensure that the instrument is powered on, connected to the computer, and the software is running.\n"
                    "2. Open Settings and ensure all entries are valid (invalid entries will be highlighted in red). Save the settings when done.\n"
                    "All folder paths must be valid. The state files folder must contain valid state files, and the correction files folder must contain the necessary correction files."
                ),
            },
            "amp_corr_tab": {
                "title": "How do I configure the amplitude corrections?",
                "content": (
                    "1. Open settings\n"
                    "2. Ensure that the Corrections Files Folder is set to the folder on the instrument that contains the correction files\n"
                    "3. Switch to the Amplitude Correction tab\n"
                    "4. Select the correction file you want to apply to each band\n"
                    "5. Save the settings"
                ),
            },
            "measurement": {
                "title": "How do I take measurements with Autosa?",
                "content": (
                    "Autosa has three measurement modes: Manual Mode, Single Band Mode, and Multi Band Mode.\n"
                    "To take a measurement in Manual Mode:\n"
                    "   1. Ensure that the settings are valid.\n"
                    "   2. Navigate to the Manual Mode tab.\n"
                    "   3. Select a band to recall the state and correction files.\n"
                    "   4. Begin the measurement using the Green Play Button.\n"
                    "   5. Stop the measurement using the Red Pause Button.\n"
                    "   6. If needed, reset the instrument using the Cyan Reset Button.\n"
                    "   7. Save the run measurement using the Purple Save Button.\n"
                    "   8. Fill out the entry boxes for the filename and save the measurement.\n\n"
                    "To take a measurement in Single Band Mode or Multi Band Mode:\n"
                    "   1. Ensure all settings are valid.\n"
                    "   2. Navigate to the mode's tab.\n"
                    "   3. Input the run note and make selections as applicable.\n"
                    "   4. Measurements are saved in the local and instrument output folders."
                ),
            },
            "save_location": {
                "title": "Where is the measurement data saved?",
                "content": (
                    "Each measurement is saved in two locations:\n"
                    "1. The local output folder, which is the folder on the computer where Autosa is running.\n"
                    "2. The instrument output folder, which is the folder on the instrument that Autosa is connected to.\n\n"
                    "To open the local output folder, click the 'Open Output Folder' button in the top right corner.\n"
                ),
            },
            "set_up_mode": {
                "title": "What is Set Up Mode?",
                "content": (
                    "Set Up Mode provides test engineers an efficient way to update state files. "
                    "To use it:\n"
                    "1. Click a band button to recall a state file\n"
                    "2. Configure the measurement as desired on the instrument\n"
                    "3. Click the 'Update State' button to update the state through Autosa."
                ),
            },
            "version": {
                "title": "What version of Autosa is this?",
                "content": (
                    f"Autosa {autosa_version}. The version is also shown in the filename of the executable and in the main window title."
                ),
            },
            "release_mode": {
                "title": "How do I use Release Mode?",
                "content": (
                    "When Autosa is connected to the instrument, the instrument switches to remote operation mode. "
                    "To use the touch interface and buttons on the instrument, the instrument must be in local operation mode. "
                    'This is done by switching to the "Release Mode" tab in Autosa.'
                ),
            },
            "settings_buttons": {
                "title": "Where are the settings actually saved?",
                "content": (
                    'The settings are saved in a json file under "%LOCALAPPDATA%\\Autosa". '
                    "Do not edit this file directly unless you know what you are doing. Deleting the file will reset the settings to default. "
                    'To quickly navigate to this file, click the "Open Settings File" button in the top left corner of the Settings window. '
                ),
            },
            "back_run_id": {
                "title": "How do I reset the Run IDs back to 01?",
                "content": (
                    "Autosa automatically generates a Run ID for each measurement based on previously saved measurements. "
                    "Since Run IDs are generated based on the current date, they will be reset back to 01 after midnight. "
                    "Manually resetting the Run IDs back to 01, or back by a few measurements is not recommended.\n\n"
                    "However, it is possible to do this by deleting all the unwanted measurement files from BOTH the local output folder and the instrument output folder. "
                    "You MUST delete the CSV and PNG files from both folders. "
                ),
            },
            "about": {
                "title": "What is Autosa?",
                "content": (
                    "Autosa was developed by Turner Engineering Corporation (Tenco) to automate data acquisition for radiated emissions testing using a signal analyzer."
                ),
            },
            "github_link": {
                "title": "More Information",
                "content": (
                    "For more information about Autosa, including source code, documentation, and updates, visit the official GitHub repository:"
                ),
                "link": {
                    "text": "https://github.com/Turner-Engineering/autosa",
                    "url": "https://github.com/Turner-Engineering/autosa",
                },
            },
        }

    def fill_frame_dynamically(self, frame, section_data):
        """Dynamically fills a frame based on the section data structure"""
        # Create main header
        self.create_header(frame, section_data["title"])

        # Check if this section has subsections or just content
        if "sections" in section_data:
            # Complex section with subsections
            row = 1
            for subsection_key, subsection_data in section_data["sections"].items():
                self.create_subheader(frame, subsection_data["title"], row)
                self.create_body_text(frame, subsection_data["content"], row + 1)
                row += 2
        else:
            # Simple section with just content
            self.create_body_text(frame, section_data["content"], 1)

            # Check if this section has a clickable link
            if "link" in section_data:
                self.create_clickable_link(
                    frame, section_data["link"]["text"], section_data["link"]["url"], 2
                )
