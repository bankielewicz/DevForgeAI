---
id: STORY-034
title: Refactor /qa command - Move Phases 4 & 5 to skill
epic: EPIC-007
sprint: Sprint-3
status: Backlog
points: 8
priority: High
assigned_to: TBD
created: 2025-11-14
format_version: "2.0"
---

# Story: Refactor /qa command - Move Phases 4 & 5 to skill

## Description

**As a** DevForgeAI framework maintainer,
**I want** the /qa command to delegate Phases 4 & 5 (feedback hooks and story updates) to the devforgeai-qa skill,
**So that** commands remain lean orchestrators following the "commands orchestrate, skills validate" pattern and business logic resides in the correct architectural layer.

## Acceptance Criteria

### 1. [ ] Phase 6 Added to devforgeai-qa Skill

**Given** the devforgeai-qa skill currently has 5 phases (coverage, anti-patterns, spec compliance, quality, report),
**When** Phase 6 is added after Phase 5,
**Then** Phase 6 implements feedback hook invocation logic (currently in /qa command Phase 4),
**And** Phase 6 determines QA status (PASSED/FAILED/PARTIAL),
**And** Phase 6 calls `devforgeai check-hooks --operation=qa --status=$STATUS`,
**And** Phase 6 conditionally invokes `devforgeai invoke-hooks` based on check-hooks exit code,
**And** Phase 6 is non-blocking (hook failures don't affect QA result).

---

### 2. [ ] Phase 7 Added to devforgeai-qa Skill

**Given** Phase 6 (feedback hooks) has completed,
**When** Phase 7 executes and validation mode is "deep" and result is "PASSED",
**Then** Phase 7 reads current story file,
**And** Phase 7 updates story status from "Dev Complete" to "QA Approved",
**And** Phase 7 updates YAML frontmatter timestamp,
**And** Phase 7 inserts QA Validation History section before Workflow History,
**And** Phase 7 appends workflow history entry,
**And** Phase 7 displays confirmation message.

---

### 3. [ ] Phases 4 & 5 Removed from /qa Command

**Given** Phases 4 & 5 logic has been moved to skill,
**When** /qa command is refactored,
**Then** old Phase 4 (Invoke Feedback Hook) is deleted from command (lines 166-242),
**And** old Phase 5 (Update Story Status) is deleted from command (lines 243-332),
**And** command has only 3 phases remaining (Phase 0, 1, 2),
**And** command size reduces from 509 lines to ~340 lines (33% reduction).

---

### 4. [ ] Command Becomes Pure Orchestrator

**Given** /qa command has been refactored,
**When** user runs `/qa STORY-XXX deep`,
**Then** Phase 0 validates arguments and loads story,
**And** Phase 1 invokes skill with context markers,
**And** Phase 2 displays skill-returned result,
**And** command does NOT execute feedback hooks (skill does),
**And** command does NOT update story file (skill does),
**And** command total is 3 phases (validate → invoke → display).

---

### 5. [ ] Skill Returns Complete Result

**Given** devforgeai-qa skill now has Phases 6 & 7,
**When** skill execution completes,
**Then** skill returns structured result including:
  - Display template (from qa-result-interpreter),
  - Story file update confirmation (if deep mode pass),
  - Feedback hook status (triggered/skipped/failed),
  - Next steps recommendations,
**And** command displays this complete result without additional processing.

---

### 6. [ ] Reference Files Created for New Phases

**Given** Phases 6 & 7 are substantial (87 + 80 lines),
**When** progressive disclosure is applied,
**Then** `references/feedback-hooks-workflow.md` is created for Phase 6 details,
**And** `references/story-update-workflow.md` is created for Phase 7 details,
**And** skill SKILL.md references these files (not inline implementation),
**And** skill remains under 500 lines entry point.

---

### 7. [ ] Lean Orchestration Pattern Validated

**Given** refactoring is complete,
**When** validating against lean-orchestration-pattern.md protocol,
**Then** command does ONLY: parse arguments, load context, set markers, invoke skill, display results,
**And** command does NOT: business logic, complex parsing, template generation, decision-making, error recovery,
**And** skill does: extract parameters, execute workflow, invoke subagents, generate outputs, return results,
**And** pattern compliance is 100% (all 5 command responsibilities, zero violations).

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Service"
      name: "QASkillPhase6FeedbackHooks"
      file_path: ".claude/skills/devforgeai-qa/SKILL.md"
      requirements:
        - id: "SERV-001"
          description: "Add Phase 6: Invoke Feedback Hooks to skill workflow"
          testable: true
          test_requirement: "Test: Grep skill SKILL.md for 'Phase 6.*Feedback Hook', verify section exists"
          priority: "Critical"
        - id: "SERV-002"
          description: "Phase 6 determines QA status (PASSED→completed, FAILED→failed, PARTIAL→partial)"
          testable: true
          test_requirement: "Test: Parse Phase 6 bash code, verify if-elif-else status mapping present"
          priority: "High"
        - id: "SERV-003"
          description: "Phase 6 calls check-hooks with --operation=qa --status=$STATUS"
          testable: true
          test_requirement: "Test: Verify 'devforgeai check-hooks --operation=qa' command in Phase 6"
          priority: "High"
        - id: "SERV-004"
          description: "Phase 6 conditionally invokes feedback hooks based on exit code 0"
          testable: true
          test_requirement: "Test: Verify 'if [ $? -eq 0 ]' wraps invoke-hooks call"
          priority: "High"
        - id: "SERV-005"
          description: "Phase 6 is non-blocking (|| { echo warning } pattern)"
          testable: true
          test_requirement: "Test: Verify non-blocking error handling in Phase 6"
          priority: "Medium"

    - type: "Service"
      name: "QASkillPhase7StoryUpdates"
      file_path: ".claude/skills/devforgeai-qa/SKILL.md"
      requirements:
        - id: "SERV-006"
          description: "Add Phase 7: Update Story File to skill workflow"
          testable: true
          test_requirement: "Test: Grep skill SKILL.md for 'Phase 7.*Update Story', verify section exists"
          priority: "Critical"
        - id: "SERV-007"
          description: "Phase 7 updates story status to 'QA Approved' (deep mode pass only)"
          testable: true
          test_requirement: "Test: Verify Edit call updating status in Phase 7"
          priority: "High"
        - id: "SERV-008"
          description: "Phase 7 updates YAML frontmatter timestamp"
          testable: true
          test_requirement: "Test: Verify 'updated: YYYY-MM-DD' Edit call in Phase 7"
          priority: "High"
        - id: "SERV-009"
          description: "Phase 7 inserts QA Validation History section"
          testable: true
          test_requirement: "Test: Verify QA Validation History template insertion before Workflow History"
          priority: "High"
        - id: "SERV-010"
          description: "Phase 7 appends workflow history entry"
          testable: true
          test_requirement: "Test: Verify workflow history entry added with QA validation details"
          priority: "Medium"

    - type: "Configuration"
      name: "QACommandRefactoring"
      file_path: ".claude/commands/qa.md"
      requirements:
        - id: "CONF-001"
          description: "Remove Phase 4 (Invoke Feedback Hook) from command"
          testable: true
          test_requirement: "Test: Grep qa.md, verify NO 'Phase 4: Invoke Feedback Hook' exists"
          priority: "Critical"
        - id: "CONF-002"
          description: "Remove Phase 5 (Update Story Status) from command"
          testable: true
          test_requirement: "Test: Grep qa.md, verify NO 'Phase 5: Update Story' exists"
          priority: "Critical"
        - id: "CONF-003"
          description: "Command has only 3 phases (Phase 0, 1, 2)"
          testable: true
          test_requirement: "Test: Count phases in qa.md, assert exactly 3"
          priority: "High"
        - id: "CONF-004"
          description: "Command size reduced to ~340 lines (33% reduction from 509)"
          testable: true
          test_requirement: "Test: wc -l qa.md, assert <360 lines"
          priority: "Medium"
        - id: "CONF-005"
          description: "Phase 1 notes skill now handles hooks and updates"
          testable: true
          test_requirement: "Test: Verify Phase 1 documentation mentions skill Phases 6 & 7"
          priority: "Low"

    - type: "DataModel"
      name: "FeedbackHooksWorkflowReference"
      file_path: ".claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md"
      requirements:
        - id: "DATA-001"
          description: "Create feedback-hooks-workflow.md reference file"
          testable: true
          test_requirement: "Test: File exists at path"
          priority: "High"
        - id: "DATA-002"
          description: "Document Phase 6 detailed implementation (status mapping, check-hooks, invoke-hooks)"
          testable: true
          test_requirement: "Test: File contains sections for status determination, hook checking, hook invocation"
          priority: "Medium"
        - id: "DATA-003"
          description: "Include non-blocking error handling pattern"
          testable: true
          test_requirement: "Test: Grep for '|| {' error handling pattern"
          priority: "Medium"

    - type: "DataModel"
      name: "StoryUpdateWorkflowReference"
      file_path: ".claude/skills/devforgeai-qa/references/story-update-workflow.md"
      requirements:
        - id: "DATA-004"
          description: "Create story-update-workflow.md reference file"
          testable: true
          test_requirement: "Test: File exists at path"
          priority: "High"
        - id: "DATA-005"
          description: "Document Phase 7 detailed implementation (Read, Edit operations, template insertion)"
          testable: true
          test_requirement: "Test: File contains sections for status update, timestamp, history, workflow entry"
          priority: "Medium"
        - id: "DATA-006"
          description: "Include QA Validation History template"
          testable: true
          test_requirement: "Test: Grep for '## QA Validation History' template"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Skill Phases 6 & 7 execute autonomously (no command intervention)"
      test_requirement: "Test: Run /qa deep pass, verify story updated without Phase 5 in command"
    - id: "BR-002"
      rule: "Phase 6 is non-blocking (hook failures don't affect QA result)"
      test_requirement: "Test: Mock hook failure, verify QA still returns PASSED"
    - id: "BR-003"
      rule: "Phase 7 only executes on deep mode PASS (not light, not fail)"
      test_requirement: "Test: Run /qa light pass, verify story NOT updated"
    - id: "BR-004"
      rule: "Command delegates ALL business logic to skill (zero logic in command)"
      test_requirement: "Test: Review qa.md, verify no if-then logic except argument validation"
    - id: "BR-005"
      rule: "Skill returns complete result (command just displays)"
      test_requirement: "Test: Verify skill returns display template, command outputs as-is"

  non_functional_requirements:
    - id: "NFR-P1"
      category: "Performance"
      requirement: "Refactoring adds <100ms overhead to /qa execution"
      metric: "Measured execution time difference (before/after refactoring) <100ms"
      test_requirement: "Test: Run /qa 10 times before/after, measure average, assert delta <100ms"
    - id: "NFR-M1"
      category: "Maintainability"
      requirement: "Command size reduced by 30%+ (509 → ~340 lines)"
      metric: "Line count reduction ≥30%"
      test_requirement: "Test: wc -l qa.md.backup vs qa.md, assert ≥30% reduction"
    - id: "NFR-C1"
      category: "Compliance"
      requirement: "100% lean orchestration pattern compliance"
      metric: "All 5 command responsibilities met, zero violations"
      test_requirement: "Test: Manual checklist validation against lean-orchestration-pattern.md"
    - id: "NFR-R1"
      category: "Reliability"
      requirement: "Zero functional regressions (behavior identical before/after)"
      metric: "100% test pass rate (existing /qa tests)"
      test_requirement: "Test: Run existing QA tests, assert all pass"
```

## UI Specification

N/A - This is a framework refactoring story with no user-facing UI components.

## Edge Cases

1. **Skill Phase 6 or 7 fails mid-execution**
   - Skill returns error result
   - Command displays error message
   - Story status remains unchanged
   - User sees clear failure reason

2. **Command modified independently during refactoring**
   - Backup command before changes (qa.md → qa.md.backup-STORY-034)
   - Conflicts detected via line number mismatches
   - Manual merge required
   - Document conflicts in story notes

3. **Existing /qa tests fail after refactoring**
   - Indicates functional regression
   - Rollback changes
   - Root cause analysis
   - Fix regression before completing story

4. **Progressive disclosure breaks skill entry point**
   - Skill SKILL.md exceeds 500 lines
   - Extract more content to reference files
   - Verify all references load correctly
   - Test skill invocation still works

5. **Reference files not found during skill execution**
   - Skill logs error "Reference file missing: feedback-hooks-workflow.md"
   - Verify file paths correct (.claude/skills/devforgeai-qa/references/)
   - Check file created and committed
   - Test skill loads references on-demand

## Non-Functional Requirements

**NFR-P1: Performance**
- Target: <100ms overhead added by refactoring
- Measurement: Run `/qa STORY-024 deep` 10 times before and after, compare averages
- Acceptable: User notices no performance difference

**NFR-M1: Maintainability**
- Target: 30%+ command size reduction (509 → ~340 lines)
- Measurement: `wc -l qa.md.backup vs qa.md`
- Acceptable: Command is easier to understand and maintain

**NFR-C1: Compliance**
- Target: 100% lean orchestration pattern compliance
- Measurement: Manual checklist against `.devforgeai/protocols/lean-orchestration-pattern.md`
- Acceptable: Command passes all 5 responsibility checks, zero violations

**NFR-R1: Reliability**
- Target: Zero functional regressions
- Measurement: Run existing /qa integration tests (75 tests)
- Acceptable: 100% test pass rate (75/75)

## Definition of Done

### Implementation
- [ ] Phase 6 added to `.claude/skills/devforgeai-qa/SKILL.md` (feedback hooks logic)
- [ ] Phase 7 added to `.claude/skills/devforgeai-qa/SKILL.md` (story update logic)
- [ ] Reference file created: `references/feedback-hooks-workflow.md`
- [ ] Reference file created: `references/story-update-workflow.md`
- [ ] Phase 4 removed from `.claude/commands/qa.md`
- [ ] Phase 5 removed from `.claude/commands/qa.md`
- [ ] Command refactored to 3 phases (Phase 0, 1, 2)
- [ ] All 7 acceptance criteria implemented

### Quality
- [ ] Command size reduced to ~340 lines (33% reduction measured)
- [ ] Skill entry point remains <500 lines
- [ ] Progressive disclosure applied (2 reference files created)
- [ ] No functional regressions (75/75 tests pass)
- [ ] Performance overhead <100ms (measured)

### Testing
- [ ] Test: Grep skill for Phase 6, verify exists
- [ ] Test: Grep skill for Phase 7, verify exists
- [ ] Test: Grep command, verify NO Phase 4/5
- [ ] Test: Count command phases, assert == 3
- [ ] Test: Run `/qa STORY-024 deep`, verify story updated automatically
- [ ] Test: Run `/qa STORY-024 light`, verify story NOT updated
- [ ] Test: Mock hook failure, verify QA result unchanged
- [ ] Test: Measure performance before/after, assert <100ms delta
- [ ] Test: Run existing 75 QA tests, assert 100% pass rate
- [ ] Test: Validate lean orchestration compliance (manual checklist)

### Documentation
- [ ] RCA-009 updated with implementation results
- [ ] lean-orchestration-pattern.md updated (if needed)
- [ ] command-budget-reference.md updated (new /qa metrics)
- [ ] Reference files documented in skill SKILL.md

## Dependencies

### Prerequisites
- RCA-009 analysis complete (provides implementation plan)
- lean-orchestration-pattern.md protocol exists
- devforgeai-qa skill exists with 5 phases

### Blocked By
- None (can proceed immediately)

### Blocks
- None (independent refactoring work)

## Notes

**Why This Refactoring Matters:**

From RCA-009 analysis:
> **Root Cause:** Phases 4 & 5 are in the command instead of the skill, violating lean orchestration.
>
> **Pattern:** "Commands orchestrate. Skills validate. Subagents specialize."

**Current violation:**
- /qa command has business logic (feedback hooks, story updates)
- Command is 509 lines (approaching 15K character budget)
- Phases 4 & 5 belong in skill, not command

**After refactoring:**
- Command: Pure orchestrator (3 phases: validate → invoke → display)
- Skill: All business logic (7 phases including hooks and updates)
- Pattern: 100% compliant with lean orchestration protocol

**Evidence-Based Solution:**
- Pattern already proven in `/dev`, `/create-sprint`, `/create-epic` refactorings
- Skills have execution model, commands do not
- Skills are designed for multi-phase workflows
- Progressive disclosure keeps entry points lean

**Implementation Effort:** 90 minutes per RCA-009 analysis
- 45 min: Move logic to skill (Phases 6 & 7)
- 15 min: Simplify command (remove Phases 4 & 5)
- 30 min: Test and validate

**Files Modified:**
1. `.claude/skills/devforgeai-qa/SKILL.md` - Add Phases 6 & 7
2. `.claude/commands/qa.md` - Remove Phases 4 & 5, simplify to 3 phases

**Files Created:**
1. `.claude/skills/devforgeai-qa/references/feedback-hooks-workflow.md`
2. `.claude/skills/devforgeai-qa/references/story-update-workflow.md`

**Related:**
- RCA-009: Root cause analysis (why Phase 5 didn't execute autonomously)
- STORY-024: Wire hooks into /qa command (added Phase 4 originally)
- lean-orchestration-pattern.md: Protocol defining command/skill responsibilities

---

## Implementation Notes

N/A - Story in Backlog status, development not yet started.

---

## Workflow History

- **2025-11-14:** Story created (STORY-034) - Status: Backlog - RCA-009 implementation plan
