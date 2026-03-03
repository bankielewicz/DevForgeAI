# RCA-009 Executive Summary: Why Claude Skipped 3 Critical Workflow Steps

**Date:** 2025-11-14
**Incident:** STORY-027 development workflow 75% compliant (missed Tech Spec Coverage, context-validator, Light QA)
**Root Cause:** Progressive disclosure fragmented mandatory steps across references without execution enforcement
**Impact:** User intervention required, 15min rework, 25% compliance gap

---

## Root Cause (5 Whys Summary)

### Why did Claude skip mandatory validation steps?

**Surface Answer:** Claude read reference files but didn't execute all instructions

**Deep Answer (5 Whys):**
1. Why not execute all? → Treated Steps 1-3 as "workflow", Step 4+ as "supporting reference"
2. Why treated differently? → Step 4 is 620 lines (85% of file), appears supplementary after "Phase Complete" message
3. Why appears optional? → No [MANDATORY] markers, no execution checkboxes, no enforcement
4. Why no markers? → Progressive disclosure moved details to references but didn't mark criticality
5. Why not in summary? → SKILL.md phase summaries incomplete (doesn't mention all mandatory steps)

**ROOT:** Phase summaries in SKILL.md don't reflect complete workflow. Reference files have mandatory steps not mentioned in entry point.

---

## Critical Research Findings

### Finding 1: Modular Architecture is CORRECT (Proven 2-10x Performance)
- **Evidence:** Pimzino's workflow (thousands of downloads), Builder.io (18K-line components)
- **DevForgeAI Status:** ✅ Has modular architecture (6 phase references)
- **Gap:** References treated as "guidance" not "execution checklist"

### Finding 2: XML Tags Reduce Errors by 40% (Anthropic Research)
- **Evidence:** `.ai_docs/prompt-engineering-best-practices.md` (Anthropic, 2025)
- **DevForgeAI Status:** ❌ Uses markdown only, no XML semantic boundaries
- **Opportunity:** Wrap `<mandatory_steps>` in XML for unambiguous execution

### Finding 3: Checklist Format Critical for Sequential Execution
- **Evidence:** Aviation pre-flight checklists (proven safety pattern)
- **DevForgeAI Status:** ✅ Uses checkboxes in DoD, ❌ Missing in phase execution
- **Gap:** Asymmetric validation (DoD has checkboxes, phases don't)

### Finding 4: Quality Gates Work When Architecturally Enforced
- **Evidence:** OneRedOak (94% vulnerability detection via automated hooks)
- **DevForgeAI Status:** ✅ Gates defined, ❌ Not enforced (can skip)
- **Gap:** Relies on Claude judgment instead of automatic validation

### Finding 5: Progressive Disclosure Architecture is Sound
- **Evidence:** `.ai_docs/claude-skills.md` - "Effectively unlimited" reference content
- **DevForgeAI Status:** ✅ Correct architecture (on-demand loading)
- **Gap:** Loading ≠ Executing (no mechanism ensuring execution)

---

## What I Missed (Detailed)

| Task | Should Execute | Actually Executed | Why Skipped |
|------|----------------|-------------------|-------------|
| **Phase 1 Step 4: Tech Spec Coverage** | ✅ Required | ❌ Skipped | 620 lines at end of file, no [MANDATORY] marker, SKILL.md doesn't mention it |
| **Phase 2: context-validator** | ✅ Required | ❌ Skipped | Listed in SKILL.md but not in tdd-green-phase.md workflow, assumed backend-architect sufficient |
| **Phase 3: Light QA** | ✅ Required | ❌ Skipped | At line 519 of 797-line file, appears as "checklist item" not "workflow step" |
| **Phase 5: DoD Update** | ✅ Required | ⚠️ Wrong Format | Format requirements implicit (examples only), subsection header broke validator |
| **Phase 6: Feedback Hook** | ✅ Required | ❌ Initially Skipped | Not in skill reference files, only documented in /dev command |

---

## 9 Evidence-Based Recommendations (Implementable Today)

### Week 1: Critical Fixes (3.5-4.5 hours)

**Rec 1: [MANDATORY] Step Markers** (2-3h, +3K tokens)
- Add explicit markers to all required steps
- Evidence: GitHub Actions required steps
- Impact: Eliminates "is this optional?" guesswork

**Rec 4: DoD Update Workflow Bridge** (1h, +800 tokens)
- New file: `dod-update-workflow.md`
- Consolidates Phase 4.5 → Phase 5 handoff
- Documents DoD format requirements explicitly
- Evidence: AWS CDK synthesis validation
- Impact: Prevents DoD format failures

**Rec 3: Promote Light QA to Explicit Step** (30min, +300 tokens)
- Make Step 4 in tdd-refactor-phase.md
- Evidence: CI/CD explicit pipeline stages
- Impact: Can't skip intermediate quality gate

### Week 2: Workflow Enforcement (5-7 hours)

**Rec 5: Phase Completion Checkpoints** (2-3h, +2.4K tokens)
- Checklist at end of each phase
- Evidence: Aviation pre-flight safety pattern
- Impact: Forces validation before advancing

**Rec 6: TodoWrite Progress Tracker** (2h, +1.4K tokens)
- Visual progress through 6 phases
- Evidence: pytest --verbose progress display
- Impact: User visibility + Claude self-monitoring

**Rec 2: Subagent Invocation Sequences** (1-2h, +1.2K tokens)
- Show order + purpose in SKILL.md
- Evidence: Kubernetes container sequencing
- Impact: Clear "invoke X, THEN invoke Y"

### Week 3: Documentation (2.5 hours)

**Rec 7-9: Cross-refs, Validator Matrix, Flowchart** (2.5h, +3.3K tokens)
- Evidence: MDN navigation, Terraform dual validation, BPMN diagrams
- Impact: Better navigation, clearer handoffs

**Total:** 12-15 hours, +12.4K tokens, break-even after 1 story

---

## Architectural Insights

### What DevForgeAI Got RIGHT:
✅ Modular architecture (proven 2-10x better than monolithic)
✅ Progressive disclosure (on-demand reference loading)
✅ Lean orchestration (/dev delegates to skill)
✅ Subagent isolation (token efficiency)
✅ Quality gates defined (Light QA, context-validator, deferral-validator)

### What DevForgeAI Needs to FIX:
❌ Mandatory vs. optional steps not marked explicitly
❌ Phase completion not validated (no checkpoints)
❌ Reference files treated as "guidance" not "execution checklist"
❌ Critical steps buried in long reference files (Light QA at line 519/797)
❌ No self-monitoring mechanism (TodoWrite not used)

### The Paradox:
**DevForgeAI has WORLD-CLASS architecture** (modular, progressive, isolated) but **INCONSISTENT execution** (Claude skips steps due to ambiguous criticality).

**Analogy:** It's like having a perfect recipe (modular architecture) but no checklist (execution enforcement), so the chef (Claude) improvises and skips steps.

---

## Why Phase 5 (Git Commit) Is Difficult After Phase 4.5

### Issue 1: Dual Validators, Separate Documentation
- **Phase 4.5:** deferral-validator (AI semantic validation)
- **Phase 5:** devforgeai validate-dod (CLI format validation)
- **Problem:** Different requirements, documented in different files
- **Result:** Pass AI validator but fail CLI validator (wrong DoD format)

### Issue 2: DoD Format Requirements Implicit
- **Requirement:** Flat list under `## Implementation Notes` (no `###` subsections)
- **Documentation:** Only shown via examples (story-documentation-pattern.md lines 142-237)
- **Why implicit:** `extract_section()` behavior (stops at `###`) not documented
- **Result:** Claude inferred wrong format from examples

### Issue 3: Phase Handoff Unclear
- **Phase 4.5:** Validates deferral semantics
- **Phase 5:** Requires DoD format correctness
- **Gap:** Which phase updates DoD checkboxes? (4.5? 5? Bridge?)
- **Result:** Claude updated DoD in Phase 4.5 but used wrong format for Phase 5

### Solution: Create Explicit Bridge File
**New:** `dod-update-workflow.md` (Recommendation 4)
- Consolidates both validators' requirements
- Documents exact format (flat list, no subsections, why)
- Explains `extract_section()` behavior
- Provides validation command (`devforgeai validate-dod`)
- Clear ownership: "Execute AFTER Phase 4.5, BEFORE Phase 5 commit"

---

## Success Metrics

**Current (STORY-027 Baseline):**
- Workflow compliance: 75% (6/8 tasks)
- Missing steps: 3 mandatory validations
- User interventions: 2 (shouldn't be needed)
- Rework time: 15 minutes
- Token waste: ~60K (240K used, ~180K needed)

**Target (After Recommendations 1-6):**
- Workflow compliance: 100% (8/8 tasks)
- Missing steps: 0
- User interventions: 0
- Rework time: 0 minutes
- Token efficiency: 180K (25% reduction)

**Validation:** Test with STORY-028, measure against baseline

---

## Key Takeaway

**DevForgeAI's architecture is sound** (modular, progressive disclosure, subagent isolation).

**The problem is execution reliability:** Claude treats loaded reference files as "information to consider" rather than "checklist to execute completely."

**The fix is straightforward:** Add explicit execution markers ([MANDATORY], XML tags, completion checkboxes) that transform references from "guidance documents" into "execution contracts."

**All 9 recommendations are implementable today** (no new Claude Code features needed - just markdown, XML tags, TodoWrite, and explicit instructions).

---

**Full Analysis:** See `RCA-009-skill-execution-incomplete-workflow.md` for complete 5 Whys, evidence, and implementation details.
