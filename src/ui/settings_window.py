import os
import re

import PySimpleGUI as sg

from instrument.folders import get_folder_info, get_folder_files

FOLDER_FIELDS = [
    {
        "key": "-STATE FOLDER-",
        "label": "State Files Folder",
        "validation": ["exists", "not_empty"],
    },
    {
        "key": "-CORR FOLDER-",
        "label": "Correction Files Folder",
        "validation": ["exists", "not_empty"],
        "events": True,
    },
    {
        "key": "-OUT FOLDER-",
        "label": "Instrument Output Folder",
        "validation": ["exists"],
    },
    {
        "key": "-LOCAL OUT FOLDER-",
        "label": "Local Output Folder",
        "validation": ["exists_local"],
        "browse": True,
    },
]


DEFAULT_SETTINGS = {
    "-STATE FOLDER-": "D:/Users/Instrument/Desktop/State Files",
    "-CORR FOLDER-": "D:/Users/Instrument/Desktop/Correction Files",
    "-OUT FOLDER-": "D:/Users/Instrument/Desktop/Test Data",
    "-LOCAL OUT FOLDER-": "",
    "-B0 CORR-": ['"Rod A kHz.csv"'],
    "-B1 CORR-": ["Rod A 10 kHz.csv"],
    "-B2 CORR-": ["Rod A 10 kHz.csv"],
    "-B3 CORR-": ["Rod A 10 kHz.csv"],
    "-B4 CORR-": ["Rod A 100 kHz.csv"],
    "-B5 CORR-": ["Bilogic 100.csv"],
    "-B6 CORR-": ["Bilogic 300.csv"],
    "-B7 CORR-": ["Bilogic 300.csv"],
    "-B0 STATE-": "State_B0.state",
    "-B1 STATE-": "State_B1.state",
    "-B2 STATE-": "State_B2.state",
    "-B3 STATE-": "State_B3.state",
    "-B4 STATE-": "State_B4.state",
    "-B5 STATE-": "State_B5.state",
    "-B6 STATE-": "State_B6.state",
    "-B7 STATE-": "State_B7.state",
    "-SWEEP DUR-": 5,
    "-RUN NOTE-": "Philadelphia",
    "-SET REF LEVEL-": True,
}

BAND_KEYS = ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"]


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
    for folder_field in folder_fields:
        # get folder label and path
        folder_key = folder_field["key"]
        folder_label = folder_field["label"]
        folder_validation = folder_field["validation"]
        folder_path = settings[folder_key]
        if "validation" not in folder_field:
            continue

        exists_local = get_folder_exists_local(folder_path)
        expect_exists_local = "exists_local" in folder_validation
        if expect_exists_local:
            if not exists_local:
                return f'{folder_label} "{folder_path}" does not exist on this computer'
            else:
                continue

        exists, empty, filenames = get_folder_info(inst, folder_path)
        expect_exists = "exists" in folder_validation
        expect_not_empty = "not_empty" in folder_validation
        error_message = ""

        if expect_exists and not exists:
            return f'{folder_label} "{folder_path}" does not exist on the instrument'

        if expect_not_empty and empty:
            return f'{folder_label} "{folder_path}" does is empty'

        # make sure all the expected files are present
        missing_state_files = get_missing_files(state_filenames, filenames)
        if "STATE" in folder_key and missing_state_files:
            error_message = (
                f'{folder_label} "{folder_path}" is missing following file(s):\n\n'
                + "\n".join(missing_state_files)
            )
            return error_message
    return error_message


def validate_corr_files(settings):
    def get_error_message(band_key):
        return f"No amplitude correction files have been selected for band {band_key}"

    error_message = ""
    for band_key in BAND_KEYS:
        key = f"-{band_key} CORR-"
        corr_filenames = settings[key]
        if len(corr_filenames) == 0:
            error_message = get_error_message(band_key)
            break
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
    settings = {key: settings[key] for key in DEFAULT_SETTINGS}

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
    corr_files_error = validate_corr_files(settings)
    if corr_files_error:
        return corr_files_error
    return ""


def get_folder_setting(folder_field):
    folder_key = folder_field["key"]
    folder_label = folder_field["label"]
    events = folder_field["events"] if "events" in folder_field else False
    default_value = DEFAULT_SETTINGS[folder_key]
    detault_text = sg.user_settings_get_entry(folder_key, default_value)

    folder_setting = [
        sg.Text(folder_label + ":"),
        sg.Input(
            key=folder_key, default_text=detault_text, size=60, enable_events=events
        ),
    ]
    if "browse" in folder_field:
        folder_setting.append(sg.FolderBrowse())
    return folder_setting


def get_folder_settings():
    folder_settings = [[sg.Text("Folders", font=("", 15))]]
    for folder_field in FOLDER_FIELDS:
        folder_setting = get_folder_setting(folder_field)
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
    layout = []
    for band_key in BAND_KEYS:
        key = f"-{band_key} {filename_type}-"
        default_text = sg.user_settings_get_entry(key, DEFAULT_SETTINGS[key])
        layout.append(
            [
                sg.Text(band_key, size=5),
                sg.Input(key=key, default_text=default_text, expand_x=True),
            ]
        )
    return layout


def get_state_files_section():
    frame1 = sg.Frame("State Files", get_filenames_frame_layout("STATE"), expand_x=True)
    return [[frame1]]


def get_multiselect(band_key, filenames):
    key = f"-{band_key} CORR-"
    select_mode = sg.LISTBOX_SELECT_MODE_MULTIPLE
    default_values = sg.user_settings_get_entry(key, DEFAULT_SETTINGS[key])
    return sg.Listbox(
        filenames,
        select_mode=select_mode,
        key=key,
        expand_y=True,
        default_values=default_values,
    )


def get_corr_frame(band_key, filenames):
    title = f"  {band_key}   "
    layout = [[get_multiselect(band_key, filenames)]]
    return sg.Frame(title, layout, expand_x=True, expand_y=True, font=("", 11, "bold"))


def get_band_setup_section(inst, corr_folder=None):
    corr_folder = (
        sg.user_settings_get_entry("-CORR FOLDER-")
        if corr_folder is None
        else corr_folder
    )
    filenames = get_folder_files(inst, corr_folder)
    print(filenames)

    row1 = []
    for band_key in BAND_KEYS[0:4]:
        row1.append(get_corr_frame(band_key, filenames))
    row2 = []
    for band_key in BAND_KEYS[4:8]:
        row2.append(get_corr_frame(band_key, filenames))

    layout = [row1, row2]

    # frame = sg.Frame("Amplitude Correction Files", layout, expand_x=True)
    return layout


def get_settings_window(inst):
    folder_settings = get_folder_settings()
    other_settings = get_other_settings()

    main_section = [
        *folder_settings,
        [sg.HorizontalSeparator()],
        *other_settings,
    ]

    sate_files_section = get_state_files_section()
    band_setup_section = get_band_setup_section(inst)

    tabs = [
        sg.Tab("     Primary     ", main_section),
        sg.Tab("     State Files     ", sate_files_section),
        sg.Tab("     Amplitude Corrections     ", band_setup_section),
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
    for key in DEFAULT_SETTINGS:
        sg.user_settings_set_entry(key, values[key])


def add_default_settings(settings):
    # add any missing settings
    # if new settings are added, this will add them in before they cause issues
    # if this is the first time the program is run, this will add the default settings
    for key in DEFAULT_SETTINGS:
        if key not in settings:
            settings[key] = DEFAULT_SETTINGS[key]
    return settings


def launch_settings_window(inst):
    window = get_settings_window(inst)
    settings_changed = False
    while True:
        event, values = window.read()
        print(event)
        if event in (sg.WIN_CLOSED, "Cancel"):
            break
        if event == "-CORR FOLDER-":
            filenames = get_folder_files(inst, values["-CORR FOLDER-"])
            for band_key in BAND_KEYS:
                key = f"-{band_key} CORR-"
                window[key].update(values=filenames)
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
