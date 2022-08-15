import PySimpleGUI as sg
from full_run_test import recordMonopoleBands

layout = [
    [sg.Text("Begin B1 - B7 Sweeps")],
    [sg.Text("Location:"), sg.Input(key="-LOCATION-")],
    [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-")],
    [sg.Button("Run")],
]

# Create the window
window = sg.Window("Autosa by Tenco", layout, margins=(100, 50))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Run":
        locationName = values["-LOCATION-"]
        lastRunIndex = int(values["-LAST INDEX-"])
        recordMonopoleBands(locationName, lastRunIndex)
    if event == sg.WIN_CLOSED:
        break

window.close()
