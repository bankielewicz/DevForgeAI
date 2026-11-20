---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
value: "\d+(?:\.\d+)?"[^\n]*\n[ \t]+effort: "\d+(?:\.\d+)?"[^\n]*\n[ \t]+risk: "(?:0|20|50)"[^\n]*\n[ \t]+score: \d+\.\d(?!\d)
