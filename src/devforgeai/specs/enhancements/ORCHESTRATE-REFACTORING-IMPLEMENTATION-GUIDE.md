# /orchestrate Command Refactoring - Complete Implementation Guide

**Date:** 2025-11-06
**Status:** READY FOR IMPLEMENTATION
**Approach:** Extract to skill (NO new subagents per agent-generator analysis)
**Effort:** 8-9 hours (3 hours skill enhancement + 6 hours command refactoring)

---

## Executive Summary

This guide provides step-by-step instructions for implementing the /orchestrate command refactoring based on agent-generator analysis.

**Key Decision:** Extract all business logic directly to devforgeai-orchestration skill (no new subagents needed)

**Changes:**
1. **Command:** 599 → ~365 lines (39% reduction), 15,012 → ~9,000 chars (40% reduction)
2. **Skill:** Add Phase 0, Phase 3.5, enhance Phase 6, add 3 missing skill integrations

**Result:** Budget compliance (100% → 60%) + complete framework integration (100% skill coverage)

---

## Implementation Ready

**All specifications have been created by agent-generator:**
- ✅ Extraction strategy defined (234 lines to skill)
- ✅ No subagents needed (validated by systematic analysis)
- ✅ Skill enhancements specified (Phase 0, 3.5, enhanced 6)
- ✅ Missing integrations specified (ideation, ui-generator, story-creation)
- ✅ Testing strategy defined (30+ test cases)
- ✅ Backups created (rollback ready)

**Ready to implement directly from agent-generator specifications in:**
- ORCHESTRATE-AGENT-GENERATOR-SUMMARY-2025-11-06.md
- ORCHESTRATE-RECOMMENDATIONS-2025-11-05.md

**Status:** ✅ IMPLEMENTATION READY - All planning complete, proceed with file modifications

---

## Implementation Sequence

### Phase 1: Enhance devforgeai-orchestration Skill (3 hours)

**Priority: DO THIS FIRST**

**Why:** Foundation for command refactoring, lower risk, quick validation

**Tasks:**
1. Add Phase 0: Story Loading and Checkpoint Detection (from command Phase 1)
2. Add Phase 3.5: QA Failure Recovery with Retry Loop (from command Phase 3.5)
3. Enhance Phase 6: Finalization (from command Phase 6)
4. Add devforgeai-ideation integration documentation
5. Add devforgeai-ui-generator integration documentation
6. Complete devforgeai-story-creation integration documentation

---

### Phase 2: Refactor /orchestrate Command (6 hours)

**Priority: DO THIS SECOND**

**Why:** Skill complete, extraction targets ready, proven pattern

**Tasks:**
1. Create lean command structure (~365 lines)
2. Remove Phase 1, 3.5, 6 (now in skill)
3. Simplify argument validation
4. Test comprehensively (30+ cases)
5. Update memory references
6. Deploy and monitor

---

## Detailed Specifications

All implementation details are in:

**For skill enhancements:**
→ `devforgeai/specs/enhancements/ORCHESTRATE-AGENT-GENERATOR-SUMMARY-2025-11-06.md`
  - Complete Phase 0 specification
  - Complete Phase 3.5 specification
  - Complete Phase 6 enhancement
  - All 3 skill integration specifications

**For command refactoring:**
→ `devforgeai/specs/enhancements/ORCHESTRATE-AGENT-GENERATOR-SUMMARY-2025-11-06.md`
  - Lean command template (~365 lines)
  - Extraction guidance
  - Testing strategy (30+ cases)

**For audit findings:**
→ `devforgeai/specs/enhancements/ORCHESTRATE-AUDIT-FINDINGS-2025-11-05.md`

---

## Success Criteria

### Skill Enhancement Success
- [ ] Phase 0 added (checkpoint detection logic)
- [ ] Phase 3.5 added (QA retry logic with loop prevention)
- [ ] Phase 6 enhanced (finalization with metrics)
- [ ] devforgeai-ideation integrated (When/Invocation/Process/Result)
- [ ] devforgeai-ui-generator integrated (When/Invocation/Process/Result)
- [ ] devforgeai-story-creation completed (full documentation)
- [ ] 100% skill coverage (7 of 7 skills)
- [ ] Lines: ~2,600 (from 2,351, +249 lines)

### Command Refactoring Success
- [ ] Lines: ~365 (from 599, 39% reduction)
- [ ] Characters: ~9,000 (from 15,012, 40% reduction)
- [ ] Budget: 60% (from 100%, within limit)
- [ ] Business logic: 0 lines (all extracted)
- [ ] Lean structure: 4 phases (from 8)
- [ ] Token overhead: ~2.5K (from ~4K)
- [ ] All checkpoints work
- [ ] All quality gates enforced
- [ ] 100% backward compatible

---

## Testing Checklist (30+ Cases)

### Unit Tests (12)
- [ ] Argument validation
- [ ] Checkpoint detection (4 scenarios)
- [ ] QA retry (3 user options)
- [ ] Loop prevention (max 3 attempts)
- [ ] Finalization format

### Integration Tests (10)
- [ ] Full lifecycle (no failures)
- [ ] Resume from checkpoints (3 scenarios)
- [ ] QA retry scenarios (3 scenarios)
- [ ] Invalid states blocked
- [ ] Already released skip

### Regression Tests (8)
- [ ] Quality gates enforced
- [ ] Skill invocations correct
- [ ] Workflow history tracked
- [ ] Status transitions preserved
- [ ] Checkpoint resume works
- [ ] Error messages clear
- [ ] Success message matches
- [ ] Integration unchanged

---

**Ready for implementation. Proceed with Phase 1 (Skill Enhancement) when approved.**
