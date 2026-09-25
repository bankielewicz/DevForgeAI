---
type: regex
target:
  source: file
  path: docs/specs/epic/EPIC-001.md
pattern: 'generated_by:\s*\n\s+tool:\s*"?claude-code"?\s*\n\s+model:\s*"?[A-Za-z0-9][^"\n]*"?\s*\n\s+session:\s*"?[A-Za-z0-9][^"\n]*"?'
---
