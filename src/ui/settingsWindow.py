import PySimpleGUI as sg


def getFolderSetting(field):
    defaultText = sg.user_settings_get_entry(field["key"], field["default"])

    folderSetting = [
        sg.Text(field["label"] + ":"),
        sg.Input(key=field["key"], default_text=defaultText, size=(60)),
    ]
    if "browse" in field:
        folderSetting.append(sg.FolderBrowse())
    return folderSetting


def getFolderSettings():
    folderFields = [
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

    folderSettings = [[sg.Text("Folders", font=("", 15))]]
    for field in folderFields:
        folderSetting = getFolderSetting(field)
        folderSettings.append(folderSetting)
    return folderSettings


def getSettingsWindow():
    folderSettings = getFolderSettings()

    layout = [
        [sg.Text("Settings", font=("_ 25"))],
        [sg.HorizontalSeparator()],
        folderSettings,
        [sg.HorizontalSeparator()],
        [sg.Button("Save"), sg.Button("Cancel")],
    ]

    window = sg.Window(
        "Settings", layout, default_element_size=(20, 1), auto_size_text=False
    )
    return window


def launchSettingsWindow():
    window = getSettingsWindow()
    settingsChanged = False
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "Save":
            sg.user_settings_set_entry("-STATE FOLDER-", values["-STATE FOLDER-"])
            sg.user_settings_set_entry("-CORR FOLDER-", values["-CORR FOLDER-"])
            sg.user_settings_set_entry("-OUT FOLDER-", values["-OUT FOLDER-"])
            sg.user_settings_set_entry(
                "-LOCAL OUT FOLDER-", values["-LOCAL OUT FOLDER-"]
            )
            settingsChanged = True
            break

    window.close()

    return settingsChanged
