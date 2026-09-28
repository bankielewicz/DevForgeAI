---
type: regex
target: {source: file, path: CHANGELOG.md}
match: not_contains
flags: m
---
^##[ \t]+\[?v?(?!1\.0\.0\]|0\.9\.0\])\d
