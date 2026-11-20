---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^- IDEA-01 tests (?:ASM-\d\d(?:, ASM-\d\d)*|no assumption)$
