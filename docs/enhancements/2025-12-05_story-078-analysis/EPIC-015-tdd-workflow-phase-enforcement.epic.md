---
id: EPIC-015
title: TDD Workflow Phase Enforcement
status: Proposed
created: 2025-12-05
business_value: HIGH
complexity_score: 14
complexity_tier: 1
target_sprint: Sprint-TBD
---

# EPIC-015: TDD Workflow Phase Enforcement

## Executive Summary

Enhance devforgeai-development skill to prevent phase skipping through mandatory validation checkpoints, eliminating systematic workflow incompleteness pattern identified in RCA-009, RCA-013, and RCA-018.

**Business Problem:** Claude skips administrative phases (4.5-7) after implementation phases (0-4) succeed, causing incomplete DoD updates, missing story commits, and requiring user intervention. Incident rate: 3 occurrences in 21 days (14% of /dev executions).

**Solution:** Apply proven validation checkpoint pattern from Phases 2-3 to Phases 4.5-7, integrate with todo list enforcement, add final self-check before completion declaration.

**Expected Outcome:** Zero phase-skipping incidents, 95%+ workflow completion without user intervention, 100% DoD accuracy.

---

## Business Context

### Current Pain Points

1. **User Intervention Required (50% of executions)**
   - User must manually check if phases completed
   - User must prompt Claude to finish skipped phases
   - User must verify story file updated correctly

2. **Workflow Inconsistency (3 incidents in 21 days)**
   - RCA-009 (STORY-027): Skipped Phases 1-6 steps
   - RCA-013 (STORY-057): Stopped at 87% twice
   - RCA-018 (STORY-078): Skipped Phases 4.5-7

3. **Documentation Incomplete**
   - DoD items not marked [x]
   - Implementation Notes missing
   - Story status not updated
   - Git commits incomplete

### Root Cause (from RCA-018)

Missing enforcement checkpoints for Phases 4.5-7. Claude's execution model treats "tests passing + code written" as completion signal, ignoring mandatory administrative work.

### Value Proposition

**For Users:**
- Zero intervention needed for standard stories
- Trust that /dev completes 100% of workflow
- Accurate DoD tracking without manual verification

**For Framework:**
- Workflow integrity guaranteed by checkpoints
- Pattern consistency across all skills
- Self-enforcing quality (can't skip phases)

**For DevForgeAI Credibility:**
- Reliable execution of documented workflows
- Professional quality (works as specified)
- User confidence in framework automation

---

## Success Metrics

### Quantitative

| Metric | Baseline | Target | Measurement |
|--------|----------|--------|-------------|
| Phase-skipping incidents | 3/month | 0/month | Count of RCAs filed for phase skipping |
| Workflow completion rate | 50% | 95%+ | % of /dev executions requiring zero user intervention |
| DoD accuracy | ~75% | 100% | % of completed stories with all DoD items marked correctly |
| User intervention rate | 50% | <5% | % of /dev executions where user must prompt completion |

### Qualitative

- ✅ Users trust /dev workflow completes fully
- ✅ No confusion about whether workflow finished
- ✅ Story files accurately reflect work done
- ✅ Pattern documented for reuse in other skills

---

## Epic Scope

### In Scope

1. Add 5 validation checkpoints (Phases 4.5, 4.5-5 Bridge, 5, 6, 7)
2. Integrate todo list with checkpoint enforcement
3. Add final workflow completion self-check
4. Document phase resumption protocol
5. Create pattern knowledge base (PATTERNS.md)

### Out of Scope

- Applying pattern to other skills (devforgeai-qa, devforgeai-release) - Future epic
- Automated checkpoint generation tooling - Future enhancement
- Runtime enforcement by system (non-Claude mechanism) - Requires platform changes

### Dependencies

- RCA-018 analysis (completed)
- Existing Phase 2-3 checkpoint pattern (proven)
- devforgeai-development skill SKILL.md (target for changes)

---

## Features

### Feature 1: Phase Validation Checkpoints

**Description:** Add validation checkpoints after Phases 4.5, 4.5-5 Bridge, 5, 6, and 7 to verify mandatory steps completed before progression.

**User Stories:**
- As a development workflow, I want to verify Phase 4.5 completed before allowing Phase 4.5-5 Bridge, so that deferrals are always validated
- As a development workflow, I want to verify DoD updated before git commit, so that pre-commit hooks don't fail
- As a development workflow, I want to verify dev-result-interpreter invoked, so that result displays follow lean orchestration pattern

**Acceptance Criteria:**
- Each of 5 phases has checkpoint section in SKILL.md
- Checkpoint searches conversation history for execution evidence
- Checkpoint HALTs with clear error if evidence missing
- Checkpoint allows progression only when all steps verified

**Implementation:**
- File: `.claude/skills/devforgeai-development/SKILL.md`
- Pattern: Copy Phase 2 Validation Checkpoint structure
- Customize: Evidence search criteria per phase requirements
- Test: Verify HALT on skip, verify PASS on complete

---

### Feature 2: Todo List Checkpoint Integration

**Description:** Modify TodoWrite usage to enforce checkpoint-first pattern where phase cannot be marked "completed" without checkpoint validation passing.

**User Stories:**
- As a todo tracker, I want to block "completed" status until checkpoint passes, so that todo list reflects actual completion
- As a phase transition, I want to require checkpoint validation before TodoWrite, so that phases cannot be falsely marked complete

**Acceptance Criteria:**
- TodoWrite pattern documented in SKILL.md shows checkpoint-first enforcement
- Each phase transition executes checkpoint BEFORE TodoWrite
- Cannot mark phase "completed" without passing checkpoint
- Clear enforcement rule: "Checkpoint → TodoWrite" not "TodoWrite → Checkpoint"

**Implementation:**
- File: `.claude/skills/devforgeai-development/SKILL.md`
- Section: "Workflow Execution Checklist" (lines 118-150)
- Change: Add enforcement pattern documentation
- Test: Verify pattern described clearly for all 7 phase transitions

---

### Feature 3: Workflow Completion Self-Check

**Description:** Add final validation before declaring workflow complete that counts all 10 checkpoints and HALTs if any missing.

**User Stories:**
- As a workflow completion, I want to count all checkpoints passed before declaring success, so that no phases are skipped
- As a completion banner, I want to display only after 10/10 checkpoints pass, so that "COMPLETE" means actually complete

**Acceptance Criteria:**
- Final self-check section added to SKILL.md
- Self-check counts 10 phase checkpoints (0, 1, 2, 3, 4, 4.5, 4.5-5, 5, 6, 7)
- HALTs if count <10 with list of missing checkpoints
- Displays "COMPLETE" banner only after 10/10 checkpoints pass

**Implementation:**
- File: `.claude/skills/devforgeai-development/SKILL.md`
- Location: After "Complete Workflow Execution Map" section
- Content: Checkbox validation + count + conditional HALT
- Test: Verify catches skipped phases before completion

---

### Feature 4: Phase Resumption Protocol

**Description:** Document how to resume workflow when stopping occurs mid-execution.

**User Stories:**
- As a user, I want to resume from stopped phase without re-executing completed work, so that I don't waste time
- As Claude, I want clear steps for resuming workflow, so that I don't duplicate work or skip verification

**Acceptance Criteria:**
- Resumption protocol section added to SKILL.md
- User detection indicators documented (how to know workflow stopped)
- User recovery command pattern provided
- Claude resumption steps documented (5 steps)
- Resumption checkpoint validates previous phases

**Implementation:**
- File: `.claude/skills/devforgeai-development/SKILL.md`
- Location: After "Complete Workflow Execution Map"
- Content: User guide + Claude steps + verification checklist
- Test: Simulate stop after Phase 4, issue resume command, verify continues from Phase 4.5

---

### Feature 5: Pattern Knowledge Base

**Description:** Create `devforgeai/RCA/PATTERNS.md` documenting "Premature Workflow Completion" recurring pattern.

**User Stories:**
- As future RCA analysis, I want to recognize recurring patterns immediately, so that I can reference known solutions
- As framework monitoring, I want documented patterns with detection/prevention strategies, so that I can track if fixes worked

**Acceptance Criteria:**
- PATTERNS.md file created in `devforgeai/RCA/`
- Pattern documented with ID, behavior, root cause, solution, detection, prevention
- Links to related RCAs (RCA-009, RCA-013, RCA-018)
- Metrics section showing incident rate and fix date

**Implementation:**
- File: `devforgeai/RCA/PATTERNS.md` (new file)
- Content: Pattern template with PATTERN-001 fully documented
- Reference: From REC-5 in RCA-018
- Test: Verify pattern recognition in next phase-skipping incident (if any)

---

## Architecture Notes

**Pattern Replication:**
- Proven pattern from Phase 2-3 checkpoints (zero skip incidents)
- Copy structure, customize evidence search
- Maintain HALT-on-failure consistency

**Integration Points:**
- devforgeai-development SKILL.md (primary target)
- TodoWrite tool (enforcement integration)
- Phase reference files (checkpoint integration)

**Future Expansion:**
- Apply to devforgeai-qa skill (7 phases)
- Apply to devforgeai-orchestration skill (11 states)
- Apply to devforgeai-release skill (6 phases)

---

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Checkpoint adds token overhead | Medium | Low | Checkpoints are lightweight (~200 tokens each), total +1K tokens acceptable |
| False positives (checkpoint blocks valid workflow) | Low | Medium | Test with 3 diverse stories, tune evidence search patterns |
| Pattern doesn't prevent future skipping | Low | High | Monitor for 1 sprint, if recurs investigate deeper cause |

---

## Implementation Roadmap

**Sprint 1: Core Checkpoints (REC-1)**
- Week 1: Implement 5 phase validation checkpoints
- Week 2: Test checkpoints with sample stories
- Deliverable: All checkpoints functional, tested, merged

**Sprint 2: Enforcement & Documentation (REC-2, REC-3, REC-4)**
- Week 3: Integrate todo list enforcement, add final self-check
- Week 4: Document resumption protocol, create PATTERNS.md
- Deliverable: Complete enforcement system documented

**Sprint 3: Validation (Monitor)**
- Run /dev on 5 different stories
- Measure: Phase-skipping incidents (target: 0)
- Measure: User intervention rate (target: <5%)
- Decision: Mark RCA-018 RESOLVED or investigate further

---

## Success Criteria

**Epic Complete When:**
- [ ] 5 validation checkpoints added (Phases 4.5-7)
- [ ] Todo list checkpoint-first pattern documented
- [ ] Final workflow completion self-check implemented
- [ ] Phase resumption protocol documented
- [ ] PATTERNS.md created with PATTERN-001
- [ ] All checkpoints tested and functional
- [ ] Zero phase-skipping incidents for 1 sprint
- [ ] User intervention rate <5%
- [ ] RCA-018 marked RESOLVED

---

## Related Documentation

- **RCA-018:** Development Skill Phase Completion Skipping (root cause analysis)
- **RCA-009:** Incomplete Skill Workflow Execution (first identification)
- **RCA-013:** Development Workflow Stops Before Completion (recurrence)
- **.claude/skills/devforgeai-development/SKILL.md:** Target file for changes
- **devforgeai/protocols/lean-orchestration-pattern.md:** Checkpoint pattern aligns with lean principles

---

**Epic Owner:** DevForgeAI Framework Team
**Estimated Effort:** 4-6 hours
**Priority:** CRITICAL (blocks user workflows)
**Target Completion:** Sprint 1 (Week 1-2)

