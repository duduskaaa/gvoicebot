import sys

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget


def _sidebar_btn(icon: str, tooltip: str, callback, name: str = "sidebar_btn") -> QPushButton:
    btn = QPushButton(icon)
    btn.setObjectName(name)
    btn.setFixedSize(36, 36)
    btn.setCursor(Qt.CursorShape.PointingHandCursor)
    btn.setToolTip(tooltip)
    btn.clicked.connect(callback)
    return btn


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
        layout.addWidget(_sidebar_btn("⚙", "Settings", self.settings_requested))
        layout.addWidget(_sidebar_btn("✕", "Exit", QApplication.quit, name="exit_btn"))
