def binblock_raw(data_in):
    # This function interprets the header for a definite binary block
    # and returns the raw binary data for both definite and indefinite binary blocks

    start_pos = data_in.find(b"#")  # old
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


def save_file_to_local(inst, file_path, out_folder):
    # Read the contents of the screen image
    file_path = file_path.replace("/", "\\")
    out_folder = out_folder.replace("/", "\\")
    inst.write(f':MMEM:DATA? "{file_path}"')

    raw_data = inst.read_raw()

    # Interpret Header and Return Raw DATA
    raw_data = binblock_raw(raw_data)
    # Save Screen Image to File

    out_filename = file_path.split("\\")[-1]
    target = open(out_folder + "\\" + out_filename, "wb")
    target.write(raw_data)
    target.close()
