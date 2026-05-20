import sys
from pathlib import Path

from PySide6.QtGui import QFont, QFontDatabase
from PySide6.QtWidgets import QApplication

from gui.env_utils import load_env
from gui.main_window import MainWindow

_QSS_PATH = Path(__file__).parent / "style.qss"


def _setup_font(app: QApplication):
    families = QFontDatabase.families()
    name = "JetBrains Mono" if "JetBrains Mono" in families else "Monospace"
    app.setFont(QFont(name, 10))


def run():
    load_env()
    app = QApplication(sys.argv)
    _setup_font(app)
    app.setStyleSheet(_QSS_PATH.read_text())
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
