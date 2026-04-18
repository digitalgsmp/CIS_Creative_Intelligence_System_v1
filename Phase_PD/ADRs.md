# CIS Architecture Decision Records
Last updated: 2026-04-18
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