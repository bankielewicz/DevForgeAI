---
name: architecture
description: Performs DevForgeAI Architecture Definition for a PRD. It identifies the architectural questions separate epics must share, settles each only by an explicit decision, an accepted ADR or approved policy, and writes an architecture description (ARCH) with ADRs and a report of which requirements are ready for epic work. Use after a PRD is written, when deciding system architecture, components, data ownership or deployment, or when resolving NEEDS ADR markers.
argument-hint: "PRD-NNN"
metadata:
  devforgeai-id: "SKL-003"
  devforgeai-version: "4"
---

# Architecture

Perform the Architecture Definition step for one PRD (`docs/specs/prd/PRD-NNN.md`). Identify the
architectural questions that separate epics must share, settle each one only by an approved policy
mandate, an accepted ADR the user confirms, or the user's explicit decision, and record the result in an
architecture description, `docs/specs/arch/ARCH-NNN.md`, plus ADRs. Then report exactly which requirements
are ready for epic work. You recommend; the user decides. The PRD is never edited.

## Inputs

- `$ARGUMENTS`: a PRD ID such as `PRD-001`, or empty. Never a file path.
- `docs/specs/prd/PRD-*.md`: PRDs (read-only, always).
- `docs/specs/policy/POL-*.md` and `.claude/devforgeai.local.md`: policy and local preferences (read-only).
- `docs/specs/adr/ADR-*.md`: existing ADRs. `docs/specs/arch/ARCH-*.md`: existing architecture descriptions.
- Code only inside the inspection scope the user names.
- `${CLAUDE_SKILL_DIR}/assets/arch.md` and `${CLAUDE_SKILL_DIR}/assets/adr.md`: the ARCH and ADR templates.
- `${CLAUDE_SKILL_DIR}/references/`: `policy.md`, `defaults.md`, `readiness.md`, `inspection.md`, `output-rules.md`.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Resolve policy (R1, R2)
- [ ] 2. Select the PRD
- [ ] 3. Read the PRD (R3, R4)
- [ ] 4. Select the ARCH
- [ ] 5. Inspect within scope
- [ ] 6. Identify the questions
- [ ] 7. Resolve the questions
- [ ] 8. Propose the outcome
- [ ] 9. Write the ARCH and ADRs (R5)
- [ ] 10. Validate
- [ ] 11. Report readiness and hand off
```

**Interactive or not.** The run is *non-interactive* when the request says to proceed without questions, or
when no one can answer (for example, an automated run). Then ask no decision, ADR-confirmation or outcome
question: every question without a policy mandate stays open, no ADR is written or accepted, and `outcome`
stays `null` unless the request itself explicitly confirms that outcome (for example "I confirm the amend outcome").
**Gating questions are never skipped**, even non-interactively: which PRD (step 2), which ARCH when several
could apply (step 4), reuse or amend when an ARCH already covers the system (step 4), and saving a draft
when the user stops, at any step. For a gating question, first write everything the user needs to decide in your reply
text (the list, the reasons, the current readiness), then ask with AskUserQuestion, or in plain text if it
is unavailable, and **end your turn**. Write no file and create no directory until it is answered. A gate
counts as answered only when the request answers that exact question (for example "amend ARCH-001").
"Proceed without questions" answers no gate. A missing inspection scope is not a gate (step 5).

**Reading `policy.md`.** It is shared unchanged with the prd skill, so read it with this mapping:

| policy.md says | For this skill |
|---|---|
| "before selecting a BRN" | before selecting the PRD |
| Stop message, second line | `No ARCH or ADR was written. Fix the policy document and run /devforgeai:architecture again.` |
| `interview.max_calls`, "interview budget" | the most AskUserQuestion calls for decisions and the outcome (steps 7 and 8). Gating questions don't count |
| R2: a mandate "applies to this PRD" | it resolves the question it answers (`readiness.md`, means 1) |
| R3: "from the request, then the BRN, then the first framing question" | from the request, then the PRD's `operating_context`. Never ask for it: it is the PRD owner's decision |
| R4: the floor and the quality round (`interview.md`) | not used here. Only evaluate which settings apply, and record them |
| R5: the mandate's link "on the constraint NFR" | on the CMP that provides the capability (`output-rules.md`, Links) |
| R5: settings that "govern how the PRD is produced" | the applied `interview.max_calls` and `quality.required_categories` settings, as ARCH frontmatter `informed_by` links |
| "PRD", "the Change Log row" (in R5 and Resolution line) | the ARCH, and the Change Log row this run adds to it |

### 1. Resolve policy (R1, R2)

1. Read `${CLAUDE_SKILL_DIR}/references/policy.md` and `${CLAUDE_SKILL_DIR}/references/defaults.md`.
2. Run R1: load `docs/specs/policy/POL-*.md`, skip and note draft or in-review documents, and validate every
   approved one against the schema and semantic rules. On a schema violation, an SV-01 to SV-04 violation or
   a disallowed override, reply with the **Stop message** (mapped above), naming the file, the setting and
   the rule, and stop. Write nothing (ERR-02). SV-05 to SV-07 never stop the run.
   Without a Glob tool, check only these exact paths: `ls docs/specs/policy/ docs/specs/prd/ docs/specs/adr/
   docs/specs/arch/` and `test -e .claude/devforgeai.local.md`. Never list the project root or any folder
   outside `docs/specs/` and the inspection scope. A one-level `ls` of the root, or of a scope's parent, counts
   as listing outside the scope.
3. Run R2: resolve `interview.max_calls` and `architecture.mandated_platforms`, reading
   `.claude/devforgeai.local.md` if it exists. Note every ignored document and local entry.

### 2. Select the PRD

1. If `$ARGUMENTS` (or, when it is empty, the request) names a PRD ID, read `docs/specs/prd/<ID>.md`. If it doesn't exist, say so, list the PRD IDs
   that exist with their titles and status, and stop. Write nothing (ERR-01).
2. If `$ARGUMENTS` is a path or anything else, say that only a PRD ID is accepted, list the PRDs, and stop.
3. If it is empty, list every PRD with its ID, title and status, ask which to use, and end your turn. Ask
   even when only one exists. If there are none, say a PRD must be written first with `/devforgeai:prd`, and stop.

### 3. Read the PRD (R3, R4)

1. Read the PRD's `version`, `status`, `stage`, `operating_context`, functional requirements, non-functional
   requirements (including `category: constraint`), its upstream links, section 12's `[NEEDS ADR: …]` and
   `[NEEDS CLARIFICATION: …]` markers, and its owner. Record the version: every link to the PRD carries it.
2. If `status` isn't `approved`, write the warning as its own line immediately after reading the PRD, even in a
   non-interactive run and even if you have nothing else to say yet, and repeat it in the handoff: "PRD-NNN is
   a <status>, so this architecture is a proposal until the PRD is approved." Don't tick step 3 until it is
   written.
3. Never turn an unanswered product question (a `null` priority or release, or a `[NEEDS CLARIFICATION]`
   marker) into an architectural decision. Never edit the PRD.
4. Run R3 and R4 as mapped above.

### 4. Select the ARCH

1. Glob `docs/specs/arch/ARCH-*.md` and read each one's `system`, title, status, version, upstream PRD links
   and section 1.
2. **None covers the system:** this is a new ARCH, the highest `ARCH-NNN` number plus one (`ARCH-001` if
   none), at `docs/specs/arch/ARCH-NNN.md`. Never ask for or accept a file name.
3. **Several could cover it (ERR-04):** list each with its ID, title, `system` and status, say which fits best
   and why, ask which to use, and end your turn. Never pick one silently.
4. **One covers it:** read `${CLAUDE_SKILL_DIR}/references/readiness.md`, compute the existing ARCH's current
   readiness for this PRD (Check the resolvers, then the readiness rule), and propose, with reasons:
   - **reuse**: it covers this PRD unchanged. Nothing is written;
   - **amend**: it needs new or changed questions or components, for example a requirement or `[NEEDS ADR]`
     marker no DEC cites, or a DEC whose resolver is no longer valid.
   Show the current readiness, including every reopened DEC and why. Ask, and end your turn. Never create a
   second ARCH for the same system unless the user chooses to. If the user chooses reuse, go to step 11.

### 5. Inspect within scope

Read `${CLAUDE_SKILL_DIR}/references/inspection.md` and follow it. Read the project documents it lists.
Code inspection is read-only, and every path it reads, lists or searches is inside the components or
directories the user named. Use Read, Glob and Grep when they are available; otherwise use read-only shell
commands (`ls`, `find`, `grep`, `cat`, `head`) with explicit paths inside the scope. Never list or search the
whole repository. Ask before leaving the scope, and record what you can't read as an unknown (ERR-03). With
no scope named, read no code and don't stop to ask. Record every project source consulted as an EVD item, classified as it says. When
evidence is insufficient, write a `[NEEDS CLARIFICATION: …]` marker, and never recommend reuse on assumption.

### 6. Identify the questions

Follow `readiness.md` (Identify the questions). Every `[NEEDS ADR]` marker becomes a DEC citing every
requirement it names. Add the other questions separate epics must share, each citing every affected
requirement, blocking unless the user says otherwise. Describe the components those epics share as CMP items,
each linked to the NFRs it serves. Leave feature-level detail to specs.

### 7. Resolve the questions

Follow `readiness.md` (Resolve a question). **Non-interactive:** do only item 1 below. Every other question
stays open, no ADR is shown for confirmation, and no ADR is written.

1. **Mandates first.** For each question a mandated platform from R2 answers exactly, set `state: resolved`,
   `resolved_by: [POL-NNN#SET-NN]`, and link the setting on the CMP that provides the capability. Tell the user
   it was applied as policy. A mandate answers only which platform provides its capability.
2. **Existing ADRs.** For an accepted, non-superseded ADR that may answer a question, show it and ask the user
   to confirm that it answers exactly that question. Only then add it to `resolved_by`.
3. **The user's decisions.** For each remaining question, present two to four options with their trade-offs
   against the quality drivers, and your recommendation. Ask at most 4 questions per AskUserQuestion call, and
   at most `interview.max_calls` calls for steps 7 and 8 together. Each explicit choice becomes a new ADR,
   `status: accepted`, that resolves that question only. A question the user defers may get a proposed ADR,
   which resolves nothing. Questions left over stay open; say so.
4. If the user stops mid-session (here or at any other step), write nothing yet and ask, as a direct question: "Save a draft ARCH now,
   with every unanswered question open and the outcome unset?" End your turn. If yes, write it (steps 9 and
   10) with those questions open and `outcome: null`. If no, write nothing (ERR-06).

### 8. Propose the outcome

Propose **reuse** (an existing ARCH covers the PRD unchanged), **amend** (an existing ARCH needs new or changed
questions or components) or **create** (no ARCH covers the system), with reasons. Reusing one platform or
component, including a mandated one, is not a reuse outcome. Ask the user to confirm it, in the same call as
decision questions if possible. Write `outcome` only when the user confirms it, in an answer or explicitly in the request; otherwise leave it
`null`. Confirming the outcome accepts no decision.

### 9. Write the ARCH and ADRs (R5)

1. Read `${CLAUDE_SKILL_DIR}/references/output-rules.md` if you haven't already.
2. **New ARCH:** if the target path exists, stop and ask; never overwrite. Build the file from
   `${CLAUDE_SKILL_DIR}/assets/arch.md`: keep every heading, replace each placeholder or mark it
   `[NEEDS CLARIFICATION: …]`, and delete every author comment and the template's example items. `status: draft`.
   Create `docs/specs/arch/` if missing.
3. **Amend:** edit the existing ARCH as `output-rules.md` (Amending an ARCH) says. Existing items stay
   byte-identical except a DEC's `state` and `resolved_by` transitions, each logged in the Change Log.
4. Write each ADR from step 7 from `${CLAUDE_SKILL_DIR}/assets/adr.md`, as `output-rules.md` (ADRs) says.
5. Provenance on the ARCH and every ADR: `generated_by.tool` `claude-code`, `generated_by.model` your current
   model ID, `generated_by.session` `${CLAUDE_SESSION_ID}`; `authors` the user's name (if known) and
   `claude-code`; `reviewed_by: []`; every `hash: null`; `created` and `updated` today. Never invent a name.
6. When a requirement is infeasible, too costly or in conflict (for example with a mandate), write the proposed
   change in ARCH section 7, addressed to the PRD owner. Never edit the PRD.
7. Run R5: add the policy links where `output-rules.md` (Links) puts them, and end the new Change Log row's
   Change cell with the resolution line.
8. Never modify a PRD, BRN or policy document. Never modify an existing ADR, except to record a supersession
   the user explicitly approved.

### 10. Validate

1. If you can run shell commands, run `devforgeai check --json <file>` for the ARCH and each ADR written. If it
   prints JSON (whatever the exit code), fix every error it lists. If it prints no JSON (not found, or some
   other program), or you can't run commands, check each file against the **Self-check list** in
   `output-rules.md`, reading the file back first.
2. Fix every problem found, then check again. Stop after three attempts.
3. If errors remain after the third attempt, stop fixing and restore only what can't stand unvalidated (ERR-05):
   - every `status`, `approved_by` and `approved_on` this write changed, back to its value before the write.
     A new ARCH stays `draft`. A new ADR the user accepted becomes `proposed` with empty approval fields; keep
     the file;
   - the DEC `state` and `resolved_by` that depended on a restored ADR: an ADR set back to `proposed` resolves
     nothing, so its DEC returns to `open` with `resolved_by: []`;
   - the matching audit record: one Change Log row (and, for an ADR, one Status history row) saying what was
     restored and why.

   Keep everything else as written, including the user's architectural choices and any content unrelated to
   the restore. Then end with a **validation-failure report**: each file path, each unresolved error, and what
   was restored. Skip step 11: leave it unticked in the checklist, and don't present readiness as validated.

### 11. Report readiness and hand off

1. Build the readiness mapping before writing anything (`readiness.md`, Readiness report). For each active FR
   and NFR of the PRD, take the active blocking DECs whose own `upstream` cites it, in the ARCH as written, and
   check each one's resolvers now (Check the resolvers). The requirement is **blocked by exactly the open ones
   among those DECs**, and ready if there are none. A DEC never blocks a requirement it doesn't cite.
2. Report:
   - the ARCH path, or that ARCH-NNN was reused unchanged;
   - the outcome, or that it is **unconfirmed** (`null`);
   - each ADR written, with its path and status;
   - **Ready for epic work:** the requirement IDs, or "none";
   - **Blocked:** each requirement with the open DEC IDs blocking it, and each reopened DEC with the superseded
     or invalid resolver that reopened it;
   - the requirement changes proposed to the PRD owner, or "none";
   - the draft-PRD warning, if step 3 gave one;
   - the policy resolution line, and every ignored policy document or local entry.

   Before sending, check the reply against the mapping: every active FR and NFR appears once, as ready or as
   blocked by its own DEC IDs, and no summary sentence contradicts the lists (never "nothing is ready" while a
   requirement is ready, or the reverse).
3. Name the next step, the **epic workflow**. Check whether `${CLAUDE_PLUGIN_ROOT}/skills/epic/SKILL.md` exists.
   - If it does: tell the user to run `/devforgeai:epic <PRD-ID>`, for the ready requirements only.
   - If it doesn't: say the epic workflow (planned as `/devforgeai:epic`) is not built yet, and that epics may be
     written only for the ready requirements above. Don't present any command as runnable now.
4. Never start the epic workflow, and never write an epic.

## Decisions that need the user

Gates (asked even non-interactively, see Interactive or not) are marked *gate*. The others are asked only
when someone can answer; otherwise the question stays open or the value `null`.

- *gate* **Which PRD**, when no ID is given (step 2).
- *gate* **Which ARCH**, when several could apply, and **reuse or amend**, when one covers the system (step 4).
- **Reading outside the inspection scope** (step 5). With no one to ask, don't read it; record an unknown.
- **Whether an existing ADR answers a question**, and **each architectural decision** (step 7).
- **The outcome** (step 8). Suggest it; never write it unconfirmed.
- *gate* **Saving a draft** when the user stops early (any step).
- **Any requirement change**: the PRD owner decides it outside this skill.

You decide on your own: the ARCH number, the wording of questions and components (the user may edit them),
which questions to ask in which call, applying a mandate that answers a question exactly, and each EVD's
classification, which you show the user.

## Output contract

- Path: `docs/specs/arch/ARCH-NNN.md`; new ADRs at `docs/specs/adr/ADR-NNN.md`, the next free numbers. The
  system name is in `system` and `title`, not the file name.
- Content: the templates `${CLAUDE_SKILL_DIR}/assets/arch.md` and `adr.md`, filled in, every heading kept;
  valid against the schemas as restated in `output-rules.md`.
- Every `[NEEDS ADR]` marker is a DEC. Every DEC cites every affected requirement at the PRD version examined.
- A DEC is `resolved` only by an effective mandate, an accepted non-superseded ADR the user confirmed, or the
  user's explicit decision recorded as a new accepted ADR. Each resolver resolves only its own question.
- `outcome` is `null` unless the user confirmed it. No ADR is `accepted` without the user's explicit decision.
- Every project source consulted is an EVD item with its kind and classification.
- `status` is `draft` (or `in-review` after amending an approved ARCH), never `approved`. The PRD, BRNs and
  policy are never modified.
- Stable CMP, DEC and EVD IDs: the epic workflow cites them. Epics may be written only for requirements the
  readiness rule reports ready.

## References

- [policy.md](references/policy.md): read in step 1, every run, with the mapping above.
- [defaults.md](references/defaults.md): read in step 1, every run.
- [readiness.md](references/readiness.md): read in steps 4, 6, 7 and 11.
- [inspection.md](references/inspection.md): read in step 5, and whenever you record evidence.
- [output-rules.md](references/output-rules.md): read before writing (step 9) and when validating (step 10).
