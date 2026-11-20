---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: contains
---
value: "(?:high|medium|low)"[^\n]*\n[ \t]+effort: "(?:high|medium|low)"[^\n]*\n[ \t]+risk: "(?:high|medium|low)"[^\n]*\n[ \t]+score: -?[0-4]\b
