import sys
import json
import copy
import argparse
from datetime import datetime
from helper import date_string
from helper import daterange
from helper import eprint
from daily_git_data import get_daily_commit_data as commit_list


def jsonify(commit_data):
    """ Converts git log data json formatted for the /commitList endpoint

    Uses git log information to create a list of entries containing the date
    and commit count. Note that this function uses the data of a single student.
    
    **Args**:
        **git_data** (dict): A dictionary containing the git commit list: ::
            
            {
                "name1": [
                    {
                        "date": datetime,
                        "commit_count": int,
                    },
                    ...
                ],
                ...
            }

    **Returns**:
        json: A json list with entries of the following format: ::
            
            {
                "date": "mm-dd-yyyy",
                "count": int
            }

    """
    new_data = []
    date1 = commit_data[0]["date"]
    date2 = commit_data[len(commit_data) - 1]["date"]
    dates = daterange(date1, date2)

    # Create a list of dictionaries for each date between the first and last
    for date in dates:
        new_bar = {"date": date_string(date), "count": 0}
        new_data.append(new_bar)

    # Replace the counts for each date with actual data
    for entry in commit_data:
        date = date_string(entry["date"])
        count = entry["commit_count"]
        for e in new_data:
            if e["date"] == date:
                e["count"] = count
                break
    return json.dumps(new_data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="path to commit log file")
    parser.add_argument("name", help="user name")
    parser.add_argument("-O", "--obfuscate", action="store_true", help="obfuscate flag")

    args = parser.parse_args()

    commit_data_file = open(args.logfile, "r")
    student_id = args.name

    data = commit_list(commit_data_file)[student_id]

    formatted_data = jsonify(data)
    print(formatted_data)
