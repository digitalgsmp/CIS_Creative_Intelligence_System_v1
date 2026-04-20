# MEMORY.md — Additions
# Append these entries to X_02_MEMORY.md

---

## Parking Lot — Application Layer Future Features

### Feature: Cloudflare Tunnel — Full Remote Dashboard Access

**Concept:**
The Cloudflare Tunnel currently serving CIS_LIVE.md can be extended to expose
the full CIS Flask dashboard (localhost:5000) via a public URL.

This would allow:
- Full dashboard access from any browser, any device, any location
- Field access during downtime — review records, approve knowledge objects,
  trigger pipeline jobs on the VM remotely
- The VM handles all compute; the browser is just the interface

**Current state:** Tunnel serves CIS_LIVE.md only.
**Prerequisite:** Stable modular backend (now complete).
**Deferred because:** Remote access architecture needs security review before exposing
the full app externally. Authentication layer required before activation.

---

### Feature: CIS_LIVE — Auto-fetch Model Responses

**Concept:**
Rather than manually pasting each model's response into the Live panel, the panel
could fetch responses from a shared URL if a model exposes a public conversation link.

**Current state:** Not viable — major models (Claude, Gemini, ChatGPT) do not
expose stable public share URLs suitable for programmatic fetch.

**Manual paste remains the correct approach** until model APIs or share features
make this practical.

**Deferred because:** No reliable fetch target exists today.

---

### Feature: CIS_LIVE — QR Code / Shareable URL Display

**Concept:**
The Live panel displays the current Cloudflare raw URL for CIS_LIVE.md as a
copyable link and optionally as a QR code. Allows opening the live scratchpad
on a second device (phone, tablet) mid-session without typing the URL.

**Current state:** URL is returned by the push endpoint but not displayed in UI.
**Deferred because:** UI not yet built. Low effort — add in next Live panel iteration.

---

### Feature: Remote Field Access Workflow

**Concept:**
When working in the field with downtime, operator opens CIS dashboard via
Cloudflare URL on phone or laptop. Actions available remotely:
- Review and approve knowledge records
- Open and log CIS_LIVE sessions
- View project state and pipeline status
- Trigger lightweight pipeline jobs (classify, normalize)

Heavy compute jobs (extract with 32B model) remain VM-only due to GPU requirement.

**Prerequisite:** Cloudflare full tunnel + authentication layer.
**Deferred because:** Authentication design not yet started.

---

## Decision Log Additions

### Decision 070

CIS dashboard backend has been refactored from a single monolithic file
into a modular structure.

**Structure:**
- app.py — entry point and blueprint registration
- config.py — all paths and constants
- api/ — one module per route group (10 modules)
- db/ — connection factory and live_db separately
- utils/ — shared helpers and project helpers

**Why:**
- single file was becoming unmanageable
- modular structure allows individual features to be modified in isolation
- aligns with sequential build principle — each capability can now be
  stabilized and tested independently

---

### Decision 071

CIS_LIVE panel is the designated UI location for multi-model scratchpad sessions.

The Session deck keys (Start / Close / Handoff) handle session lifecycle.
The Live tab in the workspace handles active problem-solving rounds.

These are distinct functions sharing a conceptual relationship:
- Session = the outer container for a day's work
- Live = the real-time problem-solving tool that runs inside it

**Why:**
Conflating session management with live scratchpad would create an overloaded
interface. Separation keeps each surface focused.

---

### Decision 072

Manual paste is the confirmed input method for CIS_LIVE model responses.

Auto-fetch from model share URLs is deferred (no reliable targets exist).
The Live panel is designed around fast paste targets for each model slot,
not programmatic response retrieval.

**Why:**
Building around an unavailable capability would add complexity with no return.
The manual workflow is fast when the UI is designed for it.
