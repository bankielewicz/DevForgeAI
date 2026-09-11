---
schema_version: "devforge.artifact/v1"
artifact_id: "ARCH-001"
artifact_type: "architecture-contract"
project_id: "havenlist"
revision: 4
status: accepted
created_at_utc: "2026-08-21T11:05:00Z"
producer:
  skill: "operator"
  skill_revision: "unknown (synthetic fixture; no skill produced this)"
execution_ref: null
upstream: []
evidence: []
supersedes: null
decision_ref: "adopted by the Havenlist steering group, 2026-08-21"
missing_inputs: []
---

# Havenlist architecture contract

**Synthetic fixture.** The stack, versions and rules below are invented for evaluation.

## Approved UI stack

| Decision | Value | Status |
| --- | --- | --- |
| RULE-012 | Server-rendered HTML templates with progressive enhancement. No client-side routing. | accepted |
| RULE-013 | The `shedkit` component set, version 2.4, is the only source of buttons, form fields, banners and empty-state blocks. New components require an amendment. | accepted |
| RULE-014 | Two breakpoints only: 360px and 1024px. Nothing between them is designed separately. | accepted |
| RULE-015 | Type scale is 16/20/28px. Spacing is a 4px grid. | accepted |
| RULE-016 | Errors appear inline beside the field that caused them, never as a page-level banner. | accepted |

## Non-UI rules relevant to this brief

RULE-021: the served-area postcode list is loaded at request time from the shed's own configuration, never hardcoded in a template.

## Amendment route

Any departure from RULE-012 to RULE-016 is a proposal recorded against this contract. It is not adopted until the steering group records it here.
