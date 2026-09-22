---
type: regex
target:
  source: file
  path: docs/specs/brainstorms/BRN-001-onboarding-drop-off.md
match: not_contains
pattern: 'BRN-000|YYYY-MM-DD|<!--|\$\{|<topic>|<persona>|<idea>|<signal>|<question>|<one sentence|<source link|<we believe|<experiment'
---
