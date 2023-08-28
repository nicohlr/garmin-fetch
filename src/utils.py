import pandas as pd

from tqdm import tqdm
from io import BytesIO
from garminconnect import Garmin


def init_api(email, password):
    """Initialize Garmin API with your credentials."""

    api = Garmin(email, password)
    api.login()

    return api


def get_activities(api, startdate, enddate, activitytype=""):
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

    # Download activities
    for activity in tqdm(activities):

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

    activities_data = (
        activities_data[columns_order]
        .drop(["Intervalle", "Heure"], axis=1)
        .reset_index(drop=True)
    )

    activities_data.to_excel(f"./{output_file}.xlsx", index=False)
