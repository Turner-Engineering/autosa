import csv
import datetime
import os

# NOTE: cannot put autosa_logger in this file due to circular import


def get_folder_info(inst, folder_path):
    folder_path = folder_path.replace("/", "\\").strip()

    # CAT is short for Catalog and lists out the files in a folder
    if inst is not None:
        resp = inst.query(f'MMEM:CAT? "{folder_path}"')

        # split by commas, but ignore commas inside quotes
        parts = next(csv.reader([resp], skipinitialspace=True))

        # these two numbers are storage used and storage available
        # they are both zero when the folder does not exist
        exists = False if parts[0] == "0" and parts[1] == "0" else True

        # contents is a string of filenames separated by commas
        empty = True if parts[2] == "" else False

        filenames = []
        if not empty:
            # file_data has the format "filename, file_type, file_size"
            filenames = [file_data.split(",")[0] for file_data in parts[2:]]
    else:
        # If inst is None, we return a dummy response
        exists = False
        empty = True
        filenames = []

    return exists, empty, filenames


def get_folder_files(inst, folder_path):
    if inst is not None:
        folder_path = folder_path.replace("/", "\\")

        # CAT is short for Catalog and lists out the files in a folder
        resp = inst.query(f'MMEM:CAT? "{folder_path}"')

        # split by commas, but ignore commas inside quotes
        parts = next(csv.reader([resp], skipinitialspace=True))

        filenames = []
        if parts[2] == "":
            return filenames
        else:
            filenames = [file_data.split(",")[0] for file_data in parts[2:]]
        return filenames
    else:
        # If inst is None, we return empty
        return []


def get_sorted_folder(out_folder, band):
    out_folder = out_folder.replace("/", "\\")

    # Create date-based subfolder (e.g., '622', '1201')
    day_folder = datetime.datetime.now().strftime("%m%d").lstrip("0")
    dated_folder = os.path.join(out_folder, day_folder)

    # Add band-specific folder
    band_folder = os.path.join(dated_folder, band)
    os.makedirs(band_folder, exist_ok=True)

    return band_folder


def get_csv_folder(out_folder):
    out_folder = out_folder.replace("/", "\\")

    # Add csv subfolder
    csv_folder = os.path.join(out_folder, "csv")
    os.makedirs(csv_folder, exist_ok=True)

    return csv_folder


def folder_exists(inst, folder_path):
    try:
        resp = inst.query(f'MMEM:CAT? "{folder_path}"').strip()

        # check if folder exists & empty
        if resp == '0,0,""':
            inst.write(f':MMEM:MDIR "{folder_path}"')  # if empty, create
            return True
    except Exception:
        try:
            # if it doesn't exist, try creating
            inst.write(f':MMEM:MDIR "{folder_path}"')
            return True
        except Exception:
            return False
