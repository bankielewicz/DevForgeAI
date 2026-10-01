---
type: regex
target: {source: file, path: docs/specs/ambiguities/AMB-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?ENT-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*question:[ \t]*["']?Commit the lock file)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*resolution:[ \t]*(?:\"folded into CTX-003 v3\"|'folded into CTX-003 v3')[ \t]*(?:#[^\n]*)?\n)
