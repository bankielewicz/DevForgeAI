---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n\|[ \t]*1[ \t]*\|[ \t]*\d{4}-\d{2}-\d{2}[ \t]*\|[ \t]*claude-code \(session [0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\)[ \t]*\|[ \t]*[^\n]*\|
