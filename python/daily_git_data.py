import sys
from helper import is_number as is_number
from datetime import datetime
from datetime import timedelta


def create_day_dict(date, files, time_spent, additions, deletions, commit_count):
    """Creates a dictionary from inputs"""
    daily_data = {}
    daily_data["date"] = date
    daily_data["files"] = files
    daily_data["time_spent"] = time_spent
    daily_data["additions"] = additions
    daily_data["deletions"] = deletions
    daily_data["commit_count"] = commit_count
    return daily_data


def select_best(all_files: list):
    """Selects 3 best files 
    
    Selects the best 3 files from **all_files** by maximizing the quantity ``(additions-deletions)`` for each file

    **Args**:
        **all_files**: list of dictionaries of the form: ::

            {
                'file_name': 'file name',
                'net_changes': additions-deletions
            }

    **Returns**: 
        **list**: top 3 files, or **all_files** if it contains fewer than 3 files

    """
    file_list = list(all_files.keys())
    file_changes = list(all_files.values())

    if len(file_list) < 3:
        return file_list
    top_files, progress = zip(
        *sorted(zip(file_list, file_changes), key=lambda k: k[1], reverse=True)
    )

    # eprint("Selected top files: {}".format(top_files))
    return top_files[:3]


def get_daily_commit_data(progress_file, max_change=None, timeout=None):
    """ Generates git commit statistics by day

    Uses the data in **progress_file** to generate git statistics by day

    **Args**:
        |  **progress_file** (file): The file pointer to a commit log file.
        |  **max_change** (int): The maximum additions or deletions for which a file 
        |      is counted.
        |  **timeout** (float): The amount of time between commits for which the 
        |      interval will still be added to the estimated time total.

    **Returns**:
        **dict**: A map of students to data, returned from create_day_dict
        

    """
    if not max_change:
        max_change = sys.maxsize
    else:
        max_change = int(max_change)
    if not timeout:
        timeout = 24
    timeout_interval = timedelta(hours=float(timeout))
    expect_time = False
    name = ""
    current_date = datetime(1, 1, 1).date()
    daily_time_spent = 0
    previous_time = datetime.strptime("00:00:00", "%H:%M:%S").time()
    daily_files = {}  # Top 3 files per commit
    daily_additions = 0
    daily_deletions = 0
    daily_commit_count = 0
    students = {}
    student_data = []
    for line in progress_file:
        # Clean line for parsing
        line = line.strip("\n").strip(" ")
        line = " ".join(line.split("\t"))

        words = line.split(" ")
        if words == [""]:
            expect_time = True
            continue
        if words[0] == "Start":  # Start of user
            student_data = []  # May hurt time tracking
            expect_time = True
            daily_time_spent = 0
            current_date = datetime(1, 1, 1).date()
            previous_time = datetime.strptime("00:00:00", "%H:%M:%S").time()
            daily_files = {}
            daily_additions = 0
            daily_deletions = 0
            daily_commit_count = 0
            name = words[1]
        elif words[0] == "End":  # End of user
            # Add the last day to student's data
            student_data.append(
                create_day_dict(
                    current_date,
                    select_best(daily_files),
                    daily_time_spent,
                    daily_additions,
                    daily_deletions,
                    daily_commit_count,
                )
            )

            # Set the student's data
            students[name] = student_data
        elif expect_time == True:  # New Data/Time/Code tuple
            expect_time = False
            if len(words) != 3:
                print("Expected date, time, and code. Found: {}".format(words))
            date = words[0]
            time = words[1]  # Unused
            code = words[2]  # Unused
            date = datetime.strptime(date, "%Y-%m-%d").date()
            time = datetime.strptime(time, "%H:%M:%S").time()
            if current_date == datetime(1, 1, 1).date():
                current_date = date
                previous_time = time
                daily_commit_count += 1
                continue
            datetime1 = datetime.combine(date, time)
            datetime2 = datetime.combine(current_date, previous_time)
            # print(datetime1, datetime2)
            time_delta = datetime1 - datetime2
            if date != current_date:
                # print("total seconds: {}".format(daily_time_spent))
                # print("New Date: {}".format(date))
                # Create dictionary of daily data
                student_data.append(
                    create_day_dict(
                        current_date,
                        select_best(daily_files),
                        daily_time_spent,
                        daily_additions,
                        daily_deletions,
                        daily_commit_count,
                    )
                )
                current_date = date
                previous_time = time
                daily_commit_count = 1
                daily_time_spent = 0
                daily_additions = 0
                daily_deletions = 0
                daily_files = {}
                continue
            # print(time_delta.total_seconds())
            if time_delta.total_seconds() < timeout_interval.total_seconds():
                daily_time_spent += time_delta.total_seconds()
            current_date = date
            previous_time = time
            daily_commit_count += 1
        else:  # New Addition/Deletion/File tuple
            if len(words) != 3:
                print("Unknown line format with words {}".format(words))
                continue
            additions = int(words[0]) if is_number(words[0]) else 0
            deletions = int(words[1]) if is_number(words[1]) else 0

            # Ignores files with more than max_changes lines changes
            if additions > max_change or deletions > max_change:
                continue

            file_path = words[2]  # Unused
            if file_path in daily_files:
                daily_files[file_path] += additions - deletions
            else:
                daily_files[file_path] = additions - deletions
            daily_additions += additions
            daily_deletions += deletions
    return students
