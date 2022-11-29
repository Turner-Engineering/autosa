import PySimpleGUI as sg


instFoundText = "Instrument Found ✔️"
instNotFoundText = "Instrument Not Found ❌"


def getMainLayout(
    instFound,
    instResource,
    bandRangeMonopole,
    bandRangeBilogical,
):

    defaultStateFolder = "D:/Users/Instrument/Desktop/Tenco State Files 8-05-2022"
    defaultCorrFolder = "D:/Users/Instrument/Desktop/Tenco Exa Amp Corr"
    defaultOutFolder = "D:/Users/Instrument/Desktop/Test Data"

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
            sg.Text("Sweep Duration (s):"),
            sg.Input(key="-SWEEP DUR-", default_text="5"),
        ],
        [
            sg.Text("Band Range:"),
            sg.OptionMenu(
                key="-BAND RANGE-", values=[bandRangeMonopole, bandRangeBilogical]
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

    section3 = [
        [
            sg.Text("States Folder:"),
            sg.Input(key="-STATE FOLDER-", default_text=defaultStateFolder, size=(60)),
        ],
        [
            sg.Text("Corrections Folder:"),
            sg.Input(key="-CORR FOLDER-", default_text=defaultCorrFolder, size=(60)),
        ],
        [
            sg.Text("Instrument Output Folder:"),
            sg.Input(key="-OUT FOLDER-", default_text=defaultOutFolder, size=(60)),
        ],
        [
            sg.Text("Local Output Folder"),
            sg.In(size=(60), enable_events=True, key="-LOCAL OUT FOLDER-"),
            sg.FolderBrowse(),
        ],
    ]

    section4 = [
        [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-", default_text="0")],
        [sg.Button("Run Sweeps")],
        [sg.ProgressBar(1, orientation="h", size=(60, 20), key="-PROGRESS-")],
    ]

    return [
        *section1,
        [sg.HorizontalSeparator()],
        *section2,
        [sg.HorizontalSeparator()],
        *section3,
        [sg.HorizontalSeparator()],
        section4,
    ]


def updateMainWindow(window, instFound, instResource):
    output = instFoundText if instFound else instNotFoundText
    window["-INSTRUMENT FOUND-"].update(output)
    window["-INSTRUMENT RESOURCE-"].update(instResource)
    return


def getMainWindow(instFound, instResource, bandRangeMonopole, bandRangeBilogical):
    layout = getMainLayout(
        instFound, instResource, bandRangeMonopole, bandRangeBilogical
    )

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
    )

    return window
