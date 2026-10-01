---
type: regex
target: {source: file, path: docs/specs/context/architecture.md}
match: contains
---
\n##[ \t]+(?:\d+\.[ \t]+)?Components[^\n]*\n(?:(?!\n##[ \t])[\s\S])*?\n\|[^\n]*ARCH-001#CMP-04\b
