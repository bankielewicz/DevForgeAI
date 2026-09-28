---
type: regex
target: {source: file, path: CHANGELOG.md}
match: not_contains
---
count_words|count_lines|[Rr]efactor|\b[Tt]ests?\b|[Hh]elper
