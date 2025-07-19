import customtkinter as ctk

from ui.get_resource_path import resource_path
from ui.ui_logger import LoggingTopLevel


class PyVisaError(LoggingTopLevel):
    def __init__(self, parent, e):
        super().__init__(parent)
        self.title("NI-VISA ERROR")
        window_width = 1170
        window_height = 760
        self.geometry(f"{window_width}x{window_height}")
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient(parent)
        self.e = e

        self.create_widgets()

    def create_widgets(self):
        self.invalid_frame()

    def invalid_frame(self):
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def handle_py_visa_error(self):
        # this is the error code when NI-VISA is not installed
        NI_VISA_ERROR_CODE = -1073807202
        if self.e.error_code == NI_VISA_ERROR_CODE:
            error_text = (
                "Error NI-VISA library not found.",
                "Autosa requires the National Instruments VISA library to be installed.",
                'Please ask Temba for help installing "NI-VISA" or install NI-VISA by searching for "NI-VISA Download" online and following the instructions.',
            )
            ctk.CTkLabel(
                self,
                text="\n".join(error_text),
                font=("", 24),
                wraplength=600,
                justify="left",
            ).grid(row=0, column=0, padx=20, pady=20, sticky="s")
        else:
            error_text = (
                "Error code: " + str(self.e.error_code) + "\n" + self.e.description
            )
            ctk.CTkLabel(
                self,
                text="\n".join(error_text),
                font=("", 24),
                wraplength=600,
                justify="left",
            ).grid(row=0, column=0, padx=20, pady=20, sticky="s")
