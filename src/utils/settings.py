import json, os
from instrument.folders import get_folder_info


filename = "\\settings.json"
default_settings = {
    "-STATE FOLDER-": "D:/Users/Instrument/Desktop/State Files",
    "-CORR FOLDER-": "D:/Users/Instrument/Desktop/Correction Files",
    "-INST OUT FOLDER-": "D:/Users/Instrument/Desktop/Test Data",
    "-LOCAL OUT FOLDER-": "",
    "-SWEEP DUR-": "5",
    "-CORR CHOICES-": {
        "B0": "No Correction",
        "B1": "No Correction",
        "B2": "No Correction",
        "B3": "No Correction",
        "B4": "No Correction",
        "B5": "No Correction",
        "B6": "No Correction",
        "B7": "No Correction",
    },
}


def get_settings_folder_path():
    return os.path.join(os.getenv("LOCALAPPDATA"), "Autosa")


def write_settings_to_file(settings):
    folder = get_settings_folder_path()

    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(get_settings_folder_path() + filename, "w") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def read_settings_from_file():
    if not os.path.exists(get_settings_folder_path() + filename):
        return default_settings

    with open(get_settings_folder_path() + filename, "r") as reader:
        return json.load(reader)


def is_settings_valid(inst):
    if not os.path.exists(get_settings_folder_path() + filename):
        return False

    # settings = read_settings_from_file()
    state_exists, state_empty, _ = get_folder_info(
        inst, read_settings_from_file()["-STATE FOLDER-"]
    )
    corr_exists, corr_empty, _ = get_folder_info(
        inst, read_settings_from_file()["-CORR FOLDER-"]
    )
    inst_exists, _, _ = get_folder_info(
        inst, read_settings_from_file()["-INST OUT FOLDER-"]
    )
    local_exists = os.path.exists(read_settings_from_file()["-LOCAL OUT FOLDER-"])

    state_blank = read_settings_from_file()["-STATE FOLDER-"].strip()
    corr_blank = read_settings_from_file()["-CORR FOLDER-"].strip()
    inst_blank = read_settings_from_file()["-INST OUT FOLDER-"].strip()
    local_blank = read_settings_from_file()["-LOCAL OUT FOLDER-"].strip()
    sweep_blank = read_settings_from_file()["-SWEEP DUR-"].strip()
    if sweep_blank:
        valid_sweep = float(sweep_blank) > 0

    if (
        not state_exists
        or not corr_exists
        or not inst_exists
        or not local_exists
        or state_empty
        or corr_empty
        or not state_blank
        or not corr_blank
        or not inst_blank
        or not local_blank
        or not sweep_blank
        or not valid_sweep
    ):

        return False

    return True
