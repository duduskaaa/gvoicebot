from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel

from gui.state import AssistantState, STATE_INFO


class StatusWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("status_frame")
        self.setFixedHeight(52)

        layout = QHBoxLayout(self)
        layout.setContentsMargins(16, 0, 16, 0)
        layout.setSpacing(12)

        self._badge = QLabel()
        self._badge.setFixedWidth(88)
        self._badge.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._label = QLabel()

        layout.addWidget(self._badge)
        layout.addWidget(self._label)
        layout.addStretch()

        self.set_state(AssistantState.WAKE)

    def set_state(self, state: AssistantState):
        info = STATE_INFO[state]
        self._badge.setText(info.badge)
        self._badge.setStyleSheet(f"""
            QLabel {{
                background-color: {info.color};
                color: #1E2030;
                border-radius: 4px;
                padding: 4px 0px;
                font-weight: bold;
                font-size: 10px;
            }}
        """)
        self._label.setText(info.description)
