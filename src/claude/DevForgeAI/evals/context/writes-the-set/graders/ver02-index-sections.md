---
type: regex
target: {source: file, path: docs/specs/context/index.md}
match: contains
---
^---[\s\S]*?\n---[ \t]*\n(?:(?!\n##[ \t])[\s\S])*\n##[ \t]+Documents[ \t]*\n(?:(?!\n##[ \t])[\s\S])*\n##[ \t]+Loading[ \t]*\n(?:(?!\n##[ \t])[\s\S])*\n##[ \t]+Change Log[ \t]*\n(?:(?!\n##[ \t])[\s\S])*$
