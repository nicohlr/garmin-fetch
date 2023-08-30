import os
import sys
import pathlib


def days_in_month(month, year):
    """Return the number of days in a given month and year."""
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            return 29
        return 28
    else:
        raise ValueError("Invalid month")


def save_settings(email, start_date, activity_type):
    path = os.path.join(pathlib.Path.home(), "settings-garmin-download.txt")
    with open(path, "w") as f:
        f.write(email + "\n")
        f.write(start_date + "\n")
        f.write(activity_type)


def load_settings():
    try:
        path = os.path.join(
            pathlib.Path.home(), "settings-garmin-download.txt"
        )
        with open(path, "r") as f:
            lines = f.readlines()
            email = lines[0].strip()
            start_date = lines[1].strip() if len(lines) > 1 else None
            activity_type = lines[2].strip() if len(lines) > 2 else None
            return email, start_date, activity_type
    except FileNotFoundError:
        return None, None, None


def save_to_excel(data, startdate, enddate):
    """Save a DataFrame to an Excel file.

    Args:
        data (DataFrame): DataFrame containing activities data.
        startdate (str): Startdate 'YYYY-MM-DD' formatted.
        enddate (str): Enddate 'YYYY-MM-DD' formatted.

    Returns:
        str: Path to the saved file.
    """

    output_file = f"activities_{startdate}_to_{enddate}"

    if getattr(sys, "frozen", False):
        # we are running in a bundle
        bundle_dir = os.path.dirname(sys.executable)
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    dump_path = os.path.join(bundle_dir, f"{output_file}.xlsx")

    data.to_excel(dump_path, index=False)

    return dump_path
