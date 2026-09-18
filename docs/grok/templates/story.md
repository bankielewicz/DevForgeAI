# Template: Story

**Producer:** current `story-create`  
**Consumers:** `dev`, `qa`  
**Operational template:** `src/agents/skills/story-create/assets/templates/story-template.md`  
**Does not:** implement behavior, run product tests, or qualify release. This file is the framework handoff contract; the operational template is the authoring source of truth.

## Envelope

| Field | Value |
| --- | --- |
| Story ID | STORY-NNN |
| Title | [observable outcome] |
| Producer | story-create |
| Downstream consumer | dev (implement); qa (oracle) |
| Failure behavior | Unresolved prerequisite blocks dependent implementation |
| Non-claims | Checklists below are planned obligations, not executed results |

## Upstream inputs

| Role | Locator | SHA-256 | Story responsibility |
| --- | --- | --- | --- |
| Work set | | | grouping |
| Product requirements | | | owned clauses |
| Architecture / policy | | | referenced, not copied |
| QA / RCA recommendation | | | if originating here |

## Description

**As a** [actor], **I want** [capability], **so that** [value].

**In scope:** [behavior and deliverables]  
**Out of scope:** [explicit]  
**Observable completion:** [what a cold session must see]

## Provenance

| Source identity | Clause / decision | This story owns or references | Quote / locator |
| --- | --- | --- | --- |
| | | owns / references shared | |

## Acceptance criteria

| ID | Implements | Given | When | Then |
| --- | --- | --- | --- | --- |
| AC1 | REQ-… | | | |

Include success, denial, boundary, and recovery as applicable.

## Technical specification (summary)

| Component / interface | Path or planned path | Owner | AC IDs | Test mapping |
| --- | --- | --- | --- | --- |
| | | | | |

Full nested technical block may follow the operational template's YAML schema (`format_version: "2.0"`). Shared canonical contracts stay outside this file.

## UI specification

Required when the story changes a user interface, including terminal interaction. Otherwise record why inapplicable.

## Dependencies

| Producer | Artifact / decision / evidence needed | Consumer need | Satisfaction observation |
| --- | --- | --- | --- |
| | | | |

## Test strategy (planned)

| Level | Cases / oracles | Platforms | Notes |
| --- | --- | --- | --- |
| Unit | | | |
| Integration | | | |
| Native / E2E | | | or inapplicable |

Planned verification is not execution. Product thresholds come from project policy.

## Open decisions

| ID | Question | Blocks ready-for-dev? | Owner |
| --- | --- | --- | --- |
| | | yes / no | |

## Downstream handoff

**To dev:** this file plus selected related specs. `dev` inventories requirements; it does not treat story DoD checkboxes as already passed.

**To qa:** same IDs and oracles. QA does not trust development completion claims.

**Return path:** non-observable AC, duplicate contract, or missing prerequisite returns to work-set / specify / architect as appropriate. Next action is a **manual** consumer invocation, not an automatic `$dev` call from this skill.
