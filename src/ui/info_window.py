import customtkinter as ctk

from ui.get_resource_path import resource_path


class MoreInfoWindow(ctk.CTkToplevel):
    def __init__(self, parent, frame_color, label_color):
        super().__init__(parent)
        self.title("More Information")
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

        """call to texts"""
        about_frame = self.init_frame(main_scroll_frame, 0)
        connect_frame = self.init_frame(main_scroll_frame, 1)
        main_window_frame = self.init_frame(main_scroll_frame, 2)
        settings_window_frame = self.init_frame(main_scroll_frame, 3)
        saved_files_info_frame = self.init_frame(main_scroll_frame, 4)

        self.fill_about_frame(about_frame)
        self.fill_connect_frame(connect_frame)
        self.fill_main_window_frame(main_window_frame)
        self.fill_settings_window_frame(settings_window_frame)
        self.fill_saved_files_info_frame(saved_files_info_frame)

    def init_frame(self, main_scroll_frame, row):
        about_frame = ctk.CTkFrame(main_scroll_frame, fg_color=self.frame_color)
        about_frame.grid(row=row, column=0, padx=self.padx, pady=0, sticky="ew")
        return about_frame

    def fill_about_frame(self, about_frame):
        about_text = 'Autosa is Tenco software used to automate data acquisition using a signal analyzer (the name is\nspelled "Autosa" or "autosa" and is read as a single word with a stress on the second syllable).'
        ctk.CTkLabel(
            about_frame,
            text="About Autosa",
            font=self.header_font,
            height=0,
        ).grid(row=0, column=0, padx=self.padx, pady=self.header_pady, sticky="nw")
        ctk.CTkLabel(
            about_frame,
            text=about_text,
            font=self.body_font,
            height=0,
            justify="left",
        ).grid(row=1, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

    def fill_connect_frame(self, connect_frame):
        instructions = (
            "To use Autosa, please ensure that the:\n"
            "   1. Instrument is plugged in to power and turned on.\n"
            "   2. Instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable.\n"
            '   3. Emulator is running on the device ("LaunchXSA" on the desktop) if instrument is unavailable.'
        )
        ctk.CTkLabel(
            connect_frame,
            text="Instrument Connection",
            font=self.header_font,
            height=0,
        ).grid(row=0, column=0, padx=self.padx, pady=self.header_pady, sticky="nw")
        ctk.CTkLabel(
            connect_frame,
            text=instructions,
            font=self.body_font,
            height=0,
            justify="left",
        ).grid(row=1, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

    def fill_main_window_frame(self, main_window_frame):
        modes_info = (
            "There are 3 main and 2 supplemental modes:\n"
            "   - Manual Mode: Full control of measurement\n"
            "   - Single Band Mode: Automated measurement for one band\n"
            "   - Multi Band Mode: Automated measurement for a range of band\n"
            "   - Set Up Mode: Adjust and update state file\n"
            "   - Release: Gives control back to the instrument"
        )

        main_window_buttons = (
            "- Settings: Located in the top right corner, this button opens a new window.\n"
            "- Open Output Folder: Located below Settings, this opens the output folder in File Explorer."
        )

        ctk.CTkLabel(
            main_window_frame,
            text="Main Window",
            font=self.header_font,
            height=0,
        ).grid(row=0, column=0, padx=self.padx, pady=self.header_pady, sticky="nw")

        ctk.CTkLabel(
            main_window_frame,
            text="Mode Tabs",
            font=self.subheader_font,
            height=0,
        ).grid(row=1, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            main_window_frame,
            text=modes_info,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=2, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

        ctk.CTkLabel(
            main_window_frame,
            text="Buttons",
            font=self.subheader_font,
            height=0,
        ).grid(row=3, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            main_window_frame,
            text=main_window_buttons,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=4, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

    def fill_settings_window_frame(self, settings_window_frame):
        settings_info = (
            "There are 2 tabs in the Settings Window:\n"
            "   - Primary: This tab contains textboxes to input valid folder paths and sweep duration.\n"
            "   - Amplitude Correct: This tab contains correction file dropdown menus for each band."
        )
        settings_button_info = (
            "- Open Settings File: Located in the top left corner, this opens the json settings file in File Explorer.\n"
            "- Browse: Located in the Primary tab, this opens the file explorer to find the local output folder.\n"
            "- Save: Located in the buttom right corner, this saves the input to the settings file.\n"
            "- Cancel: Located next to Save, this closes the settings window without saving changes."
        )

        ctk.CTkLabel(
            settings_window_frame,
            text="Settings Window Information",
            font=self.header_font,
            height=0,
        ).grid(row=0, column=0, padx=self.padx, pady=self.header_pady, sticky="nw")

        ctk.CTkLabel(
            settings_window_frame,
            text="Tabs",
            font=self.subheader_font,
            height=0,
        ).grid(row=1, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            settings_window_frame,
            text=settings_info,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=2, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

        ctk.CTkLabel(
            settings_window_frame,
            text="Buttons",
            font=self.subheader_font,
            height=0,
        ).grid(row=3, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            settings_window_frame,
            text=settings_button_info,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=4, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

    def fill_saved_files_info_frame(self, saved_files_info_frame):
        run_id_info = (
            "The run ID is a unique identifier for each measurement run generated automatically.\n"
            "   Example: 801-01 Input by Test Engineer 1s B6h 11_21_23"
        )

        saved_files_info = (
            "Autosa saves files in the output folder specified in the settings file.\n"
            "The output folder contains a:\n"
            "   - Trace: This is a CSV of the measurement.\n"
            "   - Screenshot: This is an image of the screen at the end of the measurement.\n"
            "The trace (.csv) file is saved in a sorted folder within the local output folder.\n"
            'The screenshot (.png) file is saved in a folder labelled "CSV" in the local output folder.'
        )

        back_run_id = (
            "If you want the upcoming measurement to have the previous Run ID, you will need to manually delete the\n"
            "previous file (csv and png) from the instrument's output folder.\n"
            "If a file is deleted from the instrument's output folder, it will not be deleted from the local output\nfolder and vice versa.\n"
            "If the file is only deleted from the local output folder, Autosa will not be able to generate the next Run ID."
        )

        ctk.CTkLabel(
            saved_files_info_frame,
            text="Measurement Files Information",
            font=self.header_font,
            justify="left",
            height=0,
        ).grid(row=0, column=0, padx=self.padx, pady=self.header_pady, sticky="nw")

        ctk.CTkLabel(
            saved_files_info_frame,
            text="Run IDs",
            font=self.subheader_font,
            justify="left",
            height=0,
        ).grid(row=1, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            saved_files_info_frame,
            text=run_id_info,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=2, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

        ctk.CTkLabel(
            saved_files_info_frame,
            text="Output Files",
            font=self.subheader_font,
            justify="left",
            height=0,
        ).grid(row=3, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            saved_files_info_frame,
            text=saved_files_info,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=4, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")

        ctk.CTkLabel(
            saved_files_info_frame,
            text="Going Back to Previous Run ID",
            font=self.subheader_font,
            justify="left",
            height=0,
        ).grid(row=5, column=0, padx=self.padx, pady=self.subheader_pady, sticky="nw")
        ctk.CTkLabel(
            saved_files_info_frame,
            text=back_run_id,
            font=self.body_font,
            justify="left",
            height=0,
        ).grid(row=6, column=0, padx=self.padx, pady=self.body_pady, sticky="nw")
