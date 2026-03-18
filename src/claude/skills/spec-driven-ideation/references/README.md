# spec-driven-ideation References

## Self-Contained Architecture

This skill is **self-contained** — all reference files, templates, assets, and scripts are co-located within this skill directory. No external skill dependencies exist.

## Reference Locations

| Type | Path |
|------|------|
| Phase workflows | `.claude/skills/spec-driven-ideation/references/` |
| Error handling | `.claude/skills/spec-driven-ideation/references/error-*.md` |
| Templates | `.claude/skills/spec-driven-ideation/assets/templates/` |
| Scripts | `.claude/skills/spec-driven-ideation/scripts/` |
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

## Migration History

This skill was originally created using a shared-reference pattern where phase files loaded references from `discovering-requirements/references/`. As of 2026-03-18, all reference files, assets, and scripts were migrated into this skill directory to make it fully self-sufficient. The `discovering-requirements` skill has been archived.
