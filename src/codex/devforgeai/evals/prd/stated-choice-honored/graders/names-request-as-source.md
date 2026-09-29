---
type: regex
target: last_message
match: contains
---
(?:[Nn]ew PRD|PRD-002)[^\n.]{0,120}(?:\brequest|\byou (?:asked|said|chose|stated|requested)|\bas (?:you )?(?:asked|instructed|requested)|\byour (?:instruction|choice|prompt|message))|(?:\b[Rr]equest|\b[Yy]ou (?:asked|said|chose|stated|requested)|\b[Aa]s (?:you )?(?:asked|instructed|requested)|\b[Yy]our (?:instruction|choice|prompt|message))[^\n.]{0,120}(?:new PRD|PRD-002)
