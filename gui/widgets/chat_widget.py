from PySide6.QtGui import QColor, QTextCharFormat
from PySide6.QtWidgets import QTextEdit

_STYLE: dict[str, tuple[str, str]] = {
    "user": ("#8AADF4", "You   "),
    "bot":  ("#A6DA95", "Bot   "),
}


class ChatWidget(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)

    def append_message(self, role: str, text: str):
        color, prefix = _STYLE.get(role, ("#CAD3F5", ""))

        fmt = QTextCharFormat()
        fmt.setForeground(QColor(color))

        cursor = self.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        cursor.insertText(f"{prefix}{text}\n\n", fmt)
        self.setTextCursor(cursor)
        self.ensureCursorVisible()
