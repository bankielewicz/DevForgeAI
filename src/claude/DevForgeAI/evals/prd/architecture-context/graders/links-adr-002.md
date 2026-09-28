---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^upstream:\n(?:[ \t]+-[^\n]*\n)*?[ \t]+- \{id: ADR-002, relation: constrains, version: 1\b
