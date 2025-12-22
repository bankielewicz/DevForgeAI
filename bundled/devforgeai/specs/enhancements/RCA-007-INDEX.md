# RCA-007 & Batch Story Creation - Documentation Index

**Date:** 2025-11-06
**Total Documents:** 8
**Total Lines:** ~7,850
**Status:** Complete Specification Package

---

## Document Overview

This index provides navigation for the complete RCA-007 fix and batch story creation enhancement specification package.

---

## Reading Paths

### Path 1: Executive Decision Maker (30 minutes)

**Goal:** Understand problem, solution, timeline, costs, and approve/reject

1. **Quick Reference** (5 min) - `RCA-007-QUICK-REFERENCE.md`
   - Problem summary
   - Solution overview
   - Quick answers

2. **Executive Summary** (15 min) - `RCA-007-EXECUTIVE-SUMMARY.md`
   - Complete overview
   - Timeline and costs
   - Decision points
   - Risk assessment

3. **RCA Analysis** (10 min - skim) - `devforgeai/RCA/RCA-007-multi-file-story-creation.md`
   - 5 Whys analysis
   - Root causes (scan only)

**Decision:** Approve/reject implementation

---

### Path 2: Technical Implementer (4 hours)

**Goal:** Understand architecture, implementation details, build the solution

1. **Quick Reference** (5 min) - `RCA-007-QUICK-REFERENCE.md`
   - Navigation guide

2. **RCA Analysis** (20 min) - `devforgeai/RCA/RCA-007-multi-file-story-creation.md`
   - Full 5 Whys
   - Root causes
   - Violations

3. **Fix Implementation Plan** (60 min) - `RCA-007-FIX-IMPLEMENTATION-PLAN.md`
   - 3-phase roadmap
   - Task breakdowns
   - Code examples
   - Success criteria

4. **Batch Enhancement Plan** (60 min) - `BATCH-STORY-CREATION-ENHANCEMENT.md`
   - 6-phase roadmap
   - User experience
   - Feature design
   - Performance targets

5. **Prompt Enhancement Spec** (30 min) - `SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md`
   - 4-section template
   - Per-subagent guides

6. **Contract Specification** (30 min) - `YAML-CONTRACT-SPECIFICATION.md`
   - Contract schema
   - Example contracts
   - Validation functions

**Outcome:** Ready to begin implementation

---

### Path 3: Quality Assurance Engineer (3 hours)

**Goal:** Understand testing strategy, create test cases, validate solution

1. **Quick Reference** (5 min) - `RCA-007-QUICK-REFERENCE.md`
   - Testing quick reference section

2. **Testing Strategy** (90 min) - `RCA-007-TESTING-STRATEGY.md`
   - 87 test cases
   - Unit, integration, regression, performance
   - Test automation scripts
   - Success metrics

3. **Fix Implementation Plan** (30 min) - `RCA-007-FIX-IMPLEMENTATION-PLAN.md`
   - Testing sections per task

4. **Batch Enhancement Plan** (30 min) - `BATCH-STORY-CREATION-ENHANCEMENT.md`
   - Acceptance criteria
   - User experience validation

**Outcome:** Test plan complete, ready to execute tests

---

### Path 4: Framework Architect (2 hours)

**Goal:** Understand architectural implications, approve design

1. **Executive Summary** (15 min) - `RCA-007-EXECUTIVE-SUMMARY.md`
   - Overall architecture

2. **RCA Analysis** (30 min) - `devforgeai/RCA/RCA-007-multi-file-story-creation.md`
   - Architectural trade-offs
   - Design decisions

3. **Contract Specification** (45 min) - `YAML-CONTRACT-SPECIFICATION.md`
   - Contract architecture
   - Skill-subagent integration patterns
   - Framework-wide implications

4. **Prompt Enhancement Spec** (30 min) - `SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md`
   - Subagent design patterns
   - Output constraints

**Outcome:** Architecture review complete, approve/request changes

---

## Document Details

### 1. RCA-007 Root Cause Analysis

**File:** `devforgeai/RCA/RCA-007-multi-file-story-creation.md`
**Lines:** ~350
**Read time:** 20 minutes
**Audience:** All stakeholders

**Contents:**
- Executive summary
- 5 Whys analysis (Why #1 through Why #5)
- Root causes summary (5 causes identified)
- Impact analysis (4 framework violations)
- Recommendations (7 fixes with priority/effort)

**Key takeaways:**
- Requirements-analyst subagent created 6 files (1 main + 5 supporting)
- Root cause: General-purpose subagent optimizes for completeness, not integration
- Severity: HIGH (violates single-file design principle)

---

### 2. RCA-007 Fix Implementation Plan

**File:** `RCA-007-FIX-IMPLEMENTATION-PLAN.md`
**Lines:** ~1,200
**Read time:** 60 minutes
**Audience:** Developers, implementers

**Contents:**
- Phase 1: Immediate fixes (2-4 hours)
  - Task 1.1: Update subagent prompt (30 min)
  - Task 1.2: Add validation checkpoint (1-2 hrs)
  - Task 1.3: Testing (30 min)
- Phase 2: Short-term improvements (5-7 hours)
  - Task 2.1: Create YAML contract (3-4 hrs)
  - Task 2.2: Contract validation logic (1 hr)
  - Task 2.3: File system diff check (2-3 hrs)
- Phase 3: Long-term architecture (10-14 hours)
  - Task 3.1: Create story-requirements-analyst subagent (4-6 hrs)
  - Task 3.2: Update skill (1 hr)
  - Task 3.3: Regression testing (2-3 hrs)

**Key sections:**
- Task-by-task implementation instructions
- Code examples for each change
- Validation procedures
- Testing checkpoints

**Use when:** Building the RCA-007 fix

---

### 3. Batch Story Creation Enhancement

**File:** `BATCH-STORY-CREATION-ENHANCEMENT.md`
**Lines:** ~1,800
**Read time:** 60 minutes
**Audience:** Developers, UX designers

**Contents:**
- Current vs. desired state
- Design constraints (Claude Code Terminal limitations)
- 6-phase implementation:
  - Phase 1: Basic batch mode (4-6 hrs)
  - Phase 2: Metadata inheritance (2-3 hrs)
  - Phase 3: Progress tracking (1-2 hrs)
  - Phase 4: Error handling (2-3 hrs)
  - Phase 5: Dry-run mode (1 hr)
  - Phase 6: Parallel optimization (3-4 hrs)
- User experience examples
- Feature comparison table

**Key sections:**
- Epic detection algorithm
- Multi-select implementation
- Gap-aware story ID calculation
- Batch metadata application matrix

**Use when:** Building the batch creation enhancement

---

### 4. Subagent Prompt Enhancement Spec

**File:** `SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md`
**Lines:** ~1,100
**Read time:** 30 minutes
**Audience:** Developers, prompt engineers

**Contents:**
- Standard 4-section template:
  1. Pre-Flight Briefing
  2. Output Constraints
  3. Prohibited Actions
  4. Output Format Examples
- Implementation guide per subagent (requirements-analyst, api-designer)
- Self-validation checklist
- Rollout strategy (3 phases)
- Monitoring and logging

**Key sections:**
- Complete prompt template (copy-paste ready)
- Per-subagent customization examples
- Validation script (validate_subagent_output.py)

**Use when:** Enhancing subagent prompts (RCA-007 Phase 1)

---

### 5. YAML Contract Specification

**File:** `YAML-CONTRACT-SPECIFICATION.md`
**Lines:** ~1,300
**Read time:** 30 minutes
**Audience:** Developers, framework architects

**Contents:**
- Contract architecture (location, versioning)
- Complete contract schema (template)
- Example contracts:
  - requirements-analyst-contract.yaml (complete)
  - api-designer-contract.yaml (complete)
- Contract validation helper functions (validate_contract.py)
- Integration patterns
- Maintenance procedures

**Key sections:**
- Contract template (YAML schema)
- Validation logic (Python code)
- Error handling configuration
- Monitoring setup

**Use when:** Creating YAML contracts (RCA-007 Phase 2)

---

### 6. Testing Strategy

**File:** `RCA-007-TESTING-STRATEGY.md`
**Lines:** ~1,400
**Read time:** 45 minutes
**Audience:** QA engineers, developers

**Contents:**
- Testing objectives (RCA fix + batch enhancement)
- Test execution environment (setup, teardown)
- Phase 1 tests (27 cases): Unit, integration, regression
- Phase 2 tests (6 cases): Contract, file diff, performance
- Phase 3 tests (12 cases): Skill-specific subagent, regression
- Batch tests (42 cases): Epic detection, multi-select, sequential creation, error handling, dry-run, parallel optimization
- Test automation (test-suite.sh script)
- Test reporting templates

**Key sections:**
- 87 test case specifications (detailed procedures)
- Test automation scripts
- Success metrics per phase
- Continuous testing procedures

**Use when:** Testing each implementation phase

---

### 7. Executive Summary

**File:** `RCA-007-EXECUTIVE-SUMMARY.md`
**Lines:** ~700
**Read time:** 15 minutes
**Audience:** All stakeholders

**Contents:**
- Problem statement (multi-file creation)
- Enhancement request (batch creation)
- Two-part solution (RCA fix + batch enhancement)
- Implementation timeline (6 weeks)
- Key deliverables (9 RCA + 10 batch)
- Expected outcomes (before/after comparison)
- Risk assessment
- Success criteria
- Stakeholder communication

**Key sections:**
- Cost-benefit analysis
- Decision points (3 critical decisions)
- Success declaration criteria
- File index

**Use when:** Presenting to stakeholders, decision-making

---

### 8. Quick Reference Guide

**File:** `RCA-007-QUICK-REFERENCE.md` (this file)
**Lines:** ~450
**Read time:** 10 minutes
**Audience:** All stakeholders

**Contents:**
- TL;DR summary
- Document navigation
- Quick answers (Q&A format)
- Cheat sheets (phase checklists, commands)
- Troubleshooting guide
- Performance benchmarks
- Testing quick reference
- Success criteria summary

**Use when:** First-time reading, quick lookup, navigation

---

## File Tree

```
devforgeai/
├── RCA/
│   └── RCA-007-multi-file-story-creation.md  (350 lines)
│       ├── 5 Whys Analysis
│       ├── Root Causes (5)
│       ├── Impact Analysis
│       └── Recommendations (7 fixes)
│
└── specs/
    └── enhancements/
        ├── RCA-007-INDEX.md  (this file - 450 lines)
        │   └── Document navigation and organization
        │
        ├── RCA-007-QUICK-REFERENCE.md  (450 lines)
        │   ├── TL;DR
        │   ├── Quick answers
        │   ├── Cheat sheets
        │   └── Troubleshooting
        │
        ├── RCA-007-EXECUTIVE-SUMMARY.md  (700 lines)
        │   ├── Problem statement
        │   ├── Solution overview
        │   ├── Timeline (6 weeks)
        │   ├── Deliverables (19 items)
        │   ├── Decision points (3)
        │   └── Success criteria
        │
        ├── RCA-007-FIX-IMPLEMENTATION-PLAN.md  (1,200 lines)
        │   ├── Phase 1: Immediate (2-4 hrs)
        │   │   ├── Task 1.1: Update prompt
        │   │   ├── Task 1.2: Add validation
        │   │   └── Task 1.3: Testing
        │   ├── Phase 2: Short-term (5-7 hrs)
        │   │   ├── Task 2.1: Create contract
        │   │   ├── Task 2.2: Validation logic
        │   │   └── Task 2.3: File diff
        │   └── Phase 3: Long-term (10-14 hrs)
        │       ├── Task 3.1: Create subagent
        │       ├── Task 3.2: Update skill
        │       └── Task 3.3: Regression tests
        │
        ├── BATCH-STORY-CREATION-ENHANCEMENT.md  (1,800 lines)
        │   ├── Current vs. desired state
        │   ├── Design constraints
        │   ├── Phase 1: Basic batch (4-6 hrs)
        │   ├── Phase 2: Metadata (2-3 hrs)
        │   ├── Phase 3: Progress (1-2 hrs)
        │   ├── Phase 4: Errors (2-3 hrs)
        │   ├── Phase 5: Dry-run (1 hr)
        │   ├── Phase 6: Parallel (3-4 hrs)
        │   └── User experience examples
        │
        ├── SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md  (1,100 lines)
        │   ├── Purpose and problem
        │   ├── 4-section template:
        │   │   ├── 1. Pre-Flight Briefing
        │   │   ├── 2. Output Constraints
        │   │   ├── 3. Prohibited Actions
        │   │   └── 4. Output Format Examples
        │   ├── Per-subagent implementation:
        │   │   ├── requirements-analyst
        │   │   └── api-designer
        │   ├── Self-validation checklist
        │   └── Rollout strategy
        │
        ├── YAML-CONTRACT-SPECIFICATION.md  (1,300 lines)
        │   ├── Contract architecture
        │   ├── Complete schema template
        │   ├── Example contracts:
        │   │   ├── requirements-analyst-contract.yaml (complete)
        │   │   └── api-designer-contract.yaml (complete)
        │   ├── Validation helper (validate_contract.py)
        │   ├── Integration patterns
        │   └── Maintenance procedures
        │
        └── RCA-007-TESTING-STRATEGY.md  (1,400 lines)
            ├── Testing objectives (7 RCA + 10 batch)
            ├── Test environment (setup, teardown)
            ├── Phase 1 tests (27 cases)
            ├── Phase 2 tests (6 cases)
            ├── Phase 3 tests (12 cases)
            ├── Batch tests (42 cases)
            ├── Test automation (test-suite.sh)
            └── Success metrics
```

**Total:** 8 documents, ~7,850 lines

---

## Document Relationships

### Dependency Graph

```
RCA-007-INDEX.md  (You are here)
    ↓
    ├─→ RCA-007-QUICK-REFERENCE.md  (Start here - 5 min)
    │       ↓
    │       └─→ RCA-007-EXECUTIVE-SUMMARY.md  (Overview - 15 min)
    │               ↓
    │               └─→ RCA-007-multi-file-story-creation.md  (Root cause - 20 min)
    │
    ├─→ RCA-007-FIX-IMPLEMENTATION-PLAN.md  (Implementation - 60 min)
    │       ├─→ SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md  (Phase 1 detail)
    │       └─→ YAML-CONTRACT-SPECIFICATION.md  (Phase 2 detail)
    │
    ├─→ BATCH-STORY-CREATION-ENHANCEMENT.md  (Enhancement - 60 min)
    │
    └─→ RCA-007-TESTING-STRATEGY.md  (Testing - 90 min)
```

**Reading sequence:** Top to bottom, left to right

---

## By Implementation Phase

### Week 1: RCA-007 Phase 1 (Immediate Fix)

**Read:**
1. Quick Reference → Executive Summary → RCA Analysis (45 min)
2. Fix Implementation Plan → Phase 1 section (30 min)
3. Prompt Enhancement Spec → Section 1-4 (30 min)
4. Testing Strategy → Phase 1 tests (30 min)

**Total prep time:** 2.25 hours
**Implementation time:** 2-4 hours
**Testing time:** 1 hour

---

### Week 2: RCA-007 Phase 2 (Contract Validation)

**Read:**
1. Fix Implementation Plan → Phase 2 section (30 min)
2. Contract Specification → Complete (30 min)
3. Testing Strategy → Phase 2 tests (15 min)

**Total prep time:** 1.25 hours
**Implementation time:** 5-7 hours
**Testing time:** 2 hours

---

### Week 3-4: RCA-007 Phase 3 (Skill-Specific Subagent)

**Read:**
1. Fix Implementation Plan → Phase 3 section (30 min)
2. Prompt Enhancement Spec → Skill-specific section (15 min)
3. Testing Strategy → Phase 3 tests (30 min)

**Total prep time:** 1.25 hours
**Implementation time:** 10-14 hours
**Testing time:** 3 hours

---

### Week 4-6: Batch Enhancement (Phases 1-6)

**Read:**
1. Batch Enhancement Plan → Complete (60 min)
2. Testing Strategy → Batch tests section (45 min)

**Total prep time:** 1.75 hours
**Implementation time:** 13-19 hours
**Testing time:** 6 hours

---

## By Role

### Product Owner / Decision Maker

**Must read:**
- ✅ Quick Reference (TL;DR section)
- ✅ Executive Summary (Problem, Solution, Timeline, Costs)

**Optional:**
- RCA Analysis (understand root causes)

**Total time:** 20-40 minutes

**Decision deliverables:**
- [ ] Approve/reject RCA-007 fix
- [ ] Approve/reject batch enhancement
- [ ] Approve timeline (6 weeks)
- [ ] Approve budget (38-54 hours)

---

### Technical Lead / Architect

**Must read:**
- ✅ Quick Reference
- ✅ Executive Summary
- ✅ RCA Analysis (full)
- ✅ Contract Specification

**Optional:**
- Fix Implementation Plan (if reviewing architecture)
- Batch Enhancement Plan (if reviewing design)

**Total time:** 1.5-2 hours

**Decision deliverables:**
- [ ] Approve architectural approach (contracts, skill-specific subagent)
- [ ] Approve contract schema
- [ ] Approve batch mode design
- [ ] Sign off on non-aspirational validation

---

### Developer / Implementer

**Must read:**
- ✅ Quick Reference (navigation)
- ✅ Fix Implementation Plan (if doing RCA fix)
- ✅ Batch Enhancement Plan (if doing batch feature)
- ✅ Prompt Enhancement Spec
- ✅ Contract Specification

**Optional:**
- Executive Summary (context)
- RCA Analysis (understanding why)

**Total time:** 3-4 hours

**Implementation deliverables:**
- [ ] Code changes per plan
- [ ] New files created
- [ ] Documentation updated
- [ ] Tests written and passing

---

### QA Engineer / Tester

**Must read:**
- ✅ Quick Reference (testing section)
- ✅ Testing Strategy (complete)
- ✅ Fix Implementation Plan (success criteria per task)
- ✅ Batch Enhancement Plan (acceptance criteria)

**Optional:**
- Executive Summary (context)

**Total time:** 3-4 hours

**Testing deliverables:**
- [ ] Test plan created (87 test cases)
- [ ] Test automation scripts
- [ ] Test results documented
- [ ] Success metrics measured

---

## Key Concepts

### RCA-007 Fix Concepts

**1. Output Constraints**
- Subagents return CONTENT (markdown text), not FILES
- Parent skill assembles content into template
- No file creation by subagents

**2. Validation Checkpoint**
- After subagent invocation, validate output format
- Check for file creation indicators (regex patterns)
- Re-invoke if violations detected

**3. YAML Contracts**
- Formal specification of input/output format
- Constraints enforce framework rules
- Validation rules catch violations
- Error handling defines recovery logic

**4. Skill-Specific Subagent**
- Tightly coupled to parent skill workflow
- Understands template assembly pattern
- Returns content only (by design)

---

### Batch Enhancement Concepts

**1. Epic Detection**
- Parse command argument: `epic-001` pattern
- Read epic file, extract features
- Present multi-select question

**2. Multi-Select Feature Picker**
- AskUserQuestion with `multiSelect: true`
- User selects 1-N features
- Create story for each selected

**3. Batch Metadata**
- Ask sprint/priority once for all stories
- Option to "Inherit from epic"
- Option to "Ask per story" for custom metadata

**4. Sequential Creation Loop**
- For each selected feature:
  - Calculate next story ID (gap-aware)
  - Set context markers
  - Invoke skill in batch mode
  - Update progress (TodoWrite)

**5. Gap-Aware Story ID**
- Detect gaps in existing story IDs
- Fill gaps before incrementing
- Notify user of gap filling

**6. Pseudo-Parallel Optimization**
- Multiple Skill invocations in single message
- Claude processes pseudo-concurrently
- 40-60% speedup vs. pure sequential

---

## Implementation Priorities

### Must Do (Blocking Release)

**RCA-007 Fix:**
- [ ] Phase 1: Prompt constraints + validation (Week 1)
- [ ] Test: Zero extra files (100% compliance)

**Batch Enhancement:**
- [ ] Phase 1: Epic detection + multi-select (Week 4)
- [ ] Phase 2: Batch metadata (Week 4)
- [ ] Test: Batch creation works (95%+ success rate)

**Total MVP:** 4 weeks, ~18-24 hours

---

### Should Do (Recommended)

**RCA-007 Fix:**
- [ ] Phase 2: YAML contracts (Week 2)
- [ ] Test: Contract enforcement (100% detection)

**Batch Enhancement:**
- [ ] Phase 3: Progress tracking (Week 5)
- [ ] Phase 4: Error handling (Week 5)
- [ ] Test: Partial success handled (100% recovery)

**Total with recommended:** 5 weeks, ~30-40 hours

---

### Nice to Have (Optional)

**RCA-007 Fix:**
- [ ] Phase 3: Skill-specific subagent (Week 3-4)

**Batch Enhancement:**
- [ ] Phase 5: Dry-run mode (Week 5)
- [ ] Phase 6: Parallel optimization (Week 6)

**Total complete solution:** 6 weeks, ~38-54 hours

---

## Metrics Dashboard

### RCA-007 Fix Metrics

**Track weekly:**
```bash
# Extra files created (target: 0)
extra_count=$(ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null | wc -l)
echo "Extra files: $extra_count (target: 0)"

# Violations detected (target: 0 after fix deployed)
violation_count=$(grep -c "VIOLATION DETECTED" devforgeai/logs/rca-007-violations.log 2>/dev/null || echo 0)
echo "Violations: $violation_count (target: 0)"

# Recovery success rate (target: 90%+)
success=$(grep -c "Recovery Result: SUCCESS" devforgeai/logs/rca-007-violations.log 2>/dev/null || echo 0)
total=$(grep -c "Recovery Action" devforgeai/logs/rca-007-violations.log 2>/dev/null || echo 1)
rate=$((success * 100 / total))
echo "Recovery rate: ${rate}% (target: 90%+)"
```

---

### Batch Enhancement Metrics

**Track weekly:**
```bash
# Batch creations executed
batch_count=$(grep -c "/create-story epic-" .claude/logs/command-history.log 2>/dev/null || echo 0)
echo "Batch creations: $batch_count"

# Average stories per batch
# (Manual calculation from completion summaries)

# Average execution time (target: 6-8 min for 7 stories with parallel)
# (Measure with: time /create-story epic-001)

# Question reduction (target: 86-94%)
# Questions before: 28 (for 7 stories)
# Questions after: 4 (batch mode)
# Reduction: 86%
```

---

## Common Commands

### Testing Commands

```bash
# Run all RCA-007 tests
bash devforgeai/tests/rca-007-test-suite.sh all

# Run specific phase tests
bash devforgeai/tests/rca-007-test-suite.sh phase1

# Validate contract YAML
python -c "import yaml; yaml.safe_load(open('.claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml'))"

# Validate subagent output
python .claude/skills/devforgeai-story-creation/scripts/validate_contract.py \
    /tmp/subagent-output.txt \
    .claude/skills/devforgeai-story-creation/contracts/requirements-analyst-contract.yaml

# Check for extra files
ls devforgeai/specs/Stories/STORY-*-SUMMARY.md 2>/dev/null | wc -l  # Should be 0
```

---

### Batch Creation Commands

```bash
# Single story (normal mode)
/create-story User profile management with avatar upload

# Batch from epic (all features)
/create-story epic-001

# Batch with dry-run preview
/create-story epic-002 --dry-run

# Check batch results
ls devforgeai/specs/Stories/STORY-*.story.md | tail -7  # Last 7 stories created

# Check epic updated
grep "STORY-0" devforgeai/specs/Epics/EPIC-001.epic.md
```

---

### Monitoring Commands

```bash
# Check violation log
tail -50 devforgeai/logs/rca-007-violations.log

# Count violations by type
grep "Violation Type:" devforgeai/logs/rca-007-violations.log | sort | uniq -c

# Check test results
ls devforgeai/tests/results/*.md | tail -1  # Latest test report
cat $(ls -t devforgeai/tests/results/*.md | head -1)  # Display latest
```

---

## Glossary

**RCA:** Root Cause Analysis (5 Whys methodology)

**Contract:** YAML file specifying formal input/output between skill and subagent

**Content-only output:** Subagent returns markdown text (not file artifacts)

**Batch mode:** Creating multiple stories from epic in single command execution

**Gap-aware numbering:** Detecting missing story IDs (e.g., STORY-004 missing) and filling gaps

**Pseudo-parallel:** Multiple Skill calls in single message (40-60% speedup, not true parallelism)

**Dry-run:** Preview mode that shows what will be created without actually creating files

**Multi-select:** AskUserQuestion feature allowing selection of multiple options

**Validation checkpoint:** Step in workflow that validates subagent output before proceeding

**Recovery logic:** Automatic re-invocation with stricter constraints when violations detected

---

## Quick Links

**Within DevForgeAI project:**

- Skills: `.claude/skills/devforgeai-story-creation/`
- Subagents: `.claude/agents/`
- Commands: `.claude/commands/create-story.md`
- Contracts: `.claude/skills/devforgeai-story-creation/contracts/`
- Tests: `devforgeai/tests/`
- Logs: `devforgeai/logs/`

**Documentation:**
- Framework: `CLAUDE.md`
- Skills Reference: `.claude/memory/skills-reference.md`
- Commands Reference: `.claude/memory/commands-reference.md`
- Subagents Reference: `.claude/memory/subagents-reference.md`

---

## Support Resources

### If You Get Stuck

**RCA-007 Fix issues:**
1. Check `SUBAGENT-PROMPT-ENHANCEMENT-SPEC.md` for prompt template
2. Check `YAML-CONTRACT-SPECIFICATION.md` for contract schema
3. Check `RCA-007-FIX-IMPLEMENTATION-PLAN.md` for task details
4. Review original conversation: `tmp/output2.md`

**Batch enhancement issues:**
1. Check `BATCH-STORY-CREATION-ENHANCEMENT.md` for design details
2. Check `RCA-007-TESTING-STRATEGY.md` for test procedures
3. Check epic feature extraction algorithm in batch enhancement doc

**Testing issues:**
1. Check `RCA-007-TESTING-STRATEGY.md` for test procedures
2. Run specific test case: `bash test-suite.sh test_X_Y`
3. Review test fixtures in `devforgeai/tests/fixtures/`

---

## What to Read When

### Before Starting Implementation

**Day 1:** Quick Reference + Executive Summary (20 min)
- Understand problem and solution
- Review timeline and effort

**Day 2:** RCA Analysis + Fix Plan (Phase 1) (60 min)
- Understand root causes
- Review Phase 1 tasks

**Day 3:** Prompt Enhancement Spec (30 min)
- Study 4-section template
- Review examples

**Ready to implement Phase 1 on Day 4**

---

### Before Each Implementation Phase

**Phase 1 (Week 1):**
- Re-read Fix Plan Phase 1 section (15 min)
- Review prompt template (10 min)
- Set up test environment (30 min)

**Phase 2 (Week 2):**
- Read Contract Specification (30 min)
- Review validation logic examples (15 min)
- Study contract schema (15 min)

**Phase 3 (Week 3-4):**
- Re-read skill-specific subagent section (15 min)
- Review regression test cases (15 min)

**Batch Phases 1-6 (Week 4-6):**
- Read Batch Enhancement Plan (60 min)
- Review user experience examples (15 min)
- Study epic detection algorithm (15 min)

---

### During Testing

**Always have open:**
- Testing Strategy document (test case procedures)
- Quick Reference (troubleshooting section)
- Test automation script (test-suite.sh)

**Reference as needed:**
- Implementation plans (success criteria per task)
- Contract specification (validation rules)

---

## Print-Friendly Versions

### One-Page Summary (Print This)

**Problem:** Multi-file creation violates single-file design

**Solution:**
- Fix 1: Enhance subagent prompt (no file creation)
- Fix 2: Add validation checkpoint (detect violations)
- Fix 3: Create YAML contracts (formal spec)
- Fix 4: Create skill-specific subagent (tight coupling)

**Enhancement:** Batch story creation from epics
- Epic detection (`epic-001` pattern)
- Multi-select features
- Batch metadata (ask once)
- Sequential creation with progress

**Timeline:** 6 weeks (3 fix + 3 enhancement)

**Effort:** 38-54 hours total

**Success:**
- Zero extra files (RCA fix)
- 86% fewer questions (batch enhancement)
- 43-57% faster execution (batch with parallel)

---

### Quick Implementation Checklist (Print This)

**Week 1: RCA Phase 1**
- [ ] Update requirements-analysis.md prompt
- [ ] Add validation Step 2.2
- [ ] Test single story creation
- [ ] Verify: 0 extra files

**Week 2: RCA Phase 2**
- [ ] Create contract YAML
- [ ] Add contract validation Step 2.3
- [ ] Add file diff Step 2.2.5
- [ ] Test contract enforcement

**Week 3-4: RCA Phase 3**
- [ ] Create story-requirements-analyst.md
- [ ] Update skill reference
- [ ] Regression testing
- [ ] Deploy

**Week 4: Batch Phases 1-2**
- [ ] Add epic detection
- [ ] Add batch workflow
- [ ] Add batch metadata
- [ ] Test epic-001 batch

**Week 5: Batch Phases 3-5**
- [ ] Add TodoWrite progress
- [ ] Add error handling
- [ ] Add dry-run mode
- [ ] Test all features

**Week 6: Batch Phase 6**
- [ ] Add parallel optimization
- [ ] Measure speedup
- [ ] Final testing
- [ ] Deploy

---

## Version Control

### Git Commits

**RCA-007 Fix:**
```bash
# Phase 1
git add .claude/skills/devforgeai-story-creation/references/requirements-analysis.md
git commit -m "fix(story-creation): Add subagent output constraints (RCA-007 Phase 1)

- Enhanced requirements-analyst prompt with no-file-creation constraints
- Added validation checkpoint (Step 2.2) to detect file creation
- Implements RCA-007 immediate fix

Related: RCA-007
"

# Phase 2
git add .claude/skills/devforgeai-story-creation/contracts/
git add .claude/skills/devforgeai-story-creation/scripts/validate_contract.py
git commit -m "feat(story-creation): Add YAML contract validation (RCA-007 Phase 2)

- Created requirements-analyst-contract.yaml
- Added contract validation logic (Step 2.3)
- Added file system diff check (Step 2.2.5)

Related: RCA-007
"

# Phase 3
git add .claude/agents/story-requirements-analyst.md
git commit -m "feat(subagents): Add story-requirements-analyst (RCA-007 Phase 3)

- Created skill-specific subagent for story creation
- Enforces content-only output (no file creation)
- Updated skill to use new subagent

Related: RCA-007
"
```

**Batch Enhancement:**
```bash
# Phase 1-2
git add .claude/commands/create-story.md
git add .claude/skills/devforgeai-story-creation/SKILL.md
git commit -m "feat(story-creation): Add epic batch mode (Enhancement Phase 1-2)

- Added epic detection and feature extraction
- Implemented multi-select feature picker
- Added batch metadata collection
- Enables /create-story epic-001 for batch creation

Related: RCA-007 Enhancement
"
```

---

## Stakeholder Sign-Off

### Approval Checklist

**Before starting implementation:**

- [ ] **Product Owner:** Approves problem statement and solution approach
- [ ] **Technical Lead:** Approves architectural design and contract schema
- [ ] **QA Lead:** Approves testing strategy (87 test cases adequate)
- [ ] **Engineering Manager:** Approves timeline (6 weeks) and effort (38-54 hours)

**After each phase:**

- [ ] **Phase 1:** Single story creates only 1 file (demonstrated)
- [ ] **Phase 2:** Contract validation works (demonstrated)
- [ ] **Phase 3:** Skill-specific subagent quality matches general-purpose (validated)
- [ ] **Batch Phase 1-2:** Epic batch creation works (demonstrated)
- [ ] **Batch Phase 3-5:** Progress, errors, dry-run work (demonstrated)
- [ ] **Batch Phase 6:** Parallel speedup measured (40-60% confirmed or documented actual)

---

## Final Checklist

### Before Declaring Complete

**RCA-007 Fix:**
- [ ] All 3 phases implemented
- [ ] 42 test cases pass (100%)
- [ ] Zero extra files in 100 consecutive story creations
- [ ] Zero violations logged for 1 week
- [ ] Documentation updated (4 files)
- [ ] Stakeholders sign off

**Batch Enhancement:**
- [ ] All 6 phases implemented (or MVP: Phases 1-4)
- [ ] 45 test cases pass (95%+)
- [ ] 10 successful batch creations demonstrated
- [ ] Performance targets met (6-10 min for 7 stories)
- [ ] Documentation updated (3 files)
- [ ] User feedback positive

**Combined:**
- [ ] No regressions (single story mode works)
- [ ] Framework integrity maintained
- [ ] All specifications archived
- [ ] Lessons learned documented

---

**Index Complete**

**Total Specification Package:**
- 8 documents
- ~7,850 lines
- Comprehensive coverage (problem → solution → implementation → testing)
- Ready for immediate implementation

**Recommended First Read:** `RCA-007-QUICK-REFERENCE.md` (this file) → `RCA-007-EXECUTIVE-SUMMARY.md` → Choose implementation path

**Status:** ✅ Complete Specification - Ready to Begin Week 1
