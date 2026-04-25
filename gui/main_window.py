from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import (
    QHBoxLayout, QLineEdit, QMainWindow, QPushButton, QVBoxLayout, QWidget,
)

from gui.assistant_thread import AssistantThread
from gui.widgets.chat_widget import ChatWidget
from gui.widgets.settings_dialog import SettingsDialog
from gui.widgets.sidebar import SidebarWidget
from gui.widgets.status_widget import StatusWidget


class _TextWorker(QThread):
    finished = Signal(str)

    def __init__(self, text: str, parent=None):
        super().__init__(parent)
        self._text = text

    def run(self):
        from main import process_query
        self.finished.emit(process_query(self._text))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("GVoiceBot")
        self.setMinimumSize(700, 600)
        self._build_ui()
        self._start_thread()

    def _build_ui(self):
        root = QWidget()
        self.setCentralWidget(root)

        h_layout = QHBoxLayout(root)
        h_layout.setSpacing(0)
        h_layout.setContentsMargins(0, 0, 0, 0)

        self._sidebar = SidebarWidget()
        self._sidebar.settings_requested.connect(self._open_settings)
        h_layout.addWidget(self._sidebar)

        main = QWidget()
        v_layout = QVBoxLayout(main)
        v_layout.setContentsMargins(16, 16, 16, 16)
        v_layout.setSpacing(10)

        self._status = StatusWidget()
        v_layout.addWidget(self._status)

        self._chat = ChatWidget()
        v_layout.addWidget(self._chat, stretch=1)

        text_row = QHBoxLayout()
        text_row.setSpacing(8)

        self._text_input = QLineEdit()
        self._text_input.setPlaceholderText("Type a command and press Enter...")
        self._text_input.setFixedHeight(40)
        self._text_input.returnPressed.connect(self._on_send)
        text_row.addWidget(self._text_input)

        send_btn = QPushButton("Send")
        send_btn.setObjectName("send_btn")
        send_btn.setFixedSize(80, 40)
        send_btn.clicked.connect(self._on_send)
        text_row.addWidget(send_btn)

        v_layout.addLayout(text_row)

        self._activate_btn = QPushButton("Activate")
        self._activate_btn.setObjectName("activate_btn")
        self._activate_btn.setFixedHeight(40)
        self._activate_btn.clicked.connect(self._on_activate)
        v_layout.addWidget(self._activate_btn)

        h_layout.addWidget(main)

    def _start_thread(self):
        self._thread = AssistantThread(self)
        self._thread.state_changed.connect(self._status.set_state)
        self._thread.message_added.connect(self._chat.append_message)
        self._thread.start()

    def _on_activate(self):
        self._thread.activate()

    def _on_send(self):
        text = self._text_input.text().strip()
        if not text:
            return
        self._text_input.clear()
        self._chat.append_message("user", text)
        self._worker = _TextWorker(text, self)
        self._worker.finished.connect(lambda reply: self._chat.append_message("bot", reply))
        self._worker.start()

    def _open_settings(self):
        SettingsDialog(self).exec()

    def closeEvent(self, event):
        self._thread.terminate()
        self._thread.wait(2000)
        super().closeEvent(event)
