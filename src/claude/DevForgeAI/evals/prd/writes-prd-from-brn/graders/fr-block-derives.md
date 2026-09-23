---
type: regex
target:
  source: file
  path: docs/specs/prd/PRD-001.md
pattern: '```yaml items\s*\n(#[^\n]*\n)*functional_requirements:\s*\n\s+- id: FR-001\b[\s\S]*?relation: derives'
---
