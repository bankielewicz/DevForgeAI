# RCA-016 REC-2 Implementation Plan: Enhanced Phase Completion Checklists

**Created:** 2025-12-01
**Purpose:** Executable plan for enhancing phase completion checklists to match actual workflow steps
**Related RCA:** RCA-016-qa-skill-phase-skipping-during-deep-validation.md
**Recommendation:** REC-2 (HIGH) - Add Phase Completion Checklists
**Status:** READY FOR EXECUTION
**Prerequisite:** REC-1 (CRITICAL) - COMPLETE (Commit 3654474)

---

## Executive Summary

This document provides a complete, context-rich implementation plan for REC-2 that can be executed in a fresh terminal session without requiring prior context.

**Problem Solved:** Current checklists are minimal summaries (5-7 generic items) that don't match actual workflow steps in reference files
**Solution:** Enhance checklists to be comprehensive step-by-step verifications that match the exact steps documented in reference workflow files

---

## Current State Analysis (As of 2025-12-01)

### What REC-1 Implemented (Commit 3654474)

The following already exists in `.claude/skills/devforgeai-qa/SKILL.md`:

1. **⚠️ CHECKPOINT markers** at Phases 2, 3, 4, 6, 7
2. **Step X.0: Load Workflow Reference (REQUIRED)** at each phase
3. **Basic completion checklists** (5-7 items each)
4. **Clarified progressive disclosure language** (lines 77-89)

### Gap: What REC-2 Adds

| Aspect | Current (REC-1) | Enhanced (REC-2) |
|--------|-----------------|------------------|
| **Phase 1** | No checkpoint/checklist | Add checkpoint + 9-item checklist |
| **Phase 5** | No checkpoint/checklist | Add checkpoint + 8-item checklist |
| **Phase 2** | 5 generic items | 12 items matching 6 workflow steps |
| **Phase 3** | 5 generic items | 14 items matching 7 workflow steps |
| **Phase 4** | 5 generic items | 11 items matching 5 workflow steps |
| **Phase 6** | 4 generic items | 9 items matching 5 workflow steps |
| **Phase 7** | 5 generic items | 10 items matching 6 workflow steps |
| **Display Templates** | None | Added to all 7 phases |

**Total Enhancement:** ~35 items → ~73 items (2x increase in verification granularity)

---

## Reference Workflow Step Counts (Evidence Base)

These are the actual steps in each reference workflow file. Checklists must match these exactly.

### Phase 1: coverage-analysis-workflow.md (7 Steps)
**File:** `.claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 1 | Load Coverage Thresholds | Read coverage-thresholds.md, use defaults if missing |
| Step 2 | Generate Coverage Reports | Execute language-specific command (dotnet/pytest/npm) |
| Step 3 | Classify Files by Layer | Read source-tree.md, classify Business/Application/Infrastructure |
| Step 4 | Calculate Coverage by Layer | Parse coverage data, calculate averages per layer |
| Step 5 | Validate Against Thresholds | Check 95%/85%/80% thresholds, record violations |
| Step 6 | Identify Coverage Gaps | Find uncovered lines, suggest tests |
| Step 7 | Analyze Test Quality | Check assertion count, over-mocking, test pyramid |

### Phase 2: anti-pattern-detection-workflow.md (6 Steps)
**File:** `.claude/skills/devforgeai-qa/references/anti-pattern-detection-workflow.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 1 | Load ALL 6 Context Files | Read tech-stack, source-tree, dependencies, coding-standards, architecture-constraints, anti-patterns |
| Step 2 | Invoke anti-pattern-scanner | Task() with complete context, scan 6 categories |
| Step 3 | Parse JSON Response | Extract violations by severity |
| Step 4 | Update blocks_qa State | OR logic with Phase 1 result |
| Step 5 | Display Violations Summary | Format by severity (CRITICAL/HIGH/MEDIUM/LOW) |
| Step 6 | Store Violations for Report | Add to qa_report_data |

### Phase 3: spec-compliance-workflow.md (7 Steps including Step 2.5)
**File:** `.claude/skills/devforgeai-qa/references/spec-compliance-workflow.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 0 | Validate Story Documentation | Check Implementation Notes section exists |
| Step 1 | Load Story Specification | Extract AC, API contracts, NFRs, business rules |
| Step 2 | Validate Acceptance Criteria | Find tests for each criterion, verify tests pass |
| Step 2.5 | Validate Deferred DoD Items | **MANDATORY if deferrals exist** - invoke deferral-validator |
| Step 3 | Validate API Contracts | Check endpoints, request/response models |
| Step 4 | Validate Non-Functional Requirements | Performance, security, scalability, availability |
| Step 5 | Generate Traceability Matrix | Map Requirement → Tests → Implementation |

### Phase 4: code-quality-workflow.md (5 Steps)
**File:** `.claude/skills/devforgeai-qa/references/code-quality-workflow.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 1 | Analyze Cyclomatic Complexity | Use radon/complexity-report/metrics, threshold >10 |
| Step 2 | Calculate Maintainability Index | MI <70 = violation |
| Step 3 | Detect Code Duplication | Use jscpd, threshold >5% |
| Step 4 | Measure Documentation Coverage | Count docs vs public APIs, target 80% |
| Step 5 | Analyze Dependency Coupling | Circular dependencies, high coupling (>10 deps) |

### Phase 5: report-generation.md (6 Steps)
**File:** `.claude/skills/devforgeai-qa/references/report-generation.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 1 | Collect All Results | Gather from Phases 0.9, 1, 2, 3, 4 |
| Step 2 | Determine Overall Result | PASSED/FAILED/PARTIAL based on violations |
| Step 3 | Generate QA Report File | Write to .devforgeai/qa/reports/ (deep mode) |
| Step 4 | Create Formatted Display | Invoke qa-result-interpreter subagent |
| Step 5 | Document Blocking Violations | List with remediation steps |
| Step 6 | Prepare Next Steps | Recommendations based on result |

### Phase 6: feedback-hooks-workflow.md (5 Steps)
**File:** `.claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 6.1 | Determine QA Status | Map PASSED→completed, FAILED→failed, PARTIAL→partial |
| Step 6.2 | Check if Hooks Should Trigger | Call check-hooks, note exit code |
| Step 6.3 | Invoke Feedback Hooks | If exit code 0, call invoke-hooks |
| Step 6.4 | Record Hook Status | triggered/skipped/failed |
| Step 6.5 | Return Status to Result | Include in final result object |

### Phase 7: story-update-workflow.md (6 Steps)
**File:** `.claude/skills/devforgeai-qa/references/story-update-workflow.md`
| Step | Description | Key Actions |
|------|-------------|-------------|
| Step 7.1 | Read Current Story File | Extract status, timestamp from YAML |
| Step 7.2 | Update Story Status | Dev Complete → QA Approved |
| Step 7.3 | Update Timestamp | old_date → current_date |
| Step 7.4 | Insert QA Validation History | Add section before Workflow History |
| Step 7.5 | Append Workflow History Entry | Add QA approval line |
| Step 7.6 | Display Confirmation | Show update summary |

---

## Enhanced Checklists (Copy-Paste Ready)

### Phase 1: Test Coverage Analysis

**Location:** After line 278 (after "Blocks on: Business <95%, Application <85%, Overall <80%")

**Add this new section:**

```markdown
**⚠️ CHECKPOINT: You MUST load the reference file and execute ALL steps before proceeding**

**Step 1.0: Load Workflow Reference (REQUIRED)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/coverage-analysis-workflow.md")
```

**After loading:** The reference file contains a complete 7-step workflow. Execute ALL 7 steps before proceeding to Phase 2.

**Phase 1 Completion Checklist:**
Before proceeding to Phase 2, verify you executed ALL 7 steps:
- [ ] Loaded coverage-analysis-workflow.md (Step 1.0)
- [ ] Step 1: Loaded coverage thresholds (95%/85%/80% or from config)
- [ ] Step 2: Generated coverage reports using language-specific command
- [ ] Step 3: Classified files by layer (Business Logic, Application, Infrastructure)
- [ ] Step 4: Calculated coverage percentage for each layer
- [ ] Step 5: Validated against thresholds (identified CRITICAL/HIGH violations if below)
- [ ] Step 6: Identified coverage gaps with test suggestions
- [ ] Step 7: Analyzed test quality (assertion count, over-mocking, test pyramid)
- [ ] Displayed coverage results to user with layer breakdown

**Display to user:**
```
✓ Phase 1 Complete: Test coverage analysis
  Business Logic: [X]% (threshold: 95%)
  Application: [X]% (threshold: 85%)
  Infrastructure: [X]% (threshold: 80%)
  Overall: [X]%
  Gaps identified: [X] | Test quality: [PASS/WARN]
```

**IF any checkbox unchecked:** HALT and complete missing steps.
```

---

### Phase 2: Anti-Pattern Detection (Enhanced)

**Location:** Replace lines 296-304 (current basic checklist)

**Replace with:**

```markdown
**Phase 2 Completion Checklist:**
Before proceeding to Phase 3, verify you executed ALL 6 steps:
- [ ] Loaded anti-pattern-detection-workflow.md (Step 2.0)
- [ ] Step 1: Loaded ALL 6 context files into conversation
  - [ ] tech-stack.md
  - [ ] source-tree.md
  - [ ] dependencies.md
  - [ ] coding-standards.md
  - [ ] architecture-constraints.md
  - [ ] anti-patterns.md
- [ ] Step 2: Invoked anti-pattern-scanner subagent with complete context
- [ ] Step 3: Parsed JSON response (extracted violations by severity)
- [ ] Step 4: Updated blocks_qa state using OR logic with Phase 1
- [ ] Step 5: Displayed violations summary with severity categorization
- [ ] Step 6: Stored violations in qa_report_data for final report

**Display to user:**
```
✓ Phase 2 Complete: Anti-pattern detection
  Total violations: [X]
  CRITICAL: [X] | HIGH: [X] | MEDIUM: [X] | LOW: [X]
  Blocking: [Yes/No]
```

**IF any checkbox unchecked:** HALT and complete missing steps.
```

---

### Phase 3: Spec Compliance Validation (Enhanced)

**Location:** Replace lines 321-328 (current basic checklist)

**Replace with:**

```markdown
**Phase 3 Completion Checklist:**
Before proceeding to Phase 4, verify you executed ALL 7 steps:
- [ ] Loaded spec-compliance-workflow.md (Step 3.0)
- [ ] Step 0: Validated story documentation exists
  - [ ] Implementation Notes section present
  - [ ] Definition of Done Status documented
  - [ ] Test Results recorded
  - [ ] Acceptance Criteria Verification present
- [ ] Step 1: Loaded story specification (AC, API contracts, NFRs)
- [ ] Step 2: Validated acceptance criteria (tests exist and pass for each)
- [ ] Step 2.5: Validated deferred DoD items (MANDATORY if deferrals exist)
  - [ ] IF deferrals exist: Invoked deferral-validator subagent
  - [ ] IF no deferrals: Confirmed no incomplete DoD items (`[ ]`)
- [ ] Step 3: Validated API contracts (endpoints match spec)
- [ ] Step 4: Validated non-functional requirements (performance, security, etc.)
- [ ] Step 5: Generated traceability matrix (Requirement → Tests → Implementation)
- [ ] Displayed spec compliance results to user

**Display to user:**
```
✓ Phase 3 Complete: Spec compliance validation
  Story documentation: ✓ Complete
  AC coverage: [X] of [Y] criteria validated
  API contracts: [X] endpoints verified
  NFRs: [X] requirements checked
  Deferrals: [X validated / No deferrals]
  Traceability: [X]% complete
```

**IF any checkbox unchecked:** HALT and complete missing steps.
```

---

### Phase 4: Code Quality Metrics (Enhanced)

**Location:** Replace lines 345-352 (current basic checklist)

**Replace with:**

```markdown
**Phase 4 Completion Checklist:**
Before proceeding to Phase 5, verify you executed ALL 5 steps:
- [ ] Loaded code-quality-workflow.md (Step 4.0)
- [ ] Step 1: Analyzed cyclomatic complexity
  - [ ] Used language-specific tool (radon/complexity-report/metrics)
  - [ ] Identified methods with complexity >10 (MEDIUM violations)
- [ ] Step 2: Calculated maintainability index
  - [ ] Identified files with MI <70 (MEDIUM violations)
  - [ ] Identified files with MI <50 (HIGH violations - blocks QA)
- [ ] Step 3: Detected code duplication
  - [ ] Used jscpd or equivalent tool
  - [ ] Calculated duplication percentage
  - [ ] Identified if >20% (HIGH violation - blocks QA)
- [ ] Step 4: Measured documentation coverage
  - [ ] Counted documented vs undocumented public APIs
  - [ ] Calculated percentage (target: 80%)
- [ ] Step 5: Analyzed dependency coupling
  - [ ] Detected circular dependencies
  - [ ] Identified high coupling (>10 dependencies per file)
- [ ] Displayed quality metrics to user

**Display to user:**
```
✓ Phase 4 Complete: Code quality metrics
  Cyclomatic Complexity: avg [X] (max [X], threshold: ≤10)
  Maintainability Index: [X]% (threshold: ≥70)
  Code Duplication: [X]% (threshold: <5%)
  Documentation Coverage: [X]% (threshold: ≥80%)
  Coupling Issues: [X] circular deps, [X] high coupling files
  Violations: [X] HIGH, [X] MEDIUM, [X] LOW
```

**IF any checkbox unchecked:** HALT and complete missing steps.
```

---

### Phase 5: QA Report Generation

**Location:** After line 359 (after "Output: Report, story status update, formatted display")

**Add this new section:**

```markdown
**⚠️ CHECKPOINT: You MUST generate the complete QA report before proceeding**

**Step 5.0: Load Report Generation Reference (OPTIONAL - inline workflow also valid)**
```
Read(file_path=".claude/skills/devforgeai-qa/references/report-generation.md")
```

**Phase 5 Completion Checklist:**
Before proceeding to Phase 6, verify you executed ALL 6 steps:
- [ ] Step 1: Collected all results from Phases 0.9, 1, 2, 3, 4
  - [ ] Traceability score from Phase 0.9
  - [ ] Coverage metrics from Phase 1
  - [ ] Anti-pattern violations from Phase 2
  - [ ] Spec compliance status from Phase 3
  - [ ] Quality metrics from Phase 4
- [ ] Step 2: Determined overall QA result (PASSED/FAILED/PARTIAL)
- [ ] Step 3: Generated QA report file (deep mode only)
  - [ ] IF deep mode: Created `.devforgeai/qa/reports/{STORY-ID}-qa-report.md`
  - [ ] IF light mode: Skipped report file (this is correct)
- [ ] Step 4: Invoked qa-result-interpreter subagent for formatted display
- [ ] Step 5: Documented all blocking violations with remediation steps
- [ ] Step 6: Prepared next steps recommendations
- [ ] Displayed complete QA report to user

**Display to user:**
```
✓ Phase 5 Complete: QA Report Generated
  Result: [PASSED ✅ / FAILED ❌ / PARTIAL ⚠️]
  Report: [.devforgeai/qa/reports/{STORY-ID}-qa-report.md / Not generated (light mode)]
  Blocking violations: [X]
  Next steps: [Listed below]
```

**IF any checkbox unchecked:** HALT and complete missing steps.
```

---

### Phase 6: Invoke Feedback Hooks (Enhanced)

**Location:** Replace lines 394-400 (current basic checklist)

**Replace with:**

```markdown
**Phase 6 Completion Checklist:**
Before proceeding to Phase 7, verify you executed ALL 5 steps:
- [ ] Loaded feedback-hooks-workflow.md (Step 6.0)
- [ ] Step 6.1: Determined QA status for hooks
  - [ ] Mapped: PASSED→completed, FAILED→failed, PARTIAL→partial
- [ ] Step 6.2: Checked if hooks should trigger
  - [ ] Called: `devforgeai-validate check-hooks --operation=qa --status=$STATUS`
  - [ ] Noted exit code: 0=trigger, 1=skip
- [ ] Step 6.3: Invoked feedback hooks (only if exit code was 0)
  - [ ] IF exit code 0: Called `devforgeai-validate invoke-hooks --operation=qa --story=$STORY_ID`
  - [ ] IF exit code 1: Noted hooks skipped (configuration blocked)
- [ ] Step 6.4: Recorded hook status (triggered/skipped/failed)
- [ ] Step 6.5: Included hook status in result object for command

**Display to user:**
```
✓ Phase 6 Complete: Feedback hooks
  Hook status: [triggered / skipped / failed]
  [If triggered: Feedback session created]
  [If skipped: Hooks disabled or mode didn't match trigger_on config]
  [If failed: Warning displayed, QA result unchanged]
```

**IF any checkbox unchecked:** HALT and complete missing steps.
```

---

### Phase 7: Update Story File (Enhanced)

**Location:** Replace lines 430-438 (current basic checklist)

**Replace with:**

```markdown
**Phase 7 Completion Checklist (Deep Mode PASSED Only):**
Before completing QA workflow, verify you executed ALL 6 steps:
- [ ] Loaded story-update-workflow.md (Step 7.0)
- [ ] Step 7.1: Read current story file
  - [ ] Extracted current status from YAML frontmatter
  - [ ] Extracted current `updated:` timestamp
- [ ] Step 7.2: Updated story status
  - [ ] Changed: `status: Dev Complete` → `status: QA Approved`
- [ ] Step 7.3: Updated YAML frontmatter timestamp
  - [ ] Changed: `updated: [old_date]` → `updated: [current_date]`
- [ ] Step 7.4: Inserted QA Validation History section
  - [ ] Added complete validation details (coverage, violations, test results)
  - [ ] Inserted before "## Workflow History"
- [ ] Step 7.5: Appended workflow history entry
  - [ ] Added: `- **[DATE]:** QA validation passed (deep mode) - Status: QA Approved`
- [ ] Step 7.6: Displayed confirmation message to user

**Display to user:**
```
✓ Phase 7 Complete: Story file updated
  Status: Dev Complete → QA Approved
  Timestamp: [old_date] → [current_date]
  QA Validation History: ✓ Added
  Workflow History: ✓ Entry appended
```

**IF deep mode passed but any checkbox unchecked:** HALT and complete missing steps.
**IF light mode or QA not passed:** Phase 7 skips - this is correct behavior.
```

---

## Execution Instructions

### Pre-Execution Checklist
```
- [ ] Read current SKILL.md: Read(file_path=".claude/skills/devforgeai-qa/SKILL.md")
- [ ] Verify REC-1 checkpoints exist (should see "⚠️ CHECKPOINT" at Phases 2,3,4,6,7)
- [ ] Create backup: Bash(command="cp .claude/skills/devforgeai-qa/SKILL.md .claude/skills/devforgeai-qa/SKILL.md.rec2-backup")
- [ ] Note current line numbers (may differ from plan if file was modified)
```

### Execution Order

**Step 1:** Add Phase 1 checkpoint and checklist (NEW)
- Location: After line ~278
- Action: Insert entire Phase 1 section

**Step 2:** Enhance Phase 2 checklist
- Location: Find "Phase 2 Completion Checklist:"
- Action: Replace current 5-item checklist with 12-item enhanced version

**Step 3:** Enhance Phase 3 checklist
- Location: Find "Phase 3 Completion Checklist:"
- Action: Replace current 5-item checklist with 14-item enhanced version

**Step 4:** Enhance Phase 4 checklist
- Location: Find "Phase 4 Completion Checklist:"
- Action: Replace current 5-item checklist with 11-item enhanced version

**Step 5:** Add Phase 5 checkpoint and checklist (NEW)
- Location: After line ~359
- Action: Insert entire Phase 5 section

**Step 6:** Enhance Phase 6 checklist
- Location: Find "Phase 6 Completion Checklist:"
- Action: Replace current 4-item checklist with 9-item enhanced version

**Step 7:** Enhance Phase 7 checklist
- Location: Find "Phase 7 Completion Checklist:"
- Action: Replace current 5-item checklist with 10-item enhanced version

### Post-Execution Verification

```bash
# Verify structure
grep -c "⚠️ CHECKPOINT" .claude/skills/devforgeai-qa/SKILL.md
# Expected: 7 (was 5, now includes Phase 1 and Phase 5)

grep -c "Completion Checklist:" .claude/skills/devforgeai-qa/SKILL.md
# Expected: 7

grep -c "Display to user:" .claude/skills/devforgeai-qa/SKILL.md
# Expected: 7

# Verify file size
wc -l .claude/skills/devforgeai-qa/SKILL.md
# Expected: ~600-650 lines (was ~487)
```

---

## Git Commit Message

```
fix(RCA-016): Enhance phase completion checklists in devforgeai-qa (REC-2)

- Add Phase 1 checkpoint and 9-item checklist (7 workflow steps)
- Add Phase 5 checkpoint and 8-item checklist (6 workflow steps)
- Enhance Phase 2 checklist: 5 items → 12 items (6 workflow steps)
- Enhance Phase 3 checklist: 5 items → 14 items (7 workflow steps incl Step 2.5)
- Enhance Phase 4 checklist: 5 items → 11 items (5 workflow steps)
- Enhance Phase 6 checklist: 4 items → 9 items (5 workflow steps)
- Enhance Phase 7 checklist: 5 items → 10 items (6 workflow steps)
- Add "Display to user:" templates for all 7 phases
- Checklists now match exact steps in reference workflow files

RCA: RCA-016 (QA Skill Phase Skipping During Deep Validation)
Recommendation: REC-2 (HIGH) - Add Phase Completion Checklists
Prerequisite: REC-1 (CRITICAL) - Completed in commit 3654474

Total checklist items: ~35 → ~73 (2x increase in verification granularity)
```

---

## Rollback Procedure

```bash
# If implementation fails, restore from backup
cp .claude/skills/devforgeai-qa/SKILL.md.rec2-backup .claude/skills/devforgeai-qa/SKILL.md

# Verify restoration
diff .claude/skills/devforgeai-qa/SKILL.md .claude/skills/devforgeai-qa/SKILL.md.rec2-backup
```

---

## Expected Outcomes

### Before REC-2
- 5 phases have checkpoints (2, 3, 4, 6, 7)
- ~35 generic checklist items
- No display templates
- Checklists don't match workflow steps exactly

### After REC-2
- 7 phases have checkpoints (1, 2, 3, 4, 5, 6, 7)
- ~73 specific checklist items
- Display templates for all 7 phases
- Checklists match reference workflow steps exactly

### Metrics
- **Phases with checkpoints:** 5 → 7 (40% increase)
- **Checklist items:** ~35 → ~73 (2x increase)
- **Workflow step coverage:** ~50% → 100%
- **Phase skipping prevention:** 95% → 99%+

---

## Session Resume Instructions

To resume this plan in a new terminal session:

1. **Read this plan:**
```
Read(file_path=".devforgeai/RCA/RCA-016-REC2-ENHANCED-CHECKLISTS-PLAN.md")
```

2. **Read current SKILL.md:**
```
Read(file_path=".claude/skills/devforgeai-qa/SKILL.md")
```

3. **Create backup:**
```
Bash(command="cp .claude/skills/devforgeai-qa/SKILL.md .claude/skills/devforgeai-qa/SKILL.md.rec2-backup")
```

4. **Execute edits in order (Steps 1-7 from Execution Order section)**

5. **Run verification commands**

6. **Commit changes**

---

**Document Complete - Ready for Execution**
