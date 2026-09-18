# Template: Business analysis

**Producer:** planned core `discover` (legacy `/brainstorm`)  
**Consumers:** `specify` (product requirements), `architect` when boundaries are already partly known  
**Does not:** invent stack, write stories, implement, or treat stakeholder prose as protected policy.

## Envelope

| Field | Value |
| --- | --- |
| Document ID | BA-[project]-[utc] |
| Producer | discover |
| Downstream consumer | specify (primary); architect (optional) |
| Failure behavior | Unanswered essential questions block only dependent outcomes |
| Non-claims | Not requirements IDs until specify assigns them; not architecture |

## Upstream inputs

| Role | Locator | SHA-256 | Notes |
| --- | --- | --- | --- |
| User problem | | | |
| Current behavior evidence | | | observed vs assumed |
| Research findings | | | or none |
| Prior feedback / RCA | | | or none |

## Problem and outcomes

- Problem in one paragraph: [who is stuck, doing what, with what cost]
- Desired outcomes: [observable results, not solutions]
- Non-outcomes / out of scope: [explicit]
- Why now: [user-supplied; label inference separately]

## Stakeholders

| Party | Role | Goal | Concern | Conflict with |
| --- | --- | --- | --- | --- |
| | decision maker / user / affected | | | none / [party] |

Unresolved conflicts stay listed. Do not pick a winner without a recorded user decision.

## Current behavior

| Situation | Observed result | Source | Gap vs desired |
| --- | --- | --- | --- |
| | | | |

Business rules are not inferred solely from code. If implementation already contradicts a stated rule, record a contradiction.

## Decisions and uncertainties

| ID | Question | Affects | Status | Minimum resolution |
| --- | --- | --- | --- | --- |
| BA-Q1 | | which outcomes / interfaces | open / decided | |

Example of a blocking uncertainty: what “dispatch” means, and how cancellation races with it.

## Downstream handoff

**To specify:** agreed outcomes, exclusions, stakeholder conflicts, and BA-Q IDs that still block requirement writing.

**To architect (only if selected):** business boundaries that already constrain state ownership, not a requested tech stack.

**Return path:** specify or architect may send a named missing business rule back here. Do not silently invent it in architecture.
