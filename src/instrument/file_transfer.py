import os
import datetime

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


def copy_file_to_local(inst, file_path, out_folder, band):
    # Read the contents of the screen image
    file_path = file_path.replace("/", "\\")
    out_folder = out_folder.replace("/", "\\")
    inst.write(f':MMEM:DATA? "{file_path}"')

    raw_data = inst.read_raw()

    # Interpret Header and Return Raw DATA
    raw_data = binblock_raw(raw_data)
    
    # Save Screen Image to File

    # Extract filename
    out_filename = file_path.split("\\")[-1]

    # Ensure the base output directory exists
    os.makedirs(out_folder, exist_ok=True)

    # Save to base folder
    # with open(os.path.join(out_folder, out_filename), "wb") as target:
    #     target.write(raw_data)

    # Save to date-based subfolder (e.g., '622', '1201')
    day_folder = datetime.datetime.now().strftime("%m%d").lstrip("0")
    dated_folder = os.path.join(out_folder, day_folder)

    # Add band-specific folder
    band_folder = os.path.join(dated_folder, band)
    os.makedirs(band_folder, exist_ok=True)

    with open(os.path.join(band_folder, out_filename), "wb") as target_file:
        target_file.write(raw_data)