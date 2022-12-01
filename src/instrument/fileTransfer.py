def binblock_raw(data_in):
    # This function interprets the header for a definite binary block
    # and returns the raw binary data for both definite and indefinite binary blocks

    startpos = data_in.find(b"#")  # old
    if startpos < 0:
        raise IOError("No start of block found")
    lenlen = int(data_in[startpos + 1 : startpos + 2])  # get the data length length

    # If it's a definite length binary block
    if lenlen > 0:
        # Get the length from the header
        offset = startpos + 2 + lenlen
        datalen = int(data_in[startpos + 2 : startpos + 2 + lenlen])
    else:
        # If it's an indefinite length binary block get the length from the transfer itself
        offset = startpos + 2
        datalen = len(data_in) - offset - 1

    # Extract the data out into a list.
    return data_in[offset : offset + datalen]


def saveFileToLocal(inst, filePath, outFolder):
    # Read the contents of the screen image
    filePath = filePath.replace("/", "\\")
    outFolder = outFolder.replace("/", "\\")
    inst.write(f':MMEM:DATA? "{filePath}"')

    rawData = inst.read_raw()

    # Interpret Header and Return Raw DATA
    rawData = binblock_raw(rawData)
    # Save Screen Image to File

    outFilename = filePath.split("\\")[-1]
    target = open(outFolder + "\\" + outFilename, "wb")
    target.write(rawData)
    target.close()
