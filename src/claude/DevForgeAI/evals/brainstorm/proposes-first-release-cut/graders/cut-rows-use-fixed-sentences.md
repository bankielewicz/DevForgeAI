---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
flags: m
---
^\| IDEA-\d{2} \| (?!yes \| (?:Tests ASM-\d{2}, ranked [1-3]\.|Highest score; no assumption ranked 1 to 3 picks an idea\.|Needed by IDEA-\d{2}, which is in the first release\.) \|[ \t]*$)(?!no \| (?:Tests no assumption ranked 1 to 3\.|Tests ASM-\d{2}, ranked [1-3], which IDEA-\d{2} already tests\.) \|[ \t]*$)
