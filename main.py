"""
main.py — Главный цикл голосового ассистента
"""

from stt import listen
from tts import speak
from parser import parse_intent, extract_city, extract_math_expression, extract_reminder_params
from skills.time_skill import get_time, get_date
from skills.weather import get_weather
from skills.calculator import calculate
from skills.reminder import set_reminder


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

    elif intent == "calculate":
        expression = extract_math_expression(text)
        return calculate(expression)

    elif intent == "reminder":
        seconds, message = extract_reminder_params(text)
        return set_reminder(seconds, message, callback=speak)

    else:
        return "Извините, я не понял запрос. Попробуйте ещё раз."


def main():
    speak("Голосовой ассистент запущен. Слушаю вас!")

    while True:
        try:
            text = listen()           # 1. Записываем и распознаём
            if not text:
                continue

            response = process_query(text)  # 2. Обрабатываем
            speak(response)                 # 3. Озвучиваем

        except KeyboardInterrupt:
            speak("До свидания!")
            break
        except Exception as e:
            print(f"Ошибка: {e}")
            speak("Произошла ошибка. Попробуйте ещё раз.")


if __name__ == "__main__":
    main()
