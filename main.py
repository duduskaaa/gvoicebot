from stt import listen
from tts import speak
from parser import parse_intent, extract_city
from skills.time_skill import get_time, get_date
from skills.weather import get_weather


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

    else:
        return "I did not understand the request. Please try again."


def main():
    speak("Voice assistant started. Listening.")

    while True:
        print("👂 Listening...")
        text = listen()

        if not text:
            continue

        response = process_query(text)
        speak(response)


if __name__ == "__main__":
    main()
