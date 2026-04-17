# CIS Session Handoff — Minimal Operator Dashboard
## Priority: URGENT — Build this before Phase 1 begins

---

## Context

CIS Phase 0 pipeline is proven. Five commands process a file from raw arrival to draft knowledge record:
cis-intake → cis-classify → cis-preprocess → cis_extract.py → cis-normalize

The problem: every command requires the human to type it correctly in the terminal. This creates errors, cognitive load, and makes the coworker handoff impossible. A minimal dashboard with buttons replaces terminal commands for routine operation.

---

## What to build

A local web interface running at http://localhost:5000 on the Ubuntu VM. Built with Flask (Python). Five panels:

### Panel 1 — Intake
- File drop zone or path input
- Button: "Intake File"
- Calls: cis-intake <path>
- Shows: source_id, status=arrived

### Panel 2 — Pipeline
- Input: source_id
- Buttons: Classify | Preprocess | Extract | Normalize
- Each button calls the corresponding command
- Shows: current status from manifest.json after each step
- Extract button uses the special invocation:
  PYTORCH_ALLOC_CONF=expandable_segments:True /home/eric/gpu-test/bin/python3 /mnt/projects/cis/runtime/cis_extract.py <source_id>

### Panel 3 — Review
- Shows draft records awaiting review
- For each record: title, summary, tags, visible text
- Buttons: Approve | Reject | Edit
- Calls: cis_review.py (needs to be written)

### Panel 4 — Knowledge Base
- Lists all records by status (draft / checked / approved / locked)
- Click a record to see full JSON
- Search by tag or subject

### Panel 5 — Insights
- Text input: capture a realtime insight
- Category dropdown: architectural / extraction / workflow / system
- Button: Save Insight
- Calls: cis-log insight (new command needed)

---

## What needs to exist first

Before building the dashboard:
1. cis_review.py must be written (the review command)
2. cis-log needs an "insight" subcommand added
3. The Flask app reads manifests and knowledge records directly from the filesystem

---

## Files involved

- New file: /mnt/projects/cis/runtime/cis_dashboard.py
- Existing: /mnt/projects/cis/runtime/cis_review.py (needs to be created)
- Existing: /mnt/projects/cis/memory/cis_log.py (needs insight subcommand)
- Database: /mnt/projects/cis/memory/cis_memory.db

---

## Start this session with

Run on Ubuntu VM: cis-start
Paste cis-start output + this document as opening message.
Tell Claude: "Build the minimal CIS operator dashboard. Start with cis_review.py, then add the insight command to cis-log, then build cis_dashboard.py."
