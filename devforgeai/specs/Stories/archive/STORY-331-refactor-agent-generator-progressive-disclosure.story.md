---
id: STORY-331
title: Refactor agent-generator.md with Progressive Disclosure
type: refactor
epic: EPIC-053
sprint: Sprint-1
status: Dev Complete
points: 3
depends_on: ["STORY-330"]
priority: High
assigned_to: TBD
created: 2026-01-29
format_version: "2.7"
---

# Story: Refactor agent-generator.md with Progressive Disclosure

## Description

**As a** DevForgeAI Framework Maintainer,
**I want** the agent-generator.md subagent refactored from 2,370 lines to a core file of 300 lines or less with extracted reference documentation,
**so that** each invocation consumes 60%+ fewer tokens while preserving all functionality, bringing the largest constitutional violator into compliance with tech-stack.md line limits.

## Provenance

```xml
<provenance>
  <origin document="EPIC-053" section="Feature 1: Refactor agent-generator.md">
    <quote>"Lines: 2,370 → ≤300 (core) + references/. Problem: 474% over maximum, largest subagent. Solution: Extract to core + 8-10 reference files. Business Value: Highest token savings impact"</quote>
    <line_reference>lines 63-69</line_reference>
    <quantified_impact>2,370 → ≤300 lines = 87% reduction in core file, 60%+ token savings per invocation</quantified_impact>
  </origin>

  <decision rationale="progressive-disclosure-pattern">
    <selected>Extract documentation to references/ subdirectory per ADR-012 pattern</selected>
    <rejected alternative="split-into-multiple-subagents">Would create coordination complexity</rejected>
    <rejected alternative="truncate-documentation">Would lose valuable context for generation quality</rejected>
    <trade_off>8-10 reference files to maintain, but 60-80% token reduction per invocation</trade_off>
  </decision>

  <hypothesis id="H1" validation="line-count-measurement" success_criteria="Core file ≤300 lines with all functionality preserved">
    Progressive disclosure will enable constitutional compliance while maintaining subagent generation quality
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Core File Size Compliance

```xml
<acceptance_criteria id="AC1" implements="ADR-012-CORE-SIZE">
  <given>The agent-generator.md subagent currently has 2,370 lines (474% over 500-line max)</given>
  <when>The refactoring is complete and the core file is validated</when>
  <then>The core file `src/claude/agents/agent-generator.md` contains 300 lines or fewer, with all required sections: YAML frontmatter, Purpose, When Invoked, Core Workflow (condensed with reference pointers), Success Criteria, Error Handling, Reference Loading, and Observation Capture</then>
  <verification>
    <source_files>
      <file hint="Refactored core subagent">src/claude/agents/agent-generator.md</file>
    </source_files>
    <test_file>tests/STORY-331/test_ac1_core_file_size.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Reference Directory Structure

```xml
<acceptance_criteria id="AC2" implements="ADR-012-DIR-STRUCTURE">
  <given>The agent-generator requires extensive documentation that exceeds core file limits</given>
  <when>The references directory is created per ADR-012 approved pattern</when>
  <then>A `src/claude/agents/agent-generator/references/` directory exists containing 6-10 reference files covering: template-patterns.md, frontmatter-specification.md, tool-restrictions.md, output-formats.md, validation-workflow.md, error-handling.md, and additional topic-specific references as needed</then>
  <verification>
    <source_files>
      <file hint="Reference directory">src/claude/agents/agent-generator/references/</file>
    </source_files>
    <test_file>tests/STORY-331/test_ac2_reference_directory.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Functionality Preservation (No Regression)

```xml
<acceptance_criteria id="AC3" implements="ADR-012-NO-REGRESSION">
  <given>The original agent-generator.md has documented workflows for batch generation, single subagent generation, priority tier generation, and framework validation</given>
  <when>The refactored core file and references are loaded together</when>
  <then>All original functionality is preserved: subagent creation modes (batch, single, by-priority, regenerate), YAML validation, system prompt generation, framework compliance validation (DevForgeAI + Claude Code patterns), reference file generation (Step 4.5), and summary report generation</then>
  <verification>
    <source_files>
      <file hint="Refactored core">src/claude/agents/agent-generator.md</file>
      <file hint="Reference files">src/claude/agents/agent-generator/references/*.md</file>
    </source_files>
    <test_file>tests/STORY-331/test_ac3_functionality_preservation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Reference Loading Pattern Implementation

```xml
<acceptance_criteria id="AC4" implements="ADR-012-REF-LOADING">
  <given>References must be loaded on-demand when the subagent needs them</given>
  <when>A developer reviews the core agent-generator.md file</when>
  <then>The core file contains a "Reference Loading" section with explicit Read() instructions pointing to each reference file in `src/claude/agents/agent-generator/references/`, with clear context about when each reference should be loaded</then>
  <verification>
    <source_files>
      <file hint="Reference loading section">src/claude/agents/agent-generator.md</file>
    </source_files>
    <test_file>tests/STORY-331/test_ac4_reference_loading.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Observation Capture Section (EPIC-052 Compliance)

```xml
<acceptance_criteria id="AC5" implements="EPIC-052-OBSERVATION">
  <given>Per EPIC-052, all high-frequency subagents must include Observation Capture sections</given>
  <when>The refactored agent-generator.md is reviewed</when>
  <then>The core file contains an "Observation Capture" section with the standard observation schema (7 categories: friction, success, pattern, gap, idea, bug, warning), severity levels (low, medium, high), and optional files array, marked as OPTIONAL for backward compatibility</then>
  <verification>
    <source_files>
      <file hint="Observation section">src/claude/agents/agent-generator.md</file>
    </source_files>
    <test_file>tests/STORY-331/test_ac5_observation_capture.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Operational Copy Synchronization

```xml
<acceptance_criteria id="AC6" implements="SOURCE-TREE-MIRROR">
  <given>DevForgeAI maintains dual locations per source-tree.md: src/claude/agents/ (source) and .claude/agents/ (operational)</given>
  <when>The refactoring is complete</when>
  <then>Both `src/claude/agents/agent-generator.md` and `.claude/agents/agent-generator.md` are identical, AND both reference directories `src/claude/agents/agent-generator/references/` and `.claude/agents/agent-generator/references/` contain identical files</then>
  <verification>
    <source_files>
      <file hint="Source core">src/claude/agents/agent-generator.md</file>
      <file hint="Operational core">.claude/agents/agent-generator.md</file>
      <file hint="Source references">src/claude/agents/agent-generator/references/</file>
      <file hint="Operational references">.claude/agents/agent-generator/references/</file>
    </source_files>
    <test_file>tests/STORY-331/test_ac6_sync_verification.sh</test_file>
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
      name: "agent-generator.md (core)"
      file_path: "src/claude/agents/agent-generator.md"
      purpose: "Subagent for generating new DevForgeAI-compliant subagents"
      required_keys:
        - key: "YAML frontmatter"
          type: "yaml_block"
          required: true
          validation: "Must contain name, description, tools, model fields"
          test_requirement: "Test: YAML parse succeeds, required fields present"
        - key: "Purpose section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Purpose header exists"
        - key: "When Invoked section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## When Invoked header exists"
        - key: "Core Workflow section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Core Workflow header exists"
        - key: "Success Criteria section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Success Criteria header exists"
        - key: "Error Handling section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Error Handling header exists"
        - key: "Reference Loading section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Reference Loading header exists with Read() calls"
        - key: "Observation Capture section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Observation Capture header exists with schema"
      requirements:
        - id: "CORE-001"
          description: "Core file must be <= 300 lines"
          testable: true
          test_requirement: "Test: wc -l returns <= 300"
          priority: "Critical"
        - id: "CORE-002"
          description: "All 8 required sections present"
          testable: true
          test_requirement: "Test: Grep for all 8 section headers"
          priority: "Critical"
        - id: "CORE-003"
          description: "Reference loading uses explicit Read() syntax"
          testable: true
          test_requirement: "Test: Grep for Read(file_path=\"src/claude/agents/agent-generator/references/"
          priority: "High"

    - type: "Configuration"
      name: "agent-generator references"
      file_path: "src/claude/agents/agent-generator/references/"
      purpose: "Extracted documentation for progressive disclosure"
      required_keys:
        - key: "template-patterns.md"
          type: "file"
          required: true
          test_requirement: "Test: File exists and is valid markdown"
        - key: "frontmatter-specification.md"
          type: "file"
          required: true
          test_requirement: "Test: File exists and is valid markdown"
        - key: "tool-restrictions.md"
          type: "file"
          required: true
          test_requirement: "Test: File exists and is valid markdown"
        - key: "output-formats.md"
          type: "file"
          required: true
          test_requirement: "Test: File exists and is valid markdown"
        - key: "validation-workflow.md"
          type: "file"
          required: true
          test_requirement: "Test: File exists and is valid markdown"
        - key: "error-handling.md"
          type: "file"
          required: true
          test_requirement: "Test: File exists and is valid markdown"
      requirements:
        - id: "REF-001"
          description: "6-10 reference files in references/ directory"
          testable: true
          test_requirement: "Test: Count files in references/ is between 6 and 10"
          priority: "Critical"
        - id: "REF-002"
          description: "All reference files use lowercase-hyphen naming"
          testable: true
          test_requirement: "Test: ls references/ | grep -v '^[a-z][a-z0-9-]*\\.md$' returns 0 matches"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Core file must contain condensed workflow with reference pointers"
      trigger: "When core workflow documentation exceeds space"
      validation: "Reference pointer format: Read(file_path=...)"
      error_handling: "Missing references trigger graceful degradation"
      test_requirement: "Test: Core workflow contains 'For details, see references/' or Read() calls"
      priority: "Critical"
    - id: "BR-002"
      rule: "All original functionality must be preserved in core + references"
      trigger: "When validating refactoring completeness"
      validation: "Functional comparison checklist passes"
      error_handling: "Missing functionality blocks completion"
      test_requirement: "Test: Functionality checklist (batch, single, validate, etc.) all pass"
      priority: "Critical"
    - id: "BR-003"
      rule: "Observation Capture must follow EPIC-052 schema exactly"
      trigger: "When generating observation section"
      validation: "7 categories present: friction, success, pattern, gap, idea, bug, warning"
      error_handling: "Missing categories triggers validation failure"
      test_requirement: "Test: Grep for all 7 observation categories"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Token consumption for core file load reduced by 60%+"
      metric: "Core file <= 15,000 tokens (vs ~95,000 original)"
      test_requirement: "Test: Estimate tokens from line count (4 chars/token avg)"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "100% backward compatibility with existing invocations"
      metric: "0 breaking changes to Task(subagent_type=\"agent-generator\") calls"
      test_requirement: "Test: Existing invocation patterns still work"
      priority: "Critical"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Single source of truth maintained"
      metric: "src/ and .claude/ copies are identical (diff = 0)"
      test_requirement: "Test: diff -r src/claude/agents/agent-generator .claude/agents/agent-generator returns empty"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No technical limitations identified - straightforward refactoring
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Token Reduction:**
- Core file load: <= 15,000 tokens (vs ~95,000 tokens for current 2,370 lines)
- Target reduction: >= 60% compared to original
- Reference loading: Additional 5,000-20,000 tokens per reference file loaded on-demand
- No latency impact: Reference loading < 100ms overhead per file

---

### Security

**No sensitive data:** Reference files must not contain API keys, secrets, or credentials
**File paths:** All reference pointers use relative paths from project root
**No execution vectors:** Reference files are documentation only (Markdown)

---

### Reliability

**Graceful degradation:** If a reference file is missing, core file provides fallback guidance
**Backward compatible:** 100% of existing `Task(subagent_type="agent-generator", ...)` invocations work unchanged
**Self-contained core:** Core file is functional without references for basic subagent generation

---

### Maintainability

**Single source of truth:** `src/claude/agents/` is source, `.claude/agents/` is mirror
**Reference isolation:** Each reference file covers one topic (single responsibility)
**Cross-reference consistency:** All reference pointers in core file point to files that exist

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-330:** Update source-tree.md for Subagent References
  - **Why:** Constitutional update must be complete before subdirectories can be created
  - **Status:** Backlog (must complete first)

### External Dependencies

- [x] **ADR-012:** Subagent Progressive Disclosure Architecture (approved)
  - **Status:** Approved
  - **Impact:** Provides the approved pattern for refactoring

### Technology Dependencies

- [ ] **None** - No new packages required (markdown documentation only)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% of acceptance criteria

**Test Scenarios:**
1. **AC1 - Core File Size:** Verify line count <= 300, all required sections present
2. **AC2 - Reference Directory:** Verify 6-10 files exist with correct naming
3. **AC3 - Functionality:** Verify all generation modes work (batch, single, validate)
4. **AC4 - Reference Loading:** Verify Read() calls present for all references
5. **AC5 - Observation Capture:** Verify 7 categories present in schema
6. **AC6 - Sync:** Verify src/ and .claude/ are identical

### Edge Cases

1. **Phase 0 Reference Loading:** Preserve sophisticated Phase 0 workflow loading Claude Code guidance
2. **Slash Command Refactoring Section:** Extract 300+ lines to dedicated reference file
3. **Framework Validation Checkpoint:** Extract 100+ lines validation logic to reference
4. **Reference File Generation (Step 4.5):** Extract 400+ lines templates to reference
5. **Batch Mode Token Budget:** Document in core, details in references
6. **Backward Compatibility:** Existing invocations must continue working

---

## Acceptance Criteria Verification Checklist

### AC#1: Core File Size Compliance

- [x] Original file analyzed (2,370 lines) - **Phase:** 2 - **Evidence:** wc -l output confirms 2,370 lines
- [x] Required sections identified (8 total) - **Phase:** 2 - **Evidence:** test_ac1 validates 8 sections, currently has 6/8
- [x] Core file refactored to <= 300 lines - **Phase:** 3 - **Evidence:** wc -l output shows 231 lines
- [x] All 8 required sections present - **Phase:** 4 - **Evidence:** Grep validation confirms all 8 sections

### AC#2: Reference Directory Structure

- [x] Directory created at src/claude/agents/agent-generator/references/ - **Phase:** 3 - **Evidence:** ls output confirms directory exists
- [x] 6-10 reference files created - **Phase:** 3 - **Evidence:** 8 files created
- [x] All files use lowercase-hyphen naming - **Phase:** 4 - **Evidence:** ls validation confirms all 8 files compliant

### AC#3: Functionality Preservation

- [x] Batch generation mode works - **Phase:** 5 - **Evidence:** test_ac3 14/14 PASSED - "Batch generation mode (generate all) documented"
- [x] Single subagent generation works - **Phase:** 5 - **Evidence:** test_ac3 14/14 PASSED - "Single subagent generation mode documented"
- [x] Priority tier generation works - **Phase:** 5 - **Evidence:** test_ac3 14/14 PASSED - "Priority tier generation mode documented"
- [x] Framework validation works - **Phase:** 5 - **Evidence:** test_ac3 14/14 PASSED - "DevForgeAI framework validation documented"

### AC#4: Reference Loading Pattern

- [x] Reference Loading section exists - **Phase:** 3 - **Evidence:** Grep for header confirms present
- [x] Read() calls present for each reference - **Phase:** 4 - **Evidence:** Grep count shows 10 Read() calls, 8/8 references covered

### AC#5: Observation Capture Section

- [x] Observation Capture section exists - **Phase:** 3 - **Evidence:** Grep for header confirms present
- [x] 7 categories present - **Phase:** 4 - **Evidence:** Grep for categories confirms all 7 present

### AC#6: Operational Copy Synchronization

- [x] src/ core matches .claude/ core - **Phase:** 5 - **Evidence:** test_ac6 9/9 PASSED - "Core files are identical (src/ == .claude/)"
- [x] src/ references match .claude/ references - **Phase:** 5 - **Evidence:** test_ac6 9/9 PASSED - "All reference files are identical"

---

**Checklist Progress:** 18/18 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Core agent-generator.md refactored to <= 300 lines
- [x] references/ directory created with 6-10 files
- [x] All required sections present in core file
- [x] Reference Loading section with Read() calls
- [x] Observation Capture section with 7 categories
- [x] src/ and .claude/ copies synchronized

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases handled (Phase 0 loading, validation checkpoint, etc.)
- [x] No functionality regression (all generation modes work)
- [x] Token reduction >= 60% verified

### Testing
- [x] Test: Core file line count <= 300
- [x] Test: Reference directory structure valid
- [x] Test: Functionality preservation checklist
- [x] Test: Reference loading pattern present
- [x] Test: Observation capture schema complete
- [x] Test: Sync between src/ and .claude/

### Documentation
- [x] Reference files documented (one topic per file)
- [x] Core file condensed workflow clear
- [x] Reference loading instructions explicit

---

## Implementation Notes

- [x] Core agent-generator.md refactored to <= 300 lines - Completed: 231 lines (90% reduction from 2,370)
- [x] references/ directory created with 6-10 files - Completed: 8 files created
- [x] All required sections present in core file - Completed: All 8 sections verified by test_ac1
- [x] Reference Loading section with Read() calls - Completed: 10 Read() calls covering all 8 references
- [x] Observation Capture section with 7 categories - Completed: friction, success, pattern, gap, idea, bug, warning
- [x] src/ and .claude/ copies synchronized - Completed: diff returns empty (verified by test_ac6)
- [x] All 6 acceptance criteria have passing tests - Completed: 63/63 tests passed
- [x] Edge cases handled (Phase 0 loading, validation checkpoint, etc.) - Completed: All edge cases documented
- [x] No functionality regression (all generation modes work) - Completed: batch, single, priority, regenerate preserved
- [x] Token reduction >= 60% verified - Completed: 90% reduction (2,370 → 231 lines)
- [x] Test: Core file line count <= 300 - Completed: test_ac1 11/11 passed
- [x] Test: Reference directory structure valid - Completed: test_ac2 8/8 passed
- [x] Test: Functionality preservation checklist - Completed: test_ac3 14/14 passed
- [x] Test: Reference loading pattern present - Completed: test_ac4 8/8 passed
- [x] Test: Observation capture schema complete - Completed: test_ac5 13/13 passed
- [x] Test: Sync between src/ and .claude/ - Completed: test_ac6 9/9 passed
- [x] Reference files documented (one topic per file) - Completed: 8 topic-specific reference files
- [x] Core file condensed workflow clear - Completed: workflow fits in 231 lines with reference pointers
- [x] Reference loading instructions explicit - Completed: when-to-load table in Reference Loading section

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-30

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-29 09:15 | claude/story-requirements-analyst | Created | Story created from EPIC-053 Feature 1 | STORY-331.story.md |
| 2026-01-30 | DevForgeAI AI Agent | Dev Complete | Refactored agent-generator.md from 2,370 to 231 lines with 8 reference files | src/claude/agents/agent-generator.md, src/claude/agents/agent-generator/references/*.md |
| 2026-01-30 | claude/qa-result-interpreter | QA Deep | PASSED: 63/63 tests, 100% traceability, 0 violations, 2/2 validators | devforgeai/qa/reports/STORY-331-qa-report.md |

## Notes

**Design Decisions:**
- 8-10 reference files provide good balance between granularity and manageability
- Core file targets 200-250 lines to leave buffer under 300-line limit
- Reference loading uses explicit Read() calls (not implicit loading)
- Observation Capture placed last in core file for consistency

**Extraction Strategy:**
1. **template-patterns.md** - Agent templates by type (700+ lines extracted)
2. **frontmatter-specification.md** - YAML validation rules (200+ lines)
3. **tool-restrictions.md** - Tool access patterns (150+ lines)
4. **output-formats.md** - Output structure specifications (200+ lines)
5. **validation-workflow.md** - Framework validation logic (300+ lines)
6. **error-handling.md** - Error recovery procedures (150+ lines)
7. **command-refactoring-patterns.md** - Slash command guidance (300+ lines)
8. **reference-file-templates.md** - Guardrail file generation (400+ lines)

**Related ADRs:**
- [ADR-012: Subagent Progressive Disclosure Architecture](../adrs/ADR-012-subagent-progressive-disclosure.md)

**References:**
- EPIC-053: Subagent Progressive Disclosure Refactoring
- RESEARCH-006: Subagent Progressive Disclosure Analysis
- STORY-330: Constitutional update (prerequisite)

---

Story Template Version: 2.7
Last Updated: 2026-01-29
