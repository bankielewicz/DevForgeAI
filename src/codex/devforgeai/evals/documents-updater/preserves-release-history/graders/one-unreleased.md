---
type: regex
target: {source: file, path: CHANGELOG.md}
match: not_contains
flags: m
---
^##[ \t]+\[?Unreleased[\s\S]*^##[ \t]+\[?Unreleased
