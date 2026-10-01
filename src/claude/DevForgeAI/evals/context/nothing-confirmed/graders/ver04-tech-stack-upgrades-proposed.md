---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Upgrades[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
