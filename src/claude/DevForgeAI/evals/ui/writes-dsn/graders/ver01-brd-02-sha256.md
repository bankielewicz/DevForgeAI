---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-02["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?e0f35f0cbd436f532b9b32cea5316dc067fa0370d144b197b5855d49587e5c6c["']?[ \t]*(?:#[^\n]*)?\n)
