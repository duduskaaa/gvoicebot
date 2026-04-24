import os

from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout,
    QLineEdit, QDialogButtonBox, QLabel,
)

from gui.env_utils import save_env


class SettingsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("API Keys")
        self.setMinimumWidth(420)

        layout = QVBoxLayout(self)
        layout.addWidget(QLabel("Keys are saved to <code>.env</code> in the project root."))

        form = QFormLayout()

        self._groq = QLineEdit(os.environ.get("GROQ_API", ""))
        self._groq.setEchoMode(QLineEdit.EchoMode.Password)
        self._groq.setPlaceholderText("gsk_...")

        self._weather = QLineEdit(os.environ.get("OPENWEATHER_API", ""))
        self._weather.setEchoMode(QLineEdit.EchoMode.Password)
        self._weather.setPlaceholderText("Enter OpenWeatherMap key")

        form.addRow("GROQ_API:", self._groq)
        form.addRow("OPENWEATHER_API:", self._weather)
        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _save(self):
        updates: dict[str, str] = {}

        groq = self._groq.text().strip()
        if groq:
            os.environ["GROQ_API"] = groq
            updates["GROQ_API"] = groq

        weather = self._weather.text().strip()
        if weather:
            os.environ["OPENWEATHER_API"] = weather
            updates["OPENWEATHER_API"] = weather

        if updates:
            save_env(updates)

        self.accept()
