---
paths:
  - "src/claude/DevForgeAI/evals/**"
  - "src/tests/**"
  - "tmp/eval-results/**"
---

# Evaluating a skill: tooling and flags

CLAUDE.md, "Evaluating a skill", has the suite command and the rules that always apply. This file has
the per-skill tooling, what each flag is for, and how to read results.

## Per-skill eval tooling

Run from the repository root. Cases under `src/claude/DevForgeAI/evals/<skill>/` are generated:
edit the fixtures and graders in the generator and regenerate, never the case files. The exceptions
are brainstorm's cases and prd's v1 cases, which are hand-written.

```bash
# documents-updater: regenerate every case; check one case's regex graders offline
python3 src/tests/documents-updater/make_evals.py
node src/tests/documents-updater/grade_evals.mjs src/claude/DevForgeAI/evals/documents-updater/<case> <workspace> <reply.txt>
# architecture: regenerate (validates each fixture against src/schemas/ first); check one offline;
# check the VER-17/18 graders with scripted good and bad results
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/architecture/make_evals.py
node src/tests/architecture/grade_evals.mjs src/claude/DevForgeAI/evals/architecture/<case> <workspace> <reply.txt>
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/architecture/check_graders.py
# prd: regenerate the v2 cases (VER-24..32); check their graders offline, or one case
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/prd/make_evals.py
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/prd/check_graders.py
node src/tests/prd/grade_evals.mjs src/claude/DevForgeAI/evals/prd/<case> <workspace> <reply.txt>
# epic: regenerate (validates each fixture against src/schemas/ and SPEC-004 §9 first); check one offline
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/epic/make_evals.py
node src/tests/epic/grade_evals.mjs src/claude/DevForgeAI/evals/epic/<case> <workspace> <reply.txt>
# git: regenerate (runs each scaffold and checks its premise first); check the graders offline with
# scripted good and bad runs, and the command patterns
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/git/make_evals.py
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/git/simulate_runs.py
node src/tests/git/check_patterns.mjs
# context: regenerate; check the graders offline with good and bad simulated runs; check one offline
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/context/make_evals.py
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/context/check_graders.py
node src/tests/context/grade_evals.mjs src/claude/DevForgeAI/evals/context/<case> <workspace> <reply.txt>
# spec-lookup: regenerate (checks each case's premise with the skill's find_spec.py first)
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/spec-lookup/make_evals.py
# precompact: regenerate (builds each scaffold, checks its premise and computes the fixture's head hash)
PYTHONDONTWRITEBYTECODE=1 python3 src/tests/precompact/make_evals.py
# before every paid run: bind a new results folder to the commit, plugin digest and cases
bash src/tests/prd/record_revision.sh tmp/eval-results/<new-folder> <tag>
```

The `make_evals.py` generators import `referencing`, which only the user site-packages' jsonschema
has, so run them under your normal HOME.

Running a generator rewrites its case files. To check fixtures without touching tracked files, load
the generator with `importlib` and call its `validate()` over `FIXTURES`. Importing writes nothing,
although epic's import already validates its PRD and ARCH (checked 2026-09-30). Point the module's
`SCHEMAS` at a scratch copy to try a schema change first. The architecture, prd, epic and context
generators and the policy script validate with jsonschema's `FormatChecker`, and
`common.schema.json` gives dates `"format": "date"`, so an impossible date such as `2026-13-45` is
a schema error.

What each generator's scaffolds seed: every documents-updater case builds a small git repository with
dated commits; every architecture case seeds a PRD, plus ARCHs, ADRs or a policy; every epic case
builds SPEC-004 §9's shared fixture or a variant; every git case builds a repository plus a local bare
`origin` under `remote/`, whose push hook writes `remote/origin.git/push-log.txt`. Among the
hand-written cases, brainstorm's `existing-brn` and every prd case but `ignores-unrelated-request` have
a scaffold that seeds the BRNs, PRDs, ADRs and policies the case reads.

## Flags

- `--allow-tools Write Edit Bash`: every case lists these gated tools in `allowed_tools`; Bash runs
  brainstorm's validator script. A run that prints `not granted (missing --allow-tools grant…)` still
  runs and scores, without those tools: check for that line before trusting any score.
- `--scaffold`: runs `case.yaml` scaffold scripts. Runs start in an empty workspace, so the scaffold
  must seed anything the skill reads.
- `--threshold 0.8`: the default is 1.0. The framework bar is ≥ 0.8 per case over 3 runs, the default
  run count.
- Narrow a run with `--case existing-brn`, or `--tag brainstorm`, `--tag prd`, `--tag architecture`,
  `--tag epic`, `--tag git`, `--tag context`, `--tag spec-lookup` or `--tag precompact`. Trigger cases carry
  other tags: context's 12 are tagged `trigger` and `ver-26`, spec-lookup's 5 `trigger`, `ver-06` and
  `spec-lookup-trigger`, precompact's 8 (`precompact-trigger-NN`) `trigger`, `ver-06` and `precompact-trigger`,
  so `--tag trigger` selects all three suites' trigger cases. `--tag precompact-trigger` found no cases on
  2026-10-05 (2.1.290); select precompact's with `--case "precompact-trigger-*"`. `ver-NN` tags repeat
  across skills (brainstorm, prd, architecture and epic each have a `ver-08`), and so can case names
  (prd and architecture each have `policy-bad-date`), so pair `--case` with care. `--case` takes one name; loop for several. Use
  `--runs 1` for a quick pass.
- A no-plugin baseline arm runs by default. `tool_used: Skill` graders then only indicate that the
  plugin fired and don't count toward the score.
- The HTML report publishes to claude.ai by default when the account supports it; add `--no-publish`
  to keep it local. Without `--output-dir`, results land in the plugin's `evals/results/` and would
  deploy with it; keep them under `tmp/eval-results/`.
- `--judge-model sonnet`: the default small judge failed correct replies. Even sonnet failed a correct
  8 kB PRD in 3 of 3 votes, so check claims about a written file with regex graders, and test each
  regex with `node` against a real output first.
- `--keep-temp` keeps `out/trace.jsonl`, the run's full transcript, with every tool call and the
  final reply; the workspace itself is sealed (mode 000).

## Graders and the eval sandbox

- A regex grader that fails keeps no copy of the reply: `aggregate-result.json` says only "pattern not
  found". Grade "asks the user" with an llm grader, which also keeps the reply as evidence; keep regex
  graders for exact file content.
- A slash-command prompt (`/devforgeai:git status`) injects the skill without a Skill tool call, so
  such a case can't carry a `skill-fired` grader (verified 2026-09-28, git pilot).
- The workspace is `home/cwd`, and `home/` is itself a git repository. A repository the run itself
  creates with `git init` isn't masked the way a scaffold-built one is (CLAUDE.md).

## Reading results

- Before trusting a low score, check `cases[].arms.with[].error` in `aggregate-result.json`: an
  expired login or usage limit scores 0 without being a regression.
- Run traces under `/tmp/claude-eval-*` are deleted when the run ends. `report.html` keeps what each
  llm grader saw (the reply or the file), which is usually enough to diagnose a failure.
- Each spec's §9 table records its runs: results folder, commit and plugin digest, scores, cost.

## Manual VER items

Brainstorm's manual paths (user confirmation, the extend flow, VER-05, VER-09) follow
`docs/runbooks/brainstorm-manual-test.md`, which loads a *copy* of the plugin with
`claude --plugin-dir` and never touches `src/`. prd v2's manual items (VER-11, VER-12, VER-23) and
architecture v4's (VER-12 (f) and (i), VER-19) follow `docs/runbooks/prd-v2-architecture-v4-checks.md`;
record results in its section 4. epic's VER-13 follows `docs/runbooks/epic-ver-13-checks.md`, with
manual-only fixtures that `src/tests/epic/make_manual.py` generates into `src/tests/epic/manual/`.

Other runbooks in `docs/runbooks/`:

| Runbook | Covers |
|---|---|
| `architecture-v6-checks.md` | SKL-003 v6's paid evaluation and its manual items (VER-20, VER-12 (a), (j), (k), VER-19) |
| `git-v2-checks.md` | SKL-006 v2's paid evaluation and manual items (VER-18 to VER-22, VER-24, VER-26, VER-31) |
| `git-v3-checks.md` | SKL-006 v3's decisions, verification and remaining qualification |
| `spec-011-manual-checks.md` | the context skill's evaluation and manual items VER-21 and VER-22 |
| `spec-013-probe.md` | SPEC-013's runtime probe (VER-01), as run on 2026-10-02 |
| `spec-002-v2-verification-plan.md` | SPEC-002 v2's verification plan |
