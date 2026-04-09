import sqlite3
from pathlib import Path
from typing import Optional

DB_PATH = Path("bot.db")

def _connect():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA synchronous=NORMAL;")
    return sqlite3.connect(DB_PATH)

def init_db() -> None:
    with _connect() as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS user_settings (
                user_id INTEGER PRIMARY KEY,
                language_code TEXT NOT NULL,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
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
            INSERT INTO user_settings(user_id, language_code)
            VALUES(?, ?)
            ON CONFLICT(user_id) DO UPDATE SET
                language_code = excluded.language_code,
                updated_at = CURRENT_TIMESTAMP
            """,
            (user_id, language_code),
        )
        conn.commit()
        