ACTIVITY_TYPES_MAPPING = {
    "Toutes activités": "",
    "Course": "running",
    "Vélo": "cycling",
    "Natation": "swimming",
}

CONNECTION_LOADING_MSG = "Connexion à l'API Garmin en cours ..."
SUCCESS_MSG = (
    "Activités téléchargées avec succès.\n\n"
    + "Le fichier est déposé au chemin suivant :\n\n"
)

DATE_ERROR = "La date de début ne peut pas être\npostérieure à la date de fin."
MISSING_PASSWORD_ERROR = "Mot de passe manquant."
WRONG_EMAIL_ERROR = "Email invalide."
MISSING_EMAIL_ERROR = "Email manquant."
TOO_MANY_REQUESTS_ERROR = "Trop de requêtes à Garmin Connect.\nVeuillez réessayer plus tard."
LOGIN_ERROR = "Erreur d'authentification.\n Veuillez vérifier vos identifiants."