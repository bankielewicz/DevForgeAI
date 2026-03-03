---
id: STORY-410
title: Create Automated Audit for Command/Skill Hybrid Violations
type: feature
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-14
format_version: "2.9"
source_rca: RCA-038
source_recommendation: REC-4
---

# Story: Create Automated Audit for Command/Skill Hybrid Violations

## Description

**As a** DevForgeAI framework maintainer,
**I want** an automated audit script that detects commands with excessive code blocks before Skill() invocation,
**so that** hybrid command/skill violations are systematically identified before they cause workflow problems.

**Background:** RCA-038 identified that commands with extensive code blocks before Skill() invocation cause Claude to execute manual workflow steps instead of delegating to skills immediately. This script will detect such hybrid violations to enable proactive remediation.

## Provenance

```xml
<provenance>
  <origin document="RCA-038" section="REC-4">
    <quote>"Create Automated Audit for Command/Skill Hybrid Violations - Need systematic detection of commands that document skill work"</quote>
    <line_reference>lines 398-436</line_reference>
    <quantified_impact>Prevents recurrence of skill bypass pattern documented in RCA-037 and RCA-038</quantified_impact>
  </origin>

  <decision rationale="bash-script-over-python">
    <selected>Bash script for simplicity and minimal dependencies</selected>
    <rejected alternative="Python script">
      Python would add dependency; bash is sufficient for line-based analysis
    </rejected>
    <trade_off>Less robust error handling but simpler deployment</trade_off>
  </decision>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Script Locates All Command Files

```xml
<acceptance_criteria id="AC1">
  <given>The audit script is executed from project root</given>
  <when>It scans the .claude/commands/ directory</when>
  <then>All .md files are identified for analysis</then>
  <verification>
    <source_files>
      <file hint="Audit script">.claude/scripts/audit-command-skill-overlap.sh</file>
    </source_files>
    <test_file>tests/STORY-410/test_ac1_locate_commands.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Script Counts Code Blocks Before Skill Invocation

```xml
<acceptance_criteria id="AC2">
  <given>A command file contains Skill() invocations</given>
  <when>The script analyzes the file</when>
  <then>It counts code blocks (```) appearing before the first Skill() call</then>
  <verification>
    <source_files>
      <file hint="Audit script">.claude/scripts/audit-command-skill-overlap.sh</file>
    </source_files>
    <test_file>tests/STORY-410/test_ac2_code_block_counting.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Script Flags Violations Based on Threshold

```xml
<acceptance_criteria id="AC3">
  <given>A command file has >4 code blocks before Skill() invocation</given>
  <when>The script completes analysis</when>
  <then>The file is flagged as a potential hybrid violation with ❌ marker</then>
  <verification>
    <source_files>
      <file hint="Audit script">.claude/scripts/audit-command-skill-overlap.sh</file>
    </source_files>
    <test_file>tests/STORY-410/test_ac3_violation_flagging.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Script Reports Clean Commands

```xml
<acceptance_criteria id="AC4">
  <given>A command file has ≤4 code blocks before Skill() invocation</given>
  <when>The script completes analysis</when>
  <then>The file is marked as clean with ✅ marker and code block count</then>
  <verification>
    <source_files>
      <file hint="Audit script">.claude/scripts/audit-command-skill-overlap.sh</file>
    </source_files>
    <test_file>tests/STORY-410/test_ac4_clean_reporting.py</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Script Handles Commands Without Skill Invocations

```xml
<acceptance_criteria id="AC5">
  <given>A command file contains no Skill() invocations</given>
  <when>The script analyzes the file</when>
  <then>It reports a warning ⚠️ "No Skill() invocation found"</then>
  <verification>
    <source_files>
      <file hint="Audit script">.claude/scripts/audit-command-skill-overlap.sh</file>
    </source_files>
    <test_file>tests/STORY-410/test_ac5_no_skill_warning.py</test_file>
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
      name: "audit-command-skill-overlap.sh"
      file_path: ".claude/scripts/audit-command-skill-overlap.sh"
      required_keys:
        - key: "COMMANDS_DIR"
          type: "string"
          example: ".claude/commands"
          required: true
          test_requirement: "Test: Verify script finds commands directory"
        - key: "CODE_BLOCK_THRESHOLD"
          type: "int"
          example: "4"
          required: true
          default: "4"
          test_requirement: "Test: Verify threshold is configurable"

    - type: "Service"
      name: "CommandAuditScript"
      file_path: ".claude/scripts/audit-command-skill-overlap.sh"
      interface: "Bash Script"
      lifecycle: "On-demand execution"
      dependencies:
        - "grep"
        - "head"
        - "cut"
      requirements:
        - id: "SVC-001"
          description: "Iterate over all .md files in commands directory"
          testable: true
          test_requirement: "Test: Script processes all command files"
          priority: "Critical"
        - id: "SVC-002"
          description: "Find first line containing Skill(command= pattern"
          testable: true
          test_requirement: "Test: Skill() pattern detection works"
          priority: "Critical"
        - id: "SVC-003"
          description: "Count triple backticks before Skill() line"
          testable: true
          test_requirement: "Test: Code block counting accurate"
          priority: "Critical"
        - id: "SVC-004"
          description: "Output categorized results with emoji indicators"
          testable: true
          test_requirement: "Test: Output format matches specification"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Code block threshold for violation is >4 blocks"
      trigger: "When analyzing code block count"
      validation: "count > 4 triggers violation flag"
      error_handling: "N/A - informational output"
      test_requirement: "Test: Threshold boundary (4 vs 5 blocks)"
      priority: "Critical"
    - id: "BR-002"
      rule: "Commands without Skill() get warning, not error"
      trigger: "When no Skill() pattern found in file"
      validation: "Missing Skill() is a warning, not a blocking violation"
      error_handling: "Output warning and continue to next file"
      test_requirement: "Test: No-skill commands get ⚠️ not ❌"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Complete audit of all commands within 5 seconds"
      metric: "<5 seconds for 30 command files"
      test_requirement: "Test: Time audit execution"
      priority: "Medium"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "Handle files with unusual formatting gracefully"
      metric: "No crashes on malformed files"
      test_requirement: "Test: Script handles edge cases without error exit"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Execution Time:**
- Complete audit of all commands (30+ files) in <5 seconds

### Reliability

**Error Handling:**
- Continue processing even if individual files have issues
- No crashes on malformed markdown files

---

## Dependencies

### Prerequisite Stories

None - this is a standalone utility story.

### Technology Dependencies

- Bash (standard Unix tools: grep, head, cut, wc)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for script logic

**Test Scenarios:**
1. **Happy Path:** Commands with clean Skill() invocation
2. **Edge Cases:**
   - Command with no code blocks
   - Command with code blocks but no Skill()
   - Command with Skill() on first line
3. **Error Cases:**
   - Empty file
   - Malformed markdown

---

## Acceptance Criteria Verification Checklist

### AC#1: Script Locates All Command Files

- [x] Script finds .claude/commands/ directory - **Phase:** 2 - **Evidence:** test_ac1 (tests/STORY-410/test_ac1_locate_commands.py)
- [x] All .md files enumerated - **Phase:** 2 - **Evidence:** test_ac1 (4 tests written, RED confirmed)

### AC#2: Script Counts Code Blocks Before Skill Invocation

- [x] Triple backtick pattern detected - **Phase:** 2 - **Evidence:** test_ac2 (tests/STORY-410/test_ac2_code_block_counting.py)
- [x] Count stops at first Skill() line - **Phase:** 2 - **Evidence:** test_ac2 (4 tests written, RED confirmed)

### AC#3: Script Flags Violations Based on Threshold

- [x] Threshold of 4 applied - **Phase:** 2 - **Evidence:** test_ac3 (tests/STORY-410/test_ac3_violation_flagging.py)
- [x] ❌ marker output for violations - **Phase:** 2 - **Evidence:** test_ac3 (4 tests written, RED confirmed)

### AC#4: Script Reports Clean Commands

- [x] ✅ marker for clean commands - **Phase:** 2 - **Evidence:** test_ac4 (tests/STORY-410/test_ac4_clean_reporting.py)
- [x] Code block count shown - **Phase:** 2 - **Evidence:** test_ac4 (4 tests written, RED confirmed)

### AC#5: Script Handles Commands Without Skill Invocations

- [x] ⚠️ warning for no Skill() - **Phase:** 2 - **Evidence:** test_ac5 (tests/STORY-410/test_ac5_no_skill_warning.py, 4 tests written, RED confirmed)

---

**Checklist Progress:** 9/9 items complete (100%) - Tests written, awaiting implementation (Phase 03)

---

## Definition of Done

### Implementation
- [x] Audit script created at .claude/scripts/audit-command-skill-overlap.sh
- [x] Script iterates over all command files
- [x] Script detects Skill() invocation line
- [x] Script counts code blocks before Skill()
- [x] Script outputs categorized results with emoji indicators

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Edge cases covered (no Skill, empty files, malformed content)
- [x] Threshold boundary tested (4 vs 5 code blocks)

### Testing
- [x] Unit tests for pattern detection
- [x] Unit tests for code block counting
- [x] Integration test for full audit workflow

### Documentation
- [x] Script usage documented in header comments
- [x] RCA-038 updated with story link

---

## Implementation Notes

- [x] Audit script created at .claude/scripts/audit-command-skill-overlap.sh - Completed: 67-line Bash script with strict mode, directory validation, and proper exit codes
- [x] Script iterates over all command files - Completed: Uses COMMANDS_DIR env var with nullglob for empty directory handling
- [x] Script detects Skill() invocation line - Completed: grep -n "Skill(command=" pattern with head -1
- [x] Script counts code blocks before Skill() - Completed: head + grep -c counts backtick lines (threshold 8 = 4 blocks)
- [x] Script outputs categorized results with emoji indicators - Completed: Cross-mark for violations, check-mark for clean, warning for no Skill()
- [x] All 5 acceptance criteria have passing tests - Completed: 22 tests across 5 test files, all passing
- [x] Edge cases covered (no Skill, empty files, malformed content) - Completed: test_ac5 covers no Skill, test_ac1 covers empty directory, error handling with 2>/dev/null
- [x] Threshold boundary tested (4 vs 5 code blocks) - Completed: test_ac3_threshold_boundary_4_is_clean and test_ac3_threshold_boundary_5_is_violation
- [x] Unit tests for pattern detection - Completed: test_ac2 and test_ac5 cover Skill() pattern and backtick pattern detection
- [x] Unit tests for code block counting - Completed: test_ac2 with 4 tests for counting logic
- [x] Integration test for full audit workflow - Completed: test_ac1_exit_code_1_when_violations_present and test_ac1_nonexistent_directory_returns_error
- [x] Script usage documented in header comments - Completed: Lines 1-16 document usage, purpose, threshold, and exit codes
- [x] RCA-038 updated with story link - Completed: RCA-038 line 399 already contains "Implemented in: STORY-410"

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-16

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | Complete | 20 failing tests generated across 5 test files |
| Phase 03 (Green) | Complete | Script implemented, all 20 tests passing |
| Phase 04 (Refactor) | Complete | Code review fixes applied (exit codes, input validation, strict mode) |
| Phase 05 (Integration) | Complete | 2 integration tests added, 22 total tests passing |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| .claude/scripts/audit-command-skill-overlap.sh | Created | 67 |
| tests/STORY-410/conftest.py | Created | 46 |
| tests/STORY-410/test_ac1_locate_commands.py | Created | 82 |
| tests/STORY-410/test_ac2_code_block_counting.py | Created | 71 |
| tests/STORY-410/test_ac3_violation_flagging.py | Created | 71 |
| tests/STORY-410/test_ac4_clean_reporting.py | Created | 61 |
| tests/STORY-410/test_ac5_no_skill_warning.py | Created | 61 |
| tests/STORY-410/fixtures/*.md | Created | 5 fixture files |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-14 | .claude/skills/devforgeai-story-creation | Created | Story created from RCA-038 REC-4 | STORY-410.story.md |
| 2026-02-16 | .claude/qa-result-interpreter | QA Deep | PASSED: 22/22 tests, 0 violations, 3/3 validators | - |

---

## Notes

**Source RCA:** RCA-038 - Skill Invocation Bypass Recurrence Post-RCA-037

**Script Logic (from RCA-038):**
```bash
#!/bin/bash
# Audit commands for potential lean orchestration violations

for cmd in .claude/commands/*.md; do
  # Count lines between command start and Skill() invocation
  first_skill_line=$(grep -n "Skill(command=" "$cmd" | head -1 | cut -d: -f1)

  if [ -z "$first_skill_line" ]; then
    echo "⚠️ $cmd: No Skill() invocation found"
    continue
  fi

  # Count code blocks before Skill()
  code_blocks=$(head -n "$first_skill_line" "$cmd" | grep -c '```')

  if [ "$code_blocks" -gt 4 ]; then
    echo "❌ $cmd: $code_blocks code blocks before Skill() - potential hybrid violation"
  else
    echo "✅ $cmd: Clean ($code_blocks code blocks before Skill())"
  fi
done
```

**Related RCAs:**
- RCA-037: Skill Invocation Skipped Despite Orchestrator Instructions
- RCA-038: Skill Invocation Bypass Recurrence Post-RCA-037

---

Story Template Version: 2.9
Last Updated: 2026-02-14
