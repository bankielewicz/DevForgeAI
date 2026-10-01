# Runbook: SKL-010 (context skill) — evaluation and manual checks

Covers what the build session can't run for the context skill (SKL-010 v2, SPEC-011 v3), built on
branch `feat/spec-011-context-skill`:
- section 1: the paid `claude plugin eval` runs (§11 step 8);
- section 2: setup for the manual checks;
- section 3: the plugin checklist (the deployed copy loads and triggers);
- section 4: VER-21 (a) to (j), interactive;
- section 5: VER-22 (a) to (c), validation failure and can't-run;
- section 6: results.

Every item stays **NOT_RUN** until someone runs it. Record each result in section 6: **pass**,
**fail** (with what happened), or **not run** (with why). A failure stays a failure: if a grader or a
fixture turns out to be wrong, show it with controls first, and keep the old result on record.

Paste each command on its own. None starts with `!`, and none uses a `\` continuation or a heredoc.

## 1. Evaluation (plain terminal, not inside Claude)

From the worktree root, on a committed, clean tree. Each call binds a new results folder first.

```bash
cd ~/Projects/DevForgeAI/.claude/worktrees/spec-011-context
bash tmp/run-context-evals.sh pilot
bash tmp/run-context-evals.sh triggers
bash tmp/run-context-evals.sh full
```

- **pilot:** writes-the-set once on the default model, haiku, sonnet and opus (§13: it must pass on
  sonnet and opus). It measures cost, turns and duration, and confirms that
  `context_check.py snapshot new` can write under the harness's `$TMPDIR`.
  (The baseline already confirmed that a whole-file regex works at an ARCH's size.)
- **triggers:** the 12 trigger cases, 3 runs each, on haiku, sonnet and opus. QR-04 requires 3 of 3 on
  every case on sonnet and opus; haiku is reported.
- **full:** the 18 cases (`--tag context`), 3 runs with the baseline arm, only after the cost estimate
  from the pilot is approved.

After each run, check every case's `error` field in `aggregate-result.json`, and look for a
`not granted` line, before trusting any score. Grader checks already ran offline:
`src/tests/context/check_graders.py`.

## 2. Setup (once per shell)

```bash
WT=~/Projects/DevForgeAI/.claude/worktrees/spec-011-context
T=/tmp/context-test
rm -rf "$T" && mkdir -p "$T" && cp -r "$WT/src/claude/DevForgeAI" "$T/plugin"
E="$T/plugin/evals/context"
fresh() { rm -rf "$T/ws" && mkdir "$T/ws" && cd "$T/ws" && bash "$E/$1/scaffold.sh"; }
MF="$WT/src/tests/context/manual/make_fixtures.py"
L=.claude/devforgeai.local.md
built() { rm -rf "$T/ws" && python3 "$MF" "$1" "$T/ws" && cd "$T/ws"; }
```

`fresh <case>` makes an empty project in `$T/ws` with that eval case's fixtures; `built <kind>` does
the same with a manual fixture (`make_fixtures.py` lists the kinds). The project sits outside the
repository, so the session doesn't load the repository's `CLAUDE.md` or deployed plugin. Start Claude
from `$T/ws` with the copied plugin, and restart between tests (`/exit`, then the setup line again):

```bash
claude --plugin-dir "$T/plugin"
```

Your `~/.claude/CLAUDE.md` still loads; remove any papercut entries the deliberate failures below
cause. Each run leaves its snapshots in `$TMPDIR` or `/tmp` (`devforgeai-context-*`); the reply names
the folder.

## 3. The plugin checklist

Deploy first, from a plain shell in the worktree root:

```bash
rsync -a --delete --exclude=/evals/results/ src/claude/DevForgeAI/ .claude/skills/devforgeai/
diff -r -x results src/claude/DevForgeAI .claude/skills/devforgeai && echo deployed
claude plugin validate .claude/skills/devforgeai --strict
```

Then start `claude` in the worktree root and run `/reload-plugins` if a session was open.

- **P1.** `/plugin` lists `devforgeai` from `.claude/skills/devforgeai` at version 0.8.0, and
  `/skills` lists `context`.
- **P2.** Typing `/devforgeai:` offers `/devforgeai:context` with the hint `[document]`.
- **P3.** In `fresh trigger-01`'s project (no ARCH), "Refresh the project context after the
  architecture change." invokes the skill (the reply hands back to `/devforgeai:architecture`).
- **P4.** In the same project, "Explain how React's Context API works." doesn't invoke it.

## 4. VER-21: interactive checks

### M-a. Batches, options and the budget (VER-21 a; BEH-07)

```bash
fresh writes-the-set
mkdir -p .claude && printf -- '---\ndevforgeai_local: 1\ninterview.max_calls: 3\n---\n' > $L
```

Say: "Write the project context documents." Answer the first call's questions, then pick "Leave it as
a proposal" for the rest. **Expect:**
- the first call asks the scope question (which paths may be read); the freshness question is asked
  once; both count toward the budget;
- every call has at most 4 questions, each with 2 to 4 options, the recommended one first and marked
  "(Recommended)", and a section question offers "Leave it as a proposal" and "This needs an
  architecture decision (ADR)";
- after 3 calls nothing more is asked; every unasked section is a Proposed statement with
  `[NEEDS CLARIFICATION: confirm …]`;
- the resolution line starts `interview.max_calls=3 (local)`.

### M-b. Stopping mid-interview (VER-21 b; ERR-09)

`fresh writes-the-set`. Say: "Write the project context documents." After the first question call,
say "Stop here, I have to go." **Expect:** it offers to write the documents with every unanswered
section as a Proposed statement or marker. Answer "No": nothing is written under
`docs/specs/context/`, and it says to run the skill again to resume. Repeat, answering "Yes": draft
documents with markers.

### M-c. Reading outside the scope (VER-21 c; ERR-06)

```bash
fresh observed-and-confirmed
mkdir -p shared && printf 'LEVEL = "INFO"\n' > shared/config.py
printf 'from shared.config import LEVEL\n' >> src/shiftlog/cli/main.py
```

Say: "Write the project context documents. You may read src/shiftlog/ only." **Expect:** before
reading `shared/config.py` it asks. Answer "No": the file is never read (check the tool calls), and the
affected statement is `[NEEDS CLARIFICATION: shared/config.py is outside the inspection scope]`.

### M-d. Items over 500 lines (VER-21 d; ERR-12)

`built many-items`. Say: "Write the project context documents. You may read pyproject.toml; every
package it declares is our convention, at the range it declares. Proceed without questions."
**Expect:** tech-stack.md is not written; the reply says how many items there are and asks how to
proceed; the other documents are written; no item lands in a detail file.

### M-e. Detail files (VER-21 e; BEH-09)

`built long-doc` (front-end.md approved, 494 lines). Say: "Update only front-end.md: in section 4, add
these conventions: `list` sorts newest first; `week` accepts `--from`; `stop` refuses a stopped shift;
`start` refuses a running shift; `--json` output is UTF-8; errors go to standard error; `--quiet`
prints nothing on success; `--help` lists every flag; dates print as YYYY-MM-DD; durations print as
H:MM. Proceed without questions." **Expect:**
- front-end.md is version 2, draft, within 500 lines, starts with `## Contents`, and section 6 (and
  only as many sections as needed) moved into `docs/specs/context/front-end/<topic>.md`, each linked
  with one `- [<topic>](front-end/<topic>.md): read when <condition>.` line;
- each detail file starts `> Part of CTX-011 (front-end.md), version 2.`, has no frontmatter and no
  items, stays within 500 lines, and links no detail file;
- index.md's row shows version 2, and the reply's check lines end `OK`.

### M-f. A draft ARCH (VER-21 f; BEH-02)

```bash
fresh writes-the-set
sed -i 's/^status: approved/status: draft/' docs/specs/arch/ARCH-001.md
```

Say: "Write the project context documents. Proceed without questions." **Expect:** every document's
Change Log row, and the report, say the documents are proposals because ARCH-001 isn't approved.

### M-g. Approval without a named approver (VER-21 g; BEH-17)

`fresh writes-the-set`. Say: "Write the project context documents. I confirm Typer 0.12.x for the
shiftlog CLI; Alembic 1.13.x for the Local database; pytest 8.x for every component; and dependency
updates go in their own pull request. Don't inspect any code. Approve tech-stack.md." Answer the
interview with "Leave it as a proposal". **Expect:** it asks who is approving, with "Example Owner" (the
owner) first. Answer "Example Owner": tech-stack.md is approved by Example Owner, with an `Approved`
row by Example Owner, and every other document stays draft. Repeat, and stop instead of answering:
nothing is approved, and the reply says the approver wasn't named.

### M-h. Local preferences (VER-21 h; BEH-03)

```bash
fresh writes-the-set
mkdir -p .claude && printf -- '---\ndevforgeai_local: 1\ninterview.max_calls: 4\n---\n' > $L
```

Say: "Write the project context documents. Proceed without questions." **Expect:** the resolution
line in every Change Log row and in the report starts `interview.max_calls=4 (local)`.

### M-i. A stale PRD link (VER-21 i; §4)

```bash
fresh writes-the-set
sed -i 's/^version: 1$/version: 2/' docs/specs/prd/PRD-001.md
```

Say: "Write the project context documents. Proceed without questions." **Expect:** the reply reports
that ARCH-001 links PRD-001 version 1 while version 2 is on disk; no NFR is cited; the resolution line
has `operating context unknown, resolved as production`; PRD-001 is unchanged.

### M-j. "This needs an architecture decision" (VER-21 j; BEH-06, ERR-07)

`fresh writes-the-set`. Say: "Write the project context documents. Don't inspect any code." To one
section's question (for example architecture.md's configuration), answer "This needs an architecture
decision (ADR)"; leave the rest as proposals. **Expect:** that section holds one
`[NEEDS ADR: …]` marker and no convention; the report lists it under "Handed back to architecture";
the next step tells the user to run `/devforgeai:architecture PRD-001`.

## 5. VER-22: validation failure and can't-run

### H-a. Every repair corrupted again (VER-22 a; BEH-18, ERR-08)

`built hooks-every` (the example project, with a PostToolUse hook that sets `type: contxt` in
tech-stack.md after every Edit of it). Say: "Update the context documents: in tech-stack.md, add the
convention that the lock file is committed with every dependency change. Proceed without questions."
**Expect:**
- check 1 reports tech-stack.md's `type`; each repair is corrupted again (`.claude/corrupt.log`); after
  at most four checks the run ends with the validation-failure report, with no report block and no
  next step;
- `context_check.py restore` printed `restored docs/specs/context/tech-stack.md`; its SHA-256 equals
  the snapshot's: compare `sha256sum docs/specs/context/tech-stack.md` with the line in
  `<start>/MANIFEST.sha256` (the reply names `<start>`);
- documents that pass keep their changes; index.md lists tech-stack.md at the version it has after the
  restore; no document is presented as approved.

### H-b. An approval rolled back (VER-22 b; BEH-17)

`built hooks-approval` (the shared fixture, with the hook firing only after an Edit that sets
`status: approved` in tech-stack.md). Say: "Write the project context documents. I confirm Typer 0.12.x
for the shiftlog CLI; Alembic 1.13.x for the Local database; pytest 8.x for every component; and
dependency updates go in their own pull request. None of these is hard to reverse or shared by several
epics. Don't inspect any code. Proceed without questions. I'm Example Owner, and I approve
tech-stack.md." **Expect:** the check after the approval fails; `restore <run folder>/pre-approval
docs/specs/context/tech-stack.md` prints `restored`; the reply reports tech-stack.md as not approved,
with the error; tech-stack.md is draft with `approved_by: ""`, and its SHA-256 equals the pre-approval
snapshot's.

### H-c. Policy or the context check can't run (VER-22 c; ERR-03, ERR-13)

1. The policy script can't run, with approved policy:

   ```bash
   fresh testing-policy-cited
   mv "$T/plugin/skills/context/references/schemas/policy.schema.json" "$T/policy.off"
   ```

   Say: "Write the project context documents. Proceed without questions." **Expect:** it stops
   before writing (ERR-03), quoting the script's `Cannot run:` line; no `docs/specs/context/`. Then
   `mv "$T/policy.off" "$T/plugin/skills/context/references/schemas/policy.schema.json"`.
2. The context check can't run:

   ```bash
   fresh writes-the-set
   mv "$T/plugin/skills/context/references/schemas/context.schema.json" "$T/context.off"
   ```

   Same request. **Expect:** it stops before writing (ERR-13), quoting
   `Cannot run: the schema copy context.schema.json is missing or unreadable (…).`; no
   `docs/specs/context/`. Then move the file back.

## 6. Results

| Item | Result | Date | Notes |
|---|---|---|---|
| Eval: baseline (writes-the-set, nothing-confirmed, needs-adr-handback) | recorded: 0.15, 0.06, 0.07 without the skill | 2026-10-01 | `context-baseline-*-20261001T13*`, `95145a1`; $1.02 |
| Eval: pilot | NOT_RUN | | |
| Eval: triggers (haiku, sonnet, opus) | NOT_RUN | | |
| Eval: full, 3 runs with baseline | NOT_RUN | | |
| P1–P4 plugin checklist | NOT_RUN | | |
| M-a VER-21 (a) batches and budget | NOT_RUN | | |
| M-b VER-21 (b) stopping | NOT_RUN | | |
| M-c VER-21 (c) outside the scope | NOT_RUN | | |
| M-d VER-21 (d) items over 500 lines | NOT_RUN | | |
| M-e VER-21 (e) detail files | NOT_RUN | | |
| M-f VER-21 (f) draft ARCH | NOT_RUN | | |
| M-g VER-21 (g) approver not named | NOT_RUN | | |
| M-h VER-21 (h) local preferences | NOT_RUN | | |
| M-i VER-21 (i) stale PRD link | NOT_RUN | | |
| M-j VER-21 (j) ADR answer | NOT_RUN | | |
| H-a VER-22 (a) repairs corrupted, restore | NOT_RUN | | |
| H-b VER-22 (b) approval rollback | NOT_RUN | | |
| H-c VER-22 (c) can't run | NOT_RUN | | |
