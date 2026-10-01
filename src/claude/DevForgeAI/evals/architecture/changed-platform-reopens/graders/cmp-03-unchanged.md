---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
  - id: CMP-03\n    status: active\n    name: "Identity platform"\n    responsibility: "Authenticates volunteers and issues sessions; provided by the organization"\n    owns_data:\n      - "Volunteer credentials"\n    interacts_with:\n      - "CMP-01"\n    deployment: "External: Org A Identity Platform \(OIDC\)"\n    upstream:\n      - \{id: POL-001, item: SET-01, relation: constrains, version: 3, hash: null\}\n
