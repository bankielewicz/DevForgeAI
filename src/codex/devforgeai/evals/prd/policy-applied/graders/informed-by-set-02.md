---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^upstream:\n(?:[ \t]+-[^\n]*\n)*?[ \t]+- \{id: POL-001, item: SET-02, relation: informed_by, version: 3\b
