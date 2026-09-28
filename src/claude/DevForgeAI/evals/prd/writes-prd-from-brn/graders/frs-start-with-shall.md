---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: not_contains
flags: m
---
^functional_requirements:\n(?:(?!```)[\s\S])*?statement: \"(?!The system shall )
