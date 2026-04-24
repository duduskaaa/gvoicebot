import sys

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from gui.env_utils import load_env
from gui.main_window import MainWindow

_STYLESHEET = """
/* === Catppuccin Macchiato === */

QMainWindow, QWidget {
    background-color: #24273A;
    color: #CAD3F5;
}

QWidget#sidebar {
    background-color: #1E2030;
    border-right: 1px solid #363A4F;
}

QFrame#status_frame {
    background-color: #363A4F;
    border: 1px solid #494D64;
    border-radius: 8px;
}

QPushButton#activate_btn {
    background-color: #8AADF4;
    color: #1E2030;
    border: none;
    border-radius: 6px;
    font-weight: bold;
}

QPushButton#activate_btn:hover {
    background-color: #B7BDF8;
}

QPushButton#activate_btn:pressed {
    background-color: #91D7E3;
}

QPushButton#sidebar_btn {
    background-color: transparent;
    color: #8087A2;
    border: none;
    border-radius: 6px;
    font-size: 16px;
}

QPushButton#sidebar_btn:hover {
    background-color: #363A4F;
    color: #CAD3F5;
}

QPushButton#exit_btn {
    background-color: transparent;
    color: #8087A2;
    border: none;
    border-radius: 6px;
    font-size: 16px;
}

QPushButton#exit_btn:hover {
    background-color: #ED8796;
    color: #1E2030;
}

QTextEdit {
    background-color: #1E2030;
    border: 1px solid #363A4F;
    border-radius: 8px;
    color: #CAD3F5;
    selection-background-color: #8AADF4;
    selection-color: #1E2030;
    padding: 8px;
}

QDialog {
    background-color: #24273A;
}

QLabel {
    background: transparent;
    color: #CAD3F5;
}

QLineEdit {
    background-color: #363A4F;
    border: 1px solid #494D64;
    border-radius: 4px;
    padding: 6px 10px;
    color: #CAD3F5;
}

QLineEdit:focus {
    border: 1px solid #8AADF4;
}

QDialogButtonBox QPushButton {
    background-color: #8AADF4;
    color: #1E2030;
    border: none;
    border-radius: 4px;
    padding: 6px 16px;
    min-width: 70px;
}

QDialogButtonBox QPushButton:hover {
    background-color: #B7BDF8;
}
"""


def _setup_font(app: QApplication):
    families = QFontDatabase.families()
    name = "JetBrains Mono" if "JetBrains Mono" in families else "Monospace"
    app.setFont(QFont(name, 10))


def run():
    load_env()
    app = QApplication(sys.argv)
    _setup_font(app)
    app.setStyleSheet(_STYLESHEET)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
