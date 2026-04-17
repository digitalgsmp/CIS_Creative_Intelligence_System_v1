# CIS Architecture Decision Records

Phase PD — Pre-Development Harness
Last updated: 2026-04-17

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
