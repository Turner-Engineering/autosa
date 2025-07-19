import json
import os
from json_repair import repair_json
from instrument.folders import get_folder_info


def get_autosa_version():
    src = os.path.dirname(__file__)
    path_to_version = os.path.abspath(os.path.join(src, "..", "autosa_version.txt"))
    version_number = (
        open(path_to_version, "r").read().strip()
    )  # strip just in case there's any whitespace
    return f"v{version_number}"  # e.g. v0.4.2


SETTINGS_FILENAME = f"settings_{get_autosa_version()}.json"

DEFAULT_SETTINGS = {
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


def get_settings_path():
    return os.path.join(get_settings_folder_path(), SETTINGS_FILENAME)


def get_log_path(name=None):
    folder = get_settings_folder_path()

    if not os.path.exists(folder):
        os.mkdir(folder)

    filename = f"autosa_{get_autosa_version()}.log"
    if name is not None:
        filename = filename.replace("_", f"_{name}_")

    return os.path.join(folder, filename)


def write_settings_to_file(settings):
    folder = get_settings_folder_path()

    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(get_settings_path(), "w") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def read_settings_from_file():
    settings_path = get_settings_path()

    if not os.path.exists(settings_path):
        return DEFAULT_SETTINGS

    with open(settings_path, "r") as reader:
        json_content = reader.read()
        fixed = repair_json(json_content)
        return json.loads(fixed)


def is_settings_valid(inst):
    settings = read_settings_from_file()

    if not os.path.exists(get_settings_path()):
        return False

    # settings = read_settings_from_file()
    state_exists, state_empty, _ = get_folder_info(inst, settings["-STATE FOLDER-"])
    corr_exists, corr_empty, _ = get_folder_info(inst, settings["-CORR FOLDER-"])
    inst_exists, _, _ = get_folder_info(inst, settings["-INST OUT FOLDER-"])
    local_exists = os.path.exists(settings["-LOCAL OUT FOLDER-"])

    # .strip() ensures any empty spaces are not considered an input
    state_blank = settings["-STATE FOLDER-"].strip()
    corr_blank = settings["-CORR FOLDER-"].strip()
    inst_blank = settings["-INST OUT FOLDER-"].strip()
    local_blank = settings["-LOCAL OUT FOLDER-"].strip()
    sweep_blank = settings["-SWEEP DUR-"].strip()
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


def is_valid_local_folder(path):
    return os.path.exists(path.strip()) and path.strip()


def is_valid_inst_folder(inst, folder_path):
    exists, _, _ = get_folder_info(inst, folder_path)
    return exists and folder_path.strip()


def is_valid_sweep_duration(value):
    try:
        return float(value.strip()) > 0
    except ValueError:
        return False
