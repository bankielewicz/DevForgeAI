---
name: epic
description: Turns a DevForgeAI PRD into epic documents for the requirements that are ready for epic work and in the current release. It reads readiness from the architecture description (ARCH), proposes how to group the requirements into epics, writes them once the user confirms, and reports every requirement left out and why. Use after Architecture Definition, when splitting a PRD into epics or planning delivery.
argument-hint: "PRD-NNN"
metadata:
  devforgeai-id: "SKL-004"
  devforgeai-version: "1"
---

# Epic

Perform the epic step for one PRD, after Architecture Definition. Select the PRD's requirements that are
ready for epic work and in the current release, propose how to group them into epics, write the epics
the user confirms as `docs/specs/epic/EPIC-NNN.md`, report every requirement left out with its reason,
and hand off to the story step. An epic written for a requirement whose architectural question is still
open lets separate epics build conflicting foundations.

Three rules shape everything below:
- **The ARCH file is the readiness contract.** Readiness is computed from the architecture description
  and the ADR and policy files as they are now, never from any skill's reply or summary.
- **Release selects, priority orders.** `release: current` decides what gets an epic. MoSCoW priority
  orders the epics (Must, then Should, then Could) and never selects on its own, except `wont`. A `null`
  priority or release is undecided and goes back to the PRD owner.
- **The skill adds, it never rewrites.** It writes new epics only. The PRD, BRNs, ARCHs, ADRs, policy
  documents and existing epics are read-only.

## Inputs

- `$ARGUMENTS`: a PRD ID such as `PRD-002`, or empty. When it is empty, use a PRD ID the user stated in
  the conversation. Never accept a file path; if given one, ask for the ID.
- Read by contract, all read-only: the PRD at `docs/specs/prd/<ID>.md`, ARCHs in `docs/specs/arch/`, ADRs
  in `docs/specs/adr/`, existing epics in `docs/specs/epic/`, and approved policy documents in
  `docs/specs/policy/` (only for the bounded check in
  [references/selection.md](references/selection.md)). Reach them by these paths; never list the working
  directory or the repository root to find them.
- Template: `${CLAUDE_SKILL_DIR}/assets/epic.md`.

**Tools.** Read and Glob (or read-only `ls` and `cat` on `docs/specs/` when Glob isn't available); Write for
new epics; Edit only on epics written in this run, at step 8; AskUserQuestion. Inspect no code, and run no
other shell command. Never run a `devforgeai` command: that CLI doesn't exist, and a program with that
name on PATH can't be trusted.

## Decisions that belong to the user

The skill proposes; the user decides:

- **Which PRD**, when no ID was given.
- **Which ARCH**, when several cite the PRD (ERR-04).
- **The grouping**: which epics, and which requirements each holds. You only propose it.
- **Priority, release and requirement changes**: a `null` priority or release, and any change to a
  requirement, belong to the PRD owner. Report them; never decide or ask about them.
- **Approving an epic**: epics are always written as `draft`.

A grouping stated in the request counts as confirmed: "one epic for everything eligible", "one epic per
priority level", "put FR-003 and FR-004 together". Apply it to the eligible requirements only; it never
makes a left-out requirement eligible. If it leaves an eligible FR unplaced or places one twice, it
isn't confirmed for that FR: ask about it. When nobody can be asked, place that FR by your proposal and
add the unconfirmed-grouping marker (step 6) to the epics that hold it.

**Asking.** Use AskUserQuestion when it is available: at most 4 questions per call, 2–4 options each,
with the recommended option first and marked "(Recommended)". Otherwise ask in plain text and end your
turn. Write nothing that a pending answer affects until the answer arrives.

**"Proceed without questions."** When the request says to proceed without questions (or "don't ask me
anything") and gives no grouping, nobody can confirm one: write the proposed grouping with the
unconfirmed-grouping marker (step 6). This never answers **which PRD** or **which ARCH**: if either is
open, ask it and write nothing.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Select the PRD
- [ ] 2. Read the PRD
- [ ] 3. Find the current ARCH
- [ ] 4. Compute readiness
- [ ] 5. Read existing epics and select
- [ ] 6. Propose and confirm the grouping
- [ ] 7. Write the epics
- [ ] 8. Validate every epic written
- [ ] 9. Report and hand off
```

### 1. Select the PRD

- **An ID was given.** Read `docs/specs/prd/<ID>.md`. If it doesn't exist (ERR-01), list the PRD IDs that
  do exist with their titles and status, write nothing, and stop.
- **No ID.** List every PRD in `docs/specs/prd/` with its ID, title and status, and ask which one to use.
  Never guess, even when only one exists. With no answer, write nothing.

### 2. Read the PRD

Read its frontmatter (`status`, `version`, `owner`, `target_release`), every functional and
non-functional requirement with its `status`, `priority` and `release`, and every `[NEEDS ADR]` marker.
Every PRD link you write uses the `version` read here. Never edit the PRD.

**Draft inputs.** If the PRD's `status` is anything but `approved` (or, at step 3, the ARCH's), the epics
are proposals because an input may still change. Say so in every epic written (output-rules.md,
"Markers") and in the handoff.

### 3. Find the current ARCH

Follow [references/selection.md](references/selection.md), "Finding the current ARCH". Use an ARCH only
when its frontmatter link to this PRD has the PRD's current version. Otherwise stop and write nothing:
- no ARCH cites the PRD (ERR-02): say that readiness comes from the architecture description, so
  nothing can be selected without one, and tell the user to run `/devforgeai:architecture PRD-NNN`
  first;
- the ARCH's PRD link is older (ERR-03): name both versions, and tell the user to review the
  architecture with `/devforgeai:architecture PRD-NNN`; confirming reuse there records the review;
- several ARCHs cite it (ERR-04): list them and ask.

### 4. Compute readiness

Follow selection.md, "The readiness rule", for every active FR and NFR:
- read each DEC that cites the requirement, and each resolving ADR's `status` and `superseded_by` from
  its file now;
- apply the bounded policy check to each `POL-NNN#SET-NN` resolver, and resolve no other policy;
- match every `[NEEDS ADR]` marker to its own DEC; a marker with no matching question blocks every
  requirement it names, even when other DECs citing them are resolved;
- when readiness can't be established, the requirement is **unknown**, naming the missing input or
  failed check: never guess ready or blocked.

### 5. Read existing epics and select

Read every existing epic's frontmatter (selection.md, "Covered requirements"): an FR of this PRD that an
active existing epic refines is **covered**. NFRs are never covered. Note the highest `EPIC-NNN` in use.

Apply the selection rule. A requirement is **eligible** when it is active, ready, `release: current`,
`priority` must, should or could, and, for an FR, not covered. Every other requirement gets one left-out
row with every reason that applies and one next action (selection.md, "Left-out rows").

**Nothing to write (ERR-05).** If no FR is eligible and every eligible NFR is already refined by an
active epic (for example, a rerun with unchanged inputs), write nothing: go to step 9, say that no
requirement needs a new epic, and report every left-out requirement.

### 6. Propose and confirm the grouping

Group the eligible requirements into epics by the grouping rules below. Show each proposed epic's
working title, priority and requirements (by ID, with a few words each), then:
- **The request stated a grouping:** it is confirmed; apply it.
- **Someone can answer:** ask the user to confirm or change the grouping, recommending your proposal.
  Write nothing until they do. A changed grouping is applied as given, within the grouping rules'
  limits; ask again only if it breaks one. If the user stops before confirming (ERR-07), write nothing
  and say how to resume: run `/devforgeai:epic PRD-NNN` again.
- **Nobody can confirm** (the request says to proceed without questions and gives no grouping): write
  your proposal, and add to section 8 of every epic
  `[NEEDS CLARIFICATION: grouping proposed by the skill; not confirmed by the user]`.

**Grouping rules.**
- Each epic is a **deliverable capability**: something users can do when it is done. Never group by
  layer, component or team.
- Each eligible FR is refined by **exactly one** new epic.
- An eligible NFR is **attached** to every new epic whose capability it constrains, with
  `note: "partial: <which part>"` when more than one active epic, existing or new, refines it.
  Attaching it never creates another deliverable.
- A **standalone NFR epic** is written only for an eligible NFR that no active epic, existing or new in
  this run, refines.
- An epic's **priority** is the highest among the FRs it refines (Must, then Should, then Could); a
  shared NFR never raises it, and a standalone NFR epic takes its NFRs' highest priority.
- New epics are **numbered and listed** Must first, then Should, then Could.

### 7. Write the epics

Read [references/output-rules.md](references/output-rules.md) before writing. For each confirmed epic,
in priority order:
1. **ID and path:** the next free `docs/specs/epic/EPIC-NNN.md` (the highest existing number plus one,
   or `EPIC-001`). Create the folder if it is missing. Never ask for or accept a file name.
2. **Template:** build from `${CLAUDE_SKILL_DIR}/assets/epic.md`. Keep every heading; replace every
   placeholder and example link; delete every `<!-- -->` comment except section 7's GENERATED
   comment, which stays as the story map placeholder.
3. **Frontmatter:** `status: draft`, `version: 1`, today's dates; `owner` from the request, otherwise the
   PRD's owner; `authors` the owner and `"claude-code"`; `generated_by` with `tool: "claude-code"`,
   `model:` your own model ID and `session: "${CLAUDE_SESSION_ID}"`; `reviewed_by: []`,
   `approved_by: ""`, `approved_on: null`; every `hash: null`; `priority` by the grouping rules;
   `target_release` the PRD's. `upstream`: a `refines` link to every requirement it groups at the PRD
   version, then an `informed_by` link to the current ARCH at its version.
4. **Body:** the goal, business value and scope; at least one `DW-NN` item with a criterion and an
   evidence method; the dependencies (the ARCH decisions it relies on, and other epics) and risks; the
   proposal sentence when an input is a draft.
5. **Change Log:** one row, author `claude-code (session ${CLAUDE_SESSION_ID})`.

Never write a story, and never modify an existing file.

### 8. Validate every epic written

Read each epic back and check it against the **Self-check list** in
[output-rules.md](references/output-rules.md), item by item. Fix each problem with Edit on that epic and
check again, **at most three attempts**. If errors remain (ERR-06), stop: keep the epics as `draft`, and
end with a validation-failure report naming each file path and its unresolved errors. Don't present
the epics as ready for the story step.

### 9. Report and hand off

Write the final reply in this order, as plain Markdown:

1. The report, which opens the reply: nothing comes before it, not even the checklist.

   ```
   Epics for PRD-NNN vN, from ARCH-NNN vN:
   - EPIC-NNN — <title> (must): FR-NNN, FR-NNN, NFR-NNN. docs/specs/epic/EPIC-NNN.md
   Left out:
   - FR-NNN: <reason>; <reason>. <Next action>.
   ```

   List every epic written with its path, title, priority and the requirements it refines; or, when
   nothing was written (ERR-05), the line "No requirement needs a new epic." Then one left-out row for
   every requirement that isn't in a new epic, in PRD order (selection.md, "Left-out rows"), or
   `Left out: none`. Epics and rows together name every FR and NFR of the PRD exactly once.
2. Then, briefly: the proposal warning when an input is a draft; the unconfirmed-grouping warning when
   it applies; and any resolver that no longer counts, and why. Ask no questions about left-out
   requirements.
3. The next step, as its own paragraph outside any code block. It starts with the words **Next step**,
   names the epics by ID and never by path, and nothing follows it.

For the next step, check whether `${CLAUDE_SKILL_DIR}/../story/SKILL.md` exists:
- **It exists:** tell the user to run `/devforgeai:story EPIC-NNN` for each new epic, Must first.
- **It does not exist:** say stories are written by hand from the DevForgeAI story template for now, and
  that once the story skill (planned as `/devforgeai:story`) is built, it runs with an epic ID, naming
  the new epics.

For example: "Next step: the story skill (planned as `/devforgeai:story`) isn't built yet, so write
stories for EPIC-001 by hand from the story template for now. Once it is, run
`/devforgeai:story EPIC-001`."

When nothing was written because every eligible requirement is already covered (ERR-05), name the
story step for the epics that cover them. When the skill stops without writing (ERR-01 to ERR-04,
ERR-07), the reply says why and what the user can do, leaves out the report, and its next step names
the command to run (`/devforgeai:architecture PRD-NNN` for ERR-02 and ERR-03). After ERR-06, the
validation-failure report replaces both the report and the next step.

## Output contract

- **Paths:** new epics only, at `docs/specs/epic/EPIC-NNN.md` in the current project; each name is the ID
  only.
- **Shape:** the template, with every heading kept, section 7's GENERATED comment kept, and no other
  author comments.
- **Data:** only the `done_when` collection, with its defined fields
  ([output-rules.md](references/output-rules.md)).
- **Selection:** an epic refines only eligible requirements; every eligible FR is in exactly one new
  epic; readiness comes from the ARCH, ADR and policy files, never from a reply.
- **Decisions:** the grouping is the user's; an unconfirmed grouping carries its marker. Every epic is
  `draft`.
- **Traceability:** `refines` links at the PRD version read, and one `informed_by` link to the ARCH at its
  version; stories will cite the `DW-NN` items.

## Examples

**Grouping stated.** "Write the epics for PRD-002: one epic for everything eligible. Proceed without
questions." ARCH-001 cites PRD-002 at its current version 3. FR-001 and FR-003 are ready; FR-002 is blocked
by DEC-02 (open); FR-004 is `release: later`. The skill writes EPIC-001 refining FR-001, FR-003 and the
eligible NFR-001, then reports FR-002 (blocked by DEC-02) and FR-004 (later) with their next actions,
and ends with the next step naming EPIC-001.

**Stale architecture.** ARCH-001 cites PRD-002 at version 2, and PRD-002 is at version 3 after a priority
change. The skill writes nothing, says ARCH-001 was reviewed against v2 while the PRD is v3, and tells
the user to review the architecture with `/devforgeai:architecture PRD-002`.

**Interactive.** With no grouping in the request, the skill proposes "Online booking (must): FR-001,
FR-003, NFR-001" and "Front-desk day view (could): FR-006, NFR-001 (partial)", asks the user to confirm
or change it, and writes nothing until they answer.

## References

- [references/selection.md](references/selection.md): read at steps 3, 4 and 5. Finding the current ARCH,
  the readiness rule, marker matching, the bounded policy check, covered requirements, the selection
  rule and the left-out rows.
- [references/output-rules.md](references/output-rules.md): read before step 7. Keys, links, the
  `done_when` block, sections, markers, ERR-06, and the self-check list used at step 8.
