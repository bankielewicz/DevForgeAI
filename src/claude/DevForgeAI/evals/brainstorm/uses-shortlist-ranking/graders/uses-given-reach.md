---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^\| Idea \| Reach \| Impact \| Confidence \| Effort \|\n\|(?:-+\|)+\n(?:\|[^\n]*\n)*?\| IDEA-0[1-4] \| 900 \| (?:3|2|1|0\.5|0\.25) \| (?:100|80|50) \| 3 \|
