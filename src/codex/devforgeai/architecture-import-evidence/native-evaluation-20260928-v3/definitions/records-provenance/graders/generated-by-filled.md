---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
flags: m
---
^generated_by:\n^  tool: "codex"\n^  model: "[^"\n]+"\n^  session: "[^"\n]+"\n
