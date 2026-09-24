---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(by hand|manually)[^\n]*ADR|ADR[^\n]*(by hand|manually)|architecture[^.\n]{0,60}(not|n''t)\s+(yet\s+)?(exist|available|built)|(not|n''t)\s+(yet\s+)?(exist|available|built)[^.\n]{0,20}architecture|planned as /devforgeai:architecture'
---
