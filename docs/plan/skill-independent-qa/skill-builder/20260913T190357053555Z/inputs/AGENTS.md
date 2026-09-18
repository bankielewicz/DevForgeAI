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

## Mandatory Framework Language and Authority

- Compiled Rust is mandatory for DevForgeAI framework implementation: CLI/service behavior, Codex hooks, Git/GitHub hook handlers, workflow phase gates, validators, mutation brokers, and acceptance decisions.
- Declarative hook/CI configuration may invoke compiled Rust. Shell, YAML, Python, skills, and model-written status files must not duplicate or replace framework policy or authority.
- Codex skills may use Python for supporting resources. Python evaluation is mandatory for skill builds, not merely permitted: bind a Python JSONL runner and deterministic graders as required build artifacts, together with fixtures, expected results, schema, dependency/runtime information, and artifact digests/manifests.
- Python structural checks, validation utilities, runners, and graders produce evidence only. They cannot authorize mutations, advance phases, waive gates, or issue framework acceptance. A compiled Rust authority must independently validate evidence, provenance, completeness, and thresholds before an authoritative decision.
- Missing or modified required evaluation artifacts make the build incomplete. A Python exit code, model-written PASS, or successful static check cannot substitute for actual required evaluation evidence or protected acceptance.
- Preserve these responsibilities in [the compiled-Rust design](docs/plan/devforgeai-codex-rust-enforcement-design.md). An indexing daemon's source observations remain distinct from the protected authority service.

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
