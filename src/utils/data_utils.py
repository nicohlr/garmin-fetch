def process_activities_data(data):
    """Process and order the activities data.

    Args:
        data (DataFrame): DataFrame containing raw activities data.

    Returns:
        DataFrame: Processed activities data.
    """
    data["Identifiant Garmin de l'activité"] = data[
        "Identifiant Garmin de l'activité"
    ].astype(str)
    data["Identifiant Garmin de l'appareil"] = data[
        "Identifiant Garmin de l'appareil"
    ].astype(str)

    data["Avantage principal Training Effect"] = data[
        "Avantage principal Training Effect"
    ].map(
        {
            'RECOVERY': "Récupération",
            "TEMPO": "Tempo",
            "AEROBIC_BASE": "Base",
            "LACTATE_THRESHOLD": "Seuil",
            "UNKNOWN": "",
            "VO2MAX": "VO2 Max",
        }
    )
    if "Comment vous êtes-vous senti ?" in data.columns:
        data["Comment vous êtes-vous senti ?"] = data[
            "Comment vous êtes-vous senti ?"
        ].map(
            {
                0: "Très faible",
                25: "Faible",
                50: "Normal(e)",
                75: "Fort(e)",
                100: "Très fort(e)",
            }
        )

    if "Effort perçu" in data.columns:
        data["Effort perçu"] = (
            (data["Effort perçu"].replace({"": -10}) / 10)
            .fillna(-1)
            .astype(int)
            .astype(str)
            .replace(str(-1), "")
        )

    data["Favori"] = (
        data["Favori"]
        .astype(str)
        .str.lower()
        .replace({"true": "Oui", "false": "Non"})
    )
    data["Présence d'un RP (Record personnel)"] = (
        data["Présence d'un RP (Record personnel)"]
        .astype(str)
        .str.lower()
        .replace({"true": "Oui", "false": "Non"})
    )
    data["Allure moyenne (km/h)"] = data["Allure moyenne (km/h)"] * 3.6
    data["Allure maximale (km/h)"] = data["Allure maximale (km/h)"] * 3.6

    if "Allure moyenne en déplacement (km/h)" in data.columns:
        data["Allure moyenne en déplacement (km/h)"] = (
            data["Allure moyenne en déplacement (km/h)"] * 3.6
        )

    data = data.fillna("")

    return data
