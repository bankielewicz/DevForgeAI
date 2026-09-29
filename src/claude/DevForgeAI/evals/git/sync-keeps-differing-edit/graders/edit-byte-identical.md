---
type: regex
target: {source: file, path: config.yaml}
match: contains
---
^name: tally\nretries: 10\ntimeout: 30\n$
