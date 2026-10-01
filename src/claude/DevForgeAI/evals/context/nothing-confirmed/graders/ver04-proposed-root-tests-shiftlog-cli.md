---
type: regex
target: {source: file, path: docs/specs/context/source-tree.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?SRC-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*path:[ \t]*["']?tests/shiftlog-cli/["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*basis:[ \t]*["']?proposed["']?[ \t]*(?:#[^\n]*)?\n)
