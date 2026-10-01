---
type: regex
target: {source: file, path: docs/specs/context/testing.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Fixtures and test data[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Proposed:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?\[NEEDS CLARIFICATION: confirm\b
