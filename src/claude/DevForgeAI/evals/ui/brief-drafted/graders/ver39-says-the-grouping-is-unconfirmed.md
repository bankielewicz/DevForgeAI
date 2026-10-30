---
type: regex
target: last_message
match: contains
flags: i
---
\bun-?confirmed\b|\bnot (?:yet )?confirmed\b|\bawaiting (?:your )?confirmation\b|\bneeds? (?:your |the user['’]s )?confirmation\b|\bto confirm\b|\bhaven['’]t confirmed\b|\bpending confirmation\b|\b(?:is|are|was)n['’]t (?:yet )?confirmed\b|\b(?:could(?:n['’]t| not)|cannot|can['’]t) be confirmed\b|\bnot been confirmed\b
