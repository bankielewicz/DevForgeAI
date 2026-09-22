---
type: regex
target:
  source: file
  path: docs/specs/brainstorms/BRN-001-onboarding-drop-off.md
match: not_contains
pattern: '```yaml items\n(?:#[^\n]*\n|\s*\n)*(?!(?:problems|ideas|assumptions):)[A-Za-z_][\w-]*:'
---
