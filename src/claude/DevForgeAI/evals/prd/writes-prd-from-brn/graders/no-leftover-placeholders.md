---
type: regex
target:
  source: file
  path: docs/specs/prd/PRD-001.md
match: not_contains
pattern: 'PRD-000|BRN-000|YYYY-MM-DD|\$\{|<outcome>|<metric>|<capability>|<product or release name>|<question>|<!-- (?!GENERATED)'
---
