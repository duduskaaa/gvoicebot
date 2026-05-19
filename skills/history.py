from db import clear_history, get_history, get_today_history, voice_display
from skills.base import Skill


class HistorySkill(Skill):
    keywords = ["show history", "chat history", "our conversation", "history today", "clear history"]

    def execute(self, text: str) -> str:
        lower = text.lower()

        if "clear history" in lower:
            clear_history()
            return voice_display("", "History cleared.")

        if "history today" in lower:
            rows = get_today_history()
            header = "Today's conversation:"
        else:
            rows = get_history(limit=20)
            header = "Last 20 messages:"

        if not rows:
            return voice_display("", "No conversation history saved yet.")

        lines = [header]
        for timestamp, role, message in rows:
            label = "You" if role == "user" else "Bot"
            lines.append(f"[{timestamp}] {label}: {message}")

        return voice_display("Here is the history.", "\n".join(lines))
