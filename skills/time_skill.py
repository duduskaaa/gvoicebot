import calendar
from datetime import datetime

from skills.base import Skill


class TimeSkill(Skill):
    keywords = ["time", "what time", "current time", "clock"]

    def execute(self, text: str) -> str:
        now = datetime.now()
        return f"It is {now.hour:02d}:{now.minute:02d}."


class DateSkill(Skill):
    keywords = ["date", "what day", "today", "what is today"]

    def execute(self, text: str) -> str:
        now = datetime.now()
        return f"Today is {calendar.day_name[now.weekday()]}, {calendar.month_name[now.month]} {now.day}, {now.year}."
