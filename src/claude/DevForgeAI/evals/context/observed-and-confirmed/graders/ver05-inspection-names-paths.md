---
type: regex
target: last_message
match: contains
---
(?:^|\n)[ \t>*-]*(?:\*\*)?Inspection:(?:\*\*)?[ \t]*(?=[^\n]*pyproject\.toml)(?=[^\n]*src/shiftlog)(?=[^\n]*\btests/)
