import sys
import json
import copy
import argparse
from datetime import datetime
from helper import time_string
from helper import daterange
from helper import date_string
from helper import eprint
from daily_git_data import get_daily_commit_data as get_progress
from start_end import commit_data


def extract_changes(commit_data):
    """Extracts additions and deletions from commit data

    **Args**:
        **commit_data** (dict): A list of dictionaries containing commit data,
        each with the following form: ::

            {
                "date": datetime,
                "additions": int,
                "deletions": int
            }

    **Returns**:
        dict: A dictionary that maps dates to additions and deletions
        with the following form: ::

            {
                "date1": {
                    "additions": int,
                    "deletions": int
                }
                ...
            }

    """
    new_data = {}
    for info in commit_data:
        new_entry = {}
        new_entry["additions"] = info["additions"]
        new_entry["deletions"] = info["deletions"]
        date = date_string(info["date"])
        new_data[date] = new_entry
    return new_data


def jsonify(commit_data, times):
    """Convert data to json for /progress endpoint

    Converts the data to a list of dictionaries. One dictionary is
    created per day. A dictionary is also created for each day in between
    the first and last date, even if there is no data for that date. In that case,
    progress for that day are set to the same value as the previous day.
    
    **Args**:
        **commit_data** (dict): A dictionary containing the git commit list: ::
            
            {
                "date1": {
                    "additions": datetime,
                    "deletions": int (seconds),
                },
                ...
            }

        **times** (str, str): A tuple of start and end dates of the form "mm-dd-yyyy"

    **Returns**:
        json: A json list of entries, one per day, of the following form: ::

            {
                "date": "mm-dd-yyyy",
                "progress": int,
            }

    """
    daily_data = []
    # Create date range using times file
    date1 = datetime.strptime(times[0], "%Y-%m-%d").date()
    date2 = datetime.strptime(times[1], "%Y-%m-%d").date()
    dates = daterange(date1, date2)
    progress = 0

    # Fill each date with comulative progress
    for day in dates:
        day = date_string(day)
        new_entry = {}
        new_entry["date"] = day
        if day in commit_data:
            progress += commit_data[day]["additions"] - commit_data[day]["deletions"]
        new_entry["progress"] = progress
        daily_data.append(new_entry)

    # Convert progress to a percentage by divding by the final total
    for item in daily_data:
        item["progress"] = round(item["progress"] / progress * 100)
    return daily_data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="path to commit log file")
    parser.add_argument("timefile", help="path to commit time file")
    parser.add_argument("name", help="user name")
    parser.add_argument("-O", "--obfuscate", action="store_true", help="obfuscate flag")

    args = parser.parse_args()

    commit_data_file = open(args.logfile, "r")
    commit_times_file = open(args.timefile, "r")
    student_id = args.name

    data = get_progress(commit_data_file)
    individual_data = data[student_id]
    # print("\n")
    reformatted_data = extract_changes(individual_data)

    commit_times = commit_data(commit_times_file)
    individual_commit_times = commit_times[student_id]

    api_formatted_data = jsonify(reformatted_data, individual_commit_times)
    api_json = json.dumps(api_formatted_data)
    print(api_json)
