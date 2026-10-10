---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Idea coverage[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\n\|[ \t]*`?IDEA-02`?[ \t]*\|[ \t]*`?none`?[ \t]*\|[ \t]*`?no board yet`?[ \t]*\|
