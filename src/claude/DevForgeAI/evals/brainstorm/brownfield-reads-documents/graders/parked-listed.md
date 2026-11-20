---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: contains
---
\n### Previously decided\n+\| Idea \| Decision \| Where \|\n\|---\|---\|---\|\n(?:\|[^\n]*\|\n)*\| [^|\n]+ \| parked \| BRN-001#IDEA-04 \|\n(?:\|[^\n]*\|\n)*\| [^|\n]+ \| parked \| BRN-001#IDEA-05 \|\n
