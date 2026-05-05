# CIS_LIVE — Active Scratchpad
Format: Bullets | 15 lines max | Newest first | Ends with ACTION

## ADR-048 Phase 2 — cis_download_watcher.py build — 2026-05-05 01:15 [OPEN]
Problem: ADR-048 Phase 1 is operational (drafts table, /api/drafts/stage, list/action routes, DraftIntakePanel). Phase 2 goal is a filesystem watcher that automates Downloads → inbox transport, eliminating the manual staging step. Expected return point: watcher deployed, verified, human no longer manually stages downloaded files.

### Round 1 — 2026-05-05 01:51
[YOU]: Architectural insight — log to CIS Live before we lose it

[RESPONSES]: Insight: The apparent ADR-048 primer contradiction is not a hard conflict — it is an under-specified state taxonomy. The current coarse status vocabulary (PRE-DRAFT / OPERATIONAL / LOCKED / NOT YET BUILT) cannot express hierarchical implementation state (ADR overall vs. phase vs. build step). This is a normal maturation symptom. The long-term solution is a governed State Registry layer: ADRs, components, build phases, and creative project phases stored as structured state, with primer files and handoffs rendered from that registry rather than manually maintained as prose. Drift detection, phase-aware status taxonomy, and inheritance integrity checking are all expressions of the same missing layer. This belongs in the build-plan reconstruction stage, not ADR-048 Phase 2. Do not interrupt current build sequence.

---
