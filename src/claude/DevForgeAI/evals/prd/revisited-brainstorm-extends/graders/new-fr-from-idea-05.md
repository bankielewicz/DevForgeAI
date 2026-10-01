---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
- id: FR-\d{3}\n(?:(?![ \t]*- id:)[ \t]+[^\n]*\n)*?[ \t]+- \{id: BRN-001, item: IDEA-05, relation: derives, version: 2, hash: null\}
