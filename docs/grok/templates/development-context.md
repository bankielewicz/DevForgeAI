# Template: Development context

**Producer:** current `dev` (before production changes)  
**Consumers:** later slices in the same run; resume; `qa` as supporting identity  
**Operational template:** `src/agents/skills/dev/assets/context.md`  
**Does not:** authorize extra effects, invent missing architecture, or substitute conversation memory for unread specs.

## Envelope

| Field | Value |
| --- | --- |
| Record identity / UTC | |
| Producer | dev |
| Downstream consumer | slice plan, delivery, checkpoint |
| Failure behavior | Missing essential input recorded before dependent edits |
| Non-claims | Not a candidate identity after later edits; re-bind on change |

## Upstream inputs

| Role | Exact locator | SHA-256 | Selected vs reference-only |
| --- | --- | --- | --- |
| Specs / stories | | | |
| Project instructions | | | |
| Checkpoint | | | or none |
| qa-fix packet | | | or none |

Preserve `selected_evidence_value` **literally** from the original input. Record `selection_source` and `resolved_evidence_root`.

## Authorization and scope

- Current request: [locator or retained text]
- Authorized effects: [source / test / evidence]
- Exclusions: [install, deploy, unrelated trees]
- Plan-only / subset / implementation: [which]

## Constitutional decisions

| Category | Effective decision or inapplicable | Source | Inferred? |
| --- | --- | --- | --- |
| Architecture | | | |
| Technology stack | | | |
| Source tree | | | |
| Testing and QA | | | |
| Security and operations | | | |
| Delivery | | | |

Infer routine choices only when compatible with explicit rules. Material gaps stay gaps.

## Tools

| Role | Executable / version | Command / cwd | Availability |
| --- | --- | --- | --- |
| build / test / format / coverage | | project-derived | |

Missing tooling is reported, not replaced with a different language.

## Output map

| Logical record | Concrete path under selected evidence root |
| --- | --- |
| context / slices / traceability / executions / checkpoint / delivery | |

## Gaps

| ID | Category | Affected requirements | Why dependent work stops | Independent work that may continue |
| --- | --- | --- | --- | --- |
| | missing input / contradiction / missing decision / unavailable capability / denied operation / changed input | | | |

## Downstream handoff

Slice planning consumes this record. QA may use it to reconstruct scope but must bind **current candidate bytes** independently. Resume rereads this file and rechecks hashes; it does not trust the conversation.
