---
type: llm
focus: {source: file, path: docs/specs/prd/PRD-001.md}
---

The user said: "It must run on AWS and must integrate with Stripe; I'm leaning towards
microservices", and asked the skill not to ask questions.
Judge only these claims:
1. AWS and Stripe each appear as a non-functional requirement with category constraint, stated
   as a condition (not a design) and saying where it applies.
2. Microservices appears in no functional or non-functional requirement. If it appears at all,
   it is in the open questions as a design preference or decision for a future ADR.
PASS if both hold. FAIL otherwise, quoting the offending line.
