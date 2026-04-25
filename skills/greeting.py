from skills.base import Skill


class GreetingSkill(Skill):
    keywords = ["hello", "hi", "good morning", "good evening", "hey", "greetings"]

    def execute(self, text: str) -> str:
        return "Hello! I am your voice assistant. How can I help you?"
