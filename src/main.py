import PySimpleGUI as sg
import pyvisa

from instrument.instrument import recordBands, getInstResource


stateFolder = "D:/Users/Instrument/Desktop/Tenco State Files 8-05-2022"
corrFolder = "D:/Users/Instrument/Desktop/Tenco Exa Amp Corr"
outFolder = "D:/Users/Instrument/Desktop/Test Data"

rm = pyvisa.ResourceManager()
resources = rm.list_resources()

bandRangeMonopole = "B0 - B4 (monopole)"
bandRangeBilogical = "B5 - B7 (bilogical)"
layout = [
    [
        sg.Text("Make sure to check all the fields below before starting the run"),
    ],
    [
        sg.Text("Band Range"),
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
]

# Create the window
window = sg.Window("Autosa by Tenco", layout, margins=(20, 20))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Run Sweeps":
        siteName = values["-SITE-"]
        lastRunIndex = int(values["-LAST INDEX-"])

        # FOLDERS
        stateFolder = values["-STATE FOLDER-"]
        corrFolder = values["-CORR FOLDER-"]
        outFolder = values["-OUT FOLDER-"]
        controllerOutFolder = values["-LOCAL OUT FOLDER-"]

        bandKeys = (
            ["B0", "B1", "B2", "B3", "B4"]
            if values["-BAND RANGE-"] == bandRangeMonopole
            else ["B5", "B6", "B7"]
            if values["-BAND RANGE-"] == bandRangeBilogical
            else ""
        )

        resource = getInstResource(resources)
        recordBands(
            resource,
            siteName,
            lastRunIndex,
            stateFolder,
            corrFolder,
            outFolder,
            bandKeys,
            controllerOutFolder,
        )
    if event == sg.WIN_CLOSED:
        break

window.close()
