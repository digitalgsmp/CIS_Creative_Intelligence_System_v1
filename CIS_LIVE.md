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

---
