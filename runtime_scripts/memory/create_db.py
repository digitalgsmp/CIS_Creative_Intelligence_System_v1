import sqlite3
import os
from datetime import datetime, timezone

DB_PATH = "/mnt/projects/cis/memory/cis_memory.db"

def create_database():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS decisions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            decision_number TEXT UNIQUE NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            rationale TEXT NOT NULL,
            status TEXT DEFAULT 'locked',
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS session_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_date TEXT NOT NULL,
            focus TEXT NOT NULL,
            completed TEXT NOT NULL,
            next_steps TEXT NOT NULL,
            notes TEXT,
            created_at TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS corrections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            record_id TEXT NOT NULL,
            field_name TEXT NOT NULL,
            original_value TEXT,
            corrected_value TEXT NOT NULL,
            correction_type TEXT NOT NULL,
            corrected_by TEXT DEFAULT 'human',
            created_at TEXT NOT NULL
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS schema_versions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            schema_name TEXT UNIQUE NOT NULL,
            version TEXT NOT NULL,
            description TEXT,
            is_current INTEGER DEFAULT 1,
            created_at TEXT NOT NULL
        )
    """)

    now = datetime.now(timezone.utc).isoformat()

    c.execute("""
        INSERT OR IGNORE INTO schema_versions
        (schema_name, version, description, is_current, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (
        "knowledge_record",
        "v1",
        "Minimal retrieval-ready record schema as defined in MASTER_ARCHITECTURE_MAP",
        1,
        now
    ))

    c.execute("""
        INSERT OR IGNORE INTO session_log
        (session_date, focus, completed, next_steps, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        "2026-04-17",
        "Infrastructure — storage architecture and vLLM runtime",
        "Five drives mounted and configured. vLLM 0.19.0 restored at /mnt/models/vllm-env. Qwen2.5-VL-32B confirmed ready. System disk freed from 86% to 60%.",
        "Build SQLite memory database. Begin Phase PD harness coordinator script.",
        "cis-vllm env moved from /home/eric to /mnt/models. PYTHONPATH fix applied to activate script.",
        now
    ))

    conn.commit()
    conn.close()
    print(f"Database created at {DB_PATH}")
    print("Tables: decisions, session_log, corrections, schema_versions")

if __name__ == "__main__":
    create_database()
