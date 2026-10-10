---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Idea coverage[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\n\|[ \t]*`?IDEA-01`?[ \t]*\|[ \t]*`?BRD-03`?[ \t]*\|[ \t]*`?designed`?[ \t]*\|
