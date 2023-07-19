import PySimpleGUI as sg


def get_folder_setting(field):
    detault_text = sg.user_settings_get_entry(field["key"], field["default"])

    folder_setting = [
        sg.Text(field["label"] + ":"),
        sg.Input(key=field["key"], default_text=detault_text, size=(60)),
    ]
    if "browse" in field:
        folder_setting.append(sg.FolderBrowse())
    return folder_setting


def get_folder_settings():
    folder_fields = [
        {
            "key": "-STATE FOLDER-",
            "label": "State Folder",
            "default": "D:/Users/Instrument/Desktop/State Files",
        },
        {
            "key": "-CORR FOLDER-",
            "label": "Corr Folder",
            "default": "D:/Users/Instrument/Desktop/Correction Files",
        },
        {
            "key": "-OUT FOLDER-",
            "label": "Out Folder",
            "default": "D:/Users/Instrument/Desktop/Test Data",
        },
        {
            "key": "-LOCAL OUT FOLDER-",
            "label": "Local Out Folder",
            "default": "",
            "browse": True,
        },
    ]

    folder_settings = [[sg.Text("Folders", font=("", 15))]]
    for field in folder_fields:
        folder_setting = get_folder_setting(field)
        folder_settings.append(folder_setting)
    return folder_settings


def get_other_settings():
    sweep_dur_default = sg.user_settings_get_entry("-SWEEP DUR-", 5)
    sweep_dur_default = sweep_dur_default
    layout = [
        [sg.Text("Other", font=("", 15))],
        [
            sg.Text("Sweep Duration (s):"),
            sg.Input(key="-SWEEP DUR-", default_text=sweep_dur_default),
        ],
    ]
    return layout


def get_settings_window():
    folder_settings = get_folder_settings()
    other_settings = get_other_settings()

    layout = [
        [sg.Text("Settings", font=("_ 25"))],
        [sg.HorizontalSeparator()],
        folder_settings,
        [sg.HorizontalSeparator()],
        other_settings,
        [sg.HorizontalSeparator()],
        [sg.Button("Save"), sg.Button("Cancel")],
    ]

    window = sg.Window(
        "Settings", layout, default_element_size=(20, 1), auto_size_text=False
    )
    return window


def save_settings(values):
    keys = [
        "-STATE FOLDER-",
        "-CORR FOLDER-",
        "-OUT FOLDER-",
        "-LOCAL OUT FOLDER-",
        "-SWEEP DUR-",
    ]
    for key in keys:
        sg.user_settings_set_entry(key, values[key])


def launch_settings_window():
    window = get_settings_window()
    settings_changed = False
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "Save":
            save_settings(values)
            settings_changed = True  # used as flag to update main window
            break

    window.close()

    return settings_changed
