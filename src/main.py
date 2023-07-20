import PySimpleGUI as sg
import pyvisa

from instrument.instrument import get_inst_found, get_resource_name, record_bands
from ui.main_window import get_main_mindow, update_main_window
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

    # Assert that NI-VISA is installed, else throw error dialog
    ni_visa_installed = assert_ni_visa_installed(pyvisa)
    if not ni_visa_installed:
        return

    resource_manager = pyvisa.ResourceManager()
    resource_name = get_resource_name(resource_manager)
    inst_found = get_inst_found(resource_name)
    settings_error = validate_settings(resource_name)

    main_window = get_main_mindow(inst_found, resource_name, finalize=True)
    update_main_window(main_window, inst_found, resource_name, settings_error)

    while True:
        timeout = 1000 if inst_found else 200
        event, values = main_window.read(timeout=timeout)
        # without timeout, code pauses here and waits for event
        resource_name = get_resource_name(resource_manager)
        inst_found = get_inst_found(resource_name)
        settings_error = validate_settings(resource_name)
        update_main_window(main_window, inst_found, resource_name, settings_error)

        if event == "Settings":
            settings_changed = launch_settings_window(resource_name)
            if settings_changed:
                main_window.close()
                main_window = get_main_mindow(inst_found, resource_name, finalize=True)
        elif event == sg.WIN_CLOSED:
            break

        if inst_found:
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
                resource_name,
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
