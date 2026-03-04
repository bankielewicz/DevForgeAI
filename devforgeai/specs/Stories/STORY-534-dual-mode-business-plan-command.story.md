---
id: STORY-534
title: Dual-Mode /business-plan Command
type: feature
epic: EPIC-073
sprint: Sprint-23
status: Ready for Dev
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-03-03
format_version: "2.9"
---

# Story: Dual-Mode /business-plan Command

## Description

**As a** DevForgeAI user,
**I want** a `/business-plan` command that automatically detects whether I'm in a DevForgeAI project or working standalone,
**so that** I can generate business plans enriched with codebase context when available, or from a business idea description alone.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Project-Anchored Mode Detection

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The user is in a directory containing devforgeai/specs/context/ files</given>
  <when>The user invokes /business-plan</when>
  <then>The command detects project-anchored mode, reads codebase context (tech-stack.md, architecture-constraints.md), and passes it to the planning-business skill</then>
  <verification>
    <source_files>
      <file hint="Command definition">src/claude/commands/business-plan.md</file>
    </source_files>
    <test_file>tests/STORY-534/test_ac1_project_mode.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Standalone Mode Detection

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>The user is in a directory without devforgeai/specs/context/ files</given>
  <when>The user invokes /business-plan</when>
  <then>The command operates in standalone mode, prompts for a business idea description, and invokes the planning-business skill without codebase context</then>
  <verification>
    <source_files>
      <file hint="Command definition">src/claude/commands/business-plan.md</file>
    </source_files>
    <test_file>tests/STORY-534/test_ac2_standalone_mode.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Consistent Output Format

```xml
<acceptance_criteria id="AC3" implements="SVC-003">
  <given>The command runs in either project-anchored or standalone mode</given>
  <when>The planning-business skill completes</when>
  <then>The output follows the same structured business plan format regardless of mode</then>
  <verification>
    <source_files>
      <file hint="Command definition">src/claude/commands/business-plan.md</file>
      <file hint="Skill definition">src/claude/skills/planning-business/SKILL.md</file>
    </source_files>
    <test_file>tests/STORY-534/test_ac3_consistent_output.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Explicit Mode Override

```xml
<acceptance_criteria id="AC4" implements="SVC-004">
  <given>The user is in a DevForgeAI project</given>
  <when>The user invokes /business-plan with a --standalone flag</when>
  <then>The command ignores project context and operates in standalone mode</then>
  <verification>
    <source_files>
      <file hint="Command definition">src/claude/commands/business-plan.md</file>
    </source_files>
    <test_file>tests/STORY-534/test_ac4_mode_override.sh</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Missing Context Graceful Degradation

```xml
<acceptance_criteria id="AC5" implements="SVC-005">
  <given>The user is in a DevForgeAI project but some context files are missing or unreadable</given>
  <when>The user invokes /business-plan</when>
  <then>The command logs which context files were unavailable, proceeds with available context, and does not fail</then>
  <verification>
    <source_files>
      <file hint="Command definition">src/claude/commands/business-plan.md</file>
    </source_files>
    <test_file>tests/STORY-534/test_ac5_graceful_degradation.sh</test_file>
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
      name: "business-plan-command"
      file_path: "src/claude/commands/business-plan.md"
      required_keys:
        - key: "mode_detection"
          type: "object"
          example: "Check for devforgeai/specs/context/ directory"
          required: true
          validation: "Must implement project vs standalone detection logic"
          test_requirement: "Test: Verify mode detection based on context directory presence"
        - key: "skill_invocation"
          type: "object"
          example: "Invoke planning-business skill with mode context"
          required: true
          validation: "Must invoke planning-business skill"
          test_requirement: "Test: Verify skill invocation in both modes"
        - key: "argument_handling"
          type: "object"
          example: "--standalone flag support"
          required: true
          validation: "Must support mode override flag"
          test_requirement: "Test: Verify --standalone flag overrides auto-detection"

  business_rules:
    - id: "BR-001"
      rule: "Project detection based solely on devforgeai/specs/context/ directory presence"
      trigger: "Command invocation"
      validation: "Check directory existence with Glob, not Bash"
      error_handling: "Fallback to standalone mode if directory missing"
      test_requirement: "Test: Verify detection uses Glob for context directory"
      priority: "Critical"
    - id: "BR-002"
      rule: "Standalone mode requires business idea description input; cannot proceed without it"
      trigger: "Standalone mode activation"
      validation: "User prompted for description via AskUserQuestion"
      error_handling: "HALT if no description provided"
      test_requirement: "Test: Verify standalone mode prompts for business idea"
      priority: "High"
    - id: "BR-003"
      rule: "Output format identical across modes; mode only affects input context richness"
      trigger: "Skill output generation"
      validation: "Same output structure regardless of mode"
      error_handling: "N/A - design constraint"
      test_requirement: "Test: Verify output format consistency across modes"
      priority: "High"
    - id: "BR-004"
      rule: "Mode override flag (--standalone) takes precedence over auto-detection"
      trigger: "Flag parsing"
      validation: "Standalone mode activated when flag present regardless of directory"
      error_handling: "N/A"
      test_requirement: "Test: Verify flag overrides auto-detection"
      priority: "Medium"
    - id: "BR-005"
      rule: "Mode detection uses native tools (Glob/Read), not Bash commands"
      trigger: "Directory check"
      validation: "No Bash used for file detection"
      error_handling: "N/A - design constraint"
      test_requirement: "Test: Verify no Bash commands in mode detection"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command initialization (mode detection) completes within 2 seconds"
      metric: "< 2 seconds"
      test_requirement: "Test: Verify mode detection time"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Context file reading in project-anchored mode within 5 seconds for all 6 files"
      metric: "< 5 seconds total"
      test_requirement: "Test: Verify context reading time"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Zero crashes on partial context (missing files)"
      metric: "No exceptions on missing context files"
      test_requirement: "Test: Verify graceful handling of missing context files"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "/business-plan command"
    limitation: "Cannot detect DevForgeAI project in parent directories; only checks current directory"
    decision: "workaround:User must invoke command from project root"
    discovered_phase: "Architecture"
    impact: "User must be in correct directory; clear error message if not"
```

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Mode detection:** < 2 seconds
- **Context file reading:** < 5 seconds (all 6 files)

---

### Security

**Authentication:**
- None (local CLI tool)

**Data Protection:**
- Context files read locally
- No data transmitted externally

**Security Testing:**
- [ ] No hardcoded secrets
- [ ] Native tools used for all file operations

---

### Scalability

- Not applicable (CLI tool)

---

### Reliability

**Error Handling:**
- Missing context directory: Standalone mode
- Partial context files: Warn and proceed with available
- Empty context files: Treat as unavailable

---

### Observability

**Logging:**
- INFO: Detected mode, context files loaded
- WARN: Missing or empty context files

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-531:** Lean Canvas Guided Workflow
  - **Why:** /business-plan command invokes planning-business skill
  - **Status:** Not Started

### External Dependencies

None

### Technology Dependencies

None — uses existing Claude Code command and skill framework

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Project-anchored mode detection and skill invocation
2. **Edge Cases:**
   - Partial project structure (devforgeai/ without context/)
   - Empty context files (0 bytes)
   - No business idea in standalone mode
3. **Error Cases:**
   - Missing planning-business skill
   - Invalid --standalone flag usage

---

### Integration Tests

**Coverage Target:** 85%+

**Test Scenarios:**
1. **Project-anchored flow:** Detect project → Read context → Invoke skill
2. **Standalone flow:** No project → Prompt idea → Invoke skill
3. **Mode override:** In project → --standalone → Standalone flow

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking
- **AC Checklist:** AC sub-item tracking ← YOU ARE HERE
- **Definition of Done:** Official completion record

### AC#1: Project-Anchored Mode Detection

- [ ] Context directory check implemented - **Phase:** 2 - **Evidence:** src/claude/commands/business-plan.md
- [ ] Context files read and passed to skill - **Phase:** 2 - **Evidence:** business-plan.md
- [ ] Mode displayed to user - **Phase:** 2 - **Evidence:** business-plan.md

### AC#2: Standalone Mode Detection

- [ ] Missing context triggers standalone - **Phase:** 2 - **Evidence:** business-plan.md
- [ ] Business idea prompt via AskUserQuestion - **Phase:** 2 - **Evidence:** business-plan.md

### AC#3: Consistent Output Format

- [ ] Same output structure both modes - **Phase:** 4 - **Evidence:** tests/STORY-534/

### AC#4: Explicit Mode Override

- [ ] --standalone flag parsed - **Phase:** 2 - **Evidence:** business-plan.md
- [ ] Flag overrides auto-detection - **Phase:** 1 - **Evidence:** tests/STORY-534/

### AC#5: Missing Context Graceful Degradation

- [ ] Missing files logged as warnings - **Phase:** 2 - **Evidence:** business-plan.md
- [ ] Proceeds with available context - **Phase:** 4 - **Evidence:** tests/STORY-534/
- [ ] No crash on partial context - **Phase:** 1 - **Evidence:** tests/STORY-534/

---

**Checklist Progress:** 0/11 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers before DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during /dev workflow*

## Definition of Done

### Implementation
- [ ] Command file created at src/claude/commands/business-plan.md
- [ ] Project-anchored mode detects and reads context files
- [ ] Standalone mode prompts for business idea
- [ ] --standalone flag overrides auto-detection
- [ ] Both modes produce identical output format
- [ ] Graceful degradation on missing/empty context files

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (partial project, empty files, no idea input)
- [ ] Native tools used (no Bash for file operations)
- [ ] Code coverage > 95% for business logic

### Testing
- [ ] Unit tests for mode detection logic
- [ ] Unit tests for --standalone flag
- [ ] Integration test for project-anchored flow
- [ ] Integration test for standalone flow
- [ ] Edge case tests for graceful degradation

### Documentation
- [ ] Command file documented with usage instructions
- [ ] Mode detection logic documented
- [ ] Graceful degradation behavior documented

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
| 2026-03-03 | .claude/story-requirements-analyst | Created | Story created from EPIC-073 Feature 4 | STORY-534-dual-mode-business-plan-command.story.md |

## Notes

**Design Decisions:**
- Project detection checks devforgeai/specs/context/ directory (not package.json or other markers)
- Standalone mode requires explicit business idea input (no empty invocation)
- --standalone flag enables expert users to skip context injection
- Graceful degradation logs warnings but continues (resilient design)

**Open Questions:**
- [ ] Which context files to inject in project-anchored mode (all 6 or subset?) - **Owner:** DevForgeAI - **Due:** Sprint 1

**References:**
- EPIC-073: Business Planning & Viability
- Claude Code custom slash command pattern

---

Story Template Version: 2.9
Last Updated: 2026-03-03
