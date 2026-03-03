---
id: EPIC-065
title: Skill Gerund Naming Convention Migration
status: Planning
start_date: 2026-02-15
target_date: 2026-04-15
total_points: 53
completed_points: 0
created: 2026-02-15
owner: DevForgeAI Framework Team
tech_lead: DevForgeAI AI Agent
team: DevForgeAI Framework
priority: MEDIUM
source_plan: .claude/plans/dev-analysis-phase2-online-docs.md
---

# Epic: Skill Gerund Naming Convention Migration

## Business Goal

DevForgeAI skill names use generic noun-form naming (`devforgeai-development`, `devforgeai-qa`, `designing-systems`) that violates Anthropic's officially recommended gerund naming convention (Source: `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md`, line 156). Gerund form (verb+-ing) names like `devforgeai-implementing-stories` more clearly describe what each skill does, improving Claude's skill discovery accuracy and aligning with platform best practices.

This migration also resolves Phase 2 analysis finding N3 (skill naming score gap) from the `/dev` command analysis. The migration requires ADR-017 because the current naming convention is LOCKED in two constitutional context files (source-tree.md line 834, coding-standards.md line 117).

**Business Value:**
- Alignment with Anthropic best practices for skill authoring
- Improved skill discovery accuracy (gerund names describe activities)
- Clearer skill naming for users and Claude
- Establishes naming convention that scales as more skills are added
- Differentiates similar skills (implementing-stories vs creating-stories)

## Success Metrics

- **Metric 1:** All 14 `devforgeai-*` skills use gerund naming (3 exempt: devforgeai-shared, claude-code-terminal-expert, skill-creator)
- **Metric 2:** All 6 constitutional context files updated with new naming convention
- **Metric 3:** All slash commands function correctly with new skill names
- **Metric 4:** Zero grep hits for old skill names in active (Tier 0-4) files

**Measurement Plan:**
- Grep scan across `.claude/`, `src/`, `CLAUDE.md`, `devforgeai/specs/context/` for old names
- Functional test of `/dev`, `/qa`, `/orchestrate` and other commands after each rename
- Review frequency: After each story completion
- Tier 5 historical files (backups, archives, feedback) are exempt from renaming

## Scope

### In Scope

1. **Feature 1: ADR-017 Creation & Constitutional Updates**
   - Create ADR-017-skill-gerund-naming-convention.md establishing the new `devforgeai-[gerund-phrase]` convention
   - Update 5 constitutional context files (source-tree.md, coding-standards.md, architecture-constraints.md, anti-patterns.md, tech-stack.md) with new naming pattern and bump versions
   - Update `.claude/memory/Constitution/` mirrors
   - Business value: Establishes legal basis for all subsequent renames; resolves constitutional conflict

2. **Feature 2: MVP Rename — devforgeai-development to devforgeai-implementing-stories**
   - Rename skill directory in both `.claude/skills/` and `src/claude/skills/`
   - Update SKILL.md frontmatter (name + description third-person fix per finding N2/R7)
   - Update 3 command files (dev.md, resume-dev.md, orchestrate.md)
   - Update ~165 reference files across CLAUDE.md, memory files, subagent files, other skills, and rules
   - Verify zero residual references with grep scan
   - Functional test with `/dev` invocation
   - Business value: Validates migration pattern; highest-impact rename (most referenced skill)

3. **Feature 3: Rename devforgeai-qa to devforgeai-validating-quality**
   - Same pattern as Feature 2 applied to QA skill
   - Estimated ~400-600 file references
   - Business value: Second most-used skill; validates pattern scales

4. **Feature 4: Rename devforgeai-story-creation to devforgeai-creating-stories**
   - Same pattern as Feature 2 applied to story creation skill
   - Estimated ~300-500 file references
   - Business value: Differentiates from implementing-stories (creates vs implements)

5. **Feature 5: Rename Remaining Skills (10 skills)**
   - Progressive migration of: architecture, ideation, orchestration, documentation, feedback, rca, release, ui-generator, subagent-creation, mcp-cli-converter
   - One story per skill for clean git history and isolated rollback
   - Proposed names (per plan Section 3.12):
     - `designing-systems` → `devforgeai-designing-architecture`
     - `devforgeai-ideation` → `devforgeai-discovering-requirements`
     - `devforgeai-orchestration` → `devforgeai-orchestrating-workflows`
     - `devforgeai-documentation` → `devforgeai-generating-documentation`
     - `devforgeai-feedback` → `devforgeai-collecting-feedback`
     - `devforgeai-rca` → `devforgeai-analyzing-root-causes`
     - `devforgeai-release` → `devforgeai-releasing-stories`
     - `devforgeai-ui-generator` → `devforgeai-generating-ui-specs`
     - `devforgeai-subagent-creation` → `devforgeai-creating-subagents`
     - `devforgeai-mcp-cli-converter` → `devforgeai-converting-mcp-cli`
   - Business value: Full fleet alignment with Anthropic best practices

6. **Feature 6: Full-Fleet Verification**
   - Final verification story confirming all skills renamed
   - All context files clean (no legacy naming references in active files)
   - All commands functional end-to-end
   - Remove "legacy accepted" language from context files
   - Business value: Ensures migration completeness and removes transition-period artifacts

### Out of Scope

- ❌ Non-`devforgeai-*` prefixed skills (claude-code-terminal-expert, skill-creator) — exempt per convention
- ❌ `devforgeai-shared` — utility module, not user-facing skill
- ❌ `devforgeai-brainstorming` — already uses gerund form, no migration needed
- ❌ Tier 5 historical files (backups, archives, feedback, completed workflows) — historical snapshots preserved as-is
- ❌ SKILL.md 500-line split (R1) — separate structural refactoring, not combined with rename to reduce risk
- ❌ XML tag addition (R3), role prompts (R4), multishot examples (R5) — separate improvement stories

## Target Sprints

### Sprint 1: Foundation & MVP
**Goal:** Establish naming convention (ADR-017) and validate with first rename
**Estimated Points:** 8
**Features:**
- Feature 1: ADR-017 Creation & Constitutional Updates (3 pts)
- Feature 2: MVP Rename — devforgeai-development → devforgeai-implementing-stories (5 pts)

**Key Deliverables:**
- ADR-017 accepted and context files updated
- `/dev` command works with new skill name
- Migration pattern validated for remaining skills

### Sprint 2: High-Priority Renames
**Goal:** Rename the next most-referenced skills
**Estimated Points:** 10
**Features:**
- Feature 3: Rename devforgeai-qa → devforgeai-validating-quality (5 pts)
- Feature 4: Rename devforgeai-story-creation → devforgeai-creating-stories (5 pts)

**Key Deliverables:**
- `/qa` and `/create-story` commands work with new skill names
- Pattern confirmed at scale (~700-1100 file references updated)

### Sprint 3: Remaining Skills (Batch 1)
**Goal:** Rename 5 medium-priority skills
**Estimated Points:** 15
**Features:**
- Feature 5 (partial): architecture, ideation, orchestration, documentation, feedback (3 pts each)

**Key Deliverables:**
- 5 additional skills renamed
- Core workflow skills all migrated

### Sprint 4: Remaining Skills (Batch 2) & Verification
**Goal:** Complete migration and verify
**Estimated Points:** 20
**Features:**
- Feature 5 (remainder): rca, release, ui-generator, subagent-creation, mcp-cli-converter (3 pts each)
- Feature 6: Full-Fleet Verification (5 pts)

**Key Deliverables:**
- All 14 skills use gerund naming
- Zero legacy name references in active files
- All commands functional

## User Stories

1. **As a** framework maintainer, **I want** skill names to follow Anthropic's gerund convention, **so that** Claude discovers and invokes skills more accurately
2. **As a** developer using `/dev`, **I want** the development skill to be named `devforgeai-implementing-stories`, **so that** the skill name clearly describes its function
3. **As a** framework architect, **I want** an ADR documenting the naming convention change, **so that** the decision is traceable and constitutional files remain consistent
4. **As a** developer creating new skills, **I want** a clear gerund naming standard, **so that** all new skills follow a consistent pattern from day one

*Note: Each feature will decompose into 1-2 detailed story documents. MVP story (Feature 2) has 8 pre-written acceptance criteria in plan Section 4.2 Step 3.*

## Technical Considerations

### Architecture Impact
- No new services or components needed
- No architecture changes — this is a mechanical rename operation
- Constitutional context files updated via ADR-017 (5 files + 5 mirrors)
- Skill directory renames in both `.claude/skills/` and `src/claude/skills/` trees

### Technology Decisions
- No new technologies required
- No library changes
- ADR-017 establishes new naming convention: `devforgeai-[gerund-phrase]`
- ADR-017 supersedes naming convention in source-tree.md v3.8 (line 834) and coding-standards.md v1.2 (line 117)

### Security & Compliance
- No security implications — file rename operations only
- No sensitive data handling changes
- Pre-commit hook validator paths must be checked for hardcoded skill names

### Performance Requirements
- No performance impact — naming is metadata only
- Skill invocation performance unchanged (Claude Code skill scanner auto-discovers from directory names)

### Technical Complexity Assessment

**Overall Complexity: 4/10 (Low)**

| Dimension | Score | Notes |
|-----------|-------|-------|
| Technology Stack | 0 | No new technologies |
| Architecture Impact | 0 | No architecture changes |
| Integration Complexity | 0 | No external integrations |
| Data Modeling | 0 | No data model changes |
| Testing Complexity | 1 | Grep-based verification tests |
| Security | 0 | No security implications |
| Performance | 0 | No performance impact |
| File Count Risk | 3 | ~169 files for MVP, ~1,425 total references |

**Risk Factor:** High file count means missed references are likely. Mitigation: post-rename grep scan (AC7 in MVP story).

## Dependencies

### Internal Dependencies
- [x] **ADR-016 exists** — Confirms ADR-017 is the next available ADR number
  - **Status:** Complete (ADR-016-dead-code-detector-read-only.md, accepted 2026-02-14)
  - **Impact if delayed:** N/A — already complete

- [ ] **Feature 1 (ADR-017) must complete before Feature 2** — Constitutional convention must change before directory renames
  - **Status:** Not Started
  - **Impact if delayed:** Blocks all rename stories

- [ ] **No active `/dev` workflows during rename** — Active story phase state files may reference old skill paths
  - **Status:** Check before each rename story
  - **Impact if delayed:** Low — pause active workflows temporarily

### External Dependencies
- None — this is an internal framework refactoring

## Risks & Mitigation

### Risk 1: Missed Reference
- **Probability:** HIGH
- **Impact:** MEDIUM (broken skill invocation until fixed)
- **Mitigation:** Post-rename grep scan across all active file tiers (AC7 in MVP story)
- **Contingency:** Quick-fix: update missed reference; if widespread: `git revert HEAD`

### Risk 2: Constitutional Violation Without ADR
- **Probability:** LOW (plan explicitly requires ADR-017 first)
- **Impact:** CRITICAL (LOCKED context files modified without governance)
- **Mitigation:** ADR-017 MUST be created and accepted in Feature 1 BEFORE any rename in Feature 2
- **Contingency:** Revert all changes if ADR not approved

### Risk 3: Convention Drift During Migration
- **Probability:** MEDIUM
- **Impact:** LOW (temporary; resolved when migration completes)
- **Mitigation:** source-tree.md explicitly marks legacy names as "accepted until migrated"; new convention enforced for NEW skills only
- **Contingency:** N/A — expected and documented

### Risk 4: Pre-Commit Hook Failure
- **Probability:** MEDIUM
- **Impact:** MEDIUM (commits blocked until validator paths updated)
- **Mitigation:** Check `.claude/scripts/devforgeai_cli/validators/` for hardcoded paths in Feature 2
- **Contingency:** Update validator paths before directory rename

### Risk 5: src/ Tree Drift
- **Probability:** MEDIUM
- **Impact:** MEDIUM (src/ and .claude/ get out of sync)
- **Mitigation:** Update both trees in same commit; verify with diff
- **Contingency:** Sync trees manually

## Stakeholders

### Primary Stakeholders
- **Product Owner:** DevForgeAI Framework Team — Decision authority on naming convention
- **Tech Lead:** DevForgeAI AI Agent — Implementation and validation

### Additional Stakeholders
- **Claude Code Users:** Invoke `/dev`, `/qa`, and other commands — will see new skill names in system-reminder
- **Framework Contributors:** May need to reference new skill names in documentation

## Communication Plan

### Status Updates
- **Frequency:** After each story completion
- **Format:** Story file status update + grep scan results
- **Audience:** Framework maintainers

### Demos
- **Sprint demos:** After MVP rename — demonstrate `/dev` works with new name
- **Milestone demos:** After full fleet migration — demonstrate all commands work

### Escalation Path
1. AskUserQuestion for ambiguity
2. ADR for architectural decisions
3. RCA for process failures

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════════════════
Week 1-2:  Sprint 1 - ADR-017 + MVP rename (devforgeai-development)
Week 3-4:  Sprint 2 - QA + Story-Creation renames
Week 5-6:  Sprint 3 - 5 medium-priority skill renames
Week 7-8:  Sprint 4 - 5 remaining renames + verification
════════════════════════════════════════════════════════════════
Total Duration: 8 weeks (3-4 sprints)
Target Release: 2026-04-15
```

### Key Milestones
- [ ] **Milestone 1:** Sprint 1 — ADR-017 accepted, MVP rename complete, `/dev` functional
- [ ] **Milestone 2:** Sprint 2 — `/qa` and `/create-story` renamed and functional
- [ ] **Milestone 3:** Sprint 4 — All 14 skills renamed, full-fleet verification passed
- [ ] **Final Release:** All grep scans clean, "legacy accepted" language removed

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint 1 | Not Started | 8 | 2 | 0 | 0 | 0 |
| Sprint 2 | Not Started | 10 | 2 | 0 | 0 | 0 |
| Sprint 3 | Not Started | 15 | 5 | 0 | 0 | 0 |
| Sprint 4 | Not Started | 20 | 6 | 0 | 0 | 0 |
| **Total** | **0%** | **53** | **15** | **0** | **0** | **0** |

*Updated automatically as sprints progress*

### Burndown
- **Total Points:** 53
- **Completed:** 0
- **Remaining:** 53
- **Velocity:** TBD after Sprint 1

### Full-Fleet Migration Status

| # | Current Name | Proposed Gerund Name | Priority | Story | Status |
|---|-------------|---------------------|----------|-------|--------|
| 1 | `devforgeai-development` | `devforgeai-implementing-stories` | MVP | TBD | Not Started |
| 2 | `devforgeai-qa` | `devforgeai-validating-quality` | HIGH | TBD | Not Started |
| 3 | `devforgeai-story-creation` | `devforgeai-creating-stories` | HIGH | TBD | Not Started |
| 4 | `designing-systems` | `devforgeai-designing-architecture` | MEDIUM | TBD | Not Started |
| 5 | `devforgeai-ideation` | `devforgeai-discovering-requirements` | MEDIUM | TBD | Not Started |
| 6 | `devforgeai-orchestration` | `devforgeai-orchestrating-workflows` | MEDIUM | TBD | Not Started |
| 7 | `devforgeai-documentation` | `devforgeai-generating-documentation` | LOW | TBD | Not Started |
| 8 | `devforgeai-feedback` | `devforgeai-collecting-feedback` | LOW | TBD | Not Started |
| 9 | `devforgeai-rca` | `devforgeai-analyzing-root-causes` | LOW | TBD | Not Started |
| 10 | `devforgeai-release` | `devforgeai-releasing-stories` | LOW | TBD | Not Started |
| 11 | `devforgeai-ui-generator` | `devforgeai-generating-ui-specs` | LOW | TBD | Not Started |
| 12 | `devforgeai-subagent-creation` | `devforgeai-creating-subagents` | LOW | TBD | Not Started |
| 13 | `devforgeai-brainstorming` | ✅ Already gerund | — | — | Compliant |
| 14 | `devforgeai-mcp-cli-converter` | `devforgeai-converting-mcp-cli` | LOW | TBD | Not Started |

**Exempt:** `devforgeai-shared` (utility), `claude-code-terminal-expert` (non-prefix), `skill-creator` (non-prefix)

## Reference Documents

- **Source Plan:** `.claude/plans/dev-analysis-phase2-online-docs.md` (Phase 3 + Phase 4)
- **Execution Prompt:** `.claude/plans/EPIC-065-create-epic-prompt.md`
- **ADR Draft:** Plan Section 4.3
- **MVP Story ACs:** Plan Section 4.2 Step 3 (8 pre-written acceptance criteria)
- **Migration Checklist:** Plan Section 3.5 (6 tiers, ~169 active files for MVP)
- **Execution Order:** Plan Section 3.7 (Steps 0 → 9)
- **Rollback Plan:** Plan Section 3.8
- **Risk Assessment:** Plan Section 3.9
- **Anthropic Best Practices:** `.claude/skills/claude-code-terminal-expert/references/skills/best-practices.md` (line 156)

## Retrospective (Post-Epic)

*To be completed after epic completes*

### What Went Well
- [TBD]

### What Could Be Improved
- [TBD]

### Lessons Learned
- [TBD]

### Metrics Achieved
- **Metric 1:** Skills using gerund naming — Actual vs 14 target
- **Metric 2:** Context files updated — Actual vs 6 target
- **Metric 3:** Zero legacy grep hits — Actual vs 0 target
- **Metric 4:** All commands functional — Actual vs 100% target

### Recommendations for Future Epics
- [TBD]

---

**Epic Template Version:** 1.0
**Created:** 2026-02-15
**Source Analysis:** Phase 2 Analysis of /dev command (scored 6.7/10 combined)
