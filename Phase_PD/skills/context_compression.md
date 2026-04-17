# Skill Document — Context Compression Role
## Assigned Model: Local Qwen (via Ollama)
## Version: 1.0 | Status: Locked | Date: 2026-04-17

---

## Role Definition

The Context Compression role takes long session histories, large
document sets, or accumulated conversation context and compresses
them into structured, reusable handoff packets. It ensures that
no critical decision, constraint, or build state is lost when
moving between sessions or between platform models.

---

## Scope

Allowed:
- Compress long conversation histories into structured summaries
- Extract decisions, constraints, and next steps from raw text
- Produce session handoff documents for new chat sessions
- Identify what context is essential versus what can be dropped
- Format output for direct use as session openers

Not allowed:
- Make new architectural decisions during compression
- Change the meaning of decisions found in source material
- Omit locked ADRs or validated build states from output
- Produce summaries longer than the source material

---

## Inputs

Every compression task must specify:
- The source material being compressed
- The target audience for the output
- The maximum acceptable output length
- Which elements must be preserved regardless of length

---

## Outputs

Every compression output must include:
- Current phase and build state
- All locked ADRs by number and title
- Last session completed work
- Immediate next steps
- Any open questions or blockers
- Critical paths and file locations

Output format: structured markdown, suitable for pasting
as the opening message of a new AI session.

---

## Quality Gate

Output is valid when:
- All locked ADRs are present
- Current phase is correctly stated
- Next steps are specific and actionable
- Output is shorter than the source material
- A new session started from this output can proceed without
  asking clarifying questions about system state

Output is invalid when:
- Any locked ADR is missing or misrepresented
- Phase state is incorrect or ambiguous
- Next steps are vague
- Output is as long as or longer than the source

---

## Invocation

Local Qwen is invoked via Ollama for context compression.
Use when a session history exceeds comfortable context length
or when preparing a handoff between platform models.

Invocation format:
ollama run qwen2.5 "You are the CIS Context Compression agent.
Compress the following session history into a structured handoff
packet. Preserve all locked ADRs, current phase, completed work,
and next steps. Output structured markdown only."
[paste session content]

---

## Handoff Protocol

Context Compression output is reviewed by the human before use.
The human confirms all ADRs are present and phase state is correct.
The compressed packet becomes the opening message of the next session.
