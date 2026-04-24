# CIS_LIVE — Active Scratchpad
Format: Bullets | 15 lines max | Newest first | Ends with ACTION

## Phase 1 Open — Segment canonical object + PySceneDetect — 2026-04-24 02:04 [OPEN]
Problem: Phase 0 exit criteria met. Phase 1 begins now. Build target is: (1) write ADR-031, (2) define Segment schema + DB table, (3) install and smoke-test PySceneDetect. Expected return point to main path: Segment defined, scene detection confirmed functional, batch extraction design begun.

### Round 1 — 2026-04-24 03:56
[YOU]: extraction quality requires finer granularity than a full scene. if this will be discovered when the knowledge records are trying to be used in real time, this is too late because we would go from ready to use CIS back to developing CIS.

### Round 2 — 2026-04-24 03:56
[RESPONSES]: Scene detection is the primary segmentation method. A duration-based fallback split is required for segments or source units exceeding a defined threshold. Segmentation policy (thresholds, merge floor, quality gate criteria) is defined and validated before extraction scales.

### Round 3 — 2026-04-24 03:58
[YOU]: CIS scope expanded from creative production to full life and creation management system

---
