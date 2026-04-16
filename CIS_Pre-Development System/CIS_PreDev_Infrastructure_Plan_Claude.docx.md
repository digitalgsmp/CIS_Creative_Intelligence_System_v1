

**CIS PRE-DEVELOPMENT INFRASTRUCTURE PLAN**

*Harness-First Foundation for the Creative Intelligence System*

Version 1.0  |  Bootstrap Edition

# **1\. Why This Document Exists**

The CIS Formal Phased Construction Plan defines what to build. This document defines what must exist before you can build it reliably — without hitting the 80% collapse barrier that ended the previous development attempt.

The 80% problem is not a motivation problem or a scope problem. It is a context collapse problem. When documentation grows large enough to compete with code for context window space, the AI loses coherence. Guardrail documents consume the window. The model begins hallucinating consistency. Decisions made in session 2 are invisible in session 12\. Progress degrades until the project is effectively lost.

The harness engineering principle, documented in the AI Harness Engineering source material, names the solution: externalize cognitive burden out of the model and into deterministic infrastructure outside the model. Memory, state, protocols, and procedural expertise must live in explicit artifacts — not inside context windows.

This pre-development plan builds that external infrastructure before a single line of CIS application code is written.

# **2\. What the Harness Is**

The harness is not a framework or a tool. It is a set of deterministic external systems that surround your AI models and make them reliable enough to build complex software with. The harness replaces context window dependence with structured external storage.

A harness has four layers:

| Layer | Function |
| :---- | :---- |
| **Memory** | Stores project state, decisions, session logs, and source of truth outside any model's context window |
| **Skills** | Procedural expertise stored as documents — role definitions, prompt templates, workflow protocols |
| **Protocols** | Interaction rules — how models receive context, what they return, how outputs are validated |
| **Harness Coordinator** | The human or lightweight tool that routes inputs, pastes context, validates outputs, and updates state |

In your setup, you are the harness coordinator. The Obsidian vault is the memory layer. The role documents are the skills layer. The session templates and prompt patterns are the protocol layer. All of this lives in a visible folder on your machine, not buried in terminal state.

# **3\. The 80% Barrier — Root Cause Analysis**

The previous project failed at 80% completion for a specific set of compounding reasons. Each one has a direct countermeasure in this plan.

| Failure Mode | Harness Countermeasure |
| :---- | :---- |
| Guardrail docs consumed context window, leaving no room for code | STATE.md \+ role docs are pasted as minimal structured context, not full documents |
| Decisions made early became invisible in later sessions | ADR vault — every locked decision is a permanent file, loaded by reference not memory |
| No structured handoff between sessions | Session Log template — every session ends with a structured close that becomes the next session opener |
| Models hallucinated consistency across sessions | Canonical source of truth files — models are told explicitly what is locked vs. open |
| Scope grew without a gate | Phase exit criteria — no phase advances without explicitly checking exit conditions |
| Documentation and code lived in different places | Single root folder — all docs, schemas, and code are siblings in one visible directory tree |
| No local model for low-cost context tasks | Local 32B LLM handles context summarization, document compression, and session prep without API cost |

# **4\. Infrastructure Overview**

The pre-development infrastructure has five components. They are ordered by dependency — each one enables the next.

1. The Root Folder — the visible, portable home of the entire project

2. The Obsidian Vault — the memory and knowledge layer, living inside the root folder

3. The Model Role Stack — structured role definitions for each AI platform

4. The Session Protocol — how each work session starts, runs, and closes

5. The Local LLM Layer — Ollama-served 32B model for context compression and low-cost tasks

These five components are the harness. The CIS application is built inside and on top of this harness.

# **5\. Component 1 — The Root Folder**

## **5.1 Purpose**

Everything lives here. You can open it in Windows Explorer or a Linux file manager and see every file the project has ever produced. Nothing is buried in system paths. Nothing is tied to one machine. This folder IS the project.

## **5.2 Location**

Choose one location and never move it. Recommended:

* Windows host: C:\\Projects\\CIS\\

* Proxmox VM (Linux): \~/Projects/CIS/

* If using both: keep the canonical copy on whichever machine runs Git, and sync to the other

## **5.3 Top-Level Structure**

The following structure mirrors the CIS construction plan's Epic 0.1 deliverables while adding the harness and infrastructure layers:

| Folder | Contents |
| :---- | :---- |
| **/vault** | Obsidian vault — all project memory, decisions, session logs, state |
| **/docs** | Human-readable project documentation, plans, and guides |
| **/adr** | Architecture Decision Records — locked decisions, one file each |
| **/schemas** | Canonical JSON schemas for all CIS objects |
| **/services** | Backend service code (FastAPI, etc.) |
| **/apps** | Frontend application code (React, etc.) |
| **/scripts** | Utility scripts, preprocessing tools |
| **/tests** | Test suites and fixtures |
| **/ops** | Docker files, deployment configs, environment definitions |
| **/fixtures** | Sample data for testing |
| **/harness** | Role documents, prompt templates, session protocols |
| **/mnt/archive** | Raw source material — never modified |
| **/mnt/projects** | Active CIS project working data |
| **STATE.md** | Root-level file — current phase, active blockers, last decision |
| **README.md** | One-paragraph description of what the project is and how to start |

## **5.4 Docker Portability**

The /ops folder contains the Dockerfile and docker-compose.yml that package the CIS application. When the application is ready to share, the recipient runs one command from this folder. The folder structure above becomes the container's internal structure. Nothing is system-dependent.

## **5.5 Git Initialization**

Initialize Git at the root from day one. Every session commit is a restore point. If a session produces unusable output, you revert. This is non-negotiable.

* git init at project root

* Commit after every meaningful change

* .gitignore excludes: node\_modules, \_\_pycache\_\_, .env files, large binary sources

* Obsidian vault folder is included in Git — your decisions and session logs are versioned

# **6\. Component 2 — The Obsidian Vault**

## **6.1 Purpose**

The vault is the project's external memory. It replaces context window dependence. When you start a session, you open the relevant vault files and paste their content as structured context. The model does not need to remember anything from previous sessions — the vault does.

## **6.2 Vault Location**

Place the vault inside the root folder at /vault. Open Obsidian and point it to this folder as the vault root. This means the vault is Git-versioned along with everything else.

## **6.3 Vault Structure**

| Vault Folder | Contents |
| :---- | :---- |
| **/state** | STATE.md — the single source of truth for current project status |
| **/sessions** | One note per work session — dated, structured, Git-committed at close |
| **/decisions** | One note per locked decision — replaces ADR files for quick reference |
| **/phases** | One note per delivery phase — objective, epics, exit criteria, current status |
| **/roles** | Model role definitions — what each AI platform is responsible for |
| **/schemas** | Human-readable schema summaries linked to canonical JSON files |
| **/blockers** | Active blockers — one note per unresolved issue |
| **/model-outputs** | Raw AI outputs before human review and promotion |

## **6.4 The STATE.md File**

This is the most important file in the project. It is short by design — one screen. It contains exactly:

* Current delivery phase and capability phase

* What was completed last session (2-3 lines)

* What is actively blocked and why

* The next concrete action

* Links to the three most relevant vault notes for this session

Every AI session begins by pasting STATE.md as the first context block. Every session ends by updating STATE.md before committing.

## **6.5 Session Log Structure**

Every work session produces one session note. The template is:

| Field | Content |
| :---- | :---- |
| **Date** | YYYY-MM-DD |
| **Phase** | Current delivery phase |
| **Models Used** | Which AI platforms were active and in what roles |
| **Objective** | What this session intended to accomplish |
| **Decisions Made** | Anything locked this session — link to decision note |
| **Outputs Produced** | Files created or modified — paths listed |
| **Promoted to Canon** | What was reviewed and approved by human |
| **Blockers Raised** | New issues discovered |
| **Next Session Opens With** | Exact STATE.md content to set before next session |

# **7\. Component 3 — The Model Role Stack**

## **7.1 Purpose**

Each AI platform has a defined role. Roles prevent scope overlap, reduce contradiction between models, and give each platform a context frame small enough to be effective. Role documents live in /harness/roles/ and are pasted at the start of each session with that platform.

## **7.2 Role Definitions**

| Platform | Role Title | Responsibilities |
| :---- | :---- | :---- |
| **Gemini** | System Architect | Large-context architecture review. Load the full plan plus generated code together. Design the intelligence pipeline (OCR, vision, merge layer). Validate that implementation matches design intent. Final say on system-level decisions. |
| **Claude** | Implementation Engine | Contract-first code generation. Implement to schemas and ADRs. Generate schemas, domain models, state machines, command layers. Every output references the locked contract it implements. |
| **ChatGPT** | Adversarial Reviewer | Receive outputs from Claude or Gemini and find what is wrong. Test edge cases, contradict assumptions, identify missing error handling, flag scope drift. Does not generate primary artifacts. |
| **Local 32B LLM** | Context Compressor | Summarize session logs. Compress large documents into pasteable context blocks. Generate first-pass boilerplate. Handles any task where API cost is a concern and perfect quality is not required. |

## **7.3 Role Document Format**

Each role document in /harness/roles/ contains exactly four sections:

6. Your role in this project — one paragraph

7. What you are not responsible for — explicit exclusions

8. What context you receive at session start — which files are pasted

9. What you return — format, naming convention, where it goes

These documents are pasted as the system context before any task prompt. They replace ad hoc instruction and eliminate the drift that comes from re-explaining roles each session.

# **8\. Component 4 — The Session Protocol**

## **8.1 Purpose**

The session protocol is the turn-based workflow that coordinates the four platforms. It eliminates simultaneous chaos and ensures every output is validated before it influences the next step. This is the operational heart of the harness.

## **8.2 Session Open Sequence**

Every session begins in the same order, regardless of what is being worked on:

10. Open STATE.md — read current phase, last action, active blockers

11. Open the relevant phase note in the vault — confirm what epic is active

12. Open the relevant ADR files — confirm what is locked

13. Identify which platform handles today's task using the role table

14. Paste: Role document \+ STATE.md \+ relevant ADRs \+ task prompt

15. Do not paste the full CIS construction plan — use STATE.md to scope context

## **8.3 Within-Session Relay Pattern**

When multiple platforms are involved in one session:

* Step 1: Claude generates the artifact (schema, code, model definition)

* Step 2: Paste Claude output into ChatGPT with: 'Review this against \[linked ADR\]. What is wrong or missing?'

* Step 3: If review raises issues, return to Claude with specific corrections

* Step 4: If review passes, promote output to /model-outputs/ for human review

* Step 5: Human reviews and either promotes to canon or flags for revision

* Step 6: Gemini performs system-level consistency check at phase milestones, not every session

## **8.4 Session Close Sequence**

Every session closes in the same order:

16. Update STATE.md — current phase, what completed, what is blocked, next action

17. Write session note — fill the session log template, save to /vault/sessions/

18. Move approved outputs from /model-outputs/ to their canonical location

19. git commit with message: 'Session YYYY-MM-DD: \[one line summary\]'

20. Close all AI platform sessions — no dangling context

## **8.5 Decision Lock Protocol**

When any session produces a decision that affects architecture or contracts:

* Write a decision note in /vault/decisions/ immediately

* If it modifies a schema, update the schema file and increment the version

* If it changes an ADR, create a new ADR that supersedes the old one — never edit old ADRs

* Add the decision to STATE.md under 'last decision'

* Commit before continuing — a decision that is not committed did not happen

# **9\. Component 5 — The Local LLM Layer**

## **9.1 Purpose**

Your RTX 4090 can run 32B parameter models at useful throughput. The local model handles tasks where API cost is prohibitive or where the task does not require frontier-model quality. This extends your effective working capacity without accumulating API charges.

## **9.2 Recommended Stack**

| Component | Choice and Rationale |
| :---- | :---- |
| **Runtime** | Ollama — simplest local model server, one command to pull and serve any supported model |
| **Primary Model** | Qwen2.5-32B or Mistral-Large-32B — strong instruction following, fits 4090 VRAM at Q4 quantization |
| **Interface** | Open WebUI — browser-based chat interface over your Ollama server, runs in Docker |
| **Integration Point** | Ollama REST API at localhost:11434 — same call pattern as OpenAI API, easy to switch |

## **9.3 What the Local Model Does**

* Compress a 2000-line plan into a 200-line context block for pasting into frontier sessions

* Generate first-pass boilerplate (folder structures, stub files, manifest templates)

* Summarize session logs into STATE.md update drafts

* Answer questions about your own codebase when the code is pasted in (no API cost)

* Run OCR post-processing and text cleanup pipelines once Phase 3 is built

## **9.4 What the Local Model Does Not Do**

* It does not make architecture decisions — those go to Gemini

* It does not generate production code — that goes to Claude

* It does not perform adversarial review — that goes to ChatGPT

* It does not replace frontier models — it reduces the cost of using them

## **9.5 Setup Steps**

21. Install Ollama on the Proxmox VM that has GPU passthrough to the 4090

22. Pull the chosen 32B model: ollama pull qwen2.5:32b

23. Run Open WebUI in Docker on the same VM

24. Verify GPU utilization during inference — nvidia-smi should show VRAM in use

25. Test with a context compression task before using in real sessions

# **10\. Bootstrap Sequence — Getting Started Without the Full System**

CIS is the tool. Building CIS is the first project inside CIS. This creates a bootstrapping problem: you need CIS to manage CIS before CIS exists. The solution is a manual bootstrap — run a minimal subset of CIS by hand until enough of the system exists to run itself.

## **10.1 The Bootstrap Slice**

You need only these CIS capabilities to manage its own construction:

* A project record — the CIS project entry

* A source record — the construction plan as the first ingested source

* A STATE.md — manually maintained

* A session log — manually written after each session

* A decision vault — manually populated ADR files

No pipeline. No schemas enforced by code. No validation tooling. Just the folder structure and the discipline to use it consistently. The friction is deliberate and temporary.

## **10.2 Ordered Bootstrap Steps**

Execute in this exact sequence. Do not skip steps to go faster.

26. Create the root folder at your chosen path

27. Initialize Git inside it: git init

28. Create all top-level folders from Section 5.3

29. Open Obsidian, create vault pointing to /vault inside the root

30. Create vault folder structure from Section 6.3

31. Copy the CIS construction plan into /mnt/archive/sources/cis-construction-plan/source/

32. Write STATE.md by hand — current phase: Phase 0, current blocker: none, next action: ADR baseline

33. Write the first session note for this bootstrap session

34. Write the first four ADRs from Section 3 of the construction plan

35. Install Ollama and pull 32B model on GPU VM

36. Commit everything: git commit \-m 'Bootstrap: harness and vault initialized'

37. Write role documents for each platform in /harness/roles/

38. Use local model to compress the construction plan into a 200-line context block

39. Store compressed context in /vault/schemas/ as cis-plan-context.md

40. From this point: all sessions follow the session protocol in Section 8

## **10.3 First ADRs to Write**

These four decisions are already locked in the construction plan. Write them as ADR files immediately so they are never re-litigated:

* ADR-001: Intelligence-first architecture — CIS is story-first, not tool-first

* ADR-002: knowledge\_record as canonical output object

* ADR-003: Contract-first implementation — no subsystem built before its schema is defined

* ADR-004: Human/AI boundary — AI proposes, human validates, AI does not self-finalize

## **10.4 Accepting the Startup Friction**

The manual bootstrap requires discipline in place of tooling. Specifically:

* You update STATE.md by hand after every session — this takes 5 minutes and is not optional

* You write the session note before closing any AI platform — not later, now

* You commit to Git before sleeping — uncommitted work can be lost

* You paste role documents at the start of every session with every platform — every time

The friction exists because the automation does not exist yet. The automation is what you are building. The discipline is what makes the bootstrap survivable.

# **11\. Pre-Development Phase Completion Criteria**

The pre-development infrastructure is complete and you are ready to begin Phase 0 of the CIS construction plan when ALL of the following are true:

* Root folder exists, is Git-initialized, and has the full folder structure

* Obsidian vault is open and all vault folders exist

* STATE.md exists and contains accurate current state

* At least one session note exists in /vault/sessions/

* ADR-001 through ADR-004 exist as files in /adr/

* Role documents exist for all four platforms in /harness/roles/

* Ollama is running on the GPU VM and a 32B model responds to test prompts

* The CIS construction plan source document is in /mnt/archive/

* A compressed context version of the plan is in /vault/

* First Git commit is made with message: 'Bootstrap complete'

When all ten are true, open the CIS construction plan, navigate to Phase 0 Epic 0.1, and begin.

# **12\. What You May Not Be Considering**

Based on the depth of this project and the patterns in the conversation so far, there are several areas worth flagging that have not come up yet.

## **12.1 Context Compression is a Skill**

The local 32B model will compress your documents, but you need to develop the prompt that reliably produces usable compression. A compressed context block that drops critical constraints is worse than no compression. Before relying on compression in a real session, test the compression prompt against a known document and verify the output manually.

## **12.2 The Obsidian Git Plugin**

Obsidian has a community plugin called Obsidian Git that autocommits your vault on a schedule. Enable this. It removes the human failure point of forgetting to commit session notes. Configure it to commit every 10 minutes during active sessions.

## **12.3 Schema Versioning From Day One**

Every schema file needs a version field from the first draft. When a schema changes, increment the version. Every piece of code that uses that schema records which version it was written against. This prevents the silent incompatibility problem where code and schema drift apart over phases.

## **12.4 The Model-Outputs Quarantine**

Raw AI outputs must never go directly into canonical locations. The /model-outputs/ quarantine folder is not a formality — it is the enforcement mechanism for the human/AI boundary defined in ADR-004. If outputs skip review and land in canonical locations, the harness boundary is broken. This is how hallucinations get baked into your codebase.

## **12.5 Gemini's Context Window Has a Cost**

Gemini's large context window is genuinely useful for system-level architecture reviews. But large context calls are expensive. Reserve full-plan loads for milestone reviews, not routine sessions. Most sessions should operate on STATE.md plus two or three focused files, regardless of which platform is being used.

## **12.6 The Docker Build Belongs in Phase 0**

The Docker deployment structure should be scaffolded in Phase 0, not retrofitted later. Create an empty Dockerfile and docker-compose.yml in /ops/ at bootstrap time. Every service added in later phases is added to the compose file as it is built. By Phase 4 you have a working Docker deployment, not a big bang containerization effort at the end.

# **Appendix — Quick Reference**

## **A. Daily Session Checklist**

41. Read STATE.md

42. Open relevant phase note and active ADRs

43. Paste role document \+ STATE.md \+ task prompt into target platform

44. Work session

45. Move approved outputs to canonical locations

46. Update STATE.md

47. Write session note

48. Git commit

## **B. Decision Lock Checklist**

49. Write decision note in /vault/decisions/

50. Update any affected schema — increment version

51. Create new ADR if decision affects architecture

52. Update STATE.md 'last decision' field

53. Git commit immediately

## **C. Context Paste Order**

When starting any AI session, paste context in this order:

54. Role document for this platform

55. STATE.md

56. Relevant ADRs (2-3 maximum)

57. Task prompt

Do not paste the full construction plan. Use the compressed context version from the vault for orientation if needed.

## **D. File Naming Conventions**

* Session logs: YYYY-MM-DD-session.md

* ADRs: ADR-NNN-short-title.md

* Decision notes: DEC-NNN-short-title.md

* Schema files: object-name.schema.v1.json

* Role documents: role-\[platform-name\].md

* Model outputs: YYYY-MM-DD-\[platform\]-\[artifact-type\].md

*CIS Pre-Development Infrastructure Plan  |  Bootstrap Edition  |  v1.0*