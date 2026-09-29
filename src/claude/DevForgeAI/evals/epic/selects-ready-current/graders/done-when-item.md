---
type: regex
target: {source: file, path: docs/specs/epic/EPIC-001.md}
match: contains
---
- id: DW-01\n[ \t]+status: active\n[ \t]+criterion: "[^"\n]+"\n[ \t]+evidence_method: "[^"\n]+"\n
