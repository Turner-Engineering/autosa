import PySimpleGUI as sg
import pyvisa

from instrument.instrument import recordBands, getInstResource, getInstFound


def getWindow(bandRangeMonopole, bandRangeBilogical):
    defaultStateFolder = "D:/Users/Instrument/Desktop/Tenco State Files 8-05-2022"
    defaultCorrFolder = "D:/Users/Instrument/Desktop/Tenco Exa Amp Corr"
    defaultOutFolder = "D:/Users/Instrument/Desktop/Test Data"

    layout = [
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
        [sg.HorizontalSeparator()],
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
        [sg.HorizontalSeparator()],
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
        [sg.HorizontalSeparator()],
        [
            sg.Text("Select local data folder"),
            sg.In(size=(60), enable_events=True, key="-LOCAL OUT FOLDER-"),
            sg.FolderBrowse(),
        ],
        [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-", default_text="0")],
        [sg.Button("Run Sweeps")],
        [sg.ProgressBar(1, orientation="h", size=(60, 20), key="-PROGRESS-")],
    ]

    # Create the window
    window = sg.Window(
        "Autosa by Tenco",
        layout,
        margins=(20, 20),
        default_element_size=(20, 1),
        auto_size_text=False,
    )

    return window


def updateWindowInstFound(window, instFound, instResource):
    output = instFoundText if instFound else instNotFoundText
    window["-INSTRUMENT FOUND-"].update(output)
    window["-INSTRUMENT RESOURCE-"].update(instResource)
    return


sg.theme("GrayGrayGray")
rm = pyvisa.ResourceManager()

bandRangeMonopole = "B0 - B4 (monopole)"
bandRangeBilogical = "B5 - B7 (bilogical)"

instResource = getInstResource(rm)
instFound = getInstFound(instResource)
instFoundText = "Instrument Found ✔️"
instNotFoundText = "Instrument Not Found ❌"

window = getWindow(bandRangeMonopole, bandRangeBilogical)

while True:
    timeout = 2000 if instFound else 200
    event, values = window.read(timeout=timeout)
    # without timeout, code pauses here and waits for event
    instResource = getInstResource(rm)
    instFound = getInstFound(instResource)
    updateWindowInstFound(window, instFound, instResource)
    if event == "Run Sweeps":
        # FOLDERS
        folders = {}
        folders["stateFolder"] = values["-STATE FOLDER-"]
        folders["corrFolder"] = values["-CORR FOLDER-"]
        folders["outFolder"] = values["-OUT FOLDER-"]
        folders["localOutFolder"] = values["-LOCAL OUT FOLDER-"]

        # OTHER VARS
        siteName = values["-SITE-"]
        lastRunIndex = int(values["-LAST INDEX-"])
        sweepDur = float(values["-SWEEP DUR-"])

        bandKeys = (
            ["B0", "B1", "B2", "B3", "B4"]
            if values["-BAND RANGE-"] == bandRangeMonopole
            else ["B5", "B6", "B7"]
            if values["-BAND RANGE-"] == bandRangeBilogical
            else ""
        )

        recordBands(
            instResource,
            siteName,
            lastRunIndex,
            folders,
            bandKeys,
            sweepDur,
            window,
        )
    if event == sg.WIN_CLOSED:
        break

window.close()
