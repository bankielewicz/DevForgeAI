---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
\[NEEDS ADR: [^\]\n]*affects FR-001\b[^\]\n]*\]
