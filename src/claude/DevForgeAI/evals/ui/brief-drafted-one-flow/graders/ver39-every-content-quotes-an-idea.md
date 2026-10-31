---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:^|\n)[ \t]*(?:\*\*|__)?Content\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!["“](?:Add a shift from the terminal|List shifts in a table|A weekly report page|A dark theme for the report page)["”])(?!(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?
