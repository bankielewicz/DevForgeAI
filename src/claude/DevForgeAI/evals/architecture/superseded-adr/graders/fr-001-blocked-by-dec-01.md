---
type: regex
target: last_message
flags: i
pattern: '(?<![N\w-])FR-001\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,120}?\bblocked\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,80}?\bDEC-01\b|(?<![N\w-])FR-001\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,80}?\bDEC-01\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,40}?\bblocked\b|\bblocked\b[^\n]{0,40}?(?<![N\w-])FR-001\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n]){0,100}?\bDEC-01\b|\bblocked\b[^\n]*\n(?:[ \t]*(?:[-*]|\d+\.)[^\n]*\n){0,8}?[ \t]*(?:[-*]|\d+\.)[^\n]*?(?<![N\w-])FR-001\b(?:(?!(?<![N\w-])FR-00\d|NFR-00\d)[^\n])*?\bDEC-01\b'
---
