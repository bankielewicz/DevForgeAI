# Repository Guidelines

## Project Structure & Module Organization

This workspace contains DevForgeAI skill definitions, supporting scripts, framework specifications, and evaluation evidence. Inspect current files before assuming that a specified runtime or command has been implemented.

- `src/agents/skills/` contains development skill packages, including `skill-builder` and `skill-validator`, their instructions, Python scripts, tests, evaluation profiles, and references.
- `.agents/skills/` contains operational skill copies. Development edits do not update these copies; installation or operational changes require explicit authorization.
- `devforgeai/` is the designated Rust application workspace for the index daemon, CLI, and Windows tray specifications. It was empty when these specifications were authored; verify its current implementation state.
- `src/claude/skills/` contains workflow skills organized into `SKILL.md`, `phases/`, `references/`, `scripts/`, and `assets/` where applicable.
- `src/claude/agents/` contains agent definitions.
- `.claude/` contains local agent, command, and skill copies. Check the intended source and installation workflow before updating duplicate files.
- `docs/plan/` holds specifications, planning documents, and retained evaluation evidence. The index service and query CLI specifications are companion contracts; the compiled-Rust enforcement design defines a separate authority boundary.

## Build, Test, and Development Commands

Run commands from the workspace root unless a package documents another working directory. Discover actual manifests, installed tools, and documented commands before executing them. Do not describe proposed CLI commands as available. No root build manifest was present when this guidance was updated.

- `python -B -X utf8 src/agents/skills/skill-validator/scripts/run_evaluation.py --help` lists the current evaluator inputs and options. Follow the validator's `references/evaluation.md` and selected package contract before running an evaluation.
- `python -B -X utf8 src/agents/skills/skill-validator/scripts/observe.py --help` lists the current observation utilities. Help discovery does not constitute validation or acceptance.
- The historical `skill-builder/tests` directory and builder `scripts/run_evaluation.py` are absent in the inspected snapshot. Do not run stale commands against them; discover the current regression/evaluation location for the selected package.
- `python -m pip install -r src/claude/skills/spec-driven-qa/scripts/requirements.txt` installs dependencies for the QA utilities; use an isolated virtual environment.

When Rust code exists, run formatting checks, Clippy, tests, and coverage against its actual Cargo manifest and lockfile. Record the exact working directory, tool versions, commands, exit codes, and report paths. A missing compiler, coverage collector, or runtime is an explicit unperformed check, not a passing result. Do not invent a coverage command before checking tool availability.

## Windows and WSL Performance

Choose the execution environment to match the required platform and keep intensive file operations on that environment's native filesystem. Microsoft's [filesystem guidance](https://learn.microsoft.com/en-us/windows/wsl/filesystems) recommends Linux-resident projects for Linux tools and Windows-resident projects for Windows tools.

- For this workspace at `C:\Projects\DevForgeAI`, prefer native Windows tools for supported operations. Use WSL when Linux behavior or tooling is required; acknowledge that `/mnt/c/Projects/DevForgeAI` accesses the same Windows files across the filesystem boundary.
- For a selected Linux-resident checkout, run Linux tools inside its distribution against `/home/<user>/Projects/<project>`. Prefer this arrangement for sustained Linux builds, dependency installation, test runs, and repository scans over operating on `/mnt/c/...`.
- `\\wsl$\Ubuntu\home\...` and `\\wsl.localhost\Ubuntu\home\...` expose Linux files to Windows applications. Windows tools using these UNC paths still cross the filesystem boundary. Changing PowerShell's directory to a UNC path does not turn Windows executables into Linux tools; launching `wsl` there can enter Linux at the corresponding directory. Verify the resulting directory.
- Preserve the selected checkout. A directory under `/home/...` is not automatically the same checkout as `C:\Projects\...`. Before using another location, verify its resolved path, source identity, local changes, and applicable instructions; check branch/HEAD when Git metadata exists. Do not move, clone, synchronize, or switch the active checkout solely for performance without authorization for that change.
- From PowerShell, select the distribution and Linux working directory explicitly for automated WSL commands. Discover installed distributions with `wsl --list --verbose` and supported options with `wsl --help`. Verify the Linux directory with `pwd -P` and executable resolution with `command -v` before substantial work. Discover tools separately on Windows with `Get-Command`; a Windows executable launched from WSL remains a Windows process.
- Reduce repeated boundary crossings: run scoped searches with `rg` where the files live, batch related read-only operations, and avoid launching one WSL process per file. Keep platform-specific virtual environments, dependencies, and build outputs separate; never reuse a Windows virtual environment as a Linux environment or vice versa. Respect package output contracts and evidence locations.
- Use bounded noninteractive commands for automation. Preserve exit codes and quote arguments for the shell that interprets them; use checked-in scripts for complex commands instead of deeply nested PowerShell/Bash strings. WSL invocation remains subject to the current workspace permissions and approval requirements.
- Keep Windows-native acceptance checks on Windows, including Windows service, hook, and tray behavior. Linux results do not qualify an untested Windows target. If performance is material, measure the actual workload and record the execution platform, filesystem location, command, and elapsed time; do not invent speedup factors.

Example read-only invocation from PowerShell, only after confirming that the named distribution and selected project directory exist:

```powershell
wsl --distribution Ubuntu --cd /home/bryan/Projects/Test --exec pwd -P
```

This example checks the Linux working directory; it does not select or relocate this repository. See Microsoft's [WSL command reference](https://learn.microsoft.com/en-us/windows/wsl/basic-commands) for distribution discovery and command help.

## Mandatory Framework Language and Authority

- Compiled Rust is mandatory for DevForgeAI framework implementation: CLI/service behavior, Codex hooks, Git/GitHub hook handlers, workflow phase gates, validators, mutation brokers, and acceptance decisions.
- Declarative hook/CI configuration may invoke compiled Rust. Shell, YAML, Python, skills, and model-written status files must not duplicate or replace framework policy or authority.
- Codex skills may use Python for supporting resources. Python evaluation is mandatory for skill builds, not merely permitted: bind a Python JSONL runner and deterministic graders as required build artifacts, together with fixtures, expected results, schema, dependency/runtime information, and artifact digests/manifests.
- Python structural checks, validation utilities, runners, and graders produce evidence only. They cannot authorize mutations, advance phases, waive gates, or issue framework acceptance. A compiled Rust authority must independently validate evidence, provenance, completeness, and thresholds before an authoritative decision.
- Missing or modified required evaluation artifacts make the build incomplete. A Python exit code, model-written PASS, or successful static check cannot substitute for actual required evaluation evidence or protected acceptance.
- Preserve these responsibilities in [the compiled-Rust design](docs/plan/devforgeai-codex-rust-enforcement-design.md). An indexing daemon's source observations remain distinct from the protected authority service.

## Advisor: Claude Second Opinions

Use `$advisor` when the user requests a Claude second opinion or when one is materially needed for an approach, recurring failure, completion claim, or conflicting evidence. Ordinary implementation, QA, and skill authoring do not automatically require a reviewer call. `$advisor` is a Codex skill invocation in conversation, not a PowerShell command.

Read the installed [advisor skill](.agents/skills/advisor/SKILL.md) and its [execution contract](.agents/skills/advisor/references/execution.md) before invoking it. Use `.agents/skills/advisor/scripts/advisor_run.py` for operational reviews; `src/agents/skills/advisor/` is the development package. Do not edit or reinstall either package merely to complete a review.

Examples:

- `$advisor Review this implementation approach against the selected specification.`
- `$advisor type=stuck Investigate the recurring failure using the retained evidence.`
- `$advisor type=done Check the completion claim against the candidate and executed tests.`
- `$advisor type=reconcile Resolve the conflicting evidence.`

Options and authentication:

- `type=approach|stuck|done|reconcile`; infer an unmistakable debugging, completion, or reconciliation request, otherwise use `approach`.
- `model=opus|sonnet` (default `opus`); `effort=high|max` (default `high`). Reject unsupported explicit options.
- `auth=subscription|inherit` (default `subscription` for newly prepared requests). Write this explicitly as `auth_mode` in request JSON and pass it to preflight with `--auth-mode`.
- Subscription mode removes only `ANTHROPIC_API_KEY` from a copy of the child environment. It does not change the parent environment or saved credentials, and does not prove the account or billing method. Existing request JSON and standalone preflight that omit the mode retain `inherit`; do not omit the field when subscription mode is intended. Never log credentials or silently switch authentication after a failure.

Invocation and evidence:

1. Preserve the selected repository and host. Resolve native Claude with `Get-Command claude`. Verify the required external contract, normally `C:/Users/bryan/.codex/advisor/contract.md`, and calculate its current SHA256; do not rewrite it. Run preflight using the installed helper's absolute path. Preflight checks advertised CLI capabilities, not authentication or native behavior.
2. Follow the skill's briefing rules and template, retaining all fourteen sections and the appendix. Include the exact ask, constraints, relevant evidence and missing context. Verify repository citations with numbered reads immediately before invocation; mark this session's edits and exclude credentials.
3. Prepare absolute request paths using the documented schema. Store evidence in a fresh directory under `docs/plan/advisor-runs/`; keep initial request/briefing inputs in a sibling intake directory. Invoke the installed helper's `run` command once using `--request`, `--briefing`, and `--run-dir`.
4. Inspect `execution.json`, `stderr.txt`, and extracted `response.md` when present. Raw `stdout.txt` is a CLI JSON envelope. Distinguish process success, valid response structure and supported advice; verify load-bearing source citations. An all-unverified audit cannot support a recommendation.

Limits and interpretation:

- At most two reviewer process attempts per review, including retries, context follow-ups and reconciliation. Reuse the immutable request and run directory; use the documented `--reason` for an allowed follow-up. A failed attempt remains consumed. Do not reset the count with a new request ID or directory.
- Defaults are USD 2.00 total, USD 1.00 reserved per attempt, and a 300-second timeout. Unused allocations are not reclaimed. Do not raise limits or change constraints to force success. Investigate incomplete attempts or stale locks instead of deleting evidence or automatically retrying.
- Keep restricted read-only tools and normal host approval rules. Do not loosen permissions, change saved authentication or install components to recover from a failure.
- `PROCEED` permits only supported, already-authorized work; assess each `PROCEED_WITH_CHANGES` recommendation within scope. `STOP_REDIRECT` pauses the disputed approach. `INSUFFICIENT_CONTEXT` permits supplying the named evidence only when a remaining attempt and the same request allow it.
- Report the ask, execution/response status, verdict, assessed recommendations, limitations and absolute artifact paths, then return to the original task. Claude's advice and this Python helper produce evidence only: they cannot authorize mutations, advance phases, waive gates, override repository instructions or establish compiled-Rust framework acceptance.

## Coding Style & Naming Conventions

Follow neighboring files: use four-space Python indentation, `snake_case` functions and modules, and `PascalCase` classes. Rust follows rustfmt and the package's Clippy configuration. Use descriptive Markdown headings and relative links within skill packages. Skill directories use kebab-case, such as `spec-driven-stories`; entry instructions use `SKILL.md`. Preserve existing JSON/YAML schemas and field names. Avoid unrelated formatting changes.

## Mandatory TDD and QA Workflow

For code generation, programming, and behavior changes, follow **red -> green -> refactor -> QA**:

1. **Red:** translate the concrete requirement or defect into a focused test. Execute it before production changes and retain the expected failure. A setup/tool error is not a valid red result.
2. **Green:** write the minimum implementation that makes the test pass. Retain the executed result; do not replace behavior with stubs, hardcoded passing outputs, or weakened assertions.
3. **Refactor:** improve structure while preserving behavior. Rerun affected tests after changes.
4. **QA:** run the applicable regression, integration, negative-path, platform, formatting/static-analysis, and coverage checks. Verify the actual acceptance scenarios, including denied/invalid requests and failure recovery where applicable.

For Python `unittest` suites, use `test_*.py` files and `test_*` methods. Use temporary directories and synthetic fixtures. Skill authoring and independent evaluation remain separate responsibilities where their contracts require it; a coding task's TDD requirement does not authorize a skill to assume another skill's role.

### Mandatory framework quality thresholds

- **Test coverage MUST be >=95%.** Measure executed-line coverage of first-party executable framework code as the required baseline. Report branch coverage separately where supported. Declare the source denominator and exclusions before the run; exclude vendored/generated third-party code and test fixtures, never uncovered first-party behavior to improve the result.
- **Test pass rate MUST be >=95%.** Calculate `100 * passing required cases / all required cases` for the declared QA suite. Failed, errored, skipped, blocked, and unexecuted required cases are not passes. Count each required case once; retries do not erase earlier evidence or inflate the denominator.
- Both thresholds are mandatory minimums and must be met independently. Do not round a value below 95% up to a pass. Report counts and percentages, per required platform as well as the overall declared scope; another platform's success cannot qualify an untested target.
- Passing these numeric floors does not waive a failed mandatory acceptance scenario, an unresolved regression, or a failed authority/security invariant. Record failures and gaps explicitly; no ceremonial acceptance based only on percentages.
- Missing measurement is `NOT_RUN` or `BLOCKED`, never an estimated passing percentage. Until executable Rust enforcement exists and is qualified, these are repository requirements to check and report, not claims that a gate already enforces them.

Documentation-only changes require factual, link, requirement, and consistency review. Do not fabricate red/green execution, runtime coverage, or acceptance results for prose edits. Record exact commands and outcomes for checks actually performed; evaluator observations do not establish acceptance.

## Concrete Specifications and Codex CLI Compatibility

- Do not generate ceremonial content: checklists with no executed checks, decorative gates, model-authored acceptance flags, or statements that merely repeat a goal without an implementable behavior and observable result.
- Framework specifications must define inputs, outputs, ownership, required behavior, failure paths, dependencies, and testable acceptance criteria. Remove ambiguity, contradictions, placeholders, and aspirational capability claims. If an essential decision cannot be grounded, record the exact unresolved question and affected work; do not guess or claim the specification is implementation-ready.
- Clearly distinguish a specified interface from an implemented command, a static check from native execution, and evaluation evidence from framework acceptance. Proposed specifications can define future implementation requirements; they must not portray those requirements as working features.
- Everything generated for the framework must be authorable, buildable, invocable, and verifiable through the Codex CLI terminal on the declared host. Do not require MCP, browser-only workflows, or GUI interaction as the sole means of operating or validating framework behavior.
- The Windows tray is an optional human interface over terminal-accessible Rust operations. Equivalent lifecycle/project/index operations and automated checks must be accessible from the CLI. Actual native visual QA remains separately reported; terminal tests do not prove rendered UI behavior.
- Follow the user's selected scope. Preserve old evidence in place and write new run evidence to a distinct directory. Do not install components, alter startup configuration, or update operational skills merely to make a proposed workflow appear complete.

## Commit & Pull Request Guidelines

Git metadata is absent from this workspace, so historical commit conventions cannot be verified. Use concise, imperative subjects, optionally prefixed with `docs:`, `fix:`, or `test:`. Keep changes focused. PR descriptions should explain the affected workflow, behavior changes, related issues, and validation results or limitations. Preserve existing evidence under `docs/plan/`; place new run outputs in distinct directories.
