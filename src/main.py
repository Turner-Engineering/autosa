import time

import PySimpleGUI as sg
import pyvisa

from instrument.instrument import (
    get_inst,
    get_run_id,
    get_inst_info,
    get_run_filename,
    prep_band,
    run_band,
    run_start,
    run_stop,
    run_reset,
    release_inst,
    set_marker_to_max,
    adjust_ref_level,
    save_trace_and_screen,
)
from ui.main_window import get_main_mindow, update_main_window
from ui.manual_mode import update_start_stop_button
from ui.settings_window import (
    launch_settings_window,
    validate_settings,
    add_default_settings,
    save_settings,
)

from ui.get_filename_from_user import get_filename_from_user
from utils.stopwatch import Stopwatch


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


def update_stopwatch_time(main_window, stopwatch):
    main_window["-STOPWATCH TIME-"].update(
        stopwatch.get_time_str(),
        text_color="black" if stopwatch.get_time() == 0 else "green",
    )


def handle_settings_event(inst, inst_found, main_window, inst_info):
    settings_changed = launch_settings_window(inst)
    if settings_changed:
        settings_error = validate_settings(inst)
        update_main_window(main_window, inst_found, inst_info, settings_error)


def run_single_band(inst, settings, band_key, band_ori):
    # PREPARE, RECORD, ADJUST
    error_message = run_band(inst, settings, band_key, "", save=False)

    # GET FILENAME
    run_id = get_run_id(inst, settings["-INST OUT FOLDER-"])
    run_filename = get_filename_from_user(run_id, band_key, band_ori)

    # SAVE
    if run_filename != None:
        inst_out_folder = settings["-INST OUT FOLDER-"]
        local_out_folder = settings["-LOCAL OUT FOLDER-"]
        save_trace_and_screen(inst, run_filename, inst_out_folder, local_out_folder)
    return error_message


def run_multiple_bands(inst, settings, band_keys, window, band_ori):
    # CONFIRMATION
    first_run_filename = get_run_filename(inst, settings, band_keys[0], band_ori)
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
        run_filename = get_run_filename(inst, settings, band_key, band_ori)

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
    settings = sg.user_settings()
    settings = add_default_settings(settings)
    save_settings(settings)

    # Assert that NI-VISA is installed, else throw error dialog
    ni_visa_installed = assert_ni_visa_installed(pyvisa)
    if not ni_visa_installed:
        return

    inst, inst_found = get_inst()
    main_window = get_main_mindow(inst_found, "", "")
    stopwatch = Stopwatch()

    while True:
        timeout = 50 if inst_found else 200

        # without timeout, code pauses here and waits for event
        event, values = main_window.read(timeout=timeout)
        if event == sg.WIN_CLOSED:
            inst.control_ren(pyvisa.constants.VI_GPIB_REN_DEASSERT_GTL)
            break

        inst, inst_found = get_inst()
        if "Release" not in values["-TAB GROUP-"]:
            settings_error = validate_settings(inst) if inst_found else ""
            inst_info = get_inst_info(inst) if inst_found else ""

            update_main_window(
                main_window, inst_found, inst_info, settings_error, values
            )
        else:
            release_inst(inst)

        if event == "Settings":
            handle_settings_event(inst, inst_found, main_window, inst_info)

        run_error_message = ""
        settings = sg.user_settings()
        update_stopwatch_time(main_window, stopwatch)

        main_window["-RUN-"].update(disabled=not validate_band_range(values))
        if event == "-RUN-":
            band_range = values["-BAND RANGE-"]
            band_keys = (
                ["B0", "B1", "B2", "B3", "B4"]
                if band_range == "B0 - B4 (monopole)"
                else ["B5", "B6", "B7"] if band_range == "B5 - B7 (bilogical)" else ""
            )

            # band_ori is lowercase first letter of the word "Horizontal" or "Vertical"
            band_ori = (
                values["-ORIENTATION-"][0].lower()
                if band_range == "B5 - B7 (bilogical)"
                else ""
            )

            run_error_message = run_multiple_bands(
                inst,
                settings,
                band_keys,
                main_window,
                band_ori,
            )

        if "SINGLE_BAND" in event:
            items = event.split("-")[1].split(" ")
            band_key, band_ori = items[1], items[2]
            run_error_message = run_single_band(
                inst,
                settings,
                band_key,
                band_ori,
            )

        if "PREP_BAND" in event:
            items = event.split("-")[1].split(" ")
            band_key, band_ori = items[1], items[2]
            run_error_message = prep_band(inst, settings, band_key)
            main_window["-LAST BAND PREPARED-"].update(band_key)
            stopwatch.reset()
            update_stopwatch_time(main_window, stopwatch)
            update_start_stop_button(main_window, "Start")

        if event == "-SAVE TRACE AND SCREEN-":
            run_id = get_run_id(inst, settings["-INST OUT FOLDER-"])
            run_filename = get_filename_from_user(run_id)
            if run_filename == None:
                continue
            inst_out_folder = settings["-INST OUT FOLDER-"]
            local_out_folder = settings["-LOCAL OUT FOLDER-"]

            save_trace_and_screen(inst, run_filename, inst_out_folder, local_out_folder)
            run_error_message = ""

        start_stop_state = main_window["-START STOP-"].metadata
        if event == "-START STOP-" and start_stop_state == "Start":
            run_start(inst)
            stopwatch.start()
            main_window["-STOPWATCH START TIME-"].update(stopwatch.get_start_time_str())
            update_start_stop_button(main_window, "Stop")
            update_stopwatch_time(main_window, stopwatch)

        elif event == "-START STOP-" and start_stop_state == "Stop":
            run_stop(inst)
            set_marker_to_max(inst)
            # adjust_ref_level(inst)
            stopwatch.stop()
            update_start_stop_button(main_window, "Start")
            update_stopwatch_time(main_window, stopwatch)

        elif event == "-RESET-":
            run_stop(inst)
            run_reset(inst)
            stopwatch.reset()
            update_start_stop_button(main_window, "Start")
            update_stopwatch_time(main_window, stopwatch)

        if run_error_message != "":
            sg.popup_error(
                run_error_message,
                title="Error",
            )

    main_window.close()


if __name__ == "__main__":
    main()
