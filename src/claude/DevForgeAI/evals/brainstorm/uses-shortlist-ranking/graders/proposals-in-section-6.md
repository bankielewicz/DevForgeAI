---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
flags: m
---
^## 6\. Convergence\n(?:(?!^## 7\. )[\s\S])*?^(?:> )?Proposed, awaiting confirmation: promote (?:IDEA-\d\d|none)
