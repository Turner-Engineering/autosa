import PySimpleGUI as sg
import pyvisa

from instrument.instrument import get_inst_found, get_inst_resource, record_bands
from ui.main_window import get_main_mindow, update_main_window
from ui.settings_window import launch_settings_window


def get_folders():
    folders = {}
    folders["stateFolder"] = sg.user_settings_get_entry("-STATE FOLDER-")
    folders["corrFolder"] = sg.user_settings_get_entry("-CORR FOLDER-")
    folders["outFolder"] = sg.user_settings_get_entry("-OUT FOLDER-")
    folders["localOutFolder"] = sg.user_settings_get_entry("-LOCAL OUT FOLDER-")
    return folders


def validate_input(values):
    if values["-BAND RANGE-"] == "":
        return False
    if values["-SITE-"] == "":
        return False
    return True


def main():
    sg.theme("SystemDefaultForReal")
    # default location for this file is Users/<username>/AppData/Local/PySimpleGUI/settings/
    sg.user_settings_filename("autosa.json")
    rm = pyvisa.ResourceManager()

    inst_resource = get_inst_resource(rm)
    inst_found = get_inst_found(inst_resource)

    main_window = get_main_mindow(inst_found, inst_resource)

    while True:
        timeout = 2000 if inst_found else 200
        event, values = main_window.read(timeout=timeout)
        # without timeout, code pauses here and waits for event
        inst_resource = get_inst_resource(rm)
        inst_found = get_inst_found(inst_resource)
        update_main_window(main_window, inst_found, inst_resource)

        if event == "Settings":
            settings_changed = launch_settings_window()
            if settings_changed:
                main_window.close()
                main_window = get_main_mindow(inst_found, inst_resource)
        elif event == sg.WIN_CLOSED:
            break

        input_valid = validate_input(values)
        if not input_valid:
            main_window["-RUN-"].update(disabled=True)
            continue
        else:
            main_window["-RUN-"].update(disabled=False)

        if event == "-RUN-":
            # FOLDERS
            folders = get_folders()

            # OTHER VARS
            site_name = values["-SITE-"]
            last_run_index = int(values["-LAST INDEX-"])
            sweep_dur = float(sg.user_settings_get_entry("-SWEEP DUR-"))

            band_keys = (
                ["B0", "B1", "B2", "B3", "B4"]
                if values["-BAND RANGE-"] == "B0 - B4 (monopole)"
                else ["B5", "B6", "B7"]
                if values["-BAND RANGE-"] == "B5 - B7 (bilogical)"
                else ""
            )

            record_bands(
                inst_resource,
                site_name,
                last_run_index,
                folders,
                band_keys,
                sweep_dur,
                main_window,
            )
    main_window.close()


if __name__ == "__main__":
    main()
