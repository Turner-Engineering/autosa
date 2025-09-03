import csv
import glob
import os

from utils.settings import read_settings_from_file


def get_latest_test_log():
    local_out_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

    # get all ".csv" files
    csv_files = glob.glob(os.path.join(local_out_folder, "*.csv"))

    if not csv_files:
        return None, None

    # Sort by modification time, descending
    latest_path = max(csv_files, key=os.path.getmtime)
    latest_file = os.path.basename(latest_path)

    return latest_path, latest_file


def get_test_log_project():
    log_path, log_filename = get_latest_test_log()

    if log_path is None or log_filename is None:
        return "No test logs found."  # launch window to autocreate

    with open(log_path, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:  # edge case of empty rows
                continue

            proj_info = row[0].strip()
            if proj_info.startswith("Project Name:"):
                _, value = proj_info.split(":")
                value = value.strip()
                return "No project name." if "None" or value == "" else value
