# CIS_LIVE — Active Scratchpad
Format: Bullets | 15 lines max | Newest first | Ends with ACTION

## ADR-048 Phase 1 — Staged Draft Intake Layer — 2026-05-04 02:49 [OPEN]
Problem: Human copy-paste is still the operational reality for all AI-proposed structured content. ADR-048 builds the four-zone trust model (Downloads → inbox → staging → canonical) to eliminate this. Phase 1 scope is the database schema, staging endpoint, and dashboard panel. Return point if branching: any discovered schema conflict routes back to schema-first resolution before endpoint build.

### Round 1 — 2026-05-04 02:59
[YOU]: Does this schema correctly implement the ADR-048 four-zone trust model and seven draft type lifecycle? Are any fields missing, ambiguous, or architecturally incorrect?

---
