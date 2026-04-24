from dataclasses import dataclass
from enum import Enum


class AssistantState(Enum):
    WAKE = "wake"
    COMMAND = "command"
    PROCESSING = "processing"
    SPEAKING = "speaking"


@dataclass(frozen=True)
class StateInfo:
    badge: str
    color: str
    description: str


STATE_INFO: dict[AssistantState, StateInfo] = {
    AssistantState.WAKE:       StateInfo("WAKE",     "#B7BDF8", "Listening for 'Voicebot'..."),
    AssistantState.COMMAND:    StateInfo("REC",      "#ED8796", "Listening for command..."),
    AssistantState.PROCESSING: StateInfo("THINKING", "#EED49F", "Processing..."),
    AssistantState.SPEAKING:   StateInfo("SPEAKING", "#A6DA95", "Speaking..."),
}
