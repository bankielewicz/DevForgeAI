---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
\n\|[ \t]*3[ \t]*\|[^\n]*\|[ \t]*claude-code \(session [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)[ \t]*\|
