---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-02["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*sha256:[ \t]*["']?1646eb27e0ab916803e30426c8ab0b479141a0b5b90019f15531241818d3c14f["']?[ \t]*(?:#[^\n]*)?\n)
