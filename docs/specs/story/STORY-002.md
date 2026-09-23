---
id: STORY-002
type: story
title: "Turn a brainstorm into a PRD"
status: draft
version: 1
created: 2026-09-23
updated: 2026-09-23
owner: "Bryan"
authors: ["Bryan", "claude-code"]
generated_by:
  tool: "claude-code"
  model: "claude-opus-5-5"
  session: "a2b1015f-3340-4c70-80ed-b674d486fadd"
reviewed_by: []
approved_by: ""
approved_on: null
upstream:
  - {id: EPIC-002, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-002 — Turn a brainstorm into a PRD

## 1. User story

As a **framework user**, I want **Claude to turn my brainstorm into a PRD and ask me only what the
brainstorm doesn't settle**, so that **the epics that follow build on scope I actually decided**.

## 2. Context

This is the second DevForgeAI skill. It consumes `docs/specs/brainstorm/BRN-NNN.md` as written by
the brainstorm skill (SPEC-001 §5, downstream contract).
- **Input selection** was stated by Bryan: an explicit `BRN-NNN` argument, or a scan for BRNs not yet
  turned into requirements, followed by a question.
- **Stage and scoping.** Delivery stage (prototype, MVP or production) and per-requirement scoping
  (MVP vs later) are part of the PRD.
- **Architecture** enters only as constraints.
- **Evals are non-interactive.** No user is present, so every decision must stay visibly open (`null`)
  unless the prompt supplies it.

## 3. Scope

**In scope**
- Input selection, reading the BRN, and the interview.
- Writing or extending the PRD, validating it, and handing off.

**Out of scope**
- The epic skill, architecture design, and editing the BRN.

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "Input BRN is selected deterministically"
    given:
      - "one or more BRN documents in docs/specs/brainstorm/"
    when:
      - "the user runs the skill with a BRN ID, or with no argument"
    then:
      - "with an argument such as BRN-002, the skill reads docs/specs/brainstorm/BRN-002.md"
      - "with no argument, it lists only BRNs with at least one promoted idea that no PRD item cites, and asks which to use"
      - "if no such BRN exists, it says so and writes nothing"
    upstream:
      - {id: PRD-001, item: FR-005, relation: satisfies, version: 3, hash: null}
  - id: AC-02
    status: active
    name: "PRD requirements trace to promoted ideas"
    given:
      - "a converged BRN with promoted, parked and rejected ideas"
    when:
      - "the skill writes a new PRD"
    then:
      - "it writes docs/specs/prd/PRD-NNN.md using the next free PRD number"
      - "the document validates against prd.schema.json"
      - "every functional requirement has an upstream derives link to a promoted idea of that BRN"
      - "no open, parked or rejected idea is cited anywhere in the PRD"
    upstream:
      - {id: PRD-001,  item: FR-005, relation: satisfies, version: 3, hash: null}
      - {id: EPIC-002, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-03
    status: active
    name: "Decisions stay the user's"
    given:
      - "a request that does not state the stage, a priority or a release for some requirements"
    when:
      - "the skill writes the PRD"
    then:
      - "stage, priority and release are null wherever the user did not supply or confirm them"
      - "gaps the user did not answer are [NEEDS CLARIFICATION] markers, not guesses"
      - "the PRD status is draft; the skill never sets approved"
    upstream:
      - {id: PRD-001,  item: FR-003, relation: satisfies, version: 3, hash: null}
      - {id: EPIC-002, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-04
    status: active
    name: "Interview asks only what is missing; architecture only as constraints"
    given:
      - "a BRN and a request that answer some questions already"
    when:
      - "the skill interviews the user"
    then:
      - "it asks nothing the BRN or the request already answers"
      - "it asks in batches of at most four questions"
      - "fixed external conditions such as a mandated platform or integration become NFR items with category constraint"
      - "it writes no architecture or design decision into the PRD"
    upstream:
      - {id: PRD-001, item: FR-005, relation: satisfies, version: 3, hash: null}
  - id: AC-05
    status: active
    name: "Unusable input is handled"
    given:
      - "a BRN that is not converged, or has no promoted idea"
    when:
      - "the skill reads it"
    then:
      - "for a BRN that is not converged, it warns and continues only after the user confirms"
      - "for a BRN with no promoted idea, it stops, writes nothing, and points back to the brainstorm workflow"
    upstream:
      - {id: PRD-001, item: FR-005, relation: satisfies, version: 3, hash: null}
  - id: AC-06
    status: active
    name: "New PRD or extension of an existing one"
    given:
      - "one or more existing PRDs"
    when:
      - "the skill is about to write"
    then:
      - "it asks whether to create a new PRD or extend a named existing one"
      - "extending bumps the version, continues item numbering, keeps every existing item unchanged, and adds a Change Log entry"
      - "it tells the user that epics citing the extended PRD are now suspect links to re-review"
    upstream:
      - {id: PRD-001,  item: FR-005, relation: satisfies, version: 3, hash: null}
      - {id: EPIC-002, item: DW-02,  relation: satisfies, version: 1, hash: null}
  - id: AC-07
    status: active
    name: "Handoff names the epic step and its input"
    given:
      - "the skill has written or extended a PRD"
    when:
      - "it hands off"
    then:
      - "it names the epic workflow as the next step and gives the PRD path as its input"
      - "if the epic skill is not installed, it says the step is not yet available instead of naming a command that does not exist"
      - "it does not start writing an epic itself"
    upstream:
      - {id: PRD-001, item: FR-004, relation: satisfies, version: 3, hash: null}
  - id: AC-08
    status: active
    name: "Does not trigger on unrelated requests"
    given:
      - "a request that shares vocabulary with PRDs but asks for something else, such as opening a pull request"
    when:
      - "the user sends it"
    then:
      - "the prd skill is not invoked"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 3, hash: null}
  - id: AC-09
    status: active
    name: "AI provenance is recorded"
    given:
      - "the skill writes a PRD"
    when:
      - "the frontmatter is filled"
    then:
      - "generated_by names the tool, the model and the session ID"
      - "reviewed_by is empty and every link hash is null"
    upstream:
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 3, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [ ] Every AC is verified by at least one eval case or manual check that cites it (`STORY-002#AC-NN`)
- [ ] Skill files reviewed; commits reference `STORY-002`
- [ ] SPEC-002 items implemented, or explicitly deferred to a new story
- [ ] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- None beyond SPEC-002 §13.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft | all |
