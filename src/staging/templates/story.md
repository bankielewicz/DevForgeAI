---
id: STORY-000
type: story
title: ""              # short imperative, e.g. "Request a magic link"
status: draft          # draft | ready | in-progress | in-review | done | blocked | cancelled
version: 1
created: YYYY-MM-DD
updated: YYYY-MM-DD
owner: ""
authors: []
generated_by:
  tool: ""
  model: ""
  session: ""
reviewed_by: []
approved_by: ""
approved_on: null
upstream:              # exactly one parent epic; AC own their requirement links
  - {id: EPIC-000, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []         # stories or other documents that must be done first
# --- story-specific ---
estimate: null
spec_mode: separate    # separate (a SPEC specifies this story) | embedded (section 5 holds the spec)
---

# STORY-000 — <title>

<!-- The story defines observable behavior and how we prove it. It is the unit
     of delivery. Its parent is exactly one epic. It may satisfy several PRD requirements.
     Sprint membership is recorded in the sprint file, not here. -->

## 1. User story

As a **<role>**, I want **<capability>**, so that **<benefit>**.

<!-- For enabling/technical work: "To enable <capability>, <component> needs <change>, because <reason>." -->

## 2. Context

<!-- NON-NORMATIVE background: current behavior, prior attempts, related stories,
     known pitfalls. Nothing here is a requirement. If a sentence here says something
     must be done or must not break, move it into Scope or an AC; otherwise
     it bypasses provenance and nobody verifies it. -->

## 3. Scope

**In scope**
- <behavior>

**Out of scope**
- <behavior> (covered by <other story>)

## 4. Acceptance criteria

<!-- Each AC must be observable and testable. Cover the happy path, key edge cases,
     and at least one failure path. Every AC needs at least one `satisfies` link
     (to a PRD FR/NFR and/or an epic DW). given/when/then are lists: extra lines are "and".
     Do not add verified-by or test fields: tests cite the AC, and that view is GENERATED. -->

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "<happy path name>"
    given:
      - "<precondition>"
    when:
      - "<action>"
    then:
      - "<observable result>"
    upstream:
      - {id: PRD-000,  item: FR-001, relation: satisfies, version: 1, hash: null}
      - {id: EPIC-000, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-02
    status: active
    name: "<failure path name>"
    given:
      - "<precondition>"
    when:
      - "<action>"
    then:
      - "<observable result>"
    upstream:
      - {id: PRD-000, item: NFR-001, relation: satisfies, version: 1, hash: null}
```

## 5. Specification

<!-- spec_mode: separate → leave the GENERATED line; the SPEC's frontmatter cites this story.
     spec_mode: embedded → small changes only. Replace this section with the spec template's
     sections 4–9 (DDL, OpenAPI and item blocks), using the same item IDs and collection keys.
     The spec's `constrains` links (NFRs, ADRs) then go in this story's frontmatter `upstream`.
     Spec item blocks are rejected when spec_mode is separate. -->

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [ ] Every AC is verified by at least one test that cites it (`STORY-000#AC-NN`)
- [ ] Code reviewed; commits reference `STORY-000`
- [ ] Spec items implemented, or explicitly deferred to a new story
- [ ] Docs and changelog updated
- [ ] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- [NEEDS CLARIFICATION: <question>]

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | YYYY-MM-DD | | Initial draft | all |
