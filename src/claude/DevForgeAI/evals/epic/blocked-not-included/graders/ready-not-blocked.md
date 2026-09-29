---
type: llm
---

The workspace held PRD-001 (version 2) and ARCH-001. By the readiness rule, FR-002 (its question
DEC-02 is resolved by the accepted ADR-001) and FR-012 (DEC-07 is resolved by an approved, active
policy setting, POL-001#SET-01) are ready and eligible for an epic. FR-001, FR-008, FR-009 and
FR-010 are blocked, and FR-011 is unknown.

Judge only what the final reply says about FR-002 and FR-012.
PASS if neither FR-002 nor FR-012 is reported as blocked, unknown or left out, and the reply
presents both as included in an epic (or ready).
FAIL if either one is called blocked or unknown, is listed among the left-out requirements, or if
the reply says DEC-01 or DEC-02 blocks FR-002.
