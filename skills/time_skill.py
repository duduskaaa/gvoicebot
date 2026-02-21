"""
skills/time_skill.py — Текущее время и дата
"""

from datetime import datetime

WEEKDAYS = ["понедельник", "вторник", "среда", "четверг", "пятница", "суббота", "воскресенье"]
MONTHS = ["января", "февраля", "марта", "апреля", "мая", "июня",
          "июля", "августа", "сентября", "октября", "ноября", "декабря"]

def get_time() -> str:
    now = datetime.now()
    return f"Сейчас {now.hour} часов {now.minute:02d} минут."

def get_date() -> str:
    now = datetime.now()
    weekday = WEEKDAYS[now.weekday()]
    month = MONTHS[now.month - 1]
    return f"Сегодня {weekday}, {now.day} {month} {now.year} года."
