# Technical Specification Guide

Index of domain-specific technical specification sub-references. Phase 03 Step 3.2.5 loads the relevant sub-file after API type detection (Step 3.2). Non-API stories load no sub-file.

---

## Sub-References

| Sub-Reference | When to Load | API Type |
|--------------|--------------|----------|
| `technical-specification-guide-rest.md` | Story has REST/HTTP endpoints | REST / OpenAPI |
| `technical-specification-guide-graphql.md` | Story has GraphQL API | GraphQL |
| `technical-specification-guide-grpc.md` | Story has gRPC service | gRPC / Protocol Buffers |

For non-API stories (no endpoint detected by Step 3.2), no sub-file is loaded — the inline Phase 03 templates in `technical-specification-creation.md` suffice.

---

## Progressive Disclosure

**When to load sub-references:**
- Phase 03 Step 3.2.5 — after `detect-indicators` classifies the API type
- Each sub-file is loaded on-demand, not unconditionally

**Why progressive:**
- REST guide alone is ~350 lines vs. 1,269 lines for the original monolithic file
- GraphQL and gRPC stories load only the patterns relevant to their protocol
- Non-API stories load nothing — saves the full 1,269-line context budget

---

**Use the sub-references above to document API contracts, data models, business rules, and dependencies in your technical specification.**
