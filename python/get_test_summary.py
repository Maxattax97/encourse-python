import sys
import json
import copy
import argparse
from datetime import datetime
from helper import time_string
from helper import daterange
from helper import date_string
from helper import eprint
from test_completion import get_test_completion as get_test_scores
from start_end import commit_data


def jsonify(test_data, hidden):
    """Counts the number of students who have passed each test case
   
    Sums up the total number of students who have passed each particular test case, and
    stores that information with the test case name. If the test case is hidden, "H" is
    appended to the end of the test case name

    **Args**:
        **data** (dict): A dictionary of users mapped to their respective test scores
        The dictionary has the following format: ::

            {
                "name1": {
                   "tests": {
                        "Test1": ("P" or "F"),
                        ...
                   },
                   "total": int (percentage)
                },
                ...
            }
        
        **hidden** (bool): A boolean that is true if the test cases are hidden

    **Returns**:
        json: A json array containing the percentage of students who passed each test.
        The json has the form: ::
            
            [
                {
                    "name": str,
                    "hidden": bool,
                    "score": int (percentage)
                },
                ...
            ]
    
    """
    tests = {}
    test_totals = {}
    # Collect scores for each test
    for student in test_data:
        info = test_data[student]
        test_scores = info["tests"]
        for test_name in test_scores:
            if test_scores[test_name] == "P":
                if test_name in tests:
                    tests[test_name] += 1
                    test_totals[test_name] += 1
                else:
                    tests[test_name] = 1
                    test_totals[test_name] = 1
            else:
                if test_name in tests:
                    test_totals[test_name] += 1
                else:
                    tests[test_name] = 0
                    test_totals[test_name] = 1
    test_list = []
    # Reformat into api format
    for test_name in tests:
        test_score = tests[test_name]
        test_total = test_totals[test_name]
        new_bar = {}
        new_bar["name"] = test_name + " H" if hidden else test_name
        new_bar["hidden"] = hidden
        new_bar["score"] = int(test_score * 100 / test_total)
        test_list.append(new_bar)
    return json.dumps(test_list)


def merge_data(visible, hidden):
    """Combines the visible and hidden test cases into a single json"""
    visible = list(json.loads(visible))
    hidden = list(json.loads(hidden))
    visible.append(hidden)
    return json.dumps(visible)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("visible", help="path to visible test score file")
    parser.add_argument("hidden", help="path to hidden test score file")
    parser.add_argument("-O", "--obfuscate", action="store_true", help="obfuscate flag")

    args = parser.parse_args()

    visible_test_score_file = open(args.visible, "r")
    hidden_test_score_file = open(args.hidden, "r")

    visible_data = get_test_scores(visible_test_score_file)
    hidden_data = get_test_scores(hidden_test_score_file)

    formatted_visible = jsonify(visible_data, False)
    formatted_hidden = jsonify(hidden_data, True)
    api_json = merge_data(formatted_visible, formatted_hidden)
    print(api_json)
