---
id: STORY-004
type: story
title: "Enforce the architecture skill's inspection scope and draft warning deterministically"
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
  - {id: EPIC-004, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-004 — Enforce the architecture skill's inspection scope and draft warning deterministically

## 1. User story

To make the architecture skill's inspection boundary and draft-PRD warning hold on every run, the
framework needs a deterministic check outside the skill's instructions, because wording alone makes
them likely but not certain.

## 2. Context

STORY-003 built the architecture skill (SKL-003 v3) and verified it with SPEC-003's eval cases and
manual checks. SPEC-003 §9 records what instructions alone could not guarantee:

- **Inspection scope (BEH-05).** On SKL-003 v2, both VER-12 (b) runs listed the project root and the
  scope's parent. The v3 wording fixed this in the two v3 runs (row i), but nothing prevents it.
- **Draft-PRD warning (BEH-02, VER-12 (c)).** On v2 and v3 the warning appeared only in the handoff and
  in ARCH §1, not when the PRD was read. After v3, the last wording round, it is a known limit (row i).
- **ERR-05.** Exercised once, only through the `devforgeai check` path with a test stand-in. The
  self-check path (no `devforgeai` on PATH) is not exercised (row e).

ADR-003 excludes hooks "until a hook's blocking behaviour and failure mode are specified and tested",
and the `devforgeai` CLI (including `devforgeai hook`) is not started. So this story needs an accepted
ADR before it can be ready. It records the deferred obligations; it does not choose the mechanism.

## 3. Scope

**In scope**
- Deterministic enforcement of SPEC-003 BEH-05's path rule during architecture skill runs.
- Deterministic enforcement that the draft-PRD warning comes before the first question or file write.
- Exercising ERR-05 on the self-check path, or recording why it can't be forced.

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
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 7, hash: null}
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
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 7, hash: null}
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
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 7, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [ ] Every AC is verified by at least one eval case or manual check that cites it (`STORY-004#AC-NN`)
- [ ] Changes reviewed; commits reference `STORY-004`
- [ ] Spec items implemented, or explicitly deferred to a new story
- [ ] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- [NEEDS CLARIFICATION: which mechanism enforces AC-01 and AC-02, with its blocking behaviour and failure mode (fail open or closed), needs an accepted ADR first (ADR-003 excludes hooks until then); record that ADR in blocked_by once it exists]
- [NEEDS CLARIFICATION: whether the self-check path can be forced to fail deterministically at all; if not, AC-03 is deprecated with the reason recorded]

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-24 | claude-code | Initial draft: obligations deferred from STORY-003 (SPEC-003 §9 rows e and i) | all |
