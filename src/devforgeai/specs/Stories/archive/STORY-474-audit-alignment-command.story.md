---
id: STORY-474
title: /audit-alignment Command
type: feature
epic: EPIC-081
sprint: Backlog
status: QA Approved
points: 3
depends_on: ["STORY-472", "STORY-473"]
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-02-22
format_version: "2.9"
---

# Story: /audit-alignment Command

## Description

**As a** framework maintainer,
**I want** an on-demand `/audit-alignment` slash command that validates configuration layer alignment with layer filtering and fix proposals,
**so that** I can detect contradictions, gaps, and ADR drift between CLAUDE.md, system prompt, context files, rules, and ADRs at any time and resolve drift before it causes incorrect AI behavior.

## Provenance

```xml
<provenance>
  <origin document="ENH-CLAP-001" section="solution-overview">
    <quote>"/audit-alignment command — User-facing entry point for on-demand auditing with layer filtering and fix proposals"</quote>
    <line_reference>requirements spec line 57</line_reference>
    <quantified_impact>On-demand configuration drift detection for framework maintainers</quantified_impact>
  </origin>
  <decision rationale="lean-orchestration-pattern">
    <selected>Lean orchestration command: validate args, set markers, invoke alignment-auditor subagent via Task()</selected>
    <rejected alternative="inline-validation-logic">Embedding validation logic in the command would violate lean orchestration protocol and waste context window tokens</rejected>
    <trade_off>Command depends on alignment-auditor subagent (STORY-473) existing</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Lean Orchestration Pattern Compliance

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>The /audit-alignment command file exists at .claude/commands/audit-alignment.md</given>
  <when>the command structure is inspected</when>
  <then>the command follows the lean orchestration pattern: validate arguments, set context markers, invoke alignment-auditor subagent via Task(), format results, conditionally propose fixes, conditionally write report, display summary — with no business logic (validation algorithms, comparison logic) embedded in the command</then>
  <verification>
    <source_files>
      <file hint="Command under test">.claude/commands/audit-alignment.md</file>
      <file hint="Lean orchestration pattern reference">devforgeai/protocols/lean-orchestration-pattern.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac1_lean_orchestration.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: Character Budget Compliance

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>The /audit-alignment command file exists at .claude/commands/audit-alignment.md</given>
  <when>the file character count is measured</when>
  <then>the total character count is ≤ 10,000 characters (67% of 15,000 hard limit)</then>
  <verification>
    <source_files>
      <file hint="Command file">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac2_character_budget.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: --layer Argument with 6 Valid Values

```xml
<acceptance_criteria id="AC3" implements="COMP-001">
  <given>The /audit-alignment command is invoked</given>
  <when>the --layer argument is parsed</when>
  <then>the command accepts exactly: all (default), claudemd, prompt, context, rules, adrs — and passes the selected layer as context to the alignment-auditor subagent</then>
  <verification>
    <source_files>
      <file hint="Argument parsing">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac3_layer_argument.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#4: --fix Argument with Mutability Enforcement

```xml
<acceptance_criteria id="AC4" implements="COMP-001">
  <given>The /audit-alignment command is invoked with --fix flag</given>
  <when>findings are returned from alignment-auditor</when>
  <then>mutability rules enforced: CLAUDE.md — propose edits via AskUserQuestion; system-prompt-core.md — propose additions via AskUserQuestion; Context files (6) — flag for ADR creation only, never edit; Rules — propose edits via AskUserQuestion; ADRs — recommend new ADR only, never edit existing</then>
  <verification>
    <source_files>
      <file hint="Fix workflow">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac4_fix_mutability.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#5: --output Argument with Console and File Modes

```xml
<acceptance_criteria id="AC5" implements="COMP-001">
  <given>The /audit-alignment command is invoked</given>
  <when>the --output argument is parsed</when>
  <then>accepts: console (default) displaying to terminal only, and file writing markdown report to devforgeai/qa/alignment-audit-{YYYY-MM-DD}.md AND displaying to terminal</then>
  <verification>
    <source_files>
      <file hint="Output handling">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac5_output_argument.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#6: Invokes alignment-auditor via Task()

```xml
<acceptance_criteria id="AC6" implements="COMP-001">
  <given>Arguments parsed and context markers set</given>
  <when>the subagent invocation phase executes</when>
  <then>the command invokes Task(subagent_type="alignment-auditor", ...) passing the --layer value and returning structured findings with severity, layers, line numbers, and resolutions</then>
  <verification>
    <source_files>
      <file hint="Task() invocation">.claude/commands/audit-alignment.md</file>
      <file hint="Subagent">.claude/agents/alignment-auditor.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac6_subagent_invocation.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#7: Severity-Based Display Formatting

```xml
<acceptance_criteria id="AC7" implements="COMP-001">
  <given>The alignment-auditor returns findings</given>
  <when>the command formats results</when>
  <then>findings grouped by severity in descending order: CRITICAL, HIGH, MEDIUM, LOW — each showing check ID, severity badge, layer A vs B, description, and line numbers</then>
  <verification>
    <source_files>
      <file hint="Display formatting">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac7_severity_display.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#8: Executive Summary Table

```xml
<acceptance_criteria id="AC8" implements="COMP-001">
  <given>The alignment-auditor returns findings</given>
  <when>the command displays the summary</when>
  <then>executive summary table shows: contradiction count per severity, gap count per severity, ADR drift count, total findings, and overall status (PASS/WARN/FAIL)</then>
  <verification>
    <source_files>
      <file hint="Summary generation">.claude/commands/audit-alignment.md</file>
    </source_files>
    <test_file>tests/STORY-474/test_ac8_executive_summary.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  dual_path_sync:
    note: "Per source-tree.md dual-path architecture, development happens in src/ tree. Files are created in src/claude/ and synced to .claude/ operational folders."
    source_paths:
      - "src/claude/commands/audit-alignment.md"
    operational_paths:
      - ".claude/commands/audit-alignment.md"
    test_against: "src/"

  components:
    - type: "Configuration"
      name: "audit-alignment"
      file_path: "src/claude/commands/audit-alignment.md"
      required_keys:
        - key: "description"
          type: "string"
          example: "Validate configuration layer alignment across CLAUDE.md, system prompt, context files, rules, and ADRs"
          required: true
          validation: "Non-empty string"
          test_requirement: "Test: frontmatter has description field"
        - key: "argument-hint"
          type: "string"
          example: "[--layer=all|claudemd|prompt|context|rules|adrs] [--fix] [--output=console|file]"
          required: true
          validation: "Documents all 3 arguments"
          test_requirement: "Test: argument-hint contains --layer, --fix, --output"
        - key: "model"
          type: "string"
          example: "opus"
          required: true
          validation: "Must be 'opus'"
          test_requirement: "Test: frontmatter model is opus"
        - key: "allowed-tools"
          type: "array"
          example: "[Read, Glob, Grep, Task, AskUserQuestion, Edit, Write]"
          required: true
          validation: "Contains required tools"
          test_requirement: "Test: allowed-tools includes Task and AskUserQuestion"

  business_rules:
    - id: "BR-001"
      rule: "Command must follow lean orchestration: no business logic before Task() invocation"
      trigger: "Command structure review"
      validation: "No validation algorithms, comparison logic, or data processing before Task()"
      error_handling: "Restructure command to delegate all analysis to alignment-auditor"
      test_requirement: "Test: Count code blocks before Skill/Task invocation ≤ 4"
      priority: "Critical"
    - id: "BR-002"
      rule: "--fix must never edit IMMUTABLE context files"
      trigger: "When --fix flag is active and finding targets context file"
      validation: "Fix workflow proposes ADR creation for context file findings, never Edit()"
      error_handling: "Skip edit proposal, display ADR recommendation instead"
      test_requirement: "Test: --fix with context file finding → ADR recommendation, not Edit()"
      priority: "Critical"
    - id: "BR-003"
      rule: "Character budget must not exceed 10,000"
      trigger: "Story completion / pre-commit"
      validation: "wc -c ≤ 10,000"
      error_handling: "Trim verbose sections, move detail to reference files"
      test_requirement: "Test: wc -c audit-alignment.md ≤ 10000"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Command overhead excluding subagent: < 5 seconds"
      metric: "< 5 seconds for argument parsing + formatting + summary"
      test_requirement: "Test: Time command overhead without subagent execution"
      priority: "Medium"
    - id: "NFR-002"
      category: "Security"
      requirement: "Zero silent edits — every fix requires AskUserQuestion approval"
      metric: "0 Edit() calls without prior AskUserQuestion"
      test_requirement: "Test: Every Edit() call preceded by AskUserQuestion in --fix workflow"
      priority: "Critical"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements

### Performance
- Argument parsing and context markers: < 2 seconds
- Total command overhead (excluding subagent): < 5 seconds
- Report file write: < 1 second for reports up to 500 lines

### Security
- Read-only by default (zero file modifications without --fix)
- Every --fix edit requires AskUserQuestion approval
- IMMUTABLE context files never modified regardless of --fix
- No secrets extracted into report output

### Reliability
- Graceful degradation when alignment-auditor unavailable
- Missing optional files don't cause failure
- All 6 context files must exist or command halts
- Deterministic output for identical project state

### Scalability
- Supports up to 50 ADR files without degradation
- Character budget (10K) provides 33% headroom below 15K limit
- Report file < 200KB for up to 100 findings

## Dependencies

### Prerequisite Stories
- [ ] **STORY-472:** ADR-021 Decision Record
  - **Why:** Authorizes audit-alignment.md in source-tree.md
  - **Status:** Backlog
- [ ] **STORY-473:** alignment-auditor Subagent
  - **Why:** Command invokes alignment-auditor via Task()
  - **Status:** Backlog

### Technology Dependencies
- None — uses existing Claude Code tools

## Test Strategy

### Unit Tests
**Coverage Target:** 95%+ for argument parsing and display formatting

**Test Scenarios:**
1. **Happy Path:** Full audit with all layers, findings displayed by severity, summary table rendered
2. **Edge Cases:**
   - alignment-auditor not created yet → clear error message
   - system-prompt-core.md doesn't exist → subagent handles gracefully
   - No findings (fully aligned) → PASS with zero counts
   - --fix with IMMUTABLE finding → ADR recommendation only
   - --output=file with existing same-day report → overwrite
   - --layer=adrs with no ADR files → PASS with skip note
3. **Error Cases:**
   - Invalid --layer value → AskUserQuestion with valid options
   - alignment-auditor Task() fails → error display, no inline fallback

## Acceptance Criteria Verification Checklist

### AC#1: Lean Orchestration
- [x] No business logic before Task() invocation - **Phase:** 3 - **Evidence:** Command structure verified, 3 code blocks before Task()
- [x] Follows validate → markers → invoke pattern - **Phase:** 3 - **Evidence:** Phase 0→1→2→3→4→5 ordering

### AC#2: Character Budget
- [x] wc -c ≤ 10,000 - **Phase:** 3 - **Evidence:** 8,727 characters (87% utilization)

### AC#3: --layer Argument
- [x] 6 valid values accepted - **Phase:** 2 - **Evidence:** VALID_LAYERS = [all, claudemd, prompt, context, rules, adrs]
- [x] Default is "all" - **Phase:** 2 - **Evidence:** Line 27: default: "all"

### AC#4: --fix Mutability
- [x] MUTABLE layers get Edit proposals with AskUserQuestion - **Phase:** 2 - **Evidence:** CLAUDE.md, rules use AskUserQuestion
- [x] IMMUTABLE layers get ADR recommendations only - **Phase:** 2 - **Evidence:** Context files → ADR only, never Edit()
- [x] APPEND-ONLY ADRs get new ADR recommendation - **Phase:** 2 - **Evidence:** ADRs → new ADR, never edit existing

### AC#5: --output
- [x] Console mode displays to terminal - **Phase:** 2 - **Evidence:** Default console output
- [x] File mode writes to devforgeai/qa/ - **Phase:** 2 - **Evidence:** alignment-audit-{date}.md

### AC#6: Task() Invocation
- [x] Task(subagent_type="alignment-auditor") present - **Phase:** 3 - **Evidence:** Phase 1 invocation

### AC#7: Severity Display
- [x] CRITICAL > HIGH > MEDIUM > LOW ordering - **Phase:** 2 - **Evidence:** FOR severity IN [CRITICAL, HIGH, MEDIUM, LOW]

### AC#8: Executive Summary
- [x] Category counts rendered - **Phase:** 2 - **Evidence:** Per-category severity table
- [x] Overall status (PASS/WARN/FAIL) shown - **Phase:** 2 - **Evidence:** STATUS_RULES section

**Checklist Progress:** 16/16 items complete (100%)

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Definition of Done

### Implementation
- [x] audit-alignment.md created at .claude/commands/audit-alignment.md
- [x] YAML frontmatter with description, argument-hint, model: opus, allowed-tools
- [x] Lean orchestration pattern: validate → markers → Task() → format → fix → report → summary
- [x] --layer argument parses 6 values with "all" default
- [x] --fix enforces mutability rules per layer type
- [x] --output supports console (default) and file modes
- [x] Task(subagent_type="alignment-auditor") invocation present
- [x] Severity-based display formatting (CRITICAL > HIGH > MEDIUM > LOW)
- [x] Executive summary table with category counts and status

### Quality
- [x] All 8 acceptance criteria have passing tests
- [x] Character budget ≤ 10,000 characters
- [x] Edge cases covered (6 documented scenarios)
- [x] No business logic in command (all analysis delegated to subagent)

### Testing
- [x] Lean orchestration compliance test passes
- [x] Character budget test passes
- [x] Argument parsing tests pass
- [x] Mutability enforcement tests pass

### Dual-Path Sync
- [x] File created in src/claude/commands/ (source of truth)
- [x] File synced to .claude/commands/ (operational)
- [x] Tests run against src/ tree

### Documentation
- [x] source-tree.md updated per ADR-021 authorization
- [x] Pattern reference to audit-orphans.md documented

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 01 | ✅ | Pre-flight validation passed |
| Phase 02 | ✅ | 8 test suites, 43 assertions (RED) |
| Phase 03 | ✅ | audit-alignment.md created (8,727 chars) |
| Phase 04 | ✅ | Code review approved, no refactoring needed |
| Phase 04.5 | ✅ | All 8 ACs verified PASS |
| Phase 05 | ✅ | Integration: dual-path sync completed |
| Phase 05.5 | ✅ | Post-integration AC verification PASS |
| Phase 06 | ✅ | No deferrals |
| Phase 07 | ✅ | DoD updated |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/commands/audit-alignment.md | Created | ~270 |
| .claude/commands/audit-alignment.md | Synced | ~270 |
| tests/STORY-474/test_ac1_lean_orchestration.sh | Created | 45 |
| tests/STORY-474/test_ac2_character_budget.sh | Created | 45 |
| tests/STORY-474/test_ac3_layer_argument.sh | Created | 65 |
| tests/STORY-474/test_ac4_fix_mutability.sh | Created | 55 |
| tests/STORY-474/test_ac5_output_argument.sh | Created | 60 |
| tests/STORY-474/test_ac6_subagent_invocation.sh | Created | 40 |
| tests/STORY-474/test_ac7_severity_display.sh | Created | 50 |
| tests/STORY-474/test_ac8_executive_summary.sh | Created | 50 |
| tests/STORY-474/run_all_tests.sh | Created | 30 |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-23

- [x] audit-alignment.md created at .claude/commands/audit-alignment.md - Completed: Markdown command file with 5-phase lean orchestration workflow
- [x] YAML frontmatter with description, argument-hint, model: opus, allowed-tools - Completed: All required frontmatter fields present
- [x] Lean orchestration pattern: validate → markers → Task() → format → fix → report → summary - Completed: Zero business logic before Task() delegation
- [x] --layer argument parses 6 values with "all" default - Completed: VALID_LAYERS = [all, claudemd, prompt, context, rules, adrs]
- [x] --fix enforces mutability rules per layer type - Completed: MUTABLE=AskUserQuestion, IMMUTABLE=ADR only, APPEND-ONLY=new ADR
- [x] --output supports console (default) and file modes - Completed: File writes to devforgeai/qa/alignment-audit-{date}.md
- [x] Task(subagent_type="alignment-auditor") invocation present - Completed: Phase 1 delegates all analysis
- [x] Severity-based display formatting (CRITICAL > HIGH > MEDIUM > LOW) - Completed: Descending severity loop with emoji badges
- [x] Executive summary table with category counts and status - Completed: Per-category severity matrix with PASS/WARN/FAIL
- [x] All 8 acceptance criteria have passing tests - Completed: 43 assertions across 8 test suites, all GREEN
- [x] Character budget ≤ 10,000 characters - Completed: 8,727 chars (87% utilization)
- [x] Edge cases covered (6 documented scenarios) - Completed: Error handling section in command
- [x] No business logic in command (all analysis delegated to subagent) - Completed: Verified by test and code review
- [x] Lean orchestration compliance test passes - Completed: ≤4 code blocks before Task()
- [x] Character budget test passes - Completed: wc -c = 8,727
- [x] Argument parsing tests pass - Completed: All 9 assertions pass
- [x] Mutability enforcement tests pass - Completed: All 5 assertions pass
- [x] File created in src/claude/commands/ (source of truth) - Completed: Source file created
- [x] File synced to .claude/commands/ (operational) - Completed: cp to operational directory
- [x] Tests run against src/ tree - Completed: All tests target src/claude/commands/
- [x] Pattern reference to audit-orphans.md documented - Completed: Integration section references related commands
- [x] source-tree.md updated per ADR-021 authorization - Completed: Added to directory tree and command list per ADR-021

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-22 | .claude/story-requirements-analyst | Created | Story created from EPIC-081 Feature 2 (batch 3/5) | STORY-474.story.md |
| 2026-02-23 | .claude/qa-result-interpreter | QA Deep | PASSED: 43/43 tests, 0 violations, 3/3 validators | STORY-474-qa-report.md |

## Notes

**Design Decisions:**
- Lean orchestration pattern follows audit-orphans.md precedent
- Character budget set at 67% of hard limit for future argument additions
- --fix requires AskUserQuestion per edit (consistent with immutable-first philosophy)

**Edge Cases Documented:**
1. alignment-auditor not created → clear error, no inline fallback
2. system-prompt-core.md missing → subagent handles gracefully
3. No findings → PASS with zero counts
4. --fix with IMMUTABLE finding → ADR recommendation only
5. Same-day report file exists → overwrite
6. --layer=adrs with no ADRs → PASS with skip note

**References:**
- [Requirements Specification](devforgeai/specs/requirements/clap-configuration-layer-alignment-requirements.md) (FR-003)
- [audit-orphans.md](.claude/commands/audit-orphans.md) (lean orchestration pattern reference)
- [EPIC-081](devforgeai/specs/Epics/EPIC-081-configuration-layer-alignment-protocol.epic.md)

---

Story Template Version: 2.9
Last Updated: 2026-02-22
