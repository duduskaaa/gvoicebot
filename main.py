"""
main.py — Главный цикл голосового ассистента
"""

from stt import listen
from tts import speak
from parser import parse_intent, extract_city
from skills.time_skill import get_time, get_date
from skills.weather import get_weather


def process_query(text: str) -> str:
    """
    Определяет intent и возвращает ответ.
    """
    intent = parse_intent(text)
    print(f"🧠 Intent: {intent}")

    if intent == "greeting":
        return "Привет! Я ваш голосовой ассистент. Чем могу помочь?"

    elif intent == "time":
        return get_time()

    elif intent == "date":
        return get_date()

    elif intent == "weather":
        city = extract_city(text)
        return get_weather(city)

    else:
        return "Не понял запрос. Попробуйте ещё раз."


def main():
    speak("Голосовой ассистент запущен. Слушаю вас!")

    while True:
        try:
            print("👂 Слушаю...")
            text = listen()

            if not text:
                continue

            response = process_query(text)
            speak(response)

        except KeyboardInterrupt:
            speak("До свидания!")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            speak("Произошла ошибка. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
