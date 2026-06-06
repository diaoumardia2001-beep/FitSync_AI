import requests

# Coordonnées d'Abidjan par défaut
DEFAULT_CITY = "Abidjan"
DEFAULT_LAT = 5.3600
DEFAULT_LON = -4.0083

WEATHER_CODES = {
    0:  {"desc": "Ciel dégagé",      "icon": "☀️",  "condition": "clear"},
    1:  {"desc": "Principalement clair", "icon": "🌤️", "condition": "clear"},
    2:  {"desc": "Partiellement nuageux","icon": "⛅", "condition": "cloudy"},
    3:  {"desc": "Couvert",           "icon": "☁️",  "condition": "cloudy"},
    45: {"desc": "Brouillard",        "icon": "🌫️", "condition": "cloudy"},
    48: {"desc": "Brouillard givrant","icon": "🌫️", "condition": "cloudy"},
    51: {"desc": "Bruine légère",     "icon": "🌦️", "condition": "rain"},
    53: {"desc": "Bruine modérée",    "icon": "🌦️", "condition": "rain"},
    55: {"desc": "Bruine dense",      "icon": "🌧️", "condition": "rain"},
    61: {"desc": "Pluie légère",      "icon": "🌧️", "condition": "rain"},
    63: {"desc": "Pluie modérée",     "icon": "🌧️", "condition": "rain"},
    65: {"desc": "Pluie forte",       "icon": "🌧️", "condition": "rain"},
    80: {"desc": "Averses légères",   "icon": "🌦️", "condition": "rain"},
    81: {"desc": "Averses modérées",  "icon": "🌧️", "condition": "rain"},
    82: {"desc": "Averses violentes", "icon": "⛈️",  "condition": "rain"},
    95: {"desc": "Orage",             "icon": "⛈️",  "condition": "rain"},
}


def get_weather(city=DEFAULT_CITY,
                lat=DEFAULT_LAT,
                lon=DEFAULT_LON):
    """
    Récupère la météo actuelle via API open-meteo.com
    API gratuite — aucune clé requise
    """
    try:
        url = (
            f"https://api.open-meteo.com/v1/forecast"
            f"?latitude={lat}"
            f"&longitude={lon}"
            f"&current_weather=true"
            f"&hourly=relativehumidity_2m"
        )

        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        current = data.get("current_weather", {})
        temp = current.get("temperature", 0)
        wind = current.get("windspeed", 0)
        code = current.get("weathercode", 0)

        weather_info = WEATHER_CODES.get(
            code,
            {"desc": "Inconnu",
             "icon": "🌡️",
             "condition": "unknown"}
        )

        # Déterminer condition finale
        condition = weather_info["condition"]
        if temp > 35:
            condition = "hot"

        result = {
            "city": city,
            "temperature": temp,
            "wind_speed": wind,
            "description": weather_info["desc"],
            "icon": weather_info["icon"],
            "condition": condition,
            "recommendation": get_workout_recommendation(
                condition, temp
            )
        }

        return result

    except requests.exceptions.ConnectionError:
        print("⚠️ Pas de connexion internet")
        return get_default_weather()
    except requests.exceptions.Timeout:
        print("⚠️ Timeout API météo")
        return get_default_weather()
    except Exception as e:
        print(f"⚠️ Erreur météo : {e}")
        return get_default_weather()


def get_workout_recommendation(condition, temp):
    """
    Retourne une recommandation d'entraînement
    adaptée à la météo du jour
    """
    recommendations = {
        "clear": (
            "🌤️ Beau temps → Parfait pour "
            "le Running ou le Cycling en extérieur !"
        ),
        "cloudy": (
            "⛅ Temps nuageux → Idéal pour "
            "un jogging ou une sortie vélo"
        ),
        "rain": (
            "🌧️ Pluie détectée → Privilégiez "
            "Yoga ou Strength Training en intérieur"
        ),
        "hot": (
            f"🥵 Chaleur ({temp}°C) → Entraînement léger, "
            "hydratez-vous bien, évitez le plein soleil"
        ),
        "unknown": (
            "💪 Consultez la météo locale "
            "avant votre entraînement"
        )
    }
    return recommendations.get(
        condition,
        recommendations["unknown"]
    )


def get_default_weather():
    """
    Météo par défaut si API indisponible
    """
    return {
        "city": DEFAULT_CITY,
        "temperature": 28,
        "wind_speed": 10,
        "description": "Données indisponibles",
        "icon": "🌡️",
        "condition": "unknown",
        "recommendation": (
            "💪 Consultez la météo locale "
            "avant votre entraînement"
        )
    }


def display_weather(weather):
    """
    Affiche la météo de façon formatée
    """
    print(f"\n{'='*45}")
    print(f"🌍 Météo — {weather['city']}")
    print(f"{'='*45}")
    print(f"{weather['icon']} {weather['description']}")
    print(f"🌡️  Température : {weather['temperature']}°C")
    print(f"💨 Vent        : {weather['wind_speed']} km/h")
    print(f"🏋️  Conseil     : {weather['recommendation']}")
    print(f"{'='*45}")