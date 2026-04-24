from stt import listen, listen_for_wake_word
from tts import speak
from parser import parse_intent, extract_city
from skills.time_skill import get_time, get_date
from skills.weather import get_weather
from skills.calculator import calculate
from skills.reminder import parse_reminder, set_reminder


def process_query(text):
    intent = parse_intent(text)
    print(f"🧠 Intent: {intent}")

    if intent == "greeting":
        return "Hello! I am your voice assistant. How can I help you?"

    elif intent == "time":
        return get_time()

    elif intent == "date":
        return get_date()

    elif intent == "weather":
        city = extract_city(text)
        return get_weather(city)

    elif intent == "calculator":
        return calculate(text)

    elif intent == "reminder":
        seconds, message = parse_reminder(text)
        if seconds is None:
            return "Please say how long: for example, remind me in 5 minutes to check the oven."
        return set_reminder(seconds, message, speak)

    else:
        return "I did not understand the request. Please try again."


def main():
    from gui.app import run
    run()


if __name__ == "__main__":
    main()
