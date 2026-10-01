---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?TEC-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*name:[ \t]*["']?[Tt][Yy][Pp][Ee][Rr](?: \d+(?:\.\d+)*)?["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*version_range:[ \t]*["']?[^\n]+["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*basis:[ \t]*["']?observed["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*observed_in:[ \t]*["']?pyproject\.toml["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*observed_on:[ \t]*["']?\d{4}-\d{2}-\d{2}["']?[ \t]*(?:#[^\n]*)?\n)
