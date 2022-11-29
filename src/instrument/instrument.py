import datetime
import time
from bandsData import bands
import pyvisa
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
    csvFilename = f"{folder}/{filename}.csv"
    pngFilename = f"{folder}/{filename}.png"
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csvFilename}"')
    inst.write(f':MMEM:STOR:SCR "{pngFilename}"')

    saveFileToLocal(inst, pngFilename, localOutFolder)
    saveFileToLocal(inst, csvFilename, localOutFolder)
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


def getRunFilename(runIndex, bandName, siteName, notes=""):
    runNumber = "%02d" % runIndex
    d = datetime.datetime.now()
    month = str(int(d.strftime("%m")))
    date = d.strftime("%d")
    runId = f"{month}{date}-{runNumber}"

    if notes == "":
        filename = f"{runId} {siteName} {bandName}"
    else:
        filename = f"{runId} {siteName} {notes} {bandName}"
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
    print("")
    print("recordBands()")
    print("resource:", resource)
    print("siteName:", siteName)
    print("lastRunIndex:", lastRunIndex)
    print("folders:", folders)
    print("bandKeys:", bandKeys)
    print("sweepDur:", sweepDur)
    print("window:", window)

    inst = getInst(resource)
    barMax = len(bandKeys)
    pbar = window["-PROGRESS-"]
    for i, key in enumerate(bandKeys):
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
    pbar.update_bar(0, barMax)
