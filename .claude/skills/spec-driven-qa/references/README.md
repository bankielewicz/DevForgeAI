# spec-driven-qa References

This skill is self-contained. All reference files, assets, and scripts are local to this skill directory.

## Strategy

Reference files are stored locally under `references/`, `assets/`, and `scripts/`. Phase files load references via `Read()` using relative paths from `.claude/skills/spec-driven-qa/`.

**Base path:** `.claude/skills/spec-driven-qa/references/`

## Reference Files

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
| automation-scripts.md | All | Python script documentation |

## Assets

| File | Used By Phase | Purpose |
|------|---------------|---------|
| assets/config/coverage-thresholds.md | Phase 02 | Coverage threshold config |
| assets/config/quality-metrics.md | Phase 04 | Quality metric thresholds |
| assets/config/security-policies.md | Phase 04 | Security scanning policies |
| assets/language-smoke-tests.yaml | Phase 02 | Runtime smoke test config |
| assets/templates/qa-report-template.md | Phase 05 | Report template |
| assets/templates/test-stub-template.cs | Phase 02 | Test stub generation |
| assets/traceability-report-template.md | Phase 02 | Traceability template |

## NOT Referenced (Intentional)

| File | Reason |
|------|--------|
| deep-validation-workflow.md | Consolidated loading enables token optimization bias -- the root cause of phase skipping. Each phase loads only what it needs. Archived with devforgeai-qa. |

## Migration History

- **2026-03-18:** Migrated from `devforgeai-qa` skill. All references, assets, and scripts are now local. `devforgeai-qa` archived to `backup/_devforgeai-qa.archive/`.
