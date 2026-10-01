---
type: regex
target: {source: file, path: docs/specs/context/rdbms.md}
match: contains
---
\n[ \t]*-[ \t]+\*\*Decision\*\*[ \t]*\([ \t]*ADR-002[ \t]*\):(?:(?!\n[ \t]*- |\n##|\n[ \t]*\n)[\s\S])*?
