---
id: STORY-487
title: Dual-Path Architecture Validation Function and /validate-stories Integration
type: feature
epic: null
sprint: Backlog
status: QA Approved
points: 3
depends_on: []
priority: Critical
advisory: false
source_gap: null
source_story: null
source_rca: "RCA-039"
source_recommendation: "REC-1, REC-2"
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: Dual-Path Architecture Validation Function and /validate-stories Integration

## Description

**As a** framework maintainer running `/validate-stories` or `/create-story`,
**I want** a `validate_dual_path()` function in context-validation.md that detects stories specifying `.claude/` operational paths instead of `src/claude/` source-of-truth paths, and the `/validate-stories` command updated to invoke this function,
**so that** dual-path architecture violations are caught automatically during story creation and validation, preventing the recurrence documented in RCA-039 (and previously RCA-033).

## Provenance

```xml
<provenance>
  <origin document="RCA-039" section="REC-1, REC-2">
    <quote>"No validation function checks dual-path architecture compliance in story technical specifications."</quote>
    <line_reference>RCA-039 lines 86-190</line_reference>
    <quantified_impact>13 file_path values across 6 stories (472-479) referenced .claude/ instead of src/claude/, undetected by /validate-stories</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: validate_dual_path() Function Exists

```xml
<acceptance_criteria id="AC1">
  <given>context-validation.md contains 6 validation functions (validate_technologies through validate_anti_patterns)</given>
  <when>the file is inspected after implementation</when>
  <then>a 7th function validate_dual_path(tech_spec_content) exists after validate_anti_patterns and before "Custody Chain Validation Functions", with severity HIGH, input of technical specification content, and process that reads source-tree.md to check for Dual-Location Architecture section</then>
  <verification>
    <source_files>
      <file hint="validation reference">src/claude/skills/devforgeai-story-creation/references/context-validation.md</file>
    </source_files>
    <test_file>tests/STORY-487/test_ac1_function_exists.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: Detects .claude/ Paths Without dual_path_sync

```xml
<acceptance_criteria id="AC2">
  <given>a story technical specification contains file_path: ".claude/agents/test-agent.md" and no dual_path_sync block</given>
  <when>validate_dual_path() is invoked on the content</when>
  <then>a violation with type MISSING_DUAL_PATH_SYNC, severity HIGH, and remediation suggesting "src/claude/agents/test-agent.md" with dual_path_sync block is returned</then>
  <verification>
    <source_files>
      <file hint="validation function">src/claude/skills/devforgeai-story-creation/references/context-validation.md</file>
    </source_files>
    <test_file>tests/STORY-487/test_ac2_missing_sync.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Passes Stories With src/ Paths

```xml
<acceptance_criteria id="AC3">
  <given>a story technical specification contains file_path: "src/claude/agents/test-agent.md" and a dual_path_sync block</given>
  <when>validate_dual_path() is invoked on the content</when>
  <then>zero violations are returned</then>
  <verification>
    <source_files>
      <file hint="validation function">src/claude/skills/devforgeai-story-creation/references/context-validation.md</file>
    </source_files>
    <test_file>tests/STORY-487/test_ac3_passes_src.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: Exempts Non-Dual-Path Files

```xml
<acceptance_criteria id="AC4">
  <given>a story technical specification contains file_path: "devforgeai/specs/adrs/ADR-021.md" or "CLAUDE.md" or "tests/STORY-487/"</given>
  <when>validate_dual_path() is invoked on the content</when>
  <then>zero violations are returned (these paths are exempt from dual-path translation)</then>
  <verification>
    <source_files>
      <file hint="validation function">src/claude/skills/devforgeai-story-creation/references/context-validation.md</file>
    </source_files>
    <test_file>tests/STORY-487/test_ac4_exemptions.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#5: Graceful Skip When No Dual-Path Architecture

```xml
<acceptance_criteria id="AC5">
  <given>a project whose source-tree.md does not contain a "Dual-Location Architecture" section (greenfield project)</given>
  <when>validate_dual_path() is invoked</when>
  <then>the function returns an empty violations list without error (graceful skip)</then>
  <verification>
    <source_files>
      <file hint="validation function">src/claude/skills/devforgeai-story-creation/references/context-validation.md</file>
    </source_files>
    <test_file>tests/STORY-487/test_ac5_no_dual_path.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#6: /validate-stories Invokes validate_dual_path()

```xml
<acceptance_criteria id="AC6">
  <given>/validate-stories command Phase 2 invokes 6 validation functions</given>
  <when>Phase 2 validation loop is inspected after implementation</when>
  <then>validate_dual_path(tech_spec) is invoked as the 7th check, gated by context_status.source_tree, after validate_anti_patterns and before the results append</then>
  <verification>
    <source_files>
      <file hint="command file">src/claude/commands/validate-stories.md</file>
    </source_files>
    <test_file>tests/STORY-487/test_ac6_command_invocation.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree."
    source_paths:
      - "src/claude/skills/devforgeai-story-creation/references/context-validation.md"
      - "src/claude/commands/validate-stories.md"
    operational_paths:
      - ".claude/skills/devforgeai-story-creation/references/context-validation.md"
      - ".claude/commands/validate-stories.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "validate-dual-path-function"
      file_path: "src/claude/skills/devforgeai-story-creation/references/context-validation.md"
      required_keys:
        - key: "validate_dual_path function"
          type: "string"
          required: true
          validation: "Function exists after validate_anti_patterns"
          test_requirement: "Test: Grep for 'validate_dual_path' in context-validation.md"

    - type: "Configuration"
      name: "validate-stories-integration"
      file_path: "src/claude/commands/validate-stories.md"
      required_keys:
        - key: "validate_dual_path invocation"
          type: "string"
          required: true
          validation: "validate_dual_path(tech_spec) called in Phase 2"
          test_requirement: "Test: Grep for 'validate_dual_path' in validate-stories.md"

  business_rules:
    - id: "BR-001"
      rule: "validate_dual_path must check for Dual-Location Architecture section in source-tree.md before validating"
      trigger: "Function invocation"
      validation: "Returns empty list when section missing"
      error_handling: "Graceful skip (empty list)"
      test_requirement: "Test: Remove Dual-Location section, verify empty list"
      priority: "Critical"
    - id: "BR-002"
      rule: "Exempt paths must not trigger violations"
      trigger: "When file_path matches exempt_prefixes"
      validation: "devforgeai/specs/*, CLAUDE.md, README.md, tests/* are exempt"
      error_handling: "Skip exempt paths"
      test_requirement: "Test: ADR path returns no violations"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "validate_dual_path adds <1 second to validation"
      metric: "< 1 second per story"
      test_requirement: "Test: Time validation with and without dual-path check"
      priority: "Low"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- validate_dual_path() adds < 1 second per story validation
- Single Read() call to source-tree.md (may already be cached)

### Reliability
- Graceful skip when Dual-Location Architecture section missing
- No false positives on exempt paths

## Dependencies

### Prerequisite Stories
- None

### Technology Dependencies
- None — uses existing Markdown, Read, Grep

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+

**Test Scenarios:**
1. **Happy Path:** Story with .claude/ path, no dual_path_sync → violation detected
2. **Happy Path:** Story with src/ path and dual_path_sync → passes
3. **Edge Cases:**
   - Exempt paths (devforgeai/specs/, CLAUDE.md, tests/)
   - No Dual-Location Architecture section in source-tree.md
   - Multiple .claude/ paths in one story
   - Mixed .claude/ and src/ paths
4. **Error Cases:**
   - source-tree.md missing entirely (handled by caller's context_status check)

## Acceptance Criteria Verification Checklist

### AC#1: Function Exists
- [x] validate_dual_path() in context-validation.md - **Phase:** 3 - **Evidence:** Grep confirms function at line 340

### AC#2: Detects Missing Sync
- [x] MISSING_DUAL_PATH_SYNC violation returned - **Phase:** 2 - **Evidence:** test_ac2 passes

### AC#3: Passes src/ Paths
- [x] Zero violations for correct paths - **Phase:** 2 - **Evidence:** test_ac3 passes

### AC#4: Exemptions Work
- [x] Zero violations for exempt paths - **Phase:** 2 - **Evidence:** test_ac4 passes

### AC#5: Graceful Skip
- [x] Empty list when no Dual-Location section - **Phase:** 2 - **Evidence:** test_ac5 passes

### AC#6: Command Integration
- [x] validate_dual_path in validate-stories.md Phase 2 - **Phase:** 3 - **Evidence:** Grep confirms at line 232

**Checklist Progress:** 6/6 items complete (100%)

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Definition of Done

### Implementation
- [x] validate_dual_path() function added to context-validation.md after function #6
- [x] Function checks for Dual-Location Architecture section in source-tree.md
- [x] Function detects .claude/ paths without dual_path_sync
- [x] Function returns MISSING_DUAL_PATH_SYNC or OPERATIONAL_PATH_AS_TARGET violations
- [x] Exempt paths handled (devforgeai/specs/*, CLAUDE.md, tests/*)
- [x] /validate-stories Phase 2 invokes validate_dual_path()

### Dual-Path Sync
- [x] Files modified in src/claude/ (source of truth)
- [x] Files synced to .claude/ (operational)
- [x] Tests run against src/ tree

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered

### Testing
- [x] Detection test passes (.claude/ path → violation)
- [x] Pass-through test passes (src/ path → no violation)
- [x] Exemption test passes (ADR path → no violation)
- [x] Graceful skip test passes (no section → empty list)

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 02 Red | ✅ Complete | 6 test scripts, all fail (RED confirmed) |
| 03 Green | ✅ Complete | validate_dual_path() + validate-stories integration |
| 04 Refactor | ✅ Complete | Added src/ to exempt prefixes, code review applied |
| 05 Integration | ✅ Complete | Cross-file consistency + dual-path sync verified |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/devforgeai-story-creation/references/context-validation.md | Modified | +63 lines (function #7) |
| src/claude/commands/validate-stories.md | Modified | +1 line (invocation) |
| .claude/skills/devforgeai-story-creation/references/context-validation.md | Synced | operational copy |
| .claude/commands/validate-stories.md | Synced | operational copy |
| tests/STORY-487/test_ac1_function_exists.sh | Created | AC#1 tests |
| tests/STORY-487/test_ac2_detects_missing_sync_block.sh | Created | AC#2 tests |
| tests/STORY-487/test_ac3_passes_src_with_sync_block.sh | Created | AC#3 tests |
| tests/STORY-487/test_ac4_exempts_non_dual_path_files.sh | Created | AC#4 tests |
| tests/STORY-487/test_ac5_graceful_skip_no_dual_arch_section.sh | Created | AC#5 tests |
| tests/STORY-487/test_ac6_command_invocation.sh | Created | AC#6 tests |
| tests/STORY-487/run_all_tests.sh | Created | Test orchestrator |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] validate_dual_path() function added to context-validation.md after function #6 - Completed: Added as function #7 at line 340 with severity HIGH, graceful skip, exempt prefixes, and MISSING_DUAL_PATH_SYNC violation type
- [x] Function checks for Dual-Location Architecture section in source-tree.md - Completed: Early return with empty list when section not found
- [x] Function detects .claude/ paths without dual_path_sync - Completed: Returns MISSING_DUAL_PATH_SYNC violation with src/ equivalent suggestion
- [x] Function returns MISSING_DUAL_PATH_SYNC or OPERATIONAL_PATH_AS_TARGET violations - Completed: Returns MISSING_DUAL_PATH_SYNC and DUAL_PATH_SYNC_MISSING_SRC violation types
- [x] Exempt paths handled (devforgeai/specs/*, CLAUDE.md, tests/*) - Completed: 15 exempt prefixes including devforgeai/*, CLAUDE.md, tests/, docs/, src/, installer/
- [x] /validate-stories Phase 2 invokes validate_dual_path() - Completed: Added as 7th check at line 232, gated by context_status.source_tree
- [x] Files modified in src/claude/ (source of truth) - Completed: Both files edited in src/ tree
- [x] Files synced to .claude/ (operational) - Completed: cp from src/ to .claude/ operational paths
- [x] Tests run against src/ tree - Completed: All test scripts target src/ paths
- [x] All 6 acceptance criteria have passing tests - Completed: 6/6 ACs pass (run_all_tests.sh)
- [x] Edge cases covered - Completed: Exempt paths, graceful skip, dual_path_sync present/absent
- [x] Detection test passes (.claude/ path → violation) - Completed: test_ac2 passes
- [x] Pass-through test passes (src/ path → no violation) - Completed: test_ac3 passes
- [x] Exemption test passes (ADR path → no violation) - Completed: test_ac4 passes
- [x] Graceful skip test passes (no section → empty list) - Completed: test_ac5 passes

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | /create-stories-from-rca | Created | Story created from RCA-039 REC-1+REC-2 | STORY-487.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 0 violations | - |

## Notes

**Design Decisions:**
- REC-1 and REC-2 combined into single story because REC-2 is a single line that depends on REC-1 existing
- Function placed after validate_anti_patterns (function #6) to maintain numbering consistency
- Exempt paths prevent false positives on ADRs, stories, and root files that are single-path

**References:**
- [RCA-039](devforgeai/RCA/RCA-039-dual-path-architecture-validation-gap.md) (REC-1, REC-2)
- [RCA-033](devforgeai/RCA/RCA-033-story-creation-constitutional-non-conformance.md) (predecessor, same gap)
- [source-tree.md §Dual-Location Architecture](devforgeai/specs/context/source-tree.md) (constitutional rule)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
