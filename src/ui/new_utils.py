import json, os

SETTINGS_FILE_PATH = os.path.join(os.getenv("LOCALAPPDATA"), "Autosa")


def write_json(data, json_file="settings.json"):
    if not os.path.exists(SETTINGS_FILE_PATH):
        os.mkdir(SETTINGS_FILE_PATH)

    json_path = os.path.join(SETTINGS_FILE_PATH, json_file)

    """write to the json file"""
    with open(json_path, "w") as writer:
        writer.write(json.dumps(data, indent=4))


def read_json(json_file="settings.json"):
    if not os.path.exists(SETTINGS_FILE_PATH):
        print("ERROR. Folder does not exist.")

    json_path = os.path.join(SETTINGS_FILE_PATH, json_file)

    if os.path.exists(json_path):
        with open(json_path, "r") as reader:
            return json.load(reader)

    return {}
