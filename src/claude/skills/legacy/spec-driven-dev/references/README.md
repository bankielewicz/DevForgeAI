# spec-driven-dev Reference Files

Self-contained reference library for the spec-driven-dev TDD workflow skill.

**Migration history:**
- ADR-039 (2026-03-18) — absorbed from `spec-driven-dev`.
- ADR-076 (May 2026) — ceremony-to-hook policy. References without any live consumer were moved to `_archive/` via `git mv` for history preservation.

## Live References (36 root + 3 preflight)

The active reference set carries documentation that at least one live consumer reads or cites. Each `Read(file_path="references/...")` invocation in SKILL.md, phase files, agent definitions, or sibling skills resolves here.

**Tier 1 — direct `Read()` at execution time:**

| File | Loaded by |
|------|-----------|
| `ac-verification-workflow.md` | Phase 4.5 + Phase 5.5 Step 1 |
| `technical-debt-register-workflow.md` | Phase 06 Step 6 |

**Tier 2 — transitive loads, prose-pointer citations from SKILL/phases/agents:**

The remaining live references are loaded by another reference, cited in prose from `SKILL.md` / phase files / agent definitions, or cross-referenced from sibling skills. `ls references/*.md` enumerates the current live set; consult the relevant prose pointer when context demands a specific reference. Notable cross-skill citers:

- `spec-driven-stories/references/story-type-classification.md` cites `integration-testing.md`
- Several agent definitions cite `tdd-patterns.md`, `treelint-dependency-query.md`, `context-validation.md`
- `dod-update-workflow.md` chains to `git-workflow-conventions.md`
- `ac-checklist-update-workflow.md` chains to phase-specific TDD references

**Preflight subdir (`references/preflight/`):**

| File | Cited by |
|------|----------|
| `_index.md` | agent-side prose pointer |
| `01.0-entry-dispatcher.md` | SKILL.md (Phase State Initialization & Entry Dispatcher) |
| `01.9-qa-failures.md` | SKILL.md (Remediation Mode entry path) |

The remaining Phase-01 step decompositions were superseded by the `dev-preflight` CLI and live in `_archive/preflight/`.

## Archive (`_archive/`)

33 files preserved via `git mv` for history. These were absorbed during the spec-driven-dev → spec-driven-dev consolidation (ADR-039) but no live consumer reads or prose-cites them. Composition:

- `_archive/` (root): 14 files — supplementary phase guidance, deferred capabilities (`headless-answer-resolver.md`, `observation-write-protocol.md`, `slash-command-argument-validation-pattern.md`, `progressive-task-disclosure.md`, story-documentation patterns, treelint daemon/repository lifecycle docs, dev-result-formatting-guide, memory-file legacy variants, etc.)
- `_archive/preflight/`: 19 files — obsolete Phase-01 step decompositions (01.0-project-root through 01.10-complexity) superseded by `dev-preflight` CLI

**Never `Read()` proactively from `_archive/`.** Consult only when historical context is genuinely required.
