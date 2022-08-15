import datetime
import time
from bandsData import bands
import pyvisa

rm = pyvisa.ResourceManager()

address = "USB0::0x2A8D::0x1B0B::MY57110397::INSTR"
inst = rm.open_resource(address)


def recordBand(inst, folder, filename, dur=5):
    # RECORD
    inst.write(":INIT:REST")
    inst.write(":INIT:CONT ON")
    time.sleep(dur)
    inst.write(":INIT:CONT OFF")

    # SAVE
    csvFilename = f"{folder}/{filename}.csv"
    pngFilename = f"{folder}/{filename}.png"
    inst.write(f":MMEM:STOR:TRAC:DATA ALL, '{csvFilename}'")
    inst.write(f":MMEM:STOR:SCR '{pngFilename}'")
    return


def recallState(inst, filename):
    folder = "D:/Users/Instrument/Desktop/Tenco State Files 8-05-2022"
    inst.write(f":MMEM:LOAD:STAT '{folder}/{filename}'")
    return


def recallCorr(inst, filename):
    folder = "D:/Users/Instrument/Desktop/Tenco Exa Amp Corr"
    inst.write(f":MMEM:LOAD:CORR 1,'{folder}/{filename}'")
    return


def setCoupling(inst, coupling):
    inst.write(f":INP:COUP {coupling}")
    # print(inst.query(f":INP:COUP?"))


def getRunFilename(runIndex, bandName, locationName, notes=""):
    runNumber = "%02d" % runIndex
    d = datetime.datetime.now()
    month = str(int(d.strftime("%m")))
    date = d.strftime("%d")
    runId = f"{month}{date}-{runNumber}"

    if notes == "":
        filename = f"{runId} {locationName} {bandName}"
    else:
        filename = f"{runId} {locationName} {notes} {bandName}"
    return filename


def recordMonopoleBands(locationName, lastRunIndex):
    for i, key in enumerate(bands):
        bandName = key
        runIndex = i + 1 + lastRunIndex
        coupling = bands[key]["coupling"]

        stateFilename = bands[key]["stateFilename"]
        corrFilename = bands[key]["corrFilename"]
        runFilename = getRunFilename(runIndex, bandName, locationName)

        recallState(inst, stateFilename)
        recallCorr(inst, corrFilename)
        setCoupling(inst, coupling)
        time.sleep(2)
        recordBand(inst, "D:/Users/Instrument/Desktop/Temba Tests", runFilename, 1)


time.sleep(5)
locationName = "Philadelphia"
lastRunIndex = 0
recordMonopoleBands(locationName, lastRunIndex)
