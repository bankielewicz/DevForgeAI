---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
```yaml items[ \t]*\n(?!(?:problems|ideas|assumptions):)
