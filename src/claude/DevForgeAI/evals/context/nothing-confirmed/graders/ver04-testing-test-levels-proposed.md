---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Test levels[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?(?:\n\|[^\n]*\bProposed\b[^\n]*\[NEEDS CLARIFICATION: confirm\b|\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b)
