def process_activities_data(activities_data):
    """Process and order the activities data.

    Args:
        activities_data (DataFrame): DataFrame containing raw activities data.

    Returns:
        DataFrame: Processed activities data.
    """

    columns_order = [
        "Type d'activité",
        "Date",
        "Favori",
        "Titre",
        "Intervalle",
        "Distance",
        "Heure",
        "Temps de déplacement",
        "Fréquence cardiaque moy.",
        "Fréquence cardiaque maximale",
        "Allure moyenne",
        "Allure moyenne en déplacement",
        "Meilleure allure",
        "Cadence de course moyenne",
        "Cadence de course maximale",
        "Longueur moyenne des foulées",
        "Température moyenne",
        "Calories",
        "Gain d'altitude",
        "Perte d'altitude",
    ]

    present_columns = [
        col for col in columns_order if col in activities_data.columns
    ]

    additional_columns = [
        col for col in activities_data.columns if col not in present_columns
    ]
    present_columns.extend(additional_columns)

    processed_data = (
        activities_data[present_columns]
        .drop(["Intervalle", "Heure"], axis=1)
        .reset_index(drop=True)
    )

    return processed_data
