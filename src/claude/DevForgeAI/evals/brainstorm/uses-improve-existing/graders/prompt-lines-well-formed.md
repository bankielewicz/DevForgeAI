---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^- (?:Substitute|Combine|Adapt|Modify|Put to another use|Eliminate|Reverse): (?!(?:IDEA-\d\d(?:, IDEA-\d\d)?|no idea \([^\n]+\))$)
