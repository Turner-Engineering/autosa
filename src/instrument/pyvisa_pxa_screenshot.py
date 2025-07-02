# Instrument Control using PyVISA
# Get Screenshot from PXA
# import python modules
import visa

# Define Functions for Binary Data Mangement


def binblock_raw(data_in):
    # This function interprets the header for a definite binary block
    # and returns the raw binary data for both definite and indefinite binary blocks

    start_pos = data_in.find("#")
    if start_pos < 0:
        raise IOError("No start of block found")
    len_len = int(data_in[start_pos + 1 : start_pos + 2])  # get the data length length

    # If it's a definite length binary block
    if len_len > 0:
        # Get the length from the header
        offset = start_pos + 2 + len_len
        data_len = int(data_in[start_pos + 2 : start_pos + 2 + len_len])
    else:
        # If it's an indefinite length binary block get the length from the transfer itself
        offset = start_pos + 2
        data_len = len(data_in) - offset - 1

    # Extract the data out into a list.
    return data_in[offset : offset + data_len]


try:
    # Open Connection
    rm = visa.ResourceManager(
        "C:\\Program Files (x86)\\IVI Foundation\\VISA\\WinNT\\agvisa\\agbin\\visa32.dll"
    )
    my_inst = rm.open_resource("TCPIP0::156.140.157.6::inst0::INSTR")
    # my_inst = rm.open_resource("TCPIP0::localhost::inst0::INSTR") # emulator mode address

    # Set Timeout - 10 seconds
    my_inst.timeout = 10000

    # *RST / *IDN?
    my_inst.write("*CLS")
    my_inst.write("*IDN?")
    # print myinst.read()

    my_inst.write("*OPC?")
    print("Reset Complete: " + my_inst.read())

    # Store the screen image to file
    my_inst.write(":MMEM:STOR:SCR 'D:\\PICTURE.PNG'")
    my_inst.write("*OPC?")
    complete = my_inst.read()

    # Read the contents of the screen image
    my_inst.write(":MMEM:DATA? 'D:\\PICTURE.PNG'")

    my_image = my_inst.read_raw()
    # Interpret Header and Return Raw DATA
    my_image = binblock_raw(my_image)
    # Save Screen Image to File
    target = open("C:\\Users\\Public\\python_screenshot2.jpg", "wb")
    target.write(my_image)
    target.close()

    ## Query for Instrument Errors
    while True:
        my_inst.write(":SYSTem:ERRor?")
        result = my_inst.read()
        error_list = result.split(",")
        error = error_list[0]
        print("Error #: " + error_list[0])
        print("Error Description: " + error_list[1])
        if int(error) == 0:
            break

    # Close Connection
    my_inst.close()
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
