import PySimpleGUI as sg
from instrument.instrument import create_run_filename

RUN_ID_KEY = "-RUN ID-"
RUN_NOTE_KEY = "-RUN NOTE-"
BAND_NAME_KEY = "-BAND NAME-"
RUN_FILENAME_CSV_KEY = "-RUN FILENAME CSV-"
RUN_FILENAME_PNG_KEY = "-RUN FILENAME PNG-"


def get_window_layout(run_id):
    col1 = [
        [sg.Text("Run ID:")],
        [sg.InputText(run_id, key=RUN_ID_KEY, size=(15, 1), disabled=True)],
    ]
    col2 = [
        [sg.Text("Run Note:")],
        [sg.InputText(key=RUN_NOTE_KEY, size=(30, 1), enable_events=True)],
    ]
    col3 = [
        [sg.Text("Band:")],
        [sg.InputText(key=BAND_NAME_KEY, size=(5, 1), enable_events=True)],
    ]
    col4 = [
        [sg.Text("Extension")],
        [sg.InputText(size=(10, 1), disabled=True, default_text=".csv/.png")],
    ]

    layout = [
        [sg.Column(col1), sg.Column(col2), sg.Column(col3), sg.Column(col4)],
        [sg.Text("Trace Filename:"), sg.Text("", key=RUN_FILENAME_CSV_KEY)],
        [sg.Text("Screen Filename:"), sg.Text("", key=RUN_FILENAME_PNG_KEY)],
        [sg.Button("Ok"), sg.Button("Cancel")],
    ]

    return layout


def get_filename(values):
    run_id = values[RUN_ID_KEY].strip()
    run_note = values[RUN_NOTE_KEY].strip()
    band_name = values[BAND_NAME_KEY].strip()
    run_filename = create_run_filename(run_id, run_note, band_name, "")
    return run_filename


def update_window(window, run_filename):
    window[RUN_FILENAME_CSV_KEY].update(run_filename + ".csv")
    window[RUN_FILENAME_PNG_KEY].update(run_filename + ".png")


def get_filename_from_user(run_id):
    layout = get_window_layout(run_id)
    window = sg.Window("Create filename", layout)

    while True:
        event, values = window.read()
        if event == RUN_NOTE_KEY or event == BAND_NAME_KEY:
            run_filename = get_filename(values)
            update_window(window, run_filename)
        elif event == "Ok":
            if values[RUN_NOTE_KEY].strip() == "":
                sg.Popup("Please enter a Run Note")
            else:
                run_filename = get_filename(values)
                break
        elif event == sg.WINDOW_CLOSED or event == "Cancel":
            run_filename = None
            break

    window.close()
    return run_filename
