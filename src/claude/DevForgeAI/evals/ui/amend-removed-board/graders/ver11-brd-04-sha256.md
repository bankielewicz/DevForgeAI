---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-04["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?aff1a97fda77e9736ce17e6cdea97340258cba345bed608c9346cf4865a122c1["']?[ \t]*(?:#[^\n]*)?\n)
