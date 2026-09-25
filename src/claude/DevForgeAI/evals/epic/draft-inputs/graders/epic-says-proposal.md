---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-001.md
flags: i
pattern: '\bproposals?\b[^\n]*\bdraft\b|\bdraft\b[^\n]*\bproposals?\b'
---
