from abc import ABC, abstractmethod


class Skill(ABC):
    keywords: list[str] = []

    def can_handle(self, text: str) -> bool:
        return any(kw in text.lower() for kw in self.keywords)

    @abstractmethod
    def execute(self, text: str) -> str: ...
