import sys
import json
import copy
import argparse
from datetime import datetime
from helper import time_string
from helper import eprint
from daily_git_data import get_daily_commit_data as get_progress


def date_string(date):
    """Converts datetime date object into the api's string format"""
    return date.isoformat()


def jsonify(git_data):
    """ Converts git log data json formatted for the /commitList endpoint

    Description
    
    **Args**:
        **git_data** (dict): A dictionary containing the git commit list: ::
            
            {
                "name1": [
                    {
                        "date": datetime,
                        "time_spent": int (seconds),
                        "files": ["file1",...],
                    },
                    ...
                ],
                ...
            }

    **Returns**:
        dict: A dictionary identical to **git_data**, except all "date" and "time_spent"
        properties are converted to human readable strings

    """
    # Create complete copy. Copy module may be removed in the future
    data = copy.deepcopy(git_data)
    for student in data:
        student_data = data[student]
        for day in student_data:
            day["date"] = date_string(day["date"])
            day["time_spent"] = time_string(day["time_spent"])
    eprint(data)
    return json.dumps(data)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("logfile", help="path to commit log file")
    parser.add_argument("name", help="user name")

    args = parser.parse_args()

    student_id = args.name
    commit_data_file = open(args.logfile, "r")
    data = get_progress(commit_data_file)

    api_json = jsonify(data)[student_id]
    print(api_json)
