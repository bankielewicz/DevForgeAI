---
name: epic
description: Turns a DevForgeAI PRD into epic documents for the requirements that are ready for epic work and in the current release. It reads readiness from the architecture description (ARCH), proposes how to group the requirements into epics, writes them once the user confirms, and reports every requirement left out and why. Use after Architecture Definition, when splitting a PRD into epics or planning delivery.
argument-hint: "PRD-NNN"
metadata:
  devforgeai-id: "SKL-004"
  devforgeai-version: "2"
---

# Epic

Turn one PRD (`docs/specs/prd/PRD-NNN.md`) into epics, `docs/specs/epic/EPIC-NNN.md`, for the requirements
that are **ready** for epic work and in the **current release**. Readiness comes from the architecture
description (ARCH) file, never from any skill's reply. Release selects the work and MoSCoW priority orders it.
Report every requirement you leave out, with its reason. You propose the grouping; the user confirms it. You
add new epics only: the PRD, the ARCH, ADRs, policy and existing epics are never edited.

## Inputs

- `$ARGUMENTS`: a PRD ID such as `PRD-001`, or empty. Never a file path.
- `docs/specs/prd/PRD-*.md`: PRDs. `docs/specs/arch/ARCH-*.md`: architecture descriptions.
- `docs/specs/adr/ADR-*.md`: the ADRs that resolve questions. `docs/specs/epic/EPIC-*.md`: existing epics.
- `docs/specs/policy/POL-*.md`: read only for the bounded policy-resolver check.
- `${CLAUDE_SKILL_DIR}/assets/epic.md`: the epic template.
- `${CLAUDE_SKILL_DIR}/references/`: `selection.md`, `output-rules.md`.

Every input is read-only. Use Read, and Glob when it is available. Without Glob, list only these exact folders
with `ls docs/specs/prd/ docs/specs/arch/ docs/specs/adr/ docs/specs/epic/ docs/specs/policy/` and read files
with Read or `cat`. Never list or read the project root, code, or anything outside `docs/specs/`, apart from
this skill's own files and the story skill check in step 9. Run no other command.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Select the PRD
- [ ] 2. Read the PRD
- [ ] 3. Find the current ARCH
- [ ] 4. Compute readiness
- [ ] 5. Select the requirements
- [ ] 6. Propose and confirm the grouping
- [ ] 7. Write the epics
- [ ] 8. Validate
- [ ] 9. Report and hand off
```

**Interactive or not.** The run is *non-interactive* when the request says to proceed without questions, or
when no one can answer (for example, an automated run). **Gating questions are never skipped**, even
non-interactively: which PRD (step 1) and which ARCH when several cite the PRD (step 3). For a gate, first
write everything the user needs to decide in your reply (the list and your reasons), then ask with
AskUserQuestion (at most 4 questions per call), or in plain text if it is unavailable, and **end your turn**. Write nothing until it is
answered. A gate counts as answered only when the request answers that exact question. The grouping (step 6)
is not a gate. Never ask about a left-out requirement.

### 1. Select the PRD

1. If `$ARGUMENTS` (or, when it is empty, the request) names a PRD ID, read `docs/specs/prd/<ID>.md`. If it
   doesn't exist, say so, list the PRDs that exist with their IDs, titles and status, and stop. Write
   nothing (ERR-01).
2. If `$ARGUMENTS` is a path or anything else, say that only a PRD ID is accepted, list the PRDs, and stop.
3. If it is empty, list every PRD with its ID, title and status, ask which to use, and end your turn. Ask even
   when only one exists. If there are none, say a PRD must be written first with `/devforgeai:prd`, and stop.

### 2. Read the PRD

1. Read its `version`, `status`, `owner` and `target_release`; every functional and non-functional requirement
   with its `id`, `status`, `priority`, `release` and statement; its success metrics; and every
   `[NEEDS ADR: …]` marker (section 12 and anywhere else). Every link to the PRD carries its `version`.
2. If `status` is `draft`, write this line right away, and repeat it in the handoff and in every epic written
   (`output-rules.md`, The proposal line): "PRD-NNN is a draft, so the epics are proposals until it is approved."
3. Never edit the PRD.

### 3. Find the current ARCH

Read `${CLAUDE_SKILL_DIR}/references/selection.md` and follow Find the current ARCH:
- **no ARCH cites the PRD:** write nothing and hand back to `/devforgeai:architecture PRD-NNN` (ERR-02);
- **several cite it:** list them with their systems and PRD link versions, ask, and end your turn (ERR-04);
- **its PRD link is older than the PRD's `version`:** write nothing, name both versions, and ask for a review of
  the architecture with `/devforgeai:architecture PRD-NNN` (ERR-03);
- **its PRD link equals the PRD's `version`:** it is current; use it. If its `status` is `draft`, give the
  proposal warning as in step 2, naming the ARCH.

### 4. Compute readiness

Follow `selection.md` (Readiness, Check each resolver, Match the NEEDS ADR markers). For every active FR and
NFR: take the active blocking DECs whose own `upstream` cites it, check every resolver by reading its ADR file
now (and, for a `POL-NNN#SET-NN` resolver, the bounded policy check), and match every marker to its own DEC.
A DEC blocks only what it cites. A missing ADR file or a failed policy check makes the requirement
**unknown**, never ready or blocked by assumption. Then write **the readiness table** into your reply, one row
per active FR and NFR. The selection and every left-out row must agree with it.

### 5. Select the requirements

1. Read every existing epic in `docs/specs/epic/`: its `status` and its `refines` links. Never modify,
   renumber or duplicate one.
2. Apply `selection.md` (The selection rule). **Eligible:** active, ready, `release: current`, `priority`
   `must`, `should` or `could`, and, for an FR, not covered by an active existing epic. NFRs are never covered.
3. Build one left-out row for every other requirement (`selection.md`, Left-out rows): every reason that
   applies, in order and named by its word from the table (deprecated, won't have, later, undecided, covered,
   blocked, unknown), and one next action, the first listed reason's. Several reasons never mean several questions.
4. **Nothing to write (ERR-05):** if there is no eligible FR, and every eligible NFR is already refined by an
   active existing epic, write nothing. Say that no requirement needs a new epic, report every left-out row,
   and stop.

### 6. Propose and confirm the grouping

1. Propose epics as `selection.md` (Grouping) says:
   - each epic is a deliverable capability;
   - each eligible FR is in exactly one new epic;
   - an eligible NFR is attached to every new epic whose capability it constrains;
   - a standalone NFR epic only for an eligible NFR that no active epic, existing or new, refines.
   Give each epic its priority and number (Priority and numbering). Show each proposed epic with its title,
   priority and requirements, in number order.
2. **A grouping stated in the request is confirmed.** Follow it exactly, for example "one epic for everything
   eligible" or "one epic per priority level, with NFR-003 only in the Must epic". Never add a left-out or
   covered requirement to satisfy it; say so instead.
3. **Interactive, with no grouping stated:** ask the user to confirm or change the grouping, and end your turn.
   Write nothing until they do. If they change it, write the epics their way. If they stop before confirming,
   write nothing, and say how to resume: run `/devforgeai:epic PRD-NNN` again (ERR-07).
4. **Non-interactive, with no grouping stated:** no one can confirm. Write your proposal, and put this marker
   in section 8 of each epic: `[NEEDS CLARIFICATION: grouping proposed by the skill; not confirmed by the user]`.

### 7. Write the epics

1. Read `${CLAUDE_SKILL_DIR}/references/output-rules.md` if you haven't already.
2. Write each epic to the next free `docs/specs/epic/EPIC-NNN.md` (the highest existing number plus one),
   numbered Must first, then Should, then Could. Write creates `docs/specs/epic/` if it is missing. If a target
   path exists, stop and ask; never overwrite. Never ask for or accept a file name.
3. Build each file from `${CLAUDE_SKILL_DIR}/assets/epic.md`: keep every heading, fill every section, and
   delete every author comment and the template's example links and marker, keeping only the story map's
   GENERATED comment.
4. Frontmatter:
   - `status: draft`;
   - `priority`: the highest among the FRs it refines (a shared NFR never raises it; an NFR-only epic takes
     its NFRs' highest priority);
   - `target_release`: the PRD's `target_release`;
   - `upstream`: a `refines` link to every requirement it groups, at the PRD's version (with
     `note: "partial: <which part>"` for a shared NFR), and an `informed_by` link to the ARCH at the ARCH's version.
5. Fill the goal, value and scope, at least one done-when item (`DW-01`) with a criterion and an evidence method,
   and the dependencies. Keep the story map as the GENERATED placeholder.
6. Provenance: `generated_by.tool` `claude-code`, `generated_by.model` your current model ID,
   `generated_by.session` `${CLAUDE_SESSION_ID}`; `authors` the user's name (if known) and `claude-code`;
   `reviewed_by: []`; every `hash: null`; `created` and `updated` today; `approved_by: ""` and
   `approved_on: null`. Never invent a name.
7. Never modify a PRD, BRN, ARCH, ADR, policy document or existing epic.

### 8. Validate

1. Read each epic written back and check it against the **Self-check list** in `output-rules.md`. Don't call
   any `devforgeai` command.
2. Fix every problem with Edit, only in epics written in this run, then check again. **Stop after three
   attempts.**
3. If errors remain after the third attempt (ERR-06), stop fixing. Keep the epics as written, with
   `status: draft`, and end with a **validation-failure report**: each file path and each unresolved error.
   Don't present the epics as ready for the story step, and skip the handoff in step 9.

### 9. Report and hand off

1. **Epics written:** for each, its path, title, priority and the requirements it refines, in number order.
   Say when the grouping is unconfirmed.
2. **Left out:** every left-out row from step 5, one line per requirement, each with every reason that applies
   and one next action. Ask nothing about them.
3. The proposal warning, if the PRD or the ARCH is a draft.
4. **Next step: the story step**, with the new epic IDs as its input. Check with Read whether
   `${CLAUDE_PLUGIN_ROOT}/skills/story/SKILL.md` exists:
   - if it does, tell the user to run `/devforgeai:story <EPIC-ID>` for each new epic;
   - if it doesn't, say that the story step is next for those epics, and that stories are written by hand from
     the story template for now, because the story skill isn't built yet.
5. Never write a story, and never start the story step.

## Decisions that need the user

Gates (asked even non-interactively, see Interactive or not) are marked *gate*.

- *gate* **Which PRD**, when no ID is given (step 1).
- *gate* **Which ARCH**, when several cite the PRD (step 3).
- **The grouping** (step 6). A grouping in the request counts as confirmed. With no one to confirm, write the
  proposal with the unconfirmed-grouping marker.
- **Any change to the PRD, the ARCH, an ADR or policy:** hand back to their owner or skill; never make it here.

You decide on your own: the readiness verdicts (from the files), which requirements are eligible, the epic
numbers, the proposed grouping, titles and wording, and the done-when items (the user may edit them).

## Output contract

- Path: `docs/specs/epic/EPIC-NNN.md`, the next free numbers, Must first, then Should, then Could. The
  capability is in `title`, not the file name.
- Content: the template `${CLAUDE_SKILL_DIR}/assets/epic.md`, filled in, every heading kept; valid against
  the epic schema as restated in `output-rules.md`.
- An epic refines only eligible requirements: active, ready under the ARCH, `release: current`, priority
  `must`, `should` or `could`, and for an FR not already covered. Each eligible FR is in exactly one new epic.
- Each epic links the ARCH it relied on (`informed_by`, at the ARCH's version) and starts as `draft`; only the
  user approves it.
- Stable `DW-NN` IDs and `refines` links: the story step cites them.
- Nothing is written without a current ARCH, and nothing when no requirement needs a new epic. Existing epics,
  the PRD, the ARCH, ADRs and policy are never modified.

## References

- [selection.md](references/selection.md): read in step 3, and used in steps 4 to 6.
- [output-rules.md](references/output-rules.md): read before writing (step 7) and when validating (step 8).
