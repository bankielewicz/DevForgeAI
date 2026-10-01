---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Logging[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
