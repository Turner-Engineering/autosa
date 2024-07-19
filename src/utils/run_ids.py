import datetime
import re


def run_index_to_id(run_index):
    run_number = "%02d" % run_index  # TODO confirm will work with 100s of runs
    d = datetime.datetime.now()
    month = str(int(d.strftime("%m")))
    date = d.strftime("%d")  # TODO make this shorter like medhashree's code
    run_id = f"{month}{date}-{run_number}"
    return run_id


def filenames_to_run_ids(filenames):
    # Look for 3 to 4 digits followed by a dash followed by 1 to 3 digits
    regex = r"\d{3,4}-\d{1,3}"
    matches = [re.search(regex, file) for file in filenames]

    # Filter out None and extract matched strings
    run_ids = [match.group() for match in matches if match]
    return run_ids


def get_todays_run_ids(filenames):
    run_ids = filenames_to_run_ids(filenames)

    # Get today's date as an integer without zero-padding for the month
    today_date_int = int(datetime.datetime.now().strftime("%m%d"))
    today_run_ids = []

    for run_id in run_ids:
        run_date_int = int(run_id.split("-")[0])
        if run_date_int == today_date_int:
            today_run_ids.append(run_id)
    return today_run_ids
