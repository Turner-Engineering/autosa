import PySimpleGUI as sg
import pyvisa

from instrument.instrument import recordBands, getInstResource


sg.theme("GrayGrayGray")

stateFolder = "D:/Users/Instrument/Desktop/Tenco State Files 8-05-2022"
corrFolder = "D:/Users/Instrument/Desktop/Tenco Exa Amp Corr"
outFolder = "D:/Users/Instrument/Desktop/Test Data"

rm = pyvisa.ResourceManager()

bandRangeMonopole = "B0 - B4 (monopole)"
bandRangeBilogical = "B5 - B7 (bilogical)"

instFound = False
instResource = ""
instFoundText = "Instrument Found ✔️"
instNotFoundText = "Instrument Not Found ❌"

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
            "Make sure to check all the fields below before starting the run", size=(60)
        ),
    ],
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
    [
        sg.Text("States Folder:"),
        sg.Input(key="-STATE FOLDER-", default_text=stateFolder, size=(60)),
    ],
    [
        sg.Text("Corrections Folder:"),
        sg.Input(key="-CORR FOLDER-", default_text=corrFolder, size=(60)),
    ],
    [
        sg.Text("Instrument Output Folder:"),
        sg.Input(key="-OUT FOLDER-", default_text=outFolder, size=(60)),
    ],
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


def updateInstFound(instResource):
    instFound = True if instResource != "" else False
    window["-INSTRUMENT FOUND-"].update(
        instFoundText if instFound else instNotFoundText,
    )
    window["-INSTRUMENT RESOURCE-"].update(instResource)
    return instFound


while True:
    timeout = 2000 if instFound else 200
    event, values = window.read(timeout=timeout)
    # without timeout, code pauses here and waits for event
    instResource = getInstResource(rm)
    instFound = updateInstFound(instResource)
    if event == "Run Sweeps":
        siteName = values["-SITE-"]
        lastRunIndex = int(values["-LAST INDEX-"])

        # FOLDERS
        stateFolder = values["-STATE FOLDER-"]
        corrFolder = values["-CORR FOLDER-"]
        outFolder = values["-OUT FOLDER-"]
        controllerOutFolder = values["-LOCAL OUT FOLDER-"]
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
            stateFolder,
            corrFolder,
            outFolder,
            bandKeys,
            controllerOutFolder,
            sweepDur,
            window,
        )
    if event == sg.WIN_CLOSED:
        break

window.close()
