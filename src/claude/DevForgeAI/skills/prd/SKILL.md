---
name: prd
description: Turns a DevForgeAI brainstorm (BRN) document into a product requirements document (PRD), interviewing only for what the brainstorm leaves open, such as delivery stage, priorities, current-release versus later scope, quality requirements and constraints. Use when the user wants to write a PRD, define requirements or scope from a brainstorm, or continue the DevForgeAI planning chain after brainstorming.
argument-hint: "[BRN-NNN]"
metadata:
  devforgeai-id: "SKL-002"
  devforgeai-version: "1"
---

# PRD

Turn one brainstorm (`docs/specs/brainstorm/BRN-NNN.md`) into a PRD, `docs/specs/prd/PRD-NNN.md`, whose
requirements trace to the brainstorm's promoted ideas. The PRD records the user's decisions; you never make
them. It states what and why; architecture is read and classified, never designed.

## Inputs

- `$ARGUMENTS`: a BRN ID such as `BRN-002`, or empty. Never a file path.
- `docs/specs/brainstorm/BRN-*.md`: brainstorms (read-only, always).
- `docs/specs/prd/PRD-*.md`: existing PRDs, for unprocessed BRNs, new-or-extend, ID allocation and shared constraints.
- `docs/specs/policy/POL-*.md` and `.claude/devforgeai.local.md`: policy and local preferences.
- `docs/specs/adr/ADR-*.md`, and documents the BRN or the request names: architecture context.
- `${CLAUDE_SKILL_DIR}/assets/prd.md`: the PRD template.
- `${CLAUDE_SKILL_DIR}/references/`: `policy.md`, `defaults.md`, `brn-mapping.md`, `interview.md`, `output-rules.md`.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Resolve policy (R1, R2)
- [ ] 2. Select the BRN
- [ ] 3. Read and check the BRN
- [ ] 4. Decide new PRD or extension
- [ ] 5. Read architecture context
- [ ] 6. Draft from the BRN
- [ ] 7. Interview for gaps (R3)
- [ ] 8. Write the PRD (R4, R5)
- [ ] 9. Validate the PRD
- [ ] 10. Report and hand off
```

**Interactive or not.** The run is *non-interactive* when the request says to proceed without questions, or
when no one can answer (for example, an automated run). Then ask no interview question (step 7): every
undecided value stays `null` and every gap becomes a marker. **Gating questions are never skipped**, even
non-interactively: which BRN (step 2), whether to continue with an unconverged BRN (step 3), new or extend
(step 4), and saving a draft when the user stops. For a gating question, first write everything the user
needs to decide in your reply text (the list, the warning, the reasons), then ask with AskUserQuestion, or in
plain text if it is unavailable, and **end your turn**. Write no file and create no directory until it is answered.
A gate counts as answered only when the request answers that exact question (for example "extend PRD-001" or
"continue even though BRN-001 is a draft"). "Proceed without questions" answers no gate.

### 1. Resolve policy (R1, R2)

1. Read `${CLAUDE_SKILL_DIR}/references/policy.md` and `${CLAUDE_SKILL_DIR}/references/defaults.md`.
2. Run R1: load `docs/specs/policy/POL-*.md`, skip and note draft or in-review documents, and validate every
   approved one against the schema and semantic rules. On a schema violation, an SV-01 to SV-04 violation or a
   disallowed override, reply with the policy.md **Stop message** and stop. Write nothing. SV-05 to SV-07 never
   stop the run: they skip or ignore, and are reported.
3. Run R2: resolve `interview.max_calls` (the interview budget) and `architecture.mandated_platforms`, reading
   `.claude/devforgeai.local.md` if it exists. Note every ignored document and local entry for the resolution line.

### 2. Select the BRN

1. If `$ARGUMENTS` is a BRN ID, read `docs/specs/brainstorm/<ID>.md`. If it doesn't exist, say so, list the
   BRN IDs that do exist with their titles, and stop (ERR-01). If `$ARGUMENTS` is a path or anything else,
   say that only a BRN ID is accepted, list the BRNs, and stop. Write nothing.
2. If it is empty, find the **unprocessed** BRNs (`brn-mapping.md`, Unprocessed BRNs). List each one with its
   ID, title and number of uncited promoted ideas, ask which to use, and end your turn. Ask even when only one
   is listed. Never pick one yourself.
3. If none is unprocessed, say that every promoted idea is already cited by a PRD, and stop (ERR-04).

### 3. Read and check the BRN

1. Read `${CLAUDE_SKILL_DIR}/references/brn-mapping.md` and read the BRN as it says. Never edit the BRN.
2. If an item block can't be read, stop and report the failing block and the BRN path (ERR-05).
3. If the BRN has no active promoted idea, stop, write nothing, and tell the user to converge it first with
   `/devforgeai:brainstorm` (ERR-03).
4. If `status` isn't `converged`, warn that some ideas may not be decided yet, and ask whether to continue
   with the promoted ideas only. End your turn; continue only after the user confirms (ERR-02).

### 4. Decide new PRD or extension

1. Glob `docs/specs/prd/PRD-*.md`. If there is none, this is a new PRD.
2. Otherwise read `${CLAUDE_SKILL_DIR}/references/interview.md` and follow its New PRD or extension section: compare scope, ownership and lifecycle, state a
   recommendation with reasons for each, and ask. End your turn. Never default to extending, and never
   treat the existence of a PRD, or of only one, as a reason.
3. **New PRD:** the ID is the highest `PRD-NNN` number plus one (`PRD-001` if none). The path is
   `docs/specs/prd/PRD-NNN.md`. Never ask for or accept a file name.

### 5. Read architecture context

Read `${CLAUDE_SKILL_DIR}/references/interview.md` (Round 2). Read ADRs in `docs/specs/adr/` and documents the
BRN or the request names; never crawl the codebase. Ignore superseded ADRs. Classify what you learn as that
section says. Each mandated platform from R2 becomes a constraint NFR citing its setting.

### 6. Draft from the BRN

Before asking anything, draft the PRD in memory following `brn-mapping.md`: problems into section 2 with
frontmatter `derives` links, each promoted idea into FRs starting "The system shall", assumptions with
`derives` links, success signals into metrics. Add constraint NFRs from steps 5 and the request, following
`interview.md` (Constraint or design). Add an NFR in its category for every quality requirement the request
states (for example "users must sign in" is security), with `priority` and `release` `null` unless the request
gives them. Take stage and operating context from the request as `interview.md` (Stage and operating context) says. Cite shared constraints from other PRDs instead of copying them (BEH-15).

### 7. Interview for gaps (R3)

1. Follow `interview.md`. Plan the calls first: skip every question the BRN or the request answers.
2. Establish the operating context (R3) and the stage from the request, then the BRN, then round 1.
3. Ask at most 4 questions per call and at most `interview.max_calls` calls, unless the user asks for more.
4. Non-interactive: ask nothing and go to step 8.
5. If the user stops mid-interview, ask whether to save a draft. If yes, write it (steps 8 and 9) with every
   undecided field `null`. If no, write nothing.

### 8. Write the PRD (R4, R5)

1. Read `${CLAUDE_SKILL_DIR}/references/output-rules.md` if you haven't already.
2. Run R4: required categories = the floor for the operating context plus applicable policy additions; with
   no established context, evaluate as `production` and leave `operating_context: null`.
3. **New PRD:** if the target path exists, stop and ask; never overwrite. Build the file from
   `${CLAUDE_SKILL_DIR}/assets/prd.md`. Keep every section heading, including `## 13. Epic map` and its
   GENERATED comment. Replace each placeholder or mark it `[NEEDS CLARIFICATION: <question>]`. Delete the other
   author comments and the template's example items. Create `docs/specs/prd/` if missing.
4. Write `stage`, `operating_context`, every `priority` and every `release` only as the user supplied or
   confirmed them; otherwise `null`. Mark each unanswered required category, open decision and design
   preference as `output-rules.md` (Markers) says. `status: draft` for a new PRD. Never `approved`.
5. Frontmatter provenance: `generated_by.tool` `claude-code`, `generated_by.model` your current model ID,
   `generated_by.session` `${CLAUDE_SESSION_ID}`; `authors` the user's name and `claude-code`; `reviewed_by: []`;
   `approved_by: ""`, `approved_on: null`; every `hash: null`; `created` and `updated` today. Put the product
   or release name in `title`. `owner` is the user's name, else the BRN's owner. If the user's name isn't
   known, `authors` is the BRN owner's name (if any) and `claude-code`; never invent a name.
6. Run R5: add the policy links, and end the new Change Log row's Change cell with the resolution line.
7. **Extension:** edit the PRD in place as `interview.md` (New PRD or extension) says. Leave every existing
   item byte-identical. Keep `status` unless it was `approved` (then `in-review`, approval cleared).

### 9. Validate the PRD

1. If you can run shell commands, run `devforgeai check --json <file>`. If it prints JSON (whatever the exit
   code), fix every error it lists. If it prints no JSON (not found, or some other program), or you can't run
   commands, check the file against the **Self-check list** in `output-rules.md`, reading the file back first.
2. Fix every problem found, then check again. Stop after three attempts.
3. If errors remain, leave `status` as it is (never `approved`), and list the file path and the remaining
   errors in your reply (ERR-06).

### 10. Report and hand off

1. Report the PRD path; the counts of functional requirements, constraint NFRs, other NFRs and success metrics;
   the number of `null` decisions (stage, operating context, priorities, releases); the open questions; the
   policy resolution line; and any ignored policy document or local entry.
2. List every `[NEEDS ADR]` marker and say that epics for the requirements it names must wait until an accepted
   ADR resolves it.
3. If this run extended a PRD, say that epics citing it are now suspect links to re-review.
4. Name the next step, the **architecture step** (ADR-002). Check whether
   `${CLAUDE_PLUGIN_ROOT}/skills/architecture/SKILL.md` exists.
   - If it does: tell the user to run `/devforgeai:architecture <PRD-ID>`.
   - If it doesn't: say the architecture skill (planned as `/devforgeai:architecture`) does not exist yet, that
     for now the step is done by hand by writing ADRs with the ADR template, and that this PRD and its
     `[NEEDS ADR]` markers are its input. Don't present any command as runnable now.
5. Never start architecture work, write an ADR or write an epic.

## Decisions that need the user

- **Which BRN**, when no ID is given (step 2).
- **Continuing with an unconverged BRN** (step 3).
- **New PRD or extension**, whenever a PRD exists (step 4).
- **Stage, operating context, target release, and each requirement's priority and release** (step 7). Suggest,
  never write unconfirmed.
- **Whether a design preference is a hard constraint**, and **which accepted ADRs apply** (step 5, step 7).
- **Quality requirements and metric targets** (step 7).
- **Saving a draft** when the user stops early (step 7).

You decide on your own: the PRD number, the FR wording drafted from promoted ideas (the user may edit it), the
batching of questions, and the classification of architecture context, which you show the user.

## Output contract

- Path: `docs/specs/prd/PRD-NNN.md`. The product or release name is in `title`, not the file name.
- Content: the template `${CLAUDE_SKILL_DIR}/assets/prd.md`, filled in, with every heading kept; valid against the
  PRD schema as restated in `output-rules.md`.
- Every FR `derives` from a promoted idea of the BRN. No open, parked or rejected idea is cited or named.
- `stage`, `operating_context`, `priority` and `release` are `null` unless the user decided them. `wont` with
  `release: current` is an explicit exclusion from the current release; no epic is written for it.
- Constraints are `category: constraint` NFRs; design is never a requirement. Open decisions are `[NEEDS ADR]` markers.
- Applied policy settings are upstream links with the policy version; the Change Log row carries the resolution line.
- `status` is `draft` (or `in-review` after extending an approved PRD), never `approved`. The BRN is never modified.
- Stable FR, NFR, SM and ASM IDs: the architecture step and the epic workflow cite them.

## References

- [policy.md](references/policy.md): read in step 1, every run; R3 to R5 in steps 7 and 8.
- [defaults.md](references/defaults.md): read in step 1, every run.
- [brn-mapping.md](references/brn-mapping.md): read in steps 2 and 3.
- [interview.md](references/interview.md): read in steps 4, 5 and 7.
- [output-rules.md](references/output-rules.md): read before writing (step 8) and when validating (step 9).
