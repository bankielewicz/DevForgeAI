# Migration Notes: devforgeai-github-actions -> spec-driven-ci

**Migration Date:** 2026-03-19
**Migration Type:** Skill upgrade with anti-skip enforcement
**Old Skill:** `devforgeai-github-actions` (140-line SKILL.md, no anti-skip enforcement)
**New Skill:** `spec-driven-ci` (284-line SKILL.md, 4-layer anti-skip enforcement)

---

## Reason for Migration

The `devforgeai-github-actions` skill was the last remaining `devforgeai-*` SDLC skill without structural anti-skip enforcement. Claude would skip phases/steps due to token optimization bias, causing:
- Incomplete workflow generation
- Missing cost optimization settings
- Skipped validation checks
- Double work for users who had to catch and redo skipped steps

All 16 other SDLC skills had been successfully migrated to the `spec-driven-*` pattern. This migration completes the unified pattern.

---

## What Changed

### Structural Improvements

| Aspect | Old (devforgeai-github-actions) | New (spec-driven-ci) |
|--------|--------------------------------|----------------------|
| Anti-skip enforcement | None | 4-layer (subagents, CLI gates, hooks, registry) |
| Phase execution pattern | Flat description | Execute-Verify-Gate per step |
| Reference loading | 2 monolithic files | 9 per-phase granular files |
| Phase files | None (all in SKILL.md) | 5 separate phase files |
| Template files | Inline in references | 6 separate template files |
| Total files | 3 | 22 |
| EVR steps | 0 | 28 |
| Self-check violations | None | 8-item checklist |
| Phase state tracking | None | CLI-enforced state file |

### Reference File Decomposition

```
OLD: workflow-generation.md (267 lines)
  -> git-repo-validation.md          (Phase 01)
  -> context-file-validation.md      (Phase 01)
  -> config-file-schema.md           (Phase 02)
  -> workflow-templates.md           (Phase 03)

OLD: cost-optimization-guide.md (247 lines)
  -> cost-optimization-strategies.md (Phase 04)

OLD: SKILL.md Security Prerequisites
  -> security-prerequisites.md       (Phase 01, 05)

NEW (never existed before):
  -> parameter-extraction.md         (Phase 01)
  -> ci-answers-protocol.md          (Phase 02)
  -> yaml-validation-procedures.md   (Phase 05)
```

### Command Changes

| Aspect | Before | After |
|--------|--------|-------|
| Command name | `/setup-github-actions` | `/setup-github-actions` (unchanged) |
| Skill invocation | `Skill(command="devforgeai-github-actions")` | `Skill(command="spec-driven-ci")` |
| Command backup | N/A | `src/claude/commands/backup/setup-github-actions.md` |

### Naming Convention

The skill name follows the established `spec-driven-*` pattern:
- Short, abstract domain noun ("ci" = continuous integration)
- Platform-agnostic (not locked to GitHub Actions)
- Matches existing pattern: spec-driven-dev, spec-driven-qa, spec-driven-rca, spec-driven-ui

---

## Files Created

```
src/claude/skills/spec-driven-ci/
  SKILL.md                              (284 lines)
  MIGRATION-NOTES.md                    (this file)
  phases/
    phase-01-preflight.md
    phase-02-config-loading.md
    phase-03-workflow-generation.md
    phase-04-cost-optimization.md
    phase-05-validation-summary.md
  references/
    parameter-extraction.md
    git-repo-validation.md
    context-file-validation.md
    config-file-schema.md
    workflow-templates.md
    cost-optimization-strategies.md
    ci-answers-protocol.md
    yaml-validation-procedures.md
    security-prerequisites.md
  assets/
    templates/
      dev-story-workflow.yml
      qa-validation-workflow.yml
      parallel-stories-workflow.yml
      installer-testing-workflow.yml
      github-actions-config.yaml
      ci-answers-config.yaml
```

## Files Archived

```
src/claude/skills/devforgeai-github-actions/
  -> src/claude/skills/backup/_devforgeai-github-actions.archive/
```

---

## Migration Pattern

This is the 17th skill migration following the established pattern:

1. Create new `spec-driven-{name}/` with anti-skip enforcement
2. Decompose monolithic references into per-phase granular files
3. Extract inline templates into `assets/templates/`
4. Update command to invoke new skill name
5. Backup old command
6. Archive old skill with HALT directive
7. Update skill-inventory.md

Prior migrations: brainstorming, ideation, architecture, dev, QA, feedback, release, stories, documentation, QA remediation, remediation, coverage, W3 compliance, RCA, UI generation, research.
