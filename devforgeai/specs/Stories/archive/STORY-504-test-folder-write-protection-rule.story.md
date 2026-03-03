---
id: STORY-504
title: Test Folder Write Protection Rule
type: feature
epic: EPIC-085
sprint: Sprint-18
status: QA Approved
points: 3
depends_on: ["STORY-506"]
priority: Medium
advisory: false
source_gap: null
source_story: null
assigned_to: null
created: 2026-02-27
format_version: "2.9"
---

# Story: Test Folder Write Protection Rule

## Description

**As a** DevForgeAI framework orchestrator,
**I want** a prompt-level rule that restricts write access to the `tests/` folder to only authorized subagents during their designated workflow phases,
**so that** unauthorized test modifications by any agent (including the orchestrator or backend-architect) are prevented and HALT triggers are raised before any test tampering can occur silently.

## Acceptance Criteria

> **IMPORTANT:** XML acceptance criteria format is REQUIRED for automated verification.

### XML Acceptance Criteria Format

### AC#1: Rule File Exists at Correct Path with Required Content

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The DevForgeAI framework repository is at project root</given>
  <when>The rule file .claude/rules/workflow/test-folder-protection.md is read</when>
  <then>The file exists, contains a HALT trigger section declaring tests/ as restricted-write, names test-automator as authorized during Phase 02, names integration-tester as authorized during Phase 05, and specifies AskUserQuestion for any other agent</then>
</acceptance_criteria>
```

---

### AC#2: Rule Is Auto-Loaded via .claude/rules/ Discovery

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>The rule file exists at .claude/rules/workflow/test-folder-protection.md</given>
  <when>Claude Code Terminal starts a new session</when>
  <then>The rule file is auto-loaded as part of .claude/rules/ directory, the HALT trigger is active, and CLAUDE.md references it in the conditional rules table</then>
</acceptance_criteria>
```

---

### AC#3: HALT Fires for Unauthorized Test Modification

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>The rule is loaded and the active context is NOT test-automator (Phase 02) or integration-tester (Phase 05)</given>
  <when>An agent attempts to Write(), Edit(), or create a file matching tests/** or *.test.* or *.spec.*</when>
  <then>The agent HALTs immediately, uses AskUserQuestion to request explicit user approval, and does NOT proceed until approval is granted</then>
</acceptance_criteria>
```

---

### AC#4: test-automator Permitted During Phase 02

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>The implementing-stories skill is executing Phase 02 (Red) and test-automator has been invoked</given>
  <when>test-automator writes or edits files under tests/</when>
  <then>The write proceeds without HALT, the rule explicitly declares this as permitted, no AskUserQuestion interruption</then>
</acceptance_criteria>
```

---

### AC#5: integration-tester Permitted During Phase 05

```xml
<acceptance_criteria id="AC5" implements="COMP-001">
  <given>The implementing-stories skill is executing Phase 05 (Integration) and integration-tester has been invoked</given>
  <when>integration-tester writes or edits test files</when>
  <then>The write proceeds without HALT, the rule explicitly declares this as permitted</then>
</acceptance_criteria>
```

---

### AC#6: CLAUDE.md Conditional Rules Table Updated

```xml
<acceptance_criteria id="AC6" implements="COMP-002">
  <given>CLAUDE.md exists at project root with Conditional Rules section</given>
  <when>The conditional rules table is read</when>
  <then>An entry for test-folder-protection.md appears with path pattern covering tests/**, *.test.*, *.spec.*</then>
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
      name: "test-folder-protection.md"
      file_path: ".claude/rules/workflow/test-folder-protection.md"
      required_keys:
        - key: "halt_trigger"
          type: "object"
          required: true
          test_requirement: "Test: Rule file contains HALT trigger for test file modifications"
        - key: "authorized_agents"
          type: "object"
          required: true
          test_requirement: "Test: Rule file names test-automator (Phase 02) and integration-tester (Phase 05)"
        - key: "test_path_patterns"
          type: "array"
          required: true
          test_requirement: "Test: Rule covers tests/**, *.test.*, *.spec.*, test_*.py, *_test.py"
        - key: "askuserquestion_protocol"
          type: "object"
          required: true
          test_requirement: "Test: Rule specifies AskUserQuestion for unauthorized access attempts"

    - type: "Configuration"
      name: "CLAUDE.md conditional rules update"
      file_path: "CLAUDE.md"
      required_keys:
        - key: "conditional_rules_entry"
          type: "string"
          required: true
          test_requirement: "Test: CLAUDE.md conditional rules table contains test-folder-protection.md entry"

  business_rules:
    - id: "BR-001"
      rule: "Only test-automator may modify tests during Phase 02"
      trigger: "When any agent writes to test path patterns during Phase 02"
      validation: "Agent identity must be test-automator"
      error_handling: "HALT + AskUserQuestion if not test-automator"
      test_requirement: "Test: backend-architect writing to tests/ during Phase 02 → HALT"
      priority: "Critical"
    - id: "BR-002"
      rule: "Only integration-tester may modify tests during Phase 05"
      trigger: "When any agent writes to test path patterns during Phase 05"
      validation: "Agent identity must be integration-tester"
      error_handling: "HALT + AskUserQuestion if not integration-tester"
      test_requirement: "Test: orchestrator writing to tests/ during Phase 05 → HALT"
      priority: "Critical"
    - id: "BR-003"
      rule: "All other phases: test modifications require explicit user approval"
      trigger: "When any agent writes to test paths during Phase 03, 04, or any non-02/05 phase"
      validation: "AskUserQuestion must be invoked"
      error_handling: "HALT immediately, await user response"
      test_requirement: "Test: Any test write during Phase 04 (Refactor) → HALT + AskUserQuestion"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Rule file within framework size limits"
      metric: "50-200 lines, < 8 KB"
      test_requirement: "Test: Rule file is between 50 and 300 lines"
      priority: "Medium"
    - id: "NFR-002"
      category: "Security"
      requirement: "No bypass path for test protection"
      metric: "No --override or --force equivalent; only AskUserQuestion"
      test_requirement: "Test: No override flag mentioned in rule file"
      priority: "High"
```

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Prompt-level enforcement"
    limitation: "Rule enforcement depends on Claude Code respecting .claude/rules/ files; cannot programmatically block Write tool"
    decision: "workaround:prompt-level rule combined with Feature 2 (checksums) for detection-based backup"
    discovered_phase: "Architecture"
    impact: "Rule is advisory at prompt level; checksum system (STORY-502) provides hard enforcement"
```

## Non-Functional Requirements (NFRs)

### Performance

**Rule File Size:**
- Target: 50-200 lines (~2,000-8,000 characters)
- Maximum: 300 lines
- Zero runtime overhead (loaded as static context)

### Security

**Principle of Least Privilege:**
- Only 2 subagents authorized (test-automator, integration-tester)
- Phase-specific authorization (not blanket)
- No bypass path; AskUserQuestion is the only override

### Scalability

**Framework-agnostic:**
- Path patterns work for Python, TypeScript, JavaScript, C#
- New agents default to restricted behavior

### Reliability

**Active from first session:**
- Auto-loaded via .claude/rules/ directory
- Graceful degradation if file missing (WARNING in pre-flight)

### Observability

**Logging:**
- HALT triggers logged with agent name and phase
- AskUserQuestion responses tracked

## Dependencies

### Prerequisite Stories

- [ ] **STORY-506:** ADR and Source-Tree Update
  - **Why:** ADR-025 must be accepted before implementing protection rules
  - **Status:** Not Started

### External Dependencies

None.

### Technology Dependencies

None — uses existing .claude/rules/ directory structure.

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Rule file exists with correct content, authorized agents proceed
2. **Edge Cases:**
   - Co-located test files (src/Component.test.ts) covered by patterns
   - Fixture files (tests/fixtures/) included in protection
   - Phase 04 test modification → HALT
   - Missing rule file → WARNING in pre-flight
3. **Error Cases:**
   - Agent identity not recognized → HALT
   - Phase context ambiguous → HALT

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **CLAUDE.md Integration:** Conditional rules table entry parseable
2. **Workflow Integration:** Rule active during /dev workflow execution

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

### AC#1: Rule File Exists

- [x] File created at correct path - **Phase:** 2 - **Evidence:** src/claude/rules/workflow/test-folder-protection.md
- [x] HALT trigger section present - **Phase:** 2 - **Evidence:** rule file ## HALT Trigger section
- [x] Authorized agents named - **Phase:** 2 - **Evidence:** rule file ## Authorized Agents section

### AC#2: Auto-Loaded

- [x] File in .claude/rules/ directory - **Phase:** 2 - **Evidence:** .claude/rules/workflow/test-folder-protection.md
- [x] CLAUDE.md references it - **Phase:** 2 - **Evidence:** CLAUDE.md conditional rules table

### AC#3: HALT for Unauthorized Access

- [x] HALT trigger fires for non-authorized agents - **Phase:** 1 - **Evidence:** tests/STORY-504/test-folder-protection.test.js
- [x] AskUserQuestion invoked - **Phase:** 1 - **Evidence:** tests/STORY-504/test-folder-protection.test.js

### AC#4: test-automator Permitted

- [x] No HALT during Phase 02 for test-automator - **Phase:** 1 - **Evidence:** tests/STORY-504/test-folder-protection.test.js

### AC#5: integration-tester Permitted

- [x] No HALT during Phase 05 for integration-tester - **Phase:** 1 - **Evidence:** tests/STORY-504/test-folder-protection.test.js

### AC#6: CLAUDE.md Updated

- [x] Conditional rules table entry added - **Phase:** 2 - **Evidence:** CLAUDE.md line 758

---

**Checklist Progress:** 10/10 items complete (100%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-27

- [x] Rule file created at .claude/rules/workflow/test-folder-protection.md - Completed: Created 116-line rule file with HALT trigger, authorized agents, AskUserQuestion protocol, and phase-specific behavior matrix
- [x] HALT trigger for test file write protection - Completed: HALT trigger section covers Write(), Edit(), and file creation operations on protected path patterns
- [x] test-automator authorized for Phase 02 - Completed: Authorized Agents table explicitly permits test-automator during Phase 02 (Red)
- [x] integration-tester authorized for Phase 05 - Completed: Authorized Agents table explicitly permits integration-tester during Phase 05 (Integration)
- [x] All other agents/phases require AskUserQuestion approval - Completed: AskUserQuestion Protocol section with approval format and one-time permission scope
- [x] Test path patterns cover all frameworks (tests/, *.test.*, *.spec.*, test_*.py) - Completed: Protected Path Patterns section covers tests/**, *.test.*, *.spec.*, test_*.py, *_test.py
- [x] CLAUDE.md conditional rules table updated - Completed: Added entry at line 758 with all path patterns
- [x] All 6 acceptance criteria have passing tests - Completed: 23 unit tests + 10 integration tests, all passing (33/33)
- [x] Edge cases covered (co-located tests, fixtures, Phase 04 HALT) - Completed: Phase-specific behavior table covers all phases including Phase 04 Refactor HALT
- [x] No bypass mechanism present - Completed: NFR test confirms no --override, --bypass, --force, --no-verify flags
- [x] Rule file within size limits (50-300 lines) - Completed: 116 lines, within 50-300 range
- [x] Unit tests for HALT trigger behavior - Completed: 3 tests in AC#3 describe block
- [x] Unit tests for authorized agent bypass - Completed: 2 tests each for AC#4 (test-automator) and AC#5 (integration-tester)
- [x] Unit tests for path pattern coverage - Completed: Technical Spec test verifies all 5 path patterns
- [x] Integration test for CLAUDE.md entry - Completed: Integration tests verify parseable entry, cross-story references, and file sync
- [x] Rule file contains clear rationale - Completed: Rationale section explains test integrity risks per phase
- [x] Rule file documents authorized agents and phases - Completed: Authorized Agents table with phase-specific permissions
- [x] Rule file documents HALT trigger format - Completed: HALT Trigger section with 3 conditions and consequence steps

## Definition of Done

### Implementation
- [x] Rule file created at .claude/rules/workflow/test-folder-protection.md
- [x] HALT trigger for test file write protection
- [x] test-automator authorized for Phase 02
- [x] integration-tester authorized for Phase 05
- [x] All other agents/phases require AskUserQuestion approval
- [x] Test path patterns cover all frameworks (tests/, *.test.*, *.spec.*, test_*.py)
- [x] CLAUDE.md conditional rules table updated

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (co-located tests, fixtures, Phase 04 HALT)
- [x] No bypass mechanism present
- [x] Rule file within size limits (50-300 lines)

### Testing
- [x] Unit tests for HALT trigger behavior
- [x] Unit tests for authorized agent bypass
- [x] Unit tests for path pattern coverage
- [x] Integration test for CLAUDE.md entry

### Documentation
- [x] Rule file contains clear rationale
- [x] Rule file documents authorized agents and phases
- [x] Rule file documents HALT trigger format

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | Complete | 23 unit tests written, all failing |
| Phase 03 (Green) | Complete | Rule file + CLAUDE.md entry created, 23 tests passing |
| Phase 04 (Refactor) | Complete | No refactoring needed, code-reviewer approved |
| Phase 05 (Integration) | Complete | 10 integration tests added, 33/33 passing |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/rules/workflow/test-folder-protection.md | Created | 116 |
| .claude/rules/workflow/test-folder-protection.md | Created | 116 |
| CLAUDE.md | Modified | +1 |
| tests/STORY-504/test-folder-protection.test.js | Created | 263 |
| tests/STORY-504/test-folder-protection.integration.test.js | Created | ~330 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-085 Feature 4 | STORY-504.story.md |
| 2026-02-27 | /validate-stories | Status Update | Status changed from Backlog to Ready for Dev | STORY-504.story.md |
| 2026-02-27 | .claude/qa-result-interpreter | QA Deep | PASSED: 33/33 tests, 0 violations, 3/3 validators | - |

## Notes

**Design Decisions:**
- Prompt-level enforcement (not programmatic) because Claude Code respects .claude/rules/ files
- Phase-specific authorization prevents test-automator from modifying tests outside Phase 02
- All files under tests/ protected (including helpers, fixtures, conftest.py)
- Refactor phase (Phase 04) explicitly NOT authorized — prevents test tampering masquerading as refactoring

**Related ADRs:**
- [ADR-025: QA Diff Regression Detection](../adrs/ADR-025-qa-diff-regression-detection.md)

**References:**
- EPIC-085: QA Diff Regression Detection and Test Integrity System
- Feature 4: Test Folder Write Protection Rule (FR-004)

---

Story Template Version: 2.9
Last Updated: 2026-02-27
