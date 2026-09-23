---
id: STORY-001
type: story
title: "Brainstorm a topic into a BRN document"
status: done
version: 4
created: 2026-09-22
updated: 2026-09-22
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
  - {id: EPIC-001, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-001 — Brainstorm a topic into a BRN document

## 1. User story

As a **framework user**, I want **to brainstorm a topic with Claude and get a structured
brainstorm document**, so that **the PRD that follows can cite identified problems and ideas**.

## 2. Context

This is the first DevForgeAI skill and the first real use of the templates. The `devforgeai`
CLI doesn't exist yet, so validation must work without it. Brainstorming frameworks are
deliberately deferred: this story delivers the extension point, not the catalog.

## 3. Scope

**In scope**
- Topic intake, problem and idea capture, evaluation, dispositions confirmed by the user,
  writing and validating the BRN file.
- Selecting a framework from reference files, with one default.

**Out of scope**
- Additional frameworks, and handing off automatically into a PRD skill.

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "Topic becomes a valid BRN document"
    given:
      - "a project with or without an existing docs/specs/brainstorm/ directory"
    when:
      - "the user asks to brainstorm a named topic"
    then:
      - "the skill writes docs/specs/brainstorm/BRN-NNN.md using the next free BRN number, without asking for or accepting a file name"
      - "the document's title carries the descriptive topic"
      - "the document validates against brainstorm.schema.json"
      - "it contains at least one problem, at least one idea and a named evaluation method"
    upstream:
      - {id: PRD-001,  item: FR-001, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-001, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-02
    status: active
    name: "Dispositions need the user's confirmation"
    given:
      - "a brainstorm with evaluated ideas"
    when:
      - "the skill reaches convergence"
    then:
      - "it proposes a disposition and reason for each idea and asks the user to confirm"
      - "only dispositions the user confirmed are written; every other idea stays open"
      - "status becomes converged only if the user confirms convergence"
    upstream:
      - {id: PRD-001,  item: FR-003, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-001, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-03
    status: active
    name: "AI provenance is recorded"
    given:
      - "the skill writes a BRN document"
    when:
      - "the frontmatter is filled"
    then:
      - "generated_by names the tool, the model and the session ID"
      - "reviewed_by is empty until the user reviews the document"
      - "no link hash is written"
    upstream:
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 6, hash: null}
  - id: AC-04
    status: active
    name: "Frameworks are pluggable"
    given:
      - "a framework reference file and its entry in the frameworks index"
    when:
      - "the user brainstorms a topic that matches the framework's use-when criteria, or names it"
    then:
      - "the skill states which framework it chose and why"
      - "the document still uses only the brainstorm schema's collections and fields"
      - "adding the framework required no change to SKILL.md"
    upstream:
      - {id: PRD-001,  item: FR-002, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-001, item: DW-02,  relation: satisfies, version: 1, hash: null}
  - id: AC-05
    status: active
    name: "Does not trigger on unrelated requests"
    given:
      - "a request that shares vocabulary with brainstorming but asks for something else"
    when:
      - "the user sends it"
    then:
      - "the brainstorm skill is not invoked"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 6, hash: null}
  - id: AC-06
    status: active
    name: "Asks for a missing topic"
    given:
      - "the skill is invoked with no arguments and no topic in the conversation"
    when:
      - "it starts"
    then:
      - "it asks the user for the topic"
      - "it writes no file until a topic is given"
    upstream:
      - {id: PRD-001, item: FR-001, relation: satisfies, version: 6, hash: null}
  - id: AC-07
    status: active
    name: "Handoff names the PRD step and its input"
    given:
      - "the skill has written a BRN document"
    when:
      - "it hands off"
    then:
      - "it names the PRD workflow as the next step and gives the BRN path as that step's input"
      - "if the PRD skill is not installed, it says the step is not yet available instead of naming a command that does not exist"
      - "it does not start writing a PRD itself"
    upstream:
      - {id: PRD-001, item: FR-004, relation: satisfies, version: 6, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [x] Every AC is verified by at least one test or eval case that cites it (`STORY-001#AC-NN`)
- [x] Skill files reviewed; commits reference `STORY-001`
- [x] SPEC-001 items implemented, or explicitly deferred to a new story
- [x] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- None beyond SPEC-001 §13.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-22 | claude-code | Initial draft | all |
| 2 | 2026-09-22 | claude-code | Added AC-07 (handoff to the PRD workflow) | AC-07 |
| 3 | 2026-09-22 | claude-code | AC-01: ID-only BRN path docs/specs/brainstorm/BRN-NNN.md, no user-supplied file name, topic in title (agreed with Bryan) | AC-01 |
| 4 | 2026-09-23 | claude-code | Status done: VER-01 to VER-10 recorded as passing on PR #2 (automated evals and manual VER-05/VER-09); merged to main | status, Definition of Done |
