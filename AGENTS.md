# Repository Guidelines

## Project Structure & Module Organization

DevForgeAI provides specification-driven Claude Code planning skills. Brainstorm, PRD and documents-updater are implemented; architecture and epic have specifications.

- `docs/specs/spec/SPEC-001.md` through `SPEC-004.md` define the planning workflows and `SPEC-006.md` the documents updater. Every document uses a typed folder, e.g. `docs/specs/prd/PRD-002.md`.
- `src/templates/` holds staged document templates; `src/templates/skill/` contains skill, provenance, and evaluation examples.
- `src/schemas/` holds document JSON Schemas.
- `src/claude/DevForgeAI/` is the `devforgeai` plugin source: `.claude-plugin/plugin.json`, the built skills in `skills/` (`brainstorm`, `prd`, `documents-updater`), and their eval suites in `evals/<skill>/`. It deploys to `.claude/skills/devforgeai/`.
- `src/tools/session-archive/` holds separate user-level hooks (SPEC-005, draft).

Some specs describe another layout. Verify paths against disk; see `CLAUDE.md` for mappings. Edit plugin source; deployment is the owner's step.

## Build, Test, and Development Commands

No project-wide build system, formatter, or linter is configured. Run from the repository root in WSL:

- `rg --files src docs` inventories source and documentation.
- `python3 -m json.tool src/claude/DevForgeAI/.claude-plugin/plugin.json` checks manifest JSON syntax.
- `python3 -m unittest discover -s src/tools/session-archive -p 'test_*.py'` runs archive tests.
- In a valid Git checkout, `git diff --check` checks patch whitespace.

Follow `docs/runbooks/brainstorm-manual-test.md` for manual checks and `claude plugin eval` commands. `devforgeai check` is unavailable.

## Coding Style & Naming Conventions

Use Markdown with YAML frontmatter and two-space indentation for YAML/JSON. Follow `src/templates/README.md`: quote free-text YAML values, use exactly `yaml items` for citable blocks, and keep one collection key per block.

Keep IDs stable; deprecate instead of deleting or renumbering. Example output path: `docs/specs/story/STORY-001.md`. Use lowercase hyphenated skill names matching directory and frontmatter. Keep `SKILL.md` concise, references separate, and provenance in `provenance.yaml`.

## Testing Guidelines

Archive tests use standard-library `unittest` and `test_*.py` names. Evaluation templates live under `src/templates/skill/evals/`; use descriptive cases such as `triggers-on-request`. Cover triggering, unrelated requests, and `VER-` obligations. Seed fixtures through `case.yaml`; compare against the no-plugin baseline. Follow `CLAUDE.md` for the eval threshold (0.8 per case over three runs). No code-coverage threshold is configured. Record unrun checks explicitly.

## Commit & Pull Request Guidelines

This workspace is a git repository, but most files are untracked, so check `git status` before relying on history. Use concise imperative subjects, such as `docs: clarify brainstorm validation`. In valid Git checkouts, use an isolated worktree. PRs should describe scope, cite SPEC/VER or issue IDs, and report checks and limitations.

## Agent-Specific Instructions

Before troubleshooting in WSL, consult `/mnt/c/Users/bryan/.codex/code/papercuts.md` and `/mnt/c/Users/bryan/.claude/code/papercuts.md` (Windows: `C:/Users/bryan/...`). Append obstacles only to the Codex log: date, symptom, fix/status, project. Preserve entries, avoid duplicates and secrets, and verify fixes before reuse.
