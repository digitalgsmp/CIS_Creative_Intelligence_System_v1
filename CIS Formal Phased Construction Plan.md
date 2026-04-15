# **CIS Formal Phased Construction Plan**

This plan converts the extracted CIS documentation into a build program that can be executed like a serious application-development effort. It is organized the way a senior software developer or technical lead would structure a complex system build: clear phases, bounded epics, explicit dependencies, milestone gates, and unambiguous exit criteria.

This plan is derived from the CIS source documents, not from a generic app template. The core architectural truths that govern the whole plan are:

* CIS is a **story-first creative production infrastructure**, not a tool stack.  
* The system center is **Intelligence → Knowledge → Application**, with tools as execution endpoints.  
* The build method is **contract first, then implementation, then validation**, one major contract at a time.  
* The system is **project-centered**, object-first, non-linear, and reality-driven.  
* The current operational priority is **Phase D — Intelligence**, with the main blockers being the **merge layer** and **unified execution/orchestration**.

---

## **1\. Program Charter**

## **1.1 Program objective**

Build the first usable CIS as a controlled, project-centered, knowledge-forming creative system that can:

* ingest real source material  
* preprocess it deterministically  
* run multimodal extraction  
* merge OCR and vision into structured `knowledge_record` objects  
* review and validate those records  
* store them in canonical form  
* retrieve and reuse them inside project workflows  
* expose this through a workbench interface  
* improve over time through reinforcement and accepted corrections

## **1.2 Non-goals for the first program cycle**

The following are explicitly deferred or constrained:

* fully autonomous agents  
* concurrent swarm agents  
* full polished application layer  
* broad automation before deterministic workflows are stable  
* premature database-heavy redesign  
* building every subsystem at once

## **1.3 Governing constraints**

All construction must obey:

* Operator Model overrides all lower layers.  
* STATE.md is the only source of truth for current phase.  
* No subsystem is implemented before its contract is defined.  
* Every interaction must move material toward structured knowledge.  
* All generated knowledge must be normalized, schema-valid, logged, and reviewable.  
* Only approved outputs may influence retrieval, agents, or future system behavior.

---

# **2\. Program structure**

This construction plan uses two parallel structures:

## **2.1 Capability phases**

These preserve the CIS phase model:

* Phase D — Intelligence  
* Phase E — Knowledge  
* Phase F — Workflow  
* Phase G — Agents  
* Phase H — Application

## **2.2 Delivery phases**

These are the concrete software-delivery phases:

* Phase 0 — Program setup and architecture freeze  
* Phase 1 — Core contracts and runtime foundation  
* Phase 2 — Intake, source containers, preprocessing  
* Phase 3 — Intelligence execution and merge layer  
* Phase 4 — Workbench vertical slice  
* Phase 5 — Knowledge indexing and retrieval  
* Phase 6 — Reinforcement and structure stabilization  
* Phase 7 — Bounded agent modes  
* Phase 8 — Expanded application surface

The delivery phases are the actual build order.

---

# **3\. Cross-cutting architectural decisions already locked**

These must be treated as baseline assumptions in all implementation.

## **3.1 Core object model**

The system is object-first. Core objects include:

* Project  
* Source  
* Manifest  
* KnowledgeRecord  
* Idea  
* Research  
* Reference  
* Learning  
* Template  
* Checklist

## **3.2 Canonical execution contract**

All execution must follow:

`Input → Process → Validation → Output → State Change`

## **3.3 Canonical intelligence pipeline**

The canonical multimodal pipeline is:

`ingest → OCR + visual extraction → merge → structured record → optional refinement`

## **3.4 Canonical knowledge object**

The canonical output unit is `knowledge_record`, stored as:

* JSON canonical source of truth  
* Markdown human-readable mirror

## **3.5 Canonical storage model**

Active storage architecture is:

* `/` for system and applications  
* `/mnt/projects` for active work and outputs  
* `/mnt/archive` for raw source archive

## **3.6 Naming and storage convention**

Each processed source gets its own record family folder, and no loose canonical files are allowed.

## **3.7 Human/AI boundary**

AI proposes; human validates, corrects, and promotes. AI does not self-finalize truth.

---

# **4\. Phase 0 — Program setup and architecture freeze**

## **4.1 Objective**

Create the minimum engineering structure required to build CIS without drift.

## **4.2 Epics**

### **Epic 0.1 — Repository and folder strategy**

Create the source repository and define its top-level structure.

Deliverables:

* `/docs`  
* `/adr`  
* `/schemas`  
* `/services`  
* `/apps`  
* `/scripts`  
* `/tests`  
* `/ops`  
* `/fixtures`

Dependencies:

* none

Exit criteria:

* repo initialized  
* document locations fixed  
* implementation artifacts separated from governance docs

### **Epic 0.2 — ADR baseline**

Convert the locked system decisions into architecture decision records.

Must include ADRs for:

* intelligence-first architecture  
* project-centered model  
* `knowledge_record` as canonical object  
* merge layer requirement  
* workbench-before-full-app approach  
* approval-gated reinforcement  
* naming and storage convention v2  
* phase authority in STATE.md

Dependencies:

* repo structure

Exit criteria:

* high-impact decisions documented as ADRs  
* implementation team can work without re-litigating architecture

### **Epic 0.3 — Schema registry**

Create `/schemas` and populate initial contracts for:

* project  
* manifest  
* knowledge\_record  
* retrieval\_chunk  
* state transition events  
* review actions

Dependencies:

* ADR baseline

Exit criteria:

* schemas versioned  
* validation framework chosen  
* field authority and mutability rules recorded

## **4.3 Milestone**

**M0 — Architecture frozen enough to build**

---

# **5\. Phase 1 — Core contracts and runtime foundation**

This is the first real software phase.

## **5.1 Objective**

Build the deterministic core runtime that enforces objects, state, validation, logging, permissions, and command boundaries.

## **5.2 Epics**

### **Epic 1.1 — Domain model implementation**

Implement domain models for:

* `Project`  
* `Source`  
* `Manifest`  
* `KnowledgeRecord`  
* `RetrievalChunk`  
* `ReviewEvent`  
* `ExecutionRun`

Deliverables:

* typed models  
* serialization/deserialization  
* versioning support  
* field mutability enforcement

Dependencies:

* schema registry

Exit criteria:

* models pass schema validation  
* immutable and regenerable field classes enforced

### **Epic 1.2 — State machine implementation**

Implement two state systems:

* Source state machine:  
  * arrived  
  * classified  
  * preprocessed  
  * extracted  
  * normalized  
  * draft  
  * reviewed  
  * approved  
  * rejected  
* Review state machine:  
  * valid  
  * needs\_review  
  * rejected  
  * retry, plus record promotion states draft → checked → approved → locked → deprecated

Dependencies:

* domain models

Exit criteria:

* state transition guards implemented  
* invalid transitions blocked  
* state changes logged

### **Epic 1.3 — Runtime command layer**

Implement command entry points for at least:

* `project.create`  
* `source.ingest`  
* `source.preprocess`  
* `source.extract`  
* `record.merge`  
* `record.validate`  
* `record.save`  
* `record.review`  
* `record.promote`  
* `record.deprecate`

Dependencies:

* state machine  
* domain models

Exit criteria:

* commands are callable programmatically  
* each command declares input/output contract  
* each command writes structured log entries

### **Epic 1.4 — Control and permission enforcement**

Implement CONTROL layer rules:

* SAFE / CONTROLLED / RESTRICTED permissions  
* filesystem scope boundaries  
* approval checkpoints  
* no raw model output stored  
* structured output control enforcement

Dependencies:

* runtime commands

Exit criteria:

* sensitive actions require confirmation  
* restricted actions blocked without approval  
* audit trail available

### **Epic 1.5 — Logging and observability**

Implement structured logs for:

* command invoked  
* task type  
* model used  
* source and project IDs  
* validation results  
* escalation count  
* runtime metrics

Dependencies:

* runtime commands

Exit criteria:

* every command produces a traceable execution event  
* system log exists and is queryable

## **5.3 Milestone**

**M1 — Deterministic runtime core exists**

## **5.4 Exit criteria**

* all core objects implemented  
* all key command interfaces available  
* state transitions enforceable  
* permissions and approvals active  
* logging operational

---

# **6\. Phase 2 — Intake, source containers, preprocessing**

## **6.1 Objective**

Build deterministic source intake and preprocessing so raw materials become model-ready inputs.

## **6.2 Epics**

### **Epic 2.1 — Source container creation**

Implement source container generation with required directories:

* `source/`  
* `working/`  
* `text/`  
* `pages/`  
* `intelligence/`  
* `metadata/`  
* `logs/`

Dependencies:

* runtime core

Exit criteria:

* every ingested source gets a container  
* container naming follows convention  
* original source preserved

### **Epic 2.2 — Manifest system**

Implement `metadata/manifest.json` creation before extraction.

Manifest must capture:

* source identity  
* source path  
* project context  
* processing\_profile  
* processing\_plan  
* runtime state

Dependencies:

* source container creation

Exit criteria:

* no source enters pipeline without manifest  
* manifest controls downstream behavior

### **Epic 2.3 — Processing profiles**

Implement declared processing profiles:

* `document_text`  
* `document_multimodal`  
* `reference_image`  
* `tutorial_video`  
* `audio_lesson`  
* `idea_note`

Dependencies:

* manifest system

Exit criteria:

* pipeline behavior is explicit, not guessed  
* each profile maps to a processing plan

### **Epic 2.4 — Preprocessing adapters**

Implement deterministic preprocessing for:

* PDF: `pdftotext`, `pdftoppm`  
* Image: RGB conversion  
* Video: audio extraction, frame sampling, transcript generation  
* Audio: WAV 16kHz mono conversion, transcript generation

Dependencies:

* processing profiles

Exit criteria:

* all preprocessing outputs land in predictable folders  
* no semantic interpretation occurs in preprocessing  
* outputs are deterministic and reproducible

### **Epic 2.5 — Archive-aware intake**

Support reading from `/mnt/archive` and writing active work to `/mnt/projects`.

Dependencies:

* preprocessing adapters

Exit criteria:

* sample archive material can be ingested end to end up to preprocessed state

## **6.3 Milestone**

**M2 — Source intake and preprocessing stable**

## **6.4 Exit criteria**

* any supported source can enter the system  
* manifest exists  
* profile chosen  
* preprocessed artifacts created  
* source state advances to `preprocessed`

---

# **7\. Phase 3 — Intelligence execution and Merge Layer**

This is the highest-priority delivery phase because it is the main blocker identified in `STATE.md`.

## **7.1 Objective**

Turn preprocessed source inputs into valid draft `knowledge_record` objects by combining OCR, vision, and structured synthesis.

## **7.2 Epics**

### **Epic 3.1 — Router implementation**

Implement Router with:

* task classification  
* model tier selection  
* escalation logic  
* multi-pass flow  
* logging

Dependencies:

* runtime core  
* preprocessing complete

Exit criteria:

* tasks classified into canonical enums  
* lowest viable tier chosen by default  
* escalation path functional

### **Epic 3.2 — OCR adapter**

Implement OCR extraction service using Tesseract and integrate with source pipeline.

Dependencies:

* preprocessing

Exit criteria:

* OCR output captured per extraction unit  
* OCR artifacts stored and linked to source unit

### **Epic 3.3 — Vision adapter**

Implement vision extraction path using the current local model strategy, with source/model metadata captured. Local baseline includes InternVL3-8B as primary and Qwen2.5-VL-7B as fallback from recorded decisions.

Dependencies:

* preprocessing  
* router

Exit criteria:

* vision output captured per unit  
* model provenance logged

### **Epic 3.4 — Merge Layer**

Implement the missing merge stage:

`OCR + visual → structured synthesis → normalized record`

Responsibilities:

* combine OCR \+ vision  
* resolve conflicts  
* populate canonical record fields  
* surface uncertainty  
* generate retrieval text  
* create JSON \+ markdown draft record

Dependencies:

* OCR adapter  
* vision adapter  
* `knowledge_record` schema

Exit criteria:

* one extraction unit yields one valid draft `knowledge_record`  
* uncertainty fields populated where needed  
* merge logic produces consistent field mapping

### **Epic 3.5 — Output validation**

Implement validation checks for:

* required fields  
* unsupported claims  
* schema drift  
* hallucination indicators  
* missing uncertainty  
* malformed tags  
* structural integrity

Dependencies:

* merge layer

Exit criteria:

* invalid records are blocked  
* records route to `needs_review` or retry path  
* valid records saved as draft only

### **Epic 3.6 — Model runtime and comparison harness**

Build the environment to test model quality and compare outputs, including the Phase D immediate tasks from STATE:

* stabilize local model runtime  
* deploy larger multimodal model  
* compare output quality  
* validate before scaling

Dependencies:

* router  
* OCR/vision adapters

Exit criteria:

* model comparison workflow exists  
* chosen default model strategy documented in ADR or runtime config

## **7.3 Milestone**

**M3 — Merge Layer operational**

## **7.4 Exit criteria**

* OCR \+ vision \+ merge work on real files  
* draft records created with canonical schema  
* validation blocks low-quality output  
* system can process one real archive source into draft structured knowledge

---

# **8\. Phase 4 — Workbench vertical slice**

## **8.1 Objective**

Build the first user-facing interface that makes CIS usable without terminal-heavy interaction.

## **8.2 Scope**

This is **not** the full app. It is the first operator workbench.

## **8.3 Epics**

### **Epic 4.1 — Workbench shell**

Implement workbench with panels:

* Project Panel  
* Source Panel  
* Structure Panel  
* Review Panel  
* Knowledge Output Panel

Dependencies:

* runtime core  
* merge layer

Exit criteria:

* UI shell loads  
* active project context maintained  
* panel routing works

### **Epic 4.2 — Discovery-driven ingestion screen**

Implement the first “Ingest \+ Interpret \+ Refine” screen:

* left: source material  
* center: extracted \+ proposed structure  
* right: corrections  
* bottom: resulting knowledge object

Dependencies:

* workbench shell  
* merge layer

Exit criteria:

* user can ingest a file and see proposal, uncertainty, and resulting record

### **Epic 4.3 — Review and correction workflow**

Implement UI actions for:

* approve  
* reject  
* edit  
* mark uncertainty  
* merge categories  
* add missing fields

Dependencies:

* validation engine  
* workbench shell

Exit criteria:

* review actions update record state  
* corrections persist  
* approved records saved canonically

### **Epic 4.4 — Project-aware interaction**

Ensure all workbench actions are anchored to an active project. Project is the primary interface object.

Dependencies:

* project model  
* workbench shell

Exit criteria:

* no global orphan interactions  
* each source and record can be linked to project context

## **8.4 Milestone**

**M4 — First usable CIS surface exists**

## **8.5 Exit criteria**

A user can:

* create or select a project  
* ingest source material  
* trigger processing  
* review output  
* approve a record  
* save reusable knowledge

That is the first truly usable CIS.

---

# **9\. Phase 5 — Knowledge indexing and retrieval**

## **9.1 Objective**

Transform approved records into usable knowledge through indexing, chunking, and retrieval.

## **9.2 Epics**

### **Epic 5.1 — Metadata index**

Implement lightweight index with at least:

* title  
* type  
* tool  
* topic  
* location/path

Dependencies:

* approved records available

Exit criteria:

* index browsable and queryable

### **Epic 5.2 — Retrieval chunk generation**

Implement chunking from `retrieval_text` with required metadata:

* `record_id`  
* `chunk_id`  
* `chunk_text`  
* `knowledge_category`  
* `subject`  
* `tags`  
* `project_id`  
* `source_unit`  
* `model_used`  
* `version`

Dependencies:

* index  
* approved records

Exit criteria:

* chunk set generated per approved record  
* chunk lineage preserved

### **Epic 5.3 — Search and retrieval**

Implement retrieval over structured records, not raw files. Must support text, visual, teaching, and reference-oriented use cases.

Dependencies:

* chunks  
* index

Exit criteria:

* system can retrieve relevant records/chunks by project and query  
* approved records rank above drafts

### **Epic 5.4 — Knowledge normalization views**

Implement normalized views of canonical `knowledge_record` into:

* Research  
* Reference  
* Learning  
* Template  
* Checklist

Dependencies:

* retrieval/index

Exit criteria:

* canonical JSON preserved  
* UI/agents can consume normalized views

## **9.3 Milestone**

**M5 — Approved knowledge is searchable and reusable**

## **9.4 Exit criteria**

* approved records indexed  
* retrieval operational  
* project-linked knowledge can be found quickly  
* no reliance on raw-file browsing for known material

---

# **10\. Phase 6 — Reinforcement and structure stabilization**

## **10.1 Objective**

Enable CIS to improve proposal quality and structure quality through accepted outputs and corrections.

## **10.2 Epics**

### **Epic 6.1 — Reinforcement memory**

Store:

* accepted patterns  
* rejected patterns  
* common corrections  
* merged categories  
* accepted structures

Dependencies:

* workbench review flow  
* approved records

Exit criteria:

* correction memory persists across sessions

### **Epic 6.2 — Soft convergence engine**

Implement:

* tag merging  
* category stabilization  
* conflict resolution  
* promotion of repeated fields/categories to stable schema elements

Dependencies:

* reinforcement memory

Exit criteria:

* repeated corrections reduce future entropy  
* taxonomy fragmentation decreases over time

### **Epic 6.3 — Proposal quality scoring**

Define and implement acceptance criteria for:

* good proposal  
* bad proposal  
* accepted correction  
* reusable pattern

Dependencies:

* reinforcement memory  
* review system

Exit criteria:

* measurable proposal quality standard exists  
* future proposals can be evaluated against previous accepted outcomes

### **Epic 6.4 — Pattern-assisted future proposal generation**

Feed accepted patterns back into structure proposal generation. Only approved outputs may influence future structure.

Dependencies:

* proposal quality scoring  
* reinforcement memory

Exit criteria:

* future structure proposals improve measurably  
* drafts never directly become truth

## **10.3 Milestone**

**M6 — System improves through accepted use**

## **10.4 Exit criteria**

* accepted outputs alter future proposal behavior  
* correction patterns are remembered  
* structure convergence visible over repeated ingestion

---

# **11\. Phase 7 — Bounded agent modes**

## **11.1 Objective**

Expose structured assistance on top of stable knowledge and workflow.

## **11.2 Epics**

### **Epic 7.1 — Librarian mode**

Input:

* query  
* project context

Output:

* relevant tutorials  
* references  
* documents  
* assets

Dependencies:

* retrieval operational  
* project context available

Exit criteria:

* librarian can answer from approved knowledge only

### **Epic 7.2 — Researcher mode**

Input:

* idea/topic/project

Output:

* summaries  
* key concepts  
* directions  
* risks/limitations where relevant

Dependencies:

* librarian mode  
* retrieval operational

Exit criteria:

* researcher responses are grounded in structured knowledge and project context

### **Epic 7.3 — Teacher mode**

Input:

* tool question  
* concept  
* tutorial context

Output:

* step explanations  
* simplified actions  
* linked learning path

Dependencies:

* learning knowledge accessible  
* retrieval operational

Exit criteria:

* teacher does not generate instruction from unvalidated content  
* can recontextualize knowledge for current project

### **Epic 7.4 — Agent safety and sequencing**

Enforce:

* sequential role execution  
* explicit triggers  
* visible outputs  
* approval checkpoints where appropriate  
* forbidden action constraints

Dependencies:

* all agent modes

Exit criteria:

* agents cannot act autonomously outside approved scope  
* project-centered agent operation enforced

## **11.3 Milestone**

**M7 — Bounded assistants operational**

## **11.4 Exit criteria**

* at least two agent modes used in live project workflow  
* they reduce friction without destabilizing system behavior

---

# **12\. Phase 8 — Expanded application surface**

## **12.1 Objective**

Move from workbench to broader project-centered control surface.

## **12.2 Epics**

### **Epic 8.1 — Project system module**

Expose:

* project creation  
* project state  
* relationships  
* branching/merging  
* evolving outputs

### **Epic 8.2 — Knowledge browser**

Support:

* search  
* navigation  
* normalized views  
* project-linked browsing

### **Epic 8.3 — Workflow tracker**

Show:

* current stage  
* next steps  
* status across WIAS stages

### **Epic 8.4 — Intelligence controls**

Expose:

* model tier choice  
* cost/quality tradeoffs  
* task routing visibility

### **Epic 8.5 — Asset and output view**

Expose:

* renders  
* scenes  
* audio  
* exports  
* archive-return links

## **12.3 Milestone**

**M8 — Unified CIS control surface**

## **12.4 Exit criteria**

* project-centered system can be used through the app  
* app remains a thin layer over runtime and data model  
* no business logic duplicated in UI

---

# **13\. Immediate engineering backlog order**

This is the practical build order implied by the phases above.

1. repo \+ ADR baseline  
2. schemas and domain models  
3. state machines  
4. command layer  
5. control and logging  
6. source container \+ manifest  
7. processing profiles  
8. preprocessing adapters  
9. router  
10. OCR adapter  
11. vision adapter  
12. merge layer  
13. validation engine  
14. record save \+ versioning  
15. workbench shell  
16. ingest/interpret/refine screen  
17. review/promotion workflow  
18. metadata index  
19. chunk generation  
20. retrieval  
21. reinforcement memory  
22. convergence engine  
23. librarian/researcher/teacher modes  
24. broader application modules

This ordering is faithful to the docs and avoids phase drift.

---

# **14\. Required system deliverables by category**

## **14.1 Contracts**

* schemas for all core objects  
* state transition rules  
* validation rules  
* routing rules  
* review and promotion rules

## **14.2 Runtime**

* command handlers  
* orchestrator  
* adapter layer for OCR/vision/models  
* logging  
* approvals

## **14.3 Data**

* canonical JSON knowledge records  
* markdown mirrors  
* manifests  
* retrieval chunks  
* index

## **14.4 Interface**

* workbench v1  
* discovery screen  
* review screen  
* project-aware entrypoint

## **14.5 Intelligence**

* OCR  
* vision  
* merge  
* task routing  
* reinforcement memory

## **14.6 Governance**

* ADRs  
* phase alignment  
* control enforcement  
* state updates  
* handoff discipline

---

# **15\. Quality gates and milestone gates**

Each phase should have a formal gate review.

## **Gate A — Contract gate**

Before any subsystem build:

* contract exists  
* schema exists  
* success criteria defined

## **Gate B — Runtime gate**

Before UI work:

* commands work  
* state transitions work  
* logs exist  
* validation blocks bad output

## **Gate C — Knowledge gate**

Before retrieval:

* records approved  
* versioning works  
* canonical storage stable

## **Gate D — Reinforcement gate**

Before agents:

* accepted patterns stored  
* retrieval grounded  
* corrections stable

## **Gate E — Application gate**

Before broader UI:

* workbench proven  
* runtime stable  
* project system coherent

These gates follow your own build discipline: prove, stabilize, integrate, expand.

---

# **16\. Testing strategy**

## **16.1 Unit tests**

* schemas  
* state transitions  
* field mutability  
* merge logic  
* validation rules

## **16.2 Integration tests**

* ingest → preprocess  
* preprocess → OCR/vision  
* OCR/vision → merge  
* merge → validation → save  
* save → review → approval  
* approval → index → retrieve

## **16.3 Golden-record tests**

Maintain a benchmark set of real archive samples and compare:

* extracted fields  
* uncertainty behavior  
* retrieval quality  
* merge quality  
* correction rates

This is especially important because your docs define correctness as accepted, grounded, usable output rather than raw model confidence.

---

# **17\. Risks and mitigation**

## **17.1 Risk: build the full application too early**

Mitigation:

* keep application layer thin  
* workbench first  
* runtime first

## **17.2 Risk: let model output become truth**

Mitigation:

* approval-gated promotion  
* only approved outputs affect retrieval and reinforcement

## **17.3 Risk: taxonomy fragmentation**

Mitigation:

* soft convergence engine  
* accepted pattern memory  
* category merge rules

## **17.4 Risk: brittle workflow and phase drift**

Mitigation:

* STATE-driven execution  
* one active task  
* phase-to-stream mapping

## **17.5 Risk: over-tooling and losing system identity**

Mitigation:

* tools remain execution endpoints  
* intelligence/knowledge/application remain core center

---

# **18\. Recommended first implementation target**

Given the current STATE and the extracted architecture, the first build target should be:

## **Vertical Slice 1**

* create project  
* ingest one PDF or image from `/mnt/archive`  
* preprocess  
* run OCR  
* run vision  
* merge into draft `knowledge_record`  
* validate  
* review in workbench  
* approve  
* index  
* retrieve back into same project

This vertical slice is the smallest meaningful CIS implementation because it exercises:

* project system  
* source containers  
* manifest  
* runtime  
* intelligence  
* merge layer  
* validation  
* workbench  
* knowledge storage  
* retrieval

---

# **19\. Final construction summary**

The correct organized and efficient build plan is:

**Phase 0** freeze architecture and contracts  
 **Phase 1** build runtime core and controls  
 **Phase 2** build intake and preprocessing  
 **Phase 3** build intelligence routing and merge layer  
 **Phase 4** build workbench vertical slice  
 **Phase 5** build indexing and retrieval  
 **Phase 6** build reinforcement and convergence  
 **Phase 7** add bounded agent modes  
 **Phase 8** expand application surface

This is the cleanest plan that preserves all the implementable information in the CIS documents while turning it into a disciplined software delivery program.

The next concrete move is to turn this into a **Phase 0/1 implementation backlog** with actual tickets, acceptance criteria, and file/module structure.

if I wanted to add a project management layer and a digital assett manager to the structure how would it be fitted into the CIS Formal Phased Construction Plan

It fits cleanly, but **not as a new top-level replacement layer**.

A senior developer would add both as **bounded subsystems inside the existing Application \+ Workflow \+ Knowledge structure**, with clear ownership.

## **Short version**

* **Project Management layer** fits between **Workflow** and **Application**  
* **Digital Asset Management layer** fits between **Knowledge** and **Application**  
* Neither should bypass the canonical objects, runtime, or control rules

## **Best structural fit**

### **1\. Project Management Layer**

This should be added as a **project operations subsystem**.

It belongs to:

* **Primary home:** Application Layer  
* **Core dependencies:** Workflow Layer, Project object, State, Control  
* **Purpose:** planning, task visibility, milestones, dependencies, status, handoff

It should operate on top of the already-defined **Project as primary system object**. That means it does not invent a second project model. It extends the existing one with PM fields like:

* project status  
* milestones  
* tasks  
* blockers  
* assignee  
* due dates  
* dependencies  
* active phase  
* next action  
* review checkpoints

This is consistent with your docs because the project is already the main container for workflow, knowledge attachment, execution context, and outputs.

### **2\. Digital Asset Management Layer**

This should be added as an **asset intelligence subsystem**.

It belongs to:

* **Primary home:** Knowledge Layer  
* **Exposed through:** Application Layer  
* **Core dependencies:** Knowledge records, storage conventions, indexing, retrieval, workflow outputs

Its job is to manage:

* renders  
* images  
* scenes  
* audio  
* exports  
* reusable assets  
* versions  
* previews  
* metadata  
* project linkage  
* rights/usage notes if needed later

This should **not** be a separate silo. It should extend the canonical knowledge system so assets are either:

* a specialized `knowledge_record` category like `asset`  
* or an asset object linked tightly to canonical records and projects

That matches your docs, which already define assets as reusable knowledge-adjacent outputs and require outputs to feed back into the Knowledge Layer.

## **Where they go in the formal construction plan**

I would modify the plan like this:

### **Existing Phase 4 — Workbench vertical slice**

Add:

* basic PM fields on Project  
* basic asset preview and linkage in workbench

Not full PM, not full DAM. Just enough to support the first vertical slice.

### **Existing Phase 5 — Knowledge indexing and retrieval**

Expand to include:

* asset indexing  
* preview metadata  
* asset family relationships  
* project-linked asset retrieval

This is where the DAM foundation really begins.

### **Existing Phase 8 — Expanded application surface**

Split into clearer epics:

* **Epic 8.1 Project Management Module**  
  * milestone tracking  
  * task states  
  * blockers  
  * next-step queue  
  * project health  
* **Epic 8.2 Digital Asset Management Module**  
  * asset browser  
  * previews  
  * filtering  
  * versions  
  * reuse tracking  
  * output lineage

## **Recommended layer model update**

Instead of adding two new top-level layers, I would revise the application-facing architecture to this:

* **Knowledge Layer**  
  * records  
  * retrieval  
  * asset intelligence  
* **Workflow Layer**  
  * project flow  
  * stage movement  
  * execution sequencing  
* **Application Layer**  
  * workbench  
  * project management UI  
  * DAM UI  
  * agent UI  
  * workflow tracker

## **Important rule**

Do **not** let PM or DAM become parallel truth systems.

That means:

* PM must use the existing Project object  
* DAM must use the existing storage, naming, record, and project-link rules  
* both must defer to runtime, control, validation, and state rules

Otherwise CIS splits into disconnected apps.

## **Cleanest way to express it in the plan**

Add two new epics:

### **New Epic under Phase 5 or 8:**

**Project Management Subsystem**

* extends Project object with planning and execution metadata  
* exposes milestone/task/blocker views  
* remains project-centered and workflow-aware

### **New Epic under Phase 5 or 8:**

**Digital Asset Management Subsystem**

* indexes and manages outputs and reusable assets  
* preserves lineage to source, project, and knowledge  
* exposes previews, versions, and reuse paths

## **Best implementation order**

If you want these added without derailing CIS:

1. add minimal PM fields to Project schema  
2. add minimal asset metadata to `knowledge_record` / asset records  
3. add PM \+ asset panels to workbench  
4. add indexing/retrieval support  
5. only later build full PM and DAM modules

That is how a senior developer would fit them in cleanly without breaking the current architecture.

you made no specific mention of coding stacks or spcific LLMs that would be used on this proxmox local machine running on the 4090gpu and 7950x cpu 64 gb ram currently with update planned up to 128\. how are these tools indentified by a senior developer?

Thought

Thought

Thought

Thought

Thought for 55s

A senior developer identifies these tools by **role, constraint, and fit**, not by brand name first.

For your machine, the hardware profile is a strong local-LLM workstation: an RTX 4090 with 24 GB VRAM on Ada Lovelace, plus a Ryzen 9 7950X with 16 cores / 32 threads. Ada-class GPUs are also a good fit for vLLM’s FP8 path.

## **How a senior developer would identify the stack**

They would break the system into responsibilities:

1. **API/runtime layer**  
2. **job orchestration layer**  
3. **database and retrieval layer**  
4. **LLM serving layer**  
5. **OCR / multimodal extraction layer**  
6. **frontend workbench layer**

Then they choose the simplest tool that fits each responsibility and your hardware.

## **The concrete stack I would assign to CIS on this machine**

### **1\. Backend / application runtime**

Use **Python \+ FastAPI**.

Why:

* your intelligence, OCR, extraction, and orchestration work are already Python-shaped  
* FastAPI is production-ready, type-hint based, and generates OpenAPI docs automatically, which is ideal for a contract-first system like CIS.

In senior-dev terms, this would be the **service layer** that exposes:

* project APIs  
* source ingestion APIs  
* record review APIs  
* retrieval APIs  
* agent-mode APIs

### **2\. Primary database**

Use **PostgreSQL** as the system database.

Why:

* CIS has structured objects, versioning, relationships, review states, and project linkage  
* PostgreSQL natively supports `jsonb`, which fits your canonical JSON records well  
* PostgreSQL also has built-in full-text search.

In senior-dev terms, PostgreSQL would be the **system-of-record database** for:

* projects  
* manifests  
* knowledge records  
* review states  
* correction history  
* reinforcement memory  
* asset metadata

### **3\. Vector search**

Use **pgvector on PostgreSQL** first.

Why:

* it keeps vectors in the same database as the rest of your system data  
* it supports exact and approximate nearest-neighbor search  
* it avoids prematurely splitting CIS into too many storage systems.

That is exactly how a senior developer would keep the first version organized: **one primary database, not three competing truth sources**.

### **4\. Queue / background jobs**

Use **Redis-backed jobs** only when needed, not as day-one complexity.

Why:

* Redis supports queue patterns and durable persistence options  
* it fits background tasks like preprocessing, OCR, vision extraction, chunking, and embedding.

For CIS, this means:

* Phase 1–3: synchronous or simple local worker execution is acceptable  
* Phase 4+: add Redis job queues once ingestion volume or UI responsiveness requires it

### **5\. LLM serving layer**

Use **two local serving runtimes**, not one:

#### **Primary high-performance runtime: vLLM**

Use this for:

* heavier text reasoning  
* larger open models  
* structured serving  
* batch inference  
* model comparison work

Why:

* vLLM supports GPU serving and supported-model loading  
* FP8 support is especially aligned with Ada Lovelace GPUs like the 4090\.

#### **Secondary convenience runtime: Ollama**

Use this for:

* simple local serving  
* developer convenience  
* quick agent-mode experiments  
* OpenAI-compatible local APIs for lightweight integration.

Senior-developer framing:

* **vLLM \= production inference runtime**  
* **Ollama \= convenience/dev runtime**

### **6\. Fallback local inference runtime**

Use **llama.cpp** as a fallback utility runtime, not the main CIS core.

Why:

* it is excellent for minimal-setup local inference  
* it supports multimodal input, but its multimodal path is still more limited and sometimes more awkward than a Transformers/vLLM path for serious VLM work.

Senior-developer framing:

* **llama.cpp \= utility / fallback / lightweight deployment**  
* not your primary multimodal production runtime

## **The specific LLM / VLM choices a senior developer would label for this hardware**

They would not say “an AI model.” They would assign **roles**.

### **A. Primary local multimodal extraction model**

**InternVL3-8B**  
Role: grounded page and image interpretation, visual structure extraction.

This matches your extracted docs and your own benchmark notes.

### **B. Fallback local multimodal model**

**Qwen2.5-VL-7B-Instruct**  
Role: fallback VLM for visual QA and extraction when the primary model underperforms on a file family. The official model card identifies it as the 7B instruction-tuned Qwen2.5-VL model.

### **C. Higher-quality multimodal reasoning tier**

**Qwen2.5-VL-32B-Instruct**  
Role: higher-quality multimodal interpretation, difficult extraction, and tougher structure proposals. Qwen’s official model page describes the 32B model as having reinforced mathematical and problem-solving ability and improved response quality.

Senior-developer caveat: on a 24 GB 4090, a 32B multimodal model is a **selective high-quality tier**, not the always-on default. That is an engineering inference based on your VRAM budget and the existence of smaller 7B multimodal variants plus quantized/open deployment paths.

### **D. Primary local text reasoning model**

**Qwen2.5-32B-Instruct-AWQ**  
Role: structured reasoning, planning, extraction cleanup, schema filling, and workbench proposal generation. The AWQ 4-bit model exists specifically for deployment efficiency.

### **E. Secondary reasoning model for harder reasoning workflows**

**DeepSeek-R1-Distill-Qwen-32B**  
Role: harder reasoning tasks, comparison runs, and structured synthesis experiments. The official card positions it as a high-performing dense reasoning model.

## **So how would these be identified in the actual CIS plan?**

A senior developer would write them like this:

### **Inference stack**

* **Serving runtime:** vLLM  
* **Convenience runtime:** Ollama  
* **Fallback lightweight runtime:** llama.cpp

### **Model tiers**

* **Tier V1 (default visual extraction):** InternVL3-8B  
* **Tier V1 fallback:** Qwen2.5-VL-7B-Instruct  
* **Tier V2 high-quality multimodal:** Qwen2.5-VL-32B-Instruct  
* **Tier R1 default reasoning:** Qwen2.5-32B-Instruct-AWQ  
* **Tier R2 reasoning comparison:** DeepSeek-R1-Distill-Qwen-32B

### **Application stack**

* **Backend:** Python \+ FastAPI  
* **Database:** PostgreSQL  
* **Vector search:** pgvector  
* **Optional job queue:** Redis  
* **Frontend:** project-centered workbench UI calling the FastAPI backend

## **The naming convention a senior dev would use**

They usually identify tools by **system responsibility**, not by app names alone.

So instead of:

* “use Qwen”  
* “use FastAPI”  
* “use Postgres”

they define:

* **API service**  
* **record store**  
* **vector retrieval store**  
* **job queue**  
* **multimodal extraction runtime**  
* **reasoning runtime**  
* **review workbench**

Then they assign concrete tools to those roles.

That is the clean way to keep CIS from becoming a pile of disconnected components.

## **My direct recommendation for your machine**

For your current hardware, I would identify the stack like this:

* **Core backend:** Python \+ FastAPI  
* **Primary DB:** PostgreSQL \+ pgvector  
* **Async jobs:** Redis later, not first  
* **Primary inference runtime:** vLLM  
* **Convenience local API runtime:** Ollama  
* **Primary visual model:** InternVL3-8B  
* **Fallback visual model:** Qwen2.5-VL-7B-Instruct  
* **High-quality visual tier:** Qwen2.5-VL-32B-Instruct, selectively  
* **Primary reasoning model:** Qwen2.5-32B-Instruct-AWQ  
* **Secondary reasoning model:** DeepSeek-R1-Distill-Qwen-32B

That is how a senior developer would identify the tools: **by responsibility, deployment role, and hardware fit**.

The next useful step is to rewrite the CIS construction plan with a new section called **“Target Technical Stack and Model Allocation”** so every phase names the exact runtimes, databases, APIs, and model tiers to use.

To build CIS the way it’s defined in your documents, you’re not assembling a generic “app dev team.” You’re assembling a **systems engineering \+ AI infrastructure \+ creative production hybrid team**.

A senior developer would map this directly to the responsibilities in your system:

* **Runtime (commands, state, validation)**  
* **Intelligence (OCR, vision, merge)**  
* **Knowledge (records, indexing, retrieval)**  
* **Application (workbench UI)**  
* **Workflow \+ Project system**  
* **Assets \+ outputs (creative tools integration)**

From that, the skillsets fall out very clearly.

---

# **🧠 1\) Systems Architect (You already started this role)**

This is the most important role in CIS.

### **What they actually do**

* Define **contracts, schemas, and object models**  
* Enforce **Input → Process → Validation → Output → State Change**  
* Own **phase alignment and system integrity**  
* Prevent “tool chaos”

### **Skills**

* Systems thinking  
* Software architecture patterns  
* Data modeling (JSON schemas, versioning)  
* Ability to translate ideas → enforceable contracts

### **Why this role exists in CIS**

Because your system is **contract-first and discovery-driven**, not tool-first.

👉 Without this role, CIS collapses into disconnected scripts.

---

# **⚙️ 2\) Backend / Platform Engineer**

This is the **core builder of the system engine**.

### **What they build**

* FastAPI services  
* Command layer (`source.ingest`, `record.merge`, etc.)  
* State machines  
* Validation engine  
* Logging \+ control layer

### **Skills**

* Python (advanced)  
* API design (FastAPI)  
* Data modeling (Pydantic, SQLAlchemy)  
* State machines  
* Testing \+ observability

### **Why this role exists**

Because CIS is fundamentally a **runtime system**, not just an app UI.

---

# **🧠🤖 3\) AI / ML Engineer (Multimodal \+ LLM Systems)**

This role is **not generic “AI”** — it is specifically:

👉 **multimodal extraction \+ model orchestration**

### **What they build**

* OCR \+ vision pipelines  
* Model routing (7B vs 32B vs fallback)  
* Prompt \+ structured output design  
* Merge layer logic (OCR \+ vision → record)

### **Skills**

* Hugging Face / Transformers  
* vLLM / Ollama / local inference  
* Prompt engineering (structured outputs, not chat)  
* Evaluation \+ benchmarking  
* Multimodal understanding (images, text, video)

### **Why this role exists**

Because your system depends on:

👉 **AI proposing structured knowledge, not just answering questions**

---

# **🔄 4\) Data / Knowledge Engineer**

This is one of the most critical and most overlooked roles.

### **What they build**

* `knowledge_record` schema enforcement  
* Indexing \+ retrieval (pgvector, chunking)  
* Metadata systems  
* Reinforcement memory  
* Taxonomy stabilization

### **Skills**

* Data modeling  
* Search systems (vector \+ structured)  
* Information architecture  
* JSON pipelines  
* ETL thinking (extract → transform → normalize)

### **Why this role exists**

Because CIS is:

👉 **a knowledge system first, not a file system**

---

# **🖥 5\) Frontend / Workbench Engineer**

This role builds the **actual human interface to CIS**.

### **What they build**

* Workbench panels:  
  * Project  
  * Source  
  * Structure  
  * Review  
  * Output  
* Ingest → Interpret → Refine UI  
* Review \+ approval flows

### **Skills**

* React / Next.js  
* State management  
* UI for complex workflows (not marketing sites)  
* API integration  
* UX thinking for **decision systems**

### **Why this role exists**

Because CIS requires:

👉 **human validation at the center of the loop**

---

# **🧪 6\) QA / Validation Engineer (CRITICAL for CIS)**

This is NOT optional in your system.

### **What they build**

* Validation rules:  
  * required fields  
  * hallucination detection  
  * schema integrity  
* Test pipelines:  
  * ingest → preprocess → extract → merge → validate  
* Golden dataset comparisons

### **Skills**

* Testing frameworks  
* Data validation  
* Edge-case analysis  
* Systems thinking

### **Why this role exists**

Because CIS explicitly requires:

👉 **invalid outputs must FAIL, not pass silently**

---

# **🧰 7\) DevOps / Infrastructure Engineer**

This role makes your **local AI system actually stable and scalable**.

### **What they manage**

* Proxmox \+ VM setup  
* GPU passthrough  
* Docker / containers  
* model serving (vLLM, Ollama)  
* storage mounts (`/mnt/projects`, `/mnt/archive`)  
* performance tuning

### **Skills**

* Linux systems  
* NVIDIA / CUDA stack  
* containerization  
* networking  
* monitoring

### **Why this role exists**

Because CIS is:

👉 **a local-first, GPU-dependent system**, not SaaS

---

# **🎨 8\) Creative Technologist / Pipeline Integrator**

This is a **very CIS-specific role**.

### **What they do**

* Connect CIS to:  
  * Blender  
  * Houdini  
  * Unreal  
  * ComfyUI  
* Define:  
  * output formats  
  * asset pipelines  
  * reusable templates

### **Skills**

* 3D / motion / VFX tools  
* scripting (Python, node, tool APIs)  
* pipeline design  
* asset workflows

### **Why this role exists**

Because CIS is not just knowledge—it drives:

👉 **real creative production outputs**

---

# **📊 9\) Product / Workflow Designer**

This role ensures the system is actually usable.

### **What they define**

* Workflow states (Idea → Source → Knowledge → Output)  
* Project structure  
* Task sequencing  
* User flows for coworkers

### **Skills**

* Product thinking  
* UX systems  
* workflow design  
* documentation

### **Why this role exists**

Because CIS must pass the:

👉 **“coworker test” — usable without explanation**

---

# **🧠 10\) Optional (Later Phase): Agent Systems Engineer**

This comes after Phase 6–7.

### **What they build**

* Librarian agent  
* Researcher agent  
* Teacher agent  
* Routing \+ constraints

### **Skills**

* LLM orchestration  
* tool-use patterns  
* prompt chaining  
* guardrails

### **Why this role exists**

Because agents are:

👉 **bounded assistants, not autonomous systems**

---

# **🧩 How a Senior Developer Thinks About This Team**

They do NOT think:

“we need frontend, backend, AI”

They think:

### **System Responsibility → Skillset**

| System Layer | Required Skillset |
| ----- | ----- |
| Runtime | Backend engineer |
| Intelligence | AI/ML engineer |
| Knowledge | Data engineer |
| Interface | Frontend engineer |
| Validation | QA engineer |
| Infrastructure | DevOps |
| Production tools | Creative technologist |
| System integrity | Architect |

---

# **⚠️ The Most Important Insight**

CIS requires **two uncommon combinations**:

### **1\. AI \+ Systems (not just AI)**

Most teams fail here.

You need:

* structured outputs  
* validation  
* routing  
* merge logic

NOT just “call GPT.”

---

### **2\. Creative \+ Engineering (not just software)**

Most engineering teams fail here.

You need:

* asset pipelines  
* production outputs  
* reusable creative knowledge

NOT just CRUD apps.

---

# **🧠 Realistically (Lean Team Version)**

You do NOT need 10 people to start.

A strong v1 team could be:

* **You (Architect \+ Product \+ Creative Technologist)**  
* **1 Backend/Platform Engineer**  
* **1 AI/ML Engineer**  
* **1 Frontend Engineer**

Optional early:

* DevOps (part-time or you handle initially)

---

# **🔑 Final takeaway**

The CIS team is best understood as:

👉 **a systems engineering team that builds a knowledge-forming AI runtime for creative production**

Not:

* a startup app team  
* a pure AI team  
* a design team

If you hire or think in those categories, the system will break.

## **Building a Stream Deck-style UI**

## is a great way to create a high-density, tactile-feeling dashboard for your local infrastructure. Since you’re running this in an Ubuntu VM on Proxmox, you have the flexibility to host a web-based frontend that you can access from any device.

1. The Tech Stack Recommendation For a responsive, "grid-of-buttons" feel that integrates with local scripts and databases, a Node.js/React or Vue frontend paired with a Python (FastAPI) backend is ideal.

Frontend: React with Tailwind CSS. Tailwind's grid system makes replicating the 8×4 or 5×3 button layouts effortless.

Backend: FastAPI. It’s lightweight and excellent for executing local shell scripts (to launch programs) or handling file uploads to your Qdrant/ChromaDB instances.

Communication: WebSockets (Socket.io). This allows the UI to update in real-time (e.g., showing CPU load or agent status) without refreshing.

2. UI/UX Architecture: The "Button" Component To get the aesthetic from your images, each button should be a modular component.

Glassmorphism: Use semi-transparent backgrounds with a slight blur to mimic the glowing LCD keys.

Stateful Icons: Icons should change color or animate based on whether a service (like an AI agent) is active.

Active Feedback: Implement a slight scale(0.95) transform on click to simulate a physical button press.

HTML

Start Agent

3\. Implementing the Functional Panels You can use a Tabs or Folder system to switch between your specific workflows: Panel	Primary Functionality Project Management	Integration with your Obsidian vault or a simple Kanban API. Digital Asset Mgmt	A "Drop Zone" button that triggers a script to move files to your 6-pillar storage. Local AI Chat	An embedded window or a button that opens a dedicated "Librarian" chat interface. Agent Dashboard	Start/Stop buttons for LangGraph or CrewAI processes with status LEDs. 4\. Backend Integration in Proxmox Since your frontend is in an Ubuntu VM, you need a way to "reach out" to the rest of your system:

Opening Programs: Use Python’s subprocess module to trigger scripts. If the app is GUI-based and running on the same VM, ensure your DISPLAY environment variable is set correctly.

Database Uploads: For your legacy "refinery" process, the "Upload" button can POST a file to a FastAPI endpoint, which then runs your existing indexing scripts for Qdrant.

Agent Control: Use PM2 (Process Manager 2\) to manage your AI agents. Your dashboard can send commands to PM2 to start, stop, or restart specific agentic workflows.

Add streamdeck images in obsidian as links.

![[streamdeck_01.png]]![[streamdeck_02.png]]