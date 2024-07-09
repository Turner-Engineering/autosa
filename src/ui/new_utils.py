import json, os

default_settings = {
    "State Files Folder:": "D:/Users/Instrument/Desktop/State Files",
    "Correction Files Folder:": "D:/Users/Instrument/Desktop/Correction Files",
    "Instrument Output Folder:": "D:/Users/Instrument/Desktop/Test Data",
    "Local Output Folder:": "",
    "Sweep Duration:": "5",
    "Correction Choice:": {},
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
