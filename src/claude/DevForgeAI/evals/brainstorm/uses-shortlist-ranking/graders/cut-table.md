---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^\| Rank \| Idea \| Score \| Effort \| Cumulative effort \| Cut \|\n\|(?:-+\|)+\n\| 1 \| IDEA-0[1-4] \| \d+\.\d \| [\d.]+ \| [\d.]+ \| (?:must|should|could|won't) \|$
