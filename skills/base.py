import re
from abc import ABC, abstractmethod


class Skill(ABC):
    keywords: list[str] = []

    def can_handle(self, text: str) -> bool:
        lower = text.lower()
        return any(
            re.search(rf"\b{re.escape(kw)}\b", lower)
            for kw in self.keywords
        )

    @abstractmethod
    def execute(self, text: str) -> str: ...
