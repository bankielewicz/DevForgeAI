---
type: regex
target: {source: file, path: .git/HEAD}
match: contains
---
^ref: refs/heads/feat/x\n?$
