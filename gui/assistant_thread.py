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
        speak("Voice assistant started. Say Voice to activate.")

        while True:
            self.state_changed.emit(AssistantState.WAKE)

            inline = ""
            if self._manual_event.is_set():
                self._manual_event.clear()
            else:
                detected, inline = listen_for_wake_word()
                if not detected:
                    continue

            if inline:
                text = inline
            else:
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
