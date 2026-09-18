# Template: Product requirements

**Producer:** planned core `specify` (legacy `/ideate`)  
**Consumers:** `architect`, `story-create` / work-set, `dev` when architecture already exists, `qa` as oracle source  
**Does not:** implement, choose libraries unless the user locked them, or mark features complete because a signature is written.

## Envelope

| Field | Value |
| --- | --- |
| Document ID | PRD-[product]-[utc] |
| Producer | specify |
| Downstream consumer | architect (primary); work planning; qa oracle |
| Failure behavior | Missing essential decision blocks dependent clauses only |
| Non-claims | Proposed commands are targets, not existing executables |

## Upstream inputs

| Role | Locator | SHA-256 | Notes |
| --- | --- | --- | --- |
| Business analysis | | | |
| Research findings | | | or none |
| User corrections | | | win over stale BA prose when explicit |
| Existing specs reused | | | reading ≠ selecting all deliverables |

## Identity

- Product / project: [resolved]
- Selected scope for this document: [feature set or whole product]
- Supersedes: [prior spec identity or none]
- Explicit non-goals: [list]

## Normative requirements

Assign stable IDs. Qualify with source identity if several documents reuse an ID.

| ID | Statement | Actor / trigger | Inputs | Outputs / state | Failure behavior | Acceptance scenario | Origin |
| --- | --- | --- | --- | --- | --- | --- | --- |
| REQ-001 | | | | | | AC-001 | user / BA / derived |

Mark each row as **normative**, **example**, **historical**, or **deferred**.

## Acceptance scenarios

| ID | Requirement IDs | Given | When | Then | Platforms if specified |
| --- | --- | --- | --- | --- | --- |
| AC-001 | REQ-001 | | | | |

Include denial, invalid input, recovery, and concurrency scenarios when the behavior has those risks.

## Exclusions and deferred work

| Item | Reason | Follow-up owner |
| --- | --- | --- |
| | out of scope / later increment | |

## Open decisions

| ID | Question | Blocks | Minimum resolution |
| --- | --- | --- | --- |
| PRD-Q1 | | requirement IDs | |

## Downstream handoff

**To architect:** every interface-affecting requirement, shared-state rule, and unresolved PRD-Q that architecture must not guess.

**To work planning:** complete clause inventory for decomposition. Do not pre-split by file, platform, or TDD phase.

**To dev / qa:** this document is the oracle. Failed tests never authorize rewriting expected behavior.

**Return path:** implementation or QA may report contradiction or missing decision. Record a spec revision only when that effect is selected.
