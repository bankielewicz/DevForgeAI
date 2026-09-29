---
type: regex
target: {source: file, path: .git/config}
match: contains
---
\[remote \x22origin\x22\][^\[]*\burl = \S*remote/app\.git\b
