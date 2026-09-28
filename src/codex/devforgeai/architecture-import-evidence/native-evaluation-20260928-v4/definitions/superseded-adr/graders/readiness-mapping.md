---
type: llm
---

Context the reply was written in: PRD-001 has exactly three requirements, FR-001, FR-002 and NFR-001.
The existing ARCH-001 had two architectural questions: DEC-01 (identity provider), which cites FR-001
only, and DEC-02 (data ownership), which cites FR-002 and NFR-001 only. DEC-01 was resolved by
ADR-002, which has since been superseded by ADR-003, an ADR about hosting, not identity. DEC-02 is
resolved by ADR-001, which is still accepted. The user asked to amend ARCH-001.

Judge only the readiness that the final reply reports.
PASS if all of these hold:
- FR-001 is reported blocked, with DEC-01 named as a blocker.
- FR-002 and NFR-001 are each reported ready, or reported blocked only by questions numbered DEC-03
  or higher (questions this run added). Neither is attributed to DEC-01 or DEC-02.
- All three requirements appear in the readiness report.
- No other sentence contradicts the lists (for example, saying FR-001 is ready or everything is ready).
FAIL if any of these fails, or if the reply says DEC-01 is still resolved, by ADR-002 or by ADR-003.
