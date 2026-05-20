import sqlite3
from pathlib import Path

_DB_PATH = Path(__file__).parent / "history.db"

_SEP = "\x00"


def voice_display(voice: str, display: str) -> str:
    return f"{_SEP}{voice}{_SEP}{display}"


def _connect() -> sqlite3.Connection:
    conn = sqlite3.connect(_DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id        INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT    DEFAULT (datetime('now', 'localtime')),
            role      TEXT    NOT NULL,
            text      TEXT    NOT NULL
        )
    """) #
    conn.commit()
    return conn


def save_message(role: str, text: str) -> None:
    with _connect() as conn:
        conn.execute("INSERT INTO messages (role, text) VALUES (?, ?)", (role, text))


def get_history(limit: int = 20) -> list[tuple[str, str, str]]: #
    with _connect() as conn:
        cur = conn.execute(
            "SELECT timestamp, role, text FROM messages ORDER BY id DESC LIMIT ?",
            (limit,),
        )
        return list(reversed(cur.fetchall()))


def get_today_history() -> list[tuple[str, str, str]]: #
    with _connect() as conn:
        cur = conn.execute(
            "SELECT timestamp, role, text FROM messages"
            " WHERE date(timestamp) = date('now', 'localtime')"
            " ORDER BY id"
        )
        return cur.fetchall()


def clear_history() -> None:
    with _connect() as conn:
        conn.execute("DELETE FROM messages")
