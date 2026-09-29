# Interview: question bank and batching

## Contents

- Rules for every call
- Before the rounds: the gates
- Round 1: framing
- Round 2: architecture context
- Round 3: requirements
- Round 4: quality and constraints
- Round 5: success metrics
- Depth by stage
- Recording answers

## Rules for every call

- **Draft first.** Ask only about gaps in the draft (SKILL.md step 6). Skip every question that the
  BRN, the request or an earlier answer already settles, and say in one line what you skipped and why.
- **Batch.** At most **3 questions per batch** and the active host tool limits (codex.md).
  Preserve all original options below; use numbered plain text if four options, multi-select
  or free-form answers cannot be represented faithfully. The user can answer in their own words.
  Group questions from the same round, filling unused capacity from the next round.
- **Budget.** At most `interview.max_calls` calls in total (policy step; default 8), counting gate
  questions. Stop asking when the budget is spent unless the user asks for more, and record every
  remaining gap as `[NEEDS CLARIFICATION: …]`.
- **Suggest, never assume.** An option may carry your suggestion, marked "(suggested)". A
  suggestion is written only after the user picks it.
- **No permitted question tool or incomplete choice support?** Ask the same questions as a
  numbered plain-text list, then end your turn. Do not infer an answer from a preselected default.
- **"Proceed without questions"** skips all rounds. It does not answer the gates.

## Before the rounds: the gates

These are asked when reached, even under "proceed without questions", and nothing is written
without an answer. A gate the request answers explicitly ("extend PRD-001", "it's a draft, continue
anyway") is not asked again; say in the reply that the request answered it.
- which BRN, when no ID was given (list unprocessed BRNs with titles and uncited promoted ideas);
- continue from an unconverged BRN? (options: continue anyway; stop and converge the brainstorm first);
- new PRD or extend PRD-NNN? State your recommendation first, with reasons about scope, owner and
  release lifecycle. Options: new PRD (recommended, if so); extend PRD-NNN.

## Round 1: framing

| Question | Options | Skip when |
|---|---|---|
| Stage? | prototype (exploratory, may be discarded); mvp (smallest scope real users get value from, built upon); evolution (changes an established product) | The request or BRN states it |
| Operating context? Ask first when unknown; it decides the quality questions | local (developers only, synthetic data); internal (own organization, may touch real internal data); pilot (limited real external users or real customer data); production (generally available, real users and data) | The request or BRN states it |
| Name of the current release (`target_release`)? | "MVP"; "v1"; "Pilot" (suggestions) | The request names it |
| Primary users? | The personas the BRN names, plus "others" | The BRN's target users section names them |
| Non-goals beyond the parked and rejected ideas? | none; list them | The request states them |

## Round 2: architecture context

- Which accepted ADRs apply? List each accepted, non-superseded ADR with a one-line proposal
  (applies or not). This is multi-select.
- For each design preference the user stated ("microservices", "React"): is it a hard constraint?
  Options: hard constraint; preference only (goes to open questions as a future ADR).
- Any fixed external conditions? Options: mandated platform; required integration; data residency
  or regulation; existing system to keep.
- Any architecture question still open that affects requirements? Each answer becomes a
  `[NEEDS ADR: <decision>; affects FR-NNN, …]` marker.

## Round 3: requirements

One question per drafted requirement, showing its statement:

| Option | Writes |
|---|---|
| must now | `priority: must`, `release: current` |
| should now | `priority: should`, `release: current` |
| later | `release: later`, `priority: null` |
| won't (this release) | `priority: wont`, `release: current` |

The user may also edit the statement, answer "could now" (`priority: could`, `release: current`), or
answer "decide later", which leaves both `null`. A requirement that should never be built is edited
or dropped, not marked `wont`.

## Round 4: quality and constraints

**Which categories must be asked** comes from the operating context: the quality floor in
`defaults.md`, plus the categories that applicable policy adds (policy.md R4). When the context is
unknown, use the production set. Ask one question per required category that the draft doesn't
already cover, then **always** one open question: "Any other quality need (usability,
maintainability, other)?"

| Category | Example options |
|---|---|
| constraint | mandated platform; required integration; data residency; none |
| security | sign-in required; role-based access; audit trail; none beyond the platform |
| privacy | personal data limited to its owner and staff; data retention limit; none |
| reliability | availability target (e.g. 99.5%); recovery time; best effort |
| observability | error alerting; usage dashboard; logs only |
| compliance | named regulation (e.g. GDPR, HIPAA, SOC 2); internal policy only; none |
| performance | response time target; throughput target; no target yet |
| accessibility | WCAG 2.2 AA; WCAG 2.2 A; no target yet |

Each answer becomes one NFR with that `category`, stated measurably where possible. Every required
category the user does not answer becomes, in section 12:

`[NEEDS CLARIFICATION: <category> requirements for <context>]`

Here `<context>` is the operating context, or `production` when it is unknown. For example:
`[NEEDS CLARIFICATION: accessibility requirements for production]`. Never write a placeholder NFR
for an unanswered category.

## Round 5: success metrics

For each drafted metric: baseline today, and target (with a time frame). Options may suggest values
from the BRN's evidence. Unanswered baselines or targets stay `[NEEDS CLARIFICATION: …]`.

## Depth by stage

| Stage | Requirements | Also ask |
|---|---|---|
| prototype | Capability level only: one requirement per promoted idea | Minimal rollout: who tries it, and how it is thrown away or kept |
| mvp | Confirm each current-release requirement (round 3 for every one) | Launch criteria and fallback |
| evolution | As mvp | Effects on existing behaviour and systems: what changes for current users, data migration, compatibility |
| unknown | As mvp | — |

## Recording answers

- Write only what the user answered or confirmed. An unanswered question leaves its field `null` or
  its gap marked.
- An answer that settles something drafted earlier replaces the draft; an answer that contradicts
  the BRN is recorded as the user said it, with a note in the item's `notes` (FRs) or in prose.
- If the user stops partway, ask whether to save a draft PRD with every undecided field `null`.
