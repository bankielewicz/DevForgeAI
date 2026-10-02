---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
## 7\. Non-functional requirements\n(?:(?!## )[^\n]*\n)*?(?=[^ \t\n`])[^\n]*\b[Cc]ompliance\b[^\n]*(?:\b[Nn]one\b|\b[Nn]othing\b|\b[Nn]o (?:additional|further|extra|separate|specific|dedicated)\b|\b[Nn]ot needed\b|\bbeyond (?:the|what)\b|\b[Nn]o [a-z-]+(?: [a-z-]+){0,3} (?:applies|apply|is needed|are needed|is required|are required)\b)|## 7\. Non-functional requirements\n(?:(?!## )[^\n]*\n)*?(?=[^ \t\n`])[^\n]*(?:\b[Nn]one\b|\b[Nn]othing\b|\b[Nn]o (?:additional|further|extra|separate|specific|dedicated)\b|\b[Nn]ot needed\b|\bbeyond (?:the|what)\b|\b[Nn]o [a-z-]+(?: [a-z-]+){0,3} (?:applies|apply|is needed|are needed|is required|are required)\b)[^\n]*\b[Cc]ompliance\b
