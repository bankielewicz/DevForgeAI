---
type: regex
target: {source: file, path: docs/specs/context/front-end.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Interaction and output[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
