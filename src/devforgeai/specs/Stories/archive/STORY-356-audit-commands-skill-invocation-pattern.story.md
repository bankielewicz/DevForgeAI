---
id: STORY-356
title: Audit Other Commands for Similar Skill Invocation Pattern
type: feature
epic: N/A
sprint: Backlog
status: QA Approved
points: 2
depends_on: []
priority: High
assigned_to: Unassigned
created: 2026-02-02
format_version: "2.7"
source_rca: RCA-037
source_recommendation: REC-3
---

# Story: Audit Other Commands for Similar Skill Invocation Pattern

## Description

**As a** DevForgeAI framework maintainer,
**I want** to audit the `/ideate`, `/create-context`, `/create-epic`, and `/brainstorm` commands for explicit skill invocation patterns,
**so that** I can verify all commands follow the RCA-037 Skill Invocation Checkpoint Pattern and prevent future skill bypass incidents.

**Background:**
RCA-037 identified that the `/create-story` command's Epic Batch Workflow used summary language ("Markers → Skill → Track") without explicit `Skill(command="...")` syntax, allowing Claude to deviate from the prescribed workflow. This audit ensures other commands don't have similar implicit skill invocation gaps.

## Acceptance Criteria

### AC#1: Audit /ideate Command for Explicit Skill Invocation

```xml
<acceptance_criteria id="AC1" implements="AUDIT-001">
  <given>The /ideate command file exists at .claude/commands/ideate.md (operational) and src/claude/commands/ideate.md (source)</given>
  <when>The auditor reads the command file and searches for skill invocation patterns</when>
  <then>The audit confirms COMPLIANT (Skill(command="devforgeai-ideation") appears with explicit tool call syntax) or NON-COMPLIANT (uses summary language or missing)</then>
  <verification>
    <source_files>
      <file hint="Command file to audit">src/claude/commands/ideate.md</file>
    </source_files>
    <test_file>tests/STORY-356/test_ac1_ideate_audit.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Audit /create-context Command for Explicit Skill Invocation

```xml
<acceptance_criteria id="AC2" implements="AUDIT-002">
  <given>The /create-context command file exists at .claude/commands/create-context.md (operational) and src/claude/commands/create-context.md (source)</given>
  <when>The auditor reads the command file and searches for skill invocation patterns</when>
  <then>The audit confirms COMPLIANT (Skill(command="devforgeai-architecture") appears with explicit tool call syntax) or NON-COMPLIANT</then>
  <verification>
    <source_files>
      <file hint="Command file to audit">src/claude/commands/create-context.md</file>
    </source_files>
    <test_file>tests/STORY-356/test_ac2_create_context_audit.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Audit /create-epic Command for Explicit Skill Invocation

```xml
<acceptance_criteria id="AC3" implements="AUDIT-003">
  <given>The /create-epic command file exists at .claude/commands/create-epic.md (operational) and src/claude/commands/create-epic.md (source)</given>
  <when>The auditor reads the command file and searches for skill invocation patterns</when>
  <then>The audit confirms COMPLIANT (Skill(command="devforgeai-orchestration") appears with explicit tool call syntax) or NON-COMPLIANT</then>
  <verification>
    <source_files>
      <file hint="Command file to audit">src/claude/commands/create-epic.md</file>
    </source_files>
    <test_file>tests/STORY-356/test_ac3_create_epic_audit.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Audit /brainstorm Command for Explicit Skill Invocation

```xml
<acceptance_criteria id="AC4" implements="AUDIT-004">
  <given>The /brainstorm command file exists at .claude/commands/brainstorm.md (operational) and src/claude/commands/brainstorm.md (source)</given>
  <when>The auditor reads the command file and searches for skill invocation patterns</when>
  <then>The audit confirms COMPLIANT (Skill(command="devforgeai-brainstorming") appears with explicit tool call syntax) or NON-COMPLIANT</then>
  <verification>
    <source_files>
      <file hint="Command file to audit">src/claude/commands/brainstorm.md</file>
    </source_files>
    <test_file>tests/STORY-356/test_ac4_brainstorm_audit.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Generate Audit Summary Report

```xml
<acceptance_criteria id="AC5" implements="AUDIT-005">
  <given>All four commands have been audited per AC1-AC4</given>
  <when>The audit is complete</when>
  <then>A summary report is generated containing: command name, skill invoked, line number, compliance status (COMPLIANT/NON-COMPLIANT), and remediation needed</then>
  <verification>
    <source_files>
      <file hint="All command files">src/claude/commands/*.md</file>
    </source_files>
    <test_file>tests/STORY-356/test_ac5_audit_report.py</test_file>
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
      name: "ideate.md"
      file_path: "src/claude/commands/ideate.md"
      required_keys:
        - key: "Skill invocation"
          type: "string"
          example: "Skill(command=\"devforgeai-ideation\")"
          required: true
          validation: "Must use explicit Skill(command=\"...\") syntax"
          test_requirement: "Test: Grep for Skill(command= pattern"

    - type: "Configuration"
      name: "create-context.md"
      file_path: "src/claude/commands/create-context.md"
      required_keys:
        - key: "Skill invocation"
          type: "string"
          example: "Skill(command=\"devforgeai-architecture\")"
          required: true
          validation: "Must use explicit Skill(command=\"...\") syntax"
          test_requirement: "Test: Grep for Skill(command= pattern"

    - type: "Configuration"
      name: "create-epic.md"
      file_path: "src/claude/commands/create-epic.md"
      required_keys:
        - key: "Skill invocation"
          type: "string"
          example: "Skill(command=\"devforgeai-orchestration\")"
          required: true
          validation: "Must use explicit Skill(command=\"...\") syntax"
          test_requirement: "Test: Grep for Skill(command= pattern"

    - type: "Configuration"
      name: "brainstorm.md"
      file_path: "src/claude/commands/brainstorm.md"
      required_keys:
        - key: "Skill invocation"
          type: "string"
          example: "Skill(command=\"devforgeai-brainstorming\")"
          required: true
          validation: "Must use explicit Skill(command=\"...\") syntax"
          test_requirement: "Test: Grep for Skill(command= pattern"

  business_rules:
    - id: "BR-001"
      rule: "Skill invocation must use explicit Skill(command=\"...\") syntax"
      trigger: "When auditing command files"
      validation: "Regex match: Skill\\(command=\"[a-z0-9-]+\"\\)"
      error_handling: "Mark as NON-COMPLIANT, add to remediation list"
      test_requirement: "Test: Pattern match for explicit skill syntax"
      priority: "Critical"

    - id: "BR-002"
      rule: "Summary language like '→ Skill →' is NOT compliant"
      trigger: "When searching for skill invocation"
      validation: "If only summary language found, mark NON-COMPLIANT"
      error_handling: "Require remediation to add explicit syntax"
      test_requirement: "Test: Grep for summary patterns and flag as violations"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Audit completion time"
      metric: "< 5 minutes total (< 75 seconds per command)"
      test_requirement: "Test: Measure audit execution time"
      priority: "Medium"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Audit resilience"
      metric: "Complete even if one command file missing (report as NOT FOUND)"
      test_requirement: "Test: Verify graceful handling of missing files"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified for this audit task
```

---

## Dual-Path Awareness (source-tree.md Compliance)

**Context:** DevForgeAI uses a dual-location architecture (source-tree.md, lines 512-531):

| Location | Role | Present After Deployment? |
|----------|------|--------------------------|
| `.claude/commands/*.md` | **Operational** — discovered and executed by Claude Code Terminal at runtime | Yes (always) |
| `src/claude/commands/*.md` | **Distribution source** — source of truth for framework development | No (DevForgeAI repo only) |

**Path Usage Rules for This Story:**

| Context | Path Used | Why |
|---------|-----------|-----|
| AC `<given>` clauses | Both paths documented | Describes operational reality AND source location |
| AC `<source_files>` / `<test_file>` | `src/claude/commands/` | Tests read from src/ tree per CLAUDE.md and source-tree.md line 15 |
| Technical Specification `file_path` | `src/claude/commands/` | Identifies where changes are made (source of truth) |
| Audit report findings | `.claude/commands/` | Reports describe operational runtime paths |
| Remediation actions | `src/claude/commands/` | Changes are applied to src/ tree, deployed by installer |

**Key Principle:** After DevForgeAI is deployed to another project, only `.claude/` exists. Commands, skills, and templates reference operational paths (`.claude/skills/`, `.claude/agents/`, etc.) because that is the runtime environment. The `src/` tree is a development-time concern specific to the DevForgeAI framework repository.

**Reference:** source-tree.md (Dual-Location Architecture, lines 512-531)

---

## Non-Functional Requirements (NFRs)

### Performance

- Audit completion time: < 5 minutes total (< 75 seconds per command)
- Token consumption: < 10,000 tokens for complete audit
- File read operations: Exactly 4 (one per command file)

---

### Reliability

- Audit must complete even if one command file is missing
- Pattern matching must handle variations in whitespace
- Report generation must succeed with partial results

---

### Auditability

- All findings must include source file path and line number
- Audit report must be reproducible
- Each AC verification step must be logged

---

## Edge Cases

1. **Command file contains multiple Skill() invocations:** Some commands may invoke multiple skills or invoke the same skill in different workflow modes. Audit must verify ALL skill invocations use explicit syntax.

2. **Skill invocation appears in error handling section only:** If `Skill(command="...")` only appears in error recovery, flag as NON-COMPLIANT for primary workflow.

3. **Code block contains Skill() but is commented out:** Skill invocations inside comments or "WRONG pattern" sections should not count as compliant.

4. **Skill name mismatch:** Command says it invokes one skill but actual call uses different name. Flag as configuration issue.

---

## Data Validation Rules

1. **Command file path format:** Operational: `.claude/commands/{command-name}.md`, Test source: `src/claude/commands/{command-name}.md`
2. **Skill invocation pattern:** Must match regex `Skill\(command="[a-z0-9-]+"\)`
3. **Line number reference:** Must be positive integer
4. **Compliance status:** Must be "COMPLIANT" or "NON-COMPLIANT"
5. **Remediation field:** "None" if COMPLIANT, specific action if NON-COMPLIANT

---

## Dependencies

### Prerequisite Stories

- **STORY-355:** Document Skill Invocation Checkpoint Pattern
  - **Why:** Provides the pattern criteria for this audit
  - **Status:** Backlog (can be done in parallel)

### External Dependencies

None

### Technology Dependencies

None

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%

**Test Scenarios:**
1. **Happy Path:** All 4 commands have explicit skill invocation
2. **Edge Cases:**
   - Missing command file
   - Multiple skill invocations in one file
   - Skill in comment block

---

## Audit Methodology

### For Each Command File:

1. **Read file:** `Read(file_path=".claude/commands/{command}.md")` (tests read from src/ tree per source-tree.md)
2. **Search pattern:** `Grep(pattern="Skill\\(command=", path=file)`
3. **Verify explicit syntax:** Match against `Skill(command="skill-name")`
4. **Check for summary language:** Search for "→ Skill", "Skill →", or isolated "Skill" without parentheses
5. **Document finding:** Line number, compliance status, skill name
6. **Report operational path:** Document `.claude/commands/{command}.md` as the runtime location
7. **Determine remediation:** If NON-COMPLIANT, specify required changes (applied to src/ tree, deployed to .claude/ by installer)

### Expected Findings:

| Command | Expected Skill | Expected Status |
|---------|----------------|-----------------|
| /ideate | devforgeai-ideation | COMPLIANT |
| /create-context | devforgeai-architecture | COMPLIANT |
| /create-epic | devforgeai-orchestration | COMPLIANT |
| /brainstorm | devforgeai-brainstorming | COMPLIANT |

---

## Acceptance Criteria Verification Checklist

### AC#1: Audit /ideate Command

- [x] Read src/claude/commands/ideate.md file - **Phase:** 3 - **Evidence:** Read output
- [x] Search for Skill(command= pattern - **Phase:** 3 - **Evidence:** Grep result
- [x] Verify explicit syntax used - **Phase:** 3 - **Evidence:** Pattern match
- [x] Document line number and status - **Phase:** 3 - **Evidence:** COMPLIANT, line 278

### AC#2: Audit /create-context Command

- [x] Read src/claude/commands/create-context.md file - **Phase:** 3 - **Evidence:** Read output
- [x] Search for Skill(command= pattern - **Phase:** 3 - **Evidence:** Grep result
- [x] Verify explicit syntax used - **Phase:** 3 - **Evidence:** Pattern match
- [x] Document line number and status - **Phase:** 3 - **Evidence:** COMPLIANT, line 68

### AC#3: Audit /create-epic Command

- [x] Read src/claude/commands/create-epic.md file - **Phase:** 3 - **Evidence:** Read output
- [x] Search for Skill(command= pattern - **Phase:** 3 - **Evidence:** Grep result
- [x] Verify explicit syntax used - **Phase:** 3 - **Evidence:** Pattern match
- [x] Document line number and status - **Phase:** 3 - **Evidence:** COMPLIANT, line 133

### AC#4: Audit /brainstorm Command

- [x] Read src/claude/commands/brainstorm.md file - **Phase:** 3 - **Evidence:** Read output
- [x] Search for Skill(command= pattern - **Phase:** 3 - **Evidence:** Grep result
- [x] Verify explicit syntax used - **Phase:** 3 - **Evidence:** Pattern match
- [x] Document line number and status - **Phase:** 3 - **Evidence:** COMPLIANT, line 73

### AC#5: Generate Audit Summary Report

- [x] Compile findings from AC1-AC4 - **Phase:** 4 - **Evidence:** Audit data
- [x] Generate summary table - **Phase:** 4 - **Evidence:** Report format
- [x] Determine overall status - **Phase:** 4 - **Evidence:** 4/4 COMPLIANT

---

**Checklist Progress:** 17/17 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Audit /ideate command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-ideation") at line 278
- [x] Audit /create-context command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-architecture") at line 68
- [x] Audit /create-epic command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-orchestration") at line 133
- [x] Audit /brainstorm command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-brainstorming") at line 73
- [x] Generate audit summary report with compliance status - Completed: AuditReport with 4/4 COMPLIANT, 0 NON-COMPLIANT

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 68 tests covering all 5 ACs (100% pass rate)
- [x] All findings include line number references - Completed: Lines 278, 68, 133, 73 documented per command
- [x] Report format matches specification - Completed: AuditReport with findings[], summary{} per spec

### Testing
- [x] Unit tests for pattern matching - Completed: BR-001 regex and BR-002 summary language tests in all AC test files
- [x] Integration test for full audit workflow - Completed: test_ac5_audit_report.py with 17 integration tests

### Documentation
- [x] RCA-037 Implementation Checklist updated (REC-3 marked complete) - Completed: Audit confirms all 4 commands compliant
- [x] Audit findings documented in report - Completed: AuditReport.to_dict() generates structured JSON report

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-02-05
**Branch:** main

- [x] Audit /ideate command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-ideation") at line 278
- [x] Audit /create-context command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-architecture") at line 68
- [x] Audit /create-epic command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-orchestration") at line 133
- [x] Audit /brainstorm command and document finding - Completed: COMPLIANT, Skill(command="devforgeai-brainstorming") at line 73
- [x] Generate audit summary report with compliance status - Completed: AuditReport with 4/4 COMPLIANT, 0 NON-COMPLIANT
- [x] All 5 acceptance criteria have passing tests - Completed: 68 tests covering all 5 ACs (100% pass rate)
- [x] All findings include line number references - Completed: Lines 278, 68, 133, 73 documented per command
- [x] Report format matches specification - Completed: AuditReport with findings[], summary{} per spec
- [x] Unit tests for pattern matching - Completed: BR-001 regex and BR-002 summary language tests in all AC test files
- [x] Integration test for full audit workflow - Completed: test_ac5_audit_report.py with 17 integration tests
- [x] RCA-037 Implementation Checklist updated (REC-3 marked complete) - Completed: Audit confirms all 4 commands compliant
- [x] Audit findings documented in report - Completed: AuditReport.to_dict() generates structured JSON report

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 68 tests covering all 5 acceptance criteria
- Tests placed in tests/STORY-356/
- All tests follow AAA pattern (Arrange/Act/Assert)
- Test framework: pytest

**Phase 03 (Green): Implementation**
- Implemented audit_skill_invocation.py via backend-architect subagent
- Functions: audit_command(), generate_audit_report(), _find_compliant_invocations()
- Data classes: AuditResult, AuditReport with to_dict() serialization
- All 68 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code reviewed by refactoring-specialist and code-reviewer
- Clean separation of concerns: constants, data classes, helpers, public API
- All tests remain green after refactoring

**Phase 05 (Integration): Full Validation**
- Full test suite: 68/68 passing in 3.05s
- Coverage: 99% for audit_skill_invocation.py (threshold: 95%)
- No gaming violations detected (0 skips, 0 empty tests, 0 mocks)

**Phase 06 (Deferral): DoD Validation**
- All Definition of Done items validated
- 0 deferrals - no items deferred
- No blockers detected

### Files Created/Modified

**Created:**
- tests/STORY-356/__init__.py
- tests/STORY-356/conftest.py
- tests/STORY-356/audit_skill_invocation.py
- tests/STORY-356/test_ac1_ideate_audit.py
- tests/STORY-356/test_ac2_create_context_audit.py
- tests/STORY-356/test_ac3_create_epic_audit.py
- tests/STORY-356/test_ac4_brainstorm_audit.py
- tests/STORY-356/test_ac5_audit_report.py

### Test Results

- **Total tests:** 68
- **Pass rate:** 100%
- **Coverage:** 99% for business logic
- **Execution time:** 3.05 seconds

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-02 12:30 | claude/story-requirements-analyst | Created | Story created from RCA-037 REC-3 | STORY-356.story.md |
| 2026-02-04 | claude/opus | Pre-dev fix | Added dual-path awareness: AC givens reference both operational (.claude/) and source (src/) paths; test source_files and tech spec use src/; added Dual-Path Awareness section per source-tree.md lines 512-531 | STORY-356.story.md |
| 2026-02-05 | claude/opus | DoD Update (Phase 07) | Development complete: 68 tests, 99% coverage, all 4 commands COMPLIANT, DoD validated | STORY-356.story.md |
| 2026-02-04 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 99%, 0 violations, 4/4 validators passed | STORY-356-qa-report.md |

## Notes

**Source:** RCA-037 (Skill Invocation Skipped Despite Orchestrator Instructions)

**Audit Scope:** 4 commands identified in RCA-037 REC-3:
- /ideate
- /create-context
- /create-epic
- /brainstorm

**Expected Outcome:** Based on preliminary analysis, all 4 commands are expected to be COMPLIANT with explicit `Skill(command="...")` syntax.

**References:**
- [RCA-037](devforgeai/RCA/RCA-037-skill-invocation-skipped-despite-orchestrator-instructions.md)
- [STORY-355](devforgeai/specs/Stories/STORY-355-document-skill-invocation-checkpoint-pattern.story.md) (Pattern documentation)

---

Story Template Version: 2.7
Last Updated: 2026-02-02
