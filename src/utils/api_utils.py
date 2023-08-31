import pandas as pd

from io import BytesIO
from garminconnect import Garmin

from .data_utils import process_activities_data

from customtkinter import CTk, CTkProgressBar, CTkLabel


def init_api(email: str, password: str) -> Garmin:
    """
    Initialize and log in to the Garmin API with the provided credentials.

    Args:
        email (str): The email address associated with the Garmin account.
        password (str): The password associated with the Garmin account.

    Returns:
        Garmin: An authenticated Garmin API instance.
    """

    api = Garmin(email, password)
    api.login()

    return api


def get_activities(
    api: Garmin,
    startdate: str,
    enddate: str,
    progressbar: CTkProgressBar,
    progresstext: CTkLabel,
    root: CTk,
    activitytype: str = "",
) -> pd.DataFrame:
    """
    Get activities data from the Garmin API within a specified date range.

    Args:
        api (Garmin): Authenticated API session to the Garmin service.
        startdate (str): Start date in the format 'YYYY-MM-DD' from which
            activities are fetched.
        enddate (str): End date in the format 'YYYY-MM-DD' until which
            activities are fetched.
        progressbar (CTkProgressBar): A progress bar widget to display
            the progress of activities retrieval.
        progresstext (CTkLabel): A label widget to display the progress
            status text.
        root (CTk): The main tkinter window or top-level window that
            contains the widgets.
        activitytype (str, optional): Type of activity to filter. Acceptable
            values include: 'cycling', 'running', 'swimming', 'multi_sport',
            'fitness_equipment', 'hiking', 'walking', and 'other'. Defaults to
            an empty string, implying all activity types are fetched.

    Returns:
        pd.DataFrame: A DataFrame containing the activities data.
    """

    activities = api.get_activities_by_date(startdate, enddate, activitytype)

    activities_data = pd.DataFrame()

    iter_count = 1
    progressbar.set(0)

    # Download activities
    for activity in activities:
        activity_id = activity["activityId"]

        csv_data = api.download_activity(
            activity_id, dl_fmt=api.ActivityDownloadFormat.CSV
        )
        activity_data = pd.read_csv(BytesIO(csv_data)).tail(1)

        activity_data["Type d'activité"] = activity["activityType"]["typeKey"]
        activity_data["Date"] = activity["startTimeLocal"]
        activity_data["Favori"] = str(activity["favorite"]).upper()
        activity_data["Titre"] = activity["activityName"]

        activities_data = pd.concat([activities_data, activity_data])

        # Update progress bar
        message = "Téléchargement des activités en cours ... "
        display_text = message + f"{iter_count}/{len(activities)}"
        progresstext.configure(text=display_text)
        progressbar.set(progressbar.get() + 1 / len(activities))
        root.update_idletasks()
        iter_count += 1

    display_text = f"Téléchargement de {len(activities)} activité(s) terminé !"
    progresstext.configure(text=display_text)

    # Process the data
    activities_data = process_activities_data(activities_data)

    return activities_data
