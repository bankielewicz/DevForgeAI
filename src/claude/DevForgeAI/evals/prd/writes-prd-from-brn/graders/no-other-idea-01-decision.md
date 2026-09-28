---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: not_contains
---
priority: (?!must\b)\w+\n[ \t]+release: [^\n]*\n[ \t]+notes: [^\n]*\n[ \t]+upstream:\n[ \t]+- \{id: BRN-001, item: IDEA-01\b|priority: must\n[ \t]+release: (?!current\b)\w+\n[ \t]+notes: [^\n]*\n[ \t]+upstream:\n[ \t]+- \{id: BRN-001, item: IDEA-01\b
