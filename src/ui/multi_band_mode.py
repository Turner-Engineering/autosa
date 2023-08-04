import PySimpleGUI as sg
from ui.run_buttons import get_band_button, BAND_KEYS, RUN_BUTTON_PROPS


def get_multi_band_layout():
    return [
        [
            sg.Text(
                "Multi-Band mode allows you to run multiple bands in a row with no intervention.",
                expand_x=True,
            )
        ],
        [
            sg.Text(
                "State files, correction files, and file names are set automatically.",
                expand_x=True,
            )
        ],
        [
            sg.Text("Band Range:"),
            sg.OptionMenu(
                key="-BAND RANGE-",
                values=["B0 - B4 (monopole)", "B5 - B7 (bilogical)"],
                background_color="white",
                default_value="B0 - B4 (monopole)",
            ),
        ],
        [
            sg.Text("Orientation:"),
            sg.OptionMenu(
                key="-ORIENTATION-",
                values=["Horizontal", "Vertical"],
                default_value="Horizontal",
                disabled=True,
            ),
        ],
        [
            sg.Button(
                "Run Sweeps",
                disabled=True,
                key="-RUN-",
                **RUN_BUTTON_PROPS,
            )
        ],
        [
            sg.ProgressBar(
                1, orientation="h", size=(60, 20), key="-PROGRESS-", expand_x=True
            )
        ],
    ]
