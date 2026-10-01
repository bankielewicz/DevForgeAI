---
type: regex
target: {source: file, path: docs/specs/context/middle-tier.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?id:[ \t]*["']?CTX-012["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?document:[ \t]*["']?middle-tier["']?[ \t]*(?:#[^\n]*)?\n)
