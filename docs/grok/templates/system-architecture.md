# Template: System architecture

**Producer:** planned core `architect` (legacy `/create-system-architecture`)  
**Consumers:** work-set / `story-create`, `dev`, `qa`, `release`  
**Does not:** implement, create a second state store because an extra expert exists, or copy DevForgeAI runtime rules into a managed product.

## Envelope

| Field | Value |
| --- | --- |
| Document ID | SAD-[product]-[utc] |
| Producer | architect |
| Downstream consumer | story-create / dev / qa |
| Failure behavior | Missing shared-contract owner blocks dependent stories |
| Non-claims | Not source tree inventory of unimplemented files; not QA evidence |

## Upstream inputs

| Role | Locator | SHA-256 | Notes |
| --- | --- | --- | --- |
| Product requirements | | | |
| Business analysis | | | for business boundaries |
| Current source / manifests | | | brownfield |
| User stack decisions | | | |

## Context and quality attributes

- System purpose: [from PRD]
- Qualities that shape structure: [consistency, latency, auditability, … with PRD IDs]
- Explicit non-goals: [from PRD]

## Components and ownership

| ID | Responsibility | Owns state | Interfaces provided | Interfaces consumed | Must not own |
| --- | --- | --- | --- | --- | --- |
| COMP-001 | | | | | |

Every shared protocol/schema has **one** canonical owner. Stories reference it; they do not fork it.

## Interfaces

| ID | Owner | Contract summary | Error / denial | Concurrency / idempotency | Requirement IDs |
| --- | --- | --- | --- | --- | --- |
| IF-001 | | | | | |

## Decisions

| ID | Decision | Alternatives | Reason | Status |
| --- | --- | --- | --- | --- |
| ADR-001 | | | | accepted / proposed / rejected |

## Cross-cutting rules

- Authorization / tenancy:
- Data retention / secrets:
- Failure isolation:
- Observability:
- Transaction / race rules: [e.g. cancellation vs dispatch — single state owner]

## Open decisions

| ID | Question | Blocks | Return to |
| --- | --- | --- | --- |
| SAD-Q1 | missing business meaning | IF-… | discover / specify |

## Downstream handoff

**To work planning:** component/interface owners and which requirements they satisfy, so decomposition does not create duplicate contracts.

**To dev:** reuse existing components before adding responsibility; do not invent a parallel store.

**To qa:** race, denial, and invalid-transition scenarios implied by these boundaries.

**Return path:** two owners for one contract, or implementation that contradicts a boundary, returns here — not a silent story-local rewrite.
