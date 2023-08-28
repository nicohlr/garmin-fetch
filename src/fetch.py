import os
import yaml
import hashlib
import pickle
from datetime import datetime
from tkinter import messagebox, ttk
from customtkinter import (
    CTkButton,
    CTk,
    CTkLabel,
    CTkEntry,
    CTkProgressBar,
    CTkImage,
    CTkTextbox,
)

from PIL import Image

from utils import get_activities, init_api


def submit():
    email = email_entry.get()
    password = password_entry.get()
    startdate = startdate_entry.get()
    enddate = enddate_entry.get()

    api = init_api(email=email, password=password)

    filename = get_activities(
        api=api,
        startdate=startdate,
        enddate=enddate,
        progressbar=progress,
        progresstext=progress_text,
        root=root,
        activitytype="",
    )
    messagebox.showinfo(
        "Succès",
        f"Activités téléchargées avec succès. \n\n Le fichier est déposé au chemin suivant : {filename}",
    )


root = CTk()

img_light = Image.open("imgs/garmin_lightmode.png")
img_dark = Image.open("imgs/garmin_darkmode.png").resize(img_light.size)

garmin_logo = CTkImage(
    light_image=img_light,
    dark_image=img_dark,
    size=(200, 60),
)

image_label = CTkLabel(root, image=garmin_logo, text="")
image_label.pack(pady=(20, 20))

email_label = CTkLabel(root, text="Email :")
email_label.pack(pady=(10, 0))

email_entry = CTkEntry(root)
email_entry.pack(pady=(0, 10), ipadx=80)

password_label = CTkLabel(root, text="Mot de passe :")
password_label.pack(pady=(10, 0))

password_entry = CTkEntry(root, show="*")
password_entry.pack(pady=(0, 10), ipadx=80)

startdate_label = CTkLabel(root, text="Date de début (JJ-MM-AAAA) :")
startdate_label.pack(pady=(10, 0), ipadx=100)

startdate_entry = CTkEntry(root)
startdate_entry.insert(
    0, datetime.strptime("2023-07-28", "%Y-%m-%d").strftime("%Y-%m-%d")
)
startdate_entry.pack(pady=(0, 10))

enddate_label = CTkLabel(root, text="Date de fin (JJ-MM-AAAA) :")
enddate_label.pack(pady=(10, 0), ipadx=100)

enddate_entry = CTkEntry(root)
enddate_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
enddate_entry.pack(pady=(0, 10))

submit_button = CTkButton(root, text="Télécharger", command=submit)
submit_button.pack(pady=(10, 10), ipadx=80)


progress_text = CTkLabel(root, text="")
progress_text.pack()

progress = CTkProgressBar(
    root, orientation="horizontal", width=300, height=15, mode="determinate"
)
progress.set(0)
progress.pack(pady=(0, 20))

root.mainloop()
