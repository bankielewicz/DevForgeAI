# Mapping a BRN into a PRD

## Contents

- Reading the BRN
- Mapping table
- Unprocessed BRNs
- Worked example

## Reading the BRN

The BRN is `docs/specs/brainstorm/BRN-NNN.md`. Read it; never edit it.

- **Frontmatter:** `id`, `version`, `status`, `title`, `owner`, `participants`.
- **Item blocks** (fences with info string `yaml items`): `problems` (`PRB-NN`), `ideas` (`IDEA-NN`) and
  `assumptions` (`ASM-NN`). If a fence doesn't parse as YAML, has more than one top-level key, or the
  `problems` or `ideas` collection is missing, stop (ERR-05): name the section heading and fence that failed,
  give the BRN path, and write nothing. Never repair the BRN.
- **Prose:** section 3 (target users) and section 8 (candidate success signals).
- Use an idea only if `disposition: promoted` and `status: active`. Ignore every other idea completely.

## Mapping table

| BRN | PRD | Link |
|---|---|---|
| each active problem `PRB-NN` | section 2 prose, citing `BRN-NNN#PRB-NN` in text | frontmatter `upstream`: `{id: BRN-NNN, item: PRB-NN, relation: derives, version: <BRN version>, hash: null}` |
| each promoted idea `IDEA-NN` | one or more `functional_requirements`, each `"The system shall …"`, one testable capability per FR | on each FR: `{id: BRN-NNN, item: IDEA-NN, relation: derives, …}` |
| each active assumption `ASM-NN` | an `assumptions` item with the same statement and validation, `state` carried over | on the ASM: `{id: BRN-NNN, item: ASM-NN, relation: derives, …}` |
| a candidate success signal that measures a promoted idea | a `success_metrics` item; `baseline` and `target` from the user, else `[NEEDS CLARIFICATION: …]` | on the SM: `derives` the promoted idea it measures |
| a candidate success signal tied to no promoted idea | a `success_metrics` item with a `[NEEDS CLARIFICATION: …]` target | none |
| target users (section 3), participants | section 3 prose; `stakeholders` | none |
| open, parked, rejected ideas | nothing, except a parked or rejected idea may become a non-goal **described in words** | never cited, never named by ID |

- FR statements describe **what** the system does for the user, not how. Split an idea into several FRs
  only where it holds separately testable capabilities (for example book, move, cancel).
- The PRD's `owner` is the user's name if given, else the BRN's `owner`. Ask only in an interactive run.
- `priority` and `release` stay `null` until the interview (BEH-05, BEH-06).
- FR, NFR and SM numbering starts at `FR-001`, `NFR-001`, `SM-01`, `ASM-01` in a new PRD, and continues
  from the highest existing number when extending.

## Unprocessed BRNs

A BRN is **unprocessed** when at least one of its promoted ideas is not cited by any item `upstream` link
(`{id: BRN-NNN, item: IDEA-NN, …}`) in any `docs/specs/prd/PRD-*.md`. Decide it from links alone: grep the
PRDs for `id: BRN-NNN, item: IDEA-NN`. A BRN with no promoted idea is never unprocessed. Nothing is ever
written into a BRN to mark it processed.

## Worked example

**In** (`BRN-001`, version 1, `status: converged`):

```yaml
problems:
  - id: PRB-01
    statement: "Patients can only book by phone during opening hours"
ideas:
  - id: IDEA-01
    idea: "Patients book, move and cancel their own appointments online"
    disposition: promoted
  - id: IDEA-02
    idea: "Text-message reminders the day before an appointment"
    disposition: promoted
  - id: IDEA-03
    idea: "Waitlist that offers cancelled slots to waiting patients"
    disposition: parked
assumptions:
  - id: ASM-01
    statement: "Most patients will book online if it is available"
    state: open
```

Section 8 lists "Fewer booking calls" and "Fewer missed appointments".

**Out** (`PRD-001`, before the interview):

```yaml
# frontmatter
upstream:
  - {id: BRN-001, item: PRB-01, relation: derives, version: 1, hash: null}
```

```yaml
functional_requirements:
  - id: FR-001
    status: active
    statement: "The system shall let a patient book an available appointment online."
    priority: null
    release: null
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-002
    status: active
    statement: "The system shall let a patient move or cancel their own appointment online."
    priority: null
    release: null
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
  - id: FR-003
    status: active
    statement: "The system shall send a text reminder the day before each appointment."
    priority: null
    release: null
    notes: null
    upstream:
      - {id: BRN-001, item: IDEA-02, relation: derives, version: 1, hash: null}
```

```yaml
success_metrics:
  - id: SM-01
    status: active
    metric: "Booking calls to the front desk"
    baseline: "[NEEDS CLARIFICATION: current weekly booking calls]"
    target: "[NEEDS CLARIFICATION: target for booking calls]"
    upstream:
      - {id: BRN-001, item: IDEA-01, relation: derives, version: 1, hash: null}
```

```yaml
assumptions:
  - id: ASM-01
    status: active
    statement: "Most patients will book online if it is available"
    validation: "Share of bookings made online in the first month"
    state: open
    upstream:
      - {id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null}
```

The parked waitlist appears only as a non-goal in words ("A waitlist for cancelled slots, parked in the
brainstorm"), with no idea ID.
