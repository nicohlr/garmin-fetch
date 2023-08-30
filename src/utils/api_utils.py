import pandas as pd

from io import BytesIO
from garminconnect import Garmin

from .data_utils import process_activities_data


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    api = Garmin(email, password)
    api.login()

    return api


def get_activities(
    api, startdate, enddate, progressbar, progresstext, root, activitytype=""
):
    """Get activities data from startdate 'YYYY-MM-DD' to enddate 'YYYY-MM-DD'.

    Args:
        api (Garmin): API request session.
        startdate (str): Startdate 'YYYY-MM-DD' formatted.
        enddate (str): Enddate 'YYYY-MM-DD' formatted.
        activitytype (str): Types of activities to filter. Possible values
            are: cycling, running, swimming, multi_sport, fitness_equipment,
            hiking, walking, other. Default to "".
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
