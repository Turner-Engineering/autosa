import PySimpleGUI as sg
import pyvisa

from instrument.instrument import recordMonopoleBands, getInstResource

rm = pyvisa.ResourceManager()
resources = rm.list_resources()


layout = [
    [sg.Text("Begin B1 - B7 Sweeps")],
    [sg.Text("Site Name:"), sg.Input(key="-SITE-", default_text="Philly")],
    [sg.Text("Last Run Index:"), sg.Input(key="-LAST INDEX-", default_text="0")],
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
        siteName = values["-SITE-"]
        lastRunIndex = int(values["-LAST INDEX-"])
        resource = getInstResource(resources)
        recordMonopoleBands(resource, siteName, lastRunIndex)
    if event == sg.WIN_CLOSED:
        break

window.close()
