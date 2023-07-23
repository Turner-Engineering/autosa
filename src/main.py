import time

import PySimpleGUI as sg
import pyvisa

from instrument.instrument import (
    get_inst,
    get_inst_info,
    get_run_filename,
    run_band,
)
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


def validate_band_range(values):
    if values["-BAND RANGE-"] == "":
        return False
    return True


def handle_settings_event(inst, inst_found, main_window, inst_info):
    settings_changed = launch_settings_window(inst)
    if settings_changed:
        settings_error = validate_settings(inst)
        update_main_window(main_window, inst_found, inst_info, settings_error)


def run_record_and_save(inst, settings):
    band_key = sg.popup_get_text(
        "Enter band name (e.g. B3, B5h, B7v):",
        title="Band Name",
    )
    if band_key == None:
        return

    run_filename = get_run_filename(inst, settings, band_key)

    run_band(inst, settings, band_key, run_filename, setup=False)


def run_single_band(inst, settings, band_key, orientation):
    # difference between this and run band is this one confirms the filename
    # READ SETTINGS
    run_filename = get_run_filename(inst, settings, band_key, orientation)

    # CONFIRMATION
    confirmation = sg.popup_ok_cancel(
        f'Confirm run filename:\n\n"{run_filename}"',
        title="Confirm Run",
    )
    if confirmation != "OK":
        return ""

    error_message = run_band(inst, settings, band_key, run_filename)
    return error_message


def run_multiple_bands(inst, settings, band_keys, window, orientation):
    # CONFIRMATION
    first_run_filename = get_run_filename(inst, settings, band_keys[0], orientation)
    num_runs = len(band_keys)
    part1 = f"Please confirm that you would like to run bands\n\n{band_keys[0]} to {band_keys[-1]} ({num_runs} runs total)\n\n"
    part2 = f'and that the first filename should be:\n\n"{first_run_filename}"\n (the rest will be numbered sequentially)'
    confirmation = sg.popup_ok_cancel(
        part1 + part2,
        title="Confirm Runs",
    )
    if confirmation != "OK":
        return ""

    # PROGRESS BAR
    bar_max = len(band_keys)
    pbar = window["-PROGRESS-"]
    pbar.update_bar(bar_max / 50, bar_max)

    error_message = ""
    for i in range(len(band_keys)):
        band_key = band_keys[i]
        run_filename = get_run_filename(inst, settings, band_key, orientation)

        # PROGRESS BAR
        time.sleep(2)  #  not sure what this is for
        pbar.update_bar(i + 1, bar_max)

        run_band(inst, settings, band_key, run_filename)
        if error_message != "":
            break

    # PROGRESS BAR
    time.sleep(1)
    pbar.update_bar(0, bar_max)

    return error_message


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

        update_main_window(main_window, inst_found, inst_info, settings_error, values)

        if event == "Settings":
            handle_settings_event(inst, inst_found, main_window, inst_info)
        if event == sg.WIN_CLOSED:
            break

        run_error_message = ""
        settings = sg.user_settings()

        main_window["-RUN-"].update(disabled=not validate_band_range(values))
        if event == "-RUN-":
            band_range = values["-BAND RANGE-"]
            band_keys = (
                ["B0", "B1", "B2", "B3", "B4"]
                if band_range == "B0 - B4 (monopole)"
                else ["B5", "B6", "B7"]
                if band_range == "B5 - B7 (bilogical)"
                else ""
            )

            # orientation is lowercase first letter of the word
            orientation = (
                values["-ORIENTATION-"][0].lower()
                if band_range == "B5 - B7 (bilogical)"
                else ""
            )

            run_error_message = run_multiple_bands(
                inst,
                settings,
                band_keys,
                main_window,
                orientation,
            )

        if "BUTTON" in event:
            items = event.split("-")[1].split(" ")
            band_key, orientation = items[1], items[2]
            run_error_message = run_single_band(
                inst,
                settings,
                band_key,
                orientation,
            )

        if event == "-RECORD AND SAVE-":
            run_record_and_save(inst, settings)

        if run_error_message != "":
            sg.popup_error(
                run_error_message,
                title="Error",
            )

    main_window.close()


if __name__ == "__main__":
    main()
