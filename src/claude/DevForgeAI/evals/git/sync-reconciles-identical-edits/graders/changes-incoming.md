---
type: regex
target: {source: file, path: CHANGES.md}
match: contains
---
^# Changes\n\n- Retry uploads five times\.\n$
