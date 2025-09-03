import csv
import datetime
import os
import time

import pyvisa
import pyvisa.constants as pyvisa_constants
from tzlocal import get_localzone

from instrument.file_transfer import copy_file_to_local
from instrument.folders import get_csv_folder, get_folder_files, get_sorted_folder
from instrument.logged_instrument import LoggedInstrument
from utils.logger import autosa_logger
from utils.run_ids import get_todays_run_ids, run_index_to_id
from utils.settings import get_autosa_version, read_settings_from_file
from utils.test_log import get_latest_test_log

EMULATOR_RESOURCE_NAME = "TCPIP0::localhost::inst0::INSTR"
INPUT_LOG_INFO = {}


def get_run_id(inst, inst_out_folder):
    filenames = get_folder_files(inst, inst_out_folder)
    todays_run_ids = get_todays_run_ids(filenames)
    todays_run_idxs = [int(run_id.split("-")[1]) for run_id in todays_run_ids]
    last_run_index = max(todays_run_idxs) if todays_run_idxs else 0
    run_index = last_run_index + 1
    run_id = run_index_to_id(run_index)

    autosa_logger.debug(f"Generated run ID: {run_id}")
    return run_id


def usb_inst_detected(resource_names):
    usb_resource_names = [r for r in resource_names if "USB" in r]
    return len(usb_resource_names) > 0


def get_resource_name(resource_manager):
    resource_names = resource_manager.list_resources()
    autosa_logger.debug(f"Resource Names: {resource_names}")

    if not usb_inst_detected(resource_names):
        if EMULATOR_RESOURCE_NAME in resource_names:
            return EMULATOR_RESOURCE_NAME
        else:
            return ""

    resource_names = [r for r in resource_names if "USB" in r]
    resource_names = [r for r in resource_names if "::INSTR" in r]
    resource_name = "" if len(resource_names) == 0 else resource_names[0]
    return resource_name


def get_inst():
    resource_manager = pyvisa.ResourceManager()
    resource_name = get_resource_name(resource_manager)
    inst = None

    try:
        if resource_name != "":
            rm = pyvisa.ResourceManager()
            _inst = rm.open_resource(resource_name)
            inst = LoggedInstrument(_inst, autosa_logger)
    except pyvisa.errors.VisaIOError:
        inst = None

    inst_found = inst is not None

    inst_name = (
        "Disconnected Mode"
        if inst is None
        else "Emulator"
        if resource_name is EMULATOR_RESOURCE_NAME
        else "Instrument"
    )

    if inst_found and inst_name == "Instrument":
        autosa_logger.info(f"Connected to Instrument at: '{resource_name}'")
    elif inst_found and inst_name == "Emulator":
        autosa_logger.info(f"Connected to Emulator at: '{resource_name}'")
    else:
        autosa_logger.info("No instrument found. Running in Disconnected Mode.")

    return inst, inst_found, inst_name


def get_error_message(folder_path, filename):
    part1 = f'File "{filename}" already exists in instrument folder:'
    part2 = f'"{folder_path}"'
    part3 = "Please save this run with a different filename."
    return "\n\n".join([part1, part2, part3])


def validate_filename(inst, inst_out_folder, filename):
    error_message = ""
    # NOTE: these extensions are the ones used in the record_band function
    # if the extensions in that function change, so should these
    extensions = ["csv", "png"]
    new_filenames = [f"{filename}.{ext}" for ext in extensions]
    old_filenames = get_folder_files(inst, inst_out_folder)

    # check if there are any conflicts, if so return an error message about the first one
    intersection = set(new_filenames).intersection(old_filenames)
    if len(intersection) > 0:
        bad_filename = list(intersection)[0]
        error_message = get_error_message(inst_out_folder, bad_filename)
    return error_message


# ONE LINERS
def release_inst(inst):
    inst.control_ren(pyvisa_constants.VI_GPIB_REN_DEASSERT_GTL)
    autosa_logger.info("Instrument released.")


def update_state(inst, state_folder, filename):
    inst.write(f":MMEM:STOR:STAT '{state_folder}/{filename}'")


def recall_state(inst, state_folder, filename):
    inst.write(f":MMEM:LOAD:STAT '{state_folder}/{filename}'")


def recall_corr(inst, corr_folder, filename):
    inst.write(f":MMEM:LOAD:CORR 1,'{corr_folder}/{filename}'")


def set_coupling(inst, coupling):
    inst.write(f":INP:COUP {coupling}")


def run_start(inst):
    autosa_logger.info("Measurement started.")
    inst.write(":INIT:CONT ON")


def run_stop(inst):
    autosa_logger.info("Measurement stopped.")
    inst.write(":INIT:CONT OFF")


def run_reset(inst):
    inst.write(":INIT:REST")


def set_marker_to_max(inst):
    inst.write(":CALC:MARK1:MAX")


def save_trace(inst, csv_path):
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csv_path}"')


def set_ref_level(inst, ref_level):
    inst.write(f":DISP:WIND:TRAC:Y:RLEV {ref_level}")


def get_freq_start(inst):
    return inst.query(":SENS:FREQ:STAR?").strip()


def get_freq_stop(inst):
    return inst.query(":SENS:FREQ:STOP?").strip()


def get_rbw(inst):
    return inst.query(":SENS:BAND:RES?").strip()


def get_max_amp_freq(inst, trace=1):
    get_trace_max(inst, trace)
    return inst.query(f":CALC:MARK{trace}:X?").strip()


def get_atten(inst):
    return inst.query(":POW:ATT?").strip()


def get_ref_level(inst):
    if inst is not None:
        ref_level = float(inst.query(":DISP:WIND:TRAC:Y:RLEV?").replace("\n", ""))
    else:
        ref_level = 0.0
    return ref_level


def get_ref_offset(inst):
    return float(inst.query(":DISP:WIND:TRAC:Y:RLEV:OFFS?"))


def disable_ref_level_offset(inst):
    inst.write(":DISP:WIND:TRAC:Y:RLEV:OFFS:STAT OFF")


def get_trace_max(inst, trace_num=1):
    data = inst.query(f":TRAC? TRACE{trace_num}").replace("\n", "")
    data = data.split(",")
    data = [float(d) for d in data]
    return max(data)


def compare_datetime(inst, inst_name):
    # doesn't launch in Disconnected Mode without this check
    if inst_name in ["Emulator", "Instrument"]:
        dt_fmt = "%Y,%m,%d %H,%M,%S"
        inst_date = inst.query("SYST:DATE?").strip()
        inst_time = inst.query("SYST:TIME?").strip()

        inst_datetime = datetime.datetime.strptime(f"{inst_date} {inst_time}", dt_fmt)
        local_datetime = datetime.datetime.now().replace(second=0, microsecond=0)
        inst_datetime = inst_datetime.replace(second=0, microsecond=0)

        datetime_diff = abs(inst_datetime - local_datetime)

        return datetime_diff, datetime_diff.seconds < 300

    return 0, False


def adjust_ref_level(inst):
    trace_max = get_trace_max(inst)
    ref_level = get_ref_level(inst)
    if trace_max > ref_level:
        new_ref_level = round(trace_max / 10) * 10
        set_ref_level(inst, new_ref_level)


def round_ref_level(inst):
    ref_level = get_ref_level(inst)
    new_ref_level = round(ref_level / 10) * 10
    set_ref_level(inst, new_ref_level)


def set_rounded_ref_level(inst, ref_level):
    new_ref_level = round(ref_level / 10) * 10
    set_ref_level(inst, new_ref_level)


def rename_screen(inst, new_name):
    old_name = inst.query(":INST:SCR:SELECT?").replace("\n", "").replace('"', "")
    if old_name != new_name:
        inst.write(f":INST:SCR:REN '{new_name}'")


def save_screen(inst, png_path):
    inst.write(":DISP:FSCR:STAT ON")  # set to full screen
    inst.write(":MMEM:STOR:SCR:THEM OUTL")  # set to light mode
    inst.write(f':MMEM:STOR:SCR "{png_path}"')  # save screen


def save_trace_and_screen(
    inst,
    filename: str,
    inst_out_folder: str,
    local_out_folder: str,
    band: str,
    run_note: str,
    sweep_dur: float,
):
    """Save the trace to a csv file and the screen to a png file on the instrument, then copy both to the local computer

    Args:
        inst (instrument): the signal analyzer
        filename (string): the filename without extension used to save the image and trace
        inst_out_folder (string): path to instrument output folder
        local_out_folder (string): path to local output folder
    """

    write_to_test_log(inst, filename, run_note, band, sweep_dur)  # upon save

    csv_path = f"{inst_out_folder}/{filename}.csv"
    png_path = f"{inst_out_folder}/{filename}.png"

    save_trace(inst, csv_path)
    save_screen(inst, png_path)

    sorted_csv_folder = get_csv_folder(local_out_folder)
    sorted_png_folder = get_sorted_folder(local_out_folder, band)

    copy_file_to_local(inst, csv_path, sorted_csv_folder)
    copy_file_to_local(inst, png_path, sorted_png_folder)

    autosa_logger.info(f"Trace saved to {sorted_csv_folder}")
    autosa_logger.info(f"Image saved to {sorted_png_folder}")


def record_and_adjust(inst, sweep_dur):
    inst.write(":INIT:REST")
    inst.write(":INIT:CONT ON")
    time.sleep(sweep_dur)
    inst.write(":INIT:CONT OFF")

    # ADJUST
    set_marker_to_max(inst)
    # adjust_ref_level(inst)


def recall_cors(inst, corr_folder, corr_filename):
    for i in range(16):
        idx = i + 1
        inst.write(f":SENS:CORR:CSET{idx} OFF")

    inst.write(f":MMEM:LOAD:CORR 1, '{corr_folder}/{corr_filename}'")


def create_run_filename(run_id, run_note, band_name, sweep_dur):
    saved_time = datetime.datetime.now().strftime("%H_%M_%S")
    filename = f"{run_id} {run_note} {sweep_dur}s {band_name} {saved_time}"
    return saved_time, filename


def get_run_filename(inst, band_key, run_note, sweep_dur, band_ori=""):
    inst_out_folder = read_settings_from_file()["-INST OUT FOLDER-"]
    run_id = get_run_id(inst, inst_out_folder)
    band_name = band_key + band_ori
    saved_time, filename = create_run_filename(run_id, run_note, band_name, sweep_dur)
    return saved_time, filename


def write_txt_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)
    return


def get_inst_info(inst):
    resp = inst.query(":SYST:IDN?")
    manufacturer, model, serial, _ = resp.split(",")
    return f"{manufacturer} - {model} - {serial}"


def get_state_file(inst, state_folder, band_key):
    state_filenames = get_folder_files(inst, state_folder)
    for filename in state_filenames:
        if band_key in filename:
            return filename


def prep_band(inst, band_key):
    error_message = ""
    state_folder = read_settings_from_file()["-STATE FOLDER-"]
    corr_folder = read_settings_from_file()["-CORR FOLDER-"]
    state_filename = get_state_file(inst, state_folder, band_key)
    corr_filename = read_settings_from_file()["-CORR CHOICES-"][f"{band_key}"]

    try:
        recall_state(inst, state_folder, state_filename)
        autosa_logger.debug(f"Recalled State: {state_filename}")

        if corr_filename != "No Correction":
            recall_cors(inst, corr_folder, corr_filename)
            autosa_logger.debug(f"Recalled Amplitude Correction: {corr_filename}")
        else:
            autosa_logger.debug(
                f"No Amplitude Correction file selected for {band_key}."
            )

        rename_screen(inst, band_key)
        disable_ref_level_offset(inst)
        round_ref_level(inst)
        inst.write(":INIT:REST")
        release_inst(inst)
    except Exception as e:
        error_message = str(e)
    return error_message


def run_band(inst, band_key, run_filename, band_ori, run_note, save=True):
    inst_out_folder = read_settings_from_file()["-INST OUT FOLDER-"]
    local_out_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]
    sweep_dur = float(read_settings_from_file()["-SWEEP DUR-"])

    # GET THE FILENAME AND CHECK FOR CONFLICTS
    if save:
        error_message = validate_filename(inst, inst_out_folder, run_filename)
        if error_message != "":
            return error_message

    # PREPARE THE INSTRUMENT
    error_message = prep_band(inst, band_key)

    # RECORD, ADJUST, AND SAVE
    record_and_adjust(inst, sweep_dur)
    # this gives the instrument time to clear the screen of any alerts (they take about 3 seconds to clear)

    time.sleep(5)

    if save:
        band_name = band_key + band_ori
        save_trace_and_screen(
            inst,
            run_filename,
            inst_out_folder,
            local_out_folder,
            band_name,
            run_note,
            sweep_dur,
        )

    return error_message


def get_input(test_log_data):
    global INPUT_LOG_INFO
    INPUT_LOG_INFO = test_log_data
    return INPUT_LOG_INFO


# TODO - move out of instrument.py to utils
def write_to_test_log(inst, run_filename, run_note, band, sweep_dur):
    # new test log was initiated - user input
    global INPUT_LOG_INFO
    input_fields = INPUT_LOG_INFO

    # log_filename = input_fields.get("Log Filename") # new filename
    test_engineer = input_fields.get("Test Engineer")
    project_name = input_fields.get("Project Name")

    laptop_name = os.environ.get("COMPUTERNAME")
    local_tz = get_localzone()
    version = get_autosa_version()

    # get band info
    band_key = band[:2]
    band_ori = (
        "" if (len(band) == 2 or band[2].lower() not in ["h", "v"]) else band[2].lower()
    )
    antenna_orientation = (
        "Horizontal" if band_ori == "h" else "Vertical" if band_ori == "v" else "None"
    )

    # time info
    saved_time, _ = get_run_filename(inst, band_key, run_note, sweep_dur, band_ori)
    date = datetime.datetime.now().strftime("%Y-%m-%d")

    if get_latest_test_log() == "No test logs found.":
        log_filename = f"autosa_test_log_{date}.csv"
    else:
        log_filename = get_latest_test_log()

    # folders
    settings = read_settings_from_file()
    inst_out_folder = settings["-INST OUT FOLDER-"]
    state_folder = settings["-STATE FOLDER-"]
    local_out_folder = settings["-LOCAL OUT FOLDER-"]
    corr_folder = settings["-CORR FOLDER-"]
    corr_filenames = settings["-CORR CHOICES-"]

    # filenames
    corr_filename = corr_filenames.get(band_key, "No Correction")
    state_filename = get_state_file(inst, state_folder, band_key)

    # other run info
    run_id = get_run_id(inst, inst_out_folder)
    ref_level = get_ref_level(inst)
    ref_offset = get_ref_offset(inst)
    freq_start = get_freq_start(inst)
    freq_stop = get_freq_stop(inst)
    rbw = get_rbw(inst)
    max_amp = get_trace_max(inst)
    max_amp_freq = get_max_amp_freq(inst)
    atten = get_atten(inst)
    # mode of measurement (manual, single band, multi band) - circular import

    intro_info = {
        "Project Name": project_name,
        "Timezone": local_tz,
        "Test Engineer": test_engineer,
        "Autosa Version": version,
        "Instrument ID": inst,
        "Test Laptop Name": laptop_name,
        "State Folder": state_folder,
        "Correction Folder": corr_folder,
        "Instrument Output Folder": inst_out_folder,
        "Local Output Folder": local_out_folder,
    }

    measurement_data = {
        "Run ID": run_id,
        "Run Note": run_note,
        "Sweep Dur": sweep_dur,
        "Band": band_key,
        "Antenna Orientation": antenna_orientation,
        "Time": saved_time,
        "Date": date,
        "Run Filename (csv/png)": run_filename,
        "State Filename": state_filename,
        "Correction Filename": corr_filename,
        "Reference Level": ref_level,
        "Reference Offset": ref_offset,
        "Frequency Start": freq_start,
        "Frequency Stop": freq_stop,
        "Resolution Bandwidth": rbw,
        "Max Amplitude": max_amp,
        "Max Amplitude Frequency": max_amp_freq,
        "Attenuation (dB)": atten,
    }

    try:
        test_log_path = os.path.join(local_out_folder, log_filename)
        file_exists = os.path.exists(test_log_path)
        is_empty = not file_exists or os.stat(test_log_path).st_size == 0

        if is_empty:
            with open(test_log_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                # Write once-off info
                for key, value in intro_info.items():
                    writer.writerow([f"{key}: {value}"])
                writer.writerow(["++++++++++++++++++++"])
                writer.writerow(measurement_data.keys())

        for key, value in measurement_data.items():
            if value == "" or value == "No Correction" or value is None:
                measurement_data[key] = "UNKNOWN"

        with open(test_log_path, mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(measurement_data.values())

    except Exception as e:
        print(f"Failed to write log entry: {e}")
