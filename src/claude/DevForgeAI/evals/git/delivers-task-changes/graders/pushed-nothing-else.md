---
type: regex
target: {source: file, path: remote/origin.git/push-log.txt}
match: not_contains
---
files: [^\n]*(?:notes/todo\.md|__pycache__|Zone\.Identifier|README\.md|AGENTS\.md)
