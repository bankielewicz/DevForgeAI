---
type: llm
---

The workspace held two approved policies: the regional network's organization policy POL-001, whose
SET-01 mandates a mail relay for "transactional email", and the food bank's project policy POL-002,
whose SET-01 mandates a council sign-in service for "volunteer sign-in". They mandate platforms for
different capabilities, so they don't conflict. In ARCH-001, DEC-01 (which identity provider handles
volunteer sign-in, and the question PRD-001's NEEDS ADR marker for FR-001 asks) is resolved by
POL-002#SET-01, and DEC-07 (the email service) by POL-001#SET-01. So FR-001 and FR-012 are ready and
eligible.

Judge only the final reply.
PASS if neither FR-001 nor FR-012 is reported as unknown, blocked or left out, and the reply presents
both as included in the epic.
FAIL if either one is called unknown or blocked, is listed among the left-out requirements, or if the
reply says the two policies conflict or that a second policy setting the same key disqualifies either.
