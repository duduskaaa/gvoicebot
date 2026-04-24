from datetime import datetime

_MONTHS = [
    "", "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December"
]

_WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def get_time():
    now = datetime.now()
    return f"It is {now.hour:02d}:{now.minute:02d}."


def get_date():
    now = datetime.now()
    return f"Today is {_WEEKDAYS[now.weekday()]}, {_MONTHS[now.month]} {now.day}, {now.year}."
