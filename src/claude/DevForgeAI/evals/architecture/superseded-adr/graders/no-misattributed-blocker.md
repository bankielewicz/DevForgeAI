---
type: regex
target: last_message
flags: i
match: not_contains
pattern: '(?:\bNFR-001\b|(?<![N\w-])FR-002\b)(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n.;]){0,80}?\b(?:blocked|waits?|waiting)\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n.;]){0,60}?\bDEC-0[12]\b|\bDEC-0[12]\b[^\n.;]{0,40}\bblocks?\b(?:(?!\bready\b|\bwhile\b|\bbut\b)[^\n.;]){0,40}?(?:\bNFR-001\b|(?<![N\w-])FR-002\b)|\bblocked\b[^\n]*\n(?:[ \t]*(?:[-*]|\d+\.)[^\n]*\n){0,8}?[ \t]*(?:[-*]|\d+\.)[^\n]*?(?:\bNFR-001\b|(?<![N\w-])FR-002\b)[^\n]*?\bDEC-0[12]\b'
---
