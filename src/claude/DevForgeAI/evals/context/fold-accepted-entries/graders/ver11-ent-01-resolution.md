---
type: regex
target: {source: file, path: docs/specs/ambiguities/AMB-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?ENT-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*question:[ \t]*["']?Typer 0\.12\.5)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*resolution:[ \t]*(?:\"folded into CTX-003 v3: already stated\"|'folded into CTX-003 v3: already stated')[ \t]*(?:#[^\n]*)?\n)
