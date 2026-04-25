from assistant import Assistant
from skills.greeting import GreetingSkill
from skills.time_skill import TimeSkill, DateSkill
from skills.weather import WeatherSkill
from skills.calculator import CalculatorSkill
from skills.reminder import ReminderSkill

_assistant = Assistant([
    GreetingSkill(),
    TimeSkill(),
    DateSkill(),
    WeatherSkill(),
    CalculatorSkill(),
    ReminderSkill(),
])


def process_query(text: str) -> str:
    return _assistant.process(text)


if __name__ == "__main__":
    from gui.app import run
    run()
