#!/usr/bin/env python3
import sqlite3
import argparse
from datetime import datetime, timezone

DB_PATH = "/mnt/projects/cis/memory/cis_memory.db"

def get_now():
    return datetime.now(timezone.utc).isoformat()

def ensure_insights_table(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            observation TEXT NOT NULL,
            source_record_id TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

def log_decision(number, title, description, rationale):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = get_now()
    try:
        c.execute("""
            INSERT INTO decisions
            (decision_number, title, description, rationale, status, created_at, updated_at)
            VALUES (?, ?, ?, ?, 'locked', ?, ?)
        """, (number, title, description, rationale, now, now))
        conn.commit()
        print(f"Decision {number} locked: {title}")
    except sqlite3.IntegrityError:
        print(f"Decision {number} already exists. Use update to modify.")
    finally:
        conn.close()

def log_session(focus, completed, next_steps, notes=""):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = get_now()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    c.execute("""
        INSERT INTO session_log
        (session_date, focus, completed, next_steps, notes, created_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (today, focus, completed, next_steps, notes, now))
    conn.commit()
    print(f"Session logged for {today}: {focus}")
    conn.close()

def log_correction(record_id, field_name, original, corrected, correction_type):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    now = get_now()
    c.execute("""
        INSERT INTO corrections
        (record_id, field_name, original_value, corrected_value, correction_type, corrected_by, created_at)
        VALUES (?, ?, ?, ?, ?, 'human', ?)
    """, (record_id, field_name, original, corrected, correction_type, now))
    conn.commit()
    print(f"Correction logged for {record_id}.{field_name}")
    conn.close()

def log_insight(category, title, observation, source=None):
    conn = sqlite3.connect(DB_PATH)
    ensure_insights_table(conn)
    c = conn.cursor()
    now = get_now()
    c.execute("""
        INSERT INTO insights
        (category, title, observation, source_record_id, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, (category, title, observation, source, now))
    conn.commit()
    print(f"Insight logged [{category}]: {title}")
    conn.close()

def show_recent(table, limit=5):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    if table == "decisions":
        c.execute("SELECT decision_number, title, status, created_at FROM decisions ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        print(f"\nLast {limit} decisions:")
        for r in rows:
            print(f"  [{r[0]}] {r[1]} — {r[2]} — {r[3][:10]}")
    elif table == "sessions":
        c.execute("SELECT session_date, focus, next_steps FROM session_log ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        print(f"\nLast {limit} sessions:")
        for r in rows:
            print(f"  {r[0]}: {r[1]}")
            print(f"    Next: {r[2]}")
    elif table == "corrections":
        c.execute("SELECT record_id, field_name, correction_type, created_at FROM corrections ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        print(f"\nLast {limit} corrections:")
        for r in rows:
            print(f"  {r[0]}.{r[1]} — {r[2]} — {r[3][:10]}")
    elif table == "insights":
        ensure_insights_table(conn)
        c.execute("SELECT category, title, observation, created_at FROM insights ORDER BY id DESC LIMIT ?", (limit,))
        rows = c.fetchall()
        print(f"\nLast {limit} insights:")
        for r in rows:
            print(f"  [{r[0]}] {r[1]} — {r[3][:10]}")
            print(f"    {r[2]}")
    conn.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CIS Memory Logger")
    subparsers = parser.add_subparsers(dest="command")

    d = subparsers.add_parser("decision", help="Log a locked decision")
    d.add_argument("number", help="Decision number e.g. ADR-001")
    d.add_argument("title", help="Short title")
    d.add_argument("description", help="What was decided")
    d.add_argument("rationale", help="Why it was decided")

    s = subparsers.add_parser("session", help="Log a work session")
    s.add_argument("focus", help="What this session focused on")
    s.add_argument("completed", help="What was completed")
    s.add_argument("next_steps", help="What comes next")
    s.add_argument("--notes", default="", help="Optional notes")

    cor = subparsers.add_parser("correction", help="Log a record correction")
    cor.add_argument("record_id", help="Record ID")
    cor.add_argument("field_name", help="Field that was corrected")
    cor.add_argument("original", help="Original value")
    cor.add_argument("corrected", help="Corrected value")
    cor.add_argument("correction_type", help="Type: hallucination|category|tag|structure|uncertainty")

    ins = subparsers.add_parser("insight", help="Log a realtime insight")
    ins.add_argument("category", help="Type: architectural|extraction|workflow|system")
    ins.add_argument("title", help="Short title")
    ins.add_argument("observation", help="The insight text")
    ins.add_argument("--source", default=None, help="Optional record_id this insight relates to")

    sh = subparsers.add_parser("show", help="Show recent entries")
    sh.add_argument("table", choices=["decisions", "sessions", "corrections", "insights"])
    sh.add_argument("--limit", type=int, default=5)

    args = parser.parse_args()

    if args.command == "decision":
        log_decision(args.number, args.title, args.description, args.rationale)
    elif args.command == "session":
        log_session(args.focus, args.completed, args.next_steps, args.notes)
    elif args.command == "correction":
        log_correction(args.record_id, args.field_name, args.original, args.corrected, args.correction_type)
    elif args.command == "insight":
        log_insight(args.category, args.title, args.observation, args.source)
    elif args.command == "show":
        show_recent(args.table, args.limit)
    else:
        parser.print_help()
