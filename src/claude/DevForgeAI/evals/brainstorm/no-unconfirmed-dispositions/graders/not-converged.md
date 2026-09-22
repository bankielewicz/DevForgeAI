---
type: regex
target:
  source: file
  path: docs/specs/brainstorms/BRN-001-onboarding-drop-off.md
match: not_contains
pattern: '(^|\n)status:\s*"?converged'
---
