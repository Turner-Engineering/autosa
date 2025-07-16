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
        self.window_width = 760
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
                "title": "About Autosa",
                "content": (
                    "Autosa is Tenco software used to automate data acquisition using a signal analyzer (the name is\n"
                    'spelled "Autosa" or "autosa" and is read as a single word with a stress on the second syllable).'
                ),
            },
            "connection": {
                "title": "Instrument Connection",
                "content": (
                    "To use Autosa, please ensure that the:\n"
                    "   1. Instrument is plugged in to power and turned on.\n"
                    "   2. Instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable.\n"
                    '   3. Emulator is running on the device ("LaunchXSA" on the desktop) if instrument is unavailable.'
                ),
            },
            "main_window": {
                "title": "Main Window",
                "sections": {
                    "mode_tabs": {
                        "title": "Mode Tabs",
                        "content": (
                            "There are 3 main and 2 supplemental modes:\n"
                            "   - Manual Mode: Full control of measurement\n"
                            "   - Single Band Mode: Automated measurement for one band\n"
                            "   - Multi Band Mode: Automated measurement for a range of band\n"
                            "   - Set Up Mode: Adjust and update state file\n"
                            "   - Release: Gives control back to the instrument"
                        ),
                    },
                    "buttons": {
                        "title": "Buttons",
                        "content": (
                            "- Settings: Located in the top right corner, this button opens a new window.\n"
                            "- Open Output Folder: Located below Settings, this opens the output folder in File Explorer."
                        ),
                    },
                },
            },
            "settings_window": {
                "title": "Settings Window Information",
                "sections": {
                    "tabs": {
                        "title": "Tabs",
                        "content": (
                            "There are 2 tabs in the Settings Window:\n"
                            "   - Primary: This tab contains textboxes to input valid folder paths and sweep duration.\n"
                            "   - Amplitude Correct: This tab contains correction file dropdown menus for each band."
                        ),
                    },
                    "buttons": {
                        "title": "Buttons",
                        "content": (
                            "- Open Settings File: Located in the top left corner, this opens the json settings file in File Explorer.\n"
                            "- Browse: Located in the Primary tab, this opens the file explorer to find the local output folder.\n"
                            "- Save: Located in the buttom right corner, this saves the input to the settings file.\n"
                            "- Cancel: Located next to Save, this closes the settings window without saving changes."
                        ),
                    },
                },
            },
            "measurement_files": {
                "title": "Measurement Files Information",
                "sections": {
                    "run_ids": {
                        "title": "Run IDs",
                        "content": (
                            "The run ID is a unique identifier for each measurement run generated automatically.\n"
                            "   Example: 801-01 Input by Test Engineer 1s B6h 11_21_23"
                        ),
                    },
                    "output_files": {
                        "title": "Output Files",
                        "content": (
                            "Autosa saves files in the output folder specified in the settings file.\n"
                            "The output folder contains a:\n"
                            "   - Trace: This is a CSV of the measurement.\n"
                            "   - Screenshot: This is an image of the screen at the end of the measurement.\n"
                            "The trace (.csv) file is saved in a sorted folder within the local output folder.\n"
                            'The screenshot (.png) file is saved in a folder labelled "CSV" in the local output folder.'
                        ),
                    },
                    "back_run_id": {
                        "title": "Going Back to Previous Run ID",
                        "content": (
                            "If you want the upcoming measurement to have the previous Run ID, you will need to manually delete the\n"
                            "previous file (csv and png) from the instrument's output folder.\n"
                            "If a file is deleted from the instrument's output folder, it will not be deleted from the local output\n"
                            "folder and vice versa.\n"
                            "If the file is only deleted from the local output folder, Autosa will not be able to generate the next Run ID."
                        ),
                    },
                },
            },
            "github_link": {
                "title": "More Information",
                "content": (
                    "For more information about Autosa, including source code, documentation, and updates, "
                    "visit the official GitHub repository:"
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
