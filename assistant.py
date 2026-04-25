from skills.base import Skill


class Assistant:
    def __init__(self, skills: list[Skill]):
        self._skills = skills

    def process(self, text: str) -> str:
        print(f"🧠 Processing: {text}")
        for skill in self._skills:
            if skill.can_handle(text):
                return skill.execute(text)
        return "I did not understand the request. Please try again."
