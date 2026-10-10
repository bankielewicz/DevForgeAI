---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-05["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?96efa6de4660518bfbf93f38038081a9a3e705b2bf831b4633d01b36d0c9284c["']?[ \t]*(?:#[^\n]*)?\n)
