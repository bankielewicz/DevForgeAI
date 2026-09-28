---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
```yaml items[ \t]*\n(?:(?!```).*\n)*?[ \t]+(?:- )?(?!(?:id|status|superseded_by|upstream|statement|who|evidence|severity|idea|addresses|value|effort|risk|score|disposition|reason|validation|state):)[a-z_]+:
