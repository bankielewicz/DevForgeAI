---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?The pass rule[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*DevForgeAI rule — pass rule:\*\*
