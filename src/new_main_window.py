import customtkinter as ctk
import json, os
from ui.new_manual_mode import ManualModeFrame
from ui.new_single_band_mode import SingleModeFrame
from ui.new_multi_band_mode import MultiModeFrame
from ui.new_settings_window import SettingsWindow
from ui.new_utils import write_settings_to_json, read_settings_from_json

global SETTINGS_FILE_PATH
SETTINGS_FILE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "Autosa")

ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.5)


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        self.columnconfigure([0, 1], weight=1)
        # self.rowconfigure(0, weight=1)

        title_label = ctk.CTkLabel(self, text="Autosa", font=("", 18))
        title_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)

        settings_button = ctk.CTkButton(
            self, text="Settings", command=lambda: SettingsWindow(self)
        )
        settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=10)

        info_label = ctk.CTkLabel(
            self,
            text=("✅ Instrument Detected\n✅ Settings Valid"),
            text_color="green",
            justify="left",
            anchor="w",
        )
        info_label.grid(row=1, column=0, sticky="W", padx=10, columnspan=2)

        check_label = ctk.CTkLabel(
            self, text="Make sure to check the settings before running anything!"
        )
        check_label.grid(row=3, column=0, sticky="W", padx=10, columnspan=2)


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)  # format to center
        self.rowconfigure(0, weight=1)
        self.create_widgets()

    def create_widgets(self):
        """sets the structure for the different modes"""
        tabview = ctk.CTkTabview(self)
        tabview.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

        # tab formatting
        tab1 = tabview.add("      Manual Mode      ")
        frame = ManualModeFrame(tab1)
        frame.pack(expand=1, fill="both")

        tab2 = tabview.add("      Single Band Mode      ")
        frame = SingleModeFrame(tab2)
        frame.pack(expand=1, fill="both")

        tab3 = tabview.add("      Multi Band Mode      ")
        frame = MultiModeFrame(tab3)
        frame.pack(expand=1, fill="both")


class MainApp(ctk.CTk):
    # Window creation
    def __init__(self):
        super().__init__()
        self.title("Autosa Tkinter")
        window_width = 1200
        window_height = 800
        self.geometry(f"{window_width}x{window_height}")
        self.create_widgets()
        self.iconbitmap("images/autosa_logo.ico")

    def create_widgets(self):
        """sets up the window to have the header and the mode window"""
        top_frame = HeaderFrame(self)
        top_frame.pack(fill="x")

        menu_frame = MenuFrame(self)
        # use a string for "both" to match the fill="x" above
        menu_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    # if os.path.exists(SETTINGS_FILE_PATH):
    #     print(json.dumps(read_settings_from_json(), indent=4))

    app = MainApp()

    # make it non-resizable, Autosa is a simple app and with decent design it shouldn't need to be resized
    app.resizable(False, False)
    app.mainloop()
