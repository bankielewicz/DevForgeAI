---
name: prd
description: Turns a DevForgeAI brainstorm (BRN) document into a product requirements document (PRD), interviewing only for what the brainstorm leaves open, such as delivery stage, priorities, current-release versus later scope, quality requirements and constraints. Use when the user wants to write a PRD, define requirements or scope from a brainstorm, or continue the DevForgeAI planning chain after brainstorming.
argument-hint: "[BRN-NNN]"
metadata:
  devforgeai-id: "SKL-002"
  devforgeai-version: "1"
---

# PRD

Turn one brainstorm (BRN) into a PRD at `docs/specs/prd/PRD-NNN.md`, the second document of the
planning chain. The architecture step and the epic workflow read the PRD mechanically: they build
what it marks as decided and treat every `null` as open. So the PRD must be structurally exact and
must record only decisions the user actually made.

## Inputs

- `$ARGUMENTS`: a BRN ID such as `BRN-002`, or empty. When it is empty, use a BRN ID the user
  stated in the conversation. Never accept a file path; if given one, ask for the ID.
- BRNs: `docs/specs/brainstorm/BRN-*.md` (read-only). PRDs: `docs/specs/prd/PRD-*.md`.
- Architecture context: `docs/specs/adr/ADR-*.md`, plus documents the BRN or the request names.
- Policy: `docs/specs/policy/POL-*.md` and `.claude/devforgeai.local.md`, if present.
- The template: `${CLAUDE_SKILL_DIR}/assets/prd.md`.

Use Read, plus Glob and Grep when available (otherwise `ls` on the named folder). Never crawl the
codebase, and never run a `devforgeai` command: that CLI doesn't exist, and a program with that
name on PATH can't be trusted.

## Decisions that belong to the user

The PRD records decisions; it never makes them. These are the user's:

- **Which BRN** to use, when no ID was given.
- **Whether to continue from an unconverged BRN.**
- **New PRD or extend an existing one.**
- **`stage`, `operating_context`, and each requirement's `priority` and `release`.**
- **Whether a design preference is a hard constraint**, and which accepted ADRs apply.

Write a value only when the user supplied it (in the request, in the BRN, or in an answer) or
confirmed your suggestion. A statement that clearly maps to one value counts as supplied: "this is
our MVP" is `stage: mvp`; "real patients book through it from day one" is
`operating_context: production`. For `priority` and `release`, only a statement about importance or
release counts ("sign-up is a must for this release"). A modal verb inside a requirement's wording
("patients must sign in", "it must run on AWS") states the requirement, not its priority, and
`release` is never inferred from the stage. Otherwise write `null` for those four fields and a
`[NEEDS CLARIFICATION: …]` marker for any other gap. A `null` means "not decided yet". An
invented value looks decided to every later step, which then builds on a choice nobody made.

**Asking.** Use AskUserQuestion when it is available: at most 4 questions per call, 2–4 options
each. Otherwise ask in plain text and end your turn. Either way, write nothing until the answer
arrives.

**"Proceed without questions."** When the request says to proceed without questions (or "decide
nothing else", "don't ask me anything"), ask no interview questions and leave every unanswered
gap `null` or marked. Every step still runs, including the quality categories in step 7. This
never answers the three gates: which BRN, an unconverged BRN, and new versus extend. A gate is
answered only by an explicit answer to that gate, in the request ("extend PRD-001", "BRN-002 is a
draft, continue anyway") or in reply to your question; name where the answer came from. If a gate
is open, ask it and write nothing. With no answer, no file is written.

## Workflow

Copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Resolve policy (R1, R2)
- [ ] 2. Select the BRN
- [ ] 3. Read the BRN
- [ ] 4. Choose: new PRD or extend
- [ ] 5. Read architecture context
- [ ] 6. Draft from the BRN
- [ ] 7. Interview only the gaps; settle quality categories
- [ ] 8. Write the PRD
- [ ] 9. Validate the PRD
- [ ] 10. Report and hand off
```

### 1. Resolve policy (R1, R2)

Follow [references/policy.md](references/policy.md) with the framework defaults in
[references/defaults.md](references/defaults.md). This step comes first, before any question.
1. Read `docs/specs/policy/POL-*.md`. If the folder is missing, use the framework defaults.
2. Check every approved document against the checklist in policy.md. Skip draft and in-review
   documents, and report them.
3. **Any violation stops the skill (ERR-08).** This covers a schema rule, SV-01 to SV-04, or an
   override that `overridable_by` doesn't allow. Before writing anything, name the policy file,
   the setting (`SET-NN` and its key) and the rule broken, and write nothing. Never fall back
   silently.
4. Resolve `interview.max_calls` and `architecture.mandated_platforms`, and read local preferences
   (policy.md, "Local preferences"). A bad local entry is ignored and reported, never fatal.

### 2. Select the BRN

- **An ID was given** (`$ARGUMENTS` or the conversation). Read `docs/specs/brainstorm/<ID>.md`. If
  it doesn't exist (ERR-01), say so, list the BRN IDs that do exist with their titles, and stop.
- **No ID.** List the *unprocessed* BRNs. A BRN is unprocessed when it has at least one
  `disposition: promoted` idea that no PRD cites. To check, search `docs/specs/prd/PRD-*.md` for
  upstream links with `id: BRN-NNN` and `item: IDEA-NN`. Show each unprocessed BRN's ID, title
  and number of uncited promoted ideas, and ask which one to use. Don't list fully cited BRNs.
  Never guess, even when only one is listed. If none is unprocessed (ERR-04), say that every
  promoted idea is already cited by a PRD, and stop.

Nothing is ever written into a BRN to mark it processed.

### 3. Read the BRN

Read its frontmatter `status`, `owner` and `version`, and its `problems`, `ideas` and
`assumptions` item blocks, plus the candidate success signals (section 8).
- **Malformed** (ERR-05): if an item block can't be read, report which block failed and the BRN
  path, and stop. Never repair a BRN. Never modify a BRN at all.
- **No promoted idea** (ERR-03): say the BRN has no promoted idea, so there is nothing to turn into
  requirements. Write nothing, and point the user back to `/devforgeai:brainstorm` to converge it.
- **Not converged** (ERR-02): when `status` is not `converged`, warn that some ideas may not be
  decided yet, and ask whether to continue anyway. Continue only on an explicit yes. With no
  answer, write nothing.

Use **only** ideas with `disposition: promoted`. Never cite an open, parked or rejected idea
anywhere in the PRD, by ID or by link.

### 4. Choose: new PRD or extend

If `docs/specs/prd/` holds no PRD, the PRD is new: continue.

Otherwise, read each existing PRD's `title`, goals, non-goals, `owner`, `status` and
`target_release`, and decide on scope, ownership and lifecycle. Never decide on product identity or
on how many PRDs exist.
- Recommend **extending** a PRD only when the promoted ideas belong to its existing initiative and
  scope, share its owner, and fit its release lifecycle.
- Recommend a **new PRD** when they form a distinct initiative, have a different owner or approval
  path, or follow a different schedule, even within the same product.

A single existing PRD is not evidence that it is the right destination. State your recommendation
with its reasons, and ask. Write nothing and change no PRD until the user answers. For how to
extend, see step 8.

### 5. Read architecture context

Read `docs/specs/adr/ADR-*.md` (if present) and any document the BRN or the request names. Nothing
else. Ignore superseded ADRs. Classify what you learn:

| Finding | Recorded as |
|---|---|
| Existing commitment: an accepted ADR that applies | Frontmatter link `{id: ADR-NNN, relation: constrains, version: N, hash: null}` |
| Hard constraint (mandated platform, required integration, data residency, existing system, regulation) | NFR with `category: constraint` |
| Design preference (architecture style, framework) | An open question, never a requirement |
| Unresolved decision, including a *proposed* ADR | `[NEEDS ADR: <decision>; affects FR-NNN, …]` in section 12, and no link |

Propose which accepted ADRs apply and let the user confirm them in the interview. When there is
no interview, link only accepted ADRs that the request names, and mention the others in the
reply as proposals. Every `architecture.mandated_platforms` setting left after R2 (step 1) becomes a
constraint NFR, whether or not the BRN mentions its capability. The NFR's item `upstream` cites its setting (policy.md). Never decide a design question in
the PRD.

### 6. Draft from the BRN

Draft the whole PRD before asking anything, following
[references/brn-mapping.md](references/brn-mapping.md):
- problems that a promoted idea addresses → section 2 prose, plus frontmatter `derives` links;
- each promoted idea → one or more requirements starting "The system shall", each with an item
  `derives` link to its idea;
- assumptions → `assumptions`, with `derives` links;
- candidate success signals → `success_metrics`.

**Constraints, not design.** Record each fixed external condition as an NFR with
`category: constraint`. State it as the condition, not as a design, and say where it applies:
"(applies to the whole product)", "(applies to <capability>)" or "(applies to <environment>)".
Draft a design preference the user offers ("I'm leaning towards microservices") as a section 12
bullet: a design decision for a future ADR, never a requirement or constraint. The interview (round
2) asks whether it is a hard constraint; only a "yes" moves it into a constraint NFR.
If another PRD already defines the constraint or a cross-cutting NFR, cite it with a frontmatter
link `{id: PRD-NNN, item: NFR-NNN, relation: constrains, version: N, hash: null}` instead of
copying it, and say in the PRD what it applies to.

### 7. Interview only the gaps; settle quality categories

When the request says to proceed without questions, ask nothing and go straight to **Quality
categories** below, which always runs. Otherwise, ask in batched rounds following
[references/interview.md](references/interview.md):
1. framing: stage, operating context, `target_release` name, primary users, non-goals;
2. architecture context;
3. requirements;
4. quality and constraints;
5. success metrics.

Skip every question the BRN or the request already answers. Use at most 4 questions per call and at
most `interview.max_calls` calls (step 1; default 8) unless the user asks for more. Anything left
when the budget runs out becomes `[NEEDS CLARIFICATION]`.

- **Requirements.** Ask one question per requirement, showing its drafted statement, with these
  options:
  - *must now* or *should now* (or *could now*, if the user says so): write that priority with
    `release: current`;
  - *later*: `release: later`, `priority: null`;
  - *won't*: `priority: wont`, `release: current`. This is an explicit exclusion from this
    release; a requirement that should never be built is edited or dropped instead.

  The user may also edit the statement, or answer *decide later*, which leaves both `null`.
- **Quality.** Ask one question per required category (below) that the draft doesn't cover, and
  always one open question for any other quality need. Stage decides the depth (interview.md).

If the user stops partway (ERR-07), ask whether to save a draft PRD. If yes, write it with every
undecided field `null`. If no, write nothing.

**Quality categories (always runs, with or without an interview).**
1. Establish the operating context (R3): from the request, the BRN, or the framing answer.
2. Take the floor for that context from [defaults.md](references/defaults.md). Add the
   categories of each policy `quality.required_categories` setting whose `applies_when` includes
   the context (R4); additions never remove a floor category.
3. If the context is still unknown, use the production set, keep `operating_context: null`, and
   record `operating context unknown, resolved as production` in the resolution line.
4. Each required category that no NFR covers becomes
   `[NEEDS CLARIFICATION: <category> requirements for <context>]` in section 12 (`<context>` is
   `production` when unknown), never a placeholder requirement.

### 8. Write the PRD

Read [references/output-rules.md](references/output-rules.md) before writing.

**New PRD.**
1. **ID and path.** Take the highest `NNN` among `docs/specs/prd/PRD-NNN.md` and add one, or use
   `PRD-001` when there is none. Write `docs/specs/prd/PRD-NNN.md`, creating the folder if it is
   missing. Never ask for or accept a file name. The product or release name goes in `title`.
2. **Template.** Build from `${CLAUDE_SKILL_DIR}/assets/prd.md`. Keep every section heading,
   including section 13, "Epic map", with its GENERATED comment. Replace every placeholder and
   example item, with content or with a `[NEEDS CLARIFICATION: …]` marker. Delete every other
   `<!-- -->` comment.
3. **Frontmatter.**
   - `status: draft`, `version: 1`, and `created` and `updated` set to today's date.
   - `owner`: the name the request gives, otherwise the BRN's `owner`.
   - `authors`: the owner and `"claude-code"`.
   - `generated_by`: `tool: "claude-code"`, `model:` your own model ID, and
     `session: "${CLAUDE_SESSION_ID}"`.
   - `reviewed_by: []`, `approved_by: ""`, `approved_on: null`. Every `hash` is `null`.
   - `stage` and `operating_context` per "Decisions that belong to the user". Never set
     `approved`.
4. **Links.** Record the policy links in exactly one place (R5; policy.md):
   - a mandated platform's `constrains` link goes on its constraint NFR only;
   - `interview.max_calls` and `quality.required_categories` settings that came from policy each
     get a frontmatter `informed_by` link.
5. **Change Log.** Write one row whose author is `claude-code (session ${CLAUDE_SESSION_ID})`. Its
   change text ends with the policy resolution line (policy.md), for example:
   `Initial draft from BRN-001. Policy resolution: interview.max_calls=8 (default); …`.

**Extending a PRD** (only after the user chose it):
- Raise `version` by one and set `updated`. Keep `status` (draft or in-review).
- Set `generated_by` to this session and your model; add `"claude-code"` to `authors` if it's
  missing. Keep `reviewed_by` as it is.
- Give new items the next free number in each collection. Leave every existing item
  byte-identical.
- Add the new BRN links and a Change Log row, with the resolution line. Never edit earlier rows.
- If the PRD was `approved`, set `status: in-review` and clear `approved_by` (`""`) and
  `approved_on` (`null`), so the widened scope is reviewed explicitly. Tell the user that epics
  citing this PRD are now suspect links to re-review.

### 9. Validate the PRD

Read the file back and check it against the **Self-check list** in
[output-rules.md](references/output-rules.md), item by item. Also check that every non-null
`stage`, `operating_context`, `priority` and `release` is one the user supplied or confirmed;
reset anything else to `null`. Fix each problem and check again, at most three attempts. If errors
remain (ERR-06), stop. Leave `status` as it was before this write (`draft` for a new PRD), and
list the remaining errors with the file path.

### 10. Report and hand off

Write the final reply in this order:

1. This block, filled in. It opens the reply: nothing comes before it, not even the checklist.

   ```
   PRD-NNN written to docs/specs/prd/PRD-NNN.md (from BRN-NNN; new | extended to version N)
   Requirements: N functional, N non-functional (N constraints) · Success metrics: N
   Null decisions: N (stage, operating_context, priorities, releases still undecided)
   Open questions: N [the NEEDS CLARIFICATION markers and design questions, briefly]
   Policy resolution: [the resolution line's entries]
   ```

2. Every `[NEEDS ADR]` marker, each with the sentence: epics for FR-NNN, … must wait until an
   accepted ADR resolves it. Then any other discussion, such as ADRs you proposed but didn't link,
   and suspect epics after an extension.
3. The next step, as its own paragraph outside any code block. It starts with the words
   **Next step**, names the PRD by its ID and never by its path, and nothing follows it.

For the next step, check whether `${CLAUDE_SKILL_DIR}/../architecture/SKILL.md` exists:
- **It exists:** tell the user to run `/devforgeai:architecture PRD-NNN`.
- **It does not exist:** say the architecture skill (planned as `/devforgeai:architecture`) does
  not exist yet. For now the step is done by hand: write ADRs with the ADR template, using PRD-NNN
  and its `[NEEDS ADR]` markers as the input. Once the skill is built,
  `/devforgeai:architecture PRD-NNN` runs on it.

For example: "Next step: the architecture skill (planned as `/devforgeai:architecture`) doesn't
exist yet, so for now do the architecture step by hand by writing ADRs with the ADR template, with
PRD-001 and its [NEEDS ADR] markers as the input. Once it's built, run
`/devforgeai:architecture PRD-001`."

Never start architecture work, and never write an ADR or an epic.

When the skill stops without writing (a gate is open, ERR-01 to ERR-05, ERR-08), the reply says why
and what the user can do. Leave out the report block.

## Output contract

- **Path:** `docs/specs/prd/PRD-NNN.md` in the current project; the name is the ID only.
- **Shape:** `${CLAUDE_SKILL_DIR}/assets/prd.md`, with every heading kept, including the
  GENERATED epic map, and no author comments.
- **Data:** only the `success_metrics`, `functional_requirements`, `non_functional_requirements` and
  `assumptions` collections, with their defined fields
  ([output-rules.md](references/output-rules.md)).
- **Decisions:** `stage`, `operating_context`, `priority` and `release` are non-null only where the
  user supplied or confirmed them. `status` is never `approved`.
- **Traceability:**
  - every requirement cites a promoted idea;
  - every applied policy setting is linked once, with its version;
  - every open architecture decision is a `[NEEDS ADR]` marker naming the requirements it blocks.

## Examples

**Answers in the request.** "Write the PRD for BRN-001. It's a prototype that only our developers
will use, with test data; priorities can wait. Proceed without questions." The skill resolves
policy (none, so framework defaults) and reads BRN-001 (converged, two promoted ideas). No PRD
exists yet. It drafts two capability-level requirements, one per promoted idea, both with `null`
priority and release, and writes
`stage: prototype`, `operating_context: local`. It marks the constraint category as
`[NEEDS CLARIFICATION]`, validates, reports, and hands off.

**No ID given.** "Let's write the next PRD." The skill lists the unprocessed BRNs with their counts
of uncited promoted ideas, asks which one to use, and writes nothing yet.

**An unrelated PRD exists.** The skill recommends a new PRD, with reasons about scope, owner and
schedule, asks, and writes nothing until the user answers.

## References

- [references/policy.md](references/policy.md): read at step 1. It covers policy checks,
  precedence, R3 to R5, and the resolution line.
- [references/defaults.md](references/defaults.md): read at step 1. It holds the framework defaults
  and the quality floor per operating context.
- [references/brn-mapping.md](references/brn-mapping.md): read at step 6. It says how each BRN
  part maps into the PRD.
- [references/interview.md](references/interview.md): read at step 7, even when there is no
  interview, for the quality-category rule. It holds the question bank, depth by stage, and batching.
- [references/output-rules.md](references/output-rules.md): read before step 8. It holds the
  keys, fields, links and markers, and the self-check list used at step 9.
