---
type: regex
target: last_message
match: contains
flags: i
---
\bpaths?\b[^\n]{0,80}(?:not accepted|aren['’]t accepted|isn['’]t accepted|never|not (?:taken|allowed|supported)|refus|can['’]t|cannot)|(?:never|not|doesn['’]t|don['’]t|won['’]t|no)[^\n]{0,60}\bpaths?\b
