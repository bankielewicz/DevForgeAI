---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-01["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?9dbca2f7ec0e4424d91460e526cb4871413930e499760a04594e7ee835a3fcf8["']?[ \t]*(?:#[^\n]*)?\n)
