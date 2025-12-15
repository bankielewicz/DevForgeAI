# Phase 3 Implementation Handoff Prompt

**Purpose:** Start a new Claude Code session to implement Phase 3 (Validation Enforcement)
**Prerequisites:** Phase 2 successfully deployed (all stories migrated to v2.0)
**Timeline:** 2 weeks (Weeks 9-11)
**Use this prompt:** Copy the prompt below into a new Claude Code Terminal session

---

## 🚀 **Prompt for New Session**

```
I need you to implement Phase 3 of the RCA-006 enhancement for the DevForgeAI framework.

CONTEXT:
- Phase 1 successfully deployed (autonomous deferrals eliminated)
- Phase 2 successfully deployed (all stories migrated to structured v2.0 format)
- Decision Point 2 resulted in GO (proceed to Phase 3)
- Now need to implement automated validation enforcement

TASK:
Implement Phase 3 following the complete implementation plan at:
@.devforgeai/specs/enhancements/PHASE3-IMPLEMENTATION-PLAN.md

KEY REQUIREMENTS:
1. Read and follow the Phase 3 implementation plan completely
2. Create implementation-validator subagent (validates code against tech spec)
3. Create implementation-validation-guide.md reference file
4. Add Step 3 to tdd-green-phase.md (invoke validator after backend-architect)
5. Implement validation for 7 component types (Worker, Service, Config, Logging, Repository, API, DataModel)
6. Integrate with Phase 1 decisions (combine test coverage + implementation validation)
7. Test with 5 stories before production deployment
8. Optimize for <5 min validation time and <5% false positive rate

IMPORTANT CONTEXT FILES TO READ:
@.devforgeai/specs/enhancements/PHASE3-IMPLEMENTATION-PLAN.md
@.devforgeai/specs/enhancements/RCA006-COMPLETE-ROADMAP.md
@.devforgeai/specs/enhancements/PHASE2-IMPLEMENTATION-PLAN.md (understand structured format)
@.devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md (tech spec schema)
@.claude/skills/devforgeai-development/references/tdd-green-phase.md
@.claude/agents/backend-architect.md

EXECUTION APPROACH:
1. Create comprehensive todo list for all Phase 3 work
2. Execute each task sequentially with progress reports
3. HALT if you encounter any ambiguity or need clarification
4. Create backups before any file modifications
5. Test validation rules extensively (prevent false positives)
6. Optimize performance (target: <5 min validation)

CONSTRAINTS:
- Work with structured v2.0 tech specs only (Phase 2 provides foundation)
- Prevent false positives (flexible matching, user override option)
- Integrate with Phase 1 Step 4 (don't duplicate validation)
- Follow lean orchestration (validator is subagent, not inline logic)
- Use native tools (Read, Grep, Glob for validation)
- Maintain backward compatibility (v1.0 stories skip validation)

TIMELINE:
Week 6 (now): Subagent Creation & Integration (5 days, ~32 hours)
Week 7: Testing & Deployment (5 days, ~26 hours)

SUCCESS CRITERIA:
- [ ] implementation-validator subagent created (~400 lines)
- [ ] implementation-validation-guide.md reference created (~300 lines)
- [ ] Step 3 added to tdd-green-phase.md (~250 lines)
- [ ] Validation rules cover all 7 component types
- [ ] False positive rate <5%
- [ ] Performance <5 min per validation
- [ ] Integration with Phase 1 validated
- [ ] Testing complete (12 test cases passed)
- [ ] Production deployment successful

DELIVERABLES:
By end of Phase 3:
- 2 new files (~700 lines)
- 3 modified files (~430 lines)
- 2 documentation files (~900 lines)
- Complete testing results
- Decision Point 3: Deploy or iterate

START BY:
1. Reading PHASE3-IMPLEMENTATION-PLAN.md completely
2. Reading STRUCTURED-FORMAT-SPECIFICATION.md (understand YAML schema)
3. Creating detailed todo list (15-20 tasks)
4. Executing Week 6 Day 1: Subagent Design (6 hours)

CRITICAL:
- Phase 3 depends on Phase 2 (requires structured YAML format)
- If Phase 2 not complete, HALT and complete Phase 2 first
- Validation logic must parse YAML (not freeform text)

REPORT PROGRESS:
- After completing each major section
- HALT immediately if you need clarification
- Use TodoWrite to track all tasks

NO TIME CONSTRAINTS - Be thorough and comprehensive!

Ready to begin Phase 3 implementation?
```

---

## 📋 **Session Preparation Checklist**

Before starting the new session, ensure:

**Prerequisites validated:**
- [ ] Phase 2 testing complete
- [ ] Phase 2 deployed to production
- [ ] All stories migrated to v2.0 format (100%)
- [ ] Parsing accuracy measured (should be ≥95%)
- [ ] Decision Point 2 evaluated (GO decision made)
- [ ] Deferral rate with Phase 2: ___% (target: 3-5%)

**Files ready for Phase 3:**
- [ ] PHASE3-IMPLEMENTATION-PLAN.md exists
- [ ] STRUCTURED-FORMAT-SPECIFICATION.md exists (from Phase 2)
- [ ] validate_tech_spec.py functional (from Phase 2)
- [ ] All stories have format_version: "2.0"
- [ ] Phase 2 stable in production

**Context available:**
- [ ] Phase 2 success metrics documented
- [ ] Migration lessons learned documented
- [ ] Parsing accuracy statistics available
- [ ] User feedback from Phase 2 collected

---

## 🎯 **Context Summary to Provide**

**For both Phase 2 and Phase 3 sessions, include:**

### **Phase 1 Results**
```
Deferral Rate: 70% → ___% (target <10%)
User Control: 0% → 100%
Question Count: ___ average per story
Time Impact: 20 min → ___ min
User Satisfaction: ___% (target ≥80%)
Decision: GO to Phase 2 because [REASON]
```

### **Phase 2 Results** (For Phase 3 session only)
```
Migration Success: ___% (target 100%)
Parsing Accuracy: ___% (target ≥95%)
Stories Migrated: ___ total
Deferral Rate: ___% (target 3-5%)
Decision: GO to Phase 3 because [REASON]
```

---

## 📖 **Supporting Documentation References**

**All sessions should reference:**

**Master roadmap:**
- `RCA006-COMPLETE-ROADMAP.md` - Full 11-week timeline

**Phase-specific plans:**
- `PHASE2-IMPLEMENTATION-PLAN.md` - Structured templates
- `PHASE3-IMPLEMENTATION-PLAN.md` - Validation enforcement

**Decision framework:**
- `RCA006-EXECUTIVE-SUMMARY.md` - GO/NO-GO criteria

**Quick reference:**
- `RCA006-QUICK-REFERENCE.md` - Navigation guide

---

**Use these prompts to start new sessions for Phase 2 or Phase 3 implementation when ready.**
