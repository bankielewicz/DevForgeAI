# Repository Guidelines

## Project Structure & Module Organization

DevForgeAI is a spec-driven Claude Code plugin. `src/claude/DevForgeAI/` contains the plugin manifest, `skills/<name>/` and `evals/<name>/`. Each skill owns its `SKILL.md`, `provenance.yaml`, `assets/` and `references/`. Canonical schemas live in `src/schemas/`; pending templates and examples live in `src/staging/`. Project specifications, stories, ADRs and handoffs live in `docs/specs/`.

`.claude/skills/devforgeai/` is the generated, gitignored operational copy. Edit source, then deploy; never edit that copy manually. Do not create symlinks under `src/`.

## Build, Test, and Development Commands

Use a separate worktree and `story/STORY-NNN-<slug>` branch for each skill story. Follow the guarded deployment commands in [ADR-001](docs/specs/adr/ADR-001.md) before starting `claude --worktree <name> -n <name>`. Run validation from the worktree root:

```bash
# Confirm deployed files match source, excluding eval reports.
diff -r -x results src/claude/DevForgeAI .claude/skills/devforgeai
# Validate the plugin manifest.
claude plugin validate .claude/skills/devforgeai --strict
# Run behavioral evaluations from a plain terminal.
claude plugin eval .claude/skills/devforgeai --allow-tools Write Edit --scaffold --no-publish --threshold 0.8
```

Redeploy after source changes, then run `/reload-plugins`. `/skills` doesn't show the plugin path: after a skill runs, confirm the path from the "Base directory for this skill" line in the session transcript (`~/.claude/projects/<project-dir>/<session-id>.jsonl`).

## Coding Style & Naming Conventions

Match existing Markdown and two-space YAML/JSON indentation; quote free-text YAML values. Use `yaml items` fences for citable records. Name documents by ID in singular directories, such as `docs/specs/story/STORY-003.md`; keep topics in `title`. Use lowercase, hyphenated skill and eval names. Preserve stable item IDs and place each upstream link only on its owner. Leave author-written hashes null. No repository formatter or linter is configured.

## Testing Guidelines

Use `claude plugin eval` cases mapped to specification `VER-NN` obligations. Give file graders literal paths and check fixtures against canonical schemas. Every case must score at least 0.8; follow the story's repeat-run and manual-verification requirements. Read `aggregate-result.json`, report actual results, and run the full plugin suite before a PR. Perform manual checks in scratch fixture repositories. Manifest validation alone does not establish behavior.

## Commit & Pull Request Guidelines

Follow the history's story-prefixed messages, for example `STORY-003: add architecture provenance graders`. PRs should identify the story/spec, explain changes, and include eval results, report paths, manual evidence and deviations. Record durable completion in the story's Definition of Done.

## Agent Instructions

Read `CLAUDE.md` and the applicable handoff. Resolve conflicts using SPEC > STORY > ADR > templates. Obtain explicit approval before specification edits; include version, Change Log and reviewed-link updates together. Honor handoff scope and publication restrictions.
