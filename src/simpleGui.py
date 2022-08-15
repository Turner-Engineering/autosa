import PySimpleGUI as sg
from full_run_test import main

layout = [[sg.Text("Begin B1 - B7 Sweeps")], [sg.Button("Run")]]

# Create the window
window = sg.Window("Demo", layout, margins=(100, 50))

# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Run":
        main()
    if event == sg.WIN_CLOSED:
        break

window.close()
