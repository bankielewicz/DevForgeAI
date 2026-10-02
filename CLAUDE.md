# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

This file covers where things really are, how the plugin is evaluated, and the traps. Detail needed
for only one kind of work is in `.claude/rules/` and `AGENTS.md` (see "Loaded on demand" at the end).

## What this workspace is

DevForgeAI is a Claude Code plugin, `devforgeai`, of spec-driven planning skills for the chain
Brainstorm → PRD → Architecture Definition (ARCH + ADRs) → Epic → Story → Spec. Each skill implements
an approved spec in `docs/specs/`, and its eval suite, not a reading of its instructions, is the proof.
Each spec's §9 table records its eval runs (scores, cost, bound commit) and which manual VER items ran.

| Skill | Record | Spec | State |
|---|---|---|---|
| `brainstorm` | SKL-001 v5 | SPEC-001 v10 | Built; 8 eval cases |
| `prd` | SKL-002 v5, approved | SPEC-002 v5, approved 2026-10-01 (issue #39, the `[NEEDS ADR]` rule) | SKL-002 v5 (plugin 0.11.0) requalified 2026-10-02: 35 of 35 at ≥ 0.8 over 3 runs, 34 at 1.00 (mean Δ +0.57); approved by Bryan 2026-10-02; merged in PR #57 (`0011267`) and deployed (0.11.0) 2026-10-02. 35 eval cases; VER-37 (`needs-adr-handoff`) and VER-38 (`unlinked-signal-keeps-target`) are new and failed on v4 |
| `architecture` | SKL-003 v6, approved | SPEC-003 v5, approved 2026-10-01 | Approved by Bryan 2026-10-01; merged in PR #54, deployed (0.10.0); 21 eval cases, 3-run 21 of 21 at 1.00 (mean Δ +0.63); manual VER-12 (a), (f), (i), (j), (k), (l), VER-19 and VER-20 pass (runbook `docs/runbooks/architecture-v6-checks.md`) |
| `epic` | SKL-004 v4, approved | SPEC-004 v4, approved 2026-10-01 | SKL-004 v4 (plugin 0.12.1) qualified 2026-10-02: 25 of 25 at ≥ 0.8 over 3 runs, 23 at 1.00 (mean Δ +0.58); approved by Bryan 2026-10-02, not merged or deployed. SKL-004 v3 (SPEC-004 v3) is approved, merged in PR #47 and deployed (0.8.1). 25 eval cases; VER-20 to VER-26 are new (failed on v3 as predicted); offline grader check `src/tests/epic/check_graders.py`; VER-13 not run (runbook `docs/runbooks/epic-ver-13-checks.md`; (k) automated by VER-20) |
| `documents-updater` | SKL-005 v1 | SPEC-006 v1 | Built and deployed; 8 eval cases |
| `git` | SKL-006 v3, in-review | SPEC-007 v3, in-review | v3 prepared with ERR-04 routing, all-branch carry checks and marked Compose password warnings; native/manual qualification pending (`docs/runbooks/git-v3-checks.md`). v2 remains approved and deployed; its 3-run 19 of 19 at ≥ 0.8 qualifies v2 only |
| `qa` | SKL-007, reserved | SPEC-008 v1, stub | Not built; until it is, QA follows SPEC-008 §4 by hand |
| `github-post` | SKL-009, reserved | SPEC-010 v3, in-review (v2 approved 2026-09-30) | v3 refreshes the SPEC-007 citation only; approval pending. Not built; its §11 lists the build steps |
| `context` | SKL-010 v2, approved | SPEC-011 v3, approved 2026-10-01 | Approved by Bryan 2026-10-01; merged in PR #45 (plugin 0.8.1), deployed (0.9.0); v1 merged in PR #34. 18 eval cases and 12 trigger cases: full suite 18 of 18 at ≥ 0.8 over 3 runs, triggers 3 of 3 on Sonnet and Opus; manual VER-21 and VER-22 not run (`docs/runbooks/spec-011-manual-checks.md`) |

SKL-008 is reserved for the story skill (SPEC-009).

- Outside the chain: `documents-updater` updates a repository's README, CHANGELOG and guides from git
  evidence. `git` (`/devforgeai:git <phase>`) covers worktree, commit, push, PR, merge (only with an
  independent QA session's verdict for the head commit, the `merge-approved` label and the owner's
  authorization), safe sync and prune. `github-post` (`/devforgeai:github-post [PR|Incident|Enhancement]`)
  will write a GitHub post that a reader with no context can act on, check its references and quotes,
  and post it with `gh` when authorized; it never commits, pushes or merges. Its templates are staged
  in `src/templates/github/`.
- `git` v1's results (also in SPEC-007 §9): 3 scripts (57 unit tests) and 16 eval cases; 3 runs: 16 of
  16 at ≥ 0.8, 13 at 1.00, mean Δ +0.28, $18.22 (the misses are the eval's own `.git` write
  refusals, which the skill reports). v2 (SPEC-007 §9): 76 unit tests, `src/tests/git/test_structure.py`
  and 19 eval cases; 3 runs: 19 of 19 at ≥ 0.8, 16 at 1.00, mean Δ +0.32, $22.96. Its misses: the
  same two harness refusals (`starts-worktree-from-fresh-base` can't exceed 0.88), and
  `stops-on-unrelated-histories` recommending a merge of the histories instead of ERR-04's new branch
  in 2 of 3 runs. Manual VER-18..22, VER-24, VER-26 and VER-31 not run
  (`docs/runbooks/git-v2-checks.md`).
- `git` v3's local checks, new VER-32..35 cases and remaining qualification are recorded separately
  in `docs/runbooks/git-v3-checks.md`. The candidate plugin is 0.10.1; native evaluation, manual
  checks, owner approval and deployment are pending. Retain v2's failures and results above.
- `progress/` (plugin 0.12.0; SPEC-012 approved, ADR-006 accepted) is the progress tracker's core, not a skill:
  `evaluate.py` (standard library only) judges a skill run's checklist steps by evidence from an event
  log, with the schemas and the brainstorm and architecture manifests. Its tests are in `src/tests/progress/`;
  SPEC-012 §9 lists the build's departures for Bryan. No Claude Code adapter calls it yet.
- `qa`'s stub fixes only the contract SPEC-007 reads: a verdict comment naming the reviewed SHA, and
  the `merge-approved`/`qa-failed` labels. The review criteria are open.

There is no build system or linter; the checks that exist are under Commands. The workspace is a git
repository (remote `origin`). Everything was imported in one commit (PR #1, 2026-09-28), so git
history doesn't show how the specs or the plugin evolved before then; each spec's Change Log does.
Specs were written against another repository's layout: translate their paths with
`.claude/rules/spec-paths.md`. `docs/research/Claude/` (saved Claude Code docs) and the skills-guide
PDF in `docs/` are local only. `src/codex/devforgeai/` is the Codex port (its manifest and README say
which skills it holds), built and kept by Codex sessions; its `*IMPORT-REPORT.md` files list the
differences from the Claude skills. Don't edit it from Claude. `src/grok/` is empty.

## Source and deployed copy

- `src/claude/DevForgeAI/` is the source. Edit only here.
- `.claude/skills/devforgeai/` is a byte-identical deployed copy, gitignored: after a fresh clone, run
  the deploy command below once. The names differ on purpose: a skills-dir plugin must sit at
  `.claude/skills/<name>/`, and the plugin's name is `devforgeai`. Claude Code loads it there, which
  is where `/devforgeai:brainstorm` comes from, so edits to `src/` take effect only after redeploying.
  Claude's sandbox denies writes to `.claude/skills/`, in the main checkout and in every worktree, so
  deploying (ADR-001 steps 2 and 7) is the owner's step, from a plain shell. `--delete` also clears
  stray files such as Windows `*:Zone.Identifier` copies and sandbox placeholders.
- `.codex/devforgeai/` is the deployed Codex copy. All of `.codex/` is gitignored, since it also holds
  local preferences such as `.codex/devforgeai.local.md`. The copy is built from the files `main`
  tracks, never the working tree, so untracked Codex work and gitignored raw eval transcripts stay out.
  The owner's local `tmp/deploy-main.sh` (ADR-001 step 7) pulls `main`, deploys both copies and diffs each.

```bash
# Deploy the Claude plugin
rsync -a --delete --exclude={__pycache__,results} src/claude/DevForgeAI/ .claude/skills/devforgeai/
# Deploy the Codex plugin from HEAD
T=$(mktemp -d) && git archive HEAD src/codex/devforgeai | tar -x -C "$T"
mkdir -p .codex/devforgeai && rsync -a --delete "$T/src/codex/devforgeai/" .codex/devforgeai/
```

- `src/tools/session-archive/` is not part of the plugin and is never synced into `.claude/`. It holds
  user-level hooks that archive session transcripts and record which session wrote each `docs/specs/`
  document. The owner installs them into `~/.claude/` per `docs/specs/spec/SPEC-005.md` (draft).

## Commands

Run from the repository root (see "Traps"). Per-skill eval generators and offline grader checks are in
`.claude/rules/evals.md`.

```bash
# The deployed copy matches the source
diff -rq src/claude/DevForgeAI .claude/skills/devforgeai
# Session-archive tests: all, or one by name
python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py'
python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py' -k test_scope_is_opt_in
# documents-updater's Markdown checker tests (kept outside the plugin), and the git skill's script tests
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/tests/documents-updater -p 'test_*.py'
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/tests/git -p 'test_*.py'
# The progress evaluator's tests (SPEC-012): every rule, the same under python3 -S, and the goldens
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
# brainstorm's validator tests: each case runs the script with PyYAML and without it (python3 -S)
python3 -B src/tests/brainstorm/test_validate_brn.py
# prd and the shared policy script: its tests, the shared files' byte-identity, structure
python3 -B src/tests/prd/test_validate_policy.py
python3 -B src/tests/prd/test_shared_files.py
python3 -B src/tests/prd/test_structure.py
# The Codex port's tests, leaving no __pycache__ in the Codex tree
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py'
# Run a skill's checker on a real file
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md
PYTHONDONTWRITEBYTECODE=1 python3 src/claude/DevForgeAI/skills/documents-updater/scripts/check_docs.py README.md
```

## Evaluating a skill

Run evals from a plain terminal, not inside a Claude session (SPEC-004 §2, citing ADR-001): give the
owner the commands. The source is evaluated directly; no deploy is needed.

```bash
P=src/claude/DevForgeAI; O=tmp/eval-results/$(date +%Y%m%dT%H%M%S)
A="--allow-tools Write Edit Bash --scaffold --judge-model sonnet"
# Bind the new results folder to the commit, plugin digest and cases (before every paid run)
bash src/tests/prd/record_revision.sh $O prd
# One skill's suite; or one case cheaply, into its own folder
claude plugin eval $P --tag prd $A --threshold 0.8 -j 4 --output-dir $O
claude plugin eval $P --case writes-valid-brn --runs 1 --ablation none $A --output-dir $O-quick
```

- The bar is ≥ 0.8 per case over 3 runs (the default run count) against the no-plugin baseline.
  Go cheapest first: a few cases with `--runs 1 --ablation none`, then the whole suite with
  `--runs 1`, then 3 runs with the baseline. For prd's 20 cases the last two cost about $8 and $41.
- `record_revision.sh <results-dir> <tag>` refuses an existing folder and uncommitted changes in
  `src/` or `docs/`, so commit first and use a new folder for every run. Keep results under
  `tmp/eval-results/`, never the plugin's `evals/results/`, which would deploy.
- Eval cases are generated: edit the generator in `src/tests/<skill>/` and regenerate, never the case
  files (brainstorm's and prd's v1 cases are hand-written).
- The eval sandbox masks `.git/config.lock` in a repository the scaffold built, as a session's
  sandbox does: `git config`, `remote add` and `push -u` fail there.
- Flags, grader pitfalls, reading results and the manual-check runbooks: `.claude/rules/evals.md`.

## Rules a change must not break

- **Judgment calls are the user's.** In brainstorm, idea dispositions and convergence are written only
  when the user confirmed them. Otherwise they stay `disposition: open`, `reason: null` and `status: draft`.
  With no user present, VER-02 checks exactly this. Each later spec names its own user-owned decisions.
- Skills write documents as `docs/specs/<type>/<ID>.md` in the *user's* project and allocate the ID
  themselves. They never take a file name from the user. documents-updater is the exception: it edits
  the user's existing documentation (README, CHANGELOG, guides) in place.
- An approved document changes only with a `version` bump, a new `updated` date and two Change Log
  rows: the change, authored `claude-code (session <ID>)`, and the owner's approval. Then move every
  `upstream` link that cites it (other specs, `provenance.yaml`) to the new version. Never rewrite
  earlier Change Log rows.
- **Hand-offs to documents-updater.** The planning chain's last skill, whichever that turns out to be,
  ends its Next step by recommending `/devforgeai:documents-updater` (SPEC-006 §13, decided by Bryan
  on 2026-09-28). Put that in its spec and give it an eval grader. The `git` skill also recommends it
  before opening a PR whose branch changes neither README nor CHANGELOG (SPEC-007 BEH-19, decided by
  Bryan on 2026-09-28), and runs it only on the user's yes. No other skill hands off to
  documents-updater, and documents-updater never starts itself.

## Traps

- Keep the Bash working directory at the repository root. A sandboxed command whose working
  directory is a subfolder leaves empty placeholders there (`.claude/.cc-writes/`, `.mcp.json`); remove
  them with `rmdir`, which refuses anything that isn't empty.
- Inside the sandbox, `.mcp.json` at the repository root shows as a character device (`/dev/null`,
  owned by nobody). It is the sandbox's write mask, not a file; leave it alone. So are the other
  character devices owned by nobody at the root and in `.claude/`: stage files by path, never `git add -A`.
- Commands for the owner to paste into a plain shell must not start with `!`. That prefix runs a
  command only in Claude Code's prompt; in bash it negates the exit status, so `! diff … && echo ok`
  reports success when the copies differ. Don't use `\` line continuations either, and keep each line
  under about 100 characters (put long flags in variables): copying from the terminal wraps lines.
- `git push` and `gh pr` run outside the sandbox (`.claude/settings.local.json`, also in worktree sessions)
  only when the command starts with them: run each as its own Bash call, and never pass `allowed_domains`,
  which runs it sandboxed through a proxy that is often down. The auto-mode classifier can still block a
  push; retry once after the owner confirms it in the conversation.
- In a worktree session, the isolation guard refuses `python3 -m unittest`, heredocs that mention git,
  and any command whose paths contain `git` in a form it can't verify (such as `skills/git/`). Run test
  files directly (`python3 -B src/tests/git/test_repo_state.py`), and write scratch scripts with the
  Write tool before running them.
- **Never investigate a failing test by changing the working tree** (ADR-005 D7; interim, until the
  dev skill implements it). Record a baseline test run before the first change; compare old code only
  in a disposable worktree (`git worktree add --detach <path> <commit>`) or with
  `git show <commit>:<path>`; commit work in progress before each full test run. Never restore, check
  out, stash, reset, clean or re-download files into the working tree to investigate.

## Loaded on demand

A rule loads by itself when Claude reads a file matching its `paths:` with the Read tool. Reading
through Bash (`cat`, `sed`, `grep`) doesn't trigger it, so read the rule first when you work that way.
Claude Code doesn't load `AGENTS.md` in a project that has a CLAUDE.md; read it when the table says.

| File | Loads with | Read it before |
|---|---|---|
| `AGENTS.md` | never by itself | writing or changing a document or template (format, IDs, naming), or a commit or PR. Its "Agent-Specific Instructions" are Codex's: Claude logs papercuts per the user's own CLAUDE.md |
| `.claude/rules/spec-paths.md` | `docs/specs/**`, `src/schemas/**` | following a path, file or tool a spec names |
| `.claude/rules/evals.md` | `src/claude/DevForgeAI/evals/**`, `src/tests/**`, `tmp/eval-results/**` | writing, generating, running or diagnosing an eval |
| `.claude/rules/skills.md` | `src/claude/DevForgeAI/skills/**`, `src/claude/DevForgeAI/.claude-plugin/**`, `src/templates/**` | changing a skill, its shared files or hand-offs, or building the next skill |
