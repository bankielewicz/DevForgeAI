---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-03["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?3a0c7359a7c2c9abd1f58f7d3a2b06a52d6cab9f15a714d7b9560ad86b15b0f1["']?[ \t]*(?:#[^\n]*)?\n)
