# RCA-009: /qa Command Business Logic Violation

**Date:** 2025-11-14
**Severity:** Medium
**Category:** Architecture Compliance
**Status:** RESOLVED
**Resolution:** STORY-034

---

## Issue Summary

After STORY-024 (wire hooks into /qa command) was implemented, the /qa command contained business logic in Phases 4 & 5, violating the lean orchestration pattern principle "Commands orchestrate. Skills validate. Subagents specialize."

**Impact:**
- Command grew to 509 lines (approaching 15K budget limit at 92%)
- Business logic in wrong architectural layer
- Pattern compliance violation
- Token inefficiency (~8K in main conversation)

---

## Root Cause Analysis

### What Happened

**Timeline:**
1. **2025-11-05:** /qa command refactored (692 → 295 lines, lean orchestration achieved)
2. **2025-11-06:** STORY-024 implemented (added Phase 4 for feedback hooks)
3. **2025-11-13:** Phase 5 added for story status updates after QA approval
4. **2025-11-13:** Command grew to 509 lines with business logic in Phases 4 & 5

**Phases 4 & 5 contained:**
- Phase 4: Status determination, check-hooks invocation, invoke-hooks with context (77 lines)
- Phase 5: Story file reading, YAML editing, QA Validation History insertion, workflow history appending (87 lines)
- **Total:** 164 lines of business logic in command

### Root Cause

**Primary:** Phases 4 & 5 implemented in command instead of skill

**Contributing Factors:**
1. **Incremental feature addition:** STORY-024 added Phase 4 to command (expedient but violated pattern)
2. **Missing Phase 5 in skill:** No corresponding phase existed in skill for story updates
3. **Pattern awareness:** Business logic creep not immediately detected
4. **No automated pattern validation:** No CI check enforcing lean orchestration compliance

### Why It Matters

**Architectural Concerns:**
- Commands should orchestrate, not implement business logic
- Skills designed for multi-phase workflows with execution model
- Progressive disclosure pattern broken (business logic inline, not in references)

**Practical Concerns:**
- Command at 92% of 15K budget (high risk of exceeding limit)
- Token inefficiency (business logic in main conversation)
- Maintainability (logic duplicated across command/skill layers)

---

## Resolution (STORY-034)

### Actions Taken

**1. Moved Phase 4 to Skill as Phase 6:**
- Extracted 77 lines of feedback hook logic
- Created `references/feedback-hooks-workflow.md` (327 lines)
- Added Phase 6 to devforgeai-qa skill with bash implementation

**2. Moved Phase 5 to Skill as Phase 7:**
- Extracted 87 lines of story update logic
- Created `references/story-update-workflow.md` (378 lines)
- Added Phase 7 to devforgeai-qa skill with Edit/Read implementation

**3. Refactored Command to 3 Phases:**
- Merged old Phase 2 & 3 into single Display Results phase
- Removed Phases 4 & 5 entirely
- Added note documenting skill handles Phases 6 & 7

**4. Updated Tests:**
- Updated STORY-024 tests to check skill instead of command
- Created 33 new tests for STORY-034 refactoring validation
- All 69 tests passing (100% pass rate)

### Results

**Metrics:**
- Command: 509 → 307 lines (39.7% reduction)
- Command: 13,775 → 8,172 characters (40.7% reduction)
- Budget: 92% → 54% (well under 15K limit)
- Tests: 69/69 passing (zero functional regressions)

**Pattern Compliance:**
- Command phases: 3 (Phase 0, 1, 2) ✅
- Command responsibilities: Parse, load, invoke, display ✅
- No business logic in command ✅
- Business logic in skill (Phases 6 & 7) ✅
- **Compliance: 100%** ✅

---

## Lessons Learned

### What Went Well

1. **Quick detection:** Issue identified within 1 day of Phase 5 addition
2. **Clear solution:** Lean orchestration pattern provided obvious fix path
3. **Test coverage:** Existing tests ensured zero regressions during refactoring
4. **Pattern reuse:** Successfully applied proven refactoring techniques from earlier cases

### What Could Be Improved

1. **Preventative measures:** Need automated pattern validation in CI/CD
2. **Feature addition vigilance:** New features should be evaluated for pattern compliance before implementation
3. **Skill-first enforcement:** Should default to implementing in skill, not command

### Preventative Actions

**Immediate (Completed):**
- ✅ STORY-034 resolved the violation (100% pattern compliance)
- ✅ Updated case studies with STORY-034 lessons
- ✅ Documented business logic creep risk

**Near-term (Recommended):**
- [ ] Add automated pattern validation to pre-commit hooks
- [ ] Create command/skill architecture decision checklist
- [ ] Add "Where should this logic go?" flowchart to developer guide

**Long-term (Future):**
- [ ] CI/CD check for command character budget compliance
- [ ] Automated lean pattern validation in code reviews
- [ ] Pattern compliance dashboard

---

## Impact Assessment

**Before Resolution:**
- ❌ Pattern violation (business logic in command)
- ⚠️ Budget at 92% (high risk)
- ⚠️ Token inefficiency (~8K in main conversation)

**After Resolution:**
- ✅ Pattern compliance 100%
- ✅ Budget at 54% (safe margin)
- ✅ Token efficiency improved (69% savings)
- ✅ All tests passing (zero regressions)

**User Impact:** None (internal refactoring, no functional changes)

---

## Related

**Story:** STORY-034 (implementation)
**Epic:** EPIC-007 (lean orchestration compliance)
**Pattern:** lean-orchestration-pattern.md
**Case Study:** refactoring-case-studies.md (Case Study 2 - Addendum)
**Previous RCAs:** RCA-006 (deferrals), RCA-007 (multi-file creation), RCA-008 (git stashing)

---

## Conclusion

STORY-034 successfully resolved the lean orchestration pattern violation by moving business logic from command to skill, reducing command size by 40%, and achieving 100% pattern compliance.

**Key Takeaway:** Vigilance required to prevent business logic creep in commands. Default to skill-first implementation for new features.

**Status:** ✅ RESOLVED (2025-11-14)
