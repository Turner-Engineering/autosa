import PySimpleGUI as sg


inst_found_text = "Instrument Found ✔️"
inst_not_found_text = "Instrument Not Found ❌"


def get_main_layout(
    inst_found,
    inst_resource,
):
    section1 = [
        [
            sg.Text("Instrument Found:"),
            sg.Text(
                inst_found_text if inst_found else inst_not_found_text,
                key="-INSTRUMENT FOUND-",
            ),
        ],
        [
            sg.Text("Instrument Resource:"),
            sg.Text(inst_resource, key="-INSTRUMENT RESOURCE-", size=(60)),
        ],
        [
            sg.Text(
                "Make sure to check all the fields below before starting the run",
                size=(60),
            ),
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

    return [
        [sg.B("Settings")],
        *section1,
        [sg.HorizontalSeparator()],
        *section2,
        [sg.HorizontalSeparator()],
        section4,
    ]


def update_main_window(window, inst_found, inst_resource):
    output = inst_found_text if inst_found else inst_not_found_text
    window["-INSTRUMENT FOUND-"].update(output)
    window["-INSTRUMENT RESOURCE-"].update(inst_resource)
    return


def get_main_mindow(inst_found, inst_resource):
    layout = get_main_layout(inst_found, inst_resource)

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
    )

    return window
