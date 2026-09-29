---
type: regex
target: {source: file, path: config.yaml}
match: contains
---
^name: tally\nretries: 5\ntimeout: 30\n$
