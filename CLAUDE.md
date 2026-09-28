# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

`AGENTS.md` (also loaded) covers document formatting, ID stability and naming. This file covers what
it lacks: where things really are, how the plugin is evaluated, and the traps.

## What this workspace is

DevForgeAI is a Claude Code plugin, `devforgeai`, of spec-driven planning skills for the chain
Brainstorm → PRD → Architecture Definition (ARCH + ADRs) → Epic → Story → Spec. Each skill implements
an approved spec in `docs/specs/`, and its eval suite, not a reading of its instructions, is the proof.

| Skill | Spec | State here |
|---|---|---|
| `brainstorm` (SKL-001 v5) | SPEC-001 v10 | Built, with 8 eval cases |
| `prd` (SKL-002 v1) | SPEC-002 v1 | Built and deployed, with 20 eval cases; manual VER-11, VER-12 and VER-23 not run |
| `architecture` | SPEC-003 v1 | Approved spec only |
| `epic` | SPEC-004 v1 | Approved spec only |
| `documents-updater` (SKL-005 v1) | SPEC-006 v1 | Built and deployed, with 8 eval cases (3 runs: 8 of 8 at 1.00, mean Δ +0.15); manual VER-10..12 not run. Outside the chain: it updates a repository's README, CHANGELOG and guides from git evidence |
| `git` (SKL-006, proposed) | SPEC-007 v1 (draft) | Draft spec only, no open questions; awaiting approval. Outside the chain: `/devforgeai:git <phase>` for worktree, commit, push, PR, merge (an independent QA session's verdict for the head commit and `merge-approved` label, plus the owner's authorization), safe sync and prune |
| `qa` (SKL-007, reserved) | SPEC-008 v1 (stub) | Stub spec only: the contract SPEC-007 reads (verdict comment naming the reviewed SHA, `merge-approved`/`qa-failed` labels) is fixed; the review criteria are open. Meant to approve PRs from an independent session. Until built, QA follows SPEC-008 §4 by hand |

SKL-003 and SKL-004 are reserved for `architecture` and `epic` by their specs, and SKL-007 for `qa` by SPEC-008.

There is no build system or linter; the checks that exist are under Commands. The workspace is a git
repository (remote `origin`), but most files are untracked, so git history doesn't show how the specs
or the plugin evolved; each spec's Change Log does.
Every document uses the typed folders described in `AGENTS.md` (`docs/specs/spec/SPEC-002.md`,
`docs/specs/prd/PRD-002.md`). `docs/research/Claude/` holds saved Claude Code docs whose links point
to code.claude.com; it and the skills-guide PDF in `docs/` are local only (`.gitignore`). `src/codex/devforgeai/` is a Codex port of the brainstorm skill, built and kept by
Codex sessions (`IMPORT-REPORT.md` there lists its differences); don't edit it from Claude.
`src/grok/` is empty.

## Commands

Run from the repository root (see "Traps").

```bash
# Check a brainstorm document against the skill's output rules
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md
# Session-archive tests: all, or one by name
python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py'
python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py' -k test_scope_is_opt_in
# The Codex port's validator tests, leaving no __pycache__ in the Codex tree
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py'
# documents-updater's Markdown checker: its tests (kept outside the plugin), or a run on files
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/tests/documents-updater -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 src/claude/DevForgeAI/skills/documents-updater/scripts/check_docs.py README.md
# documents-updater evals: regenerate every case from its generator; check one case's regex graders offline
python3 src/tests/documents-updater/make_evals.py
node src/tests/documents-updater/grade_evals.mjs src/claude/DevForgeAI/evals/documents-updater/<case> <workspace> <reply.txt>
# Plugin evals (plain terminal only, see "Evaluating a skill"): one skill's suite, or one case cheaply
claude plugin eval src/claude/DevForgeAI --tag prd --allow-tools Write Edit Bash --scaffold \
  --judge-model sonnet --threshold 0.8 -j 4 --output-dir tmp/eval-results/$(date +%Y%m%dT%H%M%S)
claude plugin eval src/claude/DevForgeAI --case writes-valid-brn --runs 1 --ablation none \
  --allow-tools Write Edit Bash --scaffold --judge-model sonnet --output-dir tmp/eval-results/quick
# The deployed copy matches the source
diff -rq src/claude/DevForgeAI .claude/skills/devforgeai
```

## Spec paths vs. disk

The specs were written against another repository's layout. Most of their paths now match this
workspace; translate the rest before using them:

| Specs say | Here |
|---|---|
| `src/claude/DevForgeAI/` (plugin source) | The same. It deploys to `.claude/skills/devforgeai/` (below) |
| `src/staging/templates/` | `src/templates/` |
| `src/staging/examples/` | The same: `policy-two-orgs/` and `prd-production-mvp/`, copied unchanged from DevForgeAI-SDF2 (`ef78b83`) on 2026-09-27 |
| `src/schemas/`, `schemas/*.schema.json` | `src/schemas/`. No skill reads a schema at run time: each skill's `references/output-rules.md` (and brainstorm's validator script) is its validation contract |
| PRD-001, STORY-001..005, ADR-001..003 | ADR-001..003, PRD-001 and STORY-002 are in `docs/specs/adr/`, `prd/` and `story/`, copied unchanged from DevForgeAI-SDF2 (`ef78b83`) on 2026-09-27. STORY-001, STORY-003..005 and the epics they cite are absent. ADR-001's worktree process assumes git history, which this workspace mostly lacks (most files are untracked) |
| `devforgeai check` ("the checker") | Does not exist. SPEC-004 §2: never trust anything named `devforgeai` on PATH |

## Source and deployed copy

- `src/claude/DevForgeAI/` is the source. Edit only here.
- `.claude/skills/devforgeai/` is a byte-identical deployed copy, gitignored: after a fresh clone, run
  the deploy command below once. The names differ on purpose: a
  skills-dir plugin must sit at `.claude/skills/<name>/`, and the plugin's name is `devforgeai`.
  Claude Code loads it in this directory, which is where `/devforgeai:brainstorm` comes from, so
  edits to `src/` take effect only after redeploying. Claude's sandbox denies writes to `.claude/skills/`, and the deploy
  procedure (ADR-001) is not in this workspace: redeploying is the owner's step.
- Deploy (owner, from a plain shell): `rsync -a --delete --exclude __pycache__ --exclude results src/claude/DevForgeAI/ .claude/skills/devforgeai/`.
  `--delete` also clears stray files such as Windows `*:Zone.Identifier` copies and sandbox placeholders.
- `src/tools/session-archive/` is not part of the plugin and is never synced into `.claude/`. It
  holds user-level hooks that archive session transcripts and record which session wrote each
  `docs/specs/` document. The owner installs them into `~/.claude/` per `docs/specs/spec/SPEC-005.md`
  (draft).

## Evaluating a skill

Run evals from a plain terminal, not inside a Claude session (SPEC-004 §2, citing ADR-001). The
suite command is under Commands.

- `--allow-tools Write Edit Bash`: every case lists these gated tools in `allowed_tools`; Bash runs
  brainstorm's validator script.
- `--scaffold`: runs `case.yaml` scaffold scripts. Brainstorm's `existing-brn` and every prd case but
  `ignores-unrelated-request` have one; they seed the BRNs, PRDs, ADRs and policies the case reads.
  Every documents-updater case has one that builds a small git repository with dated commits. Those
  cases are generated by `src/tests/documents-updater/make_evals.py`: edit fixtures and graders
  there and regenerate, never the case files.
- `--threshold 0.8`: the default is 1.0. The framework bar is ≥ 0.8 per case over 3 runs, the default run count.
- Narrow a run with `--case existing-brn`, `--tag brainstorm` or `--tag prd`. `ver-NN` tags repeat across
  skills (both have a `ver-08`). Use `--runs 1` for a quick pass.
- A no-plugin baseline arm runs by default. `tool_used: Skill` graders then only indicate that the plugin fired and don't count toward the score.
- The HTML report publishes to claude.ai by default when the account supports it; add `--no-publish`
  to keep it local. Without `--output-dir`, results land in the plugin's `evals/results/` and would
  deploy with it; keep them under `tmp/eval-results/`.
- Before trusting a low score, check `cases[].arms.with[].error` in `aggregate-result.json`: an
  expired login or usage limit scores 0 without being a regression.
- `--judge-model sonnet`: the default small judge failed correct replies. Even sonnet failed a correct
  8 kB PRD in 3 of 3 votes, so check claims about a written file with regex graders, and test each
  regex with `node` against a real output first.
- Run traces under `/tmp/claude-eval-*` are deleted when the run ends. `report.html` keeps what each llm
  grader saw (the reply or the file), which is usually enough to diagnose a failure. `--case` takes one
  name; loop for several.

Brainstorm's manual paths (user confirmation, the extend flow, VER-05, VER-09) follow
`docs/runbooks/brainstorm-manual-test.md`, which loads a *copy* of the plugin with
`claude --plugin-dir` and never touches `src/`. The prd skill has no runbook yet; its manual items
are SPEC-002 VER-11, VER-12 and VER-23.

## Skill anatomy (under `src/claude/DevForgeAI/`)

- `skills/<name>/SKILL.md`: the only file loaded on trigger; at most 500 lines. It holds a copyable
  checklist, the decisions that belong to the user, an output contract, and direct links to references.
- `skills/<name>/provenance.yaml`: the SKL record with an `implements` link to the spec; Claude never loads
  it. Directory name = `SKILL.md` `name` = `skill_name`. `metadata.devforgeai-id` and `devforgeai-version`
  mirror provenance `id` and `version`: bump both on any change to `SKILL.md` or its references.
- `skills/<name>/references/`: loaded on demand, one level deep. `output-rules.md` defines keys, ID
  patterns and allowed fields, and ends with the self-check list used in place of `devforgeai check`.
- `skills/<name>/scripts/`: executed, not loaded. Brainstorm's `validate_brn.py` applies the output
  rules at step 7. It can't check what the user confirmed, so step 7 also reads the file back. Keep
  `__pycache__/` out of the deployed copy. The prd skill has no script (SPEC-002 §3): step 9 reads the
  file back against the self-check list. documents-updater's `check_docs.py` checks Markdown structure
  and links at step 6; its tests live in `src/tests/documents-updater/` so they don't deploy.
- `skills/<name>/assets/<type>.md`: the canonical document template. `src/templates/brainstorm.md` is a
  leftover identical copy; edit the asset.
- `evals/<name>/<case>/`: `prompt.md`, `graders/*.md`, optional `case.yaml` + `scaffold.sh`; one case per
  automated VER item, tagged `<name>` and `ver-NN`. Runs start in an empty workspace, so the scaffold
  must seed anything the skill reads.

Brainstorm frameworks are an extension point: add a file with the six sections that
`references/frameworks/INDEX.md` requires, plus one index row. `SKILL.md` never changes.

## Rules a change must not break

- **Judgment calls are the user's.** In brainstorm, idea dispositions and convergence are written only
  when the user confirmed them. Otherwise they stay `disposition: open`, `reason: null` and `status: draft`.
  With no user present, VER-02 checks exactly this. Each later spec names its own user-owned decisions.
- Skills write documents as `docs/specs/<type>/<ID>.md` in the *user's* project and allocate the ID
  themselves. They never take a file name from the user. documents-updater is the exception: it edits
  the user's existing documentation (README, CHANGELOG, guides) in place, and `assets/` holds its
  twelve fallback templates rather than one canonical template.
- An approved document changes only with a `version` bump, a new `updated` date and two Change Log
  rows: the change, authored `claude-code (session <ID>)`, and the owner's approval. Then move every
  `upstream` link that cites it (other specs, `provenance.yaml`) to the new version. Never rewrite
  earlier Change Log rows.

## Traps

- Keep the Bash working directory at the repository root. A sandboxed command whose working
  directory is a subfolder leaves empty placeholders there (`.claude/.cc-writes/`, `.mcp.json`); remove
  them with `rmdir`, which refuses anything that isn't empty.
- Inside the sandbox, `.mcp.json` at the repository root shows as a character device (`/dev/null`,
  owned by nobody). It is the sandbox's write mask, not a file; leave it alone.
- Commands for the owner to paste into a plain shell must not start with `!`. That prefix runs a
  command only in Claude Code's prompt; in bash it negates the exit status, so `! diff … && echo ok`
  reports success when the copies differ.

## Building the next skill

Follow the implementing spec's §11, translating paths as above:
1. Copy `src/templates/skill/` and fill it in before it reaches a loaded skills directory.
2. Write `SKILL.md` from spec §5–§7, and `provenance.yaml` with the next SKL ID.
3. Move the document template from `src/templates/` into `assets/`, and update the templates README row.
4. Write `references/output-rules.md`.
5. Write one eval case per automated VER item.
6. Evaluate the source directly (no deploy needed) until every case scores ≥ 0.8, cheapest first:
   a few cases with `--runs 1 --ablation none`, then the whole suite with `--runs 1`, then 3 runs with
   the baseline. For prd's 20 cases the last two cost about $8 and $41. Then deploy, and do the manual
   VER items by hand.

When `architecture` ships, the prd `hands-off-to-architecture` graders still expect the "not built
yet" handoff. SPEC-002 VER-07 describes the shipped branch: `/devforgeai:architecture PRD-001`, with the
ID, never a path. Flip them in the same change, as the brainstorm `hands-off-to-prd` case was flipped when
`prd` shipped. The architecture skill copies the prd skill's `references/policy.md` and `defaults.md`
byte-identical (SPEC-003 §3), so both are written skill-neutral; change them in both skills together.

The planning chain's last skill, whichever that turns out to be, ends its Next step by recommending
`/devforgeai:documents-updater` (SPEC-006 §13, decided by Bryan on 2026-09-28). Put that in its spec
and give it an eval grader. The `git` skill also recommends it before opening a PR whose branch
changes neither README nor CHANGELOG (SPEC-007 BEH-19, decided by Bryan on 2026-09-28), and runs it
only on the user's yes. No other skill hands off to documents-updater, and documents-updater never
starts itself.

`src/schemas/spec.schema.json` requires a VER item's `upstream` only when the spec specifies a story.
A spec derived from another document, such as SPEC-005 or SPEC-006, may leave it out.
