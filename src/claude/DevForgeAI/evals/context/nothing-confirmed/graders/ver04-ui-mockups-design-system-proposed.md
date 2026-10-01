---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Design system[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
