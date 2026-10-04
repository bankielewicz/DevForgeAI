---
type: llm
---

The workspace's docs/specs/spec/SPEC-002.md is a draft (version 1, not approved); its BEH-01 says scheduled
exports run nightly at 02:00 UTC. docs/specs/spec/SPEC-001.md is approved (version 2); its BEH-02, which allowed
Excel workbooks, is deprecated and replaced by BEH-03 (CSV only).

Judge only the final reply.
PASS if all of these hold:
- It cites the nightly 02:00 UTC schedule to SPEC-002 and says SPEC-002 is a draft, so the schedule isn't
  approved or decided yet.
- It cites the Excel item (SPEC-001 BEH-02) as deprecated, so Excel exports aren't in force, and says CSV only
  (BEH-03) applies.
- Each citation names a file and line (docs/specs/spec/SPEC-00N.md:<line>).
FAIL if it presents the schedule as decided or Excel as allowed, or gives no file and line.
