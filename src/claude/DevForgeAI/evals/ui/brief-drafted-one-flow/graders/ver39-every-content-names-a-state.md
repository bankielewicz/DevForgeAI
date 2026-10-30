---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:^|\n)[ \t]*(?:\*\*|__)?Content\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!\b(?:empty|error|loading|loads?|mid-flow|no shifts?|zero shifts?|blank (?:list|table|state|week|report|screen)|nothing (?:recorded|yet)|not yet recorded|cannot be saved|can['’]t be saved)\b)(?!(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?
