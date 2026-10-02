---
type: regex
target: {source: file, path: remote/origin.git/push-log.txt}
match: contains
---
files: (?=[^\n]*\bapp\.py\b)(?=[^\n]*\btest_json\.py\b)
