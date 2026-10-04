# Repository Guidelines

## Project Structure & Module Organization

DevForgeAI provides specification-driven planning skills for Claude Code and a separate Codex source package. Claude implements brainstorm, PRD, architecture, epic, context, documents-updater, git and spec-lookup, plus a progress tracker (SPEC-012, SPEC-013). The git skill's source is SKL-006 v3, which with SPEC-007 v3 is in review: native and manual qualification are pending, and SKL-006 v2 is the last approved version. Codex contains brainstorm, PRD, architecture and documents-updater; epic, context, git and spec-lookup are not ported. The Codex PRD and architecture ports are drafts, not qualified; source presence does not establish acceptance.

- `docs/specs/spec/SPEC-001.md` through `SPEC-004.md` define the planning workflows, `SPEC-005.md` (draft) the session-archive hooks, `SPEC-006.md` the documents updater, `SPEC-007.md` (in-review v3; v2 approved) the git workflow, `SPEC-008.md` (stub) the QA review, `SPEC-009.md` (draft, not built) the story skill, `SPEC-010.md` (in-review v3; v2 approved, not built) the GitHub post skill, `SPEC-011.md` the context skill, `SPEC-012.md` and `SPEC-013.md` the progress tracker's core and Claude Code adapter, and `SPEC-014.md` the spec-lookup skill. Each spec's §9 records its build and evaluation results. Every document uses a typed folder, e.g. `docs/specs/prd/PRD-002.md`.
- `src/templates/` holds staged document templates; `src/templates/skill/` contains skill, provenance, and evaluation examples.
- `src/schemas/` holds document JSON Schemas.
- `src/claude/DevForgeAI/` is the `devforgeai` plugin source: `.claude-plugin/plugin.json`, the built skills in `skills/` (`brainstorm`, `prd`, `architecture`, `epic`, `context`, `documents-updater`, `git`, `spec-lookup`), the `spec-lookup` agent in `agents/`, the progress tracker's core in `progress/` and its Claude Code adapter in `hooks/`, and the eval suites in `evals/<skill>/`. It deploys to `.claude/skills/devforgeai/`.
- `src/codex/devforgeai/` holds the Codex manifest (`.codex-plugin/plugin.json`), skills, tests, evals and import reports. Its README and per-skill reports describe provider adaptations and qualification limits.
- `src/tests/` holds the Claude plugin's tests, one folder per skill (script and structure tests, evaluation generators and graders) plus `progress/` for the progress tracker. Codex tests and generators live in its package's `tests/`.
- `src/tools/session-archive/` holds separate user-level hooks (SPEC-005, draft).

Some specs describe another layout. Verify paths against disk; see `.claude/rules/spec-paths.md` for mappings, `CLAUDE.md` for Claude workflows, and the Codex package README for its current contents. Edit the relevant provider's source; deployment is the owner's step. Keep historical import evidence intact.

## Build, Test, and Development Commands

No project-wide build system, formatter, or linter is configured. Run from the repository root in WSL:

- `rg --files src docs` inventories source and documentation.
- `python3 -m json.tool src/claude/DevForgeAI/.claude-plugin/plugin.json` checks manifest JSON syntax.
- `python3 -m json.tool src/codex/devforgeai/.codex-plugin/plugin.json` checks the Codex manifest JSON syntax.
- `python3 -B -m unittest discover -s src/tools/session-archive -p 'test_*.py'` runs archive tests.
- `python3 -B -m unittest discover -s src/tests/documents-updater -p 'test_*.py'` runs Claude Markdown checker tests.
- `python3 -B -m unittest discover -s src/tests/git -p 'test_*.py'` runs the Claude git skill's script tests.
- `PYTHONDONTWRITEBYTECODE=1 python3 -B -m pytest -q -p no:cacheprovider src/tests/progress` runs the progress tracker's tests.
- `python3 -B -m unittest discover -s src/codex/devforgeai/tests -p 'test_*.py'` runs Codex package tests.
- `git diff --check` checks patch whitespace.

Follow `CLAUDE.md` and `docs/runbooks/brainstorm-manual-test.md` for Claude evals and manual checks. Follow `src/codex/devforgeai/evals/<skill>/README.md` where present for native Codex evaluations; Claude evals do not qualify Codex. `devforgeai check` is unavailable; never trust a similarly named executable on PATH.

## Coding Style & Naming Conventions

Use Markdown with YAML frontmatter and two-space indentation for YAML/JSON. Follow `src/templates/README.md`: quote free-text YAML values, use exactly `yaml items` for citable blocks, and keep one collection key per block.

Keep IDs stable; deprecate instead of deleting or renumbering. Example output path: `docs/specs/story/STORY-001.md`. Use lowercase hyphenated skill names matching directory and frontmatter. Keep `SKILL.md` concise, references separate, and provenance in `provenance.yaml`.

Use each skill's `assets/` templates and `references/output-rules.md` as its output contract. Keep skill metadata versions aligned with provenance. Preserve user-owned decisions and historical authorship when adapting between providers.

## Testing Guidelines

Archive tests use standard-library `unittest` and `test_*.py` names. Evaluation templates live under `src/templates/skill/evals/`; cover triggering, unrelated requests and `VER-` obligations. Seed fixtures through `case.yaml`; compare against the no-plugin baseline. Edit generated fixtures and graders in their provider's generator, then regenerate the suite. Follow each suite's evaluation contract; the inherited threshold is 0.8 per case over three runs. No code-coverage threshold is configured. Record unrun checks as `NOT_RUN`; static checks and aggregate scores do not waive manual obligations or establish deployment parity.

Never investigate a failing test by changing the working tree (ADR-005 D7; interim, until a dev skill implements it): record a baseline test run before the first change, compare old code only in a disposable worktree (`git worktree add --detach <path> <commit>`) or with `git show <commit>:<path>`, and commit work in progress before each full test run. Never restore, check out, stash, reset, clean or re-download files into the working tree to investigate.

## Commit & Pull Request Guidelines

Check `git status` before editing and preserve unrelated changes. The repository was initially imported in PR #1; earlier evolution is recorded in document Change Logs. Use an isolated worktree (see ADR-001) and concise imperative subjects, such as `docs: clarify brainstorm validation`. PRs should describe scope, cite SPEC/VER or issue IDs, and report checks and limitations.

## Agent-Specific Instructions

Before troubleshooting in WSL, consult `/mnt/c/Users/bryan/.codex/code/papercuts.md` and `/mnt/c/Users/bryan/.claude/code/papercuts.md` (Windows: `C:/Users/bryan/...`). Append obstacles only to the Codex log: date, symptom, fix/status, project. Preserve entries, avoid duplicates and secrets, and verify fixes before reuse.
