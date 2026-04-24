# CIS Architecture Decision Records
Last updated: 2026-04-24
---
## ADR-001 — Qwen2.5-VL-32B is the primary extraction model
**Status:** Locked
**Decision:** Qwen2.5-VL-32B is the only validated model for CIS knowledge record generation. All smaller models tested produced unacceptable output quality.
**Rationale:** Full day of model benchmarking on real archive material. InternVL3-8B, Qwen2.5-VL-7B, and llava all failed quality threshold. 32B model produced the only acceptable record.
---
## ADR-002 — vLLM is the runtime for local model serving
**Status:** Locked
**Decision:** vLLM 0.19.0 serves the Qwen2.5-VL-32B model locally on the RTX 4090. Runtime environment lives at /mnt/models/vllm-env.
**Rationale:** vLLM was validated during Phase D testing. Successfully served 32B model within 24GB VRAM using gpu-memory-utilization 0.85.
---
## ADR-003 — Storage architecture is drive-purposed not consolidated
**Status:** Locked
**Decision:** Five drives serve dedicated purposes: system disk for OS, /mnt/projects for CIS, /mnt/models for weights and runtimes, /mnt/cache for system cache, /mnt/archive for source material.
**Rationale:** Consolidating everything on the system disk caused 86% usage and blocked model deployment. Separation prevents resource competition.
---
## ADR-004 — SQLite is the persistent memory layer for CIS sessions
**Status:** Locked
**Decision:** SQLite database at /mnt/projects/cis/memory/cis_memory.db stores decisions, session logs, corrections, and schema versions across all sessions.
**Rationale:** Stateless AI sessions require external persistent memory. SQLite is lightweight, file-based, and requires no server process.
---
## ADR-005 — knowledge_record v1 is the canonical output schema
**Status:** Locked
**Decision:** All extraction outputs must conform to the knowledge_record v1 schema defined in MASTER_ARCHITECTURE_MAP. JSON is canonical, markdown is the human-readable mirror.
**Rationale:** One validated record exists proving the schema works: KNOWLEDGE__DOC__COMICS__amazing_adventures_015__001.
---
## ADR-006 — Multi-pass extraction is required for production quality
**Status:** Locked
**Decision:** Extraction runs three passes: Pass 1 extracts raw signal, Pass 2 enforces constraints and removes hallucinations, Pass 3 normalizes to canonical schema.
**Rationale:** Single-pass extraction with all models tested produced schema drift, hallucinations, and ungrounded output. Multi-pass harness is the quality gate.
---
## ADR-007 — Source manifest is the control object for all intake
**Status:** Locked
**Decision:** Every ingested source receives a manifest.json before any processing begins. The manifest tracks source identity, file hash, project link, status, and full state history.
**Rationale:** The manifest is the single source of truth for a source object. No processing step may run without a valid manifest in place.
---
## ADR-009 — Transformers + bitsandbytes is the runtime for 32B model inference
**Status:** Locked
**Decision:** Qwen2.5-VL-32B runs via transformers library with 4-bit bitsandbytes quantization using device_map=auto. vLLM cannot load the full bfloat16 weights within 24GB VRAM.
**Rationale:** Proven on April 12 2026: 21.3GB VRAM, 74% GPU-Util, 237W power draw. Model loaded and generated correct output. Environment at /home/eric/gpu-test with bitsandbytes 0.49.2.
---
## ADR-011 — Comic illustration requires ambiguity-aware extraction standards
**Status:** Locked
**Decision:** Golden and Silver Age comic illustration uses visual shorthand and symbolic compression designed for human readers fluent in the genre. Models will encounter genuine ambiguity that humans resolve through cultural literacy. Extraction quality should be evaluated against this baseline, not against photographic clarity standards.
**Rationale:** Observed during first pipeline extraction: impact strokes around rifle/axe collision caused misidentification even on repeated human review. Uncertainty field must surface these ambiguities rather than defaulting to None.
---
## ADR-012 — Phase 0 execution layer is proven
**Status:** Locked
**Decision:** Five commands complete the intake-to-record pipeline: cis_intake, cis_classify, cis_preprocess, cis_extract, cis_normalize. Full run validated on real archive material producing a canonical knowledge_record.
**Rationale:** Weird War Tales cover processed end to end. Record at IMAGE__WEIRD_WAR_TALES_COVER__001/record_001.json. Status: draft, awaiting review.
---
## ADR-008 — Qwen2.5-VL-32B full bfloat16 weights cannot load on RTX 4090
**Status:** Locked
**Decision:** The full bfloat16 weights at 64GB cannot be loaded on a 24GB GPU. FP8 on-the-fly quantization is also insufficient. 4-bit bitsandbytes quantization via transformers is required.
**Rationale:** Two vLLM load attempts failed. FP8 attempt loaded 11/18 shards then OOM. 4-bit via transformers succeeded.
---
## ADR-010 — cis_extract requires gpu-test env and PYTORCH_ALLOC_CONF flag
**Status:** Locked
**Decision:** cis_extract.py must be invoked with full gpu-test Python path and PYTORCH_ALLOC_CONF=expandable_segments:True to avoid VRAM fragmentation during generation.
**Rationale:** Failed without flag. Succeeded with: PYTORCH_ALLOC_CONF=expandable_segments:True /home/eric/gpu-test/bin/python3 cis_extract.py
---
## ADR-002-SUPERSEDED — vLLM runtime superseded by ADR-009
**Status:** Locked
**Decision:** ADR-002 designated vLLM as runtime. This is superseded. Actual runtime is transformers+bitsandbytes per ADR-009.
**Rationale:** vLLM cannot load 64GB bfloat16 weights in 24GB VRAM. See ADR-008 and ADR-009.
---
## ADR-019 — DAM is the unaffiliated knowledge layer
**Status:** Locked
**Decision:** Knowledge records exist in two modes: affiliated (project_id set) and unaffiliated (project_id null). Unaffiliated records form the DAM. Promotion moves a record into a project or makes it a standalone project. Demotion removes project linkage and returns the record to DAM status. The DAM is the same knowledge base, not a separate system.
**Rationale:** An asset may stop working within a project context and need to be returned to unaffiliated status without being deleted. The DAM provides a persistent home for all material regardless of project affiliation.
---
## ADR-013 — Handoff filename format is YYYY-MM-DD_HHMM
**Status:** Locked
**Decision:** Session handoff files are named using timestamp format YYYY-MM-DD_HHMM.
**Rationale:** Ensures chronological sorting and unambiguous session identification.
---
## ADR-014 — Handoff written to active project folder on session close
**Status:** Locked
**Decision:** The session close protocol writes the handoff file directly to the active project folder.
**Rationale:** Keeps handoff co-located with project context rather than in a generic location.
---
## ADR-015 — Session Close Protocol embedded in handoff content
**Status:** Locked
**Decision:** The session close protocol is embedded in the handoff file itself. A standalone protocol file is no longer required.
**Rationale:** Reduces file proliferation and keeps protocol with the artifact it governs.
---
## ADR-016 — Notes field has qualifying criteria
**Status:** Locked
**Decision:** The Notes field in session close captures: deferred decisions, warnings, gotchas, and mid-thought work. It does not capture next steps.
**Rationale:** Prevents Notes from becoming a duplicate of Next Steps and preserves its signal value.
---
## ADR-017 — Pipeline project association via project_id
**Status:** Locked
**Decision:** project_id is wired through the intake POST in HTML and Python route to cis_intake.py via --project flag.
**Rationale:** Ensures every ingested source is project-aware from the moment of intake.
---
## ADR-018 — Archive file browser added to intake panel
**Status:** Locked
**Decision:** A navigable file browser scoped to /mnt/archive is available in the pipeline intake panel. Clicking a file populates the path field.
**Rationale:** Removes need to manually type archive paths during intake.
---
## ADR-020 — Review page is the human validation surface for ingested assets
**Status:** Locked
**Decision:** Every ingested source has a dedicated review page showing the source image at full viewport height on the left and editable knowledge record fields on the right. The page is the point where AI-proposed metadata is confirmed, corrected, or rejected by the human before the record is promoted.
**Rationale:** AI extraction produces draft records only. Human correction at the review stage is required before any record is trusted. The review page is the primary interface where Loop 3 (system learning) activates — corrections made here become the authoritative version of the record.
---
## ADR-021 — CIS Live — active session only broadcast
**Status:** Accepted
**Decision:** CIS_LIVE.md publishes only the currently selected problem session.
**Rationale:** Prevents model confusion when multiple sessions exist. All other problems remain in DB only.
---
## ADR-022 — CIS Live — round compression toggle
**Status:** Accepted
**Decision:** Compact mode toggle strips earlier rounds from the .md broadcast after round 3.
**Rationale:** Full history on session start. After round 3 models already have earlier rounds in context. Problem statement always retained at top regardless of toggle state.
---
## ADR-023 — CIS Live — copy prompt replaces copy URL
**Status:** Accepted
**Decision:** Push generates a ready-to-paste prompt per model, not a bare URL.
**Rationale:** Bare URL gives models no instruction context. Prompt includes: live URL, problem name, current round number, and model role. Removes ambiguity about intent.
---
## ADR-024 — CIS Live — dynamic model roster replaces hardcoded slots
**Status:** Accepted
**Decision:** Per-round model roster replaces hardcoded Gemini, Claude, ChatGPT fields.
**Rationale:** Hardcoded slots break when adding DeepSeek, Mistral, Llama, Grok or local models. Roster is defined at session creation and overridable per round. Models are registered objects in the DB.
---
## ADR-025 — Model registry connects Intel sidebar tabs to Live roster
**Status:** Accepted
**Decision:** LOCAL, REMOTE, AGENT sidebar tabs become functional via shared model registry.
**Rationale:** Tabs are currently decorative. Dynamic roster draws from same registry making them functional. First wire between sidebar and execution layer. Sets up Phase 0 local model invocation.
---
## ADR-026 — Sequential build path to Phase 0
**Status:** Accepted
**Decision:** Three-step path from current state to Phase 0 execution layer entry.
**Rationale:** Step 1: Fix Live session logic — prompt generation, active-session-only push, round compression. Step 2: Replace hardcoded model slots with dynamic registry tied to Intel sidebar. Step 3: Local model invocation — registry entries get invoke button, first real execution layer wire.
---
## ADR-027 — Backend refactored into modular structure
**Status:** Accepted
**Decision:** CIS dashboard backend split from single file into modular directory structure.
**Rationale:** Single file was becoming unmanageable. Modular structure: app.py entry point, config.py constants, api/ with 10 route modules, db/ with connection and live_db, utils/ with helpers. Allows each capability to be modified and tested in isolation. Aligns with sequential build principle.
---
## ADR-028 — Session lifecycle and Live scratchpad are distinct surfaces
**Status:** Accepted
**Decision:** Session panel handles day-level lifecycle. Live panel handles real-time problem-solving rounds.
**Rationale:** Session is the outer container for a day of work. Live is the multi-model scratchpad that runs inside it. Conflating the two would create an overloaded interface. Separation keeps each surface focused on one responsibility.
---
## ADR-029 — Manual paste is the confirmed input method for CIS Live model responses
**Status:** Accepted
**Decision:** Model responses are pasted manually into the Live panel per slot. Auto-fetch is deferred.
**Rationale:** Major models do not expose stable public share URLs suitable for programmatic fetch. Building around an unavailable capability adds complexity with no return. Manual paste is fast when the UI is designed for it. Auto-fetch revisited if model APIs make it practical.
---
## ADR-030 — WIAS Project Manager is the foundational design reference for CIS
**Status:** Locked
**Decision:** The WIAS Project Manager workbook (version 1) is designated as a foundational reference document for the CIS system. It predates the LLM era and represents the original analogue design intent for a creative project management system across Word, Image, Action, Sound, and Web domains. Its taxonomy, workflow states, project object model, genre classifications, user levels, and production schedule structure are the design origin of the CIS knowledge schema, WIAS routing model, and project object. It is added to the Claude project files for session context and will be formally ingested as a knowledge_record (category: reference, subject: system_design) during the first real archive run.
**Rationale:** CIS is the AI-era implementation of the system designed in the WIAS workbook. Without this document in the system record, the design lineage is invisible to future sessions and collaborating models. The workbook's data model — projects, ideas, research, reference, learning, templates, checklists, genres, media types, user levels — directly informs the knowledge_record schema, processing profiles, WIAS stage routing, and the AI inference layer on project objects. It must be in the ADR record so its authority is explicit and traceable.
---
## ADR-031 — Segment as canonical execution object; scene detection required; fixed interval rejected
**Status:** Locked
**Decision:** Segment is the discrete video unit that passes through the extraction pipeline — the video analog of a single image file. Scene detection (PySceneDetect) is the required segmentation method. Fixed-interval segmentation is explicitly rejected — it crosses scene boundaries and degrades extraction quality.
**Rationale:** Video cannot be treated as a single intake unit. Division method has direct consequences for schema, pipeline design, and knowledge record quality. Content-boundary segmentation preserves extraction context. Fixed interval does not.
---
## ADR-032 — CIS domain taxonomy: LIFE and CREATION as top-level domains; knowledge_spine as first-class object
**Status:** Locked
**Decision:** CIS contains two top-level domains: LIFE (Home, Body, Mind) and CREATION (Word, Image, Action, Sound, Web). WIAS is retained as the historical name for CREATION only. Every project belongs to one sub-domain. The project schema is universal across all domains. knowledge_spine is a first-class CIS object — an authoritative knowledge structure for a domain or production step, ingested before source material. spine_node is the atomic concept unit within a spine, hierarchical and multi-source. knowledge_record gains anchor_node_id linking each record to its spine position. Unanchored records cannot reach approved status. Build sequence: CREATION spines and pipelines proven first; LIFE domains designed now, built later.
**Rationale:** The WIAS Project Manager was designed as a life and creation management system, not a creative production system only. Home, Body, and Mind run as equal schedule domains alongside Word, Image, Action, Sound, Web. Everything resolves into a project regardless of domain. Flat knowledge record storage does not support retrieval at scale — records must be anchored to authoritative domain knowledge structures to be useful. Splitting LIFE into a separate application would re-fragment a system that was unified by design.
---