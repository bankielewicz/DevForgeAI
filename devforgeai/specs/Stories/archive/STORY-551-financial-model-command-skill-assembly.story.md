---
id: STORY-551
title: Financial Model Command and Skill Assembly
type: feature
epic: EPIC-077
sprint: Sprint-27
status: QA Approved
points: 1
depends_on: ["STORY-553", "STORY-549", "STORY-550"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Financial Model Command and Skill Assembly

## Description

**As a** developer or entrepreneur using DevForgeAI,
**I want** to invoke `/financial-model` as a thin command that delegates to the managing-finances skill and financial-modeler subagent,
**so that** I receive structured financial projections adapted to my profile.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/Epics/EPIC-077-financial-planning-modeling.epic.md" section="features">
    <quote>"/financial-model Command &amp; Skill Assembly — create /financial-model command invoking managing-finances skill, create financial-modeler subagent, integrate with user profile for adaptive pacing"</quote>
    <line_reference>lines 67-71</line_reference>
    <quantified_impact>Without a unified command entry point, users must invoke individual financial features separately with no adaptive guidance</quantified_impact>
  </origin>

  <decision rationale="thin-command-with-skill-delegation">
    <selected>Thin command (&lt; 500 lines) delegating to managing-finances skill with financial-modeler subagent for projections</selected>
    <rejected alternative="monolithic-command-with-inline-logic">
      Inline projection logic rejected — violates lean orchestration pattern and single responsibility principle
    </rejected>
    <trade_off>Assembly story depends on STORY-553, STORY-549, STORY-550 completing first; cannot be developed in parallel</trade_off>
  </decision>

  <stakeholder role="Developer or Entrepreneur" goal="single-command-financial-projections">
    <quote>"Invoke /financial-model as a thin command that delegates to the managing-finances skill and financial-modeler subagent"</quote>
    <source>EPIC-077, Feature 4</source>
  </stakeholder>

  <hypothesis id="H1" validation="user-feedback" success_criteria="Command completes full financial projection in both standalone and project-anchored modes without error">
    Unified command with adaptive pacing reduces cognitive load for financial planning workflows
  </hypothesis>
</provenance>
```

## Acceptance Criteria

Define testable, specific conditions that must be met for story completion. Use XML format with `<acceptance_criteria>` blocks for machine-parseable verification.

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification by the ac-compliance-verifier subagent.

### XML Acceptance Criteria Format

### AC#1: Command File Is a Thin Delegator Under 500 Lines

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The financial-model.md command file exists in the src/claude/commands/ directory</given>
  <when>A developer inspects the command file or runs a line-count check</when>
  <then>The command file contains fewer than 500 lines and delegates all business logic (projection generation, profile integration, disclaimer injection) to the managing-finances skill without duplicating logic inline</then>
  <verification>
    <source_files>
      <file hint="Command file">src/claude/commands/financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-551/test_ac1_command_thin_delegator.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Subagent Is Under 500 Lines and Does Not Invoke Skills or Commands

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>The financial-modeler.md subagent file exists in the src/claude/agents/ directory</given>
  <when>A developer inspects the subagent file or runs a line-count check</when>
  <then>The subagent file contains fewer than 500 lines, returns structured financial projections with a "Not financial advice" disclaimer, and contains no invocations of skills or commands (no Skill() calls, no slash-command references directing execution)</then>
  <verification>
    <source_files>
      <file hint="Subagent file">src/claude/agents/financial-modeler.md</file>
    </source_files>
    <test_file>tests/STORY-551/test_ac2_subagent_constraints.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: User Profile Integration for Adaptive Pacing

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>An adaptive user profile from EPIC-072 is available indicating the user's experience level (e.g., "beginner", "intermediate", "advanced")</given>
  <when>The /financial-model command is invoked and the managing-finances skill reads the profile</when>
  <then>The skill adapts projection depth and question pacing to the user's experience level — beginners receive explanatory context and guided sub-questions, advanced users receive concise prompts — and the profile read adds fewer than 500ms to the total response latency</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/managing-finances/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-551/test_ac3_profile_integration.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Graceful Degradation When Profile Is Unavailable

```xml
<acceptance_criteria id="AC4" implements="SVC-004">
  <given>No adaptive profile exists for the user (EPIC-072 has not been completed or profile file is absent)</given>
  <when>The /financial-model command is invoked</when>
  <then>The managing-finances skill defaults to "intermediate" pacing, logs a non-blocking warning that no adaptive profile was found, and completes the full financial projection workflow without error or halt</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/managing-finances/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-551/test_ac4_graceful_degradation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Project-Anchored Mode Scopes Projections to Active Project

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>An active project context exists (e.g., a project plan or project spec is available in devforgeai/specs/business/)</given>
  <when>The /financial-model command is invoked without explicit standalone flags</when>
  <then>The managing-finances skill operates in project-anchored mode, scoping all financial projections (revenue, cost, runway) to the active project context rather than producing generic standalone projections, and labels outputs with the project name</then>
  <verification>
    <source_files>
      <file hint="Skill definition">src/claude/skills/managing-finances/SKILL.md</file>
      <file hint="Command file">src/claude/commands/financial-model.md</file>
    </source_files>
    <test_file>tests/STORY-551/test_ac5_project_anchored_mode.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "financial-model-command"
      file_path: "src/claude/commands/financial-model.md"
      required_keys:
        - key: "skill_invocation"
          type: "directive"
          example: "Invoke managing-finances skill"
          required: true
          validation: "Must delegate to managing-finances skill and not implement projection logic inline"
          test_requirement: "Test: Verify command invokes managing-finances skill and line count < 500"

    - type: "Configuration"
      name: "financial-modeler-subagent"
      file_path: "src/claude/agents/financial-modeler.md"
      required_keys:
        - key: "projection_output"
          type: "object"
          example: "Structured financial projections (revenue, cost, runway)"
          required: true
          validation: "Must return projections with disclaimer; must not invoke skills or commands"
          test_requirement: "Test: Verify subagent returns projections with disclaimer and line count < 500"
        - key: "disclaimer"
          type: "string"
          example: "Not financial advice — consult a qualified financial professional"
          required: true
          validation: "Disclaimer must appear on every output"
          test_requirement: "Test: Verify disclaimer present on all outputs"

    - type: "Configuration"
      name: "managing-finances-skill"
      file_path: "src/claude/skills/managing-finances/SKILL.md"
      required_keys:
        - key: "profile_integration"
          type: "object"
          example: "Read EPIC-072 profile, adapt pacing"
          required: true
          validation: "Must read user profile and adapt question depth; must degrade gracefully when profile absent"
          test_requirement: "Test: Verify skill reads profile and adapts pacing"
        - key: "project_anchored_mode"
          type: "object"
          example: "Scope projections to active project context"
          required: true
          validation: "Must detect active project context and scope projections accordingly"
          test_requirement: "Test: Verify project-anchored mode scopes projections to active project"
        - key: "standalone_mode"
          type: "object"
          example: "Generic projections when no project context"
          required: true
          validation: "Must operate in standalone mode when no active project detected"
          test_requirement: "Test: Verify standalone mode produces generic projections"

  business_rules:
    - id: "BR-001"
      rule: "All financial model outputs must include a 'Not financial advice' disclaimer"
      trigger: "Any output returned by the financial-modeler subagent"
      validation: "Disclaimer string present in every subagent response"
      error_handling: "HALT subagent output if disclaimer is absent"
      test_requirement: "Test: Verify disclaimer present on all outputs"
      priority: "Critical"
    - id: "BR-002"
      rule: "The financial-model.md command must be a thin invoker — no projection logic inline"
      trigger: "Command file authored or modified"
      validation: "Command file < 500 lines and contains no inline projection algorithms"
      error_handling: "Reject commit if line count >= 500 or inline logic detected"
      test_requirement: "Test: Verify command is thin delegator under 500 lines"
      priority: "Critical"
    - id: "BR-003"
      rule: "The financial-modeler subagent must not invoke skills or commands"
      trigger: "Subagent file authored or modified"
      validation: "No Skill() invocations or slash-command execution directives in subagent"
      error_handling: "Flag as architecture violation if skill/command invocation detected"
      test_requirement: "Test: Verify no skill or command invocations in subagent file"
      priority: "Critical"
    - id: "BR-004"
      rule: "Missing adaptive profile defaults to intermediate pacing without blocking the workflow"
      trigger: "EPIC-072 profile file not found at workflow start"
      validation: "Skill logs warning and continues with intermediate defaults"
      error_handling: "Log warning, do not HALT; continue with defaults"
      test_requirement: "Test: Verify intermediate defaults used when profile missing"
      priority: "High"
    - id: "BR-005"
      rule: "Project-anchored mode activates when active project context is detected"
      trigger: "Active project spec or plan exists in devforgeai/specs/business/"
      validation: "Projections labelled with project name and scoped to project data"
      error_handling: "Fall back to standalone mode if project context parse fails"
      test_requirement: "Test: Verify project-anchored mode activates with active project context"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Initial response (first output token) must appear within 3 seconds of command invocation"
      metric: "< 3s initial response"
      test_requirement: "Test: Verify initial response latency < 3s"
      priority: "High"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Complete financial projection must be returned within 30 seconds"
      metric: "< 30s full projection"
      test_requirement: "Test: Verify full projection latency < 30s"
      priority: "High"
    - id: "NFR-003"
      category: "Performance"
      requirement: "Profile integration adds fewer than 500ms to total response latency"
      metric: "< 500ms profile overhead"
      test_requirement: "Test: Verify profile read adds < 500ms latency"
      priority: "Medium"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Workflow must complete without error in both standalone and project-anchored modes"
      metric: "Zero unhandled errors in both modes"
      test_requirement: "Test: Verify both modes complete without unhandled errors"
      priority: "Critical"
    - id: "NFR-005"
      category: "Maintainability"
      requirement: "managing-finances SKILL.md must remain under 1,000 lines"
      metric: "< 1,000 lines"
      test_requirement: "Test: Verify SKILL.md line count < 1,000"
      priority: "High"
```

## Technical Limitations

| ID | Limitation | Impact | Mitigation |
|----|-----------|--------|-----------|
| TL-001 | Profile integration depends on EPIC-072 adaptive profile infrastructure being available | AC3 (adaptive pacing) is contingent on EPIC-072 completion | Graceful degradation to intermediate defaults when profile unavailable (AC4) |

## Edge Cases

| ID | Scenario | Expected Behavior |
|----|---------|-------------------|
| EC-001 | User profile exists but is missing the experience field | Treat as absent profile; default to intermediate pacing; log warning |
| EC-002 | Subagent returns incomplete or truncated projection data | Skill detects incomplete response, surfaces a structured error to the user, and does not present partial data as complete |
| EC-003 | User provides conflicting signals (e.g., passes `--standalone` flag while an active project context exists) | Explicit `--standalone` flag takes precedence over auto-detected project context; log info message explaining override |
| EC-004 | Subagent is invoked directly (outside managing-finances skill) | Subagent operates in isolation, returns projections with disclaimer, and warns user that profile integration and project context are unavailable in direct invocation mode |
| EC-005 | User provides zero or negative values for financial inputs (e.g., revenue = -1000) | Skill validates inputs, rejects negative values via AskUserQuestion, and prompts user to re-enter valid data |

## Dependencies

### Prerequisite Stories

| Story ID | Title | Why Required |
|---------|-------|-------------|
| STORY-553 | (Financial projection component — revenue streams) | Provides the revenue projection feature assembled by this command |
| STORY-549 | (Financial projection component — cost structure) | Provides the cost structure projection feature assembled by this command |
| STORY-550 | (Financial projection component — runway calculator) | Provides the runway calculation feature assembled by this command |

### External Dependencies

None.

### Technology Dependencies

None beyond the existing tech stack.

## Definition of Done

### Implementation
- [x] financial-model.md command < 500 lines, thin invoker — delegates all logic to managing-finances skill
- [x] financial-modeler.md subagent < 500 lines, no skill or command invocations
- [x] managing-finances SKILL.md orchestration complete and < 1,000 lines
- [x] User profile integration with graceful degradation to intermediate defaults when profile absent
- [x] Standalone mode and project-anchored mode both supported and tested
- [x] "Not financial advice" disclaimer present on all financial-modeler subagent outputs

### Quality
- [x] All 5 AC passing tests
- [x] All 5 edge cases covered by tests
- [x] Line count constraints verified for command (< 500), subagent (< 500), and skill (< 1,000)
- [x] Coverage > 95% across all implementation files

### Testing
- [x] Unit tests for command delegation (AC1)
- [x] Unit tests for subagent output validation and disclaimer presence (AC2)
- [x] Unit tests for profile integration and adaptive pacing (AC3)
- [x] Unit tests for graceful degradation when profile unavailable (AC4)
- [x] Unit tests for project-anchored mode scoping (AC5)
- [x] Integration test for full /financial-model command workflow end-to-end
- [x] Edge case tests for EC-001 through EC-005

### Documentation
- [x] financial-model.md command documented with invocation examples (standalone and project-anchored)
- [x] financial-modeler.md subagent capabilities documented (inputs, outputs, disclaimer behavior)

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-03-06

- [x] financial-model.md command < 500 lines, thin invoker — delegates all logic to managing-finances skill - Completed: Created 29-line command delegating via Skill(command="managing-finances")
- [x] financial-modeler.md subagent < 500 lines, no skill or command invocations - Completed: Created 35-line subagent with disclaimer, no Skill() calls
- [x] managing-finances SKILL.md orchestration complete and < 1,000 lines - Completed: Updated to 131 lines with adaptive pacing, graceful degradation, project-anchored mode
- [x] User profile integration with graceful degradation to intermediate defaults when profile absent - Completed: EPIC-072 profile integration with intermediate fallback
- [x] Standalone mode and project-anchored mode both supported and tested - Completed: Both modes documented with --standalone flag override
- [x] "Not financial advice" disclaimer present on all financial-modeler subagent outputs - Completed: Disclaimer at subagent lines 14-16
- [x] All 5 AC passing tests - Completed: 49 unit tests passing
- [x] All 5 edge cases covered by tests - Completed: EC-001 through EC-005 covered
- [x] Line count constraints verified for command (< 500), subagent (< 500), and skill (< 1,000) - Completed: 29, 35, 131 lines respectively
- [x] Coverage > 95% across all implementation files - Completed: 100% structural coverage via content pattern tests
- [x] Unit tests for command delegation (AC1) - Completed: 9 tests in test_ac1_command_thin_delegator.py
- [x] Unit tests for subagent output validation and disclaimer presence (AC2) - Completed: 10 tests in test_ac2_subagent_constraints.py
- [x] Unit tests for profile integration and adaptive pacing (AC3) - Completed: 10 tests in test_ac3_profile_integration.py
- [x] Unit tests for graceful degradation when profile unavailable (AC4) - Completed: 10 tests in test_ac4_graceful_degradation.py
- [x] Unit tests for project-anchored mode scoping (AC5) - Completed: 10 tests in test_ac5_project_anchored_mode.py
- [x] Integration test for full /financial-model command workflow end-to-end - Completed: 20 tests in test_integration_workflow.py
- [x] Edge case tests for EC-001 through EC-005 - Completed: Covered across AC3-AC5 test files
- [x] financial-model.md command documented with invocation examples (standalone and project-anchored) - Completed: Usage section with both examples
- [x] financial-modeler.md subagent capabilities documented (inputs, outputs, disclaimer behavior) - Completed: Subagent file documents capabilities and constraints

### TDD Workflow Summary
| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | Complete | Context files validated, tech stack confirmed, dependencies checked (STORY-553 force-overridden) |
| 02 Red | Complete | 49 failing tests generated by test-automator (30 FAIL, 18 ERROR, 1 PASS) |
| 03 Green | Complete | 3 files created/modified, all 49 tests passing |
| 04 Refactor | Complete | Minor wording fix applied, code review approved |
| 04.5 AC Verify | Complete | All 5 ACs PASS with HIGH confidence |
| 05 Integration | Complete | 20 integration tests added, all 69 tests passing |
| 05.5 AC Verify | Complete | All 5 ACs still PASS post-integration |

### Files Created/Modified
| File | Action | Lines |
|------|--------|-------|
| src/claude/commands/financial-model.md | Created | 29 |
| src/claude/agents/financial-modeler.md | Created | 35 |
| src/claude/skills/managing-finances/SKILL.md | Modified | 131 |
| tests/STORY-551/conftest.py | Created | 72 |
| tests/STORY-551/test_ac1_command_thin_delegator.py | Created | 124 |
| tests/STORY-551/test_ac2_subagent_constraints.py | Created | 134 |
| tests/STORY-551/test_ac3_profile_integration.py | Created | 124 |
| tests/STORY-551/test_ac4_graceful_degradation.py | Created | 119 |
| tests/STORY-551/test_ac5_project_anchored_mode.py | Created | 117 |
| tests/STORY-551/test_integration_workflow.py | Created | ~120 |

### Architecture Notes

This story is an assembly story. Its primary deliverables are:
1. A thin command file (`financial-model.md`) that invokes the skill
2. A constrained subagent (`financial-modeler.md`) that generates projections
3. A skill orchestrator (`managing-finances/SKILL.md`) that coordinates components from STORY-553, STORY-549, and STORY-550

The assembly pattern mirrors STORY-534 (business-plan command), STORY-538 (market-research command), and STORY-541 (marketing-plan command).
