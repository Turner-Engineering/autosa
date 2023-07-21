import csv


def get_folder_info(inst, folder_path):
    folder_path = folder_path.replace("/", "\\")

    # CAT is short for Catalog and lists out the files in a folder
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

    return exists, empty, filenames


def get_folder_files(inst, folder_path):
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
