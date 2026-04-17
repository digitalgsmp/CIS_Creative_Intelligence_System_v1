# CIS Session Handoff — Insight Capture System
## Priority: HIGH — Knowledge is being lost in chat

---

## The problem

CIS is its own first project. The most valuable knowledge being generated right now is in chat exchanges — architectural realizations, extraction quality observations, workflow discoveries. None of this is being captured in the knowledge base. The correction log captures field-level corrections but not conceptual insights.

Examples of insights lost or nearly lost today:
- Comic illustration uses visual shorthand requiring different extraction standards (ADR-011, captured)
- The impact line / rifle-axe collision ambiguity — discovered only because we were actively reviewing
- "Models are components not solutions" — stated in chat, not in database
- "Intake triggers knowledge formation" — stated in chat, not in database
- The discovery that CIS is its own first project — stated now, not captured anywhere

---

## What to build

### 1. Add insight subcommand to cis-log

New command:
```
cis-log insight "category" "title" "observation" --session "optional session ref"
```

Categories: architectural | extraction | workflow | system | quality | discovery

New database table needed:
```sql
CREATE TABLE insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    title TEXT NOT NULL,
    observation TEXT NOT NULL,
    session_ref TEXT,
    source_material TEXT,
    created_at TEXT NOT NULL
)
```

### 2. Add insight display to cis-start

cis-start should show last 3 insights at session open so they are not forgotten.

### 3. Retroactively capture insights from this session

The following insights should be logged immediately in the next session:

**INSIGHT-001**
Category: extraction
Title: Comic illustration visual language requires ambiguity-aware standards
Observation: Golden/Silver Age comic illustration uses symbolic shorthand designed for culturally fluent human readers. Impact lines, stylized action, compressed narrative cannot be interpreted by a model the way a trained human reader interprets them. The uncertainty field must surface genuine ambiguity rather than defaulting to None. This is not a model failure — it is a source material characteristic.

**INSIGHT-002**
Category: system
Title: CIS build process is CIS Project 001
Observation: The process of designing and building CIS is itself a CIS project. Every architectural decision, workflow discovery, extraction correction, and realtime observation is knowledge generated through the Intelligence → Knowledge loop. The system should treat its own construction as source material. This means the chat sessions, ADR records, and correction logs are the first corpus of structured knowledge in the system.

**INSIGHT-003**
Category: workflow
Title: Realtime insights require intentional capture mechanism
Observation: Without a dedicated capture path, conceptual insights generated during active work are lost. The correction log is too narrow (field-level only). A separate insight table with session reference, category, and free-text observation is needed. The minimal dashboard must include an insight capture panel as a first-class feature, not an afterthought.

**INSIGHT-004**
Category: architectural
Title: Minimal operator dashboard is Phase 1 priority, not Phase 5
Observation: The current terminal-only workflow places too much cognitive and execution burden on the human operator. A simple Flask dashboard with pipeline command buttons, record review panels, and insight capture should be built as the first Phase 1 deliverable. This is not application layer work — it is operator tooling that makes the pipeline usable without expert knowledge.

**INSIGHT-005**
Category: extraction
Title: Visual symbolic shorthand creates systematic model ambiguity
Observation: The Weird War Tales cover extraction misidentified the caveman as a tribal warrior and failed to identify the rifle being cut by the stone axe during impact. Both errors are understandable given that: (1) the caveman character uses visual shorthand common to the era's genre conventions, and (2) the impact collision is represented by symbolic strokes that even human observers misread on first pass. This class of error — culturally-encoded visual shorthand — will recur across the archive and requires systematic handling, not case-by-case correction.

---

## Start this session with

Run on Ubuntu VM: cis-start
Paste cis-start output + this document as opening message.
Tell Claude: "Add the insight subcommand to cis-log, update cis-start to show recent insights, then log the five retroactive insights in this document."
