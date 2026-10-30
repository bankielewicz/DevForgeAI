---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!```|(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*?\b(?:side ?bars?|headers?|footers?|toolbars?|nav ?bars?|top bars?|status bars?|tab bars?|panels?|panes?|cards?|tiles?|modals?|dialogs?|dropdowns?|buttons?|padding|margins?|spacing|gutters?|align(?:ed|ment)?|left[- ]hand|right[- ]hand|(?:top|bottom)[- ](?:left|right)|on the (?:left|right)|at the (?:top|bottom)|(?:two|three|four)[- ]columns?|above the|below the|next to the|beside)\b(?:(?!```|(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?
