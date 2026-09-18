# Repository Guidelines

## Project Structure & Module Organization

This workspace contains DevForgeAI skill definitions, supporting scripts, and evaluation evidence.

- `src/agents/skills/skill-builder/` contains the builder's instructions, Python scripts, tests, evaluation profiles, and references.
- `src/claude/skills/` contains workflow skills organized into `SKILL.md`, `phases/`, `references/`, `scripts/`, and `assets/` where applicable.
- `src/claude/agents/` contains agent definitions.
- `.claude/` contains local agent, command, and skill copies. Check the intended source and installation workflow before updating duplicate files.
- `docs/plan/` holds planning documents and retained evaluation evidence.

## Build, Test, and Development Commands

Run commands from the workspace root. No root build manifest or application launch command is present in this snapshot.

- `python -B -X utf8 -m unittest discover -s src/agents/skills/skill-builder/tests -v` runs the builder regression suite without writing bytecode.
- `python -B -X utf8 src/agents/skills/skill-builder/scripts/run_evaluation.py --help` lists evaluator inputs and options. Follow the package's `references/evaluation.md` for complete evaluation commands.
- `python -m pip install -r src/claude/skills/spec-driven-qa/scripts/requirements.txt` installs dependencies for the QA utilities; use an isolated virtual environment.

## Coding Style & Naming Conventions

Follow neighboring files: use four-space Python indentation, `snake_case` functions and modules, and `PascalCase` classes. Use descriptive Markdown headings and relative links within skill packages. Skill directories use kebab-case, such as `spec-driven-stories`; entry instructions use `SKILL.md`. Preserve existing JSON/YAML schemas and field names. No repository-wide formatter configuration was found; avoid unrelated formatting changes.

## Testing Guidelines

Builder tests use Python `unittest`, with `test_*.py` files and `test_*` methods. Add focused regression cases for behavior changes, including rejection paths and malformed inputs. Use temporary directories and synthetic fixtures, following the existing tests. No workspace-wide coverage threshold is configured. Record the exact command and result; evaluator observations do not establish acceptance.

## Commit & Pull Request Guidelines

Git metadata is absent from this workspace, so historical commit conventions cannot be verified. Use concise, imperative subjects, optionally prefixed with `docs:`, `fix:`, or `test:`. Keep changes focused. PR descriptions should explain the affected workflow, behavior changes, related issues, and validation results or limitations. Preserve existing evidence under `docs/plan/`; place new run outputs in distinct directories.
