---
type: regex
target: {source: file, path: docs/specs/ambiguities/AMB-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?ENT-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*question:[ \t]*["']?source-tree\.md names no fixtures)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*state:[ \t]*["']?open["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*resolution:[ \t]*(?:\"\"|'')[ \t]*(?:#[^\n]*)?\n)
