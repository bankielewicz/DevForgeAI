---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
\n[ \t]*-[ \t]+\*\*Decision\*\*[ \t]*\([^)\n]*\bADR-002\b[^)\n]*\):(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?
