import PySimpleGUI as sg


instFoundText = "Instrument Found ✔️"
instNotFoundText = "Instrument Not Found ❌"


def getMainLayout(
    instFound,
    instResource,
):

    section1 = [
        [
            sg.Text("Instrument Found:"),
            sg.Text(
                instFoundText if instFound else instNotFoundText,
                key="-INSTRUMENT FOUND-",
            ),
        ],
        [
            sg.Text("Instrument Resource:"),
            sg.Text(instResource, key="-INSTRUMENT RESOURCE-", size=(60)),
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
                key="-BAND RANGE-", values=["B0 - B4 (monopole)", "B5 - B7 (bilogical)"]
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
        [sg.Button("Run Sweeps")],
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


def updateMainWindow(window, instFound, instResource):

    output = instFoundText if instFound else instNotFoundText
    window["-INSTRUMENT FOUND-"].update(output)
    window["-INSTRUMENT RESOURCE-"].update(instResource)
    return


def getMainWindow(instFound, instResource):
    layout = getMainLayout(instFound, instResource)

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
    )

    return window
