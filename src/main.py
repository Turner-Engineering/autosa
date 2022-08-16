import PySimpleGUI as sg
from instrument.instrument import recordMonopoleBands

layout = [
    [sg.Text("Begin B1 - B7 Sweeps")],
    [sg.Text("Site Name:"), sg.Input(key="-site-")],
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
        siteName = values["-site-"]
        lastRunIndex = int(values["-LAST INDEX-"])
        recordMonopoleBands(siteName, lastRunIndex)
    if event == sg.WIN_CLOSED:
        break

window.close()
