import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("bot.db")

VALID_MODES = {"chat", "chat_grammar", "grammar"}
DEFAULT_MODE = "chat_grammar"


def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return conn


def _add_column_if_missing(conn, table: str, column: str, definition: str):
    try:
        conn.execute(f"SELECT {column} FROM {table} LIMIT 1")
    except sqlite3.OperationalError:
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {definition}")


def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id       INTEGER PRIMARY KEY,
                language_code TEXT NOT NULL,
                mode          TEXT NOT NULL DEFAULT 'chat_grammar',
                updated_at    TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        _add_column_if_missing(conn, "user_settings", "mode", "TEXT NOT NULL DEFAULT 'chat_grammar'")

        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id            INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id       INTEGER NOT NULL,
                role          TEXT NOT NULL,
                content       TEXT NOT NULL,
                language_code TEXT,
                mode          TEXT,
                created_at    TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        _add_column_if_missing(conn, "messages", "language_code", "TEXT")
        _add_column_if_missing(conn, "messages", "mode", "TEXT")

        conn.commit()


def get_language(user_id: int) -> Optional[str]:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT language_code FROM user_settings WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        return row[0] if row else None


def set_language(user_id: int, language_code: str) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO user_settings(user_id, language_code, mode)
            VALUES(?, ?, 'chat_grammar')
            ON CONFLICT(user_id) DO UPDATE SET
                language_code = excluded.language_code,
                updated_at    = CURRENT_TIMESTAMP
            """,
            (user_id, language_code),
        )
        conn.commit()


def get_mode(user_id: int) -> str:
    with _connect() as conn:
        cur = conn.execute(
            "SELECT mode FROM user_settings WHERE user_id = ?",
            (user_id,),
        )
        row = cur.fetchone()
        return row[0] if row else DEFAULT_MODE


def set_mode(user_id: int, mode: str) -> None:
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode: {mode}")
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO user_settings(user_id, language_code, mode)
            VALUES(?, 'vi', ?)
            ON CONFLICT(user_id) DO UPDATE SET
                mode       = excluded.mode,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, mode),
        )
        conn.commit()


def save_message(user_id: int, role: str, content: str,
                 language_code: str = None, mode: str = None) -> None:
    with _connect() as conn:
        conn.execute(
            """
            INSERT INTO messages(user_id, role, content, language_code, mode)
            VALUES(?, ?, ?, ?, ?)
            """,
            (user_id, role, content, language_code, mode),
        )
        conn.commit()


def get_recent_messages(user_id: int, limit: int = 10) -> list:
    with _connect() as conn:
        cur = conn.execute(
            """
            SELECT role, content FROM messages
            WHERE user_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (user_id, limit),
        )
        rows = cur.fetchall()
        return [{"role": r[0], "content": r[1]} for r in reversed(rows)]
