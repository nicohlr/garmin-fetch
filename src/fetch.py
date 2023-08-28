import os
import yaml
import hashlib
import pickle
from datetime import datetime
from tkinter import messagebox
from customtkinter import (
    CTkButton,
    CTk,
    CTkLabel,
    CTkEntry,
)

from utils import get_activities, init_api


def submit():
    email = email_entry.get()
    password = password_entry.get()
    startdate = startdate_entry.get()
    enddate = enddate_entry.get()

    api = init_api(email=email, password=password)
    get_activities(
        api=api,
        startdate=startdate,
        enddate=enddate,
        activitytype="",
    )
    messagebox.showinfo("Succès", "Activités téléchargées avec succès.")


root = CTk()

email_label = CTkLabel(root, text="Email:")
email_label.pack(pady=(10, 0), ipadx=100)

email_entry = CTkEntry(root)
email_entry.pack(pady=(0, 10))

password_label = CTkLabel(root, text="Mot de passe:")
password_label.pack(pady=(10, 0), ipadx=100)

password_entry = CTkEntry(root, show="*")
password_entry.pack(pady=(0, 10))

startdate_label = CTkLabel(root, text="Date de début (JJ-MM-AAAA):")
startdate_label.pack(pady=(10, 0), ipadx=100)

startdate_entry = CTkEntry(root)
startdate_entry.insert(
    0, datetime.strptime("1900-01-01", "%Y-%m-%d").strftime("%Y-%m-%d")
)
startdate_entry.pack(pady=(0, 10))

enddate_label = CTkLabel(root, text="Date de fin (JJ-MM-AAAA):")
enddate_label.pack(pady=(10, 0), ipadx=100)

enddate_entry = CTkEntry(root)
enddate_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
enddate_entry.pack(pady=(0, 10))

submit_button = CTkButton(root, text="Télécharger", command=submit)
submit_button.pack(pady=(10, 30), ipadx=80)

# email, password = load_credentials()

# if email and password:
#     email_entry.insert(0, email)
#     password_entry.insert(0, password)

root.mainloop()
