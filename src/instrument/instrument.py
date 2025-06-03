import time
import pyvisa

from instrument.file_transfer import copy_file_to_local
from instrument.folders import get_folder_files
from utils.run_ids import run_index_to_id, get_todays_run_ids
from utils.settings import read_settings_from_file


def get_run_id(inst, inst_out_folder):
    filenames = get_folder_files(inst, inst_out_folder)
    todays_run_ids = get_todays_run_ids(filenames)
    todays_run_idxs = [int(run_id.split("-")[1]) for run_id in todays_run_ids]
    last_run_index = max(todays_run_idxs) if todays_run_idxs else 0
    run_index = last_run_index + 1
    run_id = run_index_to_id(run_index)
    return run_id


def get_resource_name(resource_manager, emulator_mode):
    resource_names = resource_manager.list_resources()
    if emulator_mode:
        resource_names = ["TCPIP0::localhost::inst0::INSTR"]
        # resource_names = [r for r in resource_names if "inst0" in r]
    else:
        resource_names = [r for r in resource_names if "USB" in r]
    resource_names = [r for r in resource_names if "::INSTR" in r]
    resource_name = "" if len(resource_names) == 0 else resource_names[0]
    return resource_name


def get_inst():
    emulator_mode = False
    # emulator_mode = True  # Set to True for emulator mode, False for real instrument
    resource_manager = pyvisa.ResourceManager()
    resource_name = get_resource_name(resource_manager, emulator_mode)
    inst = None
    if resource_name != "":
        rm = pyvisa.ResourceManager()
        inst = rm.open_resource(resource_name)
    inst_found = inst is not None
    return inst, inst_found


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
    inst.control_ren(pyvisa.constants.VI_GPIB_REN_DEASSERT_GTL)


def recall_state(inst, state_folder, filename):
    inst.write(f":MMEM:LOAD:STAT '{state_folder}/{filename}'")


def recall_corr(inst, corr_folder, filename):
    inst.write(f":MMEM:LOAD:CORR 1,'{corr_folder}/{filename}'")


def set_coupling(inst, coupling):
    inst.write(f":INP:COUP {coupling}")


def run_start(inst):
    inst.write(":INIT:CONT ON")


def run_stop(inst):
    inst.write(":INIT:CONT OFF")


def run_reset(inst):
    inst.write(":INIT:REST")


def set_marker_to_max(inst):
    inst.write(":CALC:MARK1:MAX")


def save_trace(inst, csv_path):
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csv_path}"')


def set_ref_level(inst, ref_level):
    inst.write(f":DISP:WIND:TRAC:Y:RLEV {ref_level}")


def get_ref_level(inst):
    ref_level = float(inst.query(":DISP:WIND:TRAC:Y:RLEV?").replace("\n", ""))
    return ref_level


def disable_ref_level_offset(inst):
    inst.write(":DISP:WIND:TRAC:Y:RLEV:OFFS:STAT OFF")


def get_trace_max(inst, trace_num=1):
    data = inst.query(f":TRAC? TRACE{trace_num}").replace("\n", "")
    data = data.split(",")
    data = [float(d) for d in data]
    return max(data)


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


def rename_screen(inst, new_name):
    old_name = inst.query(":INST:SCR:SELECT?").replace("\n", "").replace('"', "")
    if old_name != new_name:
        inst.write(f":INST:SCR:REN '{new_name}'")


def save_screen(inst, png_path):
    inst.write(":DISP:FSCR:STAT ON")  # set to full screen
    inst.write(":MMEM:STOR:SCR:THEM OUTL")  # set to light mode
    inst.write(f':MMEM:STOR:SCR "{png_path}"')  # save screen


def save_trace_and_screen(
    inst, filename: str, inst_out_folder: str, local_out_folder: str
):
    """Save the trace to a csv file and the screen to a png file on the instrument, then copy both to the local computer

    Args:
        inst (instrument): the signal analyzer
        filename (string): the filename without extension used to save the image and trace
        inst_out_folder (string): path to instrument output folder
        local_out_folder (string): path to local output folder
    """
    csv_path = f"{inst_out_folder}/{filename}.csv"
    png_path = f"{inst_out_folder}/{filename}.png"
    save_trace(inst, csv_path)
    save_screen(inst, png_path)
    copy_file_to_local(inst, png_path, local_out_folder)
    copy_file_to_local(inst, csv_path, local_out_folder)


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


def create_run_filename(run_id, run_note, band_name):
    filename = f"{run_id} {run_note} {band_name}"
    return filename


def get_run_filename(inst, band_key, run_note, band_ori=""):
    inst_out_folder = read_settings_from_file()["-INST OUT FOLDER-"]
    run_id = get_run_id(inst, inst_out_folder)
    band_name = band_key + band_ori
    filename = create_run_filename(run_id, run_note, band_name)
    return filename


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
        if corr_filename != "No Correction":
            recall_cors(inst, corr_folder, corr_filename)
        rename_screen(inst, band_key)
        disable_ref_level_offset(inst)
        round_ref_level(inst)
        inst.write(":INIT:REST")
        release_inst(inst)
    except Exception as e:
        error_message = str(e)
    return error_message


def run_band(inst, band_key, run_filename, save=True):
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
        save_trace_and_screen(inst, run_filename, inst_out_folder, local_out_folder)

    return error_message
