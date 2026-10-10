---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-04["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?f52dbbcca7ce4951277c361f8ee22f416b9824c7ec2c48f96c479b88cd05390a["']?[ \t]*(?:#[^\n]*)?\n)
