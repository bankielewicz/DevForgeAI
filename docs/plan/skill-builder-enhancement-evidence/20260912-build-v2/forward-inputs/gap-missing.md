---
skill_name: gaps-missing
status: approved
---

# Service case exporter

REQ-01: Read a local CSV containing case_id and severity, preserving the original file. The user selects the input path.
REQ-02: Export all cases to the user's new output path. The output representation and field schema are intentionally undecided and must be selected by the product owner before implementation. No default representation is authorized.
REQ-03: Use Python 3.10 standard library and terminal tools; no network access or installation. Invalid inputs and occupied outputs must fail without overwriting files.
