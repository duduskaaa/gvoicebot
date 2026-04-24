import os
import requests

_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city="Almaty"):
    _API_KEY = os.environ.get("OPENWEATHER_API")
    if not _API_KEY:
        return "OpenWeatherMap API key is not set. Please set the OPENWEATHER_API environment variable."

    try:
        response = requests.get(
            _BASE_URL,
            params={"q": city, "appid": _API_KEY, "units": "metric", "lang": "en"},
            timeout=5,
        )
        if response.status_code == 404:
            return f"City '{city}' not found."
        response.raise_for_status()

        data = response.json()
        temp = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"]
        return f"In {city}: {temp} degrees, {description}. Feels like {feels_like}."

    except requests.exceptions.Timeout:
        return "Could not retrieve weather: request timed out."
    except requests.exceptions.RequestException:
        return "Could not retrieve weather data. Check your internet connection."
