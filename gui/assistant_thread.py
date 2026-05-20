import threading

from PySide6.QtCore import QThread, Signal #

from db import save_message
from gui.state import AssistantState
from main import process_query
from stt import listen, listen_for_wake_word #
from tts import speak #


class AssistantThread(QThread):
    state_changed = Signal(AssistantState)
    message_added = Signal(str, str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._manual_event = threading.Event()

    def activate(self):
        self._manual_event.set()

    def run(self):
        while True: #
            self.state_changed.emit(AssistantState.WAKE) #

            inline = ""
            if self._manual_event.is_set():
                self._manual_event.clear()
            else:
                detected, inline = listen_for_wake_word() #
                if not detected:
                    continue

            if inline: #
                text = inline
            else:
                speak("Yes?")
                self.state_changed.emit(AssistantState.COMMAND)
                text = listen()
                if not text:
                    continue

            self.message_added.emit("user", text) #
            save_message("user", text)

            self.state_changed.emit(AssistantState.PROCESSING) #
            voice, display = process_query(text) #

            self.state_changed.emit(AssistantState.SPEAKING) #
            self.message_added.emit("bot", display)
            save_message("bot", display)
            if voice is None: #
                speak(display)
            elif voice:
                speak(voice)
