---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Idea coverage[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\n\|[ \t]*Idea[ \t]*\|[ \t]*Boards[ \t]*\|[ \t]*Status[ \t]*\|[ \t]*\n\|[-| :\t]+\|[ \t]*(?:\n\|[^\n]*){5}(?=\n(?!\|)|$)
