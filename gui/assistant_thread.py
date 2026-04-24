import threading

from PySide6.QtCore import QThread, Signal

from gui.state import AssistantState
from stt import listen, listen_for_wake_word
from tts import speak
from main import process_query


class AssistantThread(QThread):
    state_changed = Signal(AssistantState)
    message_added = Signal(str, str)  # role, text

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manual_event = threading.Event()

    def activate(self):
        self._manual_event.set()

    def run(self):
        speak("Voice assistant started. Say Voicebot to activate.")

        while True:
            self.state_changed.emit(AssistantState.WAKE)

            if self._manual_event.is_set():
                self._manual_event.clear()
            elif not listen_for_wake_word():
                continue

            speak("Yes?")

            self.state_changed.emit(AssistantState.COMMAND)
            text = listen()
            if not text:
                continue

            self.message_added.emit("user", text)

            self.state_changed.emit(AssistantState.PROCESSING)
            response = process_query(text)

            self.state_changed.emit(AssistantState.SPEAKING)
            self.message_added.emit("bot", response)
            speak(response)
