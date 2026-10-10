---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-03["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*status:[ \t]*["']?deprecated["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*file:[ \t]*["']?"?Add\.dc\.html"?["']?[ \t]*(?:#[^\n]*)?\n)
