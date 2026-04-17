#!/usr/bin/env python3
import sqlite3
from datetime import datetime, timezone

DB_PATH = "/mnt/projects/cis/memory/cis_memory.db"

def divider(char="─", width=60):
    print(char * width)

def load_context():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    divider("═")
    print("  CIS — Creative Intelligence System")
    print(f"  Session start: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M UTC')}")
    divider("═")

    # Current phase
    print("\n  CURRENT PHASE: Phase 0 — Execution Layer (PROVEN)")
    print("  NEXT PHASE:    Phase 1 — Intelligence Extraction")

    # Last session
    divider()
    print("LAST SESSION")
    divider()
    c.execute("""
        SELECT session_date, focus, completed, next_steps, notes
        FROM session_log
        ORDER BY id DESC LIMIT 1
    """)
    row = c.fetchone()
    if row:
        print(f"  Date:      {row[0]}")
        print(f"  Focus:     {row[1]}")
        print(f"  Completed: {row[2]}")
        print(f"  Next:      {row[3]}")
        if row[4]:
            print(f"  Notes:     {row[4]}")

    # Locked decisions
    divider()
    print("LOCKED DECISIONS")
    divider()
    c.execute("""
        SELECT decision_number, title
        FROM decisions
        WHERE status = 'locked'
        ORDER BY id ASC
    """)
    rows = c.fetchall()
    for r in rows:
        print(f"  [{r[0]}] {r[1]}")

    # Storage map
    divider()
    print("STORAGE MAP")
    divider()
    storage = [
        ("System disk  ", "/         ", "491GB", "OS and installed software"),
        ("Projects     ", "/mnt/projects", "246GB", "CIS project files"),
        ("Models       ", "/mnt/models  ", "229GB", "vLLM env + model weights"),
        ("Cache        ", "/mnt/cache   ", "110GB", "System cache"),
        ("Archive      ", "/mnt/archive ", "9.1TB", "Source material"),
    ]
    for s in storage:
        print(f"  {s[0]}  {s[1]}  {s[2]}  — {s[3]}")

    # Runtime status
    divider()
    print("RUNTIME")
    divider()
    print("  Extract env:  /home/eric/gpu-test")
    print("  Activate:    source /home/eric/gpu-test/bin/activate")
    print("  Model:       Qwen2.5-VL-32B-Instruct-4bit (transformers+bnb)")
    print("  HF_HOME:     /mnt/models/huggingface")
    print("  Ollama:      llava:latest, llama3:latest")

    # CIS tree
    divider()
    print("CIS PROJECT TREE")
    divider()
    print("  /mnt/projects/cis/")
    print("    memory/     — SQLite DB + harness scripts")
    print("    docs/       — all documentation")
    print("    ingest/     — source intake folders")
    print("    knowledge/  — knowledge records")
    print("    logs/       — system logs")
    print("    projects/   — creative project containers")
    print("    runtime/    — config, prompts, schemas, scripts")

    divider("═")
    print("  Ready. What are we building today?")
    divider("═")

    conn.close()

if __name__ == "__main__":
    load_context()
