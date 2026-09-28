---
type: regex
target: {source: file, path: CHANGELOG.md}
match: contains
flags: m
---
^### Added[ \t]*\n(?:(?!#)[^\n]*\n)*?(?!#)[^\n]*--json
