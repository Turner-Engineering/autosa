import datetime
import time

import pyvisa

from bands_data import bands
from instrument.file_transfer import save_file_to_local
from instrument.folders import get_folder_files


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


def record_band(inst, inst_out_folder, filename, local_out_folder, sweep_dur=5):
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

    # TRANSFER
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


def get_run_id(run_index):
    run_number = "%02d" % run_index
    d = datetime.datetime.now()
    month = str(int(d.strftime("%m")))
    date = d.strftime("%d")
    run_id = f"{month}{date}-{run_number}"
    return run_id


def get_run_filename(run_index, band_name, notes):
    run_id = get_run_id(run_index)
    filename = f"{run_id} {notes} {band_name}"
    return filename


def record_multiple_bands(
    inst,
    site_name,
    last_run_index,
    folders,
    band_keys,
    sweep_dur,
    window,
):
    bar_max = len(band_keys)
    pbar = window["-PROGRESS-"]
    pbar.update_bar(bar_max / 50, bar_max)
    error_message = ""
    for i, band_key in enumerate(band_keys):
        time.sleep(sweep_dur)
        pbar.update_bar(i + 1, bar_max)
        run_index = i + 1 + last_run_index
        error_message = record_single_band(
            inst,
            site_name,
            run_index,
            folders,
            band_key,
            sweep_dur,
        )
        if error_message != "":
            break
    time.sleep(1)
    pbar.update_bar(0, bar_max)
    return error_message


def write_txt_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)
    return


def record_single_band(
    inst,
    site_name,
    run_index,
    folders,
    band_key,
    sweep_dur,
):
    coupling = bands[band_key]["coupling"]

    state_filename = bands[band_key]["stateFilename"]
    corr_filename = bands[band_key]["corrFilename"]
    run_filename = get_run_filename(run_index, band_key, site_name)

    recall_state(inst, folders["stateFolder"], state_filename)
    recall_corr(inst, folders["corrFolder"], corr_filename)
    set_coupling(inst, coupling)

    inst_out_folder = folders["outFolder"]
    local_out_folder = folders["localOutFolder"]

    error_message = validate_filename(inst, inst_out_folder, run_filename)
    if error_message != "":
        return error_message

    record_band(
        inst,
        inst_out_folder,
        run_filename,
        local_out_folder,
        sweep_dur,
    )
    return error_message


def get_inst_info(inst):
    resp = inst.query(":SYST:IDN?")
    manufacturer, model, serial, _ = resp.split(",")
    return f"{manufacturer} - {model} - {serial}"
