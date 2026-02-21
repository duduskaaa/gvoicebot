"""
parser.py — Определение намерения пользователя (intent)
и извлечение параметров из текста
"""

import re


# Ключевые слова для каждого intent
INTENTS = {
    "greeting": ["привет", "здравствуй", "добрый день", "добрый вечер", "хай", "салют"],
    "time": ["время", "который час", "сколько времени", "часы"],
    "date": ["дата", "какое сегодня", "какой день", "число"],
    "weather": ["погода", "температура", "на улице", "за окном"],
    "calculate": ["сколько будет", "вычисли", "посчитай", "калькулятор", "плюс", "минус", "умножить", "разделить"],
    "reminder": ["напомни", "напоминание", "через", "минут", "не забудь"],
}


def parse_intent(text: str) -> str:
    """
    Определяет намерение пользователя по ключевым словам.
    Возвращает строку с названием intent или 'unknown'.
    """
    text_lower = text.lower()

    for intent, keywords in INTENTS.items():
        for keyword in keywords:
            if keyword in text_lower:
                return intent

    return "unknown"


def extract_city(text: str) -> str:
    """
    Извлекает название города из текста.
    Пример: "погода в Москве" → "Москва"
    """
    # Ищем паттерн "в <Город>"
    match = re.search(r"\bв\s+([А-ЯЁ][а-яё]+)", text)
    if match:
        return match.group(1)
    return "Москва"  # Город по умолчанию


def extract_math_expression(text: str) -> str:
    """
    Извлекает математическое выражение из текста.
    Заменяет слова на операторы.
    Пример: "сколько будет 5 плюс 3" → "5 + 3"
    """
    text = text.lower()
    text = re.sub(r"сколько будет|вычисли|посчитай", "", text)
    text = text.replace("плюс", "+")
    text = text.replace("минус", "-")
    text = text.replace("умножить на", "*")
    text = text.replace("разделить на", "/")
    text = text.strip()
    return text


def extract_reminder_params(text: str) -> tuple[int, str]:
    """
    Извлекает время и текст напоминания.
    Пример: "напомни через 5 минут выпить воды" → (300, "выпить воды")
    Возвращает (секунды, сообщение).
    """
    # Ищем число минут
    match = re.search(r"через\s+(\d+)\s+минут", text)
    minutes = int(match.group(1)) if match else 1
    seconds = minutes * 60

    # Убираем служебные слова, остаток — сообщение
    message = re.sub(r"напомни|через\s+\d+\s+минут", "", text).strip()
    if not message:
        message = "Напоминание!"

    return seconds, message
