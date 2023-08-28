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


def save_credentials(email):
    with open("credentials.txt", "w") as f:
        f.write(email)


def load_credentials():
    try:
        with open("credentials.txt", "r") as f:
            return f.read().strip()
    except FileNotFoundError:
        return None


def submit():
    email = email_entry.get()
    password = password_entry.get()
    startdate = (
        start_year.get() + "-" + start_month.get() + "-" + start_day.get()
    )
    enddate = end_year.get() + "-" + end_month.get() + "-" + end_day.get()

    api = init_api(email=email, password=password)

    progress.set(0)
    progress.grid(row=11, column=0, columnspan=3, pady=(0, 30))

    # Save the email
    save_credentials(email)

    filename = get_activities(
        api=api,
        startdate=startdate,
        enddate=enddate,
        progressbar=progress,
        progresstext=progress_text,
        root=root,
        activitytype="",
    )
    message = (
        "Activités téléchargées avec succès.\n\n"
        + f"Le fichier est déposé au chemin suivant :\n\n{filename}"
    )
    messagebox.showinfo("Succès", message)


root = CTk()
root.title("Téléchargement d'activités Garmin")

img_light = Image.open("imgs/garmin_lightmode.png")
img_dark = Image.open("imgs/garmin_darkmode.png").resize(img_light.size)

garmin_logo = CTkImage(
    light_image=img_light,
    dark_image=img_dark,
    size=(200, 60),
)

image_label = CTkLabel(root, image=garmin_logo, text="")
image_label.grid(row=0, column=0, columnspan=3, pady=(20, 20))

email_label = CTkLabel(root, text="Email :")
email_label.grid(row=1, column=0, columnspan=3, pady=(10, 0))

email_entry = CTkEntry(root)
email = load_credentials()
if email:
    email_entry.insert(0, email)
email_entry.grid(
    row=2, column=0, columnspan=3, pady=(0, 10), ipadx=80, padx=20
)

password_label = CTkLabel(root, text="Mot de passe :")
password_label.grid(row=3, column=0, columnspan=3, pady=(10, 0))

password_entry = CTkEntry(root, show="*")
password_entry.grid(
    row=4, column=0, columnspan=3, pady=(0, 10), ipadx=80, padx=20
)

current_year = datetime.now().year

startdate_label = CTkLabel(root, text="Date de début (JJ-MM-AAAA) :")
startdate_label.grid(row=5, column=0, columnspan=3, pady=(10, 0))

start_day = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 32)],
    width=70,
    command=lambda e: update_days_combobox(start_day, start_month, start_year),
)
start_day.set("01")

start_month = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 13)],
    width=70,
    command=lambda e: update_days_combobox(start_day, start_month, start_year),
)
start_month.set("01")

start_year = CTkComboBox(
    root,
    values=[str(i) for i in range(2000, current_year + 1)][::-1],
    width=90,
    command=lambda e: update_days_combobox(start_day, start_month, start_year),
)
start_year.set(current_year)

start_day.grid(row=6, column=0, sticky="W", padx=(50, 0))
start_month.grid(row=6, column=1, sticky="W")
start_year.grid(row=6, column=2, sticky="W", padx=(0, 50))

# create comboboxes for end date
enddate_label = CTkLabel(root, text="Date de fin (JJ-MM-AAAA) :")
enddate_label.grid(row=7, column=0, columnspan=3, pady=(10, 0), ipadx=90)

end_day = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 32)],
    width=70,
    command=lambda e: update_days_combobox(end_day, end_month, end_year),
)
end_day.set(str(datetime.now().day).zfill(2))
end_month = CTkComboBox(
    root,
    values=[str(i).zfill(2) for i in range(1, 13)],
    width=70,
    command=lambda e: update_days_combobox(end_day, end_month, end_year),
)
end_month.set(str(datetime.now().month).zfill(2))
end_year = CTkComboBox(
    root,
    values=[str(i) for i in range(2000, current_year + 1)][::-1],
    width=90,
    command=lambda e: update_days_combobox(end_day, end_month, end_year),
)
end_year.set(current_year)

end_day.grid(row=8, column=0, sticky="W", padx=(50, 0))
end_month.grid(row=8, column=1, sticky="W")
end_year.grid(row=8, column=2, sticky="W", padx=(0, 50))

submit_button = CTkButton(root, text="Télécharger", command=submit)
submit_button.grid(row=9, column=0, columnspan=3, pady=(30, 10), ipadx=80)

progress_text = CTkLabel(root, text="")
progress_text.grid(row=10, column=0, columnspan=3)

progress = CTkProgressBar(
    root, orientation="horizontal", width=300, height=15, mode="determinate"
)

root.mainloop()
