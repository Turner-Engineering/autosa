import time

import pyvisa

from bands_data import bands
from instrument.file_transfer import save_file_to_local
from instrument.folders import get_folder_files
from utils.run_ids import run_index_to_id, get_todays_run_ids


def get_run_id(inst, inst_out_folder):
    filenames = get_folder_files(inst, inst_out_folder)
    todays_run_ids = get_todays_run_ids(filenames)
    todays_run_idxs = [int(run_id.split("-")[1]) for run_id in todays_run_ids]
    last_run_index = max(todays_run_idxs) if todays_run_idxs else 0
    run_index = last_run_index + 1
    run_id = run_index_to_id(run_index)
    return run_id


def get_resource_name(resource_manager):
    resource_names = resource_manager.list_resources()
    resource_names = [r for r in resource_names if "USB" in r]
    resource_names = [r for r in resource_names if "::INSTR" in r]
    resource_name = "" if len(resource_names) == 0 else resource_names[0]
    return resource_name


def get_inst():
    resource_manager = pyvisa.ResourceManager()
    resource_name = get_resource_name(resource_manager)
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


def record_and_save(inst, inst_out_folder, filename, local_out_folder, sweep_dur):
    # and this version which just does the measurement and saving
    # RECORD
    inst.write(":INIT:REST")
    inst.write(":INIT:CONT ON")
    time.sleep(sweep_dur)
    inst.write(":INIT:CONT OFF")

    # SAVE
    csv_path = f"{inst_out_folder}/{filename}.csv"
    png_path = f"{inst_out_folder}/{filename}.png"
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csv_path}"')
    inst.write(f':MMEM:STOR:SCR "{png_path}"')
    save_file_to_local(inst, png_path, local_out_folder)
    save_file_to_local(inst, csv_path, local_out_folder)
    return


def recall_state(inst, state_folder, filename):
    inst.write(f":MMEM:LOAD:STAT '{state_folder}/{filename}'")
    return


def recall_corr(inst, corr_folder, filename):
    inst.write(f":MMEM:LOAD:CORR 1,'{corr_folder}/{filename}'")
    return


def set_coupling(inst, coupling):
    inst.write(f":INP:COUP {coupling}")
    # print(inst.query(f":INP:COUP?"))


def get_run_filename(inst, settings, band_name, orientation=""):
    inst_out_folder = settings["-OUT FOLDER-"]
    notes = settings["-RUN NOTE-"]
    run_id = get_run_id(inst, inst_out_folder)
    filename = f"{run_id} {notes} {band_name}{orientation}"
    return filename


def write_txt_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)
    return


def get_inst_info(inst):
    resp = inst.query(":SYST:IDN?")
    manufacturer, model, serial, _ = resp.split(",")
    return f"{manufacturer} - {model} - {serial}"


def run_band(inst, settings, band_key, run_filename, setup=True):
    inst_out_folder = settings["-OUT FOLDER-"]
    local_out_folder = settings["-LOCAL OUT FOLDER-"]
    state_folder = settings["-STATE FOLDER-"]
    corr_folder = settings["-CORR FOLDER-"]
    sweep_dur = float(settings["-SWEEP DUR-"])

    # READ BAND SETTINGS
    coupling = bands[band_key]["coupling"]
    state_filename = bands[band_key]["stateFilename"]
    corr_filename = bands[band_key]["corrFilename"]

    # GET THE FILENAME AND CHECK FOR CONFLICTS
    error_message = validate_filename(inst, inst_out_folder, run_filename)
    if error_message != "":
        return error_message

    # SET UP THE INSTRUMENT
    if setup:
        recall_state(inst, state_folder, state_filename)
        recall_corr(inst, corr_folder, corr_filename)
        set_coupling(inst, coupling)

    # RECORD AND SAVE
    record_and_save(inst, inst_out_folder, run_filename, local_out_folder, sweep_dur)
    return error_message
