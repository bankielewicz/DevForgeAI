---
skill_name: gaps-contradictory
status: approved
---

# Case count

REQ-01: Read a selected local CSV file, count data rows, preserve the source, and write only a selected new output file. Exclude malformed input with exit 2 and no output.
REQ-02: Every successful result must be exactly one JSON object with only a count integer field; plain text output is forbidden.
REQ-03: Every successful result must be exactly one plain text decimal integer followed by a newline; JSON output is forbidden. Both REQ-02 and REQ-03 apply to the same output file and have equal priority.
REQ-04: Use Python 3.10 standard library and Windows terminal tools without network access or installation.
