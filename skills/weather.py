WEATHER_STUB = {
    "almaty": "In Almaty it is around 8 degrees, partly cloudy.",
    "astana": "In Astana it is around -3 degrees, light snow.",
}


def get_weather(city="Almaty"):
    return WEATHER_STUB.get(city.lower(), f"Weather data for {city} is not available.")
