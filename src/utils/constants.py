# Mappings
ACTIVITY_DATA_MAPPING = {

    # General data
    "activityId": "Identifiant Garmin de l'activité",
    "deviceId": "Identifiant Garmin de l'appareil",
    "startTimeLocal": "Date",
    "activityName": "Titre",
    "favorite": "Favori",
    "duration": "Durée totale (s)",
    "movingDuration": "Durée de déplacement (s)",
    "elapsedDuration": "Temps écoulé (s)",
    "pr": "Présence d'un RP (Record personnel)",

    # Geographic data
    "distance": "Distance (m)",
    "steps": "Nombre de pas",
    "startLatitude": "Latitude de départ",
    "startLongitude": "Longitude de départ",
    "endLatitude": "Latitude de fin",
    "endLongitude": "Longitude de fin",
    "elevationGain": "Gain d'altitude (m)",
    "elevationLoss": "Perte d'altitude (m)",
    "minElevation": "Altitude minimale (m)",
    "maxElevation": "Altitude maximale (m)",
    "minTemperature": "Température minimale",
    "maxTemperature": "Température maximale",

    # Body data
    "averageHR": "Fréquence cardiaque moyenne (bpm)",
    "maxHR": "Fréquence cardiaque maximale (bpm)",
    "minRespirationRate": "Fréquence respiratoire minimale (brpm)",
    "maxRespirationRate": "Fréquence respiratoire maximale (brpm)",
    "avgRespirationRate": "Fréquence respiratoire moyenne (brpm)",
    "vO2MaxValue": "VO2 Max (mL/min/kg)",
    "calories": "Total des calories brûlées",
    "bmrCalories": "Calories au repos",
    "waterEstimated": "Estimation de la transpiration (mL)",
    "waterConsumed": "Liquide consommé (mL)",
    "moderateIntensityMinutes": "Minutes intensives modérées",
    "vigorousIntensityMinutes": "Minutes intensives soutenues",
    "activityTrainingLoad": "Exercise load",
    "aerobicTrainingEffect": "Training Effect aérobie",
    "anaerobicTrainingEffect": "Training Effect anaérobie",
    "trainingEffectLabel": "Avantage principal Training Effect",

    # Données d'activités (toutes)
    "averageSpeed": "Allure moyenne (km/h)",
    "maxSpeed": "Allure maximale (km/h)",
    "avgPower": "Puissance moyenne (W)",
    "maxPower": "Puissance maximale (W)",
    "strokes": "Nombre total de mouvements",
    "avgStrokes": "Nombre moyen de mouvements",
    "floorsClimbed": "Étages grimpés",
    "floorsDescended": "Étages descendus",

    # Données d'activités (course)
    "averageRunningCadenceInStepsPerMinute": "Cadence de course moyenne (pas/min)",
    "maxRunningCadenceInStepsPerMinute": "Cadence de course maximale (pas/min)",
    "avgVerticalRatio": "Rapport vertical moyen (%)",
    "avgGroundContactBalance": "Équilibre moyen temps contact au sol gauche (%)",
    "avgStrideLength": "Longueur moyenne des foulées (m)",

    # Données d'activités (vélo)
    "averageBikingCadenceInRevPerMinute": "Cadence de vélo moyenne (tr/min)",
    "maxBikingCadenceInRevPerMinute": "Cadence de vélo maximale (tr/min)",
    "strokes": "Nombre total de mouvements",

    # Données d'activités (natation)
    "averageSwimCadenceInStrokesPerMinute": "Cadence de natation moyenne (mvt/min)",
    "maxSwimCadenceInStrokesPerMinute": "Cadence de natation maximale (mvt/min)",
    "averageSwolf": "Swolf moyen",
    "activeLengths": "Longueurs",

    # Données d'activités (musculation)
    "summarizedExerciseSets": "Ensemble d'exercices de musculation résumé",
    "totalSets": "Nombre total de séries (musculation)",
    "totalReps": "Nombre total de répétitions (musculation)",

}

ACTIVITY_TYPES_MAPPING = {
    "Toutes activités": "",
    "Course": "running",
    "Vélo": "cycling",
    "Cardio": "indoor_cardio",
    "Natation": "swimming",
    "Natation en eau libre": "open_water_swimming",
    "Marche": "walking",
    "Musculation": "strength_training",
    "Vélo d'intérieur": "indoor_cycling",
    "Multi-sport": "multi_sport",
    "Autre": "other",
}

# Messages
CONNECTION_LOADING_MSG = "Connexion à l'API Garmin en cours ..."
SUCCESS_MSG = (
    "Activités téléchargées avec succès.\n\n"
    + "Le fichier est déposé au chemin suivant :\n\n"
)
SUCCESS_MSG_TCX = (
    "\n\n Les traces TCX sont déposées au chemin suivant :\n\n"
)

# Errors
AMS_ERROR = "averageMovingSpeed (Allure moyenne en déplacement) not found for activity: "
DWF_ERROR = "directWorkoutFeel (Comment vous êtes-vous senti ?) not found for activity: "
DWR_ERROR = "directWorkoutRpe (Effort perçu) not found for activity: "

DATE_ERROR = "La date de début ne peut pas être\npostérieure à la date de fin."
MISSING_PASSWORD_ERROR = "Mot de passe manquant."
WRONG_EMAIL_ERROR = "Email invalide."
MISSING_EMAIL_ERROR = "Email manquant."
TOO_MANY_REQUESTS_ERROR = (
    "Trop de requêtes à Garmin Connect.\nVeuillez réessayer plus tard."
)
LOGIN_ERROR = (
    "Erreur d'authentification.\n Veuillez vérifier vos identifiants."
)
