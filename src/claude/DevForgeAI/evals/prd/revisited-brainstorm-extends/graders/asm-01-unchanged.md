---
type: regex
target: {source: file, path: docs/specs/prd/PRD-001.md}
match: contains
---
  - id: ASM-01\n    status: active\n    statement: "We believe that most volunteers will sign up online once they can see open shifts\."\n    validation: "Share of shifts filled online in the first month"\n    state: open\n    upstream:\n      - \{id: BRN-001, item: ASM-01, relation: derives, version: 1, hash: null\}\n
