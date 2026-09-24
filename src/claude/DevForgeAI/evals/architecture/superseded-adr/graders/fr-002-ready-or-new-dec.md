---
type: regex
target: last_message
flags: i
pattern: '(?<![N\w-])FR-002\b(?:(?!\bblock)[^\n.;]){0,100}?(?<!\bnot\s)(?<!\bnot yet\s)(?<![’'']t\s)(?<!\bnothing is\s)(?<!\bnone are\s)(?<!\bno requirement is\s)(?<!\bno requirements are\s)\bready\b|(?<!\bnot\s)(?<!\bnot yet\s)(?<![’'']t\s)(?<!\bnothing is\s)(?<!\bnone are\s)(?<!\bno requirement is\s)(?<!\bno requirements are\s)\bready\b(?![^\n]*\bnone\b)(?:(?!\bblock)[^\n.;])*?(?<![N\w-])FR-002\b|(?<!\bnot\s)(?<!\bnot yet\s)(?<![’'']t\s)(?<!\bnothing is\s)(?<!\bnone are\s)(?<!\bno requirement is\s)(?<!\bno requirements are\s)\bready\b(?![^\n]*\bnone\b)[^\n]*\n(?:[ \t]*(?:[-*]|\d+\.)(?![^\n]*\bblock)[^\n]*\n){0,8}?[ \t]*(?:[-*]|\d+\.)(?![^\n]*\bblock)[^\n]*?(?<![N\w-])FR-002\b|(?<![N\w-])FR-002\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,80}?\bblocked\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,60}?\bDEC-(?:0[3-9]|[1-9]\d)\b'
---
