# Business Analysis - Shared Reference Strategy

## Architecture

This skill maintains its own local reference files. Phase files load references via `Read()` paths from the `spec-driven-brainstorming` skill directory.

This follows the same pattern established by `spec-driven-dev`, which reads references from its own skill directory rather than cross-referencing other skills.

**Rationale:**
- Self-contained skill with no cross-skill dependencies
- References can evolve independently
- Clear ownership and maintenance boundaries

Governed by **ADR-065** (the 11-phase Business Analysis re-scope).

## Reference File Mapping

Every phase file loads `conversation-checkpoint-format.md` (its Contract REFERENCE) plus
the shared references below. Phases that cover an established domain workflow also load a
domain reference, and Stream C phases load `brainstorming-techniques.md`.

| Phase File | Domain Reference |
|------------|------------------|
| `phases/phase-01-ba-planning.md` | — |
| `phases/phase-02-stakeholder-analysis.md` | `stakeholder-discovery-workflow.md` |
| `phases/phase-03-problem-current-state.md` | `problem-exploration-workflow.md` |
| `phases/phase-04-future-state-opportunity.md` | `opportunity-mapping-workflow.md` |
| `phases/phase-05-business-case-feasibility.md` | — |
| `phases/phase-06-risk-analysis.md` | — |
| `phases/phase-07-constraints-solution-scope.md` | `constraint-discovery-workflow.md` |
| `phases/phase-08-requirements-definition.md` | — |
| `phases/phase-09-prioritization-roadmap.md` | `prioritization-workflow.md` |
| `phases/phase-10-change-transition-strategy.md` | — |
| `phases/phase-11-synthesis-handoff.md` | `brainstorm.schema.json` (data-island schema) |

## Shared References (Multiple Phases)

| Reference | Purpose |
|-----------|---------|
| `conversation-checkpoint-format.md` | Per-phase accumulating conversation checkpoint (`tmp/{BRAINSTORM_ID}/checkpoint.json`); resume logic; Phase 11 transcript appendix |
| `question-templates.md` | Canonical `AskUserQuestion` shape templates (`QT-1`..`QT-5`) |
| `user-interaction-patterns.md` | Interaction patterns and follow-up question guidance |
| `brainstorming-techniques.md` | Stream C methodology (Z13–Z18): divergent thinking, idea combination, HMW, cross-industry, pre-mortem, out-of-scope, stakeholder voice |
| `error-handling.md` | Error recovery and graceful degradation |
| `brainstorm.schema.json` | v2.0 JSON Schema validating the Phase 11 HTML data island |

## Template Assets

| Template | Purpose |
|----------|---------|
| `assets/templates/brainstorm-template.html` | Self-contained HTML Business Analysis document (Phase 11 output) |
| `assets/templates/readme-brainstorm-template.md` | Optional README artifact (Phase 11 Step 11.8) |
| `assets/templates/claude-md-template.md` | Optional CLAUDE.md artifact (Phase 11 Step 11.8) |
| `assets/templates/gitignore-template.md` | Optional .gitignore artifact (Phase 11 Step 11.8) |

## Anti-Skip Enforcement Note

Per-phase reference loading is a deliberate anti-skip mechanism. Each phase file contains a `## Reference Loading` section that loads the specific reference files for that phase. (This is advisory guidance for this workflow: brainstorming invokes no `devforgeai-validate phase-record`, so no `pre-phase-record-reference-check.sh` gate consumes the section — see gh#259.)

**Consolidated loading is explicitly forbidden.** Loading all references at once enables token optimization bias, which is the root cause of phase skipping. Each phase loads only what it needs, when it needs it.

(Source: `.claude/skills/spec-driven-qa/references/README.md` - "Consolidated loading enables token optimization bias")
