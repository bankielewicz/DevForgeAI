---
type: regex
target: last_message
match: contains
flags: i
---
next (?:free )?(?:number|ID)[^\n]{0,60}DSN-002|DSN-002[^\n]{0,60}next (?:free )?(?:number|ID)|\bDSN-002\b[^\n]{0,80}\bnext\b
