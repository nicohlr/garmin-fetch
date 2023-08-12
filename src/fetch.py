import os
import yaml

from utils import get_activities, init_api


if __name__ == "__main__":

    config_pth = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "conf/config.yml",
    )

    with open(config_pth, "r") as file:
        params = yaml.safe_load(file)

    api = init_api(email=params["email"], password=params["password"])

    get_activities(
        api=api,
        startdate=params["startdate"],
        enddate=params["enddate"],
        dest_folder="./activities/",
        activitytype="",
    )
