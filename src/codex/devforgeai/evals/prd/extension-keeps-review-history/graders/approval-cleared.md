---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^approved_by: ""[ \t]*\n^approved_on: null[ \t]*$
