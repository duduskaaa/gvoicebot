import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


class SidebarWidget(QWidget):
    settings_requested = Signal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebar")
        self.setFixedWidth(56)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(8, 16, 8, 16)
        layout.setSpacing(8)
        layout.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        layout.addStretch()

        settings_btn = QPushButton("⚙")
        settings_btn.setObjectName("sidebar_btn")
        settings_btn.setFixedSize(36, 36)
        settings_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        settings_btn.setToolTip("Settings")
        settings_btn.clicked.connect(self.settings_requested)
        layout.addWidget(settings_btn)

        exit_btn = QPushButton("✕")
        exit_btn.setObjectName("exit_btn")
        exit_btn.setFixedSize(36, 36)
        exit_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        exit_btn.setToolTip("Exit")
        exit_btn.clicked.connect(QApplication.quit)
        layout.addWidget(exit_btn)
