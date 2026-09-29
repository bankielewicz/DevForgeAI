---
type: regex
target: {source: file, path: .gitignore}
match: contains
---
^__pycache__/\n\*\.pyc\n$
