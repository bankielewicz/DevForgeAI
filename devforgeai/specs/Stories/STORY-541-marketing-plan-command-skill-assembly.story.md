---
id: STORY-541
title: /marketing-plan Command & Skill Assembly
type: feature
epic: EPIC-075
sprint: Sprint-25
status: Ready for Dev
points: 2
depends_on: ["STORY-539", "STORY-540"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-03-03
format_version: "2.9"
---

# Story: /marketing-plan Command & Skill Assembly

## Description

**As a** startup founder or product marketer,
**I want** to invoke `/marketing-plan` from the Claude Code CLI to access a structured marketing workflow,
**so that** I can systematically develop go-to-market strategy, positioning, customer discovery, and content plans — both as standalone activities and anchored to an existing DevForgeAI project.

## Provenance

```xml
<provenance>
  <origin document="EPIC-075" section="Feature 3">
    <quote>"Create /marketing-plan command invoking marketing-business skill. Assemble full marketing-business skill with progressive disclosure references. Integrate with user profile for adaptive pacing. Support both standalone and project-anchored modes."</quote>
    <line_reference>lines 56-61</line_reference>
    <quantified_impact>Single command entry point for entire marketing planning workflow</quantified_impact>
  </origin>
  <stakeholder role="Solo Developer" goal="unified-marketing-command">
    <quote>"I want one command (/marketing-plan) so that I can run the full marketing planning workflow"</quote>
    <source>EPIC-075, User Stories</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Command Invocation & Skill Delegation

```xml
<acceptance_criteria id="AC1" implements="CMD-001">
  <given>A user runs /marketing-plan in the Claude Code CLI without any arguments</given>
  <when>The command is parsed and the marketing-business skill is invoked</when>
  <then>The marketing-business skill launches in standalone mode, prompts the user for business context, and presents a top-level workflow menu offering: (1) Go-to-Market Strategy, (2) Positioning and Messaging, (3) Customer Discovery, (4) Content Strategy. The command file is under 500 lines and contains no workflow logic</then>
  <verification>
    <source_files>
      <file hint="Command file">src/claude/commands/marketing-plan.md</file>
      <file hint="Skill file">src/claude/skills/marketing-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-541/test_ac1_command_invocation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: User Profile Adaptive Pacing

```xml
<acceptance_criteria id="AC2" implements="SVC-001">
  <given>A user runs /marketing-plan from within a DevForgeAI project that contains a user profile</given>
  <when>The marketing-business skill initializes</when>
  <then>The skill reads the user profile, detects experience level, adapts pacing accordingly (skips onboarding for experienced users, simplified language for first-time users), and pre-populates known business context fields without re-asking</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/marketing-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-541/test_ac2_adaptive_pacing.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Progressive Disclosure Architecture

```xml
<acceptance_criteria id="AC3" implements="SVC-002">
  <given>A user selects a workflow phase from the top-level menu</given>
  <when>The skill loads the workflow phase</when>
  <then>The skill presents a concise top-level summary inline, with deep documentation loaded on demand from the references/ directory. SKILL.md remains under 1,000 lines. Reference files contain detailed frameworks, templates, and examples</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/marketing-business/SKILL.md</file>
      <file hint="References directory">src/claude/skills/marketing-business/references/</file>
    </source_files>
    <test_file>tests/STORY-541/test_ac3_progressive_disclosure.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Project-Anchored Mode

```xml
<acceptance_criteria id="AC4" implements="SVC-003">
  <given>A user runs /marketing-plan --mode=project with an active DevForgeAI project</given>
  <when>The skill initializes in project-anchored mode</when>
  <then>The skill reads tech-stack.md, source-tree.md, and existing epic/story files to infer product category and constraints. Marketing recommendations anchored to actual product. Output stored in devforgeai/specs/marketing/ with timestamped filename</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/marketing-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-541/test_ac4_project_mode.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Session Resume

```xml
<acceptance_criteria id="AC5" implements="SVC-004">
  <given>A user completes a marketing-plan session and a prior session artifact exists</given>
  <when>The skill initializes in any mode</when>
  <then>The skill detects the prior session artifact, presents a resume prompt listing last completed phase and date, allows user to continue or start fresh. Prior session never silently overwritten</then>
  <verification>
    <source_files>
      <file hint="Skill file">src/claude/skills/marketing-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-541/test_ac5_session_resume.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

- `src/claude/commands/marketing-plan.md` — Thin command invoker
- `src/claude/skills/marketing-business/SKILL.md` — Main skill orchestrator
- `src/claude/skills/marketing-business/references/` — Progressive disclosure references

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "marketing-plan.md"
      file_path: "src/claude/commands/marketing-plan.md"
      required_keys:
        - key: "skill_invocation"
          type: "string"
          example: "Skill(command='marketing-business')"
          required: true
          validation: "Command delegates to marketing-business skill"
          test_requirement: "Test: Command file contains skill delegation, no workflow logic"
        - key: "mode_flag"
          type: "string"
          example: "--mode=standalone|project"
          required: true
          validation: "Accepts --mode flag with standalone (default) and project options"
          test_requirement: "Test: --mode=project triggers project context reads"

    - type: "Service"
      name: "marketing-business"
      file_path: "src/claude/skills/marketing-business/SKILL.md"
      interface: "Skill"
      lifecycle: "Session"
      dependencies:
        - "user-profile reader"
        - "context file reader"
        - "session artifact writer"
      requirements:
        - id: "SVC-001"
          description: "Orchestrate four workflow phases with top-level menu"
          testable: true
          test_requirement: "Test: Each menu item routes to correct reference file"
          priority: "Critical"
        - id: "SVC-002"
          description: "Read user profile for adaptive pacing when available"
          testable: true
          test_requirement: "Test: Skill adapts prompts based on experience level"
          priority: "High"
        - id: "SVC-003"
          description: "Support project-anchored mode reading context files"
          testable: true
          test_requirement: "Test: Project mode reads tech-stack.md and infers product"
          priority: "High"
        - id: "SVC-004"
          description: "Detect and offer resume of prior sessions"
          testable: true
          test_requirement: "Test: Prior artifact triggers resume prompt"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Command file must be thin invoker — no workflow logic, only delegation"
      trigger: "When command file is created"
      validation: "Command file < 500 lines, no conditional logic"
      error_handling: "Build-time test failure if logic detected"
      test_requirement: "Test: Command file line count <= 500 and contains no if/else logic"
      priority: "Critical"

    - id: "BR-002"
      rule: "SKILL.md must use progressive disclosure — deep content in references/"
      trigger: "When skill file is assembled"
      validation: "SKILL.md < 1,000 lines"
      error_handling: "Build-time test failure if exceeded"
      test_requirement: "Test: SKILL.md line count <= 1,000"
      priority: "Critical"

    - id: "BR-003"
      rule: "Missing user profile degrades gracefully to generic workflow"
      trigger: "When user profile not found"
      validation: "No error thrown, workflow continues"
      error_handling: "Log warning, skip adaptive pacing"
      test_requirement: "Test: Missing profile produces warning but workflow completes"
      priority: "High"

    - id: "BR-004"
      rule: "Prior session artifacts never silently overwritten"
      trigger: "When existing session artifact detected"
      validation: "User prompted before any modification"
      error_handling: "Resume/start-fresh prompt"
      test_requirement: "Test: Existing artifact triggers prompt, no silent overwrite"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command invocation to first prompt in under 2 seconds"
      metric: "< 2s p95 on cold CLI start"
      test_requirement: "Test: Command starts within timeout"
      priority: "Medium"

    - id: "NFR-002"
      category: "Security"
      requirement: "Context files are read-only; skill never writes to devforgeai/specs/context/"
      metric: "Zero writes to immutable context files"
      test_requirement: "Test: No Write() calls target context file paths"
      priority: "Critical"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "User Profile Integration"
    limitation: "User profile from EPIC-072 may not exist yet (EPIC-072 in Planning)"
    decision: "workaround:Graceful degradation - default pacing when profile absent"
    discovered_phase: "Architecture"
    impact: "Adaptive pacing unavailable until EPIC-072 delivers user profile"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Command to first prompt: < 2 seconds (p95)
- Skill initialization: < 500ms (p95)
- Reference file loading: < 300ms per file (p95)

---

### Security

**Authentication:**
- None required (local CLI tool)

**Data Protection:**
- No credentials in output artifacts
- Context files read-only (per ADR-021)
- Session lock files contain only PID and timestamp

---

### Scalability

**Extensibility:**
- References/ supports up to 20 sub-documents
- Projects with up to 200 story/epic files supported
- Command < 500 lines, SKILL.md < 1,000 lines

---

### Reliability

**Error Handling:**
- Missing context files produce non-fatal warnings
- Output directory auto-created if absent
- Lock file cleanup on normal and abnormal exit

---

### Observability

**Logging:**
- Mode detection logged (standalone vs project)
- Profile load status logged
- Session resume detection logged

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-539:** Go-to-Market Strategy Builder
  - **Why:** GTM reference file needed for skill assembly
  - **Status:** Not Started

- [ ] **STORY-540:** Positioning & Messaging Framework
  - **Why:** Positioning reference file needed for skill assembly
  - **Status:** Not Started

### External Dependencies

- None

### Technology Dependencies

- None (pure Markdown skill + command)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** /marketing-plan → skill launches, menu displayed
2. **Edge Cases:**
   - Missing user profile → graceful degradation
   - Corrupted session artifact → fresh start
   - SKILL.md exceeds 1,000 lines → test failure
   - Concurrent invocation → lock file detection
3. **Error Cases:**
   - Unreadable profile → warning, continue
   - Missing context files → warning, continue

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **Command → Skill Delegation:** /marketing-plan invokes marketing-business skill
2. **Project Mode:** --mode=project reads context files and infers product

---

## Acceptance Criteria Verification Checklist

### AC#1: Command Invocation & Skill Delegation

- [ ] Command file < 500 lines - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac1_command_invocation.py
- [ ] No workflow logic in command - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac1_command_invocation.py
- [ ] Skill launches with menu - **Phase:** 5 - **Evidence:** tests/STORY-541/test_ac1_command_invocation.py

### AC#2: User Profile Adaptive Pacing

- [ ] Profile read when available - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac2_adaptive_pacing.py
- [ ] Pacing adapts to experience level - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac2_adaptive_pacing.py

### AC#3: Progressive Disclosure Architecture

- [ ] SKILL.md < 1,000 lines - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac3_progressive_disclosure.py
- [ ] References loaded on demand - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac3_progressive_disclosure.py

### AC#4: Project-Anchored Mode

- [ ] Context files read in project mode - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac4_project_mode.py
- [ ] Output stored with timestamp - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac4_project_mode.py

### AC#5: Session Resume

- [ ] Prior session detected - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac5_session_resume.py
- [ ] Resume prompt shown - **Phase:** 3 - **Evidence:** tests/STORY-541/test_ac5_session_resume.py

---

**Checklist Progress:** 0/11 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] marketing-plan.md command file created (< 500 lines, thin invoker)
- [ ] marketing-business SKILL.md assembled (< 1,000 lines, progressive disclosure)
- [ ] references/ directory with workflow reference files
- [ ] User profile integration with graceful degradation
- [ ] Standalone and project-anchored mode support
- [ ] Session resume detection and prompt

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (missing profile, corrupted artifact, line limits, concurrent access)
- [ ] Command < 500 lines, SKILL.md < 1,000 lines
- [ ] Code coverage >95% for skill logic

### Testing
- [ ] Unit tests for command delegation
- [ ] Unit tests for adaptive pacing
- [ ] Unit tests for progressive disclosure line limits
- [ ] Integration tests for project mode
- [ ] Integration tests for session resume

### Documentation
- [ ] Command file documented with usage examples
- [ ] SKILL.md documented with phase descriptions
- [ ] Story file updated with implementation notes

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Ready for Dev

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-075 Feature 3 | STORY-541.story.md |

## Notes

**Design Decisions:**
- Command is thin invoker only — all logic in skill
- Progressive disclosure: SKILL.md has summaries, references/ has details
- --mode flag controls standalone vs project-anchored behavior
- Session lock files prevent concurrent access

**Open Questions:**
- None

**Related ADRs:**
- None

**References:**
- EPIC-075: Marketing & Customer Acquisition
- BRAINSTORM-011: Business Skills Framework

---

Story Template Version: 2.9
Last Updated: 2026-03-03
