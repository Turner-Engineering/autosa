import PySimpleGUI as sg

INST_FOUND_KEY = "-INST FOUND-"
INST_NOT_FOUND_KEY = "-INST NOT FOUND-"
SETTINGS_VALIDITY_KEY = "-SETTINGS VALIDITY-"
INST_FOUND_INFO_KEY = "-INST INFO-"

BUTTON_DETAILS = [
    {"band": "B0", "freqs": "10 kHz - 160 kHz"},
    {"band": "B1", "freqs": "150 kHz - 650 kHz"},
    {"band": "B2", "freqs": "500 kHz - 3 MHz"},
    {"band": "B3", "freqs": "2.5 MHz - 7.5 MHz"},
    {"band": "B4", "freqs": "5 MHz - 30 MHz"},
    {"band": "B5", "freqs": "25 MHz - 325 MHz"},
    {"band": "B6", "freqs": "300 MHz - 1.3 GHz"},
    {"band": "B7", "freqs": "1 GHz - 6 GHz"},
]


RUN_BUTTON_PROPS = {
    "font": "Any 15",
    "button_color": ("white", "dark blue"),
    "size": (15, 2),
}


def get_section1():
    return [
        [sg.Text("", text_color="green", key=INST_FOUND_INFO_KEY, expand_x=True)],
        [sg.Text("", text_color="green", key=SETTINGS_VALIDITY_KEY, expand_x=True)],
        [
            sg.Text(
                "Make sure to check the settings before running anything!",
                expand_x=True,
            )
        ],
    ]


def get_multi_band_section():
    return [
        [
            sg.Text(
                "Multi-Band mode allows you to run multiple bands in a row with no intervention.",
                expand_x=True,
            )
        ],
        [
            sg.Text(
                "State files, correction files, coupling, and file names are set automatically.",
                expand_x=True,
            )
        ],
        [
            sg.Text("Band Range:"),
            sg.OptionMenu(
                key="-BAND RANGE-",
                values=["B0 - B4 (monopole)", "B5 - B7 (bilogical)"],
                background_color="white",
                default_value="B0 - B4 (monopole)",
            ),
        ],
        [
            sg.Text("Orientation:"),
            sg.OptionMenu(
                key="-ORIENTATION-",
                values=["Horizontal", "Vertical"],
                default_value="Horizontal",
                disabled=True,
            ),
        ],
        [
            sg.Button(
                "Run Sweeps",
                disabled=True,
                key="-RUN-",
                **RUN_BUTTON_PROPS,
            )
        ],
        [
            sg.ProgressBar(
                1, orientation="h", size=(60, 20), key="-PROGRESS-", expand_x=True
            )
        ],
    ]


def get_band_button(band_key, orientation=""):
    return sg.Button(
        band_key + orientation,
        key=f"-BUTTON {band_key} {orientation}-",
        font=RUN_BUTTON_PROPS["font"],
        button_color=RUN_BUTTON_PROPS["button_color"],
        size=(12, 2),
        expand_x=True,
    )


def get_single_band_section():
    monopole_buttons = [get_band_button(b["band"]) for b in BUTTON_DETAILS[0:5]]
    bilogical_buttons_h = [get_band_button(b["band"], "h") for b in BUTTON_DETAILS[5:8]]
    bilogical_buttons_v = [get_band_button(b["band"], "v") for b in BUTTON_DETAILS[5:8]]

    # arrange section 4 such that there are two rows for 4 buttons
    section = [
        [sg.Text("Single Band Mode lets you run one band at a time.", expand_x=True)],
        [
            sg.Text(
                "State files, correction files, coupling, and file names are set automatically.",
                expand_x=True,
            )
        ],
        [sg.Text("")],
        [sg.Text("Monopole Bands:", expand_x=True, font="Any 15")],
        monopole_buttons,
        [sg.Text("")],
        [sg.Text("Bilogical Bands:", expand_x=True, font="Any 15")],
        bilogical_buttons_h,
        bilogical_buttons_v,
    ]
    return section


def get_custom_mode_section():
    button = sg.Button(
        "Record and Save",
        key="-RECORD AND SAVE-",
        **RUN_BUTTON_PROPS,
    )

    # arrange section 4 such that there are two rows for 4 buttons
    section = [
        [
            sg.Text(
                "Record and Save will record a sweep using the current instrument settings as set up by the user.\n\n",
                expand_x=True,
            )
        ],
        [
            sg.Text(
                "It will not load state files or correction files. This is helpful for customized runs.",
                expand_x=True,
            )
        ],
        [button],
    ]
    return section


def get_defuault_layout():
    section1 = get_section1()

    multi_band_section = get_multi_band_section()

    single_band_section = get_single_band_section()

    custom_mode_section = get_custom_mode_section()

    setup_layout = [
        [
            sg.Text("Autosa by Tenco", font=("", 15)),
            sg.Text("", expand_x=True),  # This will push the button to the right
            sg.B("Settings", button_color=("black", "light gray"), size=(10, 2)),
        ],
        *section1,
    ]

    tabs = [
        sg.Tab("   Single Band Mode   ", single_band_section),
        sg.Tab("   Multi Band Mode   ", multi_band_section),
        sg.Tab("   Custom Mode   ", custom_mode_section),
    ]

    tab_group_layout = [[sg.TabGroup([tabs])]]

    layout = setup_layout + tab_group_layout

    return layout


def set_band_button_disabled(window, disabled):
    disabled_color = ("white", "grey")
    enabled_color = ("white", "dark blue")
    button_color = disabled_color if disabled else enabled_color
    for b in BUTTON_DETAILS:
        window[f"-BUTTON {b['band']}-"].update(disabled=disabled)
        window[f"-BUTTON {b['band']}-"].update(button_color=button_color)


def get_inst_not_found_layout():
    steps = [
        "1. Make sure the instrument is plugged in to power and turned on",
        "2. Make sure the instrument is connected to this computer via USB-B (back of instrument) to USB-A (computer) cable",
        '3. Make sure the signal analyzer program is running on the device (may be called "LaunchXSA" on the desktop)',
        "4. Ask for help",
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
        [sg.Text("Steps to fix:", size=(40, 1))],
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


def update_main_window(window, inst_found, inst_info, settings_error, values):
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
    update_main_window(window, inst_found, inst_info, settings_error, None)

    return window
