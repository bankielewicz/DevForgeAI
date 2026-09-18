---
description: Reference-sweep migration — replace from_pattern with to_pattern across the dual-path codebase via spec-driven-migration skill (ADR-073).
argument-hint: "--from=<pattern> --to=<pattern> [--scope=<dirs>] [--exclude=<patterns>] [--dry-run] | --migration-id=<id> (resume)"
model: opus
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill, Bash(devforgeai-validate:*)
execution-mode: immediate
---

# /migrate-refs — Reference-Sweep Migration

Execute a dual-path mechanical migration: replace every occurrence of `from_pattern`
with `to_pattern` across a defined corpus, with phase-enforced classification,
parallel cluster execution, and global verification.

Per **ADR-073**, this command delegates to `spec-driven-migration`. The playbook
was proven on PR #68 (source-tree.md → source-tree/, 324 files, 0 dual-path drift).

---

## Quick Reference

```bash
# New migration: replace string X with string Y across the framework's dual-path tree
/migrate-refs --from='source-tree.md' --to='source-tree/' --scope='.claude/,src/claude/'

# Narrow scope + add exclusions
/migrate-refs --from='old-name' --to='new-name' \
              --scope='.claude/agents/,src/claude/agents/' \
              --exclude='_archive/,context-templates/'

# Dry run — emit classification + transform-rules; no edits
/migrate-refs --from='X' --to='Y' --scope='.claude/' --dry-run

# Resume a paused migration by ID
/migrate-refs --migration-id=source-tree-2026-05-19
```

---

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT enumerate scope files
- ❌ DO NOT classify any occurrence
- ❌ DO NOT author the transform-rules
- ❌ DO NOT edit any code or context file
- ❌ NEVER perform classification, transformation, verification, or commit logic

**DO (command responsibilities only):**
- ✅ MUST validate args (one of `{--from + --to}` or `--migration-id` is required)
- ✅ MUST validate project root (CLAUDE.md exists at CWD)
- ✅ MUST resolve `MIGRATION_ID` (generate kebab-case from `--from` + date if new; use given ID if resuming)
- ✅ MUST set context markers for the skill
- ✅ MUST invoke `Skill(command="spec-driven-migration")` immediately after validation

---

## Phase 0: Plan Mode Detection + Argument Validation

### Step 0.0: Plan Mode Auto-Exit [execution-mode: immediate]

This command's frontmatter declares `execution-mode: immediate` — it should NOT be
in plan mode when invoked. If plan mode is active, the harness exits it on first
tool call. Proceed to Step 0.1.

### Step 0.1: Project-Root Validation

Verify CWD is a DevForgeAI-aware project:
```
Glob(pattern="CLAUDE.md")  # MUST return exactly 1 result
```
IF no `CLAUDE.md` at CWD: HALT with "Not a DevForgeAI project root. cd into the project root and re-invoke."

### Step 0.2: Argument Parsing

Parse `$ARGUMENTS` (the command-line tail). Three modes:

**Mode A — New migration (`--from` + `--to` required):**
- `--from=<pattern>` — literal string the migration replaces. Required.
- `--to=<pattern>` — replacement string. Required.
- `--scope=<comma-separated-dirs>` — corpus to walk. Optional; default = `.claude/,src/claude/` (the dual-path framework tree).
- `--exclude=<comma-separated-patterns>` — paths to skip. Optional; default = `_archive/,/plans/,/agent-memory/`.
- `--dry-run` — emit classification + transform-rules without edits. Optional.

**Mode B — Resume (`--migration-id` required):**
- `--migration-id=<id>` — kebab-case session ID matching an existing `tmp/<id>/` directory.

**Mode C — Show recent (no args):**
- Display the most recent 5 migration IDs (resolve via `Glob(pattern="tmp/*/intent.json")`) and HALT with a prompt asking the user to pick one (resume) or specify `--from`+`--to` (new).

### Step 0.3: Argument Validation

| Condition | Action |
|---|---|
| Neither `--from`/`--to` nor `--migration-id` given | Mode C (show recent + prompt) |
| `--from` given without `--to` (or vice versa) | HALT — "both --from and --to are required for a new migration" |
| `--migration-id` given but `tmp/<id>/intent.json` does not exist | HALT — "No migration session found for <id>" |
| `--scope` contains a path that does not exist on disk | AskUserQuestion — "Scope dir <path> does not exist. Proceed anyway / cancel?" |

### Step 0.4: Resolve MIGRATION_ID

**New migration:**
```
MIGRATION_ID = kebab-case(slugify(<--from>)) + "-" + <YYYY-MM-DD>
# Example: --from='source-tree.md' on 2026-05-20 → MIGRATION_ID="source-tree-md-2026-05-20"
```
Trim to ≤60 chars. Validate it as a filename (`[a-z0-9-]+`).

**Resume:** use the given `--migration-id` verbatim.

### Step 0.5: Set Context Markers

```
$MIGRATION_ID = <resolved>
$FROM_PATTERN = <--from> | (read from tmp/<id>/intent.json on resume)
$TO_PATTERN   = <--to>   | (read from tmp/<id>/intent.json on resume)
$SCOPE        = <--scope> | default
$EXCLUSIONS   = <--exclude> | default
$DRY_RUN      = true | false
```

These markers are read by `spec-driven-migration` Phase 00 (Context Loading +
Resume Detection) per `references/parameter-extraction.md`.

---

## Phase 1: Invoke the Skill

Invoke `spec-driven-migration` immediately — do NOT prompt for further confirmation
at this layer. The skill itself handles all interactive checkpoints (Phase 01
intent confirmation, Phase 02 classification approval, Phase 03 cluster plan
confirmation).

```
Skill(command="spec-driven-migration")
```

The skill consumes the context markers above, runs its 7-phase workflow, and
returns control to this command after Phase 06 (Commit & Memory) completes — or
HALTs at any user-decision gate.

---

## Phase 2: Result Display

When the skill returns, surface the migration outcome to the user. Read the
verification report and the commit hash:

```
Read(file_path="tmp/${MIGRATION_ID}/verification-report.md")
```

Display:
- The migration summary block (files edited, dual-path verdict, FLAGGED resolved + deferred).
- The commit hash (from `tmp/${MIGRATION_ID}/session.md`).
- Pointers to the durable artifacts under `tmp/${MIGRATION_ID}/`.

IF the skill HALTed (verification failed, user aborted, or workflow incomplete):
- Display the last successful phase + the HALT reason.
- Point the user at `tmp/.migration-checkpoint-MIG-${MIGRATION_ID}.yaml` for resume.

---

## Cross-references

- **Skill:** `.claude/skills/spec-driven-migration/SKILL.md`
- **Subagents:** `.claude/agents/migration-classifier.md`, `.claude/agents/migration-cluster-worker.md`
- **ADR:** `devforgeai/specs/adrs/ADR-073-spec-driven-migration-skill.md`
- **Playbook origin:** PR #68 (source-tree decomposition); memory `feedback_dual_path_mechanical_migration`.
- **Sibling command pattern:** `.claude/commands/fix-story.md` (lean orchestration shape).
