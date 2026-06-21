import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "sessions.db")


def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = get_conn()
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            session_id  TEXT PRIMARY KEY,
            created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
            last_active DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS messages (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT NOT NULL REFERENCES sessions(session_id),
            role        TEXT NOT NULL CHECK(role IN ('user','assistant')),
            content     TEXT NOT NULL,
            intent      TEXT,
            confidence  REAL,
            tools_used  TEXT,
            escalated   INTEGER DEFAULT 0,
            timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS escalations (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id  TEXT REFERENCES sessions(session_id),
            trigger     TEXT NOT NULL,
            summary     TEXT NOT NULL,
            timestamp   DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE INDEX IF NOT EXISTS idx_messages_session ON messages(session_id);
        CREATE INDEX IF NOT EXISTS idx_messages_timestamp ON messages(timestamp);
    """)
    conn.commit()
    conn.close()


def upsert_session(session_id: str):
    conn = get_conn()
    conn.execute("""
        INSERT INTO sessions(session_id) VALUES(?)
        ON CONFLICT(session_id) DO UPDATE SET last_active=CURRENT_TIMESTAMP
    """, (session_id,))
    conn.commit()
    conn.close()


def log_message(session_id: str, role: str, content: str,
                intent: str = None, confidence: float = None,
                tools_used: list = None, escalated: bool = False):
    import json
    conn = get_conn()
    conn.execute("""
        INSERT INTO messages(session_id, role, content, intent, confidence, tools_used, escalated)
        VALUES(?,?,?,?,?,?,?)
    """, (
        session_id, role, content, intent, confidence,
        json.dumps(tools_used) if tools_used else None,
        1 if escalated else 0
    ))
    conn.commit()
    conn.close()


def log_escalation(session_id: str, trigger: str, summary: str):
    conn = get_conn()
    conn.execute(
        "INSERT INTO escalations(session_id, trigger, summary) VALUES(?,?,?)",
        (session_id, trigger, summary)
    )
    conn.commit()
    conn.close()


def get_session_messages(session_id: str) -> list[dict]:
    conn = get_conn()
    rows = conn.execute(
        "SELECT role, content, intent, tools_used, escalated, timestamp FROM messages WHERE session_id=? ORDER BY id",
        (session_id,)
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]
