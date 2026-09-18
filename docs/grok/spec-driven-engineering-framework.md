# Adaptive spec-driven engineering framework for development

Design visualization of how a **project-agnostic core** becomes a **project-specific engineering system**, then carries selected work from intent to qualified candidate without treating a chat prompt as the source of truth.

Governing planning documents: [framework index](../specs/framework/index.md), [foundation](../specs/framework/foundation.md), [core workflows](../specs/framework/core-workflows.md), [work items](../specs/framework/work-items-and-dependencies.md), [project context and policy](../specs/framework/project-context-and-policy.md), [skills and expertise](../specs/framework/skills-and-project-expertise.md), [quality and delivery](../specs/framework/quality-and-delivery.md).

This file does not install skills, enforce gates, or issue acceptance. Python, Markdown, and mermaid are evidence of design intent only.

## 1. What the diagrams are showing

Three layers sit under every product-development step:

| Layer | What it supplies | What it does not supply |
| --- | --- | --- |
| **Core workflows** | Reusable methods and document handoffs | Product facts, language, layout, quality numbers |
| **Project policy and expertise** | This project's stack, standards, domain rules | Permission to weaken policy or accept a candidate |
| **Guardrails** | Protected checks and receipts when the Rust authority exists | Successful reasoning, or a substitute PASS when authority is absent |

**Adaptive** means: install the same cores in any project, then *discover* that project's conventions, *select* a skill set, and *specialize* only when a variant or expertise package has a distinct evidenced responsibility. See the conversation-level definition in [skills and project expertise](../specs/framework/skills-and-project-expertise.md).

**Spec-driven** means: the selected specification (and its derived story/architecture/policy documents) is the oracle. Implementation, tests, and QA are consumers of that oracle. A later passing test does not rewrite the spec.

## 2. Skill and command map

Invocation names are conversational skill selections, not claimed CLI binaries. Legacy Claude slash commands are shown only as historical entry points; they are not the forward Codex contract.

| Step | Capability | Skill | Command / mode | Status | Document templates |
| --- | --- | --- | --- | --- | --- |
| 0 | Adapt core to project | `skill-builder` | `propose`, then `author_set` | Current | [adaptation-proposal.md](templates/adaptation-proposal.md) |
| 0b | Assess skill packages | `skill-validator` | standalone or set validation | Current | validator report (skill QA, not product QA) |
| 1 | Discover problem | planned core `discover` | planned; legacy `/brainstorm`, `/research` | Planned core | [business-analysis.md](templates/business-analysis.md), [research-finding.md](templates/research-finding.md) |
| 2 | Specify product | planned core `specify` | planned; legacy `/ideate` | Planned core | [product-requirements.md](templates/product-requirements.md) |
| 3 | Architect | planned core `architect` | planned; legacy `/create-system-architecture` | Planned core | [system-architecture.md](templates/system-architecture.md), [project-policy.md](templates/project-policy.md) |
| 4 | Plan work | `story-create` | story / batch authoring | Current | [work-set.md](templates/work-set.md), [story.md](templates/story.md) |
| 5 | Implement | `dev` | implement selected specs/stories | Current | [development-context.md](templates/development-context.md), [development-slice-plan.md](templates/development-slice-plan.md), [development-traceability.md](templates/development-traceability.md), [development-delivery.md](templates/development-delivery.md) |
| 6 | Assess independently | `qa` | `run` / `plan` / `execute` / `retest` | Current | [qa-test-plan.md](templates/qa-test-plan.md), [qa-report.md](templates/qa-report.md), [qa-fix.md](templates/qa-fix.md) |
| 7 | Deliver | planned core `release` | planned; legacy `/release` | Planned core | [release-record.md](templates/release-record.md) |
| 8 | Follow up | planned cores `feedback`, `rca` | planned; legacy `/feedback`, `/rca` | Planned core | [feedback.md](templates/feedback.md), [rca.md](templates/rca.md) |
| * | Resume / interrupt | all product skills | checkpoint on stop | Current in `dev`/`qa` | [checkpoint.md](templates/checkpoint.md) |

`advisor` is an optional second-opinion skill. It produces evidence only. It does not author product documents or accept work.

## 3. Overview: entry points, not a waterfall

An adequate existing specification may enter at work planning or development. An uncertain idea starts at discovery. A confirmed QA defect returns to `dev` with a fix packet. Interrupted work resumes from a checkpoint. Optional services (index, MCP, Git, plugin) are never prerequisites of the core.

```mermaid
flowchart TB
  subgraph Adapt["Layer A — make the core this project's framework"]
    SB["skill-builder<br/>propose / author_set"]
    BIND["Operational binding<br/>.agents/devforgeai/project-binding.json"]
    POL["Project policy and facts<br/>language, layout, quality, domain"]
    EXP["Selected cores / variants / expertise"]
    SB --> BIND
    SB --> EXP
    POL --> EXP
  end

  subgraph Enter["Layer B — selected entry, not a required sequence"]
    E1["Uncertain idea"]
    E2["Specified change"]
    E3["Defect or QA finding"]
    E4["Interrupted work"]
  end

  subgraph Life["Layer C — product lifecycle capabilities"]
    D1["1 Discover"]
    D2["2 Specify"]
    D3["3 Architect"]
    D4["4 Plan work"]
    D5["5 Implement"]
    D6["6 Assess"]
    D7["7 Deliver"]
    D8["8 Follow up"]
    D1 --> D2 --> D3 --> D4 --> D5 --> D6 --> D7 --> D8
  end

  EXP --> Enter
  E1 --> D1
  E2 --> D4
  E2 --> D5
  E3 --> D5
  E4 --> Life

  D6 -->|"FAIL: qa-fix packet"| D5
  D6 -->|"PASS: delivery review"| D7
  D8 -->|"new selected work"| D1
  D8 -->|"new story"| D4
  D5 -.->|"spec gap / contradiction"| D2
  D6 -.->|"oracle conflict"| D2
  D3 -.->|"missing business rule"| D1

  subgraph Guard["Layer D — distinct decisions"]
    CAND["Candidate delivered"]
    CHK["Checks completed"]
    QAV["QA assessment"]
    RDY["Delivery readiness"]
    ACC["Framework acceptance<br/>Rust authority only"]
    REL["Release authorization"]
  end

  D5 --> CAND
  CAND --> CHK
  CHK --> QAV
  QAV --> RDY
  RDY --> ACC
  ACC --> REL
```

A later box is not implied by an earlier one. Passing developer tests is not QA. A QA PASS is not release authorization. Missing Rust authority is `NOT_EVALUATED` / unavailable, not a Markdown PASS.

## 4. Adaptation layer (why the core can be installed anywhere)

The reusable packages contain no project UUID and no hardcoded language or quality floor. Adaptation *recommends a skill set* from bounded project evidence, then a separately authorized setup writes the operational binding.

```mermaid
flowchart LR
  subgraph Upstream0["Upstream"]
    U0A["Selected project root"]
    U0B["Root instructions, manifests, docs"]
    U0C["Existing skills if any"]
    U0D["User request: propose a set"]
  end

  subgraph WF0["Workflow"]
    C0["Command: skill-builder propose"]
    S0["Skill: skill-builder core"]
    T0["Template: adaptation-proposal"]
    C0 --> S0 --> T0
  end

  subgraph Docs0["Documents produced"]
    EV["project-evidence-v1"]
    PROP["adaptation-proposal-v1"]
    REP["adaptation-report.md"]
  end

  subgraph Down0["Downstream"]
    HUM["Human selection<br/>adaptation-selection-v1"]
    AUT["Command: skill-builder author_set"]
    VAL["Manual skill-validator request"]
    SETUP["Separate setup: project-binding-v1"]
    PROD["Product workflows<br/>discover / specify / story-create / dev / qa"]
  end

  U0A --> C0
  U0B --> C0
  U0C --> C0
  U0D --> C0
  T0 --> EV
  T0 --> PROP
  T0 --> REP
  PROP --> HUM
  HUM --> AUT
  AUT --> VAL
  AUT --> SETUP
  SETUP --> PROD
  VAL -.->|"findings, no auto-repair"| HUM
  PROD -.->|"unmet responsibility"| C0
```

Rules encoded in this expansion:

- `core` discovers conventions; it does not invent a stack.
- `project_variant` keeps parent bytes and a lineage row per parent requirement.
- `expertise` needs distinct ownership and domain evidence; a job title is not a package.
- Binding is operational identity. Portable source must not embed it.
- `skill-validator` assesses the packages. It does not implement the product and does not invoke the builder.

## 5. Step expansions

Each expansion uses the same shape: **upstream → command/skill/template → documents → downstream**, plus dotted **return** paths.

### 5.1 Discover — business analysis and research

**Purpose:** agree what problem is being solved, for whom, and which outcomes/uncertainties exist. A small defect with an existing contract skips this step.

**Skill:** planned core `discover`. Supporting: planned `research`. Legacy: `/brainstorm`, `/research`.

```mermaid
flowchart LR
  subgraph Up1["Upstream"]
    U1A["User problem / observation"]
    U1B["Current product behavior"]
    U1C["Stakeholders and constraints"]
    U1D["Optional: research-finding"]
    U1E["Optional: prior feedback / RCA"]
  end

  subgraph WF1["Workflow"]
    C1["Command: discover<br/>optional: research"]
    S1["Skill: discover core<br/>optional expertise: domain"]
    T1A["Template: business-analysis"]
    T1B["Template: research-finding"]
    C1 --> S1
    S1 --> T1A
    S1 --> T1B
  end

  subgraph Doc1["Documents"]
    BA["Business analysis"]
    RF["Research finding<br/>when investigation was selected"]
    G1["Gap record: missing decisions"]
  end

  subgraph Down1["Downstream"]
    SP["specify → product-requirements"]
    AR["architect if boundaries already known"]
    ASK["Ask user: material unknowns"]
  end

  U1A --> C1
  U1B --> C1
  U1C --> C1
  U1D --> C1
  U1E --> C1
  T1A --> BA
  T1B --> RF
  S1 --> G1
  BA --> SP
  RF --> SP
  BA --> AR
  G1 --> ASK
  ASK --> C1
  SP -.->|"requirement contradicts discovery"| BA
  AR -.->|"missing business rule"| BA
```

**Handoff contract:** downstream needs agreed outcomes, in/out of scope, stakeholder conflicts, and named uncertainties. It does not need a persona essay. Unanswered race/eligibility questions block only dependent behavior, not unrelated confirmed work.

### 5.2 Specify — product requirements

**Purpose:** turn agreed outcomes into testable requirements, exclusions, and acceptance scenarios. This document is an implementation target, not proof that the software exists.

**Skill:** planned core `specify`. Legacy: `/ideate`.

```mermaid
flowchart LR
  subgraph Up2["Upstream"]
    U2A["Business analysis"]
    U2B["Research findings"]
    U2C["User corrections"]
    U2D["Existing specs to reuse"]
  end

  subgraph WF2["Workflow"]
    C2["Command: specify"]
    S2["Skill: specify core"]
    T2["Template: product-requirements"]
    C2 --> S2 --> T2
  end

  subgraph Doc2["Documents"]
    PRD["Product requirements"]
    EX2["Exclusions and deferred capabilities"]
  end

  subgraph Down2["Downstream"]
    AR2["architect"]
    WS2["plan work / story-create"]
    DEV2["dev, if architecture already exists"]
  end

  U2A --> C2
  U2B --> C2
  U2C --> C2
  U2D --> C2
  T2 --> PRD
  T2 --> EX2
  PRD --> AR2
  PRD --> WS2
  PRD --> DEV2
  AR2 -.->|"interface needs a product decision"| C2
  WS2 -.->|"clause cannot be owned"| C2
  DEV2 -.->|"failed tests do not rewrite expected behavior"| PRD
```

**Handoff contract:** every normative clause has a stable ID, observable acceptance, failure behavior, and explicit out-of-scope. Examples are labeled examples. Historical claims are labeled historical. `dev` must not treat a proposed command signature as an existing executable.

### 5.3 Architect — system design and project policy

**Purpose:** lock boundaries, interfaces, state ownership, and the quality/stack policy this project actually uses. Policy is selected, not inherited from DevForgeAI's own 95%/Rust rules unless this project *is* DevForgeAI.

**Skill:** planned core `architect`. Legacy: `/create-system-architecture`.

```mermaid
flowchart LR
  subgraph Up3["Upstream"]
    U3A["Product requirements"]
    U3B["Business analysis"]
    U3C["Current source and manifests"]
    U3D["User stack / policy decisions"]
  end

  subgraph WF3["Workflow"]
    C3["Command: architect"]
    S3["Skill: architect core"]
    T3A["Template: system-architecture"]
    T3B["Template: project-policy"]
    C3 --> S3
    S3 --> T3A
    S3 --> T3B
  end

  subgraph Doc3["Documents"]
    SAD["System architecture"]
    POL3["Project policy<br/>stack, tests, platforms, effects"]
  end

  subgraph Down3["Downstream"]
    WS3["plan work"]
    ST3["story-create"]
    DV3["dev"]
    QA3["qa"]
    RL3["release"]
  end

  U3A --> C3
  U3B --> C3
  U3C --> C3
  U3D --> C3
  T3A --> SAD
  T3B --> POL3
  SAD --> WS3
  SAD --> ST3
  SAD --> DV3
  POL3 --> DV3
  POL3 --> QA3
  POL3 --> RL3
  DV3 -.->|"implementation contradicts boundary"| SAD
  QA3 -.->|"policy missing metric rule"| POL3
  WS3 -.->|"shared contract has two owners"| SAD
```

**Handoff contract:** one owner per shared interface. Concurrency, data, and authority boundaries are explicit. Quality measures name numerator, denominator, exclusions, and required platforms. An expert recommendation cannot lower a floor.

### 5.4 Plan work — work set and stories

**Purpose:** decompose selected requirements into independently assessable stories without fragmenting a specification into one file per paragraph, platform, or TDD phase.

**Skill:** current `story-create`. Planned companion: work-set / epic planner. Legacy: `/create-story`, `/create-sprint`.

```mermaid
flowchart LR
  subgraph Up4["Upstream"]
    U4A["Product requirements"]
    U4B["System architecture"]
    U4C["Project policy"]
    U4D["QA / RCA recommendations"]
    U4E["Deferred-work gaps"]
  end

  subgraph WF4["Workflow"]
    C4["Command: story-create<br/>optional work-set pass"]
    S4["Skill: story-create core"]
    T4A["Template: work-set"]
    T4B["Template: story"]
    C4 --> S4
    S4 --> T4A
    S4 --> T4B
  end

  subgraph Doc4["Documents"]
    WS["Work set / epic map"]
    ST["One .story.md per story"]
    DEP["Producer/consumer dependencies"]
  end

  subgraph Down4["Downstream"]
    DV4["dev — selected stories/specs"]
    QA4["qa — same selected IDs"]
    HUM4["Human: select implementation scope"]
  end

  U4A --> C4
  U4B --> C4
  U4C --> C4
  U4D --> C4
  U4E --> C4
  T4A --> WS
  T4B --> ST
  S4 --> DEP
  WS --> HUM4
  ST --> HUM4
  HUM4 --> DV4
  ST --> QA4
  DEP --> DV4
  DV4 -.->|"prerequisite missing"| WS
  QA4 -.->|"acceptance not observable"| ST
  HUM4 -.->|"split/merge review"| S4
```

**Handoff contract:** each story has one observable outcome, in/out of scope, source-qualified acceptance, technical (and UI when applicable) specification, dependencies, and verification obligations in **one file**. Shared canonical specs stay external; stories reference them. Authoring a story does not implement it. `story-create` does not invoke `dev`.

Operational authoring template: `src/agents/skills/story-create/assets/templates/story-template.md`.

### 5.5 Implement — `dev`

**Purpose:** implement the explicitly selected specifications/stories through red → green → refactor → developer QA. Cold session: do not supply missing requirements from memory.

**Skill:** current `dev`. Legacy: `/dev`.

```mermaid
flowchart TB
  subgraph Up5["Upstream"]
    U5A["Selected specs and/or stories"]
    U5B["Project instructions and policy"]
    U5C["Current source"]
    U5D["Optional checkpoint"]
    U5E["Optional qa-fix packet"]
  end

  subgraph WF5["Workflow"]
    C5["Command: dev"]
    S5["Skill: dev"]
    T5A["Template: development-context"]
    T5B["Template: development-slice-plan"]
    T5C["Template: development-traceability"]
    T5D["Template: development-delivery"]
    T5E["Template: checkpoint"]
    C5 --> S5
    S5 --> T5A
    S5 --> T5B
    S5 --> T5C
    S5 --> T5D
    S5 --> T5E
  end

  subgraph Cycle5["Per-slice cycle"]
    RED["Red: failing focused test"]
    GRN["Green: minimum real behavior"]
    REF["Refactor: preserve contracts"]
    IQA["Developer QA on changed paths"]
    RED --> GRN --> REF --> IQA
  end

  subgraph Doc5["Documents"]
    CTX["Context record"]
    SLI["Slice plan"]
    TRC["Requirement traceability"]
    DEL["Development delivery"]
    CK5["Checkpoint if work remains"]
  end

  subgraph Down5["Downstream"]
    QA5["qa — independent assessment"]
    ASK5["Ask: material spec/policy gap"]
    SPEC5["specify / architect if selected change needed"]
  end

  U5A --> C5
  U5B --> C5
  U5C --> C5
  U5D --> C5
  U5E --> C5
  T5A --> CTX
  T5B --> SLI
  SLI --> Cycle5
  Cycle5 --> TRC
  T5C --> TRC
  Cycle5 --> DEL
  T5D --> DEL
  T5E --> CK5
  DEL --> QA5
  CTX --> ASK5
  ASK5 --> SPEC5
  QA5 -.->|"FAIL qa-fix"| C5
  CK5 -.->|"resume"| C5
```

**Handoff contract for QA:** identified candidate bytes, source-qualified requirement accounting, executed check receipts, remaining gaps, and exact evidence paths. Development completion is not protected acceptance and is not a QA verdict. `dev` does not invoke `skill-builder` for application code and does not require `skill-validator` for product tests.

Operational templates: `src/agents/skills/dev/assets/`.

### 5.6 Assess — independent `qa`

**Purpose:** assess the selected candidate against requirements, independently of development completion claims. Oracle is the spec/story, not the developer's report.

**Skill:** current `qa`. Modes: `run` (default), `plan`, `execute`, `retest`. Legacy: `/qa`.

```mermaid
flowchart TB
  subgraph Up6["Upstream"]
    U6A["Selected specs / stories"]
    U6B["dev delivery and candidate identity"]
    U6C["Project policy floors"]
    U6D["Optional saved test plan"]
  end

  subgraph WF6["Workflow"]
    C6["Command: qa<br/>run / plan / execute / retest"]
    S6["Skill: qa"]
    T6A["Template: qa-test-plan"]
    T6B["Template: qa-report"]
    T6C["Template: qa-fix"]
    C6 --> S6
    S6 --> T6A
    S6 --> T6B
    S6 --> T6C
  end

  subgraph Gate6["Stop vs continue"]
    INTG["Integrity / metric / critical defect<br/>stops the whole run"]
    MAND["Mandatory defect: FAIL<br/>independent checks may continue"]
    GAP["Local gap: block dependents only"]
  end

  subgraph Doc6["Documents"]
    PLN["QA test plan"]
    RPT["QA report PASS / FAIL / INCOMPLETE"]
    FIX["qa-fix packet on FAIL"]
  end

  subgraph Down6["Downstream"]
    DEV6["dev remediation"]
    RET6["qa retest on new candidate"]
    REL6["delivery review on PASS"]
    PRE6["prerequisite owner on INCOMPLETE"]
  end

  U6A --> C6
  U6B --> C6
  U6C --> C6
  U6D --> C6
  T6A --> PLN
  PLN --> Gate6
  Gate6 --> RPT
  T6B --> RPT
  RPT -->|"FAIL"| FIX
  T6C --> FIX
  FIX --> DEV6
  DEV6 --> RET6
  RET6 --> C6
  RPT -->|"PASS"| REL6
  RPT -->|"INCOMPLETE"| PRE6
  RPT -.->|"oracle / spec conflict"| U6A
```

**Handoff contract:**

| QA outcome | Next owner | Required artifact |
| --- | --- | --- |
| PASS | delivery review (human / `release`) | QA report bound to candidate hashes |
| FAIL | `dev` | qa-fix packet + copyable remediating prompt |
| INCOMPLETE | prerequisite owner | exact missing input/tool/platform |
| NOT_EVALUATED | none | planning-only; not a product verdict |

QA must not repair product source. Only an independent retest can close a QA finding. Reports are not framework acceptance.

Operational templates: `src/agents/skills/qa/assets/`.

### 5.7 Deliver — release record

**Purpose:** perform the selected publication/deployment effect only with matching authorization, after delivery readiness. This is a separate effect from QA PASS.

**Skill:** planned core `release`. Legacy: `/release`.

```mermaid
flowchart LR
  subgraph Up7["Upstream"]
    U7A["QA PASS report"]
    U7B["Exact candidate identity"]
    U7C["Project policy delivery rules"]
    U7D["Actual release authorization"]
    U7E["Optional Rust acceptance receipt"]
  end

  subgraph WF7["Workflow"]
    C7["Command: release"]
    S7["Skill: release core"]
    T7["Template: release-record"]
    C7 --> S7 --> T7
  end

  subgraph Doc7["Documents"]
    REL7["Release record"]
    GAP7["Unmet delivery obligations"]
  end

  subgraph Down7["Downstream"]
    OPS["Operations / runtime"]
    FB["feedback"]
    STOP7["Do not deploy"]
  end

  U7A --> C7
  U7B --> C7
  U7C --> C7
  U7D --> C7
  U7E --> C7
  T7 --> REL7
  T7 --> GAP7
  REL7 --> OPS
  REL7 --> FB
  GAP7 --> STOP7
  STOP7 -.->|"missing auth or platform"| U7D
  FB -.->|"production observation"| C7
```

**Handoff contract:** candidate identity must match the assessed bytes. A required unavailable platform remains a gap. No authorization means the workflow records the blocked effect; it does not deploy. Rust acceptance, when required, must be a live authority result — not an editable field in this template.

### 5.8 Follow up — feedback and RCA

**Purpose:** turn observed outcomes into selected new work without silently rewriting policy. Feedback can spawn discovery or stories. RCA is for repeated or systemic failure, not the first red test.

**Skills:** planned `feedback`, `rca`. Legacy: `/feedback`, `/rca`.

```mermaid
flowchart LR
  subgraph Up8["Upstream"]
    U8A["Release record / production observation"]
    U8B["QA findings and retained attempts"]
    U8C["Repeated TDD or integration failure"]
    U8D["User retrospective"]
  end

  subgraph WF8["Workflow"]
    C8A["Command: feedback"]
    C8B["Command: rca"]
    S8A["Skill: feedback"]
    S8B["Skill: rca"]
    T8A["Template: feedback"]
    T8B["Template: rca"]
    C8A --> S8A --> T8A
    C8B --> S8B --> T8B
  end

  subgraph Doc8["Documents"]
    FB8["Feedback record"]
    RCA8["RCA analysis"]
  end

  subgraph Down8["Downstream"]
    DIS8["discover / specify"]
    ST8["story-create from recommendations"]
    POL8["policy realignment request"]
    SK8["skill-builder propose if framework gap"]
  end

  U8A --> C8A
  U8D --> C8A
  U8B --> C8B
  U8C --> C8B
  T8A --> FB8
  T8B --> RCA8
  FB8 --> DIS8
  FB8 --> ST8
  RCA8 --> ST8
  RCA8 --> POL8
  FB8 --> SK8
  ST8 -.->|"recommendation not a requirement"| FB8
  POL8 -.->|"experts cannot lower floors"| U8A
```

**Handoff contract:** recommendations are proposed work. They do not become requirements until selected. RCA must cite evidence and remaining uncertainty. A feedback item that only restates a goal without an observable behavior is incomplete.

## 6. End-to-end handoff graph

This is the document flow the expansions implement. Solid arrows are the producer → consumer contract. Dotted arrows are return paths.

```mermaid
flowchart TB
  AP["adaptation-proposal"] --> BIND["project-binding"]
  BIND --> BA["business-analysis"]
  RF["research-finding"] --> BA
  BA --> PRD["product-requirements"]
  PRD --> SAD["system-architecture"]
  PRD --> POL["project-policy"]
  SAD --> WS["work-set"]
  POL --> WS
  WS --> ST["story"]
  ST --> CTX["development-context"]
  POL --> CTX
  SAD --> CTX
  CTX --> SLI["slice-plan"]
  SLI --> TRC["traceability"]
  SLI --> DEL["development-delivery"]
  DEL --> QPL["qa-test-plan"]
  QPL --> QRP["qa-report"]
  QRP -->|"FAIL"| QFX["qa-fix"]
  QFX --> CTX
  QRP -->|"PASS"| REL["release-record"]
  REL --> FB["feedback"]
  QRP --> RCA["rca"]
  DEL --> RCA
  FB --> BA
  FB --> ST
  RCA --> ST
  RCA --> POL

  QRP -.->|"oracle conflict"| PRD
  DEL -.->|"missing decision"| PRD
  ST -.->|"unowned shared contract"| SAD
  SAD -.->|"missing business rule"| BA
```

Continuity: any stop writes [checkpoint.md](templates/checkpoint.md). Resume rereads identities and invalidates stale candidate-bound claims. A checkpoint is a navigation aid, not current truth.

## 7. Shared handoff fields

Every template in this pack uses the same envelope so a consumer can reject an incomplete packet without guessing:

| Field | Meaning |
| --- | --- |
| Producer skill / command | Who authored the document |
| Input locators and SHA-256 | Exact upstream bytes |
| Requirement / clause IDs | Stable identities, source-qualified when reused |
| In scope / out of scope | Selected effect boundary |
| Downstream consumer | Named next owner, not an automatic invocation |
| Required artifact properties | What the consumer must be able to observe |
| Failure behavior | `block_consumer` vs `report_optional_absence` vs independent work continues |
| Gaps | Missing input, contradiction, missing decision, unavailable capability, denied operation, changed input |
| Non-claims | Explicit list of decisions this document does **not** make |

Manual handoff does not invoke the consumer skill. The user selects the next workflow.

## 8. OrderDesk walkthrough (same facts, four consumers)

Fictional example from the foundation document. Selected change: permit cancellation **before** dispatch; deny it **after**; racing cancellation and dispatch must not yield contradictory states.

```mermaid
sequenceDiagram
  participant U as User
  participant D as discover
  participant S as specify
  participant A as architect
  participant ST as story-create
  participant V as dev
  participant Q as qa
  participant R as release

  U->>D: selected change
  D-->>S: business-analysis: dispatch meaning still open
  Note over D,S: unanswered race blocks only that behavior
  U->>D: dispatch = carrier accepted scan
  D-->>S: updated analysis
  S-->>A: product-requirements with AC IDs
  A-->>ST: architecture: one order-state owner
  ST-->>U: one story, not six phase/platform files
  U->>V: implement selected story
  V-->>Q: delivery: happy path evidenced
  Q-->>V: qa-fix: race produces contradictory states
  V-->>Q: new candidate
  Q-->>R: PASS for selected scope
  Note over R: still needs release authorization
```

What this walkthrough forbids: a storage expert deciding customer eligibility; copying two cancellation rules into different stories; treating the original unit pass as closing the race; deploying because QA passed.

## 9. What remains outside these diagrams

- Compiled-Rust authority, hooks, and protected receipts — [guardrails](../specs/framework/guardrails-and-rust-runtime.md).
- Installer / update / uninstall — [installation](../specs/framework/installation-and-integrations.md); binding setup is a separate authorized effect.
- Index/query daemon — optional knowledge, not a skill prerequisite.
- Skill-package evaluation campaigns — `skill-validator`, not product `qa`.
- Legacy Claude phase files and `devforgeai-validate` subcommands — historical surface, not the portable core.

Fill the templates under [templates/](templates/) when authoring design documents in a managed project. Do not treat a completed template as implemented software, independent QA, or release permission.
