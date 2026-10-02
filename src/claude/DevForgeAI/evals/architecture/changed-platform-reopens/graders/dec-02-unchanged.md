---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
  - id: DEC-02\n    status: active\n    question: "How are a volunteer's sessions revoked within 5 minutes \(NFR-001\)\?"\n    blocking: true\n    state: open\n    resolved_by: \[\]\n    notes: null\n    upstream:\n      - \{id: PRD-001, item: FR-001, relation: informed_by, version: 1, hash: null\}\n      - \{id: PRD-001, item: NFR-001, relation: informed_by, version: 1, hash: null\}\n
