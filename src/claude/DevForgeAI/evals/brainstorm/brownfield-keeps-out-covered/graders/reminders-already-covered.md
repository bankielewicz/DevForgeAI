---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
\n### Already covered\n+\| Suggestion \| Covered by \|\n\|---\|---\|\n(?:\|[^\n]*\|\n)*\| [^|\n]*[Rr]eminder[^|\n]* \| PRD-001#FR-003 \|\n
