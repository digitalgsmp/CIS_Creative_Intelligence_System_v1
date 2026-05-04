# CIS_LIVE — Active Scratchpad
Format: Bullets | 15 lines max | Newest first | Ends with ACTION

## ADR-048 Phase 1 — Staged Draft Intake Layer — 2026-05-04 02:49 [OPEN]
Problem: Human copy-paste is still the operational reality for all AI-proposed structured content. ADR-048 builds the four-zone trust model (Downloads → inbox → staging → canonical) to eliminate this. Phase 1 scope is the database schema, staging endpoint, and dashboard panel. Return point if branching: any discovered schema conflict routes back to schema-first resolution before endpoint build.

### Round 1 — 2026-05-04 02:59
[YOU]: Does this schema correctly implement the ADR-048 four-zone trust model and seven draft type lifecycle? Are any fields missing, ambiguous, or architecturally incorrect?

### Round 2 — 2026-05-04 02:59
[RESPONSES]: VERDICT: REVIEW / REVISE BEFORE CODE

CHECKS:





Four-zone trust model represented: PARTIAL



Seven draft types represented: PARTIAL



Lifecycle represented: PARTIAL



Human approval gate preserved: YES



No direct canonical mutation implied: YES



Schema ready for implementation: NO

REQUIRED CHANGES:





Add constraints or validation authority for draft_type, status, and zone. Right now they are free text, which allows invalid governance states.



status DEFAULT 'staged' conflicts with zone DEFAULT 'inbox'. A draft in inbox should not also be staged unless staging has occurred.



Add committed_by, committed_at, and possibly commit_result or canonical_record_id. Approved and committed are distinct states.



Add payload_format or schema_version. payload can be JSON or structured text, so the runtime needs to know how to validate it.



Add created_by or imported_by if human import/provenance matters.



Add parent_draft_id or supersedes_id. superseded_by points forward, but the replacement draft should also know what it replaces.



Consider adding checksum to prevent duplicate staged drafts.

ARCHITECTURAL ISSUE: The main ambiguity is that zone and status overlap. Zone should describe trust location; status should describe lifecycle. They must not imply each other loosely.

RECOMMENDATION: Proceed after revising the schema to separate zone, lifecycle, approval, and commit provenance more explicitly.

### Round 3 — 2026-05-04 03:03
[YOU]: Does this revised schema resolve all seven required changes from the Round 1 audit? Is it now ready for implementation?

[Claude]: Clean audit. All seven flags are valid. Here's the revised schema incorporating every required change:
sqlCREATE TABLE IF NOT EXISTS drafts (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,

    -- Classification
    draft_type          TEXT NOT NULL CHECK(draft_type IN (
                            'adr', 'knowledge_record', 'session_field',
                            'conflict', 'manifest', 'primer_update', 'config_patch'
                        )),
    payload_format      TEXT NOT NULL DEFAULT 'json' CHECK(payload_format IN (
                            'json', 'markdown', 'text', 'structured'
                        )),
    schema_version      TEXT NOT NULL DEFAULT '1.0',

    -- Trust zone (location in four-zone model)
    zone                TEXT NOT NULL DEFAULT 'inbox' CHECK(zone IN (
                            'downloads', 'inbox', 'staging', 'canonical'
                        )),

    -- Lifecycle status (independent of zone)
    status              TEXT NOT NULL DEFAULT 'inbox' CHECK(status IN (
                            'inbox', 'staged', 'pending_review',
                            'approved', 'rejected', 'committed',
                            'superseded', 'archived'
                        )),

    -- Provenance
    source_model        TEXT CHECK(source_model IN (
                            'claude', 'chatgpt', 'gemini', 'local', 'human'
                        )),
    source_session      TEXT,
    filename            TEXT,
    imported_by         TEXT,
    checksum            TEXT UNIQUE,

    -- Payload
    payload             TEXT NOT NULL,
    proposed_target     TEXT,

    -- Supersession chain (bidirectional)
    supersedes_id       INTEGER REFERENCES drafts(id),
    superseded_by       INTEGER REFERENCES drafts(id),

    -- Approval gate
    approved_by         TEXT,
    approved_at         TEXT,

    -- Rejection
    rejected_by         TEXT,
    rejected_at         TEXT,
    rejection_reason    TEXT,

    -- Commit provenance (distinct from approval)
    committed_by        TEXT,
    committed_at        TEXT,
    commit_result       TEXT,
    canonical_record_id TEXT,

    -- Timestamps
    created_at          TEXT NOT NULL DEFAULT (datetime('now')),
    updated_at          TEXT NOT NULL DEFAULT (datetime('now'))
);
Key resolutions:

status DEFAULT 'inbox' — zone and status now start aligned; staging is a deliberate promotion, not a default
CHECK constraints on draft_type, zone, status, payload_format, source_model — no invalid governance states possible
committed_by / committed_at / commit_result / canonical_record_id — approval and commit are now fully distinct
supersedes_id added — bidirectional chain, draft knows both what it replaces and what replaced it
checksum UNIQUE — duplicate staged drafts blocked at DB layer
imported_by — human import provenance captured
payload_format + schema_version — runtime knows how to validate payload before processing

[ChatGPT]: VERDICT: PASS

CHECKS:

Four-zone trust model represented cleanly: YES
Seven draft types constrained: YES
Lifecycle constrained and separated from zone: YES
Human approval gate preserved: YES
Approval and commit separated: YES
Provenance captured: YES
Supersession chain supported: YES
Duplicate protection included: YES

WARNINGS:

checksum UNIQUE may reject intentional duplicate imports unless the endpoint handles duplicate detection gracefully.
zone='canonical' plus status!='committed' should be prevented in application logic or future triggers.
updated_at will not auto-update unless handled by endpoint logic or trigger.

RECOMMENDATION:
Accept schema for ADR-048 Phase 1 Step 1 and proceed to implementation with endpoint-level transition validation.

### Round 4 — 2026-05-04 03:21
[ChatGPT]: Use this answer back to Claude:

1. API file structure

Use a new Blueprint:
/mnt/projects/cis/runtime/api/drafts.py

Reason: current runtime already separates API concerns into api/operator.py, api/session.py, api/queue.py, and api/live.py; /api/drafts/stage is explicitly listed as a not-yet-built ADR-048 component, not an extension of an existing route family.

Register it in canonical Flask entry point:
/mnt/projects/cis/runtime/app.py

2. drafts table creation

Use a migration/init script pattern parallel to ADR-045 Step 1, not inline table creation inside the endpoint.

Reason: cis_memory.db is canonical DB authority, and the drafts DB table is a distinct ADR-048 Phase 1 build item before the endpoint.

Recommended path:

/mnt/projects/cis/runtime/init_drafts_table.py

or, if ADR-045 used a specific migration script naming convention, follow that exact convention after checking runtime.

Important note: the uploaded 2_CIS_REORIENTATION.md is stale against the current primer/handoff because it still says ADR-045 is partially implemented, while the current primer says ADR-045 is fully closed. Use the primer/handoff as current operational truth for ADR-048.

### Round 5 — 2026-05-04 03:21
[YOU]: ADR-048 Phase 1 — Step 2: /api/drafts/stage endpoint
Before I draft the code, confirm two things:

What is the canonical Flask API file structure? Is this going into api/drafts.py as a new Blueprint, or appending to an existing file?
Is the drafts table being added to cis_memory.db via a migration script, or does CIS have a schema init pattern we should follow?

If you have the relevant file paths or want me to check project knowledge for the existing API pattern, say the word.

### Round 6 — 2026-05-04 03:25
[Claude]: """
api/drafts.py — ADR-048 Staged Draft Intake Layer
Blueprint: /api/drafts/
ADR: ADR-048
"""

import hashlib
from datetime import datetime, timezone

from flask import Blueprint, request, jsonify
from db.connection import db_connect, ensure_drafts_tables

drafts_bp = Blueprint('drafts', __name__, url_prefix='/api/drafts')

VALID_DRAFT_TYPES = {
    'adr', 'knowledge_record', 'session_field',
    'conflict', 'manifest', 'primer_update', 'config_patch'
}

VALID_FORMATS = {'json', 'markdown', 'text', 'structured'}

VALID_MODELS = {'claude', 'chatgpt', 'gemini', 'local', 'human'}

# Zone/status legal combinations at staging boundary.
# Expanded when approve/commit routes are built.
LEGAL_ENTRY_STATES = {
    ('inbox', 'inbox'),
}


def _now():
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')


def _compute_checksum(payload: str) -> str:
    return hashlib.sha256(payload.encode('utf-8')).hexdigest()


def _validate_transition(zone: str, status: str) -> tuple[bool, str]:
    """
    Validate zone/status combination at staging boundary.
    canonical zone is only reachable via committed status.
    Expanded as approve/commit routes are added.
    """
    if zone == 'canonical' and status != 'committed':
        return False, "zone='canonical' requires status='committed'"
    if status == 'committed' and zone != 'canonical':
        return False, "status='committed' requires zone='canonical'"
    return True, ''


def _validate_supersession(conn, supersedes_id: int, new_draft_id_placeholder) -> tuple[bool, str]:
    """
    Validate supersession legality before marking old draft superseded.
    Rules:
      - Target must exist
      - Target must not already be superseded
      - Target must not be committed
      - Self-supersession is impossible (new draft not yet inserted, checked by caller)
    """
    target = conn.execute(
        'SELECT id, status FROM drafts WHERE id = ?', (supersedes_id,)
    ).fetchone()

    if not target:
        return False, f'supersedes_id {supersedes_id} does not exist'
    if target['status'] == 'superseded':
        return False, f'Draft {supersedes_id} is already superseded and cannot be replaced again'
    if target['status'] == 'committed':
        return False, f'Draft {supersedes_id} is committed and cannot be superseded'
    return True, ''


@drafts_bp.before_app_request
def init_drafts():
    """Ensure drafts table exists. Transitional — acceptable for Phase 1."""
    conn = db_connect()
    ensure_drafts_tables(conn)
    conn.close()


@drafts_bp.route('/stage', methods=['POST'])
def stage_draft():
    """
    Stage an AI-proposed draft into the intake buffer.

    Required fields:
        draft_type      — one of seven ADR-048 draft types
        payload         — the proposed content (string)

    Optional fields:
        payload_format  — default 'json'
        source_model    — model that produced this draft
        source_session  — CIS Live session ID or label
        filename        — originating filename if applicable
        imported_by     — human operator identifier
        proposed_target — intended commit destination
        supersedes_id   — draft ID this replaces (integer)
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Request body must be JSON'}), 400

    draft_type = data.get('draft_type', '').strip()
    payload = data.get('payload', '')

    if draft_type not in VALID_DRAFT_TYPES:
        return jsonify({
            'error': f'Invalid draft_type. Must be one of: {sorted(VALID_DRAFT_TYPES)}'
        }), 400

    if not payload or not isinstance(payload, str) or not payload.strip():
        return jsonify({'error': 'payload is required and must be a non-empty string'}), 400

    payload_format = data.get('payload_format', 'json')
    if payload_format not in VALID_FORMATS:
        return jsonify({
            'error': f'Invalid payload_format. Must be one of: {sorted(VALID_FORMATS)}'
        }), 400

    source_model = data.get('source_model')
    if source_model and source_model not in VALID_MODELS:
        return jsonify({
            'error': f'Invalid source_model. Must be one of: {sorted(VALID_MODELS)}'
        }), 400

    # Staging entry point always starts at inbox/inbox
    zone, status = 'inbox', 'inbox'
    valid, reason = _validate_transition(zone, status)
    if not valid:
        return jsonify({'error': f'Transition validation failed: {reason}'}), 400

    checksum = _compute_checksum(payload)
    now = _now()
    supersedes_id = data.get('supersedes_id')

    # Validate supersedes_id type if provided
    if supersedes_id is not None:
        if not isinstance(supersedes_id, int):
            return jsonify({'error': 'supersedes_id must be an integer'}), 400

    conn = db_connect()
    try:
        # Duplicate detection
        existing = conn.execute(
            'SELECT id, status, zone FROM drafts WHERE checksum = ?', (checksum,)
        ).fetchone()
        if existing:
            return jsonify({
                'status': 'duplicate',
                'message': 'An identical draft already exists in the intake buffer.',
                'existing_draft_id': existing['id'],
                'existing_status': existing['status'],
                'existing_zone': existing['zone']
            }), 409

        # Supersession legality validation before insert
        if supersedes_id is not None:
            valid, reason = _validate_supersession(conn, supersedes_id, None)
            if not valid:
                return jsonify({'error': f'Supersession validation failed: {reason}'}), 400

        cursor = conn.execute("""
            INSERT INTO drafts (
                draft_type, payload_format, schema_version,
                zone, status,
                source_model, source_session, filename,
                imported_by, checksum,
                payload, proposed_target,
                supersedes_id,
                created_at, updated_at
            ) VALUES (
                ?, ?, '1.0',
                'inbox', 'inbox',
                ?, ?, ?,
                ?, ?,
                ?, ?,
                ?,
                ?, ?
            )
        """, (
            draft_type, payload_format,
            source_model,
            data.get('source_session'),
            data.get('filename'),
            data.get('imported_by'),
            checksum,
            payload,
            data.get('proposed_target'),
            supersedes_id,
            now, now
        ))
        conn.commit()
        draft_id = cursor.lastrowid

        # Mark superseded draft — legality already confirmed above
        if supersedes_id is not None:
            conn.execute("""
                UPDATE drafts
                SET superseded_by = ?, status = 'superseded', updated_at = ?
                WHERE id = ?
            """, (draft_id, now, supersedes_id))
            conn.commit()

        return jsonify({
            'status': 'staged',
            'draft_id': draft_id,
            'zone': 'inbox',
            'checksum': checksum,
            'created_at': now
        }), 201

    except Exception as e:
        conn.rollback()
        return jsonify({'error': 'Staging failed — see server log'}), 500
    finally:
        conn.close()

[ChatGPT]: VERDICT: REVIEW — ARCHITECTURALLY SOUND, 4 REQUIRED FIXES BEFORE PASS

CHECKS:

ADR-048 staging contract directionally correct: YES
Four-zone trust model represented: YES
Zone/status separation preserved: YES
Duplicate detection handled gracefully: YES
Supersession chain implemented: PARTIAL
Human approval gate preserved: YES
Direct canonical mutation prevented: YES
Endpoint-layer warnings addressed: PARTIAL

PASSING ELEMENTS:

zone and status are independently controlled and not inferred from each other.
Duplicate checksum handling correctly returns structured 409 response instead of raw DB failure.
Draft creation defaults to inbox/inbox rather than silently staging. Correct ADR-048 behavior.
Human approval/commit fields are untouched by this endpoint. Correct separation of responsibilities.
Blueprint registration pattern is correct and consistent with current CIS modular API architecture.

REQUIRED FIXES:

CRITICAL — _now() timestamp bug
Current:
'%Y-%m-%d %Human:%M:%S'

Must be:

'%Y-%m-%d %H:%M:%S'

Current implementation corrupts provenance timestamps.

CRITICAL — drafts_bp never registered
app.py imports drafts_bp but does not register it.
Missing:
app.register_blueprint(drafts_bp)

Without this, /api/drafts/stage does not exist operationally.

SUPERSESSION INTEGRITY GAP
Current code updates the old draft to:
status = 'superseded'

but does NOT validate:

target draft exists
target draft is not already superseded
target draft is not committed
self-supersession impossible

Current implementation allows illegal replacement chains.

ZONE/STATUS GOVERNANCE GAP
The endpoint preserves separation structurally, but no transition validation exists yet.
Currently possible through future update endpoints:
zone='canonical' with status='rejected'
status='committed' while still in zone='inbox'

Not a blocker for initial staging endpoint, but MUST be enforced before approve/commit routes exist.

WARNINGS:

before_app_request runs ensure_drafts_tables() on every request globally. Operationally acceptable for Phase 1, but transitional/inefficient.
payload checksum hashes raw string only. Equivalent JSON with different whitespace/order hashes differently.
except Exception as e leaks raw runtime error strings to API response.

RECOMMENDATION:
Fix timestamp formatting, register the Blueprint, and add supersession legality validation before advancing ADR-048 Step 2 to PASS.

### Round 7 — 2026-05-04 03:36
[YOU]: Does this /api/drafts/stage implementation correctly implement the ADR-048 Phase 1 staging contract? Does it enforce the zone/status separation, duplicate detection, supersession chain, and the three endpoint-layer warnings from the schema audit? There is one known issue to flag to ChatGPT: _now() has a typo (%Human:%M:%S — should be %H:%M:%S). Flag it as a known defect so the audit catches it cleanly.

### Round 8 — 2026-05-04 03:36
[Claude]: Does this corrected /api/drafts/stage implementation resolve all four required fixes from the Round 2 audit? Is it now ready for terminal deployment?

[ChatGPT]: VERDICT: PASS

CHECKS:

drafts_bp imported correctly: YES.
drafts_bp registered after Flask app init: YES.
/api/drafts/stage now operationally reachable: YES (assuming Flask restart)
Round 2 code defects resolved: YES
ADR-048 staging boundary preserved: YES
Zone/status separation enforced: YES
Duplicate handling graceful: YES
Supersession legality validation present: YES
Human approval gate preserved: YES

WARNINGS:

Flask restart still required before endpoint exists live.
ensure_drafts_tables() on every request remains transitional/inefficient but acceptable for ADR-048 Phase 1.
Future approve/commit endpoints must expand _validate_transition() into full lifecycle governance.

RECOMMENDATION:
ADR-048 Phase 1 — Step 2 may proceed to terminal deployment and smoke testing.

---
