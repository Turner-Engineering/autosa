import json
import os
from json_repair import repair_json
from instrument.folders import get_folder_info


def get_version():
    src = os.path.dirname(__file__)
    path_to_version = os.path.join(src, "..", "version.json")
    path_to_version = os.path.abspath(path_to_version)

    with open(path_to_version, "r") as reader:
        autosa_version = json.load(reader)

    return f"v{autosa_version['__version__']}"


version_settings = f"\\settings_{get_version()}.json"

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


def get_settings_path():
    path = get_settings_folder_path() + version_settings
    print(path)

    return get_settings_folder_path() + version_settings


def write_settings_to_file(settings):
    folder = get_settings_folder_path()

    if not os.path.exists(folder):
        os.mkdir(folder)

    with open(folder + version_settings, "w") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def read_settings_from_file():
    folder = get_settings_folder_path()

    if not os.path.exists(folder + version_settings):
        return default_settings

    with open(folder + version_settings, "r") as reader:
        json_content = reader.read()
        fixed = repair_json(json_content)
        return json.loads(fixed)


def is_settings_valid(inst):
    folder = get_settings_folder_path()
    settings = read_settings_from_file()

    if not os.path.exists(folder + version_settings):
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
