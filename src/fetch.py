import os
import yaml
import getpass
import hashlib
import pickle

from utils import get_activities, init_api
from datetime import datetime


def save_credentials(email, password):
    hashed = hashlib.sha256(password.encode()).hexdigest()
    with open("credentials.pkl", "wb") as file:
        pickle.dump({"email": email, "password": hashed}, file)


def load_credentials():
    with open("credentials.pkl", "rb") as file:
        credentials = pickle.load(file)
    return credentials["email"], credentials["password"]


def check_credentials():
    if os.path.exists("credentials.pkl"):
        return load_credentials()
    else:
        email = input("Entre votre email : ")
        password = getpass.getpass("Entrez votre mot de passe : ")
        save_credentials(email, password)
        return email, password


if __name__ == "__main__":
    email, password = check_credentials()

    config_pth = os.path.join(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        "conf/config.yml",
    )

    with open(config_pth, "r") as file:
        params = yaml.safe_load(file)

    api = init_api(email=email, password=password)

    startdate = "1900-01-01"  # very old startdate
    enddate = datetime.now().strftime('%Y-%m-%d')  # current date

    get_activities(
        api=api,
        startdate=params["startdate"],
        enddate=params["enddate"],
        activitytype="",
    )
