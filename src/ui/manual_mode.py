import PySimpleGUI as sg
from ui.run_buttons import get_band_button, BAND_KEYS


def get_manual_mode_layout():
    prefix = "PREP_BAND"
    monopole_buttons = [get_band_button(bk, key_prefix=prefix) for bk in BAND_KEYS[0:5]]
    bilogical_buttons = [
        get_band_button(bk, key_prefix=prefix) for bk in BAND_KEYS[5:8]
    ]

    img_props = {
        "image_size": (60, 60),
        "image_subsample": 10,
    }

    start_stop_button = sg.Button(
        key="-START STOP-",
        image_filename="../images/play-green.png",
        metadata="Start",
        **img_props,
    )

    reset_button = sg.Button(
        key="-RESET-",
        image_filename="../images/reset-blue.png",
        **img_props,
    )

    save_button = sg.Button(
        key="-SAVE TRACE AND SCREEN-",
        image_filename="../images/save-purple.png",
        **img_props,
    )

    layout = [
        [sg.Text("Prepare Band:", expand_x=True, font="Any 15")],
        monopole_buttons,
        bilogical_buttons,
        [sg.Text("Record and Save:", expand_x=True, font="Any 15")],
        [start_stop_button, reset_button, save_button],
        [
            sg.Text(
                "0:00.0", size=(20, 1), key="-STOPWATCH TIME-", font=("Any", 45, "bold")
            )
        ],
        [
            sg.Text("Last Start Time: ", font="Any 12"),
            sg.Text("None", key="-STOPWATCH START TIME-", font=("Any", 12, "bold")),
        ],
        [
            sg.Text("Last Band Prepared: ", font="Any 12"),
            sg.Text("None", key="-LAST BAND PREPARED-", font=("Any", 12, "bold")),
        ],
    ]
    return layout


def update_start_stop_button(main_window, state):
    main_window["-START STOP-"].metadata = state
    if state == "Start":
        filename = "../images/play-green.png"
    elif state == "Stop":
        filename = "../images/pause-red.png"
    main_window["-START STOP-"].update(
        image_filename=filename,
        image_size=(60, 60),
        image_subsample=10,
    )
