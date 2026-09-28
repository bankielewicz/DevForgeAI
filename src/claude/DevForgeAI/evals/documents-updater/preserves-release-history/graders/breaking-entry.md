---
type: regex
target: {source: file, path: CHANGELOG.md}
match: contains
flags: m
---
^[^\n]*(?:[Bb]reaking|BREAKING)[^\n]*poll_interval_seconds|^[^\n]*poll_interval_seconds[^\n]*(?:[Bb]reaking|BREAKING)
