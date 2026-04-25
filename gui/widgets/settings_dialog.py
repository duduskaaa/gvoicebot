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
        updates = {
            key: value
            for key, widget in [("GROQ_API", self._groq), ("OPENWEATHER_API", self._weather)]
            if (value := widget.text().strip())
        }
        for key, value in updates.items():
            os.environ[key] = value
        if updates:
            save_env(updates)
        self.accept()
