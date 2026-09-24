---
id: STORY-004
type: story
title: "Close the architecture skill's conformance gaps that wording didn't guarantee"
status: draft
version: 2
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
  - {id: EPIC-004, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-004 — Close the architecture skill's conformance gaps that wording didn't guarantee

## 1. User story

To make the architecture skill's inspection boundary, draft-PRD warning, readiness report and evidence
records hold on every run, the framework needs a deterministic check outside the skill's instructions,
because wording alone makes them likely but not certain.

## 2. Context

STORY-003 built the architecture skill (SKL-003, final build v4) and verified it with SPEC-003's eval
cases and manual checks. SPEC-003 §9 records what instructions alone could not guarantee:

- **Inspection scope (BEH-05).** On SKL-003 v2, both VER-12 (b) runs listed the project root and the
  scope's parent. The v3 wording fixed this in the two v3 runs (row i), but nothing prevents it.
- **Draft-PRD warning (BEH-02, VER-12 (c)).** On v2 and v3 the warning appeared only in the handoff and
  in ARCH §1, not when the PRD was read. VER-12 (c) fails on v3, the last wording round (row i).
- **ERR-05.** Exercised once, only through the `devforgeai check` path with a test stand-in. The
  self-check path (no `devforgeai` on PATH) is not exercised (row e).
- **Readiness attribution (VER-05; §4, BEH-11, BEH-15).** On SKL-003 v4 the superseded-adr case met its
  threshold (0.87), but run 1 of 3 reported NFR-001 as blocked by DEC-01, which doesn't cite it (row l).
  The same misreport appeared once on v1 (row f). Failed; deferred here (row m).
- **Evidence completeness (BEH-05).** On v4, the VER-12 (k) run read ARCH-001 but recorded no EVD for it,
  while the (j) run recorded the ARCH it amended (EVD-03) (rows k and m). Failed; deferred here.

ADR-003 excludes hooks "until a hook's blocking behaviour and failure mode are specified and tested",
and the `devforgeai` CLI (including `devforgeai hook`) is not started. So this story needs an accepted
ADR before it can be ready. It records the deferred obligations; it does not choose the mechanism.

## 3. Scope

**In scope**
- Deterministic enforcement of SPEC-003 BEH-05's path rule during architecture skill runs.
- Deterministic enforcement that the draft-PRD warning comes before the first question or file write.
- Exercising ERR-05 on the self-check path, or recording why it can't be forced.
- Assurance that the readiness report matches the SPEC-003 §4 rule on every run.
- Assurance that every project document a run consults has an EVD.

**Out of scope**
- Choosing the enforcement mechanism (an ADR decides it; see Open questions).
- The rest of the `devforgeai` CLI.
- The same enforcement for the brainstorm and prd skills.
- Any change to SPEC-003's rules themselves.

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "Inspection outside the scope is blocked before it runs"
    given:
      - "an architecture skill run with an inspection_scope"
    when:
      - "a command would read, list or search a path outside inspection_scope and outside the contract document folders (docs/specs/prd/, arch/, adr/ and policy/, and .claude/devforgeai.local.md)"
    then:
      - "the command does not run, and the user sees the path and the reason"
      - "after the user agrees to widen the scope, reading that path is allowed"
      - "reads inside the scope and the contract document folders are never blocked"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 9, hash: null}
  - id: AC-02
    status: active
    name: "A draft PRD's warning comes before any question or write"
    given:
      - "an architecture skill run on a PRD whose status is draft"
    when:
      - "the skill would ask its first question or write its first file"
    then:
      - "the proposal warning has already been shown; otherwise the question or write does not happen until it is"
      - "a run on an approved PRD is not affected"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 9, hash: null}
  - id: AC-03
    status: active
    name: "ERR-05 on the self-check path"
    given:
      - "no devforgeai command on PATH, and a written ARCH that fails a self-check rule the skill can't fix"
    when:
      - "validation still fails after three attempts"
    then:
      - "the skill stops, lists the files and remaining errors, restores only statuses, approval fields, dependent DEC state and the audit record, and skips the readiness handoff, as on the CLI path"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 9, hash: null}
  - id: AC-04
    status: active
    name: "The readiness report matches the §4 rule on every run"
    given:
      - "an architecture skill run that reports readiness"
    when:
      - "it reports the requirements ready for epic work and those blocked"
    then:
      - "every reported status and blocking DEC ID matches SPEC-003 §4 applied to the ARCH and the ADRs' current statuses"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 9, hash: null}
  - id: AC-05
    status: active
    name: "Every consulted project document has an EVD"
    given:
      - "an architecture skill run that reads project documents"
    when:
      - "it writes or amends the ARCH"
    then:
      - "every PRD, ARCH (including the one being amended) and ADR the run read is recorded as an EVD per inspection.md"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 9, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [ ] Every AC is verified by at least one eval case or manual check that cites it (`STORY-004#AC-NN`)
- [ ] Changes reviewed; commits reference `STORY-004`
- [ ] Spec items implemented, or explicitly deferred to a new story
- [ ] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- [NEEDS CLARIFICATION: which mechanism enforces or checks AC-01, AC-02, AC-04 and AC-05, with its blocking behaviour and failure mode (fail open or closed), needs an accepted ADR first (ADR-003 excludes hooks until then); record that ADR in blocked_by once it exists]
- [NEEDS CLARIFICATION: whether the self-check path can be forced to fail deterministically at all; if not, AC-03 is deprecated with the reason recorded]

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-24 | claude-code | Initial draft: obligations deferred from STORY-003 (SPEC-003 §9 rows e and i) | all |
| 2 | 2026-09-24 | claude-code | Retitled to the architecture skill's conformance gaps that wording didn't guarantee. AC-04 (the readiness report matches the §4 rule on every run) and AC-05 (every consulted project document has an EVD), deferred from STORY-003 as failed (SPEC-003 §9 rows f, k, l and m); the mechanism question now covers them. Accepted by Bryan | AC-04, AC-05, title |
