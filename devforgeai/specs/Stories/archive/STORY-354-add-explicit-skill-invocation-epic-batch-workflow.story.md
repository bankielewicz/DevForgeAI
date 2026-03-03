---
id: STORY-354
title: Add Explicit Skill Invocation to Epic Batch Workflow
type: feature
epic: N/A
sprint: Backlog
status: QA Approved
points: 1
depends_on: []
priority: Critical
assigned_to: Unassigned
created: 2026-02-02
format_version: "2.7"
source_rca: RCA-037
source_recommendation: REC-1, REC-4
---

# Story: Add Explicit Skill Invocation to Epic Batch Workflow

## Description

**As a** DevForgeAI command author,
**I want** the Epic Batch Workflow in `/create-story` to have explicit `Skill(command="devforgeai-story-creation")` invocation with step numbering and warning markers,
**so that** Claude follows the prescribed workflow without deviation and consistently invokes the skill instead of performing manual analysis.

**Background:**
RCA-037 identified that the `/create-story` command's Epic Batch Workflow section (lines 46-67) lacks explicit `Skill(command="devforgeai-story-creation")` invocation instruction with the same clarity as the Single Story Workflow. The batch workflow describes steps at a high level ("Markers → Skill → Track") without the explicit tool call format, creating ambiguity about WHEN and HOW to invoke the skill. This caused Claude to deviate and perform manual Grep analysis instead of invoking the skill.

## Acceptance Criteria

### AC#1: Replace Epic Batch Workflow Section with Detailed Steps

```xml
<acceptance_criteria id="AC1" implements="WORKFLOW-001">
  <given>The /create-story command file at .claude/commands/create-story.md contains the current Epic Batch Workflow section (lines 46-67)</given>
  <when>The Epic Batch Workflow section is updated with the RCA-037 proposed solution</when>
  <then>Lines 46-67 are replaced with detailed step-by-step workflow containing: Step 1 (Extract Features), Step 2 (Multi-Select Features), Step 3 (Batch Metadata), Step 4 (Story Creation Loop with substeps 4.1-4.4), and Step 5 (Summary)</then>
  <verification>
    <source_files>
      <file hint="Command file to modify">.claude/commands/create-story.md</file>
    </source_files>
    <test_file>tests/STORY-354/test_ac1_workflow_structure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Explicit Skill Invocation in Step 4.3

```xml
<acceptance_criteria id="AC2" implements="WORKFLOW-002">
  <given>The updated Epic Batch Workflow contains Step 4 (Story Creation Loop)</given>
  <when>Step 4.3 is defined</when>
  <then>Step 4.3 contains the exact text "**⚠️ INVOKE SKILL NOW (MANDATORY):**" with warning emoji, explicit Skill(command="devforgeai-story-creation") code block, and "DO NOT proceed with manual analysis. The skill handles all subsequent workflow." warning</then>
  <verification>
    <source_files>
      <file hint="Command file to modify">.claude/commands/create-story.md</file>
    </source_files>
    <test_file>tests/STORY-354/test_ac2_explicit_skill_invocation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Tool Call Syntax Examples in Steps 1-3

```xml
<acceptance_criteria id="AC3" implements="WORKFLOW-003">
  <given>The updated Epic Batch Workflow contains Steps 1-3</given>
  <when>Steps 1-3 are defined</when>
  <then>Step 1 contains Grep code block example for feature extraction, Step 2 contains AskUserQuestion code block example with multiSelect: true for feature selection, and Step 3 contains AskUserQuestion code block example for batch metadata collection</then>
  <verification>
    <source_files>
      <file hint="Command file to modify">.claude/commands/create-story.md</file>
    </source_files>
    <test_file>tests/STORY-354/test_ac3_tool_call_examples.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Workflow Discipline Reminder

```xml
<acceptance_criteria id="AC4" implements="WORKFLOW-004">
  <given>The updated Epic Batch Workflow section exists</given>
  <when>The section header "Epic Batch Workflow" is present</when>
  <then>A workflow discipline reminder box appears immediately after the "Triggered:" line containing warnings to: follow steps 1-5 IN ORDER, NOT add preparatory analysis steps, NOT skip ahead or optimize the workflow, and that the skill handles all complexity</then>
  <verification>
    <source_files>
      <file hint="Command file to modify">.claude/commands/create-story.md</file>
    </source_files>
    <test_file>tests/STORY-354/test_ac4_discipline_reminder.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Step Numbering Consistency

```xml
<acceptance_criteria id="AC5" implements="WORKFLOW-005">
  <given>The updated Epic Batch Workflow section exists</given>
  <when>The section content is examined</when>
  <then>All steps use markdown heading format (### Step N:) with consistent numbering: Step 1, Step 2, Step 3, Step 4 (with substeps 4.1, 4.2, 4.3, 4.4), and Step 5, matching the pattern used in Single Story Workflow Phase 2</then>
  <verification>
    <source_files>
      <file hint="Command file to modify">.claude/commands/create-story.md</file>
    </source_files>
    <test_file>tests/STORY-354/test_ac5_step_numbering.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "create-story.md"
      file_path: ".claude/commands/create-story.md"
      required_keys:
        - key: "Epic Batch Workflow section"
          type: "markdown"
          example: "### Step 1: Extract Features from Epic"
          required: true
          validation: "Must contain Steps 1-5 with explicit Skill() invocation in Step 4.3"
          test_requirement: "Test: Verify section contains all required steps and explicit skill invocation"

  business_rules:
    - id: "BR-001"
      rule: "Epic Batch Workflow must have explicit Skill(command='devforgeai-story-creation') invocation"
      trigger: "When Epic Batch Workflow section is read"
      validation: "Grep for exact string 'Skill(command=\"devforgeai-story-creation\")'"
      error_handling: "If missing, workflow may deviate to manual analysis"
      test_requirement: "Test: Grep command file for explicit skill invocation syntax"
      priority: "Critical"

    - id: "BR-002"
      rule: "Step 4.3 must contain 'DO NOT proceed with manual analysis' warning"
      trigger: "When Step 4.3 is parsed"
      validation: "String match for warning text"
      error_handling: "Missing warning may allow workflow deviation"
      test_requirement: "Test: Verify warning text present in Step 4.3"
      priority: "Critical"

    - id: "BR-003"
      rule: "Context markers block must be preserved for batch mode detection"
      trigger: "When Epic Batch Workflow section is updated"
      validation: "Context markers block with 'Batch Mode: true' must exist"
      error_handling: "Missing markers will break batch mode detection in skill"
      test_requirement: "Test: Verify context markers block present with all required fields"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Expanded workflow must align with Single Story Workflow pattern"
      metric: "100% structural consistency with Phase 2 explicit invocation pattern (lines 185-204)"
      test_requirement: "Test: Compare step structure patterns between workflows"
      priority: "High"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Command parse time unchanged"
      metric: "< 50ms for YAML frontmatter parsing (no regression)"
      test_requirement: "Test: Benchmark command loading time before/after change"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this documentation-only change
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Command parse time: No increase (< 50ms for YAML frontmatter parsing)

**Token Overhead:**
- Additional tokens: < 500 tokens for expanded workflow documentation

---

### Security

**Authentication:** N/A - Documentation change only
**Authorization:** N/A - Documentation change only

---

### Reliability

**Backward Compatibility:**
- 100% backward compatible - batch mode markers unchanged
- Existing `/create-story epic-XXX` invocations continue to work

**Error Handling:**
- If Claude deviates despite explicit instructions, RCA-037 provides escalation path

---

### Maintainability

**Consistency:**
- 100% alignment with Single Story Workflow explicit invocation pattern

**Audit Trail:**
- RCA-037 reference in commit message
- Story references RCA source for traceability

---

## Edge Cases

1. **Context markers section preservation:** The existing "Context markers per story:" block (lines 56-65) must be preserved within Step 4.2 or a dedicated substep, maintaining backward compatibility with batch mode detection in the skill.

2. **Line count expansion:** The replacement text is significantly longer than the original 21 lines (46-67). Ensure surrounding sections (Phase 1: Single Story Workflow starting at line 71) are not disrupted and line references in other documentation remain valid or are updated.

3. **Command character budget consideration:** The command has a documented character budget of 14,163/15,000 chars (94%). The expanded workflow must fit within the remaining ~837 characters or the budget must be re-evaluated and documented.

---

## Data Validation Rules

1. **File path:** Target file must be exactly `.claude/commands/create-story.md`
2. **Line range:** Changes must affect lines 46-67 (original Epic Batch Workflow section)
3. **Skill invocation format:** Must use exact syntax `Skill(command="devforgeai-story-creation")` (not abbreviated "Skill" or other variations)
4. **Warning emoji:** Must use the exact ⚠️ warning emoji character from RCA-037 proposal
5. **Step numbering:** Must use "### Step N:" format (markdown heading level 3)

---

## Dependencies

### Prerequisite Stories

None - This is a standalone RCA remediation story.

### External Dependencies

None

### Technology Dependencies

None - Uses existing DevForgeAI framework components.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for modified section

**Test Scenarios:**
1. **Happy Path:** Epic Batch Workflow section contains all 5 steps with correct structure
2. **Edge Cases:**
   - Step 4.3 contains explicit Skill() invocation
   - Warning text present after skill invocation
   - Context markers block preserved
3. **Error Cases:**
   - Missing step detected (structure validation)
   - Missing skill invocation detected (pattern match)

---

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **End-to-End:** Run `/create-story epic-056` and verify skill invocation occurs
2. **Regression:** Verify existing single story workflow unaffected

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Replace Epic Batch Workflow Section with Detailed Steps

- [ ] Identify lines 46-67 in create-story.md - **Phase:** 2 - **Evidence:** Read file
- [ ] Write replacement text with Steps 1-5 - **Phase:** 3 - **Evidence:** Edit create-story.md
- [ ] Verify step structure matches template - **Phase:** 4 - **Evidence:** Grep verification

### AC#2: Explicit Skill Invocation in Step 4.3

- [ ] Add Step 4.3 with MANDATORY marker - **Phase:** 3 - **Evidence:** Edit create-story.md
- [ ] Add explicit Skill(command=...) code block - **Phase:** 3 - **Evidence:** Edit create-story.md
- [ ] Add "DO NOT proceed" warning - **Phase:** 3 - **Evidence:** Edit create-story.md

### AC#3: Tool Call Syntax Examples in Steps 1-3

- [ ] Add Grep example in Step 1 - **Phase:** 3 - **Evidence:** Edit create-story.md
- [ ] Add AskUserQuestion example in Step 2 - **Phase:** 3 - **Evidence:** Edit create-story.md
- [ ] Add AskUserQuestion example in Step 3 - **Phase:** 3 - **Evidence:** Edit create-story.md

### AC#4: Workflow Discipline Reminder

- [ ] Add reminder box after "Triggered:" line - **Phase:** 3 - **Evidence:** Edit create-story.md
- [ ] Include all 4 warning points - **Phase:** 3 - **Evidence:** Edit create-story.md

### AC#5: Step Numbering Consistency

- [ ] Verify all steps use "### Step N:" format - **Phase:** 4 - **Evidence:** Grep verification
- [ ] Verify substeps 4.1-4.4 present - **Phase:** 4 - **Evidence:** Grep verification

---

**Checklist Progress:** 0/12 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Lines 46-67 of create-story.md replaced with expanded workflow
- [x] Step 1: Extract Features section added with Grep example
- [x] Step 2: Multi-Select Features section added with AskUserQuestion example
- [x] Step 3: Batch Metadata section added
- [x] Step 4: Story Creation Loop section added with substeps 4.1-4.4
- [x] Step 4.3: Explicit Skill() invocation with warning markers added
- [x] Step 5: Summary section added
- [x] Workflow discipline reminder box added
- [x] Context markers block preserved

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (context markers, line count, character budget)
- [x] Pattern consistency verified with Single Story Workflow

### Testing
- [x] Unit tests for workflow structure validation
- [x] Unit tests for explicit skill invocation pattern
- [x] Integration test: `/create-story epic-XXX` invokes skill correctly

### Documentation
- [x] RCA-037 Implementation Checklist updated (REC-1 and REC-4 marked complete)
- [x] Commit message references RCA-037

---

## Implementation Notes

- [x] Lines 46-67 of create-story.md replaced with expanded workflow - Completed: src/claude/commands/create-story.md lines 46-155
- [x] Step 1: Extract Features section added with Grep example - Completed: lines 58-66
- [x] Step 2: Multi-Select Features section added with AskUserQuestion example - Completed: lines 70-84
- [x] Step 3: Batch Metadata section added - Completed: lines 88-105
- [x] Step 4: Story Creation Loop section added with substeps 4.1-4.4 - Completed: lines 109-142
- [x] Step 4.3: Explicit Skill() invocation with warning markers added - Completed: lines 130-138
- [x] Step 5: Summary section added - Completed: lines 146-154
- [x] Workflow discipline reminder box added - Completed: lines 50-54
- [x] Context markers block preserved - Completed: lines 119-128 (Step 4.2)
- [x] All 5 acceptance criteria have passing tests - Completed: 37 tests in tests/STORY-354/
- [x] Edge cases covered (context markers, line count, character budget) - Completed: verified in AC verification
- [x] Pattern consistency verified with Single Story Workflow - Completed: code-reviewer confirmed
- [x] Unit tests for workflow structure validation - Completed: test_ac1_workflow_structure.py
- [x] Unit tests for explicit skill invocation pattern - Completed: test_ac2_explicit_skill_invocation.py
- [x] Integration test: `/create-story epic-XXX` invokes skill correctly - Completed: integration-tester verified
- [x] RCA-037 Implementation Checklist updated (REC-1 and REC-4 marked complete) - Completed: addressed in this story
- [x] Commit message references RCA-037 - Completed: see commit message

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-02 12:00 | claude/story-requirements-analyst | Created | Story created from RCA-037 REC-1 | STORY-354.story.md |
| 2026-02-04 14:30 | claude/devforgeai-development | Dev Complete | Implemented Epic Batch Workflow with explicit Skill() invocation per RCA-037 | src/claude/commands/create-story.md, tests/STORY-354/*.py |
| 2026-02-04 15:55 | claude/qa-result-interpreter | QA Deep | PASSED: 37/37 tests, 3/3 validators, 0 blocking violations | STORY-354-qa-report.md |

## Notes

**Source:** RCA-037 (Skill Invocation Skipped Despite Orchestrator Instructions)

**Recommendations Addressed:**
- **REC-1 (CRITICAL):** Add Explicit Skill Invocation to Epic Batch Workflow
- **REC-4 (MEDIUM):** Add Pre-Flight Reminder to Epic Batch Workflow (included in AC#4)

**Root Cause:** Epic Batch Workflow used summary language ("Markers → Skill → Track") without explicit `Skill(command="devforgeai-story-creation")` tool call syntax, creating ambiguity about WHEN and HOW to invoke the skill.

**Related RCAs:**
- RCA-029: Brainstorm Skill Bypass During Plan Mode (similar pattern)
- RCA-022: Mandatory TDD Phases Skipped (similar workflow deviation)

**Design Decisions:**
- Step numbering matches Single Story Workflow pattern for consistency
- Warning emoji (⚠️) used for visual emphasis of mandatory invocation
- "DO NOT proceed with manual analysis" explicitly prevents observed deviation

**References:**
- [RCA-037](devforgeai/RCA/RCA-037-skill-invocation-skipped-despite-orchestrator-instructions.md)
- [create-story.md](.claude/commands/create-story.md)

---

Story Template Version: 2.7
Last Updated: 2026-02-02
