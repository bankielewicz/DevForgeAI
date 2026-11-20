---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^\| \d+ \| ASM-\d{2} \| Minor: [^\n]*\n(?:\|[^\n]*\n)*?\| \d+ \| ASM-\d{2} \| (?:Fatal|Serious):
