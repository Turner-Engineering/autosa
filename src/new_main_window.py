# TODO convert to using classes

import customtkinter as ctk
from ui.new_manual_mode import get_manual_mode_layout
from ui.new_single_band_mode import get_single_band_layout
from ui.new_multi_band_mode import get_multi_band_layout
from ui.new_settings_window import get_settings_window

SETTINGS_VALIDITY_KEY = "-SETTINGS VALIDITY-"
INST_FOUND_INFO_KEY = "-INST INFO-"

# window creation
window = ctk.CTk()
window.title("Autosa by Tenco")
window.geometry("1200x720")
window.columnconfigure(0, weight=1)
window.rowconfigure(0, weight=1)
window.iconbitmap("images/autosa_logo.ico")
ctk.set_widget_scaling(1.5)


# first frame of the window
def get_top_layout(top_frame):
    top_frame.columnconfigure([0, 1], weight=1)
    # top_frame.rowconfigure(0, weight=1)

    title_label = ctk.CTkLabel(top_frame, text="Autosa", font=("", 18))
    title_label.grid(row=0, column=0, sticky="W", padx=10, pady=10)

    settings_button = ctk.CTkButton(
        top_frame, text="Settings", command=lambda: get_settings_window(window)
    )
    settings_button.grid(row=0, column=1, sticky="E", padx=10, pady=10)

    info_label = ctk.CTkLabel(
        top_frame,
        text=(f"{INST_FOUND_INFO_KEY}\n" f"{SETTINGS_VALIDITY_KEY}"),
        text_color="green",
        justify="left",
        anchor="w",
    )
    info_label.grid(row=1, column=0, sticky="W", padx=10, columnspan=2)

    check_label = ctk.CTkLabel(
        top_frame, text="Make sure to check the settings before running anything!"
    )
    check_label.grid(row=3, column=0, sticky="W", padx=10, columnspan=2)


def menu_layout(menu_frame):
    """menu_layout(menu_frame) sets the structure for the different modes"""
    # format to center
    menu_frame.columnconfigure(0, weight=1)
    menu_frame.rowconfigure(0, weight=1)

    tabview = ctk.CTkTabview(menu_frame)
    tabview.grid(row=0, column=0, padx=10, pady=10, sticky="ew")

    # tab formatting
    manual_tab = tabview.add("      Manual Mode      ")
    single_tab = tabview.add("      Single Band Mode      ")
    multi_tab = tabview.add("      Multi Band Mode      ")

    # MANUAL MODE
    get_manual_mode_layout(manual_tab)

    # single band mode
    get_single_band_layout(single_tab)

    # multi band mode
    get_multi_band_layout(multi_tab, window)


def main():
    """main() sets the structure of the window into two parts"""
    top_frame = ctk.CTkFrame(window, border_width=2, fg_color="pink")
    top_frame.grid(row=0, column=0, sticky="ew")
    get_top_layout(top_frame)

    menu_frame = ctk.CTkFrame(window, border_width=2, fg_color="blue")
    menu_frame.grid(row=1, column=0, sticky="ew")
    menu_layout(menu_frame)

    window.mainloop()


if __name__ == "__main__":
    main()
