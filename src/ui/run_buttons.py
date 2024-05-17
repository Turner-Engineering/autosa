import PySimpleGUI as sg

BAND_KEYS = ["B0", "B1", "B2", "B3", "B4", "B5", "B6", "B7"]

RUN_BUTTON_PROPS = {
    "font": "Any 15",
    "button_color": ("white", "dark blue"),
    "size": (15, 2),
}


def get_band_button(band_key, band_ori="", key_prefix="SINGLE_BAND"):
    return sg.Button(
        band_key + band_ori,
        key=f"-{key_prefix} {band_key} {band_ori}-",
        font=RUN_BUTTON_PROPS["font"],
        button_color=RUN_BUTTON_PROPS["button_color"],
        size=(12, 2),
        expand_x=True,
    )
