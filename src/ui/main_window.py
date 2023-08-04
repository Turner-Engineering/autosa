import PySimpleGUI as sg
from ui.manual_mode import get_manual_mode_layout
from ui.run_buttons import BAND_KEYS
from ui.single_band_mode import get_single_band_layout
from ui.multi_band_mode import get_multi_band_layout

INST_FOUND_KEY = "-INST FOUND-"
INST_NOT_FOUND_KEY = "-INST NOT FOUND-"
SETTINGS_VALIDITY_KEY = "-SETTINGS VALIDITY-"
INST_FOUND_INFO_KEY = "-INST INFO-"


def get_top_layout():
    return [
        [
            sg.Text("Autosa by Tenco", font=("", 15)),
            sg.Text("", expand_x=True),  # This will push the button to the right
            sg.B("Settings", button_color=("black", "light gray"), size=(10, 2)),
        ],
        [sg.Text("", text_color="green", key=INST_FOUND_INFO_KEY, expand_x=True)],
        [sg.Text("", text_color="green", key=SETTINGS_VALIDITY_KEY, expand_x=True)],
        [
            sg.Text(
                "Make sure to check the settings before running anything!",
                expand_x=True,
            )
        ],
    ]


def get_release_layout():
    text1 = "Instrument Released!"
    text2 = "You can now control the instrument using the front panel."
    return [
        [sg.Text(text1, font=("Any", 40, "bold"), expand_x=True, text_color="green")],
        [sg.Text(text2, font=("", 20), expand_x=True)],
    ]


def get_defuault_layout():
    top_section = get_top_layout()

    multi_band_layout = get_multi_band_layout()

    single_band_layout = get_single_band_layout()

    manual_mode_layout = get_manual_mode_layout()

    release_layout = get_release_layout()

    tabs = [
        sg.Tab("   Manual Mode   ", manual_mode_layout),
        sg.Tab("   Single Band Mode   ", single_band_layout),
        sg.Tab("   Multi Band Mode   ", multi_band_layout),
        sg.Tab("   Release   ", release_layout),
    ]

    tab_group_layout = [[sg.TabGroup([tabs], enable_events=True, key="-TAB GROUP-")]]

    layout = top_section + tab_group_layout

    return layout


def get_inst_not_found_layout():
    steps = [
        "1. The instrument is plugged in to power and turned on",
        "2. The instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable",
        '3. The signal analyzer program is running on the device (called "LaunchXSA" on the desktop)',
    ]

    layout = [
        [
            sg.Text(
                "Instrument Not Detected",
                size=(40, 1),
                text_color="red",
                font=("Helvetica", 16, "bold"),
            )
        ],
        [sg.Text("Make sure:", size=(40, 1))],
        *[[sg.Text(step, size=(80, 1))] for step in steps],
    ]

    return layout


def get_main_layout(inst_found):
    # only one of these will be visible at a time
    default_col = sg.Column(
        get_defuault_layout(),
        visible=inst_found,
        key=INST_FOUND_KEY,
    )

    inst_not_fount_col = sg.Column(
        get_inst_not_found_layout(),
        visible=not inst_found,
        key=INST_NOT_FOUND_KEY,
    )

    return [[sg.pin(default_col)], [sg.pin(inst_not_fount_col)]]


def update_main_window(window, inst_found, inst_info, settings_error, values=None):
    settings_validity_text = (
        "✅ Settings Valid"
        if not settings_error
        else f'❎ Settings Invalid. Please open settings and click "Save" to see error.'
    )
    settings_validity_color = "red" if settings_error else "green"
    inst_found_info_text = "✅ Instrument Detected - " + inst_info

    window[INST_FOUND_KEY].update(visible=inst_found)
    window[INST_NOT_FOUND_KEY].update(visible=not inst_found)
    if not inst_found:
        return
    window[SETTINGS_VALIDITY_KEY].update(settings_validity_text)
    window[SETTINGS_VALIDITY_KEY].update(text_color=settings_validity_color)
    window[INST_FOUND_INFO_KEY].update(inst_found_info_text)
    # check if the band range is B5-B7, if so, show the orientation option

    if values is not None:
        window["-ORIENTATION-"].update(
            disabled=values["-BAND RANGE-"] == "B0 - B4 (monopole)"
        )
    else:
        window["-ORIENTATION-"].update(disabled=True)

    return


def get_main_mindow(inst_found, inst_info, settings_error):
    layout = get_main_layout(inst_found)

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
        finalize=True,
        # icon="images/32x32.ico",
    )
    update_main_window(window, inst_found, inst_info, settings_error)

    return window
