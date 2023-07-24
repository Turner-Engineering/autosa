import PySimpleGUI as sg

from bands_data import bands
from instrument.folders import get_folder_info

FOLDER_FIELDS = [
    {
        "key": "-STATE FOLDER-",
        "label": "State Files Folder",
        "default": "D:/Users/Instrument/Desktop/State Files",
        "validation": ["exists", "not_empty"],
    },
    {
        "key": "-CORR FOLDER-",
        "label": "Correction Files Folder",
        "default": "D:/Users/Instrument/Desktop/Correction Files",
        "validation": ["exists", "not_empty"],
    },
    {
        "key": "-OUT FOLDER-",
        "label": "Instrument Output Folder",
        "default": "D:/Users/Instrument/Desktop/Test Data",
        "validation": ["exists"],
    },
    {
        "key": "-LOCAL OUT FOLDER-",
        "label": "Local Output Folder",
        "default": "",
        "browse": True,
    },
]

# these are the keys used to address all settings
SETTINGS_KEYS = [field["key"] for field in FOLDER_FIELDS if "key" in field] + [
    "-SWEEP DUR-",
    "-RUN NOTE-",
    "-SET REF LEVEL-",
]


def get_corr_filenames(bands):
    corr_filenames = []
    for band in bands:
        corr_filename = bands[band]["corrFilename"]
        corr_filenames.append(corr_filename)
    corr_filenames = list(set(corr_filenames))
    corr_filenames.sort()
    return corr_filenames


def get_state_filenames(bands):
    state_filenames = []
    for band in bands:
        state_filename = bands[band]["stateFilename"]
        state_filenames.append(state_filename)
    state_filenames = list(set(state_filenames))
    state_filenames.sort()
    return state_filenames


def filenames_in_folder(expected_filenames, actual_filenames):
    return set(expected_filenames).issubset(set(actual_filenames))


def validate_folders(inst, settings, folder_fields):
    state_filenames = get_state_filenames(bands)
    corr_filenames = get_corr_filenames(bands)
    for folder_field in folder_fields:
        # get folder label and path
        folder_label = folder_field["label"]
        folder_path = settings[folder_field["key"]]
        if "validation" not in folder_field:
            continue

        exists, empty, filenames = get_folder_info(inst, folder_path)
        expect_exists = "exists" in folder_field["validation"]
        expect_not_empty = "not_empty" in folder_field["validation"]
        error_message = ""

        if expect_exists and not exists:
            return f'{folder_label} "{folder_path}" does not exist on the instrument'

        if expect_not_empty and empty:
            return f'{folder_label} "{folder_path}" does is empty'

        # make sure all the expected files are present
        state_files_present = filenames_in_folder(state_filenames, filenames)
        if "STATE" in folder_field["key"] and not state_files_present:
            error_message = (
                f'{folder_label} "{folder_path}" is missing one or more of the following files:\n\n'
                + "\n".join(state_filenames)
            )
            return error_message

        corr_files_present = filenames_in_folder(corr_filenames, filenames)
        if "CORR" in folder_field["key"] and not corr_files_present:
            error_message = (
                f'{folder_label} "{folder_path}" is missing one or more of the following files:\n\n'
                + "\n".join(corr_filenames)
            )
            return error_message
    return error_message


def validate_sweep_dur(settings):
    sweep_dur = settings["-SWEEP DUR-"]
    error_message = ""
    if float(sweep_dur) <= 0:
        error_message = "Sweep duration must be greater than 0"
    return error_message


def validate_run_note(settings):
    run_note = settings["-RUN NOTE-"]
    error_message = ""
    if run_note == "":
        error_message = "Run note cannot be empty"
    # should be something that is valid to use as a filename
    forbidden_chars = ["\\", "/", ":", "*", "?", '"', "<", ">", "|"]
    for char in forbidden_chars:
        if char in run_note:
            error_message = f'Run note cannot contain the following characters: {", ".join(forbidden_chars)}'
            break

    return error_message


def validate_settings(inst, settings=None):
    settings = sg.user_settings() if settings is None else settings

    # validate saved user settings
    folders_error = validate_folders(inst, settings, FOLDER_FIELDS)
    if folders_error:
        return folders_error
    sweep_dur_error = validate_sweep_dur(settings)
    if sweep_dur_error:
        return sweep_dur_error
    run_note_error = validate_run_note(settings)
    if run_note_error:
        return run_note_error
    return ""


def get_folder_setting(field):
    detault_text = sg.user_settings_get_entry(field["key"], field["default"])

    folder_setting = [
        sg.Text(field["label"] + ":"),
        sg.Input(key=field["key"], default_text=detault_text, size=60),
    ]
    if "browse" in field:
        folder_setting.append(sg.FolderBrowse())
    return folder_setting


def get_folder_settings(folder_fields):
    folder_settings = [[sg.Text("Folders", font=("", 15))]]
    for field in folder_fields:
        folder_setting = get_folder_setting(field)
        folder_settings.append(folder_setting)
    return folder_settings


def get_other_settings():
    sweep_dur_default = sg.user_settings_get_entry("-SWEEP DUR-", 5)
    run_note_default = sg.user_settings_get_entry("-RUN NOTE-", "Philadelphia")
    set_ref_level_default = sg.user_settings_get_entry("-SET REF LEVEL-", True)
    layout = [
        [sg.Text("Other", font=("", 15))],
        [
            sg.Text("Adjust Reference Level:"),
            sg.Checkbox(
                "If this is checked, the reference adjusted such that all trace peaks are visible.",
                key="-SET REF LEVEL-",
                default=set_ref_level_default,
                expand_x=True,
            ),
        ],
        [
            sg.Text("Sweep Duration (s):"),
            sg.Input(key="-SWEEP DUR-", default_text=sweep_dur_default, size=60),
        ],
        [
            sg.Text("Run Note:"),
            sg.Input(key="-RUN NOTE-", default_text=run_note_default, size=60),
        ],
        [
            sg.Text(
                "The run note is the text placed after the run id and band name in a filename.",
                expand_x=True,
            ),
        ],
        [
            sg.Text(
                'Files will be saved as "808-13 B3 [run note].csv and "808-13 B3 [run note].png".',
                expand_x=True,
            ),
        ],
        [
            sg.Text(
                "This can be used for location, test type, or any other information.",
                expand_x=True,
            ),
        ],
    ]
    return layout


def get_settings_window(folder_fields):
    folder_settings = get_folder_settings(folder_fields)
    other_settings = get_other_settings()

    layout = [
        [sg.Text("Settings", font=("_ 25"))],
        [sg.HorizontalSeparator()],
        folder_settings,
        [sg.HorizontalSeparator()],
        other_settings,
        [sg.HorizontalSeparator()],
        [sg.Button("Save"), sg.Button("Cancel")],
    ]

    window = sg.Window(
        "Settings", layout, default_element_size=(20, 1), auto_size_text=False
    )
    return window


def save_settings(values):
    for key in SETTINGS_KEYS:
        sg.user_settings_set_entry(key, values[key])


def launch_settings_window(inst):
    window = get_settings_window(FOLDER_FIELDS)
    settings_changed = False
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        elif event == "Save":
            # save first so we can validate from the saved settings
            settings_error_message = validate_settings(inst, values)
            if settings_error_message:
                sg.popup_error(settings_error_message, title="Settings Error")
            else:
                save_settings(values)
                settings_changed = True  # used as flag to update main window
                break

    window.close()

    return settings_changed
