---
type: regex
target: {source: file, path: docs/specs/context/back-end.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Jobs and queues[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\[NEEDS ADR:[^\]\n]*[Bb]roker
