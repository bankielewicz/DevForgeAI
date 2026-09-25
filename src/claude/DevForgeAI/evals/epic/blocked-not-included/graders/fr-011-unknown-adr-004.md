---
type: regex
target: last_message
flags: i
pattern: '(?<![\w-])FR-011\b(?:\s*(?:,|and|&|/)\s*(?<![\w-])N?FR-\d{3}\b)*(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bunknown\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:\bADR-004\b))(?=(?:(?!(?<![\w-])N?FR-\d{3}\b)[^\n])*?(?:not found|missing|n[o’\'']t exist|does not exist|no such|absent|can[’\'']?t be found|cannot be found|couldn[’\'']t be found|could not be found|no file))'
---
