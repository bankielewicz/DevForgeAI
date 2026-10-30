---
type: regex
target: last_message
match: contains
flags: i
---
IDEA-04[^\n]{0,160}\b(?:no screen|names? no|not a screen|nothing|none|doesn['’]t|does not|no user interface|isn['’]t a screen)\b
