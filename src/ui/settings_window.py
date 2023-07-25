import os
import re

import PySimpleGUI as sg

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
        "validation": ["exists_local"],
        "browse": True,
    },
]

DEFAULT_FILENAMES = {
    "-B0 CORR 1-": "Rod A 1 kHz.csv",
    "-B1 CORR 1-": "Rod A 10 kHz.csv",
    "-B2 CORR 1-": "Rod A 10 kHz.csv",
    "-B3 CORR 1-": "Rod A 10 kHz.csv",
    "-B4 CORR 1-": "Rod A 100 kHz.csv",
    "-B5 CORR 1-": "Bilogic 100.csv",
    "-B6 CORR 1-": "Bilogic 300.csv",
    "-B7 CORR 1-": "Bilogic 300.csv",
    "-B0 STATE-": "State_B0.state",
    "-B1 STATE-": "State_B1.state",
    "-B2 STATE-": "State_B2.state",
    "-B3 STATE-": "State_B3.state",
    "-B4 STATE-": "State_B4.state",
    "-B5 STATE-": "State_B5.state",
    "-B6 STATE-": "State_B6.state",
    "-B7 STATE-": "State_B7.state",
}


# these are the keys used to address all settings
folder_keys = [field["key"] for field in FOLDER_FIELDS if "key" in field]
filename_keys = [key for key in DEFAULT_FILENAMES]
other_keys = ["-SWEEP DUR-", "-RUN NOTE-", "-SET REF LEVEL-"]
SETTINGS_KEYS = folder_keys + filename_keys + other_keys


def get_corr_filenames(settings):
    regex = r"^-B\d CORR \d-$"
    corr_filenames = [settings[key] for key in settings if re.match(regex, key)]
    corr_filenames = list(set(corr_filenames))
    corr_filenames.sort()
    return corr_filenames


def get_state_filenames(settings):
    regex = r"^-B\d STATE-$"
    state_filenames = [settings[key] for key in settings if re.match(regex, key)]
    state_filenames = list(set(state_filenames))
    state_filenames.sort()
    return state_filenames


def get_missing_files(expected_filenames, actual_filenames):
    return set(expected_filenames).difference(set(actual_filenames))


def get_folder_exists_local(folder_path):
    return os.path.isdir(folder_path)


def validate_folders(inst, settings, folder_fields):
    state_filenames = get_state_filenames(settings)
    corr_filenames = get_corr_filenames(settings)
    for folder_field in folder_fields:
        # get folder label and path
        folder_label = folder_field["label"]
        folder_path = settings[folder_field["key"]]
        if "validation" not in folder_field:
            continue

        exists_local = get_folder_exists_local(folder_path)
        expect_exists_local = "exists_local" in folder_field["validation"]
        if expect_exists_local:
            if not exists_local:
                return f'{folder_label} "{folder_path}" does not exist on this computer'
            else:
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
        missing_state_files = get_missing_files(state_filenames, filenames)
        if "STATE" in folder_field["key"] and missing_state_files:
            error_message = (
                f'{folder_label} "{folder_path}" is missing following file(s):\n\n'
                + "\n".join(missing_state_files)
            )
            return error_message

        missing_corr_files = get_missing_files(corr_filenames, filenames)
        if "CORR" in folder_field["key"] and missing_corr_files:
            error_message = (
                f'{folder_label} "{folder_path}" is missing the following file(s):\n\n'
                + "\n".join(missing_corr_files)
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
    settings = {key: settings[key] for key in SETTINGS_KEYS}

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


def get_filenames_frame_layout(filename_type):
    band_keys = ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"]
    layout = [
        [
            sg.Text(band_key, size=5),
            sg.Input(
                key=f"-{band_key} {filename_type}-",
                expand_x=True,
                default_text=DEFAULT_FILENAMES[f"-{band_key} {filename_type}-"],
            ),
        ]
        for band_key in band_keys
    ]
    return layout


def get_band_setup_section():
    layout1 = [
        [sg.Frame("State Files", get_filenames_frame_layout("STATE"), expand_x=True)]
    ]
    layout2 = [
        [
            sg.Frame(
                "Correction Files", get_filenames_frame_layout("CORR 1"), expand_x=True
            )
        ]
    ]

    band_setup_section = [
        [sg.Text("Band Setup", font=("", 15))],
        [sg.Column(layout1, expand_x=True), sg.Column(layout2, expand_x=True)],
    ]
    return band_setup_section


def get_settings_window(folder_fields):
    folder_settings = get_folder_settings(folder_fields)
    other_settings = get_other_settings()

    main_section = [
        *folder_settings,
        [sg.HorizontalSeparator()],
        *other_settings,
    ]

    band_setup_section = get_band_setup_section()

    tabs = [
        sg.Tab("     Primary     ", main_section),
        sg.Tab("     Band Setup     ", band_setup_section),
    ]

    layout = [
        [sg.Text("Settings", font=("_ 25"))],
        [sg.TabGroup([tabs])],
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
