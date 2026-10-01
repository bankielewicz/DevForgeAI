---
type: regex
target: {source: file, path: docs/specs/context/index.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Loading[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*DevForgeAI rule — context loading:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?read this index first
