---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?[ \t]*-[ \t]*\{(?![^}\n]*\bitem:)(?=[^}\n]*\bid:[ \t]*["']?BRN-001\b)(?=[^}\n]*\brelation:[ \t]*["']?derives\b)(?=[^}\n]*\bversion:[ \t]*["']?1\b)[^}\n]*\})
