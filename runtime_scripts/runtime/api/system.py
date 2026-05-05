"""
api/system.py — System status endpoint.
Route: GET /api/status
"""

from flask import Blueprint, jsonify
from config import RECORDS_ROOT
from db.connection import db_connect, ensure_tables, ensure_phase1_tables
from utils.helpers import ts
from utils.project_helpers import get_all_projects

system_bp = Blueprint("system", __name__)


@system_bp.route("/api/status")
def api_status():
    record_count  = sum(1 for _ in RECORDS_ROOT.rglob("*.json")) if RECORDS_ROOT.exists() else 0
    project_count = len(get_all_projects())

    conn = db_connect()
    ensure_tables(conn)
    ensure_phase1_tables(conn)
    open_tasks = conn.execute("SELECT COUNT(*) FROM tasks WHERE status='open'").fetchone()[0]
    conn.close()

    return jsonify({
        "status":    "online",
        "timestamp": ts(),
        "counts": {
            "records":    record_count,
            "projects":   project_count,
            "open_tasks": open_tasks
        }
    })
