import os
import re

import requests

from skills.base import Skill

_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


class WeatherSkill(Skill):
    keywords = ["weather", "temperature", "outside"]

    def execute(self, text: str) -> str:
        city = self._extract_city(text)
        return self._fetch(city)

    def _extract_city(self, text: str) -> str:
        match = re.search(r"\b(?:in|for)\s+([A-Za-z][A-Za-z ]*[A-Za-z]|[A-Za-z]+)", text)
        if match:
            return match.group(1).strip().title()
        match = re.search(r"\bweather\s+([A-Za-z][A-Za-z ]*[A-Za-z]|[A-Za-z]+)", text)
        return match.group(1).strip().title() if match else "Almaty"

    def _fetch(self, city: str) -> str:
        api_key = os.environ.get("OPENWEATHER_API")
        if not api_key:
            return "OpenWeatherMap API key is not set. Please set the OPENWEATHER_API environment variable."
        try:
            response = requests.get(
                _BASE_URL,
                params={"q": city, "appid": api_key, "units": "metric", "lang": "en"},
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
