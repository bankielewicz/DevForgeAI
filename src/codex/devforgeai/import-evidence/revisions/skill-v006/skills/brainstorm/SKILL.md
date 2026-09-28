---
name: brainstorm
description: Runs a structured brainstorming session and writes a DevForgeAI brainstorm (BRN) document with identified problems, ideas, assumptions and user-confirmed dispositions. Use whenever the user asks to brainstorm, explore ideas or options, come up with ways to solve a problem, or generate ideas for a product, feature or process, even when they don't mention a document, and to start the DevForgeAI planning chain before a PRD.
metadata:
  devforgeai-id: "SKL-001"
  devforgeai-version: "6"
---

# Brainstorm

Run a brainstorming session on one topic and record it as a BRN document at
`docs/specs/brainstorm/BRN-NNN.md`, the first document of the planning chain. A PRD cites the BRN's
problems, ideas and assumptions by ID, so the document must be structurally exact and must only
claim decisions the user actually made.

## Inputs

- The topic supplied with the Brainstorm skill mention (for example `$brainstorm dental
  appointment no-shows`), or in the conversation. If absent, ask for it.
- Existing BRNs: `docs/specs/brainstorm/BRN-*.md` in the current project.
- The template: `assets/brainstorm.md`.

Resolve every asset, reference, and script path relative to the directory containing this
`SKILL.md`, using its actual loaded location. Do not resolve these paths from the user's project
or assume a provider environment variable. Resolve `docs/specs/` from the user's project root.
Use the host's normal file, shell, and question capabilities; this skill grants no tool approvals.

## Decisions that belong to the user

Two decisions are the user's, never yours:

- **Each idea's disposition** (`promoted`, `parked` or `rejected`) and its `reason`.
- **Convergence**: whether the brainstorm is finished (`status: converged`).

Propose both, then ask. Anything the user has not explicitly confirmed stays `disposition: open`,
`reason: null` and `status: draft`. When no confirmation can be obtained, treat it as *not
confirmed* and continue with those values. This happens when the user said to proceed without
questions or no user is there to answer. Record your proposals in section 6 prose so nothing is
lost. An unconfirmed disposition looks valid to every structural check, and a PRD would build on
a choice nobody made. That is why this rule matters more than any other in this skill.

## Workflow

Once you have a topic, copy this checklist into your response and tick items off as you go:

```
- [ ] 1. Intake: topic, existing BRNs, clarifying questions
- [ ] 2. Select a framework
- [ ] 3. Diverge: problems, ideas, assumptions
- [ ] 4. Evaluate with the framework
- [ ] 5. Propose dispositions and ask the user to confirm
- [ ] 6. Write the BRN
- [ ] 7. Validate the BRN
- [ ] 8. Report and hand off
```

### 1. Intake

1. **Topic.** Use the topic accompanying the skill mention, or stated in the conversation. If there is none, ask
   "What topic should we brainstorm?" and stop. Create no file and no directory until the user
   gives a topic.
2. **Existing BRNs.** Find `docs/specs/brainstorm/BRN-*.md` and read each file's `title`. If one
   covers the same or a closely similar topic, show its ID, title and path and ask:
   *extend it* (version + 1, with a Change Log entry) or *create a new BRN*. Wait for the answer
   and write nothing before it. Never overwrite an existing BRN silently.
3. **Clarifying questions.** Ask at most three, in one message: what triggered this, who is
   affected, and what constraints apply. Skip any the request already answers. Ask none when
   the request says to proceed without questions. Record anything still unknown as
   `[NEEDS CLARIFICATION: question]` in the document; never fill a gap with a guess.

Use an available Codex question tool when appropriate to its supported mode; otherwise ask
in plain text and end your turn. A pending question, silence, or timeout is never confirmation.

### 2. Select a framework

Read `references/frameworks/INDEX.md`. Pick the framework the user named, or
the one whose *use when* criteria best fit the topic; use `diverge-converge` when nothing fits
better. Read the chosen framework file and follow it from here on. Tell the user in one
sentence which framework you chose and why, and switch if they ask.

If the index is missing, or the chosen file is missing or lacks any section the index requires,
fall back to `diverge-converge` and tell the user which file was the problem.

### 3. Diverge

Follow the framework's steps and questions.

- Frame **problems** first (`PRB-NN`), stated from the affected user's side.
- Capture **ideas** (`IDEA-NN`). Record the user's own ideas in their own words, alongside the
  ideas you generate. Generate between 5 and 15 ideas unless the user asks for another number.
  Every idea addresses at least one problem and starts with `disposition: open`.
- Capture **assumptions** (`ASM-NN`): beliefs the ideas depend on, each with how to validate it.

### 4. Evaluate

Fill `value`, `effort`, `risk` and `score` on each idea exactly as the framework's *Mapping to the
BRN* section says. Write only into the `problems`, `ideas` and `assumptions` collections and
their defined fields, whatever the framework. Framework-specific reasoning goes into the section
5 (evaluation method) and section 6 (convergence) prose, never into new YAML keys.

### 5. Propose dispositions and confirm

Present a table: idea, proposed disposition, one-line reason. Ask the user to confirm or change
each one, and whether the brainstorm has converged. Then:

- Write each disposition and reason the user confirmed (explicitly, or by accepting the table).
- Leave every other idea `open` with `reason: null`.
- Set `status: converged` only if the user confirmed convergence; otherwise `draft`.

If the user stops partway through the session, ask whether to save what has been captured as a
draft BRN. If yes, write it with every disposition `open`. If no, write nothing.

### 6. Write the BRN

1. **ID and path.** Take the highest `NNN` among `docs/specs/brainstorm/BRN-NNN.md` and add one;
   use `BRN-001` when there is none. Zero-pad to three digits. Write the file to
   `docs/specs/brainstorm/BRN-NNN.md`. The file name is the ID only: never ask for a file name, and
   if the user offers one, say the file is named by its ID and put their wording in the title.
   Create `docs/specs/brainstorm/` if it is missing, and say that you created it.
2. **Build from the template.** Read `assets/brainstorm.md`. Keep every section
   heading. Replace every placeholder with content or with a `[NEEDS CLARIFICATION: …]` marker.
   Replace the example items with the real ones. Delete every HTML comment.
3. **Frontmatter.**
   - `id`: the allocated ID. `title`: the descriptive topic. `version: 1`.
   - `created` and `updated`: today's date as `YYYY-MM-DD`.
   - `status`: see step 5.
   - `owner`: the user's name if the conversation or existing `docs/specs/` documents show it.
     Otherwise ask, or use `"[NEEDS CLARIFICATION: owner]"` when you cannot ask.
   - `authors`: the user (the owner's name) and `"codex"`.
   - `generated_by`: `tool: "codex"`, `model:` the actual model ID exposed by the host, and
     `session:` the current Codex task/session ID exposed by the host (for example the value
     of `CODEX_THREAD_ID` when available). Read the values; never write variable names or
     invent identifiers. If the host does not expose a value, use the explicit sentinel
     `"unknown"`, keep the document draft, and disclose the missing provenance in section 7
     and the handoff. This is incomplete provenance, not successful verification of VER-03.
   - `reviewed_by: []`, `approved_by: ""`, `approved_on: null`. Every `hash` is `null`.
   - `upstream`, `participants` and `sources`: fill from the conversation, or leave them empty.
4. **Change Log.** One row: version, today's date, `codex (session ACTUAL-SESSION-ID)`,
   what changed. Substitute the same session value as `generated_by.session`. Preserve that
   identifier for traceability; do not promise a transcript location, retention period, or
   a provider-specific resume command. If unavailable, use `codex (session unknown)` and
   disclose incomplete provenance as above.

**Extending an existing BRN.** Keep every existing item ID with its meaning unchanged, because PRD
requirements cite these IDs. Give new items the next free number in their collection. Retire an
item by setting `status: deprecated` (plus `superseded_by` if replaced), never by deleting or
renumbering it. Bump `version`, set `updated`, update `generated_by.tool` to `codex`,
`generated_by.model` to the actual current model and `generated_by.session` to this session,
and add a Change Log row naming this session. Retain prior authors and add `codex` once. Never edit earlier Change Log rows: they keep the
sessions that wrote earlier versions.

Read [output-rules.md](references/output-rules.md) before writing: it defines the frontmatter
keys, ID patterns, item-block rules and allowed fields.

### 7. Validate the BRN

1. Run the validator:

   ```bash
   python3 "/absolute/path/to/brainstorm/scripts/validate_brn.py" docs/specs/brainstorm/BRN-NNN.md
   ```

   Substitute the actual loaded skill directory in the command and run from the user's
   project root. Use the available Python 3 executable on the host.

   It prints one line per problem (`line N: message`) and exits 1, or prints `OK: path` and
   exits 0. Don't run any `devforgeai` command, even if one is on PATH. Only without a shell or
   Python, check the file by hand against the *Validation checklist* in
   [output-rules.md](references/output-rules.md).
2. The validator can't know what the user confirmed. After it passes, read the file back and
   check that every disposition other than `open`, and `status: converged`, is one the user
   confirmed in step 5. Reset anything else to `disposition: open` with `reason: null`, or to
   `status: draft`.
3. Fix every problem found, then run the checks again. Stop after three attempts.
4. If errors remain after three attempts, set `status: draft`, stop, and list the remaining
   errors with the file path.

### 8. Report and hand off

Write the final reply in this order, so the facts come first and the next step is the last thing
the user reads:

1. This block, filled in. It opens the reply: nothing comes before it, not even the workflow
   checklist.

   ```
   BRN-NNN written to docs/specs/brainstorm/BRN-NNN.md (framework: [name])
   Problems: N · Ideas: N · Assumptions: N
   Promoted: IDEA-NN, … | none confirmed yet (proposals are in section 6)
   Open questions: [each NEEDS CLARIFICATION marker and open assumption, briefly]
   ```

2. Any discussion.
3. The next step, as its own paragraph outside any code block, starting with the words
   **Next step**. Nothing follows it.

For the next step, check whether `../prd/SKILL.md`, relative to this skill, exists
and is available as the DevForgeAI PRD skill in Codex:

- **It exists and is available:** tell the user to select the DevForgeAI PRD skill
  (for example `$prd BRN-NNN` in Codex CLI) with the BRN **ID**, never a path, and name the
  BRN path separately as its input.
- **It is absent or unavailable:** say this Codex package does not provide the PRD workflow.
  Once the DevForgeAI Codex PRD skill is supplied and available, it can take this BRN's ID.
  Do not imply that a Claude command or an unrelated installed `prd` skill is equivalent.

For example: "Next step: this Codex package does not provide the PRD workflow yet. Once the
DevForgeAI Codex PRD skill is available, use it with `BRN-001`; the input is
`docs/specs/brainstorm/BRN-001.md`."

Do not start writing a PRD.

## Output contract

- **Path:** `docs/specs/brainstorm/BRN-NNN.md` in the current project; the name is the ID only.
- **Shape:** the template `assets/brainstorm.md`, with every heading kept and
  no author comments.
- **Data:** only the `problems`, `ideas` and `assumptions` collections with their defined fields
  ([output-rules.md](references/output-rules.md)).
- **Decisions:** dispositions and `status: converged` appear only when the user confirmed them.

## Examples

**Named topic, user answers.** User: "Let's brainstorm how our dental clinic could cut no-shows."
1. The skill asks up to three questions (trigger, who is affected, constraints) and picks
   `diverge-converge`, saying why.
2. It captures 3 problems, 10 ideas (two in the user's own words) and 4 assumptions, and
   rates them.
3. It proposes promote IDEA-01 and IDEA-04, park 3 ideas and reject 1. The user confirms all
   but one, which they change to parked, and says the brainstorm is done.
4. It writes `docs/specs/brainstorm/BRN-001.md` with those dispositions and `status: converged`.
5. The validator prints OK, and the skill reports and hands off.

**User says to proceed without questions.** The skill asks nothing and records unknowns as
`[NEEDS CLARIFICATION]`. It writes every idea with `disposition: open` and `status: draft`, and
puts its proposals in section 6. It asks the user to confirm them in the final reply.

**A BRN on the topic already exists.** The skill shows it and asks: extend it or create a new
one. It writes nothing until the user answers.

## References

- [references/frameworks/INDEX.md](references/frameworks/INDEX.md): read at step 2 to choose a
  framework. It links to each framework file.
- [references/output-rules.md](references/output-rules.md): read before step 6.
- `scripts/validate_brn.py`: run at step 7; it applies the output rules mechanically.
