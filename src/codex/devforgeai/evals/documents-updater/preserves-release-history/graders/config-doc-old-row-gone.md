---
type: regex
target: {source: file, path: docs/configuration.md}
match: not_contains
flags: m
---
^\|[ \t]*`poll_interval`[ \t]*\|
