import csv
import glob
import os

from utils.logger import autosa_logger
from utils.settings import read_settings_from_file


def get_test_logs():
    local_out_folder = read_settings_from_file()["-LOCAL OUT FOLDER-"]

    # get all ".csv" files
    csv_files = glob.glob(os.path.join(local_out_folder, "*.csv"))

    if not csv_files:
        return None

    return csv_files


def get_project_name(filepath):
    if filepath is None:
        autosa_logger.warning("No test log path provided.")
        return

    if not os.path.exists(filepath):
        autosa_logger.warning(f"Test log path {filepath} does not exist.")
        return

    with open(filepath, "r") as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if not row:  # edge case of empty rows
                continue

            proj_info = row[0].strip()
            if proj_info.startswith("Project Name:"):
                _, value = proj_info.split(":", 1)
                value = value.strip()
                if value.lower() == "none" or value == "":
                    autosa_logger.info(
                        f"No project name found in test log {
                            os.path.basename(filepath)
                        }."
                    )
                    return os.path.basename(filepath)
                else:
                    return value

    return os.path.basename(filepath)
