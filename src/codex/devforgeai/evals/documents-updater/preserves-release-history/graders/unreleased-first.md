---
type: regex
target: {source: file, path: CHANGELOG.md}
match: contains
flags: m
---
^## \[?Unreleased\]?[ \t]*\n[\s\S]*^## \[1\.0\.0\]
