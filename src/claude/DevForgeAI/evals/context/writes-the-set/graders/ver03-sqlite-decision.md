---
type: regex
target: {source: file, path: docs/specs/context/tech-stack.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?TEC-\d{2}["']?[ \t]*\n(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*name:[ \t]*["']?[Ss][Qq][Ll][Ii][Tt][Ee](?: \d+(?:\.\d+)*)?["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*version_range:[ \t]*["']?3\.x["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*basis:[ \t]*["']?decision["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*(?:- id:[ \t]*["']?(?:TEC|SRC|ENT)-\d|```))[^\n]*\n)*?[ \t]*-[ \t]*(?:\{(?=[^}\n]*\bid:[ \t]*["']?ADR-002\b)(?=[^}\n]*\brelation:[ \t]*["']?constrains\b)[^}\n]*\}|id:[ \t]*["']?ADR-002["']?[ \t]*\n(?=(?:[ \t]+(?!- )[^\n]*\n){0,6}?[ \t]+relation:[ \t]*["']?constrains\b)))
