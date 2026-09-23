---
id: STORY-002
type: story
title: "Turn a brainstorm into a PRD"
status: done
version: 7
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
  - {id: EPIC-002, relation: refines, version: 3, hash: null}
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
- **Stage and scoping.** Scope maturity (`stage`: prototype, mvp or evolution), who uses the product
  (`operating_context`), and per-requirement scoping (`release`: current or later) are part of the PRD.
- **Architecture** is read and classified (commitments, constraints, preferences, open decisions), never
  designed in the PRD (SPEC-002 BEH-16).
- **Evals are non-interactive.** No user is present, so every decision must stay visibly open (`null`)
  unless the prompt supplies it.

## 3. Scope

**In scope**
- Input selection, reading the BRN, and the interview.
- Writing or extending the PRD, validating it, and handing off.

**Out of scope**
- The architecture and epic skills, architecture design, and editing the BRN.

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
      - {id: PRD-001, item: FR-005, relation: satisfies, version: 6, hash: null}
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
      - {id: PRD-001,  item: FR-005, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-002, item: DW-01,  relation: satisfies, version: 3, hash: null}
  - id: AC-03
    status: active
    name: "Decisions stay the user's"
    given:
      - "a request that does not state the stage, a priority or a release for some requirements"
    when:
      - "the skill writes the PRD"
    then:
      - "stage, operating context, priority and release are null wherever the user did not supply or confirm them"
      - "gaps the user did not answer are [NEEDS CLARIFICATION] markers, not guesses"
      - "a new PRD is written with status draft; the skill never sets approved (extension status follows AC-06)"
    upstream:
      - {id: PRD-001,  item: FR-003, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-002, item: DW-01,  relation: satisfies, version: 3, hash: null}
  - id: AC-04
    status: active
    name: "Interview asks only what is missing; architecture is read and classified, not designed"
    given:
      - "a BRN and a request that answer some questions already"
    when:
      - "the skill interviews the user"
    then:
      - "it asks nothing the BRN or the request already answers"
      - "it asks in batches of at most four questions"
      - "it reads accepted ADRs in docs/specs/adr/ and any architecture document the BRN or request names"
      - "existing commitments become constrains links to the accepted ADR; hard constraints become NFR items with category constraint; preferences become open questions"
      - "an open architecture decision becomes a [NEEDS ADR] marker naming the requirements it affects"
      - "it writes no architecture or design decision into the PRD"
    upstream:
      - {id: PRD-001, item: FR-005, relation: satisfies, version: 6, hash: null}
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
      - {id: PRD-001, item: FR-005, relation: satisfies, version: 6, hash: null}
  - id: AC-06
    status: active
    name: "New PRD or extension, decided by scope, ownership and lifecycle"
    given:
      - "one or more existing PRDs"
    when:
      - "the skill is about to write"
    then:
      - "it recommends a new PRD or extending a named one, giving its reasons in terms of scope, owner and lifecycle, and the user decides"
      - "the existence of a PRD, even a single one for the same product, is never on its own a reason to extend it"
      - "extending bumps the version, continues item numbering, keeps every existing item unchanged, and adds a Change Log entry"
      - "extending an approved PRD returns it to in-review as an explicit, reviewable scope change"
      - "it tells the user that epics citing the extended PRD are now suspect links to re-review"
    upstream:
      - {id: PRD-001,  item: FR-005, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-002, item: DW-02,  relation: satisfies, version: 3, hash: null}
  - id: AC-07
    status: active
    name: "Handoff names the architecture step and its input"
    given:
      - "the skill has written or extended a PRD"
    when:
      - "it hands off"
    then:
      - "it names the architecture step (ADR-002) as the next step and gives the PRD path as its input, listing any [NEEDS ADR] markers"
      - "if the architecture skill is not installed, it says the step is done by hand with ADRs for now, instead of naming a command that does not exist"
      - "it does not start architecture work or write an epic itself"
    upstream:
      - {id: PRD-001, item: FR-004, relation: satisfies, version: 6, hash: null}
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
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 6, hash: null}
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
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 6, hash: null}
  - id: AC-10
    status: active
    name: "Stage and operating context are independent, and production is never under-asked"
    given:
      - "an MVP that will serve real users with real data in production"
    when:
      - "the skill interviews and writes the PRD"
    then:
      - "it records stage mvp and operating_context production as separate values"
      - "it asks about every quality category that production requires, whatever the stage, and offers any other category"
      - "each required category left unanswered becomes a [NEEDS CLARIFICATION] marker, not a placeholder requirement"
      - "when the operating context is unknown, it is treated as production for deciding which gaps to mark, and left null"
    upstream:
      - {id: PRD-001,  item: FR-005, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-002, item: DW-01,  relation: satisfies, version: 3, hash: null}
  - id: AC-11
    status: active
    name: "Organizational policy is resolved, applied and recorded"
    given:
      - "zero or more policy documents in docs/specs/policy/"
    when:
      - "the skill prepares and writes the PRD"
    then:
      - "policy is resolved in the ADR-003 sequence: load and validate, unconditional settings, operating context, conditional settings, record"
      - "approved active settings that apply are used: extra required quality categories for the established or fail-safe context, mandated platforms as cited constraints, and the interview call budget"
      - "a project setting overrides an organization setting only where the organization setting allows it; otherwise the skill stops"
      - "deprecated settings and draft or in-review policies never apply, and ignored documents are reported"
      - "a valid local preference changes only interaction defaults; an invalid one is ignored and reported"
      - "each applied policy setting is an upstream link with the policy version, and the Change Log carries the resolution line, including defaults and local values"
      - "an invalid, contradictory or disallowed approved setting stops the skill before anything is written, naming the file, setting and rule"
    upstream:
      - {id: PRD-001,  item: FR-006, relation: satisfies, version: 6, hash: null}
      - {id: PRD-001,  item: FR-007, relation: satisfies, version: 6, hash: null}
      - {id: PRD-001,  item: FR-008, relation: satisfies, version: 6, hash: null}
      - {id: EPIC-003, item: DW-01,  relation: satisfies, version: 1, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [x] Every AC is verified by at least one eval case or manual check that cites it (`STORY-002#AC-NN`)
- [x] Skill files reviewed; commits reference `STORY-002`
- [x] SPEC-002 items implemented, or explicitly deferred to a new story
- [x] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

Evidence (2026-09-23):
- **Automated:** 20 prd eval cases, one per automated VER, each citing its AC in the case description. Full-plugin run
  `evals/results/2026-09-23T16-15-59-135Z`: 28/28 cases pass at the 0.8 threshold over 3 runs, mean Δ +0.57 against the
  no-plugin baseline. The 8 brainstorm cases show no regression.
- **Manual:** VER-11, VER-12 and VER-23 run by hand in scratch projects, all pass. The results are in the STORY-002 build
  report.
- **Review:** the skill was reviewed by the advisory `plugin-dev:skill-reviewer` and `plugin-validator` agents; human
  review happens on the pull request. Every commit message references `STORY-002`.
- **Last item open:** `blocked_by` is empty, but SPEC-002 §13 still has two `[NEEDS CLARIFICATION]` markers: PRD-001's
  own stage (Bryan to decide), and the VER-04 fixture question. That fixture was written fresh, as the build brief
  directs, so the second marker can be closed.

## 7. Open questions

- None beyond SPEC-002 §13.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft | all |
| 2 | 2026-09-23 | claude-code | AC-06: new vs extend decided by scope, ownership and lifecycle; approved PRDs re-enter review when extended (agreed with Bryan) | AC-06 |
| 3 | 2026-09-23 | claude-code | AC-03 status wording no longer contradicts AC-06; AC-04 reads and classifies architecture context; AC-10 stage vs operating context | AC-03, AC-04, AC-10 |
| 4 | 2026-09-23 | claude-code | AC-07: handoff goes to the architecture step (ADR-002) | AC-07 |
| 5 | 2026-09-23 | claude-code | AC-11: policy resolved, applied and recorded (ADR-003) | AC-11 |
| 6 | 2026-09-23 | claude-code | AC-11 follows ADR-003 v2: sequence, overrides, retired settings, local preferences, resolution line | AC-11 |
| 7 | 2026-09-23 | claude-code | Status done: automated VER items scored at least 0.8 and manual VER-11, VER-12 and VER-23 recorded on PR #5; deferred gaps listed there; merged to main | status, Definition of Done |
