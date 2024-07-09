import json, os

default_settings = {
    "state_folder": "D:/Users/Instrument/Desktop/State Files",
    "corr_folder": "D:/Users/Instrument/Desktop/Correction Files",
    "inst_out_folder": "D:/Users/Instrument/Desktop/Test Data",
    "local_out_folder": "",
    "sweep_dur": "5",
    "corr_choice": {},
}


def get_settings_file_path():
    return os.path.join(os.getenv("LOCALAPPDATA"), "Autosa", "settings.json")


def write_settings_to_file(settings):
    # this will overwrite the file if it exists and create it if it doesn't
    with open(get_settings_file_path(), "w") as f:
        json.dump(settings, f, ensure_ascii=False, indent=2)


def read_settings_from_file():
    if not os.path.exists(get_settings_file_path()):
        # TODO: this should raise a user-facing error
        print("ERROR. Settings file does not exist. Using default settings.")
        return default_settings

    with open(get_settings_file_path(), "r") as reader:
        return json.load(reader)
