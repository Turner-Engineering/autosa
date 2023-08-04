import PySimpleGUI as sg
from ui.run_buttons import get_band_button, BAND_KEYS


def get_single_band_layout():
    monopole_buttons = [get_band_button(bk) for bk in BAND_KEYS[0:5]]
    bilogical_buttons_h = [get_band_button(bk, "h") for bk in BAND_KEYS[5:8]]
    bilogical_buttons_v = [get_band_button(bk, "v") for bk in BAND_KEYS[5:8]]

    # arrange section 4 such that there are two rows for 4 buttons
    section = [
        [sg.Text("Single Band Mode lets you run one band at a time.", expand_x=True)],
        [
            sg.Text(
                "State files, correction files, and file names are set automatically.",
                expand_x=True,
            )
        ],
        [sg.Text("")],
        [sg.Text("Prepare, Record, and Save:", expand_x=True, font="Any 15")],
        monopole_buttons,
        bilogical_buttons_h,
        bilogical_buttons_v,
    ]
    return section
