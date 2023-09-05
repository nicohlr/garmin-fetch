import os
import sys

from functools import partial
from datetime import datetime
from PIL import Image, ImageTk

from utils.base_utils import load_settings
from utils.constants import ACTIVITY_TYPES_MAPPING
from utils.app_utils import submit, update_days_combobox

from customtkinter import (
    CTkButton,
    CTk,
    CTkLabel,
    CTkEntry,
    CTkProgressBar,
    CTkImage,
    CTkComboBox,
    CTkSegmentedButton,
)


def create_main_window() -> None:
    """
    Create the main window for the Garmin activities download application.

    Determines the path for the assets based on whether the application is
    bundled (e.g., using PyInstaller) or running in a typical Python
    environment. Sets up the main window, including the window's appearance,
    title, and widgets.
    """
    if getattr(sys, "frozen", False):
        # we are running in a bundle
        bundle_dir = sys._MEIPASS
    else:
        # we are running in a normal Python environment
        file_dir = os.path.dirname(os.path.abspath(__file__))
        bundle_dir = os.path.dirname(file_dir)

    root = CTk()
    root.title("Téléchargement d'activités Garmin Connect")
    root.resizable(False, False)

    icon_path_ico = os.path.join(bundle_dir, "assets", "garmin-download.ico")
    icon_path_png = os.path.join(bundle_dir, "assets", "garmin-download.png")

    if os.name == "nt":
        root.iconbitmap(icon_path_ico)
    else:
        iconpil = ImageTk.PhotoImage(Image.open(icon_path_png))
        root.iconphoto(False, iconpil)

    # Configure column weights
    root.grid_columnconfigure(0, weight=1)  # left padding column
    root.grid_columnconfigure(1, weight=2)  # main content column
    root.grid_columnconfigure(2, weight=1)  # right padding column

    # Configure row weights
    for i in range(1, 15):
        root.grid_rowconfigure(i, weight=1)

    img_light_path = os.path.join(bundle_dir, "assets", "garmin_lightmode.png")
    img_dark_path = os.path.join(bundle_dir, "assets", "garmin_darkmode.png")

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
        sticky="ew",
        row=3,
        column=0,
        columnspan=3,
        pady=(0, 10),
        ipadx=70,
        padx=40,
    )

    password_label = CTkLabel(root, text="Mot de passe :")
    password_label.grid(
        sticky="ew", row=4, column=0, columnspan=3, pady=(10, 0)
    )

    password_entry = CTkEntry(root, show="●")
    password_entry.grid(
        sticky="ew",
        row=5,
        column=0,
        columnspan=3,
        pady=(0, 10),
        ipadx=70,
        padx=40,
    )

    current_year = datetime.now().year

    startdate_label = CTkLabel(root, text="Date de début (JJ-MM-AAAA) :")
    startdate_label.grid(
        sticky="ew", row=6, column=0, columnspan=3, pady=(10, 0)
    )

    start_day = CTkComboBox(
        root,
        values=[str(i).zfill(2) for i in range(1, 32)],
        width=60,
        command=lambda e: update_days_combobox(
            root, start_day, start_month, start_year
        ),
    )

    start_month = CTkComboBox(
        root,
        values=[str(i).zfill(2) for i in range(1, 13)],
        width=60,
        command=lambda e: update_days_combobox(
            root, start_day, start_month, start_year
        ),
    )

    start_year = CTkComboBox(
        root,
        values=[str(i) for i in range(2000, current_year + 1)][::-1],
        width=80,
        command=lambda e: update_days_combobox(
            root, start_day, start_month, start_year
        ),
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
        command=lambda e: update_days_combobox(
            root, end_day, end_month, end_year
        ),
    )
    end_day.set(str(datetime.now().day).zfill(2))
    end_month = CTkComboBox(
        root,
        values=[str(i).zfill(2) for i in range(1, 13)],
        width=60,
        command=lambda e: update_days_combobox(
            root, end_day, end_month, end_year
        ),
    )
    end_month.set(str(datetime.now().month).zfill(2))
    end_year = CTkComboBox(
        root,
        values=[str(i) for i in range(2000, current_year + 1)][::-1],
        width=80,
        command=lambda e: update_days_combobox(
            root, end_day, end_month, end_year
        ),
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

    activity_type_combobox = CTkComboBox(
        root, values=list(ACTIVITY_TYPES_MAPPING.keys()), width=15
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

    switch_tcx_label = CTkLabel(
        root,
        text="Inclure les données au format TCX :\n(téléchargement plus long)",
        justify="left",
        font=("SF Display", 11)
    )

    switch_tcx = CTkSegmentedButton(root, values=["Oui", "Non"])
    switch_tcx.set("Non")
    switch_tcx_label.grid(
        row=12, column=0, columnspan=2, sticky="ew", pady=(9, 0), padx=(50, 0)
    )
    switch_tcx.grid(
        row=12, column=2, columnspan=2, sticky="ew", pady=(12, 0), padx=(0, 60)
    )

    submit_button = CTkButton(
        root,
        text="Télécharger les activités ↓",
    )
    submit_button.grid(
        sticky="ew",
        row=13,
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

    widgets = {
        "activity_type_combobox": activity_type_combobox,
        "activity_type_label": activity_type_label,
        "email_entry": email_entry,
        "email_label": email_label,
        "end_day": end_day,
        "end_month": end_month,
        "end_year": end_year,
        "enddate_label": enddate_label,
        "error_message": error_message,
        "garmin_logo": garmin_logo,
        "image_label": image_label,
        "password_entry": password_entry,
        "password_label": password_label,
        "progress": progress,
        "progress_text": progress_text,
        "start_day": start_day,
        "start_month": start_month,
        "start_year": start_year,
        "startdate_label": startdate_label,
        "switch_tcx": switch_tcx,
        "switch_tcx_label": switch_tcx_label,
        "submit_button": submit_button,
    }

    submit_with_args = partial(submit, root, widgets)
    submit_button.configure(command=submit_with_args)

    root.mainloop()


if __name__ == "__main__":
    create_main_window()
