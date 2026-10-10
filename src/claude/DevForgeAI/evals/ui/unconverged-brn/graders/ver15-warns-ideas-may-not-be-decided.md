---
type: regex
target: last_message
match: contains
flags: i
---
\bideas?\b[^\n]{0,100}\b(?:may|might|could)\b[^\n]{0,60}\bnot\b[^\n]{0,40}\b(?:decided|settled|final|confirmed|converged)\b|\bnot (?:yet )?(?:converged|decided)\b|\bundecided\b|\bnot all (?:of )?the ideas\b
