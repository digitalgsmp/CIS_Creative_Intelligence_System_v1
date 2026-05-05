#!/usr/bin/env python3
"""
app.py — CIS Dashboard entry point.
Initialises Flask, registers all API blueprints, serves the frontend.

Usage:
    python3 /mnt/projects/cis/runtime/app.py

Access:
    http://localhost:5000
"""

from flask import Flask, jsonify, send_from_directory
from config import RUNTIME_DIR

# ── Blueprint imports ──────────────────────────────────────────────────────────
from api.system          import system_bp
from api.projects        import projects_bp
from api.session         import session_bp
from api.tasks           import tasks_bp
from api.pipeline        import pipeline_bp
from api.records         import records_bp
from api.captures        import captures_bp
from api.decisions       import decisions_bp
from api.extraction_runs import extraction_runs_bp
from api.live            import live_bp
from api.models          import models_bp
from api.operator        import operator_bp          # ADR-044
from api.queue           import queue_bp             # ADR-045
from api.drafts import drafts_bp


# ── Worker import ──────────────────────────────────────────────────────────────
from queue_worker import start_worker, worker_status  # ADR-045


# ── App init ───────────────────────────────────────────────────────────────────
app = Flask(__name__, static_folder=None)

# ── Register blueprints ────────────────────────────────────────────────────────
app.register_blueprint(system_bp)
app.register_blueprint(projects_bp)
app.register_blueprint(session_bp)
app.register_blueprint(tasks_bp)
app.register_blueprint(pipeline_bp)
app.register_blueprint(records_bp)
app.register_blueprint(captures_bp)
app.register_blueprint(decisions_bp)
app.register_blueprint(extraction_runs_bp)
app.register_blueprint(live_bp)
app.register_blueprint(models_bp)
app.register_blueprint(operator_bp)                 # ADR-044
app.register_blueprint(queue_bp)                    # ADR-045
app.register_blueprint(drafts_bp)

# ── Worker status route ────────────────────────────────────────────────────────

@app.route("/api/queue/worker-status")
def api_worker_status():
    """Return current queue worker state. Used by dashboard polling."""
    return jsonify(worker_status())

# ── Frontend routes ────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory(str(RUNTIME_DIR), "cis_dashboard.html")

@app.route("/project/<project_id>")
@app.route("/project/<project_id>/<panel>")
def project_view(project_id, panel="overview"):
    return send_from_directory(str(RUNTIME_DIR), "cis_dashboard.html")

# ── Run ────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("═" * 60)
    print("  CIS Dashboard — Modular Backend")
    print("  http://localhost:5000")
    print("═" * 60)
    start_worker()                                   # ADR-045 — queue worker
    app.run(host="0.0.0.0", port=5000, debug=False)
