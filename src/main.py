import PySimpleGUI as sg
import pyvisa

from instrument.instrument import (
    get_inst,
    get_inst_info,
    record_multiple_bands,
    record_single_band,
)
from ui.main_window import get_main_mindow, update_main_window, set_band_button_disabled
from ui.settings_window import launch_settings_window, validate_settings


def handle_py_visa_error(e):
    # this is the error code when NI-VISA is not installed
    NI_VISA_ERROR_CODE = -1073807202
    if e.error_code == NI_VISA_ERROR_CODE:
        sg.popup_error(
            "Error NI-VISA library not found.",
            "Autosa requires the National Instruments VISA library to be installed.",
            'Please ask Temba for help installing "NI-VISA" or install NI-VISA by searching for "NI-VISA Download" online and following the instructions.',
            title="NI-VISA library not found",
        )
    else:
        sg.popup_error(
            "Error code: " + str(e.error_code) + "\n" + e.description,
            title="Error",
        )


def assert_ni_visa_installed(pyvisa):
    try:
        pyvisa.ResourceManager()
        return True
    except pyvisa.errors.VisaIOError as e:
        handle_py_visa_error(e)
        return False
    except Exception as e:
        sg.popup_error(
            "Error: " + str(e),
            title="Error",
        )
        return False


def get_folders():
    folders = {}
    folders["stateFolder"] = sg.user_settings_get_entry("-STATE FOLDER-")
    folders["corrFolder"] = sg.user_settings_get_entry("-CORR FOLDER-")
    folders["outFolder"] = sg.user_settings_get_entry("-OUT FOLDER-")
    folders["localOutFolder"] = sg.user_settings_get_entry("-LOCAL OUT FOLDER-")
    return folders


def validate_band_range(values):
    if values["-BAND RANGE-"] == "":
        return False
    return True


def handle_settings_event(inst, inst_found, main_window, inst_info):
    settings_changed = launch_settings_window(inst)
    if settings_changed:
        settings_error = validate_settings(inst)
        update_main_window(main_window, inst_found, inst_info, settings_error)


def main():
    sg.theme("SystemDefaultForReal")
    # default location for this file is Users/<username>/AppData/Local/PySimpleGUI/settings/
    sg.user_settings_filename("autosa.json")

    # Assert that NI-VISA is installed, else throw error dialog
    ni_visa_installed = assert_ni_visa_installed(pyvisa)
    if not ni_visa_installed:
        return

    inst, inst_found = get_inst()
    main_window = get_main_mindow(inst_found, "", "")

    while True:
        timeout = 500 if inst_found else 200

        # without timeout, code pauses here and waits for event
        event, values = main_window.read(timeout=timeout)

        inst, inst_found = get_inst()
        settings_error = validate_settings(inst) if inst_found else ""
        inst_info = get_inst_info(inst) if inst_found else ""

        update_main_window(main_window, inst_found, inst_info, settings_error)

        if event == "Settings":
            handle_settings_event(inst, inst_found, main_window, inst_info)
        if event == sg.WIN_CLOSED:
            break

        site_name = sg.user_settings_get_entry("-SITE-")
        last_run_index = int(values["-LAST INDEX-"])
        sweep_dur = float(sg.user_settings_get_entry("-SWEEP DUR-"))
        folders = get_folders()
        run_error_message = ""

        main_window["-RUN-"].update(disabled=not validate_band_range(values))
        if event == "-RUN-":
            band_keys = (
                ["B0", "B1", "B2", "B3", "B4"]
                if values["-BAND RANGE-"] == "B0 - B4 (monopole)"
                else ["B5", "B6", "B7"]
                if values["-BAND RANGE-"] == "B5 - B7 (bilogical)"
                else ""
            )

            run_error_message = record_multiple_bands(
                inst,
                site_name,
                last_run_index,
                folders,
                band_keys,
                sweep_dur,
                main_window,
            )

        if "BUTTON" in event:
            substring = event.split("-")[1]
            band_key = substring.split(" ")[1]

            run_error_message = record_single_band(
                inst, site_name, last_run_index, folders, band_key, sweep_dur
            )

        if run_error_message != "":
            sg.popup_error(
                run_error_message,
                title="Error",
            )

    main_window.close()


if __name__ == "__main__":
    main()
