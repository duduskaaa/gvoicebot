from db import _SEP
from skills.base import Skill


class Assistant:
    def __init__(self, skills: list[Skill]):
        self._skills = skills

    def process(self, text: str) -> tuple[str | None, str]:
        print(f"🧠 Processing: {text}")
        for skill in self._skills:
            if skill.can_handle(text):
                raw = skill.execute(text)
                if raw.startswith(_SEP):
                    parts = raw.split(_SEP, 2)
                    return (parts[1], parts[2]) if len(parts) == 3 else (None, raw)
                return None, raw
        return None, "I did not understand the request. Please try again."
