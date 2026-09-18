# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Read AGENTS.md first

`AGENTS.md` is the authoritative policy document for this workspace and is not restated here. It governs: the mandatory red → green → refactor → QA cycle, the ≥95% coverage **and** ≥95% pass-rate thresholds (independent minimums; missing measurement is `NOT_RUN`/`BLOCKED`, never an estimate), the compiled-Rust authority boundary, evidence preservation under `docs/plan/`, the ban on ceremonial content, and Windows/WSL filesystem guidance. Read it before any substantive change.

The load-bearing rule from it has two halves, and quoting only one steers wrong:

1. **Python evaluation is mandatory for skill builds**, not merely permitted — a bound JSONL runner and deterministic graders are *required build artifacts*, with fixtures, expected results, schema, runtime information, and digests/manifests. Missing or modified required evaluation artifacts make the build **incomplete**.
2. **Python produces evidence only.** Scripts, skills, YAML, and model-written status files cannot authorize mutations, advance phases, waive gates, or issue acceptance. Only compiled Rust holds framework authority.

So: Python is required, and Python is never sufficient.

## Legacy status — read before changing anything

**`devforgeai-validate` and the entire Claude Code framework under `src/claude/` and `.claude/` are legacy and superseded. They require refreshing.**

This is maintainer direction, stated 2026-09-13. No document in this repository records it, and none contradicts it — do not go looking for in-tree confirmation, and do not conclude from the framework's polished, self-consistent appearance that it is current.

What follows from that:

- The *Architecture* section below describes how the legacy framework works. It is accurate and worth reading — you cannot refresh what you do not understand — but it documents the thing being replaced, not the target design.
- Do not extend the legacy framework by reflex. Adding a command, agent, phase file, or subagent to `src/claude/`+`.claude/` is maintenance on superseded code. Confirm intent first.
- `devforgeai-validate` v0.3.0 still runs and its gates still fire. Treat its 158-subcommand surface as the legacy contract, not the forward one. Its source is not in this repository, so it cannot be refreshed from here.
- The mirror rule below still applies for as long as the legacy framework exists: if you do edit it, edit both paths.
- **The successor is the DevForgeAI Adaptive Spec-Driven Framework** — the three skills under `src/agents/skills/`. That is where new work goes. See its section below.
- Still unsettled: the compiled-Rust enforcement design and the index-daemon specs in `docs/plan/` remain `proposed` / `implementation_status: not_started`. The new framework does not yet have the Rust authority that AGENTS.md requires, so its Python stays evidence-only.

## What this repository is

This is the **source** of the DevForgeAI framework — the prompts, skills, agents, schemas, and evaluation harnesses that drive a spec-driven SDLC. It is not an application, and it is not a project being developed *with* the framework. There is no git metadata and no root build manifest. The only `Cargo.toml`/`package.json`/`pyproject.toml` files in the tree are synthetic fixtures inside `docs/plan/` evidence runs.

Two largely independent halves live here:

| Half | Source of truth | Operational copy | Runtime |
| --- | --- | --- | --- |
| Claude Code workflow framework — **legacy, superseded** | `src/claude/` | `.claude/` | Claude Code |
| DevForgeAI Adaptive Spec-Driven Framework — **current** | `src/agents/skills/` | `.agents/skills/` | OpenAI Codex CLI |

## Repository layout and the mirror rule

`.claude/` and `src/claude/` are **independent byte-identical copies** — not symlinks, not hardlinks (verified: distinct inodes, link count 1). 896 files each, currently `diff -rq`-clean. Any edit to a command, agent, or skill must be applied to **both paths with identical strings**, and the pair self-diffed to empty. This is the ADR-073 dual-path contract that `migration-cluster-worker` enforces during sweeps. Editing only one path silently desynchronizes the framework.

`.agents/` and `src/agents/` are **deliberately not** a mirror (157 vs. 132 files). `src/agents/` is the development copy; `.agents/` is the installed operational copy. Per AGENTS.md, development edits do not propagate, and updating `.agents/` requires explicit authorization — so do not "sync" the two by reflex. But not all of this drift is benign: see the eval-artifact gaps under the current framework below. Distinguish *prose/reference* drift (expected) from *missing required build artifacts* (a gap).

Other top-level directories:

- `devforgeai/` — **empty, and claimed by two different designs.** The `docs/plan/` specs earmark it as the future Rust workspace for the proposed index daemon/CLI/tray (status `proposed`, `implementation_status: not_started`). Separately, the `src/claude/skills/` workflows carry ~2,200 references to runtime artifacts under `devforgeai/specs/`, `devforgeai/feedback/`, `devforgeai/qa/`, `devforgeai/workflows/`, `devforgeai/config/` — but in a *target* project, not here. Before creating anything under `devforgeai/`, confirm which of the two you mean.
- `docs/plan/` — specifications plus retained evaluation evidence run directories. Evidence is append-only: preserve existing runs in place and write new output to a new, distinct directory.
- `docs/Agentskills/`, `docs/codex/` — upstream OpenAI/Anthropic guidance the skill packages cite as authority.
- `tmp/old-framework/` — a retired framework snapshot, 1,254 files. It has no current authority and pollutes repo-wide `rg`/`grep`; exclude it (`--glob '!tmp/**'`).

## Commands

There is no root build manifest, no aggregate test runner, and no lint task. Everything below is verified working in this workspace.

### The Rust authority CLI (legacy)

```bash
devforgeai-validate --version   # 0.3.0
devforgeai-validate --help      # 158 subcommands
```

Legacy and superseded (see above), but still the binary every `src/claude/` workflow calls. Installed at `~/.cargo/bin/devforgeai-validate`. **Its source is not in this repository** — it is an external prerequisite, so you cannot build or modify it from here. Skills and commands invoke it constantly; if it is absent, the workflow gates cannot run and that is a `BLOCKED` result, not a pass.

### Codex skill package tests

```bash
# Full skill-validator suite (292 tests, ~2m on /mnt/c)
python3 -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests

# A single test file — use -p, not -t; the tests directory has no __init__.py,
# so `-t <pkg-root>` fails with "Start directory is not importable"
python3 -B -X utf8 -m unittest discover -s src/agents/skills/skill-validator/tests -p test_observe.py
```

`.agents/skills/skill-builder/tests/` holds a second suite reachable the same way. Per `src/agents/skills/skill-validator/evals/README.md`, **all quality campaigns belong to the validator**; skill-builder contains no quality campaign of its own.

### Deterministic graders / evaluation runner

```bash
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/run_evaluation.py \
  --package-root <pkg> --candidate-root <candidate> --cases <cases.jsonl> \
  --output <new-file> --run-id <id> [--profile <profile>]
```

All five long flags are required. `--output` must be a *new* file inside an *existing* directory, outside both roots. Profiles are declared in `PROFILES` at the top of the script: `legacy-import-v1` (default), `import-v2`, `spec-v1`, `revision-import-v2`, `revision-spec-v1`, `revision-spec-v2`, `builder-v2`, `adoption-v1`, `routing-adoption-v1`. A suite must exercise exactly its profile's graders or the runner rejects it.

### Read-only observation helpers

```bash
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/observe.py {snapshot,structure,readback,records} --help
python3 -B -X utf8 src/agents/skills/skill-validator/scripts/adaptive_observe.py {package,intake-set,records} --help
```

`snapshot` is the only helper subcommand that writes. Everything these emit is observation, never acceptance.

### QA utility dependencies

```bash
python3 -m pip install -r src/claude/skills/spec-driven-qa/scripts/requirements.txt   # use an isolated venv
```

Python 3.12 is what is installed here; the packages target 3.10+.

## Architecture: how the legacy workflow executes

This is the part that requires reading many files to see, so it is spelled out. It describes the superseded framework — read it to understand what a refresh has to replace, not as the pattern to extend.

**Slash command → Skill → phases → subagents → CLI gates.**

1. **Command** (`src/claude/commands/<name>.md`) is a thin dispatcher. YAML front matter declares `description`, `argument-hint`, `model`, `effort`, `allowed-tools`, `execution-mode`. The body parses arguments, runs one preflight CLI call (e.g. `devforgeai-validate dev-preflight ${STORY_ID} --project-root=. --format=json`), sets context markers, and hands off with `Skill(command="spec-driven-dev")`. Commands must stay lean — `/audit-budget` and `/audit-hybrid` exist specifically to catch commands that do too much work before invoking their skill. Namespaced commands live in `commands/DF/` and `commands/skill/`; shared prose lives in `commands/references/`.

2. **Skill** (`src/claude/skills/<name>/SKILL.md`) is the orchestrator. It never inlines phase content; it loads one phase file at a time. Of the 19 skills, the 14 `spec-driven-*` ones carry 6–21 phases each (`spec-driven-dev`: 12, `spec-driven-documentation`: 21, `spec-driven-brainstorming`: 11). The 5 `github-incident-*` skills are phaseless and are the **only** place in the framework permitted to call `gh issue create`.

3. **Phase file** (`phases/phase-NN-<name>.md`) has a fixed shape: an **Entry Gate**, a **Contract** block (PURPOSE / REQUIRED SUBAGENTS / REQUIRED ARTIFACTS / STEP COUNT), mandatory **Reference Loading**, numbered steps, and an **Exit Gate**. Every step follows **EXECUTE → VERIFY → RECORD**:

   ```
   EXECUTE: devforgeai-validate git-check --project-root=. --format=json
   VERIFY:  parse JSON; branch on assessment.status
   RECORD:  devforgeai-validate phase-record ${STORY_ID} --phase=01 --subagent=git-validator --step=01.1
   ```

   Gates bracket each phase: `phase-init` → `phase-check --from=N-1 --to=N` → steps → `phase-complete --phase=NN --checkpoint-passed` (exit 0 proceed, exit 1 HALT). This is the **Execute-Verify-Gate** anti-skip design: enforcement lives in the binary and in `settings.json`-registered hooks, *not* in the prose. Prose that merely asserts a gate is ceremonial content and is prohibited.

4. **Subagents** (`src/claude/agents/*.md`, 59 of them) supply fresh context for work the orchestrator must not do from a polluted window — independent AC verification, custody-chain auditing, coverage analysis, anti-pattern scanning. Terminal workers never invoke other subagents. Several have been replaced outright by CLI subcommands for determinism (phase-01 Step 1 notes `git-check` "replaces git-validator subagent — 0 LLM tokens"); prefer the CLI when both exist. Agents with a sibling directory (`agents/<name>/`) keep their references there.

**The 6 constitutional context files** are the law every workflow enforces: `tech-stack.md`, `source-tree/`, `dependencies.md`, `coding-standards.md`, `architecture-constraints.md`, `anti-patterns.md`. Phases load their generated `.ai.md` companions from `devforgeai/specs/context/`. On ambiguity or conflict, workflows must HALT and use `AskUserQuestion` rather than guess.

**Hooks are not installed here.** Skills reference `.claude/hooks/` and `.claude/hooks/phase-steps-registry.json` (ADR-076), but no `hooks/` directory exists in this workspace — it is created in a consuming project. Treat hook-backed gates as unavailable locally and report them `NOT_RUN`.

## The DevForgeAI Adaptive Spec-Driven Framework (current)

Three skills under `src/agents/skills/`, operational copies in `.agents/skills/`. This is the active framework and where new work belongs.

The framework's name is maintainer-supplied; the phrase "Adaptive Spec-Driven" appears nowhere in the tree, so do not search for it. The specs below are real and are the grounding.

| Skill | Role | Specification |
| --- | --- | --- |
| `dev` | Implements a product from explicitly selected specification documents through TDD, integration, and QA. | `docs/specs/dev-skill-spec.md` |
| `skill-builder` | Authors, scaffolds, converts, and regenerates skill packages. | `docs/plan/claude-to-codex-skill-import-spec.md`, `skill-builder-authoring-enhancement-spec.md`, `skill-builder-adaptive-enhancement-spec.md` |
| `skill-validator` | Independently assesses a selected skill or skill set. | `docs/plan/skill-validator-spec.md`, `skill-validator-adaptive-enhancement-spec.md` |

**The separation of duties is the framework's core invariant**, declared in each spec's authoring metadata and enforced by the workflows:

- **skill-builder** holds authoring custody. Custody is explicitly *not* quality evidence.
- **skill-validator** independently assesses: establishes an origin specification, snapshots exact bytes, runs bounded disposable trials under `trials/`, emits findings plus a proposed revision specification for human review. It never repairs, installs, or invokes the builder.
- **`dev`** owns product implementation directly and must not invoke a skill-authoring workflow for application code, or require the package validator for ordinary product tests.

A spec names its own build targets — authoring owner, development parent (`src/agents/skills`), independent assessor — in an authoring-metadata table marked **do not copy into the runtime workflow**. Those paths select one build; they must never appear as runtime defaults in a generated skill.

**Why "Adaptive": portability is the design contrast with the legacy framework.** `src/claude/` hardcodes `devforgeai-validate` gate calls and a fixed `devforgeai/specs/context/` artifact tree. These skills derive language, architecture, tools, layout, commands, thresholds, platforms, and delivery locations from runtime inputs instead. Git, an index, a service, a descriptor, an operational binding, MCP, or a plugin is never a prerequisite. The `adaptive-*` and `project-binding-*` schemas in each package carry that machinery. When the target project *is* DevForgeAI, its Rust requirement and ≥95% thresholds arrive as project-policy inputs — not as constants baked into the skill.

**Package shapes differ, and two of the gaps are unresolved against AGENTS.md — do not read them as design choices.** `skill-validator` is complete: `SKILL.md` + `references/` + `schemas/` + `scripts/` + `assets/` + `evals/` + `tests/`. The other two are not:

- **`dev` has no bound Python evaluation artifacts at all** — no `scripts/`, `schemas/`, `evals/`, or `tests/` in either copy. Its only `.jsonl` is `assets/execution-record.jsonl`, a runtime template, not eval cases.
- **`src/agents/skills/skill-builder` is missing its harness** — `evals/`, `tests/`, `graders.py`, and `run_evaluation.py` exist only in `.agents/skills/skill-builder/`, yet its own spec names "the development skill `skill-builder` and its required evaluation artifacts" as the authorized deliverable.

By AGENTS.md §Mandatory Framework Language those are **incomplete builds**, not stylistic variation. This is a reported observation, not an acceptance decision — confirm with the maintainer before treating either as finished or as a pattern to copy for a new skill.

Every validation run creates a fresh UTC directory at `docs/plan/skill-validations/<target-name>/<run-id>/`, disjoint from the target, and records `SOURCE_CHANGED` via `readback` rather than trusting a stale snapshot.

Future plugin identity is `devforgeai` (display name `DevForgeAI`); packaging is deferred.

## Stale facts in AGENTS.md and spec headers

AGENTS.md remains the authoritative policy document, but several of its factual statements are stale. Trust this file on these points:

- **It describes `src/agents/skills/` as containing "`skill-builder` and `skill-validator`" and never mentions `dev`.** There are three skills; `dev` is authored and present.
- **`docs/specs/dev-skill-spec.md` frontmatter says `status: proposed` and `package_status: not_authored`.** The package exists at `src/agents/skills/dev/`. The frontmatter was not updated after authoring — do not read it as "not built yet."
- It says skill-builder's `tests/` and `scripts/run_evaluation.py` are absent. They exist — but only in **`.agents/skills/skill-builder/`**, not in the `src/agents/` development copy. AGENTS.md is right that they are missing from where it looked; it is the *inventory* that is incomplete, and the development copy's absence is an open gap rather than settled drift (see above).
- It treats `devforgeai-validate` as a proposed interface and says no runnable CLI exists. It is installed and real (v0.3.0, 158 subcommands) — and now legacy. Its *source* is still absent from this repository, which is what keeps the proposed-Rust-workspace language in `docs/plan/` accurate.

## Conventions

Four-space Python indent, `snake_case` functions and modules, `PascalCase` classes. Skill directories are kebab-case; entry instructions are always `SKILL.md`. Preserve existing JSON/YAML schema field names. Avoid unrelated formatting changes. Commit subjects are concise and imperative, optionally prefixed `docs:`, `fix:`, or `test:`.
