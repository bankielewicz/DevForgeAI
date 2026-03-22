---
id: EPIC-070
title: "Discovering-Requirements Anthropic Conformance Remediation (v3)"
status: Planning
start_date: 2026-02-19
target_date: 2026-03-19
total_points: 16
completed_points: 0
created: 2026-02-19
owner: DevForgeAI Framework Team
tech_lead: DevForgeAI AI Agent
team: DevForgeAI
source_analysis: devforgeai/specs/analysis/discovering-requirements-conformance-analysis.md
supersedes: EPIC-069
complexity_score: 4
---

# Epic: Discovering-Requirements Anthropic Conformance Remediation (v3)

## Business Goal

Bring the `/ideate` command and `discovering-requirements` skill into full Anthropic Agent Skills specification conformance by remediating the remaining 16 actionable findings from the 2026-02-19 conformance analysis. This supersedes EPIC-069, which targeted 28 findings — of which 21 have been resolved by STORY-444 through STORY-450.

**Problem:** The conformance analysis scores 3 of 9 categories as "Partially Conformant" (Progressive Disclosure, Chain of Thought, YAML Frontmatter). The `/ideate` command has 15 code blocks before `Skill()` invocation (lean target: ≤4). Six reference file chains violate Anthropic's one-level-deep rule, risking incomplete reads. These are the remaining tail-end findings after the bulk of remediation work in EPIC-069.

**Value:** Full conformance improves Claude's requirements analysis accuracy, reduces context token waste, ensures reliable inter-phase data flow, and aligns with platform vendor best practices. The discovering-requirements skill is the first skill new users encounter — conformance quality here sets expectations for the entire framework.

**Source:** `devforgeai/specs/analysis/discovering-requirements-conformance-analysis.md` (9 categories, 24 findings total, 16 actionable)

## Success Metrics

- **Metric 1:** All 16 actionable findings resolved and verified (from 16 to 0)
- **Metric 2:** Re-audit shows 0 Partially Conformant categories (currently 3), achieving 9/9 Conformant
- **Metric 3:** SKILL.md remains under 500 lines after all additions (currently 407)
- **Metric 4:** No regression — all existing ideation workflows continue to function correctly

**Measurement Plan:**
- Tracked via story completion in `devforgeai/specs/Stories/`
- Re-run conformance audit after Sprint 2 to validate structural changes
- Final re-audit after Sprint 3 showing 9/9 PASS categories
- Review frequency: per-sprint

## Scope

### In Scope

6 features implementing 16 findings across 3 sprints, grouped by theme for efficient implementation.

**Primary files modified:**
- `.claude/skills/discovering-requirements/SKILL.md` (407 lines)
- `.claude/commands/ideate.md` (400 lines)
- `.claude/skills/discovering-requirements/references/` (25 files, ~9,947 lines)

### Out of Scope

- ❌ Skill functional changes (no new phases or capabilities)
- ❌ Other skill conformance (separate epics for /dev, /qa, etc.)
- ❌ Anthropic spec changes (we conform to current spec, not propose changes)
- ❌ Finding 1.4 (Skill() tool not in spec — platform limitation, no action needed)
- ❌ Story-level detail (ACs, NFRs, data models — handled by `/create-story`)

## Features

### Feature 1: YAML Frontmatter, Metadata & Naming Housekeeping — 2 pts

**Description:** Apply all single-touch YAML, metadata, and naming corrections to SKILL.md and ideate.md. These are low-risk one-liners that together bring both files into full frontmatter and naming conformance.

**Findings:** 1.1 (remove quotes from allowed-tools), 1.2 (remove unused WebFetch), 1.3 (standardize model field), 2.1 (natural trigger phrases), 2.2 (command description context), 4.2 (condense Core Philosophy), 5.1 (standardize XML tag naming to hyphenated), 5.2 (remove orphaned phase-4-output tag)

**Files:** `.claude/skills/discovering-requirements/SKILL.md`, `.claude/commands/ideate.md`
**Estimated Effort:** 45 minutes
**Priority:** High (zero-risk, immediate compliance gain)

### Feature 2: Portability Fix — Remove Hardcoded WSL Path — 1 pt

**Description:** Replace machine-specific `/mnt/c/Projects/DevForgeAI2/...` absolute path in `user-input-guidance.md` line 590 with the correct relative path. Investigate whether the self-reference (file loading itself) is intentional or a copy-paste error.

**Findings:** 4.1 (hardcoded absolute path)

**Files:** `.claude/skills/discovering-requirements/references/user-input-guidance.md`
**Estimated Effort:** 10 minutes
**Priority:** High (breaks non-WSL environments)

### Feature 3: Flatten Nested Reference Chains — 3 pts

**Description:** Eliminate all 2-level-deep reference chains by adding direct load instructions in SKILL.md for chained files (Option A — no file merges to avoid invalidating existing story targets).

**Findings:** 3.1 (6 nested reference chains violate one-level-deep rule)

**Chains to flatten:**

| Source (loaded from SKILL.md) | Chains To | Notes |
|-------------------------------|-----------|-------|
| `self-validation-workflow.md` | → `validation-checklists.md` | Both active |
| `requirements-elicitation-workflow.md` | → `requirements-elicitation-guide.md` | Most-used workflow path |
| `user-input-integration-guide.md` | → `user-input-guidance.md` | May be merge candidate (thin guide) |
| `error-type-1-incomplete-answers.md` | → `requirements-elicitation-guide.md` | Shared target |
| `error-type-3-complexity-errors.md` | → `complexity-assessment-matrix.md` | **Target file is in designing-systems skill, not discovering-requirements — cross-skill reference** |
| `error-type-4-validation-failures.md` | → `validation-checklists.md` | Shared target |

**Implementation strategy (per architect-reviewer recommendation):**
- Use Option A: Add direct `Read()` instructions in SKILL.md phase sections
- Remove redundant chained `Read()` from source reference files after adding SKILL.md direct loads
- For `error-type-3` chain: Verify cross-skill reference to `designing-systems/references/complexity-assessment-matrix.md` is intentional; if not, remove dead reference
- Optional: Merge `user-input-integration-guide.md` into `user-input-guidance.md` (Option C partial merge — thin guide file has no active story targets)

**Files:** `.claude/skills/discovering-requirements/SKILL.md` (6 additions), up to 6 reference files (remove redundant chained reads)
**Estimated Effort:** 2 hours
**Priority:** High (Anthropic best-practices violation — Claude may silently fail to read chained files completely)

### Feature 4: Structured Phase Output Tags & Command Consolidation — 3 pts

**Description:** Upgrade `<phase-N-output>` tags from comma-separated field name placeholders to proper nested XML with template variables. Consolidate command code blocks from 15 to ~7-10 before `Skill()` by merging blocks that share the same logical guard condition.

**Findings:** 7.1 (phase output tags lack structured handoffs), 9.1 (15 code blocks exceeds lean target)

**Implementation strategy (per architect-reviewer recommendation):**
- **Sub-task A (Phase output tags):** Verify whether any downstream step actually consumes these tags before adding production instructions. If tags are documentation-only, label them explicitly as such.
- **Sub-task B (Code block consolidation):** Merge only blocks with no AskUserQuestion branch points between them. Phase 2.0 blocks (4→1) are safe to merge. Phase 0 brainstorm blocks (5) should NOT be fully merged due to branching logic.

**Files:** `.claude/skills/discovering-requirements/SKILL.md`, `.claude/commands/ideate.md`
**Estimated Effort:** 2 hours
**Priority:** Medium (structural improvement to handoff quality and command leanness)

### Feature 5: Table of Contents for Large Reference Files — 5 pts

**Description:** Add `## Table of Contents` section to every reference file exceeding 100 lines that currently lacks one. Batch operation across 21 files, prioritizing largest files first.

**Findings:** 3.2 (21 of 26 files >100 lines missing TOC)

**Pre-flight verification:** Read each file before editing to confirm TOC absence. STORY-449/450 may have already added TOCs to some files — exclude any that already have them.

**Batch strategy:** Process 8 largest files first (validation-checklists.md 604 lines, user-interaction-patterns.md 462 lines, brainstorm-handoff-workflow.md 402 lines, resume-logic.md 382 lines, requirements-elicitation-workflow.md 368 lines, output-templates.md 352 lines, discovery-workflow.md 331 lines, examples.md 305 lines), verify anchor links, then process remaining 13 files.

**Files:** 21 reference files in `.claude/skills/discovering-requirements/references/`
**Estimated Effort:** 2-3 hours
**Priority:** Medium (Anthropic best-practices requirement for files >100 lines)

### Feature 6: Content Quality — CoT Guidance & Progressive Examples — 2 pts

**Description:** Add Chain-of-Thought guidance for requirements prioritization in the elicitation workflow, and restructure the examples file reference to load per-phase rather than all-upfront.

**Findings:** 7.3 (no CoT guidance for prioritization), 8.2 (examples loaded all-upfront instead of per-phase)

**Files:** `.claude/skills/discovering-requirements/references/requirements-elicitation-workflow.md`, `.claude/skills/discovering-requirements/SKILL.md` (update examples load instruction)
**Estimated Effort:** 30 minutes
**Priority:** Low (quality improvement after structural work is stable)

## Target Sprints

**Estimated Duration:** 3 sprints / 3-4 weeks

### Sprint 1: High-Impact Fixes (Features 1, 2, 3) — 6 pts

**Goal:** Resolve all High-priority findings including the one-level-deep rule violation.

**Stories:**
- STORY-451: YAML Frontmatter, Metadata & Naming Housekeeping (2 pts)
- STORY-452: Portability Fix — Remove Hardcoded WSL Path (1 pt)
- STORY-453: Flatten Nested Reference Chains (3 pts)

**Execution order:** STORY-451 and STORY-452 can run in parallel. STORY-453 should follow STORY-452 (clarifies user-input chain intent).

**Key Deliverables:**
- Compliant YAML frontmatter and consistent XML tag naming
- No machine-specific paths
- All reference chains flattened to one-level-deep

### Sprint 2: Structural Improvements (Features 4, 5) — 8 pts

**Goal:** Phase output tag structure and TOC coverage.

**Stories:**
- STORY-454: Structured Phase Output Tags & Command Consolidation (3 pts)
- STORY-455: Table of Contents for Large Reference Files (5 pts)

**Execution order:** STORY-453 must be complete before starting (flattening may change which files exist). STORY-454 and STORY-455 can run in parallel.

**Key Deliverables:**
- Structured XML phase handoffs (or documented as documentation-only)
- Command code blocks reduced from 15 toward target
- TOC in all 21+ reference files >100 lines
- Mid-epic conformance re-audit checkpoint

### Sprint 3: Polish & Final Verification (Feature 6) — 2 pts

**Goal:** Content quality additions and final re-audit.

**Stories:**
- STORY-456: Content Quality — CoT Guidance & Progressive Examples (2 pts)

**Key Deliverables:**
- `<thinking>` tag guidance for requirements prioritization
- Per-phase example loading
- Final conformance re-audit showing 9/9 Conformant categories

## User Stories

1. **As a** framework maintainer, **I want** all YAML frontmatter and XML tags to follow Anthropic conventions, **so that** the skill passes spec validators and Claude parses tags consistently
2. **As a** framework user on non-WSL systems, **I want** no hardcoded machine-specific paths, **so that** the skill works on any environment
3. **As a** framework maintainer, **I want** all reference chains to be one-level deep, **so that** Claude reads complete files instead of partial previews
4. **As a** framework maintainer, **I want** structured phase output tags and a leaner command, **so that** inter-phase handoffs are reliable and the command follows lean orchestration
5. **As a** framework maintainer, **I want** table of contents in all large reference files, **so that** Claude can navigate them efficiently during partial reads
6. **As a** framework maintainer, **I want** CoT guidance for prioritization and per-phase example loading, **so that** Claude produces better-reasoned requirements with targeted context

## Technical Considerations

### Architecture Impact
- No new services or components — all changes are prompt engineering edits to existing Markdown/YAML files
- Feature 3 (flatten chains) adds 6 `Read()` instructions to SKILL.md — net token budget neutral (removes redundant chained reads)
- Feature 5 (TOC batch) adds ~1-3 lines per file — negligible overhead (~60 lines total)
- SKILL.md must remain under 500 lines (currently 407, ~93 lines of budget)

### Technology Decisions
- No new technologies — all work is Markdown/YAML editing
- XML tags follow Anthropic's documented patterns (not custom invention)
- Option A (direct loads) preferred over Option B (file merges) per architect-reviewer

### Security & Compliance
- No security implications — prompt engineering changes only
- Finding 4.1 (hardcoded path) is a portability bug, not a security vulnerability

## Dependencies

### Internal Dependencies
- [x] **EPIC-069:** Superseded (21/28 findings resolved by STORY-444 through STORY-450)
- [x] **Conformance Analysis:** Complete (`devforgeai/specs/analysis/discovering-requirements-conformance-analysis.md`)

### External Dependencies
- None

### Blocking Issues
- **STORY-453 (flatten chains)** must complete before STORY-454/455/456 — flattening may change which files exist or are merged
- **Verify `complexity-assessment-matrix.md` cross-skill reference** — `error-type-3-complexity-errors.md` references a file in `designing-systems` skill, not `discovering-requirements`. Must confirm intentionality before Feature 3.

## Stakeholders

- **Product Owner:** DevForgeAI Framework Team
- **Tech Lead:** DevForgeAI AI Agent

## Risks & Mitigation

### Risk 1: Flattening Chains Causes Double-Loading
- **Probability:** Medium
- **Impact:** Low (token waste, not failure)
- **Mitigation:** Remove redundant chained `Read()` from source reference files after adding SKILL.md direct loads
- **Contingency:** If double-loading detected in testing, remove the source-file `Read()` and keep only the SKILL.md load

### Risk 2: Code Block Consolidation Reduces Parse Fidelity
- **Probability:** Medium
- **Impact:** Medium (Claude may skip branches in merged blocks)
- **Mitigation:** Do not merge across AskUserQuestion branch points. Only merge blocks with same logical guard.
- **Contingency:** Revert consolidation for any block where testing shows branch skipping

### Risk 3: SKILL.md Exceeds 500 Lines After Additions
- **Probability:** Low (93 lines of budget)
- **Impact:** Medium (performance degradation)
- **Mitigation:** Feature 3 adds ~6 lines of `Read()` instructions, Feature 4 adds ~15 lines of structured output tags, Feature 1 removes ~8 lines. Net: ~+13 lines → 420 lines (well under 500)
- **Contingency:** Move excess to reference files

### Risk 4: TOC Anchor Links Break on Special Characters in Headings
- **Probability:** Low
- **Impact:** Low (misleading navigation, not functional failure)
- **Mitigation:** Process 8 largest files first as verification batch before remaining 13
- **Contingency:** Fix malformed anchors in follow-up commit

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1:    Sprint 1 - Housekeeping, WSL fix, flatten chains (6 pts)
Week 2-3:  Sprint 2 - Phase tags, command consolidation, TOC batch (8 pts)
Week 3-4:  Sprint 3 - CoT guidance, examples, final re-audit (2 pts)
════════════════════════════════════════════════════
Total Duration: 3-4 weeks
Total Points: 16
Target Release: 2026-03-19
```

### Key Milestones
- [ ] **Milestone 1:** End Sprint 1 — All High-priority findings resolved, chains flattened
- [ ] **Milestone 2:** End Sprint 2 — Structural improvements complete, mid-epic re-audit
- [ ] **Milestone 3:** End Sprint 3 — Final re-audit ≥9/9 Conformant categories

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Stories Created | 6 | 3 (STORY-451, 452, 453) | 0 | 0 | 0 |
| Sprint 2 | Stories Created | 8 | 2 (STORY-454, 455) | 0 | 0 | 0 |
| Sprint 3 | Stories Created | 2 | 1 (STORY-456) | 0 | 0 | 0 |
| **Total** | **0%** | **16** | **6** | **0** | **0** | **0** |

### Burndown
- **Total Points:** 16
- **Completed:** 0
- **Remaining:** 16

## Dependency Graph

```
STORY-451 (housekeeping, 2pt) ─────┐
                                    ├─ independent, Sprint 1
STORY-452 (WSL path fix, 1pt) ────┘
    │
    ▼ (soft: clarifies user-input chain intent)
STORY-453 (flatten chains, 3pt) ── Sprint 1
    │
    ├──▶ STORY-454 (phase tags + consolidation, 3pt) ── Sprint 2
    │
    ├──▶ STORY-455 (TOC batch, 5pt) ── Sprint 2
    │
    └──▶ STORY-456 (CoT + examples, 2pt) ── Sprint 3
```

## Supersedes

**EPIC-069** (`/ideate & discovering-requirements Anthropic Conformance Remediation (v2)`) is superseded by this epic. Reasons:
- EPIC-069 targeted 28 actionable findings from a 10-category audit
- 21 of those findings have been resolved by STORY-444 through STORY-450
- This epic (EPIC-070) targets the remaining 16 findings from a fresh 9-category conformance analysis
- EPIC-070 uses the updated analysis (`discovering-requirements-conformance-analysis.md`) which tracked prior finding resolution
- EPIC-069 should be marked `Cancelled (superseded by EPIC-070)`

## Architect Review Notes

**Complexity Score:** 4/10 — Prompt engineering epic with no runtime dependencies, no API contracts, no infrastructure changes. Two genuine technical risks (Feature 3 chain flattening and Feature 4 code block consolidation) against a backdrop of largely mechanical work.

**Key Recommendations:**
1. Feature 3: Use Option A (SKILL.md direct loads), NOT Option B (file merges) — avoids invalidating STORY-450 file targets
2. Feature 4: Split into two sub-tasks (phase output tags separate from code block consolidation)
3. Feature 5: Process 8 largest files as first verified batch before remaining 13
4. Verify `complexity-assessment-matrix.md` cross-skill reference before Feature 3 story creation

**Source:** Architect-reviewer subagent assessment, 2026-02-19

## Retrospective (Post-Epic)

*To be completed after epic completes*

---

**Epic Template Version:** 1.0
**Last Updated:** 2026-02-19
