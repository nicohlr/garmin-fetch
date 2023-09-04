import threading

from garminconnect import Garmin

from typing import Union, Optional

from utils.base_utils import days_in_month
from utils.api_utils import init_api, get_activities
from utils.base_utils import save_settings, save_to_excel, save_gpx_files
from utils.constants import (
    ACTIVITY_TYPES_MAPPING,
    DATE_ERROR,
    LOGIN_ERROR,
    WRONG_EMAIL_ERROR,
    MISSING_EMAIL_ERROR,
    MISSING_PASSWORD_ERROR,
    TOO_MANY_REQUESTS_ERROR,
    SUCCESS_MSG,
    SUCCESS_MSG_GPX,
    CONNECTION_LOADING_MSG,
)

from customtkinter import CTk, CTkComboBox

from datetime import datetime, date
from tkinter import messagebox
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)


def reset_interface(widgets):
    """Reset some widgets to the state when progress bar is not displayed.

    Args:
        widgets (dict): A dictionary containing all the customtkinter widgets
            of the app.
    """
    widgets["progress"].grid_forget()
    widgets["progress_text"].grid_forget()
    widgets["submit_button"].grid_configure(pady=(20, 60))
    widgets["error_message"].grid(sticky="ew", row=1, column=0, columnspan=3)


def update_days_combobox(
    root: CTk,
    combobox_day: CTkComboBox,
    combobox_month: CTkComboBox,
    combobox_year: CTkComboBox,
) -> None:
    """
    Update the number of days available in the day combobox based on the
    selected month and year.

    When a user changes the month or year, the number of days in that month
    might differ. This function adjusts the available days in the
    'combobox_day' dropdown to fit the valid days for the selected month and
    year. If the previously selected day exceeds the valid day range, it
    resets to the maximum valid day.

    Args:
        root (CTk): The main customtkinter window or top-level window where the
            comboboxes are placed.
        combobox_day (CTkComboBox): The combobox representing the day of
            the date.
        combobox_month (CTkComboBox): The combobox representing the month
            of the date.
        combobox_year (CTkComboBox): The combobox representing the year of
            the date.
    """
    month = int(combobox_month.get())
    year = int(combobox_year.get())
    current_day = int(combobox_day.get())

    max_day = days_in_month(month, year)

    combobox_day["values"] = [str(i).zfill(2) for i in range(1, max_day + 1)]
    if current_day > max_day:
        combobox_day.set(str(max_day).zfill(2))
    root.update_idletasks()


def init_api_and_followup(
    root: CTk,
    email: str,
    password: str,
    startdate: Union[date, str],
    enddate: Union[date, str],
    activity_type: str,
    widgets: dict,
) -> None:
    """
    Initialize the API using provided credentials and setup follow-up tasks.

    This function attempts to initialize an API instance with the given email
    and password. If the initialization is successful, a follow-up task
    (`post_init`) is set up with the provided arguments. If there's an error
    in initializing the API, the error is passed to the follow-up task.

    Args:
        root (CTk): The main customtkinter window or top-level
            window.
        email (str): The email address to be used for API authentication.
        password (str): The password corresponding to the email for API
            authentication.
        startdate (datetime.date or str): The starting date for activity
            retrieval.
        enddate (datetime.date or str): The end date for activity retrieval.
        activity_type (str): The type of activity to be retrieved (e.g.,
            'running', 'cycling').
        widgets (dict): A dictionary containing all the customtkinter widgets
            of the app.
    """
    try:
        api = init_api(email=email, password=password)
        error = None
    except Exception as e:
        api = None
        error = e

    root.after(
        0,
        post_init,
        root,
        error,
        api,
        startdate,
        enddate,
        activity_type,
        widgets,
    )


def post_init(
    root: CTk,
    error: Optional[Exception],
    api: Garmin,
    startdate: Union[date, str],
    enddate: Union[date, str],
    activity_type: str,
    widgets: dict,
) -> None:
    """
    Handle post-initialization tasks after attempting API connection.

    Once API initialization has been attempted, this function manages the UI
    updates and potential errors. If there is no error and the API
    initialization is successful, it retrieves activities and saves them to an
    Excel file.

    Args:
        root (CTk): The main customtkinter window or top-level
            window.
        error (Optional[Exception]): Any error that occurred during API
            initialization.
        api (Garmin): The initialized API instance.
        startdate (datetime.date or str): The starting date for activity
            retrieval.
        enddate (datetime.date or str): The end date for activity retrieval.
        activity_type (str): The type of activity to be retrieved (e.g.,
            'running', 'cycling').
        widgets (dict): A dictionary containing all the customtkinter widgets
            of the app.
    """
    widgets["progress"].stop()
    widgets["progress"]["mode"] = "determinate"
    widgets["progress_text"].configure(text="")

    if error:
        if isinstance(error, GarminConnectAuthenticationError):
            widgets["error_message"].configure(text=LOGIN_ERROR)
        elif isinstance(error, GarminConnectTooManyRequestsError):
            widgets["error_message"].configure(text=TOO_MANY_REQUESTS_ERROR)
        else:
            widgets["error_message"].configure(
                text=f"Erreur inattendue: {str(error)}"
            )
        widgets["progress"].grid_forget()
        widgets["progress_text"].grid_forget()
        widgets["submit_button"].grid_configure(pady=(20, 60))
        widgets["error_message"].grid(
            sticky="ew", row=1, column=0, columnspan=3
        )
        return

    include_gpx = dict(Oui=True, Non=False).get(widgets["switch_gpx"].get())

    activities_data, gpx_data = get_activities(
        api=api,
        startdate=startdate,
        enddate=enddate,
        progressbar=widgets["progress"],
        progresstext=widgets["progress_text"],
        root=root,
        activitytype=activity_type,
        include_gpx=include_gpx,
    )

    dump_path = save_to_excel(activities_data, startdate, enddate)
    dump_path_gpx = save_gpx_files(gpx_data)

    if not include_gpx:
        messagebox.showinfo("Succès", SUCCESS_MSG + dump_path)
    else:
        messagebox.showinfo(
            "Succès", SUCCESS_MSG + dump_path + SUCCESS_MSG_GPX + dump_path_gpx
        )


def submit(root: CTk, widgets: dict) -> None:
    """
    Initiates the API call based on provided widget inputs and updates the GUI.

    This function first validates the input data, including checking email
    format, password presence, and date validity. If the inputs are valid, it
    initiates a separate thread to call the API without blocking the GUI. The
    progress and potential errors are reflected in the provided widgets.

    Args:
        root (CTk): The main customtkinter window or top-level
            window.
        widgets (dict): A dictionary containing all the customtkinter widgets
            of the app.
    """
    email = widgets["email_entry"].get()
    password = widgets["password_entry"].get()
    startdate = (
        widgets["start_year"].get()
        + "-"
        + widgets["start_month"].get()
        + "-"
        + widgets["start_day"].get()
    )
    enddate = (
        widgets["end_year"].get()
        + "-"
        + widgets["end_month"].get()
        + "-"
        + widgets["end_day"].get()
    )
    selected_activity = widgets["activity_type_combobox"].get()
    activity_type = ACTIVITY_TYPES_MAPPING[selected_activity]

    # Check if password is empty
    if not email:
        widgets["error_message"].configure(text=MISSING_EMAIL_ERROR)

        return

    # Check email validity
    if not email or "@" not in email:
        widgets["error_message"].configure(text=WRONG_EMAIL_ERROR)
        reset_interface(widgets)
        return

    # Check if password is empty
    if not password:
        widgets["error_message"].configure(text=MISSING_PASSWORD_ERROR)
        reset_interface(widgets)
        return

    # Convert the start and end dates to datetime objects for comparison
    start_datetime = datetime.strptime(startdate, "%Y-%m-%d")
    end_datetime = datetime.strptime(enddate, "%Y-%m-%d")

    # Check if start date is after end date
    if start_datetime > end_datetime:
        widgets["error_message"].configure(text=DATE_ERROR)
        reset_interface(widgets)
        return

    widgets["error_message"].grid_forget()

    widgets["progress_text"].configure(text=CONNECTION_LOADING_MSG)
    widgets["progress"]["mode"] = "indeterminate"
    widgets["progress_text"].grid(
        sticky="ew", row=14, column=0, columnspan=3, pady=(10, 0)
    )
    widgets["progress"].grid(
        sticky="ew", row=15, column=0, columnspan=3, pady=(0, 50), padx=40
    )
    widgets["submit_button"].grid_configure(pady=(30, 10))

    widgets["progress"].start()
    root.update_idletasks()

    # Use threading to run the lengthy function without blocking the GUI
    thread = threading.Thread(
        target=init_api_and_followup,
        args=(
            root,
            email,
            password,
            startdate,
            enddate,
            activity_type,
            widgets,
        ),
    )
    thread.start()

    # If the request is successful, save settings for next request
    save_settings(email, startdate, selected_activity)
