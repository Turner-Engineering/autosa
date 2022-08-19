import PySimpleGUI as sg
import pyvisa

from instrument.instrument import recordBands, getInstResource


stateFolder = "D:/Users/Instrument/Desktop/Tenco State Files 8-05-2022"
corrFolder = "D:/Users/Instrument/Desktop/Tenco Exa Amp Corr"
outFolder = "D:/Users/Instrument/Desktop/Test Data"

rm = pyvisa.ResourceManager()
resources = rm.list_resources()


layout = [
    [sg.Text("Begin B1 - B7 Sweeps")],
    [
        sg.Text("Site Name:"),
        sg.Input(
            key="-SITE-",
            default_text="Philly",
        ),
    ],
    [
        sg.Text("States Folder:"),
        sg.Input(key="-STATE FOLDER-", default_text=stateFolder, size=(90)),
    ],
    [
        sg.Text("Corrections Folder:"),
        sg.Input(key="-CORR FOLDER-", default_text=corrFolder, size=(90)),
    ],
    [
        sg.Text("Output Folder:"),
        sg.Input(key="-OUT FOLDER-", default_text=outFolder, size=(90)),
    ],
    [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-", default_text="0")],
    [sg.Button("Run Sweeps")],
]

# Create the window
window = sg.Window("Autosa by Tenco", layout, margins=(100, 50))

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

        resource = getInstResource(resources)
        recordBands(
            resource, siteName, lastRunIndex, stateFolder, corrFolder, outFolder
        )
    if event == sg.WIN_CLOSED:
        break

window.close()
