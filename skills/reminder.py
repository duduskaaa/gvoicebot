import re
import threading

_PATTERN = re.compile(
    r"in\s+(\d+)\s*(seconds|second|minutes|minute|hours|hour)",
    re.IGNORECASE,
)

_UNITS_TO_SECONDS = {
    "second": 1, "seconds": 1,
    "minute": 60, "minutes": 60,
    "hour": 3600, "hours": 3600,
}


def parse_reminder(text: str):
    match = _PATTERN.search(text)
    if not match:
        return None, None

    amount = int(match.group(1))
    unit = match.group(2).lower()
    seconds = amount * _UNITS_TO_SECONDS[unit]

    message = text[match.end():].strip()
    if not message:
        message = "Time is up!"

    return seconds, message


def set_reminder(seconds: int, message: str, callback) -> str:
    def _remind():
        callback(f"Reminder: {message}")

    threading.Timer(seconds, _remind).start()

    if seconds >= 3600:
        value = seconds // 3600
        unit = "hour" if value == 1 else "hours"
    elif seconds >= 60:
        value = seconds // 60
        unit = "minute" if value == 1 else "minutes"
    else:
        value = seconds
        unit = "second" if value == 1 else "seconds"

    return f"Got it, I will remind you in {value} {unit}."
