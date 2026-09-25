# The current ARCH, readiness and the selection rule

## Contents

- When to use this
- Find the current ARCH
- Readiness
- Check each resolver
- Match the NEEDS ADR markers
- The readiness table
- The selection rule
- Left-out rows
- Grouping
- Priority and numbering

## When to use this

Read this in steps 3 to 6. **The ARCH file is the readiness contract.** Compute readiness from the ARCH and
the ADR and policy files as they are now. Never take it from any skill's reply or handoff, from chat text, or
from a readiness summary in an ARCH's prose. Everything read here is read-only.

## Find the current ARCH

1. List `docs/specs/arch/ARCH-*.md` (with Glob, or `ls docs/specs/arch/`) and read each one's frontmatter.
2. An ARCH **cites the PRD** when its frontmatter `upstream` has a link whose `id` is this PRD's ID.
3. **None cites it (ERR-02):** write nothing. Say that readiness comes from the architecture description, and
   tell the user to run `/devforgeai:architecture PRD-NNN` first. Stop.
4. **Several cite it (ERR-04, a gate):** list each with its ID, title, `system`, `status` and the version of
   its PRD link, ask which to use, and end your turn. Never pick one silently.
5. **One cites it:** it is **current** when that link's `version` equals the PRD's `version`. Use it only then.
6. **Not current (ERR-03):** write nothing. Name both versions, for example "ARCH-004 was last reviewed
   against PRD-003 v2; PRD-003 is now v3." Tell the user to review the architecture against this PRD version
   with `/devforgeai:architecture PRD-NNN`: confirming reuse there records the review, and the architecture
   changes only if the review finds a change is needed. A version mismatch means a review is due, not that the
   architecture must change. Stop.
7. If the ARCH's `status` is `draft`, the epics are proposals (the proposal warning, SKILL.md step 2).

## Readiness

Compute readiness for **every active FR and NFR** of the PRD, whatever its priority or release. For a
requirement R:

1. **Its DECs.** Take every DEC in the ARCH with `status: active` and `blocking: true` whose **own
   `upstream`** has a link with this PRD's ID and `item: R`, at any version. A DEC blocks only the requirements
   its own `upstream` cites. Never infer a link from a DEC's question, from R's topic, or from another DEC.
2. **Each DEC's state.** A DEC with `state: open` is open. A DEC with `state: resolved` counts as resolved only
   if every entry in its `resolved_by` passes Check each resolver. An entry that fails makes the DEC open again.
   An entry that can't be checked makes R unknown.
3. **The markers.** Apply Match the NEEDS ADR markers.
4. **The verdict:**
   - **blocked** when any of R's DECs is open (or open again), or a marker naming R has no matching DEC;
   - **unknown** when readiness can't be established: a resolving ADR's file is missing or unreadable, a
     policy resolver fails the bounded check, or an input can't be read;
   - both can apply; report both;
   - **ready** only when neither applies. A requirement cited by no blocking DEC and named by no marker is ready.

Readiness is architectural only. The PRD's `priority` and `release` decide separately which ready
requirements get epics (The selection rule).

## Check each resolver

Check every `resolved_by` entry **now**, by reading the file, not from what the ARCH says about it.

**`ADR-NNN`:** read `docs/specs/adr/ADR-NNN.md`.
- The file doesn't exist or can't be read: R is **unknown**, "ADR-NNN not found".
- `status: accepted` and `superseded_by: null`: the entry passes.
- `status: superseded`, or `superseded_by` set: the entry fails. The DEC is open again and R is **blocked**,
  naming the resolver, for example "DEC-05 open again: ADR-012 superseded by ADR-015". The successor doesn't
  inherit the resolution, even when it is accepted.
- Any other status (`proposed`, `rejected`, `deprecated`): the entry fails; name the status.

**`POL-NNN#SET-NN`:** a bounded, read-only check. It is **not** policy resolution: don't apply R1 to R5,
don't read `.claude/devforgeai.local.md`, and write no resolution line. The entry passes only when all four hold:
1. `docs/specs/policy/POL-NNN.md` exists and has `status: approved`;
2. the setting `SET-NN` in its `settings` block has `status: active`;
3. the policy document's `version` equals the `version` of the ARCH's link to that setting (a link
   `{id: POL-NNN, item: SET-NN, …}` on a CMP, a DEC or the frontmatter). No such link fails this check;
4. no other approved document in `docs/specs/policy/` has an active setting with the same `key`.

If any fails, R is **unknown**, naming the resolver and the failed condition, for example "POL-002#SET-03:
setting deprecated" or "POL-002#SET-03: policy v4, ARCH links v3". The next action is to review the
architecture with `/devforgeai:architecture`, which re-resolves policy.

**Anything else** in `resolved_by`: R is unknown, naming the entry.

## Match the NEEDS ADR markers

Read every `[NEEDS ADR: <decision>; affects <IDs>]` marker in the PRD, in section 12 and anywhere else.
**Each marker needs its own matching DEC:** an active DEC whose `question` answers the marker's decision (the
same decision, not only the same requirement or a related topic) **and** whose `upstream` cites every
requirement the marker names.

- **A DEC matches:** it is one of those requirements' DECs anyway. Its state decides, as above.
- **No DEC clearly matches:** every requirement the marker names is **blocked** by "a marker without a matching
  question", even when every other DEC citing it is resolved. A resolved DEC about a different decision
  doesn't answer the marker. When in doubt, it doesn't match.
- One DEC answers one decision. It doesn't match two markers about different decisions.

## The readiness table

Before selecting anything, write the readiness table into your reply: one row for every active FR and NFR,
built from the files as above. It is how the user checks your reading, and the selection and the left-out rows
must agree with it. For example:

| Req | Priority / release | DECs citing it (state; resolver check) | Marker | Readiness |
|---|---|---|---|---|
| FR-021 | must / current | DEC-11 resolved by ADR-014: accepted | matched by DEC-11 | ready |
| FR-022 | should / current | DEC-12 resolved by ADR-015: superseded by ADR-019 | none | blocked (DEC-12) |
| FR-023 | must / current | none | "search provider": no matching DEC | blocked (marker) |
| FR-024 | must / later | DEC-13 open | none | blocked (DEC-13) |
| FR-025 | must / current | DEC-14 resolved by ADR-016: file not found | none | unknown (ADR-016 not found) |
| NFR-004 | could / current | DEC-11 resolved by ADR-014: accepted | none | ready |

## The selection rule

A requirement R of the PRD (an FR or an NFR) is **eligible** when all of these hold:

1. R has `status: active`;
2. R is ready;
3. `release: current`;
4. `priority` is `must`, `should` or `could`;
5. **for an FR only:** it isn't covered. An FR is **covered** when an active existing epic (one whose
   `status` isn't `superseded` or `deprecated`) has a `refines` link with this PRD's ID and `item:` that FR,
   at any version. Both the PRD ID and the item must match.

**NFRs are never covered.** An eligible NFR is attached to every new epic it constrains, even when an
existing epic already refines it (Grouping).

## Left-out rows

Every requirement that isn't eligible is **left out** and gets **one compact row** listing **every reason that
applies, in this order**, and **one next action: the first listed reason's**.

| # | Reason | When | Next action |
|---|---|---|---|
| 1 | `deprecated` | R is not active | none |
| 2 | `wont` | `priority: wont` | none for this release |
| 3 | `later` | `release: later` | none for the current release |
| 4 | `undecided` | `priority` or `release` is `null` | the PRD owner decides |
| 5 | `covered` | an active existing epic refines this PRD's FR; name the epic | none, unless it is also blocked: then review that epic's work before continuing |
| 6 | `blocked` | R is not ready: name the blocking DEC IDs, any superseded resolver, or the marker without a matching question | resolve it with `/devforgeai:architecture PRD-NNN` |
| 7 | `unknown` | readiness can't be established: name the missing or unreadable input, or the policy resolver and the failed check | fix that input, or review the architecture, then run again |

Write each row as one line: the requirement ID first, then each reason **named by its word from the table**
(`won't have` for `wont`), followed by its detail, then the next action. For example:

- `FR-031: later; DEC-17 open. No action for the current release.`
- `FR-032: won't have. No action for this release.`
- `FR-033: undecided (priority not set). The PRD owner decides.`
- `FR-034: covered by EPIC-006; now blocked by DEC-18 (ADR-021 superseded by ADR-024). Review EPIC-006's work before continuing.`
- `FR-035: blocked by DEC-19 (open). Resolve it with /devforgeai:architecture PRD-004.`
- `FR-036: blocked: the [NEEDS ADR: search provider] marker has no matching question. Resolve it with /devforgeai:architecture PRD-004.`
- `FR-037: unknown: ADR-026 (resolver of DEC-20) not found. Fix that input, or review the architecture, then run again.`
- `NFR-006: unknown: POL-002#SET-03 fails the policy check (setting deprecated). Review the architecture with /devforgeai:architecture PRD-004, then run again.`

Several reasons never mean several questions. Never ask about a left-out requirement.

## Grouping

- Each epic is a **deliverable capability**, named for what users can do when it is done.
- **Each eligible FR is refined by exactly one new epic.** Never put a covered or left-out requirement in one.
- **An eligible NFR is attached** to every new epic whose capability it constrains. When it is shared by
  several epics, or only part of it applies, its link carries `note: "partial: <which part>"`. Attaching it
  never creates a second deliverable.
- **A standalone NFR epic** is written only for an eligible NFR that no active epic, existing or new in this
  run, refines.
- **Nothing to write (ERR-05):** when there is no eligible FR, and every eligible NFR is already refined by an
  active existing epic, no new epic is needed. A rerun with unchanged inputs ends here.
- A grouping stated in the request is confirmed: follow it exactly, including where it says an NFR applies.

## Priority and numbering

- An epic's `priority` is the **highest priority among the FRs it refines** (must > should > could). An
  attached NFR never raises it. A standalone NFR epic takes its NFRs' highest priority.
- New epics take the next free numbers (the highest existing `EPIC-NNN` plus one, `EPIC-001` if none) and are
  numbered, and listed, **Must first, then Should, then Could**. Within one priority, keep the proposed order.
