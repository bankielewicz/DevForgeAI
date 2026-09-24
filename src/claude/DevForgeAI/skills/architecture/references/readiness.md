# Architectural questions and readiness

## Contents

- When to use this
- Identify the questions
- Resolve a question
- What never resolves a question
- The readiness rule
- Check the resolvers
- Readiness report

## When to use this

Read this before identifying questions (step 6), when resolving them (step 7) and when computing
readiness (steps 4 and 11). The readiness rule here is the contract the epic workflow consumes.

## Identify the questions

A question belongs in the ARCH only if **separate epics must share its answer**. Consider:

- component boundaries and responsibilities;
- data ownership (which component is the owner of which data);
- major interactions and interfaces between components and with external systems;
- deployment (units, environments, what runs where);
- how each quality requirement (NFR) is met, for example how sessions are revoked or how availability is reached.

Rules:

1. **Every `[NEEDS ADR: <decision>; affects FR-NNN, …]` marker in the PRD becomes one DEC.** Its `question`
   restates the decision. Its `upstream` cites every requirement the marker names.
2. Each DEC's `upstream` cites **every** affected requirement (FR or NFR), at the PRD version examined,
   with `relation: informed_by`. A question about how an NFR is met cites that NFR and every FR it applies to.
3. `blocking: true` unless the user said this question doesn't block epics.
4. One question per DEC. "Which identity provider?" and "How are sessions revoked?" are two questions,
   even when both concern sign-in, because one can be answered without the other.
5. **Leave feature-level detail to specs:** exact API fields, database columns, migrations, class
   structures, error messages, UI layouts. If a question only one epic needs answered, it isn't a DEC.
6. **Never turn a product question into an architectural one.** A `null` priority or release, or a
   `[NEEDS CLARIFICATION]` marker in the PRD, stays the PRD owner's question. Don't answer it here.
7. When amending, keep existing DECs and add new ones with the next free number. Never renumber.

## Resolve a question

A DEC becomes `state: resolved` only by one of these three means. Each resolver resolves **only the
question it answers**.

| Means | Condition | `resolved_by` | Who decides |
|---|---|---|---|
| 1. Mandated platform | An approved, active `architecture.mandated_platforms` setting, effective after policy R2, whose capability answers exactly this question | `POL-NNN#SET-NN` | Policy. Applied without asking, and never presented as the user's decision |
| 2. Existing ADR | An ADR with `status: accepted` and `superseded_by: null` that the user confirms answers exactly this question | `ADR-NNN` | The user confirms |
| 3. The user's decision | The user chooses among options you presented with their trade-offs | the new ADR, `status: accepted` | The user decides |

- **A mandated platform answers one question only: which platform provides the named capability.** It
  doesn't answer how the platform is used or configured, how sessions are revoked, which data it
  holds, or how any quality requirement is met. For example, "identity and authentication: Org A Identity
  Platform" resolves "Which identity provider do we use?" and leaves "How are sessions revoked?" open.
- **Means 2 needs the user's confirmation, every time.** Show the ADR's title and decision, and ask whether
  it answers this exact question. An ADR that cites the same requirement usually answers a different question.
- **Means 3:** for each question, present two to four options, each with its trade-offs against the
  quality drivers, and a recommendation if you have one. Only an explicit choice counts. Then write a new
  ADR from `${CLAUDE_SKILL_DIR}/assets/adr.md` with `status: accepted`, `approved_by` the user's name and
  `approved_on` today, and put its ID in that DEC's `resolved_by`, and in no other DEC's.
- **Deferring:** if the user wants the options recorded but not decided, you may write an ADR with
  `status: proposed`. It resolves nothing, and the DEC stays open.
- Anything else leaves the DEC `state: open` with `resolved_by: []`.

## What never resolves a question

- Confirming the outcome (reuse, amend or create). It accepts no decision inside the ARCH.
- "Proceed", "go ahead", "use your judgment", or a run with no user present.
- An accepted ADR that cites the same requirement but answers a different question.
- A proposed, rejected, deprecated or superseded ADR, including an ADR's successor when that successor
  answers a different question.
- A policy document that isn't approved, a deprecated setting, or a mandate for a different capability.
- Evidence of any classification (`references/inspection.md`): observed practice, or context such as the PRD.
- A request to reuse an existing system that wasn't inspected, such as "reuse our current auth service"
  with no inspection scope. No options were presented with trade-offs, so it isn't means 3. Record the
  missing evidence as a `[NEEDS CLARIFICATION: …]` marker, and keep the question open.
- Your own recommendation, however clear.

## The readiness rule

A requirement R is **ready** for epic work when, for **every** active DEC with `blocking: true` whose
`upstream` cites R:

- `state` is `resolved`, and
- every `resolved_by` entry is either an ADR with `status: accepted` and `superseded_by: null`, or an
  approved policy's active setting that is effective after this run's R2.

Otherwise R is **blocked**, and the report names the DEC IDs blocking it. A requirement cited by no
blocking DEC is ready. Readiness is architectural only: the PRD's `priority` and `release` still decide
which ready requirements get epics.

## Check the resolvers

Check every `resolved_by` entry now, when writing, not as recorded earlier:

1. **ADR:** read `docs/specs/adr/<ADR-ID>.md`. It must exist, with `status: accepted` and
   `superseded_by: null`. If it is superseded, the question is **open again**. Its successor doesn't
   inherit the resolution: the successor resolves the question only by means 2, with the user's confirmation.
   That applies only to a successor that existed before this run. An ADR written in this run from the user's
   explicit decision resolves its DEC by means 3, with no second confirmation (`output-rules.md`, Amending an
   ARCH).
2. **Policy setting:** it must be in an approved policy document, `status: active`, and effective after
   R2. Otherwise the question is open again.
3. If an entry fails, the DEC is open. When amending, change it to `state: open`, `resolved_by: []`, and
   log the transition in the Change Log, naming the failed resolver and why, for example
   `DEC-01 resolved → open: ADR-002 superseded by ADR-003`. Change nothing else in the DEC. In a new ARCH,
   write the DEC open and put the reason in its `notes`.

## Readiness report

For the handoff (and for the reuse or amend proposal, when an ARCH exists), build the mapping first: for each
active FR and NFR, the active blocking DECs whose own `upstream` cites it, and which of those are open. A
requirement is blocked by exactly those open DECs; a DEC never blocks a requirement it doesn't cite. Then report:

- **Ready:** every active FR and NFR of the PRD that the rule reports ready.
- **Blocked:** every other active FR and NFR, each with the open DEC IDs blocking it, for example
  `FR-001: blocked by DEC-01, DEC-02`.
- For every DEC reopened because its resolver failed, name the resolver and the reason, for example
  `DEC-01 is open: ADR-002 was superseded by ADR-003, which answers a different question`.
- Every active FR and NFR appears exactly once. A summary sentence must agree with the lists: never "nothing
  is ready" while a requirement is ready.
