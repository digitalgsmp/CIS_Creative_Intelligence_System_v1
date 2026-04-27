# CIS_LIVE — Active Scratchpad
Format: Bullets | 15 lines max | Newest first | Ends with ACTION

## Verification UI gap — no dashboard surface for verification status — 2026-04-26 22:56 [OPEN]
Problem: cis_verify.py is operational but verification is terminal-only. The dashboard has no way to view the verification log, submit manifests, or see pass/fail status on pipeline actions. As Phase 1 produces real output, verification becomes load-bearing. A UI surface is needed before the verification layer can be considered production-ready. This is a branch observation — not blocking the intake run, expected return point is after Phase 1 intake is proven.
Tags: verification, phase-1, ui, adr-033

---
