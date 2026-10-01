---
type: regex
target: {source: file, path: docs/specs/context/middle-tier.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Validation[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
