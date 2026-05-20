import os

from groq import Groq

from db import _SEP
from skills.base import Skill


def _groq_chat(text: str) -> str:
    api_key = os.environ.get("GROQ_API")
    if not api_key:
        return "I did not understand the request. Please try again."
    try:
        client = Groq(api_key=api_key)
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant", #
            messages=[{"role": "user", "content": text}],
            max_tokens=150, #
        )
        return response.choices[0].message.content.strip()
    except Exception:
        return "I did not understand the request. Please try again."


class Assistant:
    def __init__(self, skills: list[Skill]):
        self._skills = skills

    def process(self, text: str) -> tuple[str, str]: #
        print(f"🧠 Processing: {text}")
        for skill in self._skills:
            if skill.can_handle(text):
                raw = skill.execute(text)
                if raw.startswith(_SEP):
                    parts = raw.split(_SEP, 2)
                    return (parts[1], parts[2]) if len(parts) == 3 else (None, raw)
                return None, raw
        return None, _groq_chat(text)
