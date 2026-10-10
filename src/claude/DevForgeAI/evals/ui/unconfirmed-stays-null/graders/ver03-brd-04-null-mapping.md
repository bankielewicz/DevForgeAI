---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
(?:^|\n)[ \t]*- id:[ \t]*["']?BRD-04["']?[ \t]*\n(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*file:[ \t]*["']?Report\.dc\.html["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*title:[ \t]*["']?Report["']?[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*flow:[ \t]*(?:null|~)[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*surface:[ \t]*(?:null|~)[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*ideas:[ \t]*(?:null|~)[ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*answers:[ \t]*\[[ \t]*\][ \t]*(?:#[^\n]*)?\n)(?=(?:(?![ \t]*- id:[ \t]*["']?BRD-\d|```)[^\n]*\n)*?[ \t]*notes:[^\n]*\[NEEDS CLARIFICATION)
