---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Idea coverage[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\n\|[ \t]*`?IDEA-04`?[ \t]*\|[ \t]*`?none`?[ \t]*\|[ \t]*`?not a screen`?[ \t]*\|
