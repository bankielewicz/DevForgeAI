---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Open questions[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\[NEEDS CLARIFICATION:[^\]\n]*IDEA-06
