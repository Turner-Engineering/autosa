import PySimpleGUI as sg
import pyvisa

from instrument.instrument import getInstFound, getInstResource, recordBandsDebug
from ui.mainWindow import getMainWindow, updateMainWindow
from ui.settingsWindow import launchSettingsWindow


def getFolders():
    folders = {}
    folders["stateFolder"] = sg.user_settings_get_entry("-STATE FOLDER-")
    folders["corrFolder"] = sg.user_settings_get_entry("-CORR FOLDER-")
    folders["outFolder"] = sg.user_settings_get_entry("-OUT FOLDER-")
    folders["localOutFolder"] = sg.user_settings_get_entry("-LOCAL OUT FOLDER-")
    return folders


def validateInput(values):
    if values["-BAND RANGE-"] == "":
        return False
    if values["-SITE-"] == "":
        return False
    return True


def main():
    sg.theme("SystemDefaultForReal")
    # default location for this file is Users/<username>/AppData/Local/PySimpleGUI/settings/
    sg.user_settings_filename("autosa.json")
    rm = pyvisa.ResourceManager()

    instResource = getInstResource(rm)
    instFound = getInstFound(instResource)

    mainWindow = getMainWindow(instFound, instResource)

    while True:
        timeout = 2000 if instFound else 200
        event, values = mainWindow.read(timeout=timeout)
        # without timeout, code pauses here and waits for event
        instResource = getInstResource(rm)
        instFound = getInstFound(instResource)
        updateMainWindow(mainWindow, instFound, instResource)

        if event == "Settings":
            settingsChanged = launchSettingsWindow()
            if settingsChanged:
                mainWindow.close()
                mainWindow = getMainWindow(instFound, instResource)
        elif event == sg.WIN_CLOSED:
            break

        inputValid = validateInput(values)
        if not inputValid:
            mainWindow["-RUN-"].update(disabled=True)
            continue
        else:
            mainWindow["-RUN-"].update(disabled=False)

        if event == "-RUN-":
            # FOLDERS
            folders = getFolders()

            # OTHER VARS
            siteName = values["-SITE-"]
            lastRunIndex = int(values["-LAST INDEX-"])
            sweepDur = float(sg.user_settings_get_entry("-SWEEP DUR-"))

            bandKeys = (
                ["B0", "B1", "B2", "B3", "B4"]
                if values["-BAND RANGE-"] == "B0 - B4 (monopole)"
                else ["B5", "B6", "B7"]
                if values["-BAND RANGE-"] == "B5 - B7 (bilogical)"
                else ""
            )

            recordBandsDebug(
                instResource,
                siteName,
                lastRunIndex,
                folders,
                bandKeys,
                sweepDur,
                mainWindow,
            )

    mainWindow.close()


if __name__ == "__main__":
    main()
