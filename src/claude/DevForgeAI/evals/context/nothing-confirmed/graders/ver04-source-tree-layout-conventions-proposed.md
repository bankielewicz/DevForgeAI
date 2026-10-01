---
type: regex
target: {source: file, path: docs/specs/context/source-tree.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Layout conventions[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
