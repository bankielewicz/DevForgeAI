---
type: regex
target: {source: file, path: docs/specs/design/DSN-001.md}
match: contains
---
^---[ \t]*\n(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?generated_by:(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+|[^\n]*[{,][ \t]*)tool:[ \t]*["']?claude-code["']?[ \t]*[,}\n#])(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?generated_by:(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+|[^\n]*[{,][ \t]*)model:[ \t]*["']?[A-Za-z0-9][^\"'\n,}]*["']?[ \t]*[,}\n#])(?=(?:(?!---[ \t]*\n)[^\n]*\n)*?generated_by:(?:[ \t]*\n(?:[ \t]+[^\n]*\n)*?[ \t]+|[^\n]*[{,][ \t]*)session:[ \t]*["']?[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}["']?[ \t]*[,}\n#])
