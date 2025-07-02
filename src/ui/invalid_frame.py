import customtkinter as ctk
from ui.get_resource_path import resource_path


class InvalidFrame(ctk.CTkToplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("INSTRUMENT DISCONNECTED")
        window_width = 1170
        window_height = 760
        self.geometry(f"{window_width}x{window_height}")
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.transient(parent)

        self.create_widgets()

    def create_widgets(self):
        self.invalid_frame()

    def invalid_frame(self):
        self.rowconfigure([0, 1], weight=1)
        self.columnconfigure(0, weight=1)
        instructions = (
            "1. The instrument is plugged in to power and turned on\n",
            "2. The instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable\n",
            '3. The signal analyzer program is running on the device (called "LaunchXSA" on the desktop)',
        )

        label_frame = ctk.CTkFrame(self)
        label_frame.grid(row=0, column=0, sticky="nsew")
        label_frame.rowconfigure(0, weight=1)
        label_frame.columnconfigure(0, weight=1)

        instructions_frame = ctk.CTkFrame(self)
        instructions_frame.grid(row=1, column=0, sticky="nsew")
        instructions_frame.rowconfigure(0, weight=1)
        instructions_frame.columnconfigure(0, weight=1)

        ctk.CTkLabel(
            label_frame,
            text="❌ Instrument NOT Detected",
            text_color="red",
            font=("", 48),
        ).grid(row=0, column=0, padx=20, pady=20, sticky="s")

        ctk.CTkLabel(
            instructions_frame,
            text="\n".join(instructions),
            text_color="black",
            font=("", 24),
            wraplength=600,
            justify="left",
        ).grid(row=0, column=0, padx=20, pady=20, sticky="n")


class PyVisaError(ctk.CTkToplevel):
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
