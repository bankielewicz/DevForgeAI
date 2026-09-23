# Interview

## Contents

- Stage and operating context
- Quality floor and stage depth
- Batching and budget
- Round 1: framing
- Round 2: architecture context
- Round 3: requirements
- Round 4: quality and constraints
- Round 5: success metrics
- Constraint or design
- New PRD or extension

## Stage and operating context

Two independent fields. Record each only when the user stated or confirmed it. A request that describes the
product in the terms of exactly one definition below states that value, for example "real patients will book
through it from day one" states `operating_context: production`. Never infer a value from the other field, from
the BRN's ideas, or from how the product sounds; when the request doesn't describe it, it is unknown.

**`stage`**: scope maturity. Controls interview depth.

| Value | Observable definition |
|---|---|
| `prototype` | Exploratory; may be thrown away. Nothing built on it is expected to last |
| `mvp` | The smallest scope that delivers value to real users, and that later work builds on |
| `evolution` | Changes an established product: a new capability, maintenance, a migration or a refactoring |

**`operating_context`**: who uses it, with what data. Controls which quality categories must be asked.

| Value | Observable definition |
|---|---|
| `local` | Developers only, synthetic data |
| `internal` | People in the user's own organization; may touch real internal data |
| `pilot` | A limited group of real external users, or real customer data |
| `production` | Generally available to real users with real data |

"An MVP real customers use from day one" is `stage: mvp` with `operating_context: production`. Never infer
one field from the other.

## Quality floor and stage depth

**Floor** of NFR categories that must be asked, by operating context (a framework requirement; policy can
add to it through `quality.required_categories`, never remove from it):

| Operating context | Required categories |
|---|---|
| `local` | constraint |
| `internal` | constraint, security, privacy |
| `pilot` | constraint, security, privacy, reliability, observability, compliance |
| `production` | constraint, security, privacy, reliability, observability, compliance, performance, accessibility |
| unknown | ask it in round 1; if it can't be asked, use the `production` row to decide what to mark, and leave `operating_context: null` |

Always also offer one open question: "Any other quality need (usability, maintainability, anything else)?"

**Depth** by stage:

| Stage | Depth |
|---|---|
| `prototype` | Requirements at capability level only; a minimal rollout section |
| `mvp` | Confirm priority and release of each current-release requirement |
| `evolution` | As mvp, plus ask about effects on existing behaviour, users, data and systems |
| unknown | Ask it in round 1; if it stays unanswered, `stage: null` |

## Batching and budget

- At most **4 questions per AskUserQuestion call**, each with 2 to 4 options (a platform limit). The user can
  always answer "Other" in their own words.
- At most **`interview.max_calls` calls** in the whole interview, as resolved by `policy.md` (default 8).
  Exceed it only if the user asks to continue.
- Plan the calls before asking: drop every question the BRN or the request already answers, then merge
  rounds into as few calls as fit. Rounds may share a call.
- When the budget runs out, record each question still unasked as `[NEEDS CLARIFICATION: <question>]`
  (and each required quality category as its category marker).
- **Non-interactive** (the request says to proceed without questions, or no one can answer): ask no interview
  question at all. Every open decision stays `null`, and every gap becomes a marker.
- Questions may propose a value ("Suggested: mvp"), but a suggestion is written only when the user confirms it.

## Round 1: framing

Ask only what is missing:

- **Stage:** prototype, MVP or evolution (with the definitions above)?
- **Operating context:** local, internal, pilot or production? Always ask when unknown; it decides round 4.
- **Current release name** (`target_release`), for example "MVP" or "v2.1".
- **Primary users**, only if the BRN's target users section is empty or unclear.
- **Non-goals** beyond the parked and rejected ideas already listed in words.
- **Owner**, only if neither the request nor the BRN gives one.

## Round 2: architecture context

Sources: ADRs in `docs/specs/adr/`, and documents the BRN or the request names. Never crawl the codebase.

1. List the accepted ADRs (`status: accepted`, not superseded). Propose which apply to this product, and ask
   the user to confirm. Non-interactive: use only the ADRs the request names.
2. Ask whether any system, platform or integration is fixed (a hard constraint), and where it applies.
3. Ask whether any architecture decision is still open that affects these requirements.
4. For each design preference in the request, ask whether it is a hard constraint (Constraint or design).

Classify each answer:

| What was learned | Written as |
|---|---|
| An accepted ADR that applies | frontmatter `{id: ADR-NNN, relation: constrains, version: N, hash: null}` |
| A hard constraint | NFR with `category: constraint`, stating the condition and where it applies |
| A preference, not a hard constraint | open question: `Design preference for a future ADR: … (not a requirement)` |
| An open decision, or a **proposed** ADR | `[NEEDS ADR: <decision>; affects FR-NNN, …]`, naming the FRs whose epics it blocks. Never link a proposed ADR |
| A mandated platform from policy (R2) | NFR with `category: constraint`, citing its setting (see `output-rules.md`, Links) |
| A superseded ADR | nothing |

Never decide a design question in the PRD.

## Round 3: requirements

One question per drafted FR (and per NFR drafted from the request), showing the statement:

> FR-002: "The system shall let a patient move or cancel their own appointment online." For the current
> release (`<target_release>`)?
> Options: **Must, now** · **Should, now** · **Later** · **Won't**

| Answer | `priority` | `release` |
|---|---|---|
| Must, now | `must` | `current` |
| Should, now | `should` | `current` |
| Later | `null` (only the release was decided) | `later` |
| Won't | `wont` | `current` (an explicit exclusion from this release) |
| "Decide later", or no answer | `null` | `null` |

If the user means a requirement should never be built, they edit or drop it ("Other") instead of choosing
Won't. The user may edit the statement in "Other". For `prototype`, ask at capability level: one question may
cover several FRs of the same idea. For `evolution`, add one question on effects on existing behaviour.

## Round 4: quality and constraints

Ask each required category (Quality floor plus policy additions) that the request doesn't already answer, with
concrete options, for example:

- security: "Must users sign in? Which roles see what?"
- privacy: "Which personal data is stored, and who may see it?"
- reliability: "What availability and recovery are needed?"
- observability: "What must be monitored or alerted on?"
- compliance: "Which regulations or certifications apply?"
- performance: "What response time or load must it meet?"
- accessibility: "Which accessibility standard applies (for example WCAG 2.2 AA)?"
- constraint: "Which platforms, integrations, data residency or existing systems are fixed?"

Plus the open "anything else" question. Each answer becomes an NFR in its category, with priority and release
asked or `null`. Each required category not answered becomes
`[NEEDS CLARIFICATION: <category> requirements for <context>]`. Never write a placeholder NFR.

**Shared constraints (BEH-15).** Before writing a constraint or cross-cutting NFR, check the other PRDs in
`docs/specs/prd/`. If one already defines it, don't copy it: add a frontmatter
`{id: PRD-NNN, item: NFR-NNN, relation: constrains, version: N, hash: null}` link and say in section 9 what it
applies to here. A new constraint's statement ends with where it applies (whole product, a named capability,
or an environment).

## Round 5: success metrics

For each metric drafted from the BRN's success signals: ask for the baseline and target together. Unanswered
values are `[NEEDS CLARIFICATION: …]` markers.

## Constraint or design

A **constraint** is a fixed external condition the product must accept: a mandated platform ("must run on
AWS"), a required integration ("must integrate with Stripe"), data residency, an existing system of record,
a regulatory mandate. Record it as an NFR with `category: constraint`.

A **design choice** is how the product is built: an architecture style ("microservices"), a framework, a
database, a sync-or-async choice. It is never a requirement or a constraint in a PRD. When the user offers
one, ask whether it is a hard constraint. If yes, record it as a constraint. If no, or no one can answer,
record it only as `Design preference for a future ADR: <preference> (not a requirement)` in open questions.

## New PRD or extension

Ask this whenever `docs/specs/prd/` holds any PRD. Read each PRD's `title`, goals, non-goals, `owner`,
`status` and `target_release`, and compare with the BRN's promoted ideas:

| Criterion | Recommend extending PRD-NNN when | Recommend a new PRD when |
|---|---|---|
| Scope | The ideas belong to that PRD's existing initiative and goals | They form a distinct initiative or outcome |
| Ownership | Same owner and approval path | Different owner or approval path |
| Lifecycle | They fit its `target_release` and schedule | They follow a different schedule or release |

- Recommend extending only when all three favour it. Being the same product, or being the only PRD, is never a
  reason on its own.
- State the recommendation and the reasons for each criterion in the reply text, then ask. Write nothing until
  the user answers, even in a non-interactive run.

**Extending** (the user chose it): `version` + 1, `updated` today, new items take the next free number in each
collection, every existing item stays byte-identical, add the new BRN's links, add a Change Log row. If
`status` was `approved`, set `status: in-review`, `approved_by: ""` and `approved_on: null`. Tell the user that
epics citing this PRD are now suspect links to re-review.
