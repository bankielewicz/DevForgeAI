---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Idea coverage[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\n\|[ \t]*`?IDEA-06`?[ \t]*\|[ \t]*`?BRD-05`?[ \t]*\|[ \t]*`?designed`?[ \t]*\|
