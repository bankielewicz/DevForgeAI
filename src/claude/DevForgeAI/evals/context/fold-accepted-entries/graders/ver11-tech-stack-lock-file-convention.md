---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Upgrades[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\*\*Convention:\*\*(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?[Ll]ock[ -]?file
