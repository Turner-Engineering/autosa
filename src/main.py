import PySimpleGUI as sg
import pyvisa

from instrument.instrument import recordBands, getInstResource, getInstFound
from ui.mainWindow import updateMainWindow, getMainWindow


def getFolders(values):
    folders = {}
    folders["stateFolder"] = values["-STATE FOLDER-"]
    folders["corrFolder"] = values["-CORR FOLDER-"]
    folders["outFolder"] = values["-OUT FOLDER-"]
    folders["localOutFolder"] = values["-LOCAL OUT FOLDER-"]
    return folders


def main():
    sg.theme("GrayGrayGray")
    rm = pyvisa.ResourceManager()

    bandRangeMonopole = "B0 - B4 (monopole)"
    bandRangeBilogical = "B5 - B7 (bilogical)"

    instResource = getInstResource(rm)
    instFound = getInstFound(instResource)

    mainWindow = getMainWindow(
        instFound, instResource, bandRangeMonopole, bandRangeBilogical
    )

    while True:
        timeout = 2000 if instFound else 200
        event, values = mainWindow.read(timeout=timeout)
        # without timeout, code pauses here and waits for event
        instResource = getInstResource(rm)
        instFound = getInstFound(instResource)
        updateMainWindow(mainWindow, instFound, instResource)
        if event == "Run Sweeps":
            # FOLDERS
            folders = getFolders(values)

            # OTHER VARS
            siteName = values["-SITE-"]
            lastRunIndex = int(values["-LAST INDEX-"])
            sweepDur = float(values["-SWEEP DUR-"])

            bandKeys = (
                ["B0", "B1", "B2", "B3", "B4"]
                if values["-BAND RANGE-"] == bandRangeMonopole
                else ["B5", "B6", "B7"]
                if values["-BAND RANGE-"] == bandRangeBilogical
                else ""
            )

            recordBands(
                instResource,
                siteName,
                lastRunIndex,
                folders,
                bandKeys,
                sweepDur,
                mainWindow,
            )
        if event == sg.WIN_CLOSED:
            break

    mainWindow.close()


if __name__ == "__main__":
    main()
