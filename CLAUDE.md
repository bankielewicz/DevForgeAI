# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

It holds what every session needs: what is built, where the source is, the commands, the rules and the
traps. Detail for one kind of work is in `.claude/rules/` and `AGENTS.md` ("Loaded on demand", at the
end). Everything here is the state of `main`, except "Future roadmap", which lists recorded, undecided
work.

## What this workspace is

DevForgeAI is a Claude Code plugin, `devforgeai` (version 0.27.0 in
`src/claude/DevForgeAI/.claude-plugin/plugin.json`), of spec-driven planning skills for the chain
Brainstorm → PRD → Architecture Definition (ARCH + ADRs) → Epic → Story → Spec. Brainstorm, PRD,
Architecture and Epic are built; `context` writes the project context documents between Architecture
and Story. Each skill implements an approved or in-review spec in `docs/specs/spec/`, and its eval
suite is the evidence that it works. Each spec's §9 holds the build and eval record (results folders,
bound commit, scores, cost, manual VER items run and not run); its §13 holds open questions; its
Change Log holds the history. Read those, not this file, for any number or date.

| Skill | Record (provenance) | Spec | Evals on the current version | Merged |
|---|---|---|---|---|
| `brainstorm` | SKL-001 v10, in-review | SPEC-001 v17, approved | v10: 1 run, 9 of 10 at 1.00, saves-work-as-it-goes 0.78 (its tool clause waived for the merge by Bryan; SPEC-001 §13) | PR #99 (0.27.0) |
| `prd` | SKL-002 v5, approved | SPEC-002 v5, approved | 3 runs, 35 of 35 at ≥ 0.8 | PR #57 (0.11.0) |
| `architecture` | SKL-003 v9, approved | SPEC-003 v11, approved | 1 run, 24 of 24; 3-run qualification waived by Bryan | PR #83 (0.21.0) |
| `epic` | SKL-004 v4, approved | SPEC-004 v4, approved | 3 runs, 25 of 25 at ≥ 0.8 | PR #62 (0.12.1) |
| `context` | SKL-010 v2, approved | SPEC-011 v3, approved | 3 runs, 18 of 18 at ≥ 0.8 | PR #45 (0.8.1) |
| `documents-updater` | SKL-005 v1, draft | SPEC-006 v1, approved | 1 run, 8 of 8 at 1.00 | PR #1 (0.2.0) |
| `git` | SKL-006 v3, in-review | SPEC-007 v3, in-review | v3: not run. v2 (approved): 3 runs, 19 of 19 at ≥ 0.8 | PR #56 (0.10.1) |
| `spec-lookup` | SKL-011 v1, approved | SPEC-014 v3, approved | 3 runs, 4 of 4 at 1.00 | PR #75 (0.19.0) |
| `precompact` | SKL-012 v1, approved | SPEC-015 v2, approved | 1 run, 12 of 12 at 1.00; 3-run qualification waived by Bryan | PR #93 (0.26.0) |
| `qa` | SKL-007, reserved | SPEC-008 v1, draft stub | not built | — |
| `story` | SKL-008, reserved | SPEC-009 v2, draft | not built | — |
| `github-post` | SKL-009, reserved | SPEC-010 v3, in-review | not built | — |

- The `git` skill on `main`, and in every plugin version since 0.10.1, is SKL-006 v3, which is not
  approved. Its remaining checks are in `docs/runbooks/git-v3-checks.md`.
- `spec-lookup` also ships a plugin agent, `agents/spec-lookup.md` (`devforgeai:spec-lookup`), which
  runs the lookup script for another skill's workflow.
- The progress tracker is part of the plugin, not a skill: `progress/` (SPEC-012 v16, the evaluator; v16, question forms, Bash writes and the carried draft, and v15, work files and their cleanup, merged in PR #99 (`51571ce`), deployed 0.27.0; v14, carried steps for a run that continues an earlier one, merged in PR #91 (`f128047`), deployed 0.25.0; v13, the run-end `returned`, merged in PR #89 (`9fdda66`), deployed 0.24.0; v12, the run-end `stopped`, merged in PR #85 (`4daa7c4`), deployed 0.22.0)
  and `hooks/progress.tsx` (SPEC-013 v22, the Claude Code adapter; v22, forms recorded, Bash writes refused and checked, the line on continuing states the draft, merged in PR #99 (`51571ce`), deployed 0.27.0, built before v21; v21, other mods' tool calls unrecorded, `/progress`, and a warning at 70% of the context window that `/devforgeai:precompact` runs at 80%, approved 2026-10-06, not built (its BEH-33 origin check is built for Bash only, with v22); v20, deleting a run's work files through prune.py, merged in PR #99 (`51571ce`), deployed 0.27.0; v18 and v19, untracked skills (a plugin skill whose
  SKILL.md metadata says `devforgeai-tracked: "false"`, precompact the first: its load and its turn's tool calls and replies
  are recorded in no run), merged in PR #93 (`909a252`), deployed 0.26.0; v16 and v17, the offer to continue an earlier unfinished run, merged in PR #91 (`f128047`), deployed 0.25.0; v14 and v15, nested runs paused and resumed,
  merged in PR #89 (`9fdda66`), deployed 0.24.0; v13, the trail of return points for skills Claude loads mid-run,
  merged in PR #87 (`13184e5`), deployed 0.23.0; v12, the deliberate stop and the /clear, /exit, /resume
  confirmation, merged in PR #85 (`4daa7c4`), deployed 0.22.0; v11, the review only after an answered turn,
  merged in PR #83 (`ab8301c`), deployed 0.21.0). It records each tracked skill run
  (brainstorm and architecture have manifests) and shows its checklist steps in the status line and
  a band above the prompt. Its detail is in `.claude/rules/progress.md`.
- **The dashboard** (PRD-001 v12 FR-022; SPEC-016 v2, approved 2026-10-08, not built; design `docs/specs/devforgeai-dashboard.md`; prototype `src/tools/dashboard-probe/`) is a pane of the tracker's mod, `/devforgeai:dashboard`. It needs SPEC-012 v17 and v18 and SPEC-013 v23 (the precompact row counted by fuel left) to v25 (the automatic precompact run's turn marked through BEH-41's set of names), all approved (v18, v25 and SPEC-016 v2 on 2026-10-08), not built. Plugin 0.28.0 builds the evaluator and adapter parts; the pane waits for the design skill's place in the chain (0.29.0).
- `qa`'s stub fixes only the contract SPEC-007 reads: a verdict comment naming the reviewed SHA, and
  the `merge-approved`/`qa-failed` labels.
- ADR-001 to ADR-006 in `docs/specs/adr/` are accepted. PRD-001 (DevForgeAI itself) and PRD-002
  (DevForgeAI CLI, draft) are in `docs/specs/prd/`.

Other folders:
- `src/templates/`: document templates not yet owned by a skill (story, spec, sprint, policy,
  ambiguities, `github/`, `skill/`); a built skill's template is in its `assets/`.
  `src/templates/brainstorm.md` is a leftover identical copy of brainstorm's asset.
- `src/schemas/`: the documents' JSON Schemas. `src/staging/examples/`: example projects.
- `src/codex/devforgeai/`: the Codex port (brainstorm, prd, architecture, documents-updater), built and
  kept by Codex sessions; its README and `*IMPORT-REPORT.md` files give each skill's status. Don't
  edit it from Claude. `src/grok/` is empty.
- `src/tools/session-archive/`: user-level hooks that archive session transcripts (SPEC-005 v1,
  draft). Not part of the plugin; the owner installs them into `~/.claude/`.
- `docs/runbooks/`: manual VER checks. `docs/research/` and the skills-guide PDF in `docs/` are local
  only (gitignored). `tmp/` is gitignored.

There is no build system or linter. Everything before 2026-09-28 was imported in one commit (PR #1);
each spec's Change Log has the earlier history. Specs name paths from another repository's layout:
translate them with `.claude/rules/spec-paths.md`.

## Source and deployed copy

- `src/claude/DevForgeAI/` is the source. Edit only here.
- `.claude/skills/devforgeai/` is the deployed copy, gitignored, which Claude Code loads as the
  `devforgeai` plugin (`/devforgeai:brainstorm`). Edits to `src/` take effect only after a deploy.
  Claude's sandbox denies writes to `.claude/skills/` in every checkout, so deploying (ADR-001 steps 2
  and 7) is the owner's step, from a plain shell. After a fresh clone, deploy once.
- `.codex/devforgeai/` is the deployed Codex copy, built from the files `main` tracks. All of
  `.codex/` is gitignored.

```bash
# Deploy the Claude plugin; the adapter's tests and Claude Code's generated files stay out
X=(--exclude=__pycache__ --exclude=results --exclude='*.test.ts' --exclude='*.test.tsx')
X+=(--exclude=/tsconfig.json --exclude=/.claude-plugin/types/)
rsync -a --delete "${X[@]}" src/claude/DevForgeAI/ .claude/skills/devforgeai/
# Deploy the Codex plugin from HEAD
T=$(mktemp -d) && git archive HEAD src/codex/devforgeai | tar -x -C "$T"
mkdir -p .codex/devforgeai && rsync -a --delete "$T/src/codex/devforgeai/" .codex/devforgeai/
```

`--delete` also clears stray files such as Windows `*:Zone.Identifier` copies. After a deploy, an
open session loads the new adapter with `/reload-plugins`.

## Commands

Run from the repository root. Eval generators and offline grader checks: `.claude/rules/evals.md`.

```bash
# The deployed copy matches the source, apart from what the deploy leaves out
D=(-x '*.test.ts' -x '*.test.tsx' -x tsconfig.json -x __pycache__ -x results)
diff -rq "${D[@]}" src/claude/DevForgeAI .claude/skills/devforgeai
# Every Python test under src/tests (pytest.ini sets importlib mode; see "Traps")
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests
# One folder or one test file
PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress
python3 -B src/tests/brainstorm/test_validate_brn.py
python3 -B src/tests/prd/test_shared_files.py
# Session-archive tests: all, or one by name
python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py'
python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py' -k test_scope_is_opt_in
# The progress adapter's kit tests, and what Claude Code reads from the plugin
claude plugin test src/claude/DevForgeAI
claude plugin validate src/claude/DevForgeAI
# The Codex port's tests, leaving no __pycache__ in the Codex tree
PYTHONDONTWRITEBYTECODE=1 python3 -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py'
# A skill's checker on a real file
python3 src/claude/DevForgeAI/skills/brainstorm/scripts/validate_brn.py docs/specs/brainstorm/BRN-001.md
PYTHONDONTWRITEBYTECODE=1 python3 src/claude/DevForgeAI/skills/documents-updater/scripts/check_docs.py README.md
```

`src/tests/<skill>/` holds the skills' tests and eval generators.
`test_shared_files.py` checks that the prd, architecture and context skills' shared policy files are
byte-identical.

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

- The bar is ≥ 0.8 per case over 3 runs (the default run count) against the no-plugin baseline, unless
  Bryan records a waiver in the spec's §9. Go cheapest first: a few cases with
  `--runs 1 --ablation none`, then the suite with `--runs 1`, then 3 runs with the baseline.
- `record_revision.sh <results-dir> <tag>` refuses an existing folder and uncommitted changes in
  `src/` or `docs/`: commit first, and use a new folder for every run. Keep results under
  `tmp/eval-results/`, never the plugin's `evals/results/`, which would deploy.
- Eval cases are generated: edit the generator in `src/tests/<skill>/` and regenerate, never the case
  files. Brainstorm's cases and prd's v1 cases are hand-written.
- The eval sandbox masks `.git/config.lock` in a repository the scaffold built: `git config`,
  `remote add` and `push -u` fail there.

## Rules a change must not break

- **Look it up before building it** (SPEC-014 BEH-08). Before proposing, designing or changing any
  DevForgeAI behaviour, use `/devforgeai:spec-lookup` (or
  `src/claude/DevForgeAI/skills/spec-lookup/scripts/find_spec.py`) and cite what it finds, or ask
  Bryan. Never build what no spec, ADR or recorded decision covers. During another devforgeai skill's
  workflow, hand the lookup to the `devforgeai:spec-lookup` agent, which leaves that run alone: a skill
  the user types ends the run, and one Claude loads pauses it until Claude goes back (SPEC-013 v15).
- **Judgment calls are the user's.** In brainstorm, idea dispositions and convergence are written only
  when the user confirmed them; otherwise they stay `disposition: open`, `reason: null` and
  `status: draft` (VER-02). Each later spec names its own user-owned decisions.
- Skills write documents as `docs/specs/<type>/<ID>.md` in the *user's* project and allocate the ID
  themselves; they never take a file name from the user. documents-updater is the exception: it edits
  the user's existing README, CHANGELOG and guides in place.
- An approved document changes only with a `version` bump, a new `updated` date and two Change Log
  rows: the change, authored `claude-code (session <ID>)`, and the owner's approval. Then move every
  `upstream` link that cites it (other specs, `provenance.yaml`) to the new version. Never rewrite
  earlier Change Log rows. A §9 status record (built, evaluated, merged) needs no version bump.
- **Hand-offs to documents-updater** (decided by Bryan on 2026-09-28). The skill that ends the
  planning chain ends its Next step by recommending `/devforgeai:documents-updater`, with an eval
  grader for it (SPEC-006 §13); no built skill is that last step yet. The `git` skill recommends it
  before opening a PR whose branch changes neither README nor CHANGELOG, and runs it only on the
  user's yes (SPEC-007 BEH-19). No other skill hands off to documents-updater, and it never starts
  itself.

## Traps

- Keep the Bash working directory at the repository root. A sandboxed command run from a subfolder
  leaves empty placeholders there (`.claude/.cc-writes/`, `.mcp.json`); remove them with `rmdir`.
- Inside the sandbox, `.mcp.json` and other entries owned by nobody at the root and in `.claude/`
  (character devices, dotfiles such as `.bashrc` and `.gitconfig`) are the sandbox's write masks, not
  files. Leave them alone, and stage files by path, never `git add -A`.
- Several test folders have a `test_structure.py`, and `src/tests/spec-lookup/` can't be a package
  (pytest takes a folder as one only when its name is a Python identifier). The root `pytest.ini`
  sets `--import-mode=importlib` so they don't clash; keep it, or `pytest src/tests` stops at
  collection with "import file mismatch".
- Commands for the owner to paste into a plain shell never start with `!` (in bash it negates the exit
  status, so `! diff … && echo ok` reports success when the copies differ), use no `\` continuations,
  and keep each line under about 100 characters (put long flags in variables).
- `git push` and `gh pr` run outside the sandbox (`.claude/settings.local.json`) only when the command
  starts with them: run each as its own Bash call, and never pass `allowed_domains`, which routes it
  through a proxy that is often down. If the auto-mode classifier blocks a push, retry once after the
  owner confirms it in the conversation.
- In a worktree session, the isolation guard refuses `python3 -m unittest`, heredocs that mention git,
  and commands whose paths contain `git` in a form it can't verify (such as `skills/git/`). Run test
  files directly (`python3 -B src/tests/git/test_repo_state.py`), and write scratch scripts with the
  Write tool before running them.
- **Never investigate a failing test by changing the working tree** (ADR-005 D7). Record a baseline
  test run before the first change; compare old code only in a disposable worktree
  (`git worktree add --detach <path> <commit>`) or with `git show <commit>:<path>`; commit work in
  progress before each full test run. Never restore, check out, stash, reset, clean or re-download
  files into the working tree to investigate.

## Future roadmap

Recorded and not decided; each needs Bryan's decision before any work (see "Look it up before
building it"). The source of each item is named.

- **Unbuilt skills:** `qa` (SPEC-008, a stub whose review criteria are open), `story` (SPEC-009,
  draft), `github-post` (SPEC-010 v3, awaiting approval; its templates are staged in
  `src/templates/github/`), and the chain's final Spec step, which only PRD-001 FR-017 covers (no
  spec, no reserved SKL ID).
- **`git` SKL-006 v3:** native evaluation, the manual VER items and Bryan's approval
  (SPEC-007 §9, §13; `docs/runbooks/git-v3-checks.md`).
- **Progress tracker** (SPEC-012 §11): the progress pane and its graphics, `progress.html`,
  `chain_state.py` and phases, manifests for the other skills, and a Codex copy.
- **Open questions** in the §13 of SPEC-001, SPEC-003, SPEC-010, SPEC-012, SPEC-013 and SPEC-014
  (for example, the waiver question's treatment of a dismissal, and whether a challenge in the
  end-of-run review should do more than record).
- **Manual VER items not run**, listed in each spec's §9.

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
| `.claude/rules/progress.md` | `src/claude/DevForgeAI/progress/**`, `src/claude/DevForgeAI/hooks/**`, `src/tests/progress/**` | changing or debugging the progress tracker or its adapter |
