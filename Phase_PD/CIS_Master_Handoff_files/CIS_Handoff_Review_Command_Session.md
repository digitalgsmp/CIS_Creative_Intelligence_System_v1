# CIS Session Handoff — cis_review.py
## Priority: HIGH — Pipeline is incomplete without review

---

## Context

Phase 0 pipeline has five working commands:
cis-intake → cis-classify → cis-preprocess → cis_extract → cis-normalize

The pipeline ends at status=draft. cis_review.py is the missing final command that moves a record from draft to checked/approved and captures human corrections.

One draft record exists:
- KNOWLEDGE__IMAGE__WEIRD_WAR_TALES_COVER__001__001
- Location: /mnt/projects/cis/knowledge/records/IMAGE__WEIRD_WAR_TALES_COVER__001/record_001.json
- Three corrections already logged in the database for this record

---

## What cis_review.py must do

1. Load the draft knowledge record JSON
2. Display it in the terminal in readable format
3. Show any corrections already logged for this record from the database
4. Allow the human to: approve / reject / edit specific fields
5. Apply corrections to the record JSON
6. Update status: draft → checked (human has reviewed)
7. Update manifest status to match
8. Log the review action to the session log
9. Print next step

---

## Corrections already logged for the Weird War Tales record

From the corrections table in the database:

1. scene_description — hallucination
   Original: "muscular bearded man who appears to be a tribal warrior"
   Corrected: "caveman — prehistoric human with heavy brow, body hair, loincloth, primitive weapon. Lost world scenario."

2. uncertainty — structure
   Original: "None"
   Corrected: "Thematic context of lost world scenario inferrable but not stated in visible text. Impact strokes cause visual ambiguity."

3. visible_text — missed_visible_text
   Original: missing
   Corrected: "Joe Kubert signature visible bottom left corner"

cis_review.py should show these corrections and ask whether to apply them to the record.

---

## File location

/mnt/projects/cis/runtime/cis_review.py

---

## Database connection

Database at: /mnt/projects/cis/memory/cis_memory.db
Corrections table: record_id, field_name, original_value, corrected_value, correction_type, corrected_by, created_at

---

## Important: use VS Code for file creation

Do not paste Python scripts into the terminal.
Claude should produce the file as a download.
Human places it via VS Code file explorer.

---

## Start this session with

Run on Ubuntu VM: cis-start
Paste cis-start output + this document as opening message.
Tell Claude: "Write cis_review.py. It should load a draft record, show existing corrections from the database, allow the human to apply or skip each correction, update the record JSON, and move status to checked."
