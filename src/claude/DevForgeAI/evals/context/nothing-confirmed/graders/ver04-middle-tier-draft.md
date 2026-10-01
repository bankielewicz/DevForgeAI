---
type: regex
target: {source: file, path: docs/specs/context/middle-tier.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?status:[ \t]*["']?draft["']?[ \t]*(?:#[^\n]*)?\n)
