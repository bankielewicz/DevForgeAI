# The current ARCH, readiness and selection

## Contents

- When to use this
- Finding the current ARCH
- The readiness rule
- Matching `[NEEDS ADR]` markers
- The bounded policy check
- Covered requirements
- The selection rule
- Left-out rows
- Worked example

## When to use this

Read this at SKILL.md step 3 (find the ARCH), step 4 (compute readiness) and step 5 (select). An epic
written for a requirement whose architectural question is still open lets two epics build conflicting
foundations, so readiness comes from the files, never from a skill's reply or a summary.

## Finding the current ARCH

Read the frontmatter of every `docs/specs/arch/ARCH-*.md`. An ARCH **cites this PRD** when its
frontmatter `upstream` has a link whose `id` is this PRD's ID (with no `item`). Links on items inside the
ARCH don't count.

| What you find | Result |
|---|---|
| No ARCH cites the PRD, or the folder doesn't exist | **ERR-02.** Write nothing. Readiness comes from the architecture description, so tell the user to run `/devforgeai:architecture PRD-NNN` first |
| One ARCH cites it, and that link's `version` equals the PRD's `version` | It is the **current ARCH**. Use it |
| One ARCH cites it, and that link's `version` is older than the PRD's `version` | **ERR-03.** Write nothing. Name both versions ("ARCH-001 was last reviewed against PRD-001 v1; the PRD is now v2") and tell the user to review the architecture against this PRD version with `/devforgeai:architecture PRD-NNN`. Confirming reuse there records the review; the architecture changes only if the review finds it must |
| Several ARCHs cite it | **ERR-04.** List each with its `system` and the version of its PRD link, and ask which one to use. Never pick one silently. With no one to answer, write nothing |

A version mismatch means a review is due, not that the architecture is wrong. Never treat an ARCH
reviewed against an older PRD version as current, and never treat "no ARCH" as "nothing blocks".

## The readiness rule

Apply it to every active FR and NFR of the PRD, from the current ARCH's `decisions` block and the ADR and
policy files as they are **now**. A requirement R is **ready** when, for every DEC with `status: active`
and `blocking: true` whose `upstream` cites R:
- `state` is `resolved`, and
- every `resolved_by` entry counts:
  - `ADR-NNN`: `docs/specs/adr/ADR-NNN.md` exists, and its frontmatter has `status: accepted` and
    `superseded_by: null`. Read the file; never trust what the ARCH, its evidence or its notes say
    about the ADR.
  - `POL-NNN#SET-NN`: it passes the bounded policy check below.

In addition, every `[NEEDS ADR]` marker that names R must have its own matching DEC (next section).

The outcome for R is one of:
- **ready**: every DEC that cites R passes, and every marker naming R is matched.
- **blocked**, naming each cause:
  - a DEC whose `state` is `open`: `DEC-01 (open)`;
  - a DEC resolved by an ADR that no longer counts: `DEC-03 (ADR-002 superseded by ADR-003)`, or
    `(ADR-007 is proposed)`, `(… rejected)`, `(… deprecated)`;
  - a marker with no matching DEC: `[NEEDS ADR] marker without a matching question ("<the marker's
    decision>")`.
- **unknown**, naming the input: readiness can't be established, so R is never asserted ready or blocked
  on that point. Causes: a resolving ADR's file is missing (`ADR-004 not found`) or unreadable, a
  `resolved_by` entry in no recognizable form, or a policy resolver that fails the bounded check
  (`POL-001#SET-01 fails the policy check: setting deprecated`).

A DEC blocks **only** the requirements its own `upstream` cites. A DEC with `blocking: false` or
`status: deprecated` blocks nothing. A requirement no DEC cites and no marker names is ready. If one DEC
blocks R and another is unknown, R has both reasons.

## Matching `[NEEDS ADR]` markers

Find every `[NEEDS ADR: <decision>; affects FR-NNN, …]` marker in the PRD. For each one, look for its
**matching DEC**: an active DEC whose `question` asks the marker's decision, and whose `upstream` cites
every requirement the marker names. "Which identity provider handles sign-in?" matches
`[NEEDS ADR: identity provider for sign-in; affects FR-001]`.

- A matching DEC is then judged like any other DEC: open, resolved by a resolver that counts, or not.
- **No DEC clearly asks the marker's decision:** every requirement the marker names is **blocked**
  ("marker without a matching question"), even when other DECs citing that requirement are resolved.
- A resolved DEC about a **different** decision never answers the marker, even when it cites the same
  requirement: an audit-storage DEC doesn't answer a payment-provider marker. When in doubt, treat the
  marker as unmatched; a wrong "ready" is worse than a wrong "blocked".

## The bounded policy check

A `POL-NNN#SET-NN` resolver counts only when all four hold. This is a check, not policy resolution: never
apply precedence rules, defaults or local preferences, and never resolve anything else from policy.

1. `docs/specs/policy/POL-NNN.md` exists and has `status: approved`.
2. Setting `SET-NN` in its `settings` block has `status: active`.
3. The policy document's `version` equals the `version` of the ARCH's link to that setting (a link with
   `id: POL-NNN` and `item: SET-NN`, usually on the component that provides the capability).
4. No other approved document in `docs/specs/policy/` has an active setting with the same `key`.

If any fails, R is **unknown**, naming the resolver and the condition that failed:
`POL-001#SET-01 fails the policy check: setting deprecated (check 2)`. The next action is to review the
architecture with `/devforgeai:architecture PRD-NNN`, which re-resolves policy.

## Covered requirements

Read the frontmatter of every `docs/specs/epic/EPIC-*.md`. An existing epic is **active** unless its
`status` is `superseded` or `deprecated`. An FR is **covered** when an active existing epic's frontmatter
`upstream` has a link with `relation: refines`, `id` equal to this PRD's ID and `item` equal to the FR's
ID, at any `version`.

- An FR of another PRD with the same number is not this FR: both the PRD ID and the item must match.
- **NFRs are never covered.** An eligible NFR is attached to every new epic it constrains, even when an
  existing epic already refines it (SKILL.md, "Grouping rules").
- A covered FR that is also blocked or unknown now gets both reasons: the existing epic's work rests on
  a question that is no longer settled.
- Existing epics are read-only: never modify, renumber, supersede or duplicate one.

## The selection rule

A requirement R of the PRD (an FR or an NFR) is **eligible** when all hold:
1. `status: active`;
2. R is ready;
3. `release: current`;
4. `priority` is `must`, `should` or `could`;
5. for an FR only: R is not covered.

Priority orders the epics and never selects on its own, apart from `wont`. A `null` priority or release
is undecided: it belongs to the PRD owner, never to you.

## Left-out rows

Every requirement that isn't eligible gets **one row** in the reply, with **every reason that applies**,
in this order, and **one next action: the first listed reason's**. Several reasons never mean several
questions, and a row never asks the user anything.

| Order | Reason, as written in the row | When | Next action |
|---|---|---|---|
| 1 | `deprecated` | `status` is not `active` | `No action.` |
| 2 | `won't have (priority wont)` | `priority: wont` | `No action for this release.` |
| 3 | `later (release later)` | `release: later` | `No action for the current release.` |
| 4 | `undecided (priority null)`, `(release null)` or `(priority and release null)` | `priority` or `release` is `null` | `The PRD owner decides.` |
| 5 | `covered by EPIC-NNN` | An active existing epic refines this FR | `No action.`, or when also blocked or unknown: `Review EPIC-NNN's work before continuing.` |
| 6 | `blocked by DEC-NN (<cause>)`, or `blocked: [NEEDS ADR] marker without a matching question ("<decision>")` | Not ready | `Resolve it with /devforgeai:architecture PRD-NNN.` |
| 7 | `unknown: <input and failed condition>` | Readiness can't be established | `Fix <the input>, or review the architecture with /devforgeai:architecture PRD-NNN, then run again.` |

Compute readiness for a requirement left out for another reason too (`later`, `wont`, `undecided`), and
list its blocking DECs: they tell the PRD owner what else waits. A deprecated requirement gets only
`deprecated`.

Row format, one line each, the requirement ID first:

```
- FR-005: later (release later); blocked by DEC-06 (open). No action for the current release.
- FR-008: covered by EPIC-002; blocked by DEC-03 (ADR-002 superseded by ADR-003). Review EPIC-002's work before continuing.
```

## Worked example

PRD-003 (version 4) has FR-001 to FR-006 and NFR-001, and
`[NEEDS ADR: calendar sync with the practice system; affects FR-002]`. ARCH-002 cites PRD-003 at version 4.
EPIC-004 (approved) refines FR-001.

| DEC | Question | Cites | State | Resolver now |
|---|---|---|---|---|
| DEC-01 | Which component owns appointment data? | FR-001, FR-002, NFR-001 | resolved | ADR-005, accepted |
| DEC-02 | How are SMS reminders sent? | FR-003 | resolved | ADR-006, superseded by ADR-009 |
| DEC-03 | Which video service hosts remote visits? | FR-004 | open | none |

FR-004 has `release: later`, FR-005 has `priority: null`, and FR-006 (`could`, `current`) has no DEC.
Every other requirement is `must`, `current`.

```
- FR-001: covered by EPIC-004. No action.
- FR-002: blocked: [NEEDS ADR] marker without a matching question ("calendar sync with the practice system"). Resolve it with /devforgeai:architecture PRD-003.
- FR-003: blocked by DEC-02 (ADR-006 superseded by ADR-009). Resolve it with /devforgeai:architecture PRD-003.
- FR-004: later (release later); blocked by DEC-03 (open). No action for the current release.
- FR-005: undecided (priority null). The PRD owner decides.
```

FR-002 is blocked although DEC-01, which cites it, is resolved: DEC-01 asks about data ownership, not
calendar sync. The eligible requirements are FR-006 and NFR-001; NFR-001 is never covered, although
EPIC-004 touches it.
