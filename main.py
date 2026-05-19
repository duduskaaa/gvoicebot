from assistant import Assistant
from skills.calculator import CalculatorSkill
from skills.greeting import GreetingSkill
from skills.history import HistorySkill
from skills.reminder import ReminderSkill
from skills.time_skill import DateSkill, TimeSkill
from skills.weather import WeatherSkill

_assistant = Assistant([
    HistorySkill(),
    GreetingSkill(),
    TimeSkill(),
    DateSkill(),
    WeatherSkill(),
    CalculatorSkill(),
    ReminderSkill(),
])


def process_query(text: str) -> tuple[str | None, str]:
    return _assistant.process(text)


if __name__ == "__main__":
    from gui.app import run
    run()
