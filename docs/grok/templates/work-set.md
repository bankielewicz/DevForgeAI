# Template: Work set

**Producer:** work-planning pass before or with `story-create`  
**Consumers:** human selection, `story-create`, `dev`, `qa`  
**Does not:** implement, mark epics complete from a subset of stories, or split by file/flag/platform/TDD phase alone.

## Envelope

| Field | Value |
| --- | --- |
| Work-set ID | WS-[capability]-[utc] |
| Producer | plan work |
| Downstream consumer | story-create (author stories); human (select implementation) |
| Failure behavior | Unresolved shared-contract owner blocks dependent stories |
| Non-claims | Proposed grouping is not approved scope until selected |

## Upstream inputs

| Role | Locator | SHA-256 | Notes |
| --- | --- | --- | --- |
| Product requirements | | | clause inventory |
| System architecture | | | owners |
| Project policy | | | |
| QA / RCA recommendations | | | optional |

## Clause inventory

| Source-qualified ID | Statement locator | Canonical owner | Proposed story | Notes |
| --- | --- | --- | --- | --- |
| PRD REQ-001 | | COMP / story | STORY-… | no duplicate owners |

Every normative clause appears once as owner, elsewhere as reference.

## Proposed stories

| ID | Observable outcome | In scope | Out of scope | Prerequisites | Verification | Split/merge reason |
| --- | --- | --- | --- | --- | --- | --- |
| STORY-001 | | | | | | seed / split / merge |

Do not seed a story per source paragraph. Split only when both results have independently assessable outcomes. Merge when they cannot be assessed without the same unfinished behavior.

## Dependencies

| Consumer | Needs from producer | Kind | Satisfaction observation |
| --- | --- | --- | --- |
| STORY-002 | STORY-001 | contract / interface / evidence / decision | |

Cycles are invalid. Reading a spec does not select its implementation.

## Epic-level acceptance that must remain visible

| ID | Scenario | Why it is not a separate story |
| --- | --- | --- |
| | e.g. cancellation/dispatch race | shared obligation across the capability |

## Review

- Adversarial grouping notes: [coupling or independence cited]
- Unresolved semantic disputes: [DFF-03-Q3 owner once designated]
- State: `PROPOSED` / `SELECTED` / `BLOCKED`

## Downstream handoff

**To story-create:** selected story IDs, owned clauses, and dependency kinds. One story → one complete `.story.md`.

**To dev / qa:** only after human selection of the work set or individual stories.

**Return path:** `dev` reporting a missing prerequisite, or `qa` reporting non-observable acceptance, returns to this map — do not hide the gap inside a Definition-of-Done checkbox.
