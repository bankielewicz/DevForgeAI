---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-002.md}
match: not_contains
---
```yaml items[ \t]*\nideas:[ \t]*\n(?:(?!```)[\s\S])*[Dd]eposit
