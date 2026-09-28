---
type: llm
---

The workspace held PRD-001 and an existing, approved EPIC-001 that refines FR-002, FR-008 and part of
NFR-001. By the skill's rule, an FR that an existing epic refines is "covered" and gets no new epic,
but an NFR is never covered: an eligible NFR is attached to every new epic it constrains. The user
asked for one new epic covering everything eligible, with NFR-001 applying to it.

Judge only the final reply.
PASS if the reply reports FR-002 as covered by EPIC-001 and does not report NFR-001 as covered or
left out; NFR-001 is presented as part of the new epic.
FAIL if NFR-001 is listed as covered, already refined, or left out, or if the reply says EPIC-001
was changed.
