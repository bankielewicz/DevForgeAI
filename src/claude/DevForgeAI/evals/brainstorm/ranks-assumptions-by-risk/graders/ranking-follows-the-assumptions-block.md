---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^## 7\. Assumptions and open questions\n[\s\S]*?^```[ \t]*\n+### Assumption risk ranking[ \t]*\n+\| Rank \| Assumption \| If wrong \| Confidence \| Cheapest test \|[ \t]*\n\|(?:[ \t]*:?-+:?[ \t]*\|){5}[ \t]*\n\| 1 \| ASM-\d{2} \|
