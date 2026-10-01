---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?TEC-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*name:[ \t]*["']?[Pp][Yy][Tt][Ee][Ss][Tt](?: \d+(?:\.\d+)*)?["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*version_range:[ \t]*["']?8\.x["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*basis:[ \t]*["']?convention["']?[ \t]*(?:#[^\n]*)?\n)
