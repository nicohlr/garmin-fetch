import os
import sys
import threading
import customtkinter

from datetime import datetime
from tkinter import messagebox
from customtkinter import (
    CTkButton,
    CTk,
    CTkLabel,
    CTkEntry,
    CTkProgressBar,
    CTkImage,
    CTkComboBox,
)

from PIL import Image

from utils import get_activities, init_api
from garminconnect import (
    GarminConnectAuthenticationError,
    GarminConnectTooManyRequestsError,
)


customtkinter.set_appearance_mode("dark")


def days_in_month(month, year):
    """Return the number of days in a given month and year."""
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


def update_days_combobox(combobox_day, combobox_month, combobox_year):
    """Update the number of days in a combobox based on the month and year."""
    month = int(combobox_month.get())
    year = int(combobox_year.get())
    current_day = int(combobox_day.get())

    max_day = days_in_month(month, year)

    combobox_day["values"] = [str(i).zfill(2) for i in range(1, max_day + 1)]
    if current_day > max_day:
        combobox_day.set(str(max_day).zfill(2))
    root.update_idletasks()


def save_settings(email, start_date, activity_type):
    with open("settings.txt", "w") as f:
        f.write(email + "\n")
        f.write(start_date + "\n")
        f.write(activity_type)


def load_settings():
    try:
        with open("settings.txt", "r") as f:
            lines = f.readlines()
            email = lines[0].strip()
            start_date = lines[1].strip() if len(lines) > 1 else None
            activity_type = lines[2].strip() if len(lines) > 2 else None
            return email, start_date, activity_type
    except FileNotFoundError:
        return None, None, None


def init_api_and_followup(
    email, password, startdate, enddate, activity_type, selected_activity
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
        api,
        email,
        startdate,
        enddate,
        activity_type,
        selected_activity,
        error,
    )


def post_init(
    api, email, startdate, enddate, activity_type, selected_activity, error
):
    progress.stop()
    progress["mode"] = "determinate"
    progress_text.configure(text="")

    if error:
        if isinstance(error, GarminConnectAuthenticationError):
            error_message.configure(
                text="Erreur d'authentification.\n Veuillez vérifier vos identifiants."
            )
        elif isinstance(error, GarminConnectTooManyRequestsError):
            error_message.configure(
                text="Trop de requêtes à Garmin Connect.\nVeuillez réessayer plus tard."
            )
        else:
            error_message.configure(text=f"Erreur inattendue: {str(error)}")
        progress.grid_forget()
        progress_text.grid_forget()
        submit_button.grid_configure(pady=(20, 60))
        error_message.grid(sticky="ew", row=1, column=0, columnspan=3)
        return

    save_settings(email, startdate, selected_activity)

    filename = get_activities(
        api=api,
        startdate=startdate,
        enddate=enddate,
        progressbar=progress,
        progresstext=progress_text,
        root=root,
        activitytype=activity_type,
    )
    message = (
        "Activités téléchargées avec succès.\n\n"
        + f"Le fichier est déposé au chemin suivant :\n\n{filename}"
    )
    messagebox.showinfo("Succès", message)


def submit():
    email = email_entry.get()
    password = password_entry.get()
    startdate = (
        start_year.get() + "-" + start_month.get() + "-" + start_day.get()
    )
    enddate = end_year.get() + "-" + end_month.get() + "-" + end_day.get()
    selected_activity = activity_type_combobox.get()
    activity_type = activity_types[selected_activity]

    # Check if password is empty
    if not email:
        error_message.configure(text="Email manquant.")
        progress.grid_forget()
        progress_text.grid_forget()
        submit_button.grid_configure(pady=(20, 60))
        error_message.grid(sticky="ew", row=1, column=0, columnspan=3)
        return

    # Check email validity
    if not email or "@" not in email:
        error_message.configure(text="Email invalide.")
        progress.grid_forget()
        progress_text.grid_forget()
        submit_button.grid_configure(pady=(20, 60))
        error_message.grid(sticky="ew", row=1, column=0, columnspan=3)
        return

    # Check if password is empty
    if not password:
        error_message.configure(text="Mot de passe manquant.")
        progress.grid_forget()
        progress_text.grid_forget()
        submit_button.grid_configure(pady=(20, 60))
        error_message.grid(sticky="ew", row=1, column=0, columnspan=3)
        return

    # Convert the start and end dates to datetime objects for comparison
    start_datetime = datetime.strptime(startdate, "%Y-%m-%d")
    end_datetime = datetime.strptime(enddate, "%Y-%m-%d")

    # Check if start date is after end date
    if start_datetime > end_datetime:
        error_message.configure(
            text="La date de début ne peut pas être\npostérieure à la date de fin."
        )
        progress.grid_forget()
        progress_text.grid_forget()
        submit_button.grid_configure(pady=(20, 60))
        error_message.grid(sticky="ew", row=1, column=0, columnspan=3)
        return

    error_message.grid_forget()

    progress_text.configure(text="Connexion à l'API Garmin en cours ...")
    progress["mode"] = "indeterminate"
    progress_text.grid(sticky="ew", row=13, column=0, columnspan=3)
    progress.grid(
        sticky="ew", row=14, column=0, columnspan=3, pady=(0, 30), padx=40
    )
    submit_button.grid_configure(pady=(30, 10))

    progress.start()
    root.update_idletasks()

    # api = init_api(email=email, password=password)
    # Use threading to run the lengthy function without blocking the GUI
    thread = threading.Thread(
        target=init_api_and_followup,
        args=(
            email,
            password,
            startdate,
            enddate,
            activity_type,
            selected_activity,
        ),
    )
    thread.start()


if getattr(sys, "frozen", False):
    # we are running in a bundle
    bundle_dir = os.path.dirname(sys.executable)
else:
    # we are running in a normal Python environment
    bundle_dir = os.path.dirname(os.path.abspath(__file__))

icon_path = os.path.join(os.path.dirname(bundle_dir), "imgs", "garmin.ico")

root = CTk()
root.title("Téléchargement d'activités Garmin Connect")
root.resizable(False, False)
root.iconbitmap(icon_path)

# Configure column weights
root.grid_columnconfigure(0, weight=1)  # left padding column
root.grid_columnconfigure(1, weight=2)  # main content column
root.grid_columnconfigure(2, weight=1)  # right padding column

# Configure row weights
for i in range(1, 15):
    root.grid_rowconfigure(i, weight=1)


img_light_path = os.path.join(
    os.path.dirname(bundle_dir), "imgs", "garmin_lightmode.png"
)
img_dark_path = os.path.join(
    os.path.dirname(bundle_dir), "imgs", "garmin_darkmode.png"
)

img_light = Image.open(img_light_path)
img_dark = Image.open(img_dark_path).resize(img_light.size)

garmin_logo = CTkImage(
    light_image=img_light,
    dark_image=img_dark,
    size=(200, 60),
)

image_label = CTkLabel(root, image=garmin_logo, text="")
image_label.grid(sticky="ew", row=0, column=0, columnspan=3, pady=(20, 20))

error_message = CTkLabel(root, text="", text_color="red")

email_label = CTkLabel(root, text="Email :")
email_label.grid(sticky="ew", row=2, column=0, columnspan=3, pady=(10, 0))

email_entry = CTkEntry(root)
email, saved_start_date, saved_activity_type = load_settings()

if email:
    email_entry.insert(0, email)
email_entry.grid(
    sticky="ew", row=3, column=0, columnspan=3, pady=(0, 10), ipadx=70, padx=40
)

password_label = CTkLabel(root, text="Mot de passe :")
password_label.grid(sticky="ew", row=4, column=0, columnspan=3, pady=(10, 0))

password_entry = CTkEntry(root, show="●")
password_entry.grid(
    sticky="ew", row=5, column=0, columnspan=3, pady=(0, 10), ipadx=70, padx=40
)

current_year = datetime.now().year

startdate_label = CTkLabel(root, text="Date de début (JJ-MM-AAAA) :")
startdate_label.grid(sticky="ew", row=6, column=0, columnspan=3, pady=(10, 0))

start_day = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 32)],
    width=60,
    command=lambda e: update_days_combobox(start_day, start_month, start_year),
)

start_month = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 13)],
    width=60,
    command=lambda e: update_days_combobox(start_day, start_month, start_year),
)

start_year = CTkComboBox(
    root,
    values=[str(i) for i in range(2000, current_year + 1)][::-1],
    width=80,
    command=lambda e: update_days_combobox(start_day, start_month, start_year),
)

if saved_start_date:
    saved_year, saved_month, saved_day = saved_start_date.split("-")
    start_year.set(saved_year)
    start_month.set(saved_month)
    start_day.set(saved_day)
else:
    start_year.set(current_year)
    start_month.set("01")
    start_day.set("01")


start_day.grid(row=7, column=0, sticky="EW", padx=(60, 10))
start_month.grid(row=7, column=1, sticky="EW", padx=(10, 10))
start_year.grid(row=7, column=2, sticky="EW", padx=(10, 60))

# create comboboxes for end date
enddate_label = CTkLabel(root, text="Date de fin (JJ-MM-AAAA) :")
enddate_label.grid(
    sticky="ew", row=8, column=0, columnspan=3, pady=(10, 0), ipadx=90
)

end_day = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 32)],
    width=60,
    command=lambda e: update_days_combobox(end_day, end_month, end_year),
)
end_day.set(str(datetime.now().day).zfill(2))
end_month = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 13)],
    width=60,
    command=lambda e: update_days_combobox(end_day, end_month, end_year),
)
end_month.set(str(datetime.now().month).zfill(2))
end_year = CTkComboBox(
    root,
    values=[str(i) for i in range(2000, current_year + 1)][::-1],
    width=80,
    command=lambda e: update_days_combobox(end_day, end_month, end_year),
)
end_year.set(current_year)

end_day.grid(row=9, column=0, sticky="EW", padx=(60, 10))
end_month.grid(row=9, column=1, sticky="EW", padx=(10, 10))
end_year.grid(row=9, column=2, sticky="EW", padx=(10, 60))


# After the end_date ComboBox
activity_type_label = CTkLabel(root, text="Type d'activité :")
activity_type_label.grid(
    sticky="ew", row=10, column=0, columnspan=3, pady=(10, 0)
)

activity_types = {
    "Toutes activités": "",
    "Course": "running",
    "Vélo": "cycling",
    "Natation": "swimming",
}
activity_type_combobox = CTkComboBox(
    root, values=list(activity_types.keys()), width=15
)
activity_type_combobox.set(
    saved_activity_type if saved_activity_type else "Toutes activités"
)
activity_type_combobox.grid(
    sticky="ew",
    row=11,
    column=0,
    columnspan=3,
    pady=(0, 10),
    ipadx=50,
    padx=60,
)

submit_button = CTkButton(
    root, text="Télécharger les activités ↓", command=submit
)
submit_button.grid(
    sticky="ew",
    row=12,
    column=0,
    columnspan=3,
    pady=(20, 60),
    ipadx=70,
    padx=60,
)

progress_text = CTkLabel(root, text="")

progress = CTkProgressBar(
    root,
    orientation="horizontal",
    width=30,
    height=15,
    mode="determinate",
    indeterminate_speed=10,
)

root.mainloop()
