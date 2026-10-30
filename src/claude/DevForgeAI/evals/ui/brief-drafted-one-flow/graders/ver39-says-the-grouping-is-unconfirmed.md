---
type: regex
target: last_message
match: contains
flags: i
---
\bun-?confirmed\b|\bnot (?:yet )?confirmed\b|\bawaiting (?:your )?confirmation\b|\bneeds? (?:your |the user['’]s )?confirmation\b|\bto confirm\b|\bhaven['’]t confirmed\b|\bpending confirmation\b
