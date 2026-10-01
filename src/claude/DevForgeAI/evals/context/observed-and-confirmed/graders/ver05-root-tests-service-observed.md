---
type: regex
target: {source: file, path: docs/specs/context/source-tree.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?SRC-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*path:[ \t]*["']?tests/service/["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*holds:[ \t]*["']?tests["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*basis:[ \t]*["']?observed["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*observed_in:[ \t]*["']?[^\"'\n]+["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*observed_on:[ \t]*["']?\d{4}-\d{2}-\d{2}["']?[ \t]*(?:#[^\n]*)?\n)
