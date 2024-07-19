import customtkinter as ctk

from ui.new_manual_mode import ManualModeFrame
from ui.new_single_band_mode import SingleModeFrame
from ui.new_multi_band_mode import MultiModeFrame
from ui.new_settings_window import SettingsWindow

ctk.set_appearance_mode("light")
ctk.set_widget_scaling(1.5)
ctk.set_default_color_theme("theme.json")


class HeaderFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.frame_color = parent.frame_color if parent.debug else "#dbdbdb"
        self.label_color = parent.label_color
        self.configure(fg_color=self.frame_color, bg_color=self.frame_color)
        self.columnconfigure(0, weight=1)
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
            command=lambda: SettingsWindow(self),
        ).grid(row=0, column=1, sticky="ne", padx=10, pady=10, rowspan=3)

        ctk.CTkLabel(
            self,
            text=("✅ Instrument Detected"),
            text_color="green",
            justify="left",
            anchor="w",
            fg_color=self.label_color,
            font=("", 12),
            height=20,
        ).grid(row=1, column=0, sticky="w", padx=10)

        ctk.CTkLabel(
            self,
            text=("✅ Settings Valid"),
            text_color="green",
            justify="left",
            anchor="w",
            fg_color=self.label_color,
            font=("", 12),
            height=20,
        ).grid(row=2, column=0, sticky="w", padx=10)


class MenuFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.columnconfigure(0, weight=1)  # format to center
        self.rowconfigure(0, weight=1)
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
        frame = ManualModeFrame(tab1, self.frame_color, self.label_color)
        frame.pack(expand=1, fill="both")

        tab2 = tabview.add("      Single Band Mode      ")
        frame = SingleModeFrame(tab2, self.frame_color, self.label_color)
        frame.pack(expand=1, fill="both")

        tab3 = tabview.add("      Multi Band Mode      ")
        frame = MultiModeFrame(tab3, self.frame_color, self.label_color)
        frame.pack(expand=1, fill="both")


class MainApp(ctk.CTk):
    # Window creation
    def __init__(self):
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
    app = MainApp()

    # make it non-resizable, Autosa is a simple app and with decent design it shouldn't need to be resized
    app.resizable(False, False)

    # good for debugging, seems not to be recommended for production code
    app.eval("tk::PlaceWindow . center")  # TODO: remove this if it causes issues
    app.mainloop()
