# CIS Master Session Handoff
## Date: 2026-04-17
## Status: Phase PD Complete + Phase 0 Proven

---

## What CIS actually is (the real statement)

CIS is a local creative intelligence studio that takes an idea, understands your source material, organizes and transforms knowledge, guides execution, and coordinates specialized assistants around real projects. The 10TB archive is not a storage problem — it is the raw material the system learns from and serves.

**The system center:** Intelligence → Knowledge → Application
**The build order:** Phase PD → Phase 0 → Phase 1 → Phase 2 → Phase 3 → Phase 4 → Phase 5
**Current position:** Phase PD complete. Phase 0 proven. Phase 1 is next.

---

## What was built today (confirmed working)

### Infrastructure
- 5 drives mounted and configured: system (491GB/60%), /mnt/projects (246GB), /mnt/models (229GB), /mnt/cache (110GB), /mnt/archive (9.1TB)
- SQLite memory database at /mnt/projects/cis/memory/cis_memory.db
- cis-log command: logs decisions, sessions, corrections to database
- cis-start harness coordinator: loads full context at session start
- Obsidian vault synced to GitHub at digitalgsmp/CIS_Creative_Intelligence_System_v1

### Phase 0 Pipeline (all five commands proven)
- cis-intake — creates source manifest, sets status=arrived
- cis-classify — assigns processing profile, sets status=classified
- cis-preprocess — extracts files for processing, sets status=preprocessed
- cis_extract.py — runs Qwen2.5-VL-32B, produces raw extraction, sets status=extracted
- cis-normalize — converts raw extraction to canonical JSON + markdown, sets status=draft

### First knowledge record produced
- Source: Weird_War_Tales_cover.jpg
- Record ID: KNOWLEDGE__IMAGE__WEIRD_WAR_TALES_COVER__001__001
- Location: /mnt/projects/cis/knowledge/records/IMAGE__WEIRD_WAR_TALES_COVER__001/record_001.json
- Status: draft (awaiting cis_review.py which is not yet written)

---

## The 12 locked ADRs

- ADR-001: Qwen2.5-VL-32B is the primary extraction model
- ADR-002: vLLM was original runtime target (superseded by ADR-009)
- ADR-003: Storage architecture is drive-purposed not consolidated
- ADR-004: SQLite is the persistent memory layer
- ADR-005: knowledge_record v1 is the canonical output schema
- ADR-006: Multi-pass extraction is required for production quality
- ADR-007: Source manifest is the control object for all intake
- ADR-008: Full bfloat16 weights cannot load on RTX 4090
- ADR-009: Transformers + bitsandbytes is the runtime for 32B inference
- ADR-010: cis_extract requires gpu-test env + PYTORCH_ALLOC_CONF flag
- ADR-011: Comic illustration requires ambiguity-aware extraction standards
- ADR-012: Phase 0 execution layer is proven

---

## Critical extract invocation (must not be lost)

```
PYTORCH_ALLOC_CONF=expandable_segments:True \
  /home/eric/gpu-test/bin/python3 \
  /mnt/projects/cis/runtime/cis_extract.py <source_id>
```

---

## Key insights discovered during this session (not yet formalized)

**Insight 1 — CIS is its own first project**
The process of building CIS is itself a CIS project. Every architectural decision, every extraction correction, every workflow discovery should be captured as system knowledge. The build process generates the first corpus of structured knowledge about how the system works.

**Insight 2 — Comic illustration visual language**
Golden/Silver Age comic illustration uses symbolic shorthand designed for culturally fluent human readers. Impact lines, stylized action, compressed narrative — these require a different extraction standard than photographs. The uncertainty field must surface ambiguity rather than defaulting to None. This applies broadly to any illustrated or symbolic source material.

**Insight 3 — Realtime insights are being lost**
The most valuable knowledge in this project is being generated in chat and not captured. The correction log captures field-level corrections but not conceptual insights. A separate insight capture mechanism is needed before Phase 1 begins.

**Insight 4 — The minimal dashboard is needed now, not at Phase 5**
The current workflow requires the human to remember and type every command correctly. A simple operator console with buttons for each pipeline command should be built as the first Phase 1 deliverable, not the last Phase 5 deliverable. This reduces human error and makes the coworker handoff possible.

**Insight 5 — VS Code is the file creation tool**
For any Python script longer than 20 lines, the correct workflow is: Claude produces downloadable file → human places via VS Code file explorer. Never paste complex scripts into terminal.

**Insight 6 — Session logging is still manual and fragile**
The human has to remember to run cis-log at session end. This should be automated. cis_review.py should trigger session logging automatically. A session-end script should be added.

---

## What is missing / not yet built

- cis_review.py — the human review interface for draft records
- Insight capture command in cis-log
- Automated session logging
- Minimal operator dashboard (Flask or similar)
- Vector index and retrieval system
- The README in the vault was not updated from 6 to 12 ADRs

---

## Machine state
- OS: Ubuntu 24.04 in Proxmox VM (VM 100, node wander)
- GPU: RTX 4090 (24GB VRAM), CUDA 13.0, driver 580.126.09
- RAM: 48GB allocated to VM
- Model: Qwen2.5-VL-32B at /mnt/models/huggingface/hub/models--Qwen--Qwen2.5-VL-32B-Instruct/snapshots/7cfb30d71a1f4f49a57592323337a4a4727301da
- Inference env: /home/eric/gpu-test (bitsandbytes 0.49.2, transformers)
- GitHub: digitalgsmp/CIS_Creative_Intelligence_System_v1

---

## How to start any new session

Run on the Ubuntu VM:
```
cis-start
```

Paste the output as the first message in the new chat along with this handoff document.
