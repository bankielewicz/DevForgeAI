# spec-driven-dev Shared References

This skill shares reference files with the `implementing-stories` skill to avoid duplication and drift.

## Strategy

Reference files are NOT duplicated. Phase files in this skill use absolute paths via `Read()` to load references from the implementing-stories skill directory.

**Base path:** `.claude/skills/implementing-stories/references/`

## Shared Reference Files

| File | Used By | Purpose |
|------|---------|---------|
| parameter-extraction.md | SKILL.md | Story ID extraction algorithm |
| memory-file-schema.md | SKILL.md, Phase 01 | Phase state JSON schema |
| memory-file-operations.md | SKILL.md | Memory file read/write operations |
| resume-detection.md | SKILL.md | Resume workflow detection |
| test-integrity-snapshot.md | Phase 02 | Red-phase test checksum snapshot |
| observation-capture.md | Phases 02-08 | Observation JSON schema |
| qa-remediation-workflow.md | SKILL.md | Remediation mode workflow |
| technical-debt-register-workflow.md | Phase 06 | Debt register update workflow |
| deferral-budget-enforcement.md | Phase 08 | Deferral budget limits |
| lock-file-coordination.md | Phase 08 | Parallel story locking |
| ac-verification-workflow.md | Phases 4.5, 5.5 | AC verification procedure |
| dod-update-workflow.md | Phase 07 | DoD format specification |
| git-workflow-conventions.md | Phase 08 | Git commit patterns |
| dev-result-formatting-guide.md | Phase 10 | Result display templates |
| progressive-task-disclosure.md | All phases | Task creation pattern |
| workflow-deviation-protocol.md | SKILL.md | When user consent needed |
| ambiguity-protocol.md | All phases | AskUserQuestion triggers |
| phase-transition-validation.md | All phases | CLI validation commands |
| pre-phase-planning.md | SKILL.md | Optional pre-phase planning |
| tdd-red-phase.md | Phase 02 | Detailed Red phase guidance |
| tdd-green-phase.md | Phase 03 | Detailed Green phase guidance |
| tdd-refactor-phase.md | Phase 04 | Detailed Refactor phase guidance |
| phase-06-deferral-challenge.md | Phase 06 | Detailed deferral guidance |

## Why Shared (Not Copied)

1. **No drift** - Single source of truth for reference content
2. **No maintenance burden** - Updates to implementing-stories references automatically apply
3. **Lean skill** - spec-driven-dev contains only its unique value: the Execute-Verify-Gate phase files
4. **Rollback safe** - If spec-driven-dev is removed, implementing-stories remains fully functional
