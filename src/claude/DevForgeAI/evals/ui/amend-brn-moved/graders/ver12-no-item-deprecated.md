---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
status:[ \t]*["']?deprecated
