---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
flags: m
---
^status: draft\n[\s\S]*^target_release: \"[^\"\n]*Spring pilot[^\"\n]*\"\n^stage: mvp\b[^\n]*\n^operating_context: pilot\b
