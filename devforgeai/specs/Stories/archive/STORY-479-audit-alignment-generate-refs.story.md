---
id: STORY-479
title: /audit-alignment --generate-refs Integration
type: feature
epic: EPIC-082
sprint: Backlog
status: QA Approved
points: 2
depends_on: ["STORY-474", "STORY-478"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: /audit-alignment --generate-refs Integration

## Description

**As a** framework maintainer,
**I want** a `--generate-refs` flag on the existing `/audit-alignment` command that triggers on-demand regeneration of project-specific domain reference files when context files are updated,
**so that** domain references stay in sync with the source of truth (context files) without requiring a full `/create-context` re-run, and stale references are detected and removed.

## Provenance

```xml
<provenance>
  <origin document="ENH-CLAP-001" section="Part 3 - Domain Reference Generation">
    <quote>"Integration with /audit-alignment — --generate-refs flag enables on-demand regeneration"</quote>
    <line_reference>requirements spec FR-005</line_reference>
    <quantified_impact>On-demand domain reference regeneration keeps references in sync with updated context files</quantified_impact>
  </origin>
  <decision rationale="on-demand-regeneration-only">
    <selected>On-demand via /audit-alignment --generate-refs flag (locked decision DR-4)</selected>
    <rejected alternative="auto-trigger-on-context-change">Automatic regeneration on context file changes would create hidden side-effects on ADR acceptance</rejected>
    <trade_off>User must manually trigger regeneration after context file updates</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: --generate-refs Flag Triggers Regeneration

```xml
<acceptance_criteria id="AC1">
  <given>The /audit-alignment command exists at .claude/commands/audit-alignment.md (delivered by STORY-474)</given>
  <when>The command is invoked with --generate-refs flag</when>
  <then>The command invokes Phase 5.7 heuristic engine and template system (STORY-478) to regenerate project-*.md files in targeted subagent references/ directories</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac1_generate_refs_flag.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: --generate-refs Requires --fix Flag

```xml
<acceptance_criteria id="AC2">
  <given>The /audit-alignment command is invoked with --generate-refs but WITHOUT --fix</given>
  <when>The argument parsing phase executes</when>
  <then>Error message displayed: "--generate-refs requires --fix (regeneration is a fix action)" and execution halts without invoking regeneration</then>
  <verification>
    <source_files>
      <file hint="Argument validation">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac2_fix_required.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Regeneration Overwrites Existing Files

```xml
<acceptance_criteria id="AC3">
  <given>One or more project-*.md files already exist from a previous generation</given>
  <when>--generate-refs --fix is invoked</when>
  <then>Existing project-*.md files are overwritten with freshly generated content (not appended), auto-generation header contains current date and updated source file list</then>
  <verification>
    <source_files>
      <file hint="Overwrite behavior">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac3_overwrite.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: All 4 Heuristics Re-Evaluated

```xml
<acceptance_criteria id="AC4">
  <given>Context files have been updated since last domain reference generation</given>
  <when>--generate-refs --fix is invoked</when>
  <then>All 4 detection heuristics (DH-01 through DH-04) are re-evaluated against current context files, regardless of which heuristics triggered previously</then>
  <verification>
    <source_files>
      <file hint="Re-evaluation logic">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac4_re_evaluation.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#5: Stale File Removal with User Confirmation

```xml
<acceptance_criteria id="AC5">
  <given>A project-*.md file exists from a previous generation but its heuristic no longer triggers</given>
  <when>--generate-refs --fix is invoked</when>
  <then>The stale file is flagged and user prompted via AskUserQuestion with options: "Remove stale file" or "Keep file (manual override)" before deletion</then>
  <verification>
    <source_files>
      <file hint="Stale removal">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac5_stale_removal.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#6: Character Budget Compliance

```xml
<acceptance_criteria id="AC6">
  <given>The /audit-alignment command file includes --generate-refs handling</given>
  <when>The total file character count is measured</when>
  <then>The file remains within the 10,000 character budget established by STORY-474 AC#2</then>
  <verification>
    <source_files>
      <file hint="Character count">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac6_character_budget.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#7: Lean Orchestration Pattern Compliance

```xml
<acceptance_criteria id="AC7">
  <given>The --generate-refs logic is added to the command</given>
  <when>The command structure is inspected</when>
  <then>--generate-refs handling follows lean orchestration: argument validation and context markers in command, all regeneration logic (heuristic evaluation, template population, file generation) delegated to subagent/skill via Task()</then>
  <verification>
    <source_files>
      <file hint="Command structure">.claude/commands/audit-alignment.md</file>
      <file hint="Lean pattern">devforgeai/protocols/lean-orchestration-pattern.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac7_lean_orchestration.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#8: Cross-Epic Additive Modification

```xml
<acceptance_criteria id="AC8">
  <given>The /audit-alignment command was created in EPIC-081 (STORY-474)</given>
  <when>The --generate-refs flag handling is added</when>
  <then>Modification is additive only (no removal of STORY-474 functionality), argument-hint frontmatter updated to document new flag, Quick Reference includes --generate-refs usage example</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-479/test_ac8_additive_modification.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree. Files are modified in src/claude/ and synced to .claude/ operational folders."
    source_paths:
      - "src/claude/commands/audit-alignment.md"
    operational_paths:
      - ".claude/commands/audit-alignment.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "audit-alignment-generate-refs"
      file_path: "src/claude/commands/audit-alignment.md"
      required_keys:
        - key: "--generate-refs flag"
          type: "string"
          required: true
          validation: "Boolean flag parsed in argument validation section"
          test_requirement: "Test: Grep for '--generate-refs' in command file"
        - key: "--fix co-requirement"
          type: "string"
          required: true
          validation: "--generate-refs requires --fix to be present"
          test_requirement: "Test: Grep for 'requires --fix' validation logic"
        - key: "argument-hint update"
          type: "string"
          required: true
          validation: "argument-hint frontmatter includes --generate-refs"
          test_requirement: "Test: Grep argument-hint field for '--generate-refs'"
        - key: "Task() delegation"
          type: "string"
          required: true
          validation: "Regeneration logic delegated via Task() invocation"
          test_requirement: "Test: Grep for Task() call in --generate-refs section"

  business_rules:
    - id: "BR-001"
      rule: "--generate-refs requires --fix flag (regeneration is a fix action)"
      trigger: "When --generate-refs parsed in argument validation"
      validation: "Error displayed if --fix absent when --generate-refs present"
      error_handling: "HALT with error message, no regeneration invoked"
      test_requirement: "Test: Invoke with --generate-refs without --fix, verify error"
      priority: "Critical"
    - id: "BR-002"
      rule: "Stale file removal requires user confirmation via AskUserQuestion"
      trigger: "When heuristic no longer triggers but project-*.md exists"
      validation: "AskUserQuestion invoked before any file deletion"
      error_handling: "Skip deletion if user selects 'Keep file'"
      test_requirement: "Test: Stale file detected, AskUserQuestion shown before deletion"
      priority: "Critical"
    - id: "BR-003"
      rule: "Character budget must not exceed 10,000 characters after modification"
      trigger: "Story completion / pre-commit"
      validation: "wc -c <= 10,000"
      error_handling: "Extract logic to reference file or subagent to reduce size"
      test_requirement: "Test: wc -c audit-alignment.md <= 10000"
      priority: "High"
    - id: "BR-004"
      rule: "Modification must be additive only (no STORY-474 functionality removed)"
      trigger: "During implementation"
      validation: "All 8 STORY-474 ACs continue to pass after modification"
      error_handling: "Revert changes that break existing functionality"
      test_requirement: "Test: Run STORY-474 test suite after modification, all pass"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Argument parsing overhead for --generate-refs under 500ms"
      metric: "< 500ms additional parsing time"
      test_requirement: "Test: Time argument parsing with and without --generate-refs"
      priority: "Low"
    - id: "NFR-002"
      category: "Security"
      requirement: "Zero silent file deletions"
      metric: "0 deletions without AskUserQuestion confirmation"
      test_requirement: "Test: Every deletion preceded by AskUserQuestion"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- Argument parsing overhead: < 500ms additional
- Command-level orchestration overhead: < 2 seconds
- Stale file detection: < 1 second
- Full --generate-refs --fix execution: < 120 seconds

### Security
- Zero silent file deletions (AskUserQuestion required)
- Zero file writes without --fix flag
- Read-only context file access during heuristic evaluation
- No secrets in generated output

### Reliability
- Graceful degradation when STORY-478 deliverables unavailable
- Idempotent regeneration (same input = same output)
- Existing STORY-474 functionality unaffected
- AskUserQuestion cancellation does not abort entire workflow

### Scalability
- Supports 4 target agent directories without command modification
- Future heuristic additions require only engine updates (not command changes)
- Character budget provides 33% headroom below 15K hard limit

## Dependencies

### Prerequisite Stories
- [ ] **STORY-478:** Phase 5.7 Domain Reference Generation Workflow
  - **Why:** Provides heuristic engine and template that --generate-refs invokes
  - **Status:** Backlog
- [ ] **STORY-474:** /audit-alignment Command (EPIC-081)
  - **Why:** Base command that this story extends with --generate-refs flag
  - **Status:** Backlog

### Technology Dependencies
- None

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+ for argument parsing and delegation logic

**Test Scenarios:**
1. **Happy Path:** --generate-refs --fix invokes regeneration, files updated
2. **Edge Cases:**
   - No existing project-*.md files (first-time generation)
   - All heuristics no longer trigger (flag all for removal)
   - Partial trigger change (some regenerate, some flagged for removal)
   - Context files missing (halt with clear error)
   - Command at character budget ceiling
   - STORY-478 deliverables unavailable (graceful error)
3. **Error Cases:**
   - --generate-refs without --fix (error and halt)

## Acceptance Criteria Verification Checklist

### AC#1: Flag Behavior
- [x] --generate-refs triggers regeneration - **Phase:** 3

### AC#2: --fix Dependency
- [x] Error when --fix missing - **Phase:** 2

### AC#3: Overwrite
- [x] Existing files overwritten with fresh content - **Phase:** 2

### AC#4: Re-Evaluation
- [x] All 4 heuristics re-evaluated - **Phase:** 2

### AC#5: Stale Removal
- [x] AskUserQuestion before deletion - **Phase:** 2

### AC#6: Character Budget
- [x] wc -c <= 10,000 (actual: 9,977) - **Phase:** 3

### AC#7: Lean Orchestration
- [x] Delegation via Task() - **Phase:** 3

### AC#8: Additive Modification
- [x] STORY-474 ACs still pass - **Phase:** 3

**Checklist Progress:** 8/8 items complete (100%)

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Definition of Done

### Implementation
- [x] --generate-refs flag parsed in argument validation section
- [x] --fix co-requirement validated (error if missing)
- [x] Regeneration delegated via Task() to Phase 5.7 engine
- [x] Stale file detection via Glob for existing project-*.md
- [x] AskUserQuestion for stale file removal confirmation
- [x] argument-hint frontmatter updated with --generate-refs
- [x] Quick Reference section includes --generate-refs example

### Quality
- [x] All 8 acceptance criteria have passing tests
- [x] Character budget <= 10,000 characters
- [x] STORY-474 test suite passes after modification
- [x] Lean orchestration pattern compliance verified

### Testing
- [x] --fix dependency test passes
- [x] Stale file removal test passes
- [x] Character budget test passes
- [x] STORY-474 regression tests pass

### Dual-Path Sync
- [x] Command modified in src/claude/commands/ (source of truth)
- [x] File synced to .claude/commands/ (operational)
- [x] Tests run against src/ tree

### Documentation
- [x] Cross-epic dependency documented in Notes section

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Red | ✅ Complete | 8 test scripts, 23 assertions |
| Green | ✅ Complete | 4 edits to audit-alignment.md |
| Refactor | ✅ Complete | No changes needed |
| Integration | ✅ Complete | Dual-path sync, STORY-474 regression |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/commands/audit-alignment.md | Modified | +35 lines |
| .claude/commands/audit-alignment.md | Synced | Mirror of src/ |
| tests/STORY-479/test_ac1_generate_refs_flag.sh | Created | 34 lines |
| tests/STORY-479/test_ac2_fix_required.sh | Created | 34 lines |
| tests/STORY-479/test_ac3_overwrite.sh | Created | 34 lines |
| tests/STORY-479/test_ac4_re_evaluation.sh | Created | 35 lines |
| tests/STORY-479/test_ac5_stale_removal.sh | Created | 40 lines |
| tests/STORY-479/test_ac6_character_budget.sh | Created | 34 lines |
| tests/STORY-479/test_ac7_lean_orchestration.sh | Created | 34 lines |
| tests/STORY-479/test_ac8_additive_modification.sh | Created | 50 lines |
| tests/STORY-479/run_all_tests.sh | Created | 30 lines |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] --generate-refs flag parsed in argument validation section - Completed: Added to Phase 0 argument parsing with default false
- [x] --fix co-requirement validated (error if missing) - Completed: IF block at line 33-35 with error message and HALT
- [x] Regeneration delegated via Task() to Phase 5.7 engine - Completed: Phase 3.5 delegates via Task(subagent_type="general-purpose")
- [x] Stale file detection via Glob for existing project-*.md - Completed: Delegated in Task() prompt requirement #3
- [x] AskUserQuestion for stale file removal confirmation - Completed: Specified in Task() prompt with Remove/Keep options
- [x] argument-hint frontmatter updated with --generate-refs - Completed: Added [--generate-refs] to line 3
- [x] Quick Reference section includes --generate-refs example - Completed: Added line 20 with --fix --generate-refs usage
- [x] All 8 acceptance criteria have passing tests - Completed: 8/8 test scripts pass (23 assertions)
- [x] Character budget <= 10,000 characters - Completed: 9,977 chars (23 char headroom)
- [x] STORY-474 test suite passes after modification - Completed: All 8 STORY-474 AC tests pass
- [x] Lean orchestration pattern compliance verified - Completed: Arg parsing in command, all logic via Task()
- [x] --fix dependency test passes - Completed: test_ac2_fix_required.sh 3/3 pass
- [x] Stale file removal test passes - Completed: test_ac5_stale_removal.sh 3/3 pass
- [x] Character budget test passes - Completed: test_ac6_character_budget.sh 2/2 pass
- [x] STORY-474 regression tests pass - Completed: Verified via integration-tester subagent
- [x] Command modified in src/claude/commands/ (source of truth) - Completed: All edits in src/claude/commands/audit-alignment.md
- [x] File synced to .claude/commands/ (operational) - Completed: cp from src/ to .claude/
- [x] Tests run against src/ tree - Completed: All test scripts reference src/claude/commands/
- [x] Cross-epic dependency documented in Notes section - Completed: Already documented in story Notes section

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from EPIC-082 Feature 4 (batch 3/3) | STORY-479.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 8/8 ACs, 23/23 tests, 0 violations | - |

## Notes

**Design Decisions:**
- --generate-refs requires --fix because regeneration modifies files (consistent with EPIC-081 mutability rules)
- On-demand regeneration only (locked decision DR-4) — no auto-trigger on context changes
- Lean orchestration: command handles arg parsing only, delegates all logic to subagent/skill
- Stale file removal requires explicit user confirmation (zero silent deletions)

**Cross-Epic Dependency:**
- This story modifies .claude/commands/audit-alignment.md which is created by STORY-474 (EPIC-081)
- Modification is strictly additive — no existing STORY-474 functionality removed or restructured
- STORY-474's 10,000 character budget must be maintained after adding --generate-refs handling

**Edge Cases Documented:**
1. No existing project-*.md files (first-time generation)
2. All heuristics no longer trigger (flag all files for removal)
3. Partial trigger change (regenerate some, flag others)
4. Context files missing (halt with clear error)
5. Command at character budget ceiling (extract to reference file)
6. STORY-478 deliverables unavailable (graceful error message)

**References:**
- [Requirements Specification](devforgeai/specs/requirements/domain-reference-generation-requirements.md) (FR-005)
- [STORY-474](devforgeai/specs/Stories/STORY-474-audit-alignment-command.story.md) (base command)
- [EPIC-082](devforgeai/specs/Epics/EPIC-082-domain-reference-generation.epic.md)
- [Lean Orchestration Pattern](devforgeai/protocols/lean-orchestration-pattern.md)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
