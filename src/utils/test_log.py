import glob
import os

from utils.settings import read_settings_from_file


def get_latest_test_log():
    local_out_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

    # return last updated file, if nothing return "No test logs found."
    if not local_out_folder or not os.path.isdir(local_out_folder):
        return "No test logs found."

    # get all ".csv" files
    csv_files = glob.glob(os.path.join(local_out_folder, "*.csv"))

    if not csv_files:
        return "No test logs found."

    # Sort by modification time, descending
    latest_path = max(csv_files, key=os.path.getmtime)
    latest_file = os.path.basename(latest_path)

    return latest_file
