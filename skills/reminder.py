import re
import threading

from skills.base import Skill

_PATTERN = re.compile(
    r"in\s+(\d+)\s*(seconds|second|minutes|minute|hours|hour)",
    re.IGNORECASE,
)
_UNITS = {
    "second": 1, "seconds": 1,
    "minute": 60, "minutes": 60,
    "hour": 3600, "hours": 3600,
}


class ReminderSkill(Skill):
    keywords = ["remind me", "set a reminder", "reminder in"]

    def execute(self, text: str) -> str:
        match = _PATTERN.search(text)
        if not match:
            return "Please say how long: for example, remind me in 5 minutes to check the oven."

        seconds = int(match.group(1)) * _UNITS[match.group(2).lower()]
        message = text[match.end():].strip() or "Time is up!"

        self._schedule(seconds, message)

        if seconds >= 3600:
            v, u = seconds // 3600, "hour"
        elif seconds >= 60:
            v, u = seconds // 60, "minute"
        else:
            v, u = seconds, "second"
        if v != 1:
            u += "s"
        return f"Got it, I will remind you in {v} {u}."

    def _schedule(self, seconds: int, message: str) -> None:
        from tts import speak
        threading.Timer(seconds, lambda: speak(f"Reminder: {message}")).start()
