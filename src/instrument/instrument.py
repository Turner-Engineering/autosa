import datetime
import time

import pyvisa

from bands_data import bands
from instrument.file_transfer import save_file_to_local


def get_resource_name(resource_manager):
    resource_names = resource_manager.list_resources()
    resource_names = [r for r in resource_names if "USB" in r]
    resource_names = [r for r in resource_names if "::INSTR" in r]
    resource_name = "" if len(resource_names) == 0 else resource_names[0]
    return resource_name


def get_inst_found(resource_name):
    return True if resource_name != "" else False


def get_inst(resource_name):
    rm = pyvisa.ResourceManager()
    inst = rm.open_resource(resource_name)
    return inst


def record_band(inst, folder, filename, local_out_folder, sweep_dur=5):
    # RECORD
    inst.write(":INIT:REST")
    inst.write(":INIT:CONT ON")
    time.sleep(sweep_dur)
    inst.write(":INIT:CONT OFF")

    # SAVE
    csvPath = f"{folder}/{filename}.csv"
    pngPath = f"{folder}/{filename}.png"
    inst.write(f':MMEM:STOR:TRAC:DATA ALL, "{csvPath}"')
    inst.write(f':MMEM:STOR:SCR "{pngPath}"')

    save_file_to_local(inst, pngPath, local_out_folder)
    save_file_to_local(inst, csvPath, local_out_folder)
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


def record_bands(
    resource,
    site_name,
    last_run_index,
    folders,
    band_keys,
    sweep_dur,
    window,
):
    inst = get_inst(resource)
    bar_max = len(band_keys)
    pbar = window["-PROGRESS-"]
    pbar.update_bar(bar_max / 50, bar_max)
    for i, key in enumerate(band_keys):
        time.sleep(sweep_dur)
        pbar.update_bar(i + 1, bar_max)
        bannd_name = key
        run_index = i + 1 + last_run_index
        coupling = bands[key]["coupling"]

        state_filename = bands[key]["stateFilename"]
        corr_filename = bands[key]["corrFilename"]
        run_filename = get_run_filename(run_index, bannd_name, site_name)

        recall_state(inst, folders["stateFolder"], state_filename)
        recall_corr(inst, folders["corrFolder"], corr_filename)
        set_coupling(inst, coupling)

        out_folder = folders["outFolder"]
        local_out_folder = folders["localOutFolder"]
        record_band(
            inst,
            out_folder,
            run_filename,
            local_out_folder,
            sweep_dur,
        )
    time.sleep(1)
    pbar.update_bar(0, bar_max)


def write_txt_file(filename, text):
    with open(filename, "w") as f:
        f.write(text)
    return


def record_bands_debug(
    resource, site_name, last_run_index, folders, band_keys, sweep_dur, window
):
    print("")
    print("recordBands()")
    print("resource:", resource)
    print("site_name:", site_name)
    print("last_run_index:", last_run_index)
    print("folders:", folders)
    print("band_keys:", band_keys)
    print("sweep_dur:", sweep_dur)
    print("window:", window)
    # inst = getInst(resource)
    bar_max = len(band_keys)
    pbar = window["-PROGRESS-"]
    pbar.update_bar(bar_max / 50, bar_max)
    for i, key in enumerate(band_keys):
        time.sleep(sweep_dur)
        pbar.update_bar(i + 1, bar_max)
        band_name = key
        run_index = i + 1 + last_run_index
        run_filename = get_run_filename(run_index, band_name, site_name)

        local_out_folder = folders["localOutFolder"]
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        write_txt_file(
            f"{local_out_folder}/{run_filename}.txt",
            f"{timestamp} {run_filename}",
        )
    time.sleep(1)
    pbar.update_bar(0, bar_max)
