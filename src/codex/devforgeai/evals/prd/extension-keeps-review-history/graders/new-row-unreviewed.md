---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
\n\| 2 \| \d{4}-\d{2}-\d{2} \| codex \(session [^)\n]+\) \|[^\n]*(?:(?:has not|hasn't|have not|not)(?: yet)? been reviewed|[Uu]nreviewed)
