"""
skills/weather.py — Получение погоды через OpenWeatherMap API
"""

import requests
import os

API_KEY = os.environ.get("OPENWEATHER_API_KEY")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"


def get_weather(city: str = "Москва") -> str:
    """
    Возвращает строку с описанием погоды в городе.
    """
    try:
        response = requests.get(BASE_URL, params={
            "q": city,
            "appid": API_KEY,
            "units": "metric",   # Цельсий
            "lang": "ru"
        })
        data = response.json()

        if response.status_code != 200:
            return f"Не удалось получить погоду для города {city}."

        temp = round(data["main"]["temp"])
        description = data["weather"][0]["description"]
        wind = round(data["wind"]["speed"])
        humidity = data["main"]["humidity"]

        return (
            f"В {city} сейчас {temp} градусов по Цельсию, {description}. "
            f"Скорость ветра {wind} метров в секунду, влажность {humidity} процентов."
        )

    except Exception as e:
        return f"Ошибка при получении погоды: {e}"
