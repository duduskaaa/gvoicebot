from datetime import datetime

from skills.base import Skill

_DAYS = ("Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
_MONTHS = ("", "January", "February", "March", "April", "May", "June",
           "July", "August", "September", "October", "November", "December")


class TimeSkill(Skill):
    keywords = ["time", "what time", "current time", "clock"] #

    def execute(self, text: str) -> str:
        now = datetime.now()
        return f"It is {now.hour:02d}:{now.minute:02d}."


class DateSkill(Skill):
    keywords = ["date", "what day", "today", "what is today"]

    def execute(self, text: str) -> str:
        now = datetime.now()
        return f"Today is {_DAYS[now.weekday()]}, {_MONTHS[now.month]} {now.day}, {now.year}."
