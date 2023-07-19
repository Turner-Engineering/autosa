import datetime
import time

import pyvisa

from bandsData import bands
from instrument.fileTransfer import saveFileToLocal


def getInstResource(resourceManager):
    resources = resourceManager.list_resources()
    usbResources = [r for r in resources if "USB" in r]
    instUsbResources = [r for r in usbResources if "::INSTR" in r]
    instResource = "" if len(instUsbResources) == 0 else instUsbResources[0]
    return instResource


def getInstFound(instResource):
    return True if instResource != "" else False


def getInst(instResource):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(instResource)
    return inst


def recordBand(inst, folder, filename, localOutFolder, sweepDur=5):
    # RECORD
    inst.write(":INIT:REST")
    inst.write(":INIT:CONT ON")
    time.sleep(sweepDur)
    inst.write(":INIT:CONT OFF")

    # SAVE
    csvPath = f"{folder}/{filename}.csv"
    pngPath = f"{folder}/{filename}.png"
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csvPath}"')
    inst.write(f':MMEM:STOR:SCR "{pngPath}"')

    saveFileToLocal(inst, pngPath, localOutFolder)
    saveFileToLocal(inst, csvPath, localOutFolder)
    return


def recallState(inst, stateFolder, filename):
    inst.write(f":MMEM:LOAD:STAT '{stateFolder}/{filename}'")
    return


def recallCorr(inst, corrFolder, filename):
    inst.write(f":MMEM:LOAD:CORR 1,'{corrFolder}/{filename}'")
    return


def setCoupling(inst, coupling):
    inst.write(f":INP:COUP {coupling}")
    # print(inst.query(f":INP:COUP?"))


def getRunId(runIndex):
    runNumber = "%02d" % runIndex
    d = datetime.datetime.now()
    month = str(int(d.strftime("%m")))
    date = d.strftime("%d")
    runId = f"{month}{date}-{runNumber}"
    return runId


def getRunFilename(runIndex, bandName, notes):
    runId = getRunId(runIndex)
    filename = f"{runId} {notes} {bandName}"
    return filename


def recordBands(
    resource,
    siteName,
    lastRunIndex,
    folders,
    bandKeys,
    sweepDur,
    window,
):

    inst = getInst(resource)
    barMax = len(bandKeys)
    pbar = window["-PROGRESS-"]
    pbar.update_bar(barMax / 50, barMax)
    for i, key in enumerate(bandKeys):
        time.sleep(sweepDur)
        pbar.update_bar(i + 1, barMax)
        bandName = key
        runIndex = i + 1 + lastRunIndex
        coupling = bands[key]["coupling"]

        stateFilename = bands[key]["stateFilename"]
        corrFilename = bands[key]["corrFilename"]
        runFilename = getRunFilename(runIndex, bandName, siteName)

        recallState(inst, folders["stateFolder"], stateFilename)
        recallCorr(inst, folders["corrFolder"], corrFilename)
        setCoupling(inst, coupling)

        outFolder = folders["outFolder"]
        localOutFolder = folders["localOutFolder"]
        recordBand(
            inst,
            outFolder,
            runFilename,
            localOutFolder,
            sweepDur,
        )
    time.sleep(1)
    pbar.update_bar(0, barMax)


def writeTxtFile(filename, text):
    with open(filename, "w") as f:
        f.write(text)
    return


def recordBandsDebug(
    resource, siteName, lastRunIndex, folders, bandKeys, sweepDur, window
):
    print("")
    print("recordBands()")
    print("resource:", resource)
    print("siteName:", siteName)
    print("lastRunIndex:", lastRunIndex)
    print("folders:", folders)
    print("bandKeys:", bandKeys)
    print("sweepDur:", sweepDur)
    print("window:", window)
    # inst = getInst(resource)
    barMax = len(bandKeys)
    pbar = window["-PROGRESS-"]
    pbar.update_bar(barMax / 50, barMax)
    for i, key in enumerate(bandKeys):
        time.sleep(sweepDur)
        pbar.update_bar(i + 1, barMax)
        bandName = key
        runIndex = i + 1 + lastRunIndex
        runFilename = getRunFilename(runIndex, bandName, siteName)

        localOutFolder = folders["localOutFolder"]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writeTxtFile(
            f"{localOutFolder}/{runFilename}.txt",
            f"{timestamp} {runFilename}",
        )
    time.sleep(1)
    pbar.update_bar(0, barMax)
