import logging
import pandas as pd

from io import BytesIO
from itertools import zip_longest
from garminconnect import Garmin

from .data_utils import process_activities_data
from .constants import ACTIVITY_DATA_MAPPING, AMS_ERROR, DWF_ERROR, DWR_ERROR

from customtkinter import CTk, CTkProgressBar, CTkLabel


logging.basicConfig(
    level="INFO",
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


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
    # Initialize progress bar
    iter_count = 1
    message = "Initialisation du téléchargement des activités ... "
    progresstext.configure(text=message)
    progressbar.set(0)
    root.update_idletasks()

    # Download activities default data
    activities = api.get_activities_by_date(startdate, enddate, activitytype)

    # Format activities default data
    activities_data = pd.DataFrame(activities)
    activities_data = activities_data[ACTIVITY_DATA_MAPPING.keys()]
    activities_data = activities_data.rename(columns=ACTIVITY_DATA_MAPPING)

    # Add missing data
    ams_list, dwf_list, dwr_list = ([], [], [])
    ams_top, dwf_top, dwr_top = (False, False, False)
    hrz_data_list = []

    for activity in activities:
        activity_id = activity["activityId"]

        details_data = api.get_activity_evaluation(activity_id)

        hrz_data = api.get_activity_hr_in_timezones(activity_id)
        hrz_data_list.append(hrz_data)

        try:
            ams_list.append(details_data["summaryDTO"]["averageMovingSpeed"])
        except KeyError:
            ams_list.append("")
            logging.info(AMS_ERROR + f"{activity_id}")
        try:
            dwf_list.append(details_data["summaryDTO"]["directWorkoutFeel"])
            dwf_top = True
        except KeyError:
            dwf_list.append("")
            logging.info(DWF_ERROR + f"{activity_id}")
        try:
            dwr_list.append(details_data["summaryDTO"]["directWorkoutRpe"])
            dwr_top = True
        except KeyError:
            dwr_list.append("")
            logging.info(DWR_ERROR + f"{activity_id}")

        # Update progress bar
        message = "Téléchargement des activités en cours ... "
        display_text = message + f"{iter_count}/{len(activities)}"
        progresstext.configure(text=display_text)
        progressbar.set(progressbar.get() + 1 / len(activities))
        root.update_idletasks()
        iter_count += 1

    # Add detailled data
    meanspeed_idx = activities_data.columns.get_loc("Allure moyenne (km/h)")
    if ams_top:
        activities_data.insert(
            meanspeed_idx + 1,
            "Allure moyenne en déplacement (km/h)",
            ams_list,
        )
    exload_idx = activities_data.columns.get_loc("Exercise load")
    if dwf_top:
        activities_data.insert(
            exload_idx + 1,
            "Comment vous êtes-vous senti ?",
            dwf_list,
        )
    if dwr_top:
        activities_data.insert(
            exload_idx + 2,
            "Effort perçu",
            dwr_list,
        )

    # Add HR zones data
    maxhr_idx = activities_data.columns.get_loc("Fréquence cardiaque maximale (bpm)")
    hrzones_cols = [
        [zone.get("secsInZone", "") if zone else "" for zone in activity]
        for activity in zip_longest(*hrz_data_list)
    ]
    for i, col in enumerate(hrzones_cols):
        activities_data.insert(
            maxhr_idx + i + 1,
            f"Temps en Zone de FC {i + 1} (sec)",
            col,
        )

    # Final update progresstext
    display_text = f"Téléchargement de {len(activities)} activité(s) terminé !"
    progresstext.configure(text=display_text)

    # Process the data
    activities_data = process_activities_data(activities_data)

    return activities_data
