import customtkinter as ctk
from ui.invalid_frame import InvalidFrame
from ui.manual_mode import ManualModeFrame
from ui.single_band_mode import SingleModeFrame
from ui.multi_band_mode import MultiModeFrame
from ui.settings_window import SettingsWindow
from ui.get_resource_path import resource_path
from utils.settings import is_settings_valid

ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.5)
# ctk.set_default_color_theme("theme.json")


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent, inst_found, inst):
        super().__init__(parent)
        self.frame_color = parent.frame_color if parent.debug else "#dbdbdb"
        self.label_color = parent.label_color
        self.configure(fg_color=self.frame_color, bg_color=self.frame_color)
        self.columnconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst

        self.valid_settings_label = ctk.CTkLabel(self)
        self.settings_error_var = ctk.StringVar()
        self.settings_error_color = None
        self.update_valid()

        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure([0, 1], weight=1)

        ctk.CTkLabel(
            self,
            text="Autosa",
            font=("", 18),
            fg_color=self.label_color,
        ).grid(row=0, column=0, sticky="w", padx=10, pady=10)

        ctk.CTkButton(
            self,
            text="Settings",
            command=lambda: self.settings_window(),
        ).grid(row=0, column=1, sticky="ne", padx=10, pady=10, rowspan=3)

        inst_found_var = ctk.StringVar(
            value=(
                "✅ Instrument Detected - " + str(self.inst)
                if self.inst_found
                else "❌ Instrument NOT Detected"
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

    def is_valid_settings(self):
        is_valid = is_settings_valid(self.inst)
        return is_valid

    def update_valid(self):
        is_valid = self.is_valid_settings()
        self.settings_error_var.set(
            value=(
                "✅ Settings Valid"
                if is_valid
                else "❌ Settings Invalid. Please change settings."
            )
        )
        self.settings_error_color = "green" if is_valid else "red"
        self.valid_settings_label.configure(text_color=self.settings_error_color)

    def settings_window(self):
        SettingsWindow(self, self.inst, self.update_valid, self.inst_found)


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent, inst_found, inst):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)  # format to center
        self.rowconfigure(0, weight=1)
        self.inst_found = inst_found
        self.inst = inst
        self.frame_color = parent.frame_color
        self.label_color = parent.label_color

        self.create_widgets()

    def create_widgets(self):
        """sets the structure for the different modes"""
        tabview = ctk.CTkTabview(self)
        tabview.grid(row=0, column=0, padx=0, pady=0, sticky="ewns")
        tabview.configure(border_width=2)

        # tab formatting
        tab1 = tabview.add("      Manual Mode      ")
        frame = ManualModeFrame(
            tab1,
            self.inst_found,
            self.inst,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")

        tab2 = tabview.add("      Single Band Mode      ")
        frame = SingleModeFrame(
            tab2,
            self.inst_found,
            self.inst,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")

        tab3 = tabview.add("      Multi Band Mode      ")
        frame = MultiModeFrame(
            tab3,
            self.inst_found,
            self.inst,
            self.frame_color,
            self.label_color,
        )
        frame.pack(expand=1, fill="both")


class MainApp(ctk.CTk):
    # Window creation
    def __init__(self, inst_found, inst):
        super().__init__()
        self.title("Autosa Tkinter")
        window_width = 1170
        window_height = 760
        self.debug = True
        self.debug = False
        if self.debug:
            self.frame_color = "pink"
            self.label_color = "white"
        else:
            self.frame_color = "transparent"
            self.label_color = "transparent"
        self.geometry(f"{window_width}x{window_height}")
        self.logo = resource_path("images/autosa_logo.ico")
        self.iconbitmap(self.logo)

        self.inst_found = inst_found
        self.inst = inst

        self.create_widgets()

    def create_widgets(self):
        """sets up the window to have the header and the mode window"""
        if self.inst_found:
            top_frame = HeaderFrame(self, self.inst_found, self.inst)
            top_frame.pack(fill="x")

            # use a string for "both" to match the fill="x" above
            menu_frame = MenuFrame(self, self.inst_found, self.inst)
            menu_frame.pack(fill="both", expand=True)
        else:
            InvalidFrame.invalid_frame(self)
