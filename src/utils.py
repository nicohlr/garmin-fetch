import sys
import os
import pandas as pd

from io import BytesIO
from garminconnect import Garmin


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    api = Garmin(email, password)
    api.login()

    return api


def get_activities(
    api, startdate, enddate, progressbar, progresstext, root, activitytype=""
):
    """Get activities data from startdate 'YYYY-MM-DD' to enddate 'YYYY-MM-DD',

    Args:
        api (Garmin): API request session.
        startdate (str): Startdate 'YYYY-MM-DD' formatted.
        enddate (str): Enddate 'YYYY-MM-DD' formatted.
        dest_folder (str): Where to dump activities data.
        activitytype (str): Types of activities to filter. Possible values
            are: cycling, running, swimming, multi_sport, fitness_equipment,
            hiking, walking, other. Default to "".
    """

    # today.isoformat()
    activities = api.get_activities_by_date(startdate, enddate, activitytype)

    output_file = f"activities_{startdate}_to_{enddate}"

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

    columns_order = [
        "Type d'activité",
        "Date",
        "Favori",
        "Titre",
        "Intervalle",
        "Distance",
        "Heure",
        "Temps de déplacement",
        "Fréquence cardiaque moy.",
        "Fréquence cardiaque maximale",
        "Allure moyenne",
        "Allure moyenne en déplacement",
        "Meilleure allure",
        "Cadence de course moyenne",
        "Cadence de course maximale",
        "Longueur moyenne des foulées",
        "Température moyenne",
        "Calories",
        "Gain d'altitude",
        "Perte d'altitude",
    ]

    present_columns = [
        col for col in columns_order if col in activities_data.columns
    ]

    additional_columns = [
        col for col in activities_data.columns if col not in present_columns
    ]
    present_columns.extend(additional_columns)

    activities_data = (
        activities_data[present_columns]
        .drop(["Intervalle", "Heure"], axis=1)
        .reset_index(drop=True)
    )

    if getattr(sys, "frozen", False):
        # we are running in a bundle
        bundle_dir = os.path.dirname(sys.executable)
    else:
        # we are running in a normal Python environment
        bundle_dir = os.path.dirname(os.path.abspath(__file__))

    dump_path = os.path.join(bundle_dir, f"{output_file}.xlsx")

    activities_data.to_excel(dump_path, index=False)

    return dump_path
