---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
priority: should\n[ \t]+release: current\n[ \t]+notes: [^\n]*\n[ \t]+upstream:\n[ \t]+- \{id: BRN-001, item: IDEA-03\b
