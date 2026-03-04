"""
skills/reminder.py — Напоминания
"""

import threading


def set_reminder(seconds: int, message: str, callback) -> str:
    """
    Устанавливает напоминание через N секунд.
    callback — функция, которую вызовем когда время придёт (например speak()).
    """
    def _remind():
        callback(f"Напоминание: {message}")

    timer = threading.Timer(seconds, _remind)
    timer.start()

    minutes = seconds // 60
    if minutes > 0:
        return f"Хорошо, напомню через {minutes} минут."
    else:
        return f"Хорошо, напомню через {seconds} секунд."
