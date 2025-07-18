import customtkinter as ctk
import webbrowser

from ui.get_resource_path import resource_path


class HelpWindow(ctk.CTkToplevel):
    def __init__(self, parent, frame_color, label_color):
        super().__init__(parent)
        self.title("Help")
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
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

        self.create_widgets()

    def create_widgets(self):
        """main scrollable frame"""
        main_scroll_frame = ctk.CTkScrollableFrame(self)
        main_scroll_frame.pack(expand=True, fill="both")

        """dynamically create frames based on content structure"""
        content_data = self.get_content_data()
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

    def get_content_data(self):
        """Returns all text content in a structured format"""
        return {
            "about": {
                "title": "What is Autosa?",
                "content": (
                    "Autosa is Tenco software used to automate data acquisition using a signal analyzer (the name is spelled "
                    '"Autosa" or "autosa" and is read as a single word with a stress on the second syllable).'
                ),
            },
            "version": {
                "title": "What version of Autosa is this?",
                "content": (
                    "In the title bar (top left) of the main window, you can find Autosa's current version."
                ),
            },
            "connection": {
                "title": "How do I connect Autosa to the Instrument?",
                "content": (
                    "To connect Autosa to the instrument, please ensure that:\n"
                    "   1. The instrument is plugged in to power and turned on.\n"
                    "   2. The instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable.\n"
                    "   3. Autosa is launched after the instrument is fully on."
                ),
            },
            "connection2": {
                "title": 'How do I fix "No Instrument Detected"?',
                "content": (
                    "1. Ensure that either the instrument or the emulator is fully turned on and running.\n"
                    "2. Relaunch Autosa."
                ),
            },
            "settings_invalid": {
                "title": 'How do I fix "Settings Invalid?"',
                "content": (
                    "1. Ensure either the instrument or emulator is running. If it is not, instrument files will not be detected.\n"
                    "2. Navigate to the Settings window, ensure all entries are valid, and save.\n"
                    "3. If there are still issues, navigate to the top right of Settings window and click the 'Open Settings File Button.'"
                ),
            },
            "amp_corr_tab": {
                "title": "Where can I select/change amplitude corrections?",
                "content": (
                    'Next to the "Primary" tab in the Settings window, there is a "Amplitude Correction" tab where there are dropdown menus for each band.'
                ),
            },
            "measurement": {
                "title": "How do I take measurements with Autosa?",
                "content": (
                    "There are 3 tabs dedecated to measurement: Manual Mode, Single Band Mode, Multi Band Mode.\n"
                    "To take a measurement in Manual Mode:\n"
                    "   1. Ensure all settings are valid.\n"
                    "   2. Navigate to Manual Mode tab.\n"
                    "   3. Select a band to recall the state file and correction file, if applicable.\n"
                    "   4. Begin the measurement using the green button.\n"
                    "   5. Stop the measurement using the red button.\n"
                    "   6. If needed, reset the instrument using the cyan button.\n"
                    "   7. Save the run measurement using the purple button.\n"
                    "   8. Fill out the entry boxes for the filename and save the measurement.\n\n"
                    "To take a measurement in Single Band Mode or Multi Band Mode:\n"
                    "   1. Ensure all settings are valid.\n"
                    "   2. Navigate to the mode's tab.\n"
                    "   3. Input the run note and make selections as applicable.\n"
                    "   4. Measurements can be found in the local and instrument output folder."
                ),
            },
            "buttons": {
                "title": "Where can I find the output folder?",
                "content": (
                    'The "Open Output Folder" button is located below the Settings button and opens the output folder in File Explorer. '
                    "Image files, on the local output folder, can be found in a subfolder sorted by date and band. "
                    'Trace files, on the local output folder, can be found in a subfolder labeled "csv".'
                ),
            },
            "set_up_mode": {
                "title": "What is Set Up Mode?",
                "content": (
                    "Set Up Mode is the 4th tab in Autosa's main window that provides test engineers a efficient way to update states. "
                    "The band buttons recall just the state file. Then, test engineers can make adjustment to the state on Autosa or the instrument. "
                    'Using the "Update State" button, test engineers can update the state through Autosa.'
                ),
            },
            "release_mode": {
                "title": "What is Release Mode?",
                "content": (
                    "Release Mode is the 5th tab in Autosa's main window. Test engineers will need to navigate to this tab to interact with the instrument."
                ),
            },
            "settings_buttons": {
                "title": "Where is the settings file actually located?",
                "content": (
                    "This file might be difficult to find, so within the Settings window there is a button to navigate to it. "
                    'In the top left corner of the Settings window, find the "Open Settings File" button. '
                    "This will open the json settings file in File Explorer."
                ),
            },
            "back_run_id": {
                "title": "How do I reset the Run IDs back to 01?",
                "content": (
                    "If you have alreay ran some measurements but want to reset to back to 01, you will need to manually delete the "
                    "previous files (csv and png) from the local output folder and the instrument output folder. If the file is only "
                    "deleted from the one of the output folders, Autosa will NOT be able to generate the next Run ID."
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
