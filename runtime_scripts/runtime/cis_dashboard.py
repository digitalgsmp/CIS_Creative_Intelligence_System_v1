#!/usr/bin/env python3
"""
cis_dashboard.py — CIS Operator Dashboard v2
Flask backend with URL-based project routing.

Routes:
    /                          Project Launcher
    /project/<project_id>      Project workspace
    /project/<project_id>/<panel>  Specific panel

Usage:
    python3 /mnt/projects/cis/runtime/cis_dashboard.py

Access:
    http://localhost:5000
"""

import json
import sqlite3
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from flask import Flask, jsonify, request, send_from_directory

app = Flask(__name__, static_folder=None)

# ── Paths ──────────────────────────────────────────────────────────────────────
PROJECTS_ROOT = Path("/mnt/projects/cis")
RECORDS_ROOT  = PROJECTS_ROOT / "knowledge" / "records"
INGEST_ROOT   = PROJECTS_ROOT / "ingest" / "processing"
PROJECTS_DIR  = PROJECTS_ROOT / "projects"
DB_PATH       = PROJECTS_ROOT / "memory" / "cis_memory.db"
RUNTIME_DIR   = PROJECTS_ROOT / "runtime"
HARNESS_PATH  = PROJECTS_ROOT / "memory" / "cis_harness.py"
VAULT_DIR     = PROJECTS_ROOT / "docs" / "CIS_Creative_Intelligence_System_v1"

EXTRACT_CMD = (
    "PYTORCH_ALLOC_CONF=expandable_segments:True "
    "/home/eric/gpu-test/bin/python3 "
    "/mnt/projects/cis/runtime/cis_extract.py"
)

WIAS_STAGES = ["word", "image", "action", "sound", "web"]

# ── Helpers ────────────────────────────────────────────────────────────────────

def ts():
    return datetime.now(timezone.utc).isoformat()

def today():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d")

def db_connect():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

def run_command(cmd, timeout=300):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "returncode": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "stdout": "", "stderr": "Command timed out", "returncode": -1}
    except Exception as e:
        return {"success": False, "stdout": "", "stderr": str(e), "returncode": -1}

def ensure_tables(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS insights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            observation TEXT NOT NULL,
            source_record_id TEXT,
            project_id TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            command TEXT,
            phase TEXT,
            project_id TEXT,
            priority INTEGER DEFAULT 5,
            status TEXT DEFAULT 'open',
            created_at TEXT NOT NULL,
            completed_at TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS captures (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            capture_type TEXT NOT NULL,
            title TEXT NOT NULL,
            observation TEXT NOT NULL,
            source_record_id TEXT,
            project_id TEXT,
            created_at TEXT NOT NULL
        )
    """)
    conn.commit()

def get_all_projects():
    projects = []
    if not PROJECTS_DIR.exists():
        return projects
    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir():
            continue
        for project_file in project_dir.glob("*.json"):
            try:
                p = load_json(project_file)
                record_count = 0
                for r in RECORDS_ROOT.rglob("*.json"):
                    try:
                        rec = load_json(r)
                        if rec.get("project_id") == p.get("project_id"):
                            record_count += 1
                    except Exception:
                        pass
                p["_record_count"] = record_count
                projects.append(p)
            except Exception:
                pass
    return projects

def get_project(project_id):
    if not PROJECTS_DIR.exists():
        return None, None
    for project_dir in PROJECTS_DIR.iterdir():
        if not project_dir.is_dir():
            continue
        for project_file in project_dir.glob("*.json"):
            try:
                p = load_json(project_file)
                if p.get("project_id") == project_id:
                    return p, project_file
            except Exception:
                pass
    return None, None

def compute_wias_progress(project_id, project):
    active_stages = [s.lower() for s in project.get("active_stages", [])]
    progress = {s: 0 for s in WIAS_STAGES}
    for stage in active_stages:
        if stage in progress:
            progress[stage] = max(progress[stage], 1)
    if not RECORDS_ROOT.exists():
        return progress
    for record_dir in RECORDS_ROOT.iterdir():
        if not record_dir.is_dir():
            continue
        for record_file in record_dir.glob("*.json"):
            try:
                rec = load_json(record_file)
                if rec.get("project_id") != project_id:
                    continue
                status = rec.get("status", "")
                for stage in (rec.get("active_stages") or []):
                    stage = stage.lower()
                    if stage not in progress:
                        continue
                    if status == "draft":
                        progress[stage] = max(progress[stage], 2)
                    elif status == "checked":
                        progress[stage] = max(progress[stage], 3)
                    elif status in ("approved", "locked"):
                        progress[stage] = max(progress[stage], 4)
            except Exception:
                pass
    return progress

# ── Frontend Routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(str(RUNTIME_DIR), "cis_dashboard.html")

@app.route("/project/<project_id>")
@app.route("/project/<project_id>/<panel>")
def project_view(project_id, panel="overview"):
    return send_from_directory(str(RUNTIME_DIR), "cis_dashboard.html")

# ── API: System ────────────────────────────────────────────────────────────────

@app.route("/api/status")
def api_status():
    record_count  = sum(1 for _ in RECORDS_ROOT.rglob("*.json")) if RECORDS_ROOT.exists() else 0
    project_count = len(get_all_projects())
    conn = db_connect()
    ensure_tables(conn)
    open_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='open'").fetchone()[0]
    conn.close()
    return jsonify({
        "status": "online",
        "timestamp": ts(),
        "counts": {
            "records": record_count,
            "projects": project_count,
            "open_tasks": open_tasks
        }
    })

# ── API: Projects ──────────────────────────────────────────────────────────────

@app.route("/api/projects")
def api_projects():
    return jsonify(get_all_projects())

@app.route("/api/projects", methods=["POST"])
def api_create_project():
    data          = request.get_json()
    title         = data.get("title", "").strip()
    concept       = data.get("concept", "").strip()
    output_type   = data.get("intended_output_type", "").strip()
    scope         = data.get("project_scope", "minor")
    active_stages = data.get("active_stages", ["word"])
    if not title:
        return jsonify({"success": False, "error": "title is required"}), 400
    slug       = title.upper().replace(" ", "_").replace("-", "_")[:40]
    project_id = f"PROJECT__{slug}__V1"
    project = {
        "project_id":           project_id,
        "project_type":         data.get("project_type", "creative"),
        "title":                title,
        "working_title":        title,
        "created_at":           ts(),
        "updated_at":           ts(),
        "created_by":           "human",
        "status":               "active",
        "concept":              concept,
        "intended_output_type": output_type,
        "project_scope":        scope,
        "active_stages":        active_stages,
        "knowledge_links":      {"record_ids": [], "research_ids": [], "reference_ids": [], "learning_ids": [], "template_ids": []},
        "version":              "v1",
        "is_current":           True
    }
    project_dir = PROJECTS_DIR / project_id
    project_dir.mkdir(parents=True, exist_ok=True)
    save_json(project_dir / f"{project_id.lower()}.json", project)
    return jsonify({"success": True, "project_id": project_id, "project": project})

@app.route("/api/projects/<project_id>")
def api_project_detail(project_id):
    project, _ = get_project(project_id)
    if not project:
        return jsonify({"error": "Project not found"}), 404
    project["_wias_progress"] = compute_wias_progress(project_id, project)
    return jsonify(project)

# ── API: Session ───────────────────────────────────────────────────────────────

@app.route("/api/session/start", methods=["POST"])
def api_session_start():
    result = run_command(f"python3 {HARNESS_PATH}", timeout=30)
    return jsonify(result)

@app.route("/api/session/close", methods=["POST"])
def api_session_close():
    data       = request.get_json()
    focus      = data.get("focus", "").strip()
    completed  = data.get("completed", "").strip()
    next_steps = data.get("next_steps", "").strip()
    notes      = data.get("notes", "").strip()
    if not focus or not completed or not next_steps:
        return jsonify({"success": False, "error": "focus, completed, and next_steps are required"}), 400

    results  = {}
    step_log = []

    # ── Step 1: Write session record to DB ────────────────────────────────────
    conn = db_connect()
    ensure_tables(conn)
    try:
        conn.execute(
            "INSERT INTO session_log (session_date, focus, completed, next_steps, notes, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (today(), focus, completed, next_steps, notes, ts())
        )
        conn.commit()
        results["session_logged"] = True
        step_log.append("✓ Session logged to database")
    except Exception as e:
        results["session_logged"] = False
        results["session_error"] = str(e)
        step_log.append(f"✗ Session log failed: {e}")

    # ── Step 2: Regenerate ADRs.md from decisions table ───────────────────────
    try:
        rows = conn.execute(
            "SELECT decision_number, title, description, rationale, status, created_at "
            "FROM decisions ORDER BY id ASC"
        ).fetchall()
        adrs_lines = [
            "# CIS Architecture Decision Records",
            f"Last updated: {today()}",
            "---",
        ]
        for r in rows:
            adrs_lines += [
                f"## {r['decision_number']} — {r['title']}",
                f"**Status:** {r['status'].capitalize()}",
                f"**Decision:** {r['description']}",
                f"**Rationale:** {r['rationale']}",
                "---",
            ]
        adrs_path = VAULT_DIR / "Phase_PD" / "ADRs.md"
        adrs_path.write_text("\n".join(adrs_lines), encoding="utf-8")
        results["adrs_regenerated"] = True
        step_log.append(f"✓ ADRs.md regenerated ({len(rows)} decisions)")
    except Exception as e:
        results["adrs_error"] = str(e)
        step_log.append(f"✗ ADRs.md failed: {e}")

    conn.close()

    # ── Step 3: Sync knowledge records to vault ───────────────────────────────
    try:
        kr_vault = VAULT_DIR / "knowledge_records"
        kr_vault.mkdir(exist_ok=True)
        result = run_command(f"cp -r {RECORDS_ROOT}/. {kr_vault}/", timeout=30)
        if result["success"]:
            step_log.append("✓ Knowledge records synced to vault")
        else:
            step_log.append(f"✗ Knowledge records sync failed: {result['stderr']}")
    except Exception as e:
        step_log.append(f"✗ Knowledge records sync error: {e}")

    # ── Step 4: Sync projects folder to vault ─────────────────────────────────
    try:
        proj_vault = VAULT_DIR / "projects"
        proj_vault.mkdir(exist_ok=True)
        result = run_command(f"cp -r {PROJECTS_DIR}/. {proj_vault}/", timeout=30)
        if result["success"]:
            step_log.append("✓ Projects folder synced to vault")
        else:
            step_log.append(f"✗ Projects sync failed: {result['stderr']}")
    except Exception as e:
        step_log.append(f"✗ Projects sync error: {e}")

    # ── Step 5: Sync runtime scripts to vault ─────────────────────────────────
    try:
        mem_vault  = VAULT_DIR / "runtime_scripts" / "memory"
        run_vault  = VAULT_DIR / "runtime_scripts" / "runtime"
        mem_vault.mkdir(parents=True, exist_ok=True)
        run_vault.mkdir(parents=True, exist_ok=True)
        r1 = run_command(f"cp {PROJECTS_ROOT}/memory/cis_harness.py {mem_vault}/", timeout=15)
        r2 = run_command(f"cp {PROJECTS_ROOT}/memory/cis_log.py {mem_vault}/", timeout=15)
        r3 = run_command(f"cp {PROJECTS_ROOT}/memory/create_db.py {mem_vault}/", timeout=15)
        r4 = run_command(f"cp {RUNTIME_DIR}/cis_intake.py {run_vault}/", timeout=15)
        r5 = run_command(f"cp {RUNTIME_DIR}/cis_classify.py {run_vault}/", timeout=15)
        r6 = run_command(f"cp {RUNTIME_DIR}/cis_preprocess.py {run_vault}/", timeout=15)
        r7 = run_command(f"cp {RUNTIME_DIR}/cis_extract.py {run_vault}/", timeout=15)
        r8 = run_command(f"cp {RUNTIME_DIR}/cis_normalize.py {run_vault}/", timeout=15)
        r9 = run_command(f"cp {RUNTIME_DIR}/cis_review.py {run_vault}/", timeout=15)
        r10 = run_command(f"cp {RUNTIME_DIR}/cis_dashboard.py {run_vault}/", timeout=15)
        r11 = run_command(f"cp {RUNTIME_DIR}/cis_dashboard.html {run_vault}/", timeout=15)
        step_log.append("✓ Runtime scripts synced to vault")
    except Exception as e:
        step_log.append(f"✗ Runtime scripts sync error: {e}")

    # ── Step 6: Append to system_log.md ──────────────────────────────────────
    try:
        system_log_path = PROJECTS_ROOT / "logs" / "system_log.md"
        entry = (
            f"\n## {ts()[:16].replace('T', ' ')} UTC — SESSION CLOSE\n"
            f"- Focus: {focus}\n"
            f"- Completed: {completed[:120]}{'...' if len(completed) > 120 else ''}\n"
            f"- Next: {next_steps[:120]}{'...' if len(next_steps) > 120 else ''}\n"
        )
        with open(system_log_path, "a", encoding="utf-8") as f:
            if system_log_path.stat().st_size == 0 if system_log_path.exists() else True:
                f.write("# CIS System Log\nAppend-only record of all system actions.\n\n")
            f.write(entry)
        step_log.append("✓ system_log.md updated")
    except Exception as e:
        step_log.append(f"✗ system_log.md failed: {e}")

    # ── Step 7: Write handoff markdown ────────────────────────────────────────
    handoff_content = f"""# CIS Session Handoff
## Date: {today()}

## Session Focus
{focus}

## Completed
{completed}

## Next Steps
{next_steps}

## Notes
{notes or '—'}

## Sync Status
{chr(10).join(step_log)}

## How to start next session
Run on Ubuntu VM:
```
cis-start
```
Paste output as first message in new chat along with this handoff document.
"""
    handoff_filename = f"CIS_Handoff_{today()}.md"
    handoff_path = VAULT_DIR / "Phase_PD" / handoff_filename
    try:
        handoff_path.write_text(handoff_content, encoding="utf-8")
        results["handoff_written"] = str(handoff_path)
        step_log.append("✓ Handoff document written")
    except Exception as e:
        results["handoff_error"] = str(e)
        step_log.append(f"✗ Handoff write failed: {e}")

    results["handoff_content"] = handoff_content

    # ── Step 8: Git commit and push ───────────────────────────────────────────
    git_cmd = (
        f"cd {VAULT_DIR} && git add -A && "
        f"git commit -m 'Session close: {focus}' && git push"
    )
    git_result = run_command(git_cmd, timeout=60)
    results["git"] = git_result
    if git_result["success"]:
        step_log.append("✓ Git committed and pushed")
    else:
        # Nothing to commit is not a real error
        if "nothing to commit" in git_result["stdout"] + git_result["stderr"]:
            step_log.append("✓ Git — nothing new to commit")
            results["git"]["success"] = True
        else:
            step_log.append(f"✗ Git failed: {git_result['stderr']}")

    results["step_log"] = step_log
    results["success"]  = True
    return jsonify(results)

@app.route("/api/session/recent")
def api_session_recent():
    conn = db_connect()
    try:
        rows = conn.execute(
            "SELECT session_date, focus, completed, next_steps, notes, created_at "
            "FROM session_log ORDER BY id DESC LIMIT 5"
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception:
        return jsonify([])
    finally:
        conn.close()

# ── API: Tasks ─────────────────────────────────────────────────────────────────

@app.route("/api/tasks")
def api_tasks_get():
    project_id = request.args.get("project_id")
    conn = db_connect()
    ensure_tables(conn)
    try:
        if project_id:
            rows = conn.execute(
                "SELECT * FROM tasks WHERE project_id=? ORDER BY priority ASC, created_at ASC",
                (project_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM tasks ORDER BY priority ASC, created_at ASC"
            ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()

@app.route("/api/tasks", methods=["POST"])
def api_tasks_post():
    data       = request.get_json()
    title      = data.get("title", "").strip()
    desc       = data.get("description", "").strip()
    command    = data.get("command", "").strip() or None
    phase      = data.get("phase", "").strip() or None
    project_id = data.get("project_id", "").strip() or None
    priority   = int(data.get("priority", 5))
    if not title:
        return jsonify({"success": False, "error": "title is required"}), 400
    conn = db_connect()
    ensure_tables(conn)
    try:
        conn.execute(
            "INSERT INTO tasks (title, description, command, phase, project_id, priority, status, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, 'open', ?)",
            (title, desc, command, phase, project_id, priority, ts())
        )
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/tasks/<int:task_id>/complete", methods=["POST"])
def api_task_complete(task_id):
    conn = db_connect()
    ensure_tables(conn)
    try:
        conn.execute(
            "UPDATE tasks SET status='complete', completed_at=? WHERE id=?",
            (ts(), task_id)
        )
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

@app.route("/api/tasks/<int:task_id>/run", methods=["POST"])
def api_task_run(task_id):
    conn = db_connect()
    ensure_tables(conn)
    try:
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if not row:
            return jsonify({"success": False, "error": "Task not found"}), 404
        task = dict(row)
        if not task.get("command"):
            return jsonify({"success": False, "error": "No command defined for this task"}), 400
        result = run_command(task["command"])
        if result["success"]:
            conn.execute(
                "UPDATE tasks SET status='complete', completed_at=? WHERE id=?",
                (ts(), task_id)
            )
            conn.commit()
        return jsonify(result)
    finally:
        conn.close()

# ── API: Pipeline ──────────────────────────────────────────────────────────────

@app.route("/api/intake", methods=["POST"])
def api_intake():
    data      = request.get_json()
    file_path = data.get("path", "").strip()
    if not file_path:
        return jsonify({"success": False, "error": "No path provided"}), 400
    result = run_command(f"python3 {RUNTIME_DIR}/cis_intake.py '{file_path}'")
    return jsonify(result)

@app.route("/api/pipeline/<action>", methods=["POST"])
def api_pipeline(action):
    data      = request.get_json()
    source_id = data.get("source_id", "").strip()
    if not source_id:
        return jsonify({"success": False, "error": "No source_id provided"}), 400
    commands = {
        "classify":   f"python3 {RUNTIME_DIR}/cis_classify.py '{source_id}'",
        "preprocess": f"python3 {RUNTIME_DIR}/cis_preprocess.py '{source_id}'",
        "extract":    f"{EXTRACT_CMD} '{source_id}'",
        "normalize":  f"python3 {RUNTIME_DIR}/cis_normalize.py '{source_id}'",
    }
    if action not in commands:
        return jsonify({"success": False, "error": f"Unknown action: {action}"}), 400
    result = run_command(commands[action])
    manifest_path = INGEST_ROOT / source_id.lower() / "manifest.json"
    if manifest_path.exists():
        try:
            manifest = load_json(manifest_path)
            result["manifest_status"] = manifest.get("status", "unknown")
        except Exception:
            pass
    return jsonify(result)

@app.route("/api/pipeline/status/<source_id>")
def api_pipeline_status(source_id):
    manifest_path = INGEST_ROOT / source_id.lower() / "manifest.json"
    if not manifest_path.exists():
        return jsonify({"found": False}), 404
    try:
        manifest = load_json(manifest_path)
        return jsonify({
            "found": True,
            "source_id": source_id,
            "status": manifest.get("status"),
            "source_name": manifest.get("source_name"),
            "history": manifest.get("history", [])
        })
    except Exception as e:
        return jsonify({"found": False, "error": str(e)}), 500

# ── API: Records ───────────────────────────────────────────────────────────────

@app.route("/api/records")
def api_records():
    project_id    = request.args.get("project_id")
    status_filter = request.args.get("status")
    records = []
    if not RECORDS_ROOT.exists():
        return jsonify([])
    for record_dir in sorted(RECORDS_ROOT.iterdir()):
        if not record_dir.is_dir():
            continue
        for record_file in sorted(record_dir.glob("*.json")):
            try:
                record = load_json(record_file)
                if project_id and record.get("project_id") != project_id:
                    continue
                if status_filter and record.get("status") != status_filter:
                    continue
                records.append({
                    "record_id":          record.get("record_id", record_file.stem),
                    "title":              record.get("title", ""),
                    "status":             record.get("status", ""),
                    "knowledge_category": record.get("knowledge_category", ""),
                    "project_id":         record.get("project_id"),
                    "active_stages":      record.get("active_stages", []),
                    "created_at":         record.get("created_at", ""),
                    "updated_at":         record.get("updated_at", ""),
                })
            except Exception:
                pass
    return jsonify(records)

@app.route("/api/records/<path:record_id>")
def api_record_detail(record_id):
    for record_dir in RECORDS_ROOT.iterdir():
        if not record_dir.is_dir():
            continue
        for record_file in record_dir.glob("*.json"):
            try:
                record = load_json(record_file)
                if record.get("record_id") == record_id:
                    return jsonify(record)
            except Exception:
                pass
    return jsonify({"error": "Record not found"}), 404

# ── API: Captures ──────────────────────────────────────────────────────────────

@app.route("/api/captures", methods=["GET"])
def api_captures_get():
    project_id = request.args.get("project_id")
    conn = db_connect()
    ensure_tables(conn)
    try:
        if project_id:
            rows = conn.execute(
                "SELECT * FROM captures WHERE project_id=? ORDER BY id DESC LIMIT 50",
                (project_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM captures ORDER BY id DESC LIMIT 50"
            ).fetchall()
        return jsonify([dict(r) for r in rows])
    finally:
        conn.close()

@app.route("/api/captures", methods=["POST"])
def api_captures_post():
    data         = request.get_json()
    capture_type = data.get("capture_type", "insight").strip()
    title        = data.get("title", "").strip()
    observation  = data.get("observation", "").strip()
    source       = data.get("source_record_id", "").strip() or None
    project_id   = data.get("project_id", "").strip() or None
    if not title or not observation:
        return jsonify({"success": False, "error": "title and observation are required"}), 400
    conn = db_connect()
    ensure_tables(conn)
    try:
        conn.execute(
            "INSERT INTO captures (capture_type, title, observation, source_record_id, project_id, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (capture_type, title, observation, source, project_id, ts())
        )
        if capture_type == "insight":
            conn.execute(
                "INSERT INTO insights (category, title, observation, source_record_id, project_id, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?)",
                ("workflow", title, observation, source, project_id, ts())
            )
        conn.commit()
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
    finally:
        conn.close()

# ── API: Decisions ─────────────────────────────────────────────────────────────

@app.route("/api/decisions")
def api_decisions():
    conn = db_connect()
    try:
        rows = conn.execute(
            "SELECT decision_number, title, description, rationale, status, created_at "
            "FROM decisions ORDER BY id ASC"
        ).fetchall()
        return jsonify([dict(r) for r in rows])
    except Exception:
        return jsonify([])
    finally:
        conn.close()

# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═" * 60)
    print("  CIS Dashboard v2")
    print("  http://localhost:5000")
    print("═" * 60)
    app.run(host="0.0.0.0", port=5000, debug=False)
