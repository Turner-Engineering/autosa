# Instrument Control using PyVISA
# Get Screenshot from PXA
# import python modules
import visa

# Define Functions for Binary Data Mangement


def binblock_raw(data_in):
    # This function interprets the header for a definite binary block
    # and returns the raw binary data for both definite and indefinite binary blocks

    startpos = data_in.find("#")
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


try:

    # Open Connection
    rm = visa.ResourceManager(
        "C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll"
    )
    myinst = rm.open_resource("TCPIP0::156.140.157.6::inst0::INSTR")

    # Set Timeout - 10 seconds
    myinst.timeout = 10000

    # *RST / *IDN?
    myinst.write("*CLS")
    myinst.write("*IDN?")
    # print myinst.read()

    myinst.write("*OPC?")
    print("Reset Complete: " + myinst.read())

    # Store the screen image to file
    myinst.write(":MMEM:STOR:SCR 'D:\\PICTURE.PNG'")
    myinst.write("*OPC?")
    complete = myinst.read()

    # Read the contents of the screen image
    myinst.write(":MMEM:DATA? 'D:\\PICTURE.PNG'")

    my_image = myinst.read_raw()
    # Interpret Header and Return Raw DATA
    my_image = binblock_raw(my_image)
    # Save Screen Image to File
    target = open("C:\\Users\\Public\\python_screenshot2.jpg", "wb")
    target.write(my_image)
    target.close()

    ## Query for Instrument Errors
    while True:
        myinst.write(":SYSTem:ERRor?")
        Result = myinst.read()
        ErrorList = Result.split(",")
        Error = ErrorList[0]
        print("Error #: " + ErrorList[0])
        print("Error Description: " + ErrorList[1])
        if int(Error) == 0:
            break

    # Close Connection
    myinst.close()
    print("close instrument connection")

except IOError as err:
    print("Unable to open file: " + str(err.strerror) + str(err.message))

except OSError as err:
    print("Library error: " + str(err.strerror) + str(err.message))

except Exception as err:
    print("Exception: " + str(err.message))

finally:
    # perform clean up operations
    print("complete")
