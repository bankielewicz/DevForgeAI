# Repository Guidelines

## Layout and ownership

| Path | Purpose |
| --- | --- |
| `src/agents/skills/` | Development skill packages, scripts, evaluations, and references. |
| `.agents/skills/` | Operational skill copies. |
| `devforgeai/` | Rust application and experiments; main manifest: `devforgeai/Cargo.toml`. |
| `src/claude/skills/`, `src/claude/agents/` | Claude workflow skills and agent definitions. |
| `.claude/` | Local agent, command, and skill copies. |
| `docs/plan/` | Specifications, plans, and retained evaluation evidence. |

- Edit the selected source package. Installation and operational-copy changes require explicit authorization; development edits do not update installed copies.
- Preserve unrelated files and prior evidence. Write new run evidence to a distinct directory under the applicable evidence contract.
- Stay within the requested scope. Do not install components or alter startup configuration merely to complete validation.
- Use request_user_input tool to resolve ambiguities with clickable or tabbed choices.

## Repository changes and delivery

Before modifying repository source, skills or documentation—or committing,
pushing or opening a PR—read and follow
[Worktree and PR delivery](docs/workflows/worktree-and-pr-delivery.md).

Do not load that procedure for discussion or read-only inspection.
If the task later becomes a change request, load it before the first edit.

A change request authorizes the task worktree, branch, commits, push and
draft PR described by that procedure, unless the user limits those effects.
Preserve unrelated work. Merging, installation and deployment require
separate authorization.

Keep the selected skill's responsibility boundaries intact. In particular,
skill-builder authoring does not automatically invoke skill validation.

## Commands and execution environment

When creating execution evidence, relocating retained artifacts or considering
cleanup, read [Artifact retention](docs/workflows/artifact-retention.md). Keep
routine source-only work free of that additional context unless it needs it.

Run from the workspace root unless the selected package documents another directory. Inspect actual manifests, tools, scripts, and tests before using commands from specifications or old reports.

- For Rust changes, use the selected Cargo manifest and lockfile. Run formatting, Clippy, tests, and executed-line coverage after discovering the installed toolchain and coverage collector.
- For skill evaluation, follow the selected package contract and the validator's [evaluation instructions](src/agents/skills/skill-validator/references/evaluation.md). Discover its interfaces with:

  ```powershell
  python -B -X utf8 src/agents/skills/skill-validator/scripts/run_evaluation.py --help
  python -B -X utf8 src/agents/skills/skill-validator/scripts/observe.py --help
  ```

- Prefer native Windows tools for `C:\Projects\DevForgeAI`. Use WSL for required Linux behavior or tooling, and Linux-resident files for sustained Linux workloads. `/mnt/c/...` and Windows access through `\\wsl$\...` or `\\wsl.localhost\...` cross the filesystem boundary.
- Preserve the selected checkout. Before using another location, verify its resolved path, source identity, local changes, applicable instructions, and branch/HEAD when Git metadata exists. Moving, cloning, synchronizing, or switching checkouts solely for performance requires authorization.
- Discover WSL distributions/options with `wsl --list --verbose` and `wsl --help`. Select distribution and directory explicitly; verify `pwd -P` and `command -v`. Use `Get-Command` on Windows. A Windows executable remains a Windows process when launched from WSL or a UNC directory.
- Use scoped `rg` searches and batch related reads. Keep platform-specific virtual environments, dependencies, and build outputs separate; use an isolated environment for Python dependency installation.
- Use bounded, noninteractive commands, preserve exit codes, and quote for the executing shell. Prefer scripts over deeply nested PowerShell/Bash commands. Normal host permissions apply to WSL.
- Run Windows service, hook, and tray acceptance checks on Windows. Support performance claims with the measured workload, platform, filesystem location, command, and elapsed time.

## Framework authority and skill evaluation

- Implement framework CLI/service behavior, Codex/Git/GitHub hooks, phase gates, validators, mutation brokers, and acceptance decisions in **compiled Rust**. Declarative hooks and CI may invoke Rust; shell, YAML, Python, skills, and model-written status files cannot duplicate or replace its policy or authority.
- Python utilities, skill evaluations, reviewer advice, and index observations produce evidence only. They cannot authorize mutations, advance phases, waive gates, or grant framework acceptance. Rust authority must independently validate evidence, provenance, completeness, and thresholds. Follow the [compiled-Rust design](docs/plan/devforgeai-codex-rust-enforcement-design.md); the index daemon is separate from the protected authority service.
- Skill builds require a Python JSONL runner, deterministic graders, fixtures, expected results, schema, dependency/runtime information, and artifact digests/manifests. Missing or modified required evaluation artifacts make a build incomplete.
- Distinguish specified interfaces, structural checks, native execution, and framework acceptance. Help output, an exit code, or a model-written PASS cannot substitute for required evidence. Claim enforced gates only after their Rust implementation is qualified.

## Development and QA

For code generation and behavior changes, follow **red -> green -> refactor -> QA**:

1. Execute a focused test before production changes and retain its expected failure. Setup or tool errors do not count as red.
2. Implement the minimum behavior that passes and retain the result. Do not substitute stubs, hardcoded passing outputs, or weakened assertions.
3. Refactor while preserving behavior; rerun affected tests after changes.
4. Run applicable regression, integration, negative-path, platform, formatting/static-analysis, and coverage checks. Exercise acceptance scenarios, including invalid/denied requests and failure recovery.

Use `test_*.py` files, `test_*` methods, temporary directories, and synthetic fixtures for Python `unittest`. Keep skill authoring and independent evaluation separate where their contracts require it; TDD does not expand a skill's role.

Framework checks must meet both thresholds:

- **Executed-line coverage >=95%** of first-party executable framework code. Declare the source denominator and exclusions before running. Exclude vendored/generated third-party code and test fixtures, never uncovered first-party behavior. Report branch coverage separately where supported.
- **Required-case pass rate >=95%**, calculated as `100 * passing required cases / all required cases`. Failed, errored, skipped, blocked, and unexecuted required cases remain in the denominator. Count each case once; retries neither erase prior evidence nor inflate counts.
- Report raw counts and percentages for each required platform and overall. Do not round a result below 95% up to a pass or use another platform's results to qualify an untested target.
- Numeric thresholds do not waive a failed mandatory scenario, unresolved regression, or authority/security invariant.

Record the working directory, tool versions, exact commands, exit codes, and report paths. Mark missing tools, unperformed checks, and missing measurements `NOT_RUN` or `BLOCKED`; do not estimate passing results.

For documentation-only changes, review facts, links, requirements, and consistency. Report the checks actually performed; do not invent TDD, coverage, or runtime acceptance.

## Specifications and terminal access

- Define inputs, outputs, ownership, required behavior, failure paths, dependencies, and testable acceptance criteria. Read companion contracts together, including the index service and query CLI specifications.
- Resolve ambiguity and contradictions. Record any ungrounded essential decision and affected work instead of inventing an answer or claiming readiness.
- Write concrete actions and observable outcomes. Omit decorative gates, unexecuted checklists presented as evidence, unsupported acceptance flags, and restatements of goals.
- Framework work must be authorable, buildable, invocable, and verifiable from the Codex CLI terminal on the declared host. MCP, browser, or GUI access cannot be the sole workflow.
- The optional Windows tray must expose equivalent lifecycle, project, and index operations through Rust CLI commands and automated checks. Report native visual QA separately; terminal tests do not verify rendering.

## Claude second opinions

Use `$advisor` when requested or materially needed for an approach, recurring failure, completion claim, or conflicting evidence. Routine implementation, QA, and skill authoring do not require a review.

Read and follow the installed [advisor skill](.agents/skills/advisor/SKILL.md) and [execution contract](.agents/skills/advisor/references/execution.md) for options, authentication, preflight, briefing, evidence, follow-ups, and verdict handling.

- Invoke `.agents/skills/advisor/scripts/advisor_run.py` by absolute path. Keep runs under `docs/plan/advisor-runs/` and initial inputs in a sibling intake directory.
- Allow at most two reviewer process attempts per review, including retries and follow-ups, using the same immutable request and run directory. Defaults: USD 2.00 total, USD 1.00 reserved per attempt, 300-second timeout. Do not reclaim unused allocations or reset attempt accounting.
- Investigate incomplete attempts or stale locks before retrying. Do not delete evidence, raise limits, relax read-only restrictions, change saved authentication, or edit/reinstall either advisor package to force completion. Follow normal host approvals.
- Verify load-bearing citations and distinguish execution success, valid response, and supported advice. Report findings, limitations, and artifact paths, then return to the original task.

## Style and delivery

Follow neighboring style: four-space Python indentation, `snake_case` functions/modules, `PascalCase` classes, rustfmt, and package Clippy configuration. Preserve JSON/YAML schemas and field names. Use descriptive Markdown headings, relative package links, kebab-case skill directories, and `SKILL.md` entry files. Avoid unrelated formatting.

When using Git, use concise imperative subjects, optionally prefixed with `docs:`, `fix:`, or `test:`. Keep changes focused; PR descriptions should explain behavior, related issues, validation, and limitations.
