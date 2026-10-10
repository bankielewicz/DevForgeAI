---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: not_contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Idea coverage[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\|[ \t]*not a screen[ \t]*\|
