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

---
