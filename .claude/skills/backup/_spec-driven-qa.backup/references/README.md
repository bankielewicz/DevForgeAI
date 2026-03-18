# spec-driven-qa Shared References

This skill shares reference files with the `devforgeai-qa` skill to avoid duplication and drift.

## Strategy

Reference files are NOT duplicated. Phase files in this skill use absolute paths via `Read()` to load references from the devforgeai-qa skill directory.

**Base path:** `.claude/skills/devforgeai-qa/references/`

## Shared Reference Files

| File | Used By Phase | Purpose |
|------|---------------|---------|
| shared-protocols.md | Phase 01 | Pre-flight, CLI gates, task tracking |
| phase-0-setup-workflow.md | Phase 01 | Setup step details |
| parameter-extraction.md | Phase 01 | Story ID/mode extraction |
| test-isolation-service.md | Phase 01 | Test isolation configuration |
| parallel-validation.md | Phase 01, 04 | Adaptive validator selection |
| traceability-validation-algorithm.md | Phase 02 | AC-DoD traceability |
| coverage-analysis.md | Phase 02 | 7-step coverage workflow |
| diff-regression-detection.md | Phase 03 | Git diff analysis |
| test-tampering-heuristics.md | Phase 03 | Test tampering patterns |
| anti-pattern-detection.md | Phase 04 | Anti-pattern scanning |
| spec-compliance-validation.md | Phase 04 | Spec compliance checks |
| code-quality-workflow.md | Phase 04 | Quality metrics |
| dod-protocol.md | Phase 04 | Deferral validation (conditional) |
| qa-result-formatting-guide.md | Phase 05 | Result formatting |
| phase-3-reporting-workflow.md | Phase 05 | Report generation |
| story-update-workflow.md | Phase 05 | Atomic story updates |
| phase-4-cleanup-workflow.md | Phase 06 | Cleanup procedures |
| feedback-hooks-workflow.md | Phase 06 | Feedback hook invocation |

## Shared Assets

| File | Used By Phase | Purpose |
|------|---------------|---------|
| assets/config/coverage-thresholds.md | Phase 02 | Coverage threshold config |
| assets/language-smoke-tests.yaml | Phase 02 | Runtime smoke test config |
| assets/templates/qa-report-template.md | Phase 05 | Report template |
| assets/traceability-report-template.md | Phase 02 | Traceability template |

## NOT Referenced (Intentional)

| File | Reason |
|------|--------|
| deep-validation-workflow.md | Consolidated loading enables token optimization bias -- the root cause of phase skipping. Each phase loads only what it needs. |

## Why Shared (Not Copied)

1. **No drift** - Single source of truth for reference content
2. **No maintenance burden** - Updates to devforgeai-qa references automatically apply
3. **Lean skill** - spec-driven-qa contains only its unique value: the EVG phase files
4. **Rollback safe** - If spec-driven-qa is removed, devforgeai-qa remains fully functional
