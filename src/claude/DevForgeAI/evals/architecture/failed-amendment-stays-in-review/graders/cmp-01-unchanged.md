---
type: regex
target: {source: file, path: docs/specs/arch/ARCH-001.md}
match: contains
---
  - id: CMP-01\n    status: current\n    name: "Volunteer web app"\n    responsibility: "Sign-in and booking screens; holds no data of its own"\n    owns_data: \[\]\n    interacts_with:\n      - "CMP-02"\n      - "CMP-03"\n    deployment: "Static site on the hosting provider"\n
