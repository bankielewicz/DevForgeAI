---
type: regex
target: {source: file, path: docs/specs/brainstorm/BRN-001.md}
match: not_contains
---
\n[ \t]+evidence: (?!"\[NEEDS CLARIFICATION: [^\[\]"\n]+\]"[ \t]*\n)(?!"[^"\n]+ \((?:document|data|ticket|interview|url|note): [^"\n]+\)"[ \t]*\n)
