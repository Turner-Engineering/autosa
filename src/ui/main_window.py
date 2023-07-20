import PySimpleGUI as sg

INST_FOUND_KEY = "-INST FOUND-"
INST_NOT_FOUND_KEY = "-INST NOT FOUND-"
RESOURCE_NAME_KEY = "-RESOURCE NAME-"
SETTINGS_VALIDITY_KEY = "-SETTINGS VALIDITY-"


def get_defuault_layout(resource_name):
    section1 = [
        [sg.Text("✅ Instrument Detected", text_color="green")],
        [sg.Text("", text_color="green", key=SETTINGS_VALIDITY_KEY, size=60)],
        [
            sg.Text("Instrument Resource Name:"),
            sg.Text(resource_name, key=RESOURCE_NAME_KEY, size=60),
        ],
        [
            sg.Text(
                "Make sure to check all the fields below before starting the run",
                size=60,
            )
        ],
    ]

    section2 = [
        [
            sg.Text("Band Range:"),
            sg.OptionMenu(
                key="-BAND RANGE-",
                values=["B0 - B4 (monopole)", "B5 - B7 (bilogical)"],
                background_color="white",
            ),
        ],
        [
            sg.Text("Site Name:"),
            sg.Input(
                key="-SITE-",
                default_text="Philly",
            ),
        ],
    ]

    section4 = [
        [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-", default_text="0")],
        [sg.Button("Run Sweeps", disabled=False, key="-RUN-")],
        [sg.ProgressBar(1, orientation="h", size=(60, 20), key="-PROGRESS-")],
    ]

    layout = [
        [sg.B("Settings")],
        *section1,
        [sg.HorizontalSeparator()],
        *section2,
        [sg.HorizontalSeparator()],
        *section4,
    ]

    return layout


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


def get_main_layout(inst_found, resource_name):
    # only one of these will be visible at a time
    default_col = sg.Column(
        get_defuault_layout(resource_name),
        visible=inst_found,
        key=INST_FOUND_KEY,
    )

    inst_not_fount_col = sg.Column(
        get_inst_not_found_layout(),
        visible=not inst_found,
        key=INST_NOT_FOUND_KEY,
    )

    return [[sg.pin(default_col)], [sg.pin(inst_not_fount_col)]]


def update_main_window(window, inst_found, resource_name, settings_error):
    settings_validity_text = (
        "✅ Settings Valid"
        if not settings_error
        else f"❎ Settings Invalid. Please open settings and fix."
    )
    settings_validity_color = "red" if settings_error else "green"

    window[RESOURCE_NAME_KEY].update(resource_name)
    window[INST_FOUND_KEY].update(visible=inst_found)
    window[INST_NOT_FOUND_KEY].update(visible=not inst_found)
    window[SETTINGS_VALIDITY_KEY].update(settings_validity_text)
    window[SETTINGS_VALIDITY_KEY].update(text_color=settings_validity_color)
    return


def get_main_mindow(inst_found, resource_name, finalize=False):
    layout = get_main_layout(inst_found, resource_name)

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
        finalize=finalize,
    )

    return window
