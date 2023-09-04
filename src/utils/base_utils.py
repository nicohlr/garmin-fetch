import os
import sys
import pathlib


def days_in_month(month: int, year: int) -> int:
    """
    Return the number of days in the specified month and year.

    Args:
        month (int): The month (1-12).
        year (int): The year in YYYY format.

    Returns:
        int: The number of days in the given month and year.

    Raises:
        ValueError: If the provided month is not within 1-12 range.
    """
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


def save_settings(email: str, start_date: str, activity_type: str) -> None:
    """
    Save the settings to a file in the user's home directory.

    Args:
        email (str): The email address.
        start_date (str): The start date in the 'YYYY-MM-DD' format.
        activity_type (str): The type of activity.
    """
    path = os.path.join(pathlib.Path.home(), "settings-garmin-download.txt")
    with open(path, "w") as f:
        f.write(email + "\n")
        f.write(start_date + "\n")
        f.write(activity_type)


def load_settings() -> tuple:
    """
    Load the settings from a file in the user's home directory.

    Returns:
        tuple: A tuple containing email (str), start_date (str or None),
        and activity_type (str or None). If the file does not exist, all
        values in the tuple are None.
    """
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


def save_gpx_files(gpx_data: dict) -> str:
    """
    Save GPX byte data to .gpx files in the 'gpx_data' folder.

    This function determines the running environment (bundled application
    or normal Python environment) and sets the save path accordingly. Each
    GPX entry in the dictionary is saved as a separate file named by its
    activity ID.

    Args:
        gpx_data (dict): A dictionary with activity IDs as keys and GPX byte
            data as values.

    Returns:
        str: The path to the 'gpx_data' folder where the files were saved.
    """
    output_folder = "gpx_data"

    if getattr(sys, "frozen", False):
        # we are running in a bundle
        bundle_dir = os.path.dirname(sys.executable)
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    for activity_id, byte_data in gpx_data:
        dump_path = os.path.join(
            bundle_dir, output_folder, f"{activity_id}.gpx"
        )
        with open(dump_path, "wb") as file:
            file.write(byte_data)

    return os.path.join(bundle_dir, output_folder)
