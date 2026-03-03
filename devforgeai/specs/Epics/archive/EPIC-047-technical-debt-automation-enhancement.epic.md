---
id: EPIC-047
title: Technical Debt Automation Enhancement
status: Cancelled
start_date: 2026-01-20
target_date: 2026-02-17
total_points: 34
completed_points: 0
created: 2026-01-19
owner: User
tech_lead: Claude
team: DevForgeAI
priority: High
---

# Epic: Technical Debt Automation Enhancement

## Business Goal

Close automation gaps in technical debt discovery and remediation workflow. Currently, debt discovered during QA review or manual AC verification is NOT automatically captured in the technical debt register - users must explicitly request updates. Additionally, after debt is recorded, there is no "next steps" workflow to guide remediation actions.

This epic delivers:
1. **Automated debt capture** from all discovery points (QA, manual verification)
2. **Structured debt format** enabling machine-readable parsing
3. **Next steps workflow** prompting remediation actions after debt is recorded
4. **Prevention mechanisms** alerting developers to existing debt before compounding

## Success Metrics

- **Metric 1:** 100% of spec deviations detected during QA are auto-prompted for debt register addition
- **Metric 2:** 100% of `/verify-ac` findings are auto-prompted for debt register addition
- **Metric 3:** "Next Steps" workflow triggers after every debt item addition
- **Metric 4:** `/dev` pre-flight warns about related debt items before development starts

**Measurement Plan:**
- Track via user testing with existing STORY files
- Baseline: 0% automation (manual requests only)
- Target: 100% automated prompts
- Review: After each sprint

## Scope

### In Scope

1. **Feature F1: Technical Debt Register v2.0 Format Migration** (5 pts)
   - Convert to Hybrid YAML + Markdown format
   - Add structured `entries` array with typed fields
   - Include `cross_references` object for bidirectional traceability (AC→Debt, Debt→Story, Epic→Debt, ADR→Debt)
   - Enable cross-session queryability via Grep patterns
   - Enable machine-readable parsing for automation

2. **Feature F2: QA-to-Technical-Debt Bridge** (8 pts)
   - Add Step 6.5 to QA report-generation workflow
   - Auto-detect spec deviations for debt tracking
   - Prompt user confirmation before adding to register

3. **Feature F3: Standalone /verify-ac Command** (8 pts)
   - New slash command for ad-hoc AC verification
   - Add `--verify-ac` flag to existing `/qa` command
   - Create `devforgeai-ac-verification` skill

4. **Feature F4: Next Steps Workflow After Debt Addition** (8 pts)
   - Create `devforgeai-debt-workflow` skill
   - Options: Create remediation story, Create debt epic, Add to sprint
   - Auto-trigger after any debt item addition

5. **Feature F5: Debt Compounding Prevention - Dev Pre-flight** (3 pts)
   - Add pre-flight check to `/dev` command
   - Warn about related existing debt
   - Prompt for acknowledgment or resolution

6. **Feature F6: Debt Compounding Prevention - Story Creation** (2 pts)
   - Add related debt check to `/create-story`
   - Display related debt during story discovery
   - Offer linking options

### Out of Scope

- Automatic debt resolution (requires human judgment)
- Debt aging alerts and escalation (future epic)
- Cross-project debt tracking (single project only)
- Debt metrics dashboard (future epic)

## Target Sprints

### Sprint 1: Foundation + Core Automation

**Goal:** Establish v2.0 format and implement primary automation bridges
**Estimated Points:** 21
**Features:** F1, F2, F3

**Key Deliverables:**
- Technical Debt Register v2.0 format
- QA → Debt bridge operational
- `/verify-ac` command available

### Sprint 2: Workflow + Prevention

**Goal:** Complete next steps workflow and prevention mechanisms
**Estimated Points:** 13
**Features:** F4, F5, F6

**Key Deliverables:**
- Next Steps workflow prompts after debt addition
- Dev pre-flight warns about related debt
- Story creation checks for related debt

## User Stories

High-level user stories to be decomposed into detailed stories:

1. **As a** DevForgeAI user, **I want** the debt register to use structured YAML format, **so that** automation can reliably parse and update debt items.

2. **As a** DevForgeAI user, **I want** QA spec deviations to auto-prompt for debt register addition, **so that** discovered debt is never lost.

3. **As a** DevForgeAI user, **I want** a `/verify-ac` command, **so that** I can verify acceptance criteria and capture deviations without running full QA.

4. **As a** DevForgeAI user, **I want** "Next Steps" options after debt is recorded, **so that** I'm guided toward remediation actions.

5. **As a** DevForgeAI user, **I want** `/dev` to warn me about existing debt on related files, **so that** I don't unknowingly compound technical debt.

6. **As a** DevForgeAI user, **I want** `/create-story` to show related debt items, **so that** I can scope stories appropriately.

*Note: Each high-level story will decompose into 1-3 detailed story documents.*

## Technical Considerations

### Architecture Impact

- **New Skills:** `devforgeai-ac-verification`, `devforgeai-debt-workflow`
- **New Command:** `/verify-ac`
- **Modified Skills:** `devforgeai-qa`, `devforgeai-development`, `devforgeai-story-creation`
- **Data Format:** Technical debt register v2.0 (YAML + Markdown hybrid)

### Technology Decisions

- **ADR-012 Required:** Technical Debt Register v2.0 Format (before implementation)
- **No new technologies:** All changes use existing Claude Code terminal patterns
- **Markdown-based:** Skills and commands follow established framework patterns

### Security & Compliance

- No sensitive data in debt register
- User confirmation required before register updates (prompt-first pattern)
- No external API calls

### Performance Requirements

- Debt register parsing: <100ms for <100 items
- Pre-flight check impact: <500ms additional startup time
- Lazy loading with Grep for large registers

## Dependencies

### Internal Dependencies

- [x] **ac-compliance-verifier subagent exists** (v1.3)
  - Status: Complete
  - Impact if missing: F3 would require subagent creation

- [x] **technical-debt-analyzer subagent exists**
  - Status: Complete (may need v2.0 format update)
  - Impact if missing: F4 would have limited analysis

### External Dependencies

- None (pure framework enhancement)

## Risks & Mitigation

### Risk 1: QA Skill Integration Complexity

- **Probability:** Medium
- **Impact:** High
- **Mitigation:** Extract debt bridge to separate reference file (`technical-debt-bridge.md`)
- **Contingency:** Gate on PASS WITH WARNINGS status only

### Risk 2: Circular Dependency in Debt Workflow

- **Probability:** Low
- **Impact:** High (would violate architecture constraints)
- **Mitigation:** Design `devforgeai-debt-workflow` as terminal skill (recommendations only, no skill invocations)
- **Contingency:** User decision points via AskUserQuestion

### Risk 3: Pre-flight Performance Degradation

- **Probability:** Medium (with large debt registers)
- **Impact:** Medium
- **Mitigation:** Lazy loading with Grep, threshold-based full load
- **Contingency:** Index file for >50 items (future enhancement)

### Risk 4: Backward Compatibility

- **Probability:** Low
- **Impact:** Low
- **Mitigation:** Version header, backward-compatible parser during transition
- **Contingency:** Migration script documented in register header

## Stakeholders

### Primary Stakeholders

- **Product Owner:** User - Requirements and acceptance
- **Tech Lead:** Claude - Architecture and implementation
- **Framework Team:** DevForgeAI - Pattern compliance

## Communication Plan

### Status Updates

- **Frequency:** Per sprint
- **Format:** Story completion tracking
- **Audience:** User

### Escalation Path

1. Story blockers → Tech Lead (Claude)
2. Architecture concerns → ADR creation
3. Scope changes → User approval

## Timeline

```
Epic Timeline:
════════════════════════════════════════════════════
Week 1-2:  Sprint 1 - Foundation + Core Automation
           F1: Debt Register v2.0 Format
           F2: QA-to-Debt Bridge
           F3: /verify-ac Command
Week 3-4:  Sprint 2 - Workflow + Prevention
           F4: Next Steps Workflow
           F5: Dev Pre-flight Check
           F6: Story Creation Check
════════════════════════════════════════════════════
Total Duration: 4 weeks (2 sprints)
Target Release: 2026-02-17
```

### Key Milestones

- [ ] **Milestone 1:** 2026-01-27 - F1 complete (v2.0 format operational)
- [ ] **Milestone 2:** 2026-02-03 - Sprint 1 complete (core automation)
- [ ] **Milestone 3:** 2026-02-17 - Sprint 2 complete (full epic delivery)

## Progress Tracking

### Sprint Summary

| Sprint | Status | Points | Stories | Completed | In Progress | Blocked |
|--------|--------|--------|---------|-----------|-------------|---------|
| Sprint-1 | Not Started | 21 | ~8 | 0 | 0 | 0 |
| Sprint-2 | Not Started | 13 | ~5 | 0 | 0 | 0 |
| **Total** | **0%** | **34** | **~13** | **0** | **0** | **0** |

### Burndown

- **Total Points:** 34
- **Completed:** 0
- **Remaining:** 34
- **Velocity:** TBD (after Sprint 1)

## User Locked Preferences

**These decisions are LOCKED per user specification:**

| Decision | Choice |
|----------|--------|
| Automation Level | **Prompt first** (confirm before adding to register) |
| Next Steps Options | **Remediation story**, **Debt epic**, **Add to sprint** |
| Command Design | **Both** standalone `/verify-ac` AND `/qa --verify-ac` flag |
| Format | **Hybrid YAML + Markdown** |

## Feature Dependency Graph

```
F1 (Register v2.0) ─┬─> F2 (QA Bridge) ──> F4 (Next Steps)
                    ├─> F3 (verify-ac)
                    ├─> F5 (Dev Pre-flight)
                    └─> F6 (Story Creation Check)
```

**Critical Path:** F1 → F2 → F4

## Prerequisite Actions

1. **ADR-012:** Create Architecture Decision Record for Debt Register v2.0 Format (BEFORE Sprint 1)

## Retrospective (Post-Epic)

*To be completed after epic completes*

### What Went Well
- TBD

### What Could Be Improved
- TBD

### Lessons Learned
- TBD

### Metrics Achieved
- **Metric 1:** TBD
- **Metric 2:** TBD
- **Metric 3:** TBD
- **Metric 4:** TBD

---

**Epic Template Version:** 1.0
**Plan Reference:** `/home/bryan/.claude/plans/jaunty-weaving-barto.md`
**Created:** 2026-01-19
