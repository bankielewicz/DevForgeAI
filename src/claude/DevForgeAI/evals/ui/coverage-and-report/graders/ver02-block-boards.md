---
type: regex
target: last_message
match: contains
flags: i
---
(?:^|\n)[ \t>*-]*(?:\*\*)?Boards:(?:\*\*)?[ \t]*docs/specs/design/DSN-001/boards/[^\n]*?\b4\b[^\n]*?\bversion 17-example\b
