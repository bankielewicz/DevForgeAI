---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Investigating a failing test[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*DevForgeAI rule — investigating a failing test:\*\*
