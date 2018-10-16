import json


def commit_counts(count_file):
    """Creates a mapping from users to commit counts

    Args:
        count_file (file): A file which contains the commit count associated with each user

    Returns:
        dict: A dictionary of mappings from student to commit counts::

            {
                "student1": int,
                "student2": int,
                ...
            }

    """
    counts = {}
    line = count_file.readline()
    line = line.strip("\n").strip(" ")
    while line != "":
        words = line.split(" ")
        if len(words) == 2:
            user = words[0]
            count = words[1]
            if user in counts:
                print(
                    "Multiple counts for user {}: ({}, {})".format(
                        user, user[counts], count
                    )
                )
            counts[user] = count

        line = count_file.readline()
        line = line.strip("\n").strip(" ")
    return counts
