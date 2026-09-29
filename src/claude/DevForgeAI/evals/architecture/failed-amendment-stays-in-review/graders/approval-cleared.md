---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
^approved_by: ""[ \t]*\n^approved_on: null[ \t]*$
