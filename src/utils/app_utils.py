import threading

from utils.base_utils import days_in_month
from utils.api_utils import init_api, get_activities
from utils.base_utils import save_settings, save_to_excel
from utils.constants import (
    ACTIVITY_TYPES_MAPPING,
    DATE_ERROR,
    LOGIN_ERROR,
    WRONG_EMAIL_ERROR,
    MISSING_EMAIL_ERROR,
    MISSING_PASSWORD_ERROR,
    TOO_MANY_REQUESTS_ERROR,
    SUCCESS_MSG,
    CONNECTION_LOADING_MSG,
)

from datetime import datetime
from tkinter import messagebox
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)


def reset_interface(widgets):
    widgets["progress"].grid_forget()
    widgets["progress_text"].grid_forget()
    widgets["submit_button"].grid_configure(pady=(20, 60))
    widgets["error_message"].grid(sticky="ew", row=1, column=0, columnspan=3)


def update_days_combobox(root, combobox_day, combobox_month, combobox_year):
    """Update the number of days in a combobox based on the month and year."""
    month = int(combobox_month.get())
    year = int(combobox_year.get())
    current_day = int(combobox_day.get())

    max_day = days_in_month(month, year)

    combobox_day["values"] = [str(i).zfill(2) for i in range(1, max_day + 1)]
    if current_day > max_day:
        combobox_day.set(str(max_day).zfill(2))
    root.update_idletasks()


def init_api_and_followup(
    root, email, password, startdate, enddate, activity_type, widgets
):
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


def post_init(root, error, api, startdate, enddate, activity_type, widgets):
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

    activities_data = get_activities(
        api=api,
        startdate=startdate,
        enddate=enddate,
        progressbar=widgets["progress"],
        progresstext=widgets["progress_text"],
        root=root,
        activitytype=activity_type,
    )

    dump_path = save_to_excel(activities_data, startdate, enddate)

    messagebox.showinfo("Succès", SUCCESS_MSG + dump_path)


def submit(root, widgets):
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
        sticky="ew", row=13, column=0, columnspan=3, pady=(10, 0)
    )
    widgets["progress"].grid(
        sticky="ew", row=14, column=0, columnspan=3, pady=(0, 50), padx=40
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
