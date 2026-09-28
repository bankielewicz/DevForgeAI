---
type: regex
target: {source: file, path: CHANGELOG.md}
match: not_contains
flags: m
---
^##[ \t]+\[?v?\d+\.\d+
