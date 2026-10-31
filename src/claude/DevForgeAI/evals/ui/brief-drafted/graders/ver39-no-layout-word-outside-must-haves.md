---
type: regex
target: last_message
match: not_contains
flags: i
---
(?:(?:^|\n)[ \t]*(?:\*\*|__)?Context\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?|(?:^|\n)[ \t]*(?:\*\*|__)?Content\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)(?:(?!```|(?:^|\n)[ \t]*(?:\*\*|__)?Must[- ]haves?\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?)[\s\S])*?\b(?:side ?bars?|headers?|footers?|toolbars?|nav ?bars?|top bars?|status bars?|tab bars?|panels?|panes?|cards?|tiles?|modals?|dialogs?|dropdowns?|buttons?|padding|margins?|spacing|gutters?|align(?:ed|ment)?|left[- ]hand|right[- ]hand|(?:top|bottom)[- ](?:left|right)|on the (?:left|right)|at the (?:top|bottom)|(?:two|three|four)[- ]columns?|above the|below the|next to the|beside)\b|(?:^|\n)[ \t]*(?:\*\*|__)?Style\b(?:\*\*|__)?[ \t]*:?(?:\*\*|__)?(?:(?!```|Give me 3 distinctly different directions of the key screen first, with a one-line tradeoff under each\.)[\s\S])*?\b(?:side ?bars?|headers?|footers?|toolbars?|nav ?bars?|top bars?|status bars?|tab bars?|panels?|panes?|cards?|tiles?|modals?|dialogs?|dropdowns?|buttons?|padding|margins?|spacing|gutters?|align(?:ed|ment)?|left[- ]hand|right[- ]hand|(?:top|bottom)[- ](?:left|right)|on the (?:left|right)|at the (?:top|bottom)|(?:two|three|four)[- ]columns?|above the|below the|next to the|beside)\b
