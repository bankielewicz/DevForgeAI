# spec-driven-ideation References

## Shared-Reference Strategy

This skill uses the **shared-reference pattern** (same approach as `discovering-problems` reading from `brainstorming/`). Phase files in `spec-driven-ideation` load references from `discovering-requirements/references/` via `Read()`.

This prevents content duplication and ensures a single source of truth.

## Reference Locations

| Type | Path |
|------|------|
| Phase workflows | `.claude/skills/discovering-requirements/references/` |
| Error handling | `.claude/skills/discovering-requirements/references/error-*.md` |
| Templates | `.claude/skills/discovering-requirements/assets/templates/` |
| Scripts | `.claude/skills/discovering-requirements/scripts/` |
| Phase files | `.claude/skills/spec-driven-ideation/phases/` |

## Phase-to-Reference Map

| Phase | References Loaded Fresh |
|-------|------------------------|
| 01 (Pre-Flight) | `brainstorm-handoff-workflow.md`, `brainstorm-data-mapping.md`, `user-input-guidance.md` |
| 02 (Discovery) | `discovery-workflow.md`, `user-interaction-patterns.md` |
| 03 (Elicitation) | `requirements-elicitation-workflow.md`, `requirements-elicitation-guide.md`, `domain-specific-patterns.md`, `user-interaction-patterns.md` |
| 04 (Compliance) | Context files read directly from `devforgeai/specs/context/` |
| 05 (Artifacts) | `artifact-generation.md`, `examples.md` |
| 06 (Validation) | `self-validation-workflow.md`, `validation-checklists.md` |
| 07 (Handoff) | `completion-handoff.md`, `output-templates.md` |

## Why Shared References

1. **Single source of truth** - No content drift between copies
2. **Maintenance** - Updates to reference files automatically apply to both skills
3. **Token efficiency** - No duplicated file storage
4. **Proven pattern** - Same approach used by discovering-problems + brainstorming
