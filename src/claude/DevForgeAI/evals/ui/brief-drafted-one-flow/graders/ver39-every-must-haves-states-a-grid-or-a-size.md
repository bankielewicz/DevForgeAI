---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!(?:\b\d{2,3}[ \t-]*(?:columns?|cols?)\s*(?:by|x|×|\*|and|,)?\s*\d{2,3}[ \t-]*rows?\b|\b\d{2,3}\s*(?:x|×|by)\s*\d{2,3}\s*(?:cells?|characters?|chars?|grid)\b|\b\d{3,4}[ \t-]*(?:px|pixels?)\b|\b\d{3,4}\s*(?:x|×|by)\s*\d{3,4}\b|\b\d{3,4}\s*(?:px|pixels?)?\s*(?:wide|tall|high)\b))(?!(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?|(?:^|\n)```[^\n]*\n(?:[ \t]*\n)*(?![^\n]*\b(?:web|browser|desktop|mobile)\b)[^\n]*\b(?:terminal|command line|CLI)\b[^\n]*(?:(?!```)[\s\S])*?(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!\b\d{2,3}[ \t-]*(?:columns?|cols?)\s*(?:by|x|×|\*|and|,)?\s*\d{2,3}[ \t-]*rows?\b|\b\d{2,3}\s*(?:x|×|by)\s*\d{2,3}\s*(?:cells?|characters?|chars?|grid)\b)(?!(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)
