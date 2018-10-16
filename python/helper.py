from __future__ import print_function
from datetime import date, timedelta
import sys


def is_number(string):
    """Returns true if a string can be converted to an int, false otherwise"""
    try:
        int(string)
        return True
    except ValueError:
        return False


def date_string(date):
    """Converts a datetime object into the api's standard date format"""
    return date.isoformat()


def time_string(seconds):
    """Converts a datetime object to a concise string
    
    **Args**
        **seconds** (int): The number of seconds that a student has worked on a project

    **Returns**:
        str: Returns a string representing a (rounded) time, using the following rules:

        |  - "None" if the number of seconds < 60
        |  - "X minutes" if the number of minutes if greater than 1
        |  - "X hours" if the number of hours is greater than 0

    """

    if seconds < 60:
        return "None"
    minutes, seconds = divmod(seconds, 60)
    if minutes < 60:
        return "{} minutes".format(int(minutes))
    hours, minutes = divmod(minutes, 60)
    return "{} hours".format(int(hours))


def daterange(start, end):
    """Returns a list of every date between **start** and **end**
        
    **Args**:
        |  **start** (date): A datetime date object, representing the start of the range
        |  of dates to be returned        
        |  **end** (date): A datetime date object, representing the end of the range
        |  of dates to be returned

    **Returns**
        list: A list of datetime date objects representing every date between start
        and end (inclusive)

    """
    for n in range(int((end - start).days)):
        yield start + timedelta(n)


def eprint(*args, **kwargs):
    """A duplicate of the python print method that instead prints to standard error"""
    print(*args, file=sys.stderr, **kwargs)
