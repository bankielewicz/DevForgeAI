---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
```yaml items[ \t]*\n[a-z_]+:.*\n(?:(?!```).*\n)*?[a-z_]+:
