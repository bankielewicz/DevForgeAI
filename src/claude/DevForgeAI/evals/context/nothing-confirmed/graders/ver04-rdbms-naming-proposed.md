---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Naming[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
