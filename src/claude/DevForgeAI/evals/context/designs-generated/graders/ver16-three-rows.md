---
type: regex
target: {source: file, path: docs/specs/context/ui-mockups.md}
match: not_contains
---
(?:\n\|[ \t]*STORY-\d{3}[ \t]*\|[^\n]*){4}
