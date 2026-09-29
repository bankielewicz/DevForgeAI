---
type: regex
target: {source: file, path: remote/origin.git/push-log.txt}
match: contains
flags: m
---
^refs/heads/feat/json-output based[ ]
