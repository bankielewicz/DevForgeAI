# spec-driven-dev Reference Files

Self-contained reference library for the spec-driven-dev TDD workflow skill. All reference files are local to this skill directory.

**Migration:** Absorbed from `implementing-stories` per ADR-039 (2026-03-18).

## Reference Inventory

### Core References (Phase Execution)

| File | Used By | Purpose |
|------|---------|---------|
| parameter-extraction.md | SKILL.md | Story ID extraction algorithm |
| memory-file-schema.md | SKILL.md, Phase 01 | Phase state JSON schema |
| memory-file-operations.md | SKILL.md | Memory file read/write operations |
| resume-detection.md | SKILL.md | Resume workflow detection |
| test-integrity-snapshot.md | Phase 02 | Red-phase test checksum snapshot (STORY-502) |
| observation-capture.md | Phases 02-08 | Observation JSON schema |
| qa-remediation-workflow.md | SKILL.md | Remediation mode workflow |
| technical-debt-register-workflow.md | Phase 06 | Debt register update workflow |
| deferral-budget-enforcement.md | Phase 08 | Deferral budget limits |
| lock-file-coordination.md | Phase 08 | Parallel story locking |
| ac-verification-workflow.md | Phases 4.5, 5.5 | AC verification procedure |
| ac-checklist-update-workflow.md | Phases 02-08 | AC checklist update procedure |
| dod-update-workflow.md | Phase 07 | DoD format specification |
| dod-validation-checkpoint.md | Phase 07 | DoD validation gate |
| git-workflow-conventions.md | Phase 08 | Git commit patterns |
| dev-result-formatting-guide.md | Phase 10 | Result display templates |
| progressive-task-disclosure.md | All phases | Task creation pattern |
| workflow-deviation-protocol.md | SKILL.md | When user consent needed |
| ambiguity-protocol.md | All phases | AskUserQuestion triggers |
| phase-transition-validation.md | All phases | CLI validation commands |
| pre-phase-planning.md | SKILL.md | Optional pre-phase planning |

### TDD Phase Guidance

| File | Used By | Purpose |
|------|---------|---------|
| tdd-red-phase.md | Phase 02 | Detailed Red phase guidance |
| tdd-green-phase.md | Phase 03 | Detailed Green phase guidance |
| tdd-refactor-phase.md | Phase 04 | Detailed Refactor phase guidance |
| tdd-patterns.md | Phases 02-04 | Comprehensive TDD patterns reference |
| refactoring-patterns.md | Phase 04 | Code improvement techniques |
| integration-testing.md | Phase 05 | Integration test guidance |
| phase-06-deferral-challenge.md | Phase 06 | Detailed deferral guidance |

### Technical Debt

| File | Purpose |
|------|---------|
| technical-debt-atomic-write.md | Atomic debt register writes |
| technical-debt-id-generation.md | DEBT-NNN ID generation |
| technical-debt-register-workflow.md | Full debt register workflow |
| technical-debt-type-derivation.md | Debt type classification |

### Treelint Integration

| File | Purpose |
|------|---------|
| treelint-integration.md | AST-aware search setup |
| treelint-daemon-lifecycle.md | Daemon management |
| treelint-dependency-query.md | Call-graph queries |
| treelint-repository-map.md | Repository structure mapping |

### Session & State

| File | Purpose |
|------|---------|
| session-checkpoint.md | Cross-session checkpoint persistence |
| parallel-context-loader.md | Parallel subagent invocation |
| background-executor.md | Background task execution |
| headless-answer-resolver.md | Context-less answer resolution |
| task-result-aggregation.md | Multi-subagent result aggregation |

### Supporting References

| File | Purpose |
|------|---------|
| context-validation.md | Context file validation procedures |
| observation-write-protocol.md | Observation file writing protocol |
| qa-deferral-recovery.md | QA deferral recovery workflow |
| remediation-story-creator.md | Remediation story generation |
| story-documentation-pattern.md | Story documentation format |
| slash-command-argument-validation-pattern.md | Command argument validation |

### Preflight References (references/preflight/)

| File | Purpose |
|------|---------|
| _index.md | Preflight reference index |
| 01.0-project-root.md | Project root verification |
| 01.0.5-cli-check.md | CLI installation validation |
| 01.1-git-status.md | Git repository checks |
| 01.1.5-user-consent.md | User consent for git operations |
| 01.1.6-stash-warning.md | Stash detection warnings |
| 01.1.7-story-isolation.md | Story file isolation check |
| 01.2-worktree.md | Git worktree management |
| 01.2.5-dependency-graph.md | Story dependency analysis |
| 01.2.6-file-overlap.md | File overlap detection |
| 01.3-workflow-adapt.md | Git vs file-based workflow |
| 01.4-file-tracking.md | File-based tracking setup |
| 01.5-context-files.md | Context file validation |
| 01.6-load-story.md | Story file loading |
| 01.7-validate-spec.md | Spec vs context conflict detection |
| 01.8-tech-stack.md | Technology stack detection |
| 01.9-qa-failures.md | Previous QA failure detection |
| 01.10-complexity.md | Story complexity assessment |
| completion-checkpoint.md | Phase 01 completion verification |

### Assets (assets/templates/)

| File | Purpose |
|------|---------|
| implementation-notes-template.md | Story Implementation Notes format |
| parallel.yaml.example | Multi-story parallel execution example |
