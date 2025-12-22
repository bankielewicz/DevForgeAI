# Phase 2 Implementation Handoff Prompt

**Purpose:** Start a new Claude Code session to implement Phase 2 (Structured Templates)
**Prerequisites:** Phase 1 successfully deployed and validated
**Timeline:** 4 weeks (Weeks 4-8)
**Use this prompt:** Copy the prompt below into a new Claude Code Terminal session

---

## 🚀 **Prompt for New Session**

```
I need you to implement Phase 2 of the RCA-006 enhancement for the DevForgeAI framework.

CONTEXT:
- Phase 1 has been successfully implemented and deployed
- Phase 1 eliminated autonomous deferrals (70% → <10% deferral rate)
- Decision Point 1 resulted in GO (proceed to Phase 2)
- Now need to implement structured technical specifications

TASK:
Implement Phase 2 following the complete implementation plan at:
@devforgeai/specs/enhancements/PHASE2-IMPLEMENTATION-PLAN.md

KEY REQUIREMENTS:
1. Read and follow the Phase 2 implementation plan completely
2. Create machine-readable YAML format for Technical Specifications
3. Build migration script to convert v1.0 (freeform) → v2.0 (structured) stories
4. Create validation library (validate_tech_spec.py) to parse and validate YAML
5. Update story creation skill to generate structured format
6. Implement dual format support (backward compatibility)
7. Execute pilot migration (10 stories) before full migration
8. Maintain complete rollback capability at each step

IMPORTANT CONTEXT FILES TO READ:
@devforgeai/specs/enhancements/PHASE2-IMPLEMENTATION-PLAN.md
@devforgeai/specs/enhancements/RCA006-COMPLETE-ROADMAP.md
@devforgeai/specs/enhancements/PHASE1-IMPLEMENTATION-SUMMARY.md
@.claude/skills/devforgeai-story-creation/SKILL.md
@.claude/skills/devforgeai-story-creation/references/technical-specification-guide.md
@.claude/skills/devforgeai-story-creation/assets/templates/story-template.md

EXECUTION APPROACH:
1. Create comprehensive todo list for all Phase 2 work
2. Execute each task sequentially with progress reports
3. HALT if you encounter any ambiguity or need clarification
4. Create backups before any file modifications
5. Test incrementally (don't wait until end)
6. Document all decisions and changes

CONSTRAINTS:
- Follow lean orchestration pattern (commands delegate to skills)
- Maintain DevForgeAI framework principles (spec-driven, zero technical debt)
- No aspirational content (only proven, feasible solutions)
- Use native tools (Read, Edit, Write, not Bash for file operations)
- Preserve backward compatibility (dual format support required)

TIMELINE:
Week 2 (now): Design & Specification (5 days, ~30 hours)
Week 3: Migration Tooling (5 days, ~30 hours)
Week 4: Pilot Migration (5 days, ~24 hours)
Week 5: Full Migration (5 days, ~30 hours)

SUCCESS CRITERIA:
- [ ] Structured YAML format defined and documented
- [ ] validate_tech_spec.py functional (can parse and validate)
- [ ] migrate_story_v1_to_v2.py reliable (≥95% success rate)
- [ ] Pilot migration successful (10 stories, 100% success)
- [ ] Full migration successful (all stories migrated)
- [ ] Dual format support working (v1.0 + v2.0 both work)
- [ ] /dev command works with v2.0 stories
- [ ] Parsing accuracy ≥95%
- [ ] Zero data loss during migration

DELIVERABLES:
By end of Phase 2:
- 8 modified files (~1,400 lines added)
- 3 new files (~1,000 lines)
- 3 documentation files (~1,500 lines)
- All stories migrated to v2.0 format
- Complete testing results
- GO/NO-GO decision for Phase 3

START BY:
1. Reading PHASE2-IMPLEMENTATION-PLAN.md completely
2. Creating detailed todo list (20-30 tasks)
3. Executing Week 2 Day 1: Format Design (6 hours)

REPORT PROGRESS:
- After completing each major section
- HALT immediately if you need clarification
- Use TodoWrite to track all tasks

NO TIME CONSTRAINTS - Be thorough and comprehensive!

Ready to begin Phase 2 implementation?
```

---

## 📋 **Session Preparation Checklist**

Before starting the new session, ensure:

**Prerequisites validated:**
- [ ] Phase 1 testing complete (9 test cases passed)
- [ ] Phase 1 deployed to production
- [ ] 10 stories monitored with Phase 1 active
- [ ] Deferral rate measured (should be <10%)
- [ ] Decision Point 1 evaluated (GO decision made)
- [ ] User feedback collected (satisfaction ≥80%)

**Files ready for Phase 2:**
- [ ] PHASE2-IMPLEMENTATION-PLAN.md exists
- [ ] RCA006-COMPLETE-ROADMAP.md exists
- [ ] Phase 1 implementation stable
- [ ] Git repository clean (no uncommitted changes)

**Context available:**
- [ ] Phase 1 success metrics documented
- [ ] Deferral rate from Phase 1 known
- [ ] User feedback from Phase 1 available
- [ ] Lessons learned from Phase 1 documented

---

## 🎯 **Alternative: If Phase 1 Was Sufficient (STOP)**

**Use this prompt instead:**

```
Phase 1 of RCA-006 has successfully resolved the autonomous deferral problem.

CONTEXT:
- Phase 1 reduced deferral rate from 70% → <10%
- User control increased from 0% → 100%
- Implementation quality improved from 30% → 90%+
- Decision Point 1 result: STOP (Phase 1 sufficient)

TASK:
Document Phase 1 as the complete solution to RCA-006.

ACTIONS NEEDED:
1. Create final implementation report:
   - Document Phase 1 success metrics
   - Note that Phase 2-3 were planned but deemed unnecessary
   - Record decision rationale (why Phase 1 was sufficient)

2. Update framework documentation:
   - Update CLAUDE.md to note Phase 1 enhancement
   - Update .claude/memory/commands-reference.md (note /dev Step 4)
   - Update .claude/memory/skills-reference.md (note enhancement)

3. Archive Phase 2-3 plans:
   - Move PHASE2-IMPLEMENTATION-PLAN.md to archive/
   - Move PHASE3-IMPLEMENTATION-PLAN.md to archive/
   - Note: Available if needed in future

4. Create lessons learned document:
   - What worked well in Phase 1
   - What could be improved
   - Recommendations for future enhancements

FILES TO READ:
@devforgeai/specs/enhancements/PHASE1-IMPLEMENTATION-SUMMARY.md
@devforgeai/specs/enhancements/RCA006-COMPLETE-ROADMAP.md
@CLAUDE.md

DELIVERABLES:
- RCA006-FINAL-REPORT.md (success documentation)
- Updated framework documentation (3 files)
- Archived Phase 2-3 plans
- Lessons learned document

This documents Phase 1 as complete solution and closes RCA-006.
```

---

## 🎯 **Session Context to Include**

### **Essential Context for Phase 2 Session**

**Copy this section into the new session after the prompt:**

```markdown
## Phase 1 Results (From Previous Session)

**Deferral Rate Achieved:** [FILL IN AFTER TESTING]
- Target: <10%
- Actual: ____%
- Status: ✅ Met | ⚠️ Close | ❌ Missed

**User Satisfaction:** [FILL IN AFTER MONITORING]
- Target: ≥80%
- Actual: ____%
- Feedback: [Summary]

**Time Impact:** [FILL IN AFTER MONITORING]
- Target: <40 min per story
- Actual: ___ min average
- Status: ✅ Acceptable | ⚠️ High

**Decision Point 1 Rationale:**
- Phase 1 reduced deferrals by 86% but not sufficient because: [REASON]
- User feedback indicates: [FEEDBACK]
- Proceeding to Phase 2 to achieve: [GOAL]

## What Worked Well in Phase 1
- [List successes]

## What Needs Improvement
- [List issues that Phase 2 should address]

## Phase 2 Specific Goals
Based on Phase 1 experience:
- [Goal 1]
- [Goal 2]
- [Goal 3]
```

---

## 📝 **Quick Copy Templates**

### **Template 1: Phase 2 Implementation (Full Details)**

```
Implement DevForgeAI Phase 2: Structured Technical Specifications

Read complete implementation plan:
@devforgeai/specs/enhancements/PHASE2-IMPLEMENTATION-PLAN.md

Context from Phase 1:
- Deferral rate reduced: 70% → 10%
- User control: 0% → 100%
- Decision Point 1: GO (proceed to Phase 2)

Phase 2 objectives:
1. Create machine-readable YAML format for tech specs
2. Build migration script (v1.0 → v2.0)
3. Implement validation library (validate_tech_spec.py)
4. Update story creation to generate structured format
5. Pilot migration (10 stories) then full migration

Timeline: 4 weeks (30h + 30h + 24h + 30h = 114 hours)

Follow the plan exactly, create todo list, execute sequentially, report progress.
HALT on any ambiguity. No time constraints!

Ready to begin?
```

---

### **Template 2: Phase 2 Quick Start (Minimal)**

```
Implement Phase 2: Structured Tech Specs

Read: @devforgeai/specs/enhancements/PHASE2-IMPLEMENTATION-PLAN.md

Task: Create YAML format for Technical Specifications, build migration script, migrate all stories.

Timeline: 4 weeks, follow plan exactly.

Create todo list and execute sequentially. Report progress. HALT on ambiguity.
```

---

### **Template 3: Phase 1 Closure (If Stopping)**

```
Document Phase 1 completion as final solution to RCA-006.

Read: @devforgeai/specs/enhancements/PHASE1-IMPLEMENTATION-SUMMARY.md

Phase 1 Results:
- Deferral rate: 70% → 10% (-86%)
- Decision: STOP (sufficient)

Tasks:
1. Create RCA006-FINAL-REPORT.md
2. Update framework docs (CLAUDE.md, commands-reference.md, skills-reference.md)
3. Archive Phase 2-3 plans
4. Document lessons learned

Phase 1 solved the problem - Phase 2-3 unnecessary.
```

---

## 🔍 **Verification Before New Session**

### **Pre-Session Checklist**

**Before starting Phase 2 session, verify:**

- [ ] Phase 1 testing complete (all 9 test cases passed)
- [ ] Phase 1 deployed to production
- [ ] Monitoring period complete (10 stories tracked)
- [ ] Metrics collected:
  - [ ] Deferral rate: ____%
  - [ ] Question count: ___ average
  - [ ] Time per story: ___ min average
  - [ ] User satisfaction: ____%
- [ ] Decision Point 1 evaluated
- [ ] GO decision made (proceed to Phase 2)
- [ ] Rationale documented (why Phase 1 insufficient)

**If ANY unchecked:** Complete Phase 1 validation before Phase 2

---

## 📂 **Files to Attach to New Session**

**Essential context files (attach via @file):**

1. `@devforgeai/specs/enhancements/PHASE2-IMPLEMENTATION-PLAN.md`
2. `@devforgeai/specs/enhancements/RCA006-COMPLETE-ROADMAP.md`
3. `@devforgeai/specs/enhancements/PHASE1-IMPLEMENTATION-SUMMARY.md`
4. `@.claude/skills/devforgeai-story-creation/SKILL.md`
5. `@.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`

**Optional (load if needed):**
- `@devforgeai/specs/enhancements/PHASE1-IMPLEMENTATION-GUIDE.md`
- `@.claude/skills/devforgeai-story-creation/references/technical-specification-guide.md`

---

## ✅ **Expected New Session Output**

**After Phase 2 session completes, you should have:**

**Code:**
- [ ] STRUCTURED-FORMAT-SPECIFICATION.md (format definition)
- [ ] validate_tech_spec.py (parser and validator)
- [ ] migrate_story_v1_to_v2.py (migration script)
- [ ] Updated story-template.md (YAML tech spec section)
- [ ] Updated requirements-analyst.md (generate structured format)
- [ ] Updated api-designer.md (structured API specs)

**Documentation:**
- [ ] PHASE2-IMPLEMENTATION-GUIDE.md (user guide)
- [ ] PHASE2-MIGRATION-GUIDE.md (migration procedures)
- [ ] PHASE2-TESTING-CHECKLIST.md (validation tests)

**Migrated Stories:**
- [ ] 10 pilot stories migrated (v1.0 → v2.0)
- [ ] All stories migrated (30+ stories to v2.0)
- [ ] All stories validated (validate_tech_spec.py passes)

**Decision:**
- [ ] Decision Point 2 evaluation complete
- [ ] GO/NO-GO decision for Phase 3 documented

---

## 🎯 **Success Indicators for Phase 2**

**If Phase 2 successful:**
- ✅ Migration success rate: 100%
- ✅ Parsing accuracy: ≥95%
- ✅ Validation passes: 100% of migrated stories
- ✅ /dev works with v2.0 stories
- ✅ Deferral rate: 10% → 3-5% (-50% more)

**Proceed to Phase 3 if:**
- All success indicators met
- User wants automated validation
- Can invest 2 more weeks

**Stop if:**
- Structured format sufficient
- Manual validation acceptable
- Cannot invest 2 more weeks

---

**Copy the prompt above to start Phase 2 implementation in a new session.**
