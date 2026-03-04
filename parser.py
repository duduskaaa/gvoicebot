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
    Пример: "погода в Алматы" → "Алматы"
    """
    match = re.search(r"\bв\s+([А-ЯЁ][а-яё]+)", text)
    if match:
        return match.group(1)
    return "Алматы"  # Город по умолчанию
