---
id: STORY-005
type: story
title: "Turn a PRD's ready requirements into epics"
status: draft
version: 1
created: 2026-09-24
updated: 2026-09-24
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
  - {id: EPIC-005, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-005 — Turn a PRD's ready requirements into epics

## 1. User story

As a **framework user**, I want **Claude to group the requirements that are ready and in the current
release into epics, with my confirmation, and tell me why every other requirement was left out**, so
that **delivery starts only on settled foundations and nothing drops out of sight**.

## 2. Context

This is the epic step, after Architecture Definition (ADR-002). It reads a PRD and its architecture
description (ARCH). The ARCH file is the readiness contract (SPEC-003 §4 and §5); the architecture
skill's reply is advisory, and it misreported readiness once in three runs (STORY-004 AC-04). MoSCoW
priority orders the work; `release: current` selects it (PRD-001 v9 notes on FR-014).

## 3. Scope

**In scope**
- Selecting requirements by readiness and the current release, and reporting the rest with reasons.
- Proposing a grouping into epics, confirmed by the user, and writing new epics.
- Handing off to the story step.

**Out of scope**
- Writing stories, sprint planning, modifying existing epics, organizational policy (FR-012) and the
  `devforgeai check` CLI.

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "Epics only for ready, current-release requirements"
    given:
      - "a PRD and an ARCH that examined its current version"
    when:
      - "the user runs the skill with the PRD ID and confirms the grouping"
    then:
      - "it writes new epics whose refines links name only active requirements that are ready under SPEC-003 §4 and have release current and priority must, should or could"
      - "every such requirement not already covered by an existing epic appears in at least one new epic"
    upstream:
      - {id: PRD-001,  item: FR-014, relation: satisfies, version: 9, hash: null}
      - {id: EPIC-005, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-02
    status: active
    name: "Readiness is read from the ARCH file"
    given:
      - "an ARCH with open, resolved and superseded-resolver questions"
    when:
      - "the skill decides which requirements are ready"
    then:
      - "it applies SPEC-003 §4 to the ARCH's questions and the ADRs' current status, not to any skill's reply"
      - "a question blocks only the requirements its upstream links cite"
      - "a question resolved by a superseded ADR blocks its requirements again"
    upstream:
      - {id: PRD-001,  item: FR-014, relation: satisfies, version: 9, hash: null}
      - {id: EPIC-005, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-03
    status: active
    name: "Every requirement left out is reported with its reason"
    given:
      - "requirements that are blocked, released later, won't have, undecided or already covered"
    when:
      - "the skill hands off"
    then:
      - "each is listed with its reason: the blocking question IDs, later, won't have, undecided (a null priority or release, for the PRD owner) or the epic that covers it"
    upstream:
      - {id: PRD-001, item: FR-014, relation: satisfies, version: 9, hash: null}
  - id: AC-04
    status: active
    name: "No current architecture, no epics"
    given:
      - "a PRD with no ARCH, or an ARCH that examined an older PRD version"
    when:
      - "the user runs the skill"
    then:
      - "it writes nothing and hands back to the architecture step with the PRD ID"
    upstream:
      - {id: PRD-001,  item: FR-014, relation: satisfies, version: 9, hash: null}
      - {id: EPIC-005, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-05
    status: active
    name: "The user confirms the grouping"
    given:
      - "eligible requirements"
    when:
      - "the skill proposes how to group them into epics"
    then:
      - "it writes epics only after the user confirms or changes the grouping"
      - "if no one can confirm, each epic it writes carries a [NEEDS CLARIFICATION] marker saying the grouping is unconfirmed"
    upstream:
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 9, hash: null}
  - id: AC-06
    status: active
    name: "Priority orders the epics"
    given:
      - "eligible requirements with must, should and could priorities"
    when:
      - "the skill writes epics"
    then:
      - "each epic's priority is the highest priority among the requirements it refines"
      - "epics are numbered and listed Must, then Should, then Could"
    upstream:
      - {id: PRD-001, item: FR-014, relation: satisfies, version: 9, hash: null}
  - id: AC-07
    status: active
    name: "Existing epics are never modified or duplicated"
    given:
      - "an existing epic that refines some requirements"
    when:
      - "the skill runs"
    then:
      - "the existing epic is unchanged, and the requirements it refines are reported as covered and get no new epic"
    upstream:
      - {id: PRD-001,  item: FR-014, relation: satisfies, version: 9, hash: null}
      - {id: EPIC-005, item: DW-02,  relation: satisfies, version: 1, hash: null}
  - id: AC-08
    status: active
    name: "A draft PRD or ARCH gives proposals"
    given:
      - "a PRD or ARCH whose status is draft"
    when:
      - "the skill writes epics"
    then:
      - "the handoff and each epic written say the epics are proposals because an input is a draft"
    upstream:
      - {id: PRD-001, item: FR-014, relation: satisfies, version: 9, hash: null}
  - id: AC-09
    status: active
    name: "Handoff names the story step and its input"
    given:
      - "the skill has written epics"
    when:
      - "it hands off"
    then:
      - "it names the story step as next, with the epic IDs as its input, and does not write stories itself"
    upstream:
      - {id: PRD-001, item: FR-004, relation: satisfies, version: 9, hash: null}
  - id: AC-10
    status: active
    name: "Does not trigger on unrelated requests"
    given:
      - "a request that shares vocabulary with epics but asks for something else, such as writing an epic poem"
    when:
      - "the user sends it"
    then:
      - "the skill does not run"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 9, hash: null}
  - id: AC-11
    status: active
    name: "AI provenance is recorded"
    given:
      - "the skill writes an epic"
    when:
      - "the file is read"
    then:
      - "generated_by names the tool, model and session, reviewed_by is empty, every hash is null and status is draft"
    upstream:
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 9, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [ ] Every AC is verified by at least one eval case or manual check that cites it (`STORY-005#AC-NN`)
- [ ] Skill files reviewed; commits reference `STORY-005`
- [ ] SPEC-004 items implemented, or explicitly deferred to a new story
- [ ] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- None.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-24 | claude-code | Initial draft | all |
