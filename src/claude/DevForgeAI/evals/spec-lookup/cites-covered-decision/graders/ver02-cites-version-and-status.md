---
type: llm
---

The workspace's docs/specs/spec/SPEC-001.md is approved, version 2, and its BEH-03 says exports are CSV files
only (UTF-8, header row), with no other format offered. Its BEH-02, which allowed Excel workbooks, is deprecated.

Judge only the final reply.
PASS if all of these hold:
- It cites SPEC-001 as docs/specs/spec/SPEC-001.md:<line>, and says the document is version 2 (v2) and approved.
- What it proposes for the export format is CSV only, grounded in that citation.
- It doesn't propose Excel or any other format as decided.
FAIL if any of these is missing.
