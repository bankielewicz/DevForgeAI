---
id: STORY-003
type: story
title: "Define the architecture for a PRD"
status: in-progress
version: 2
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
  - {id: EPIC-004, relation: refines, version: 1, hash: null}
supersedes: []
superseded_by: null
blocked_by: []
# --- story-specific ---
estimate: null
spec_mode: separate
---

# STORY-003 — Define the architecture for a PRD

## 1. User story

As a **framework user**, I want **Claude to settle the architectural questions my epics must share,
asking me to decide each one**, so that **separate epics don't invent conflicting foundations, and I
know which requirements are ready to build**.

## 2. Context

This is the Architecture Definition step (ADR-002, accepted). It reads a PRD, including its
`[NEEDS ADR]` markers and constraints, and applies organization and project policy (ADR-003,
accepted). It produces an ARCH description and ADRs. It hosts the two-organization demonstration
(EPIC-003 DW-02). Detailed feature design stays in later specs.

## 3. Scope

**In scope**
- Selecting or creating an ARCH.
- Bounded read-only inspection.
- Architectural questions and their explicit resolution.
- Readiness reporting.
- Handing requirement changes back to the PRD owner.

**Out of scope**
- Experts, exhaustive code indexing, detailed feature design, and the epic skill.

## 4. Acceptance criteria

```yaml items
acceptance_criteria:
  - id: AC-01
    status: active
    name: "A PRD becomes an ARCH with explicit architectural questions"
    given:
      - "a PRD, draft or approved, with requirements, constraints and possibly [NEEDS ADR] markers"
    when:
      - "the user runs the skill with the PRD ID"
    then:
      - "it writes docs/specs/arch/ARCH-NNN.md that validates against arch.schema.json, with components and architectural questions"
      - "every [NEEDS ADR] marker becomes a question whose upstream links name the affected requirements at the PRD version examined"
      - "questions cover only what separate epics must share, not feature-level detail"
      - "a draft PRD produces proposals with a warning; unanswered product questions are not turned into decisions"
    upstream:
      - {id: PRD-001,  item: FR-013, relation: satisfies, version: 7, hash: null}
      - {id: EPIC-004, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-02
    status: active
    name: "Readiness is decision-specific"
    given:
      - "a requirement affected by more than one blocking architectural question"
    when:
      - "some but not all of those questions are resolved"
    then:
      - "the requirement is reported blocked, naming the open questions"
      - "an accepted ADR that cites the requirement but answers a different question resolves nothing"
      - "a question resolved by an ADR that is later superseded is reported open again"
      - "a policy setting resolves only the question it actually answers"
    upstream:
      - {id: PRD-001,  item: FR-013, relation: satisfies, version: 7, hash: null}
      - {id: EPIC-004, item: DW-01,  relation: satisfies, version: 1, hash: null}
  - id: AC-03
    status: active
    name: "Decisions are accepted one by one, only explicitly"
    given:
      - "architectural questions with options"
    when:
      - "the user confirms the overall outcome, or answers some questions"
    then:
      - "an ADR is written as accepted only for a decision the user explicitly made, and it resolves only that question"
      - "confirming reuse, amend or create never accepts the decisions inside"
      - "with no user present, nothing is accepted: any ADR written is proposed, the questions stay open, and the outcome stays null"
    upstream:
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 7, hash: null}
  - id: AC-04
    status: active
    name: "An existing architecture is reused or amended, not duplicated"
    given:
      - "an ARCH already covering the same system"
    when:
      - "the skill runs for a new or changed PRD"
    then:
      - "it proposes reusing or amending that ARCH, with reasons, and asks"
      - "it never creates a second baseline without the user's choice"
      - "reusing one platform or component is not reported as a reuse outcome for the whole architecture"
    upstream:
      - {id: PRD-001,  item: FR-013, relation: satisfies, version: 7, hash: null}
      - {id: EPIC-004, item: DW-02,  relation: satisfies, version: 1, hash: null}
  - id: AC-05
    status: active
    name: "Inspection is bounded, recorded and honest about evidence"
    given:
      - "the user names components or directories to inspect"
    when:
      - "the skill examines the existing system"
    then:
      - "it uses read-only searches within that scope and follows references only inside it, asking before going further"
      - "every source consulted is recorded as evidence with its kind and, separately, its classification: observed practice, approved policy, an accepted decision, or context (inputs and historical material, such as the PRD itself, an existing ARCH or a superseded ADR, that establish neither implemented behavior nor a decision)"
      - "insufficient evidence produces an explicit unknown, never a confident reuse recommendation"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 7, hash: null}
  - id: AC-06
    status: active
    name: "Organizational policy is applied as in ADR-003"
    given:
      - "approved organization or project policy"
    when:
      - "the skill resolves policy"
    then:
      - "it follows the ADR-003 sequence and failure rules, and records the resolution line and links"
      - "an approved mandated-platform setting resolves only the question it answers, cited as POL-NNN#SET-NN"
    upstream:
      - {id: PRD-001, item: FR-006, relation: satisfies, version: 7, hash: null}
      - {id: PRD-001, item: FR-007, relation: satisfies, version: 7, hash: null}
      - {id: PRD-001, item: FR-008, relation: satisfies, version: 7, hash: null}
  - id: AC-07
    status: active
    name: "Two organizations, one unchanged workflow"
    given:
      - "the same policy-neutral PRD, prompt, knowledge and plugin, varying only the organization policy"
    when:
      - "the skill runs in fresh workspaces for Organization A and Organization B"
    then:
      - "for A, the identity-provider question is resolved by A's mandate while other identity questions, such as session revocation, stay open"
      - "for B, the identity-provider question stays open"
      - "neither run reports a reuse outcome merely because a platform is reused"
      - "the deployed plugin is byte-identical before and after both runs"
    upstream:
      - {id: PRD-001,  item: FR-009, relation: satisfies, version: 7, hash: null}
      - {id: EPIC-003, item: DW-02,  relation: satisfies, version: 1, hash: null}
  - id: AC-08
    status: active
    name: "Requirement changes go back to the PRD owner"
    given:
      - "an architectural finding that makes a requirement infeasible, too costly or conflicting"
    when:
      - "the skill writes the ARCH"
    then:
      - "it records a proposed requirement change in the ARCH and the handoff"
      - "it never edits the PRD"
    upstream:
      - {id: PRD-001, item: FR-013, relation: satisfies, version: 7, hash: null}
  - id: AC-09
    status: active
    name: "Handoff reports readiness and names the epic step"
    given:
      - "the skill has written or amended an ARCH"
    when:
      - "it hands off"
    then:
      - "it lists requirements ready for epic work and requirements blocked, with the blocking question IDs"
      - "it names the epic workflow as next, or says it is not yet available, and never starts it"
    upstream:
      - {id: PRD-001, item: FR-004, relation: satisfies, version: 7, hash: null}
  - id: AC-10
    status: active
    name: "Does not trigger on unrelated requests"
    given:
      - "a request about architecture in general or someone else's system"
    when:
      - "the user sends it"
    then:
      - "the architecture skill is not invoked"
    upstream:
      - {id: PRD-001, item: NFR-003, relation: satisfies, version: 7, hash: null}
  - id: AC-11
    status: active
    name: "AI provenance is recorded"
    given:
      - "the skill writes an ARCH or ADR"
    when:
      - "the frontmatter is filled"
    then:
      - "generated_by names the tool, the model and the session ID; reviewed_by is empty; every hash is null"
    upstream:
      - {id: PRD-001, item: FR-003, relation: satisfies, version: 7, hash: null}
```

## 5. Specification

- GENERATED: specs whose upstream cites this story

## 6. Definition of Done

- [x] Every AC is verified by at least one eval case or manual check that cites it (`STORY-003#AC-NN`). On SKL-003 v3 (2026-09-24, SPEC-003 §9 rows i and j):
  - all 12 architecture cases scored ≥ 0.8 over 3 runs in the full-plugin run (40/40);
  - the fresh Organization A/B sequence passed with identical hashes;
  - VER-12 (b) passed every clause (AC-05).

  Caveats:
  - VER-12 (a), (d), (e), (g) and the ERR-04 check are carried forward from build 469e984;
  - VER-12 (c)'s early draft warning is a known limit, since the warning appears only in the handoff and ARCH (AC-01's "with a warning" holds);
  - ERR-05 is exercised only through a stand-in CLI.
- [ ] Skill files reviewed; commits reference `STORY-003`
- [x] SPEC-003 items implemented, or explicitly deferred to a new story: deferred to STORY-004 (draft) are the early draft-PRD warning (VER-12 (c) known limit), deterministic enforcement of the BEH-05 path rule, and ERR-05 on the self-check path
- [ ] No open `[NEEDS CLARIFICATION]` markers; `blocked_by` empty

## 7. Open questions

- None beyond SPEC-003 §13.
- AC-05's bounded-inspection and classification clauses are cited only by SPEC-003 VER-08, which doesn't test them; VER-12 (b) does, by hand. The next SPEC-003 revision should add AC-05 to VER-12's upstream links.

## Change Log

| Version | Date | Author | Change | AC affected |
|---|---|---|---|---|
| 1 | 2026-09-23 | claude-code | Initial draft | all |
| 2 | 2026-09-23 | claude-code | AC-05: evidence classification adds context, independent of kind (SPEC-003 v3). Approved by Bryan | AC-05 |
