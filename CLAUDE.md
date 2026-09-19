# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read these first, in this order

1. **[AGENTS.md](AGENTS.md)** — the authoritative policy document. Execution boundaries, the compiled-Rust authority rule, the red → green → refactor → QA cycle, the ≥95% coverage **and** ≥95% required-case pass-rate thresholds (independent minimums; a missing measurement is `NOT_RUN`/`BLOCKED`, never an estimate).
2. **[README.md](README.md)** — current component inventory and the Rust command set.
3. **[docs/workflows/worktree-and-pr-delivery.md](docs/workflows/worktree-and-pr-delivery.md)** — **mandatory before the first edit** to repository source, skills or documentation, and before any commit, push or PR. Do not load it for discussion or read-only inspection. It requires a real `git worktree` under `worktrees/git/<task-name>/`, explicit path staging (never `git add .`/`-A`), push to a task branch (never to `main`, never force), and a **draft** PR that stays draft while mandatory validation is missing or failing.

   The root **`DevForgeAI-Console.ps1`** implements that procedure interactively (option 6 creates the task branch and worktree, 8 pushes, 10 opens the draft PR, 3 takes a safety checkpoint first). It is the human operator's path, documented in [docs/workflows/operator-console.md](docs/workflows/operator-console.md); the written procedure remains authoritative for agent work.

This file adds only what those three do not say, or where they are stale.

## The DevForgeAI Adaptive Spec-Driven Engineering Framework

**The framework is a specification collection, not a running system.** Its entry point is [docs/specs/framework/index.md](docs/specs/framework/index.md) (`id: DFF-00`, `status: planning-baseline`, `implementation_readiness: not-ready`). Twelve capability documents `DFF-01`–`DFF-12` define it; every one is "planning baseline", "design only" or "proposed". Read the index and [foundation.md](docs/specs/framework/foundation.md) before reasoning about framework behavior.

Use the index's **status vocabulary** in every claim, because these four words are what keep the repository unambiguous:

| Status | Means |
| --- | --- |
| Discussed / planning baseline | A direction with boundaries and open questions. Not a runnable promise. |
| Specified | Complete inputs, outputs, failure behavior, dependencies, testable acceptance cases. |
| Implemented | Identified source supplies the behavior. Evidence must name the candidate and checks. |
| Qualified | Native scenarios, integrity conditions and thresholds actually demonstrated for a named scope. |

A package existing on disk, a passing Python suite, a complete-looking document or a model-written PASS **cannot** promote a status. Protected acceptance requires its own authority.

**Six capabilities, not a pipeline.** Discovery/business analysis, architecture/design, work planning, development, independent QA, delivery/follow-up ([core-workflows.md](docs/specs/framework/core-workflows.md)). They are not a compulsory sequence — an adequate specification or a specified defect may enter development with no brainstorm, PRD or story. The selected discovery route is **brainstorm → prd-create → prd-review**, then work planning and stories when needed. Setup/activation is a separate responsibility, never a mandatory phase 0.

**Design constraint:** the base must be feasible on supported Codex with an individual ChatGPT Pro subscription. No hidden paid-API, Enterprise, undocumented-host or unlimited-agent assumptions.

**Portability is the point.** Skills derive language, architecture, tools, layout, commands, thresholds, platforms and delivery locations from runtime inputs. Git, an index, a service, a descriptor, an operational binding, MCP, a browser or a plugin is never a prerequisite. When the target project *is* DevForgeAI, its Rust requirement and ≥95% thresholds arrive as project-policy inputs — never as constants baked into a skill. Never bake a destination path into a skill; deployment targets are runtime inputs.

### Skill inventory

Development source is `src/agents/skills/` (Codex). `src/claude/skills/` holds Claude Code ports of the same responsibilities. Operational copies are `.agents/skills/` and `.claude/skills/`.

| Skill | Codex | Claude port | Bound eval artifacts | Specification |
| --- | --- | --- | --- | --- |
| `brainstorm` | yes | — | none | `framework/workflows/phase-1-brainstorm-spec.md` (DFF-WF-01) |
| `prd-create` | yes | — | none | `framework/workflows/phase-2-prd-create-spec.md` (DFF-WF-02) |
| `prd-review` | **not authored** | — | — | `framework/workflows/phase-3-prd-review-spec.md` (DFF-WF-03) — next selectable authoring |
| `story-create` | yes | — | `scripts/` only | — |
| `dev` | yes | yes | **none** | `docs/specs/dev-skill-spec.md` |
| `qa` | yes | yes | none | `docs/specs/qa-skill-spec.md`, `qa-skill-postmvp-spec.md` |
| `skill-builder` | yes | yes | `scripts/`, `schemas/`; **`evals/`+`tests/` only in `.agents/`** | `docs/plan/skill-builder-*-spec.md` |
| `skill-validator` | yes | yes | complete | `docs/plan/skill-validator-spec.md`, `-adaptive-enhancement-spec.md` |
| `advisor` | yes | yes | complete | AGENTS.md § Claude second opinions |

**Separation of duties is the core invariant.** `skill-builder` holds authoring custody — custody is *not* quality evidence. `skill-validator` independently assesses and never repairs, installs or invokes the builder. `dev` owns product implementation directly and must not invoke a skill-authoring workflow for application code. `story-create` requires a project binding; standalone `dev` does not. `dev` and `qa` carry *different* quality-policy and stop rules — see MIG-01/MIG-02 in [roadmap-and-decisions.md](docs/specs/framework/roadmap-and-decisions.md#compatibility-and-migration-register).

Per AGENTS.md §Framework authority, a skill build requires a JSONL runner, deterministic graders, fixtures, expected results, schema, runtime information and digests/manifests; missing required evaluation artifacts make a build **incomplete**. Several rows above are therefore incomplete builds, not stylistic variation. Report that as an observation — confirm with the maintainer before treating any as finished or as a pattern to copy.

`advisor` is a bounded external-CLI second opinion, not a subagent: at most two reviewer attempts per review, USD 2.00 total / USD 1.00 reserved per attempt, 300-second timeout, runs under `docs/plan/advisor-runs/`. Do not raise limits or edit either advisor package to force completion.

## Commands

No repository-root build manifest, no aggregate test runner, no lint task. The Python and Pester commands below were executed in this workspace; the Cargo commands are from the package README with the toolchain confirmed present (cargo/rustc 1.97.1) but no build run here. A documented command is not a claim that this checkout has passed a fresh build or QA campaign.

### Rust — the index application

`devforgeai/` is a real crate: `devforgeai-index` v0.1.0, edition 2024, Rust ≥1.93, `[workspace] members = ["."]`. It builds the `devforgeai` CLI, `devforgeai-indexd` daemon and (Windows) `devforgeai-tray`. Needs a native C compiler for bundled Tree-sitter grammars and SQLite. From the repository root:

```powershell
cargo build   --manifest-path .\devforgeai\Cargo.toml --locked
cargo test    --manifest-path .\devforgeai\Cargo.toml --locked --all-targets
cargo fmt     --manifest-path .\devforgeai\Cargo.toml --all -- --check
cargo clippy  --manifest-path .\devforgeai\Cargo.toml --locked --all-targets -- -D warnings
```

It is a *development implementation* of [the index-service spec](docs/plan/devforgeai-index-service-mvp-spec.md) with no framework-acceptance or mutation-broker authority. CLI groups: `daemon`, `project`, `index`, `job`, `environment`, `tray`. The [query CLI spec](docs/plan/devforgeai-index-query-cli-spec.md) is a *separate* contract whose commands this CLI does not supply. On Linux, tray commands return `UNSUPPORTED_PLATFORM`.

`devforgeai/experiments/` holds three isolated worker probes with their own Cargo manifests — build them separately, never via the main manifest.

### Python — skill test suites

```bash
# Full validator suite (~2m on /mnt/c)
python3 -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests

# A single file — use -p, not -t; the tests dirs have no __init__.py,
# so `-t <pkg-root>` fails with "Start directory is not importable"
python3 -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -p test_observe.py
```

Same shape for `advisor/tests` (105 tests) and `.agents/skills/skill-builder/tests`. Python 3.10.11 with PyYAML 6.0.2 is installed here; use `python` in PowerShell, `python3` in Git Bash.

### Python — evaluation runner and observation helpers

```bash
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/run_evaluation.py \
  --package-root <pkg> --candidate-root <candidate> --cases <cases.jsonl> \
  --output <new-file> --run-id <id> [--profile <profile>]
```

All five long flags are required. `--output` must be a *new* file in an *existing* directory, outside both roots. Profiles are declared in `PROFILES` at the top of the script — read it rather than trusting a list; a suite must exercise exactly its profile's graders or the runner rejects it.

```bash
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/observe.py {snapshot,structure,readback,records} --help
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/adaptive_observe.py {package,intake-set,records} --help
```

`snapshot` is the only helper that writes; its `--output` directory must not already exist. Exits: `0` observations completed, `1` deterministic mismatch, `2` usage/access/dependency failure. **Exit 0 is not a semantic or behavioral PASS.** `tiktoken` is absent here, so `adaptive_observe package` reports token counts `NOT_RUN` and exits 2.

### PowerShell — the operator console

```powershell
Invoke-Pester -Path .\tests\operator-console -Output Minimal        # 42 tests, ~95s
Invoke-Pester -Path .\tests\operator-console\Compatibility.Tests.ps1 # one file
Invoke-Pester -Path .\tests\operator-console -Tag Confirmation       # one tagged group
```

Pester 5.7.1 is installed (3.4.0 is also present — `-Output`/`-Tag` require v5). The suite builds throwaway Cargo fixtures in `$env:TEMP` and prints rendered menus; a Rust `expected one of ! or ::` error in the log is a **deliberate negative fixture**, not a failure. The console itself targets Windows PowerShell 5.1 and PowerShell 7.2+, so avoid PS7-only syntax in `scripts/operator-console/OperatorConsole.psm1`.

## Layout, the mirror rule, and legacy

| Path | Role |
| --- | --- |
| `src/agents/skills/` → `.agents/skills/` | Codex development source → operational copy. **Deliberately not a mirror** (204 vs 230 files). Development edits do not propagate; updating `.agents/` needs explicit authorization. |
| `src/claude/skills/` ↔ `.claude/skills/` | Claude Code source ↔ operational copy. **Byte-identical mirror pair** for the five ported skills, plus `agents/` and `commands/`. |
| `src/claude/{skills,agents,commands}/legacy/` | The retired 19 `spec-driven-*` / `github-incident-*` workflows, 90 legacy agents, 70 legacy commands. **Superseded; do not extend.** |

**The mirror rule (ADR-073):** any edit to a non-legacy `src/claude/` skill, agent or command must be applied to **both** paths with identical strings, and the pair self-diffed to empty. Editing one path silently desynchronizes the framework.

The `legacy/` subtrees are **asymmetric by design**: `.claude/skills/legacy/` exists on disk but is gitignored; `.claude/agents/legacy/` and `.claude/commands/legacy/` do not exist at all. So a whole-tree `diff -rq .claude src/claude` reports legacy-only differences — that is expected, not drift. Scope the diff to the paths you changed.

`devforgeai-validate` is **legacy and will not be installed** (maintainer direction, 2026-09-18). It is absent from `PATH` and from `~/.cargo/bin/`. Every `legacy/` phase file that calls it for a gate is permanently unrunnable: report those gates `NOT_RUN`/`BLOCKED`, never estimate a pass, and do not try to build it — its source is not in this repository.

## Line endings and byte-exact evidence

`.gitattributes` sets `* -text` with the rationale *"Retained manifests bind exact bytes. Do not normalize line endings on add/checkout."* Retained manifests hold file hashes, so a line-ending conversion moves a package digest for reasons unrelated to content.

- **The convention is LF.** Verify with `git check-attr text <path>` (expect `text: unset`) and `git ls-files --eol`.
- `core.autocrlf` is `true` in this working copy, but `-text` **overrides it per path** — the attribute is the safeguard, not the config. Do not reason from `core.autocrlf`.
- **After any skill-file edit, compare `git diff --stat` against `git diff --ignore-cr-at-eol --stat`.** Divergence means a line-ending conversion rode along with your content change. This has happened twice: `qa/SKILL.md` carries a committed CRLF conversion, and `dev/SKILL.md` had one caught before it reached history (PR #10). `git ls-files --eol` distinguishes them — `i/lf w/crlf` is still fixable, `i/crlf` is already committed.

## Evidence contracts

`docs/plan/` holds specifications plus retained evidence runs. **Evidence is append-only**: preserve existing runs in place and write to a new, distinct directory.

- Validation: `docs/plan/skill-validations/<target>/<run-id>/` — schema-1 records (`origin-record.json`, `rule-set.json`, `sources.json`, `checks.jsonl`, `findings.json`, `workflow-map.json`, `handoff.json`), a byte-exact `source/` snapshot with manifest, and a `validation-report.md`.
- Authoring: `docs/plan/skill-authorings/<target>/<run-id>/` — contract, before/candidate/delivered manifests, `authoring-record.json`, `validation-request.json`.
- Run IDs are UTC `YYYYMMDDTHHMMSSZ`. Machine paths inside a run are forward-slash **run-relative**; `..` is rejected, so copy an external input into `inputs/` rather than pointing outside the run.
- `/docs/plan/**/trials/` and `**/fixtures/` are gitignored, so trial artifacts stay local and digest references into them resolve only in the originating checkout. Note that in any PR.
- Reports name their own candidate, platform, executed checks and limitations. Preserve those distinctions when citing; a checkout is not a complete copy of every historical run.

## Authority boundary

Framework CLI/service behavior, hooks, phase gates, validators, mutation brokers and acceptance decisions belong in **compiled Rust** ([design](docs/plan/devforgeai-codex-rust-enforcement-design.md), still `proposed`). Python utilities, skill evaluations, reviewer advice and index observations produce **evidence only** — they cannot authorize mutations, advance phases, waive gates or grant acceptance. So: Python evaluation is *required* for a skill build, and Python is *never sufficient*.

Distinguish specified interfaces, structural checks, native execution and framework acceptance. Help output, an exit code or a model-written PASS substitutes for none of them. Claim an enforced gate only after its Rust implementation is qualified.

**No `hooks/` directory exists in this workspace.** Skills that reference `.claude/hooks/` describe a consuming project; treat hook-backed gates as unavailable locally and report them `NOT_RUN`.

## Known-stale statements

This repository's status metadata lags its contents. Verify before relying on any of these:

- **`README.md`** says `prd-create`'s "full workflow specification and package not authored" — both now exist. It also lists 7 skill packages; there are 8 (`prd-create` is missing from its table).
- **`docs/specs/framework/index.md`** cites evidence runs that are absent from this checkout and not gitignored: `skill-validations/brainstorm/20260918T021707Z/`, `skill-validations/prd-create/20260918T121331Z/`, `framework-worker-logging/20260917T105456Z-qa-retest/`. Only `dev` exists under `skill-validations/` and `skill-authorings/`.
- **`docs/specs/dev-skill-spec.md`** frontmatter reads `status: proposed`, `package_status: not_authored`; the package exists in four host copies. Do not read it as unbuilt.
- **`AGENTS.md`** describes `src/agents/skills/` as `skill-builder` and `skill-validator` only, and treats `devforgeai-validate` as a proposed interface. It is also right that `skill-builder`'s `tests/`+`run_evaluation.py` are missing from the `src/agents/` development copy — that gap is real and open.
- **`.claude/skills/skill-builder/references/claude-frontmatter.md`** (lines 13, 28) states `allowed-tools` *restricts* tool availability. It does not — it pre-approves for the invoking turn and removes nothing (`disallowed-tools` is the restricting field, and it is turn-scoped too). That reference regenerates the defect on every port; `qa`, `skill-builder` and `skill-validator` still carry the incorrect claim in their own `SKILL.md`.

## Conventions

Four-space Python indent, `snake_case` functions/modules, `PascalCase` classes; rustfmt and the package Clippy configuration for Rust. Preserve existing JSON/YAML schema field names. Skill directories are kebab-case; entry instructions are always `SKILL.md`; use relative package links. Avoid unrelated formatting changes.

Commit subjects are concise and imperative, optionally prefixed `docs:`, `fix:` or `test:`. Changes land via pull request — every recent commit on `main` is a PR merge. PR descriptions explain behavior, related issues, validation actually performed, and limitations.

Prefer native Windows tooling for `C:\Projects\DevForgeAI`; use WSL only for required Linux behavior, and keep platform-specific virtual environments and build outputs separate. `/mnt/c/...` and `\\wsl$\...` cross the filesystem boundary. On ambiguity or conflict, record the exact unresolved decision and the work it affects rather than inventing an answer.
