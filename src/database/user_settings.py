import os
import psycopg2
import psycopg2.extras
from typing import Optional
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

VALID_MODES = {"chat", "chat_grammar", "grammar"}
DEFAULT_MODE = "chat_grammar"


def _connect():
    conn = psycopg2.connect(DATABASE_URL, sslmode="require")
    return conn


def init_db() -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id       BIGINT PRIMARY KEY,
                    language_code TEXT NOT NULL,
                    mode          TEXT NOT NULL DEFAULT 'chat_grammar',
                    updated_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS messages (
                    id            BIGSERIAL PRIMARY KEY,
                    user_id       BIGINT NOT NULL,
                    role          TEXT NOT NULL,
                    content       TEXT NOT NULL,
                    language_code TEXT,
                    mode          TEXT,
                    message_type  TEXT,
                    created_at    TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        conn.commit()


def get_language(user_id: int) -> Optional[str]:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT language_code FROM user_settings WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()
            return row[0] if row else None


def set_language(user_id: int, language_code: str) -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_settings(user_id, language_code, mode)
                VALUES(%s, %s, 'chat_grammar')
                ON CONFLICT(user_id) DO UPDATE SET
                    language_code = EXCLUDED.language_code,
                    updated_at    = CURRENT_TIMESTAMP
            """, (user_id, language_code))
        conn.commit()


def get_mode(user_id: int) -> str:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT mode FROM user_settings WHERE user_id = %s",
                (user_id,)
            )
            row = cur.fetchone()
            return row[0] if row else DEFAULT_MODE


def set_mode(user_id: int, mode: str) -> None:
    if mode not in VALID_MODES:
        raise ValueError(f"Invalid mode: {mode}")
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_settings(user_id, language_code, mode)
                VALUES(
                    %s,
                    COALESCE(
                        (SELECT language_code FROM user_settings WHERE user_id = %s),
                        'vi'
                    ),
                    %s
                )
                ON CONFLICT(user_id) DO UPDATE SET
                    mode       = EXCLUDED.mode,
                    updated_at = CURRENT_TIMESTAMP
            """, (user_id, user_id, mode))
        conn.commit()


def save_message(user_id: int, role: str, content: str,
                 language_code: str = None, mode: str = None,
                 message_type: str = None) -> None:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO messages(user_id, role, content, language_code, mode, message_type)
                VALUES(%s, %s, %s, %s, %s, %s)
            """, (user_id, role, content, language_code, mode, message_type))
        conn.commit()


def get_stats(user_id: int) -> dict:
    from datetime import date, timedelta
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) FROM messages WHERE user_id = %s AND role = 'user'",
                (user_id,)
            )
            total_messages = cur.fetchone()[0]

            cur.execute("""
            SELECT COUNT(*) FROM messages
            WHERE user_id = %s AND message_type = 'grammar'
            """, (user_id,))
            grammar_corrections = cur.fetchone()[0]

            cur.execute("""
                SELECT DISTINCT language_code FROM messages
                WHERE user_id = %s AND role = 'user' AND language_code IS NOT NULL
            """, (user_id,))
            languages = [r[0] for r in cur.fetchall()]

            cur.execute("""
                SELECT DISTINCT DATE(created_at) as d FROM messages
                WHERE user_id = %s AND role = 'user'
                ORDER BY d DESC
            """, (user_id,))
            active_dates = [r[0] for r in cur.fetchall()]

    streak = 0
    if active_dates:
        today = date.today()
        check = today
        for d in active_dates:
            if d == check or d == check - timedelta(days=1):
                streak += 1
                check = d
            else:
                break

    return {
        "total_messages":      total_messages,
        "grammar_corrections": grammar_corrections,
        "languages":           languages,
        "streak":              streak,
        "active_days":         len(active_dates),
    }


def get_recent_messages(user_id: int, limit: int = 10) -> list:
    with _connect() as conn:
        with conn.cursor() as cur:
            cur.execute("""
                SELECT role, content FROM messages
                WHERE user_id = %s
                ORDER BY created_at DESC
                LIMIT %s
            """, (user_id, limit))
            rows = cur.fetchall()
            return [{"role": r[0], "content": r[1]} for r in reversed(rows)]