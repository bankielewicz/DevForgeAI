---
id: STORY-334
title: Refactor ac-compliance-verifier.md with Progressive Disclosure
type: refactor
epic: EPIC-053
sprint: Sprint-2
status: QA Approved
points: 2
depends_on: ["STORY-330"]
priority: High
assigned_to: TBD
created: 2026-01-30
format_version: "2.7"
---

# Story: Refactor ac-compliance-verifier.md with Progressive Disclosure

## Description

**As a** DevForgeAI Framework Maintainer,
**I want** the ac-compliance-verifier.md subagent refactored from 1,165 lines to a core file of 300 lines or fewer with extracted reference documentation,
**so that** each invocation consumes 60%+ fewer tokens while preserving all AC verification functionality, bringing this critical quality gate subagent into constitutional compliance with tech-stack.md line limits.

## Provenance

```xml
<provenance>
  <origin document="EPIC-053" section="Feature 4: Refactor ac-compliance-verifier.md">
    <quote>"Lines: 1,165 → ≤300 (core) + references/. Problem: 233% over maximum. Solution: Extract verification workflows to references. Business Value: Completes CRITICAL tier refactoring"</quote>
    <line_reference>lines 84-89</line_reference>
    <quantified_impact>1,165 → ≤300 lines = 74% reduction in core file, 60%+ token savings per invocation, completes all P0 subagent refactoring</quantified_impact>
  </origin>

  <decision rationale="progressive-disclosure-for-ac-verification-subagent">
    <selected>Extract verification workflows to references/ subdirectory per ADR-012 pattern</selected>
    <rejected alternative="split-into-multiple-subagents">Would fragment the fresh-context verification workflow that must operate as single unit</rejected>
    <rejected alternative="truncate-documentation">Would lose XML parsing protocols critical for EPIC-046 compliance</rejected>
    <trade_off>4-6 reference files to maintain, but maintains single-responsibility fresh-context verification</trade_off>
  </decision>

  <hypothesis id="H1" validation="line-count-and-verification-accuracy" success_criteria="Core file ≤300 lines with all verification workflows preserved, zero regression in AC compliance verification accuracy">
    Progressive disclosure will enable constitutional compliance while maintaining ac-compliance-verifier's role as independent quality gate
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Core File Size Compliance

```xml
<acceptance_criteria id="AC1" implements="ADR-012-CORE-SIZE">
  <given>The ac-compliance-verifier.md subagent currently has 1,165 lines (233% over 500-line max)</given>
  <when>The refactoring is complete and the core file is validated</when>
  <then>The core file `src/claude/agents/ac-compliance-verifier.md` contains 300 lines or fewer, with all required sections: YAML frontmatter, Purpose, When Invoked, Fresh-Context Technique, Core Verification Workflow (condensed with reference pointers), Success Criteria, Error Handling, Reference Loading, and Observation Capture</then>
  <verification>
    <source_files>
      <file hint="Refactored core subagent">src/claude/agents/ac-compliance-verifier.md</file>
    </source_files>
    <test_file>tests/STORY-334/test_ac1_core_file_size.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Reference Directory Structure

```xml
<acceptance_criteria id="AC2" implements="ADR-012-DIR-STRUCTURE">
  <given>The ac-compliance-verifier requires extensive documentation for XML parsing protocol, verification workflows, scoring methodology, and report generation that exceeds core file limits</given>
  <when>The references directory is created per ADR-012 approved pattern</when>
  <then>A `src/claude/agents/ac-compliance-verifier/references/` directory exists containing 4-6 reference files covering: xml-parsing-protocol.md (EPIC-046 XML AC format extraction), verification-workflow.md (Phase 4.5/5.5 execution steps), scoring-methodology.md (evidence evaluation, confidence scoring), report-generation.md (JSON report format, gap documentation), and verification-hints.md (source_files element usage, test file mapping)</then>
  <verification>
    <source_files>
      <file hint="Reference directory">src/claude/agents/ac-compliance-verifier/references/</file>
    </source_files>
    <test_file>tests/STORY-334/test_ac2_reference_directory.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Functionality Preservation (No Regression)

```xml
<acceptance_criteria id="AC3" implements="ADR-012-NO-REGRESSION">
  <given>The original ac-compliance-verifier.md has documented workflows for fresh-context verification, XML AC parsing (EPIC-046), evidence collection, confidence scoring, and JSON report generation</given>
  <when>The refactored core file and references are loaded together</when>
  <then>All original functionality is preserved: fresh-context technique enforcement, XML AC block detection and parsing (given/when/then extraction), verification hints processing (source_files, test_file, coverage_threshold), evidence collection from source code, confidence scoring methodology, Phase 4.5/5.5 workflow integration, and JSON verification report generation</then>
  <verification>
    <source_files>
      <file hint="Refactored core">src/claude/agents/ac-compliance-verifier.md</file>
      <file hint="Reference files">src/claude/agents/ac-compliance-verifier/references/*.md</file>
    </source_files>
    <test_file>tests/STORY-334/test_ac3_functionality_preservation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Reference Loading Pattern Implementation

```xml
<acceptance_criteria id="AC4" implements="ADR-012-REF-LOADING">
  <given>References must be loaded on-demand when the subagent needs them for specific verification scenarios</given>
  <when>A developer reviews the core ac-compliance-verifier.md file</when>
  <then>The core file contains a "Reference Loading" section with explicit Read() instructions pointing to each reference file, with clear context about when each reference should be loaded: xml-parsing-protocol for AC extraction, verification-workflow for full verification execution, scoring-methodology for evidence evaluation, report-generation for JSON output creation, and verification-hints for source_files processing</then>
  <verification>
    <source_files>
      <file hint="Reference loading section">src/claude/agents/ac-compliance-verifier.md</file>
    </source_files>
    <test_file>tests/STORY-334/test_ac4_reference_loading.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Observation Capture Section (EPIC-052 Compliance)

```xml
<acceptance_criteria id="AC5" implements="EPIC-052-OBSERVATION">
  <given>Per EPIC-052, all high-frequency subagents must include Observation Capture sections, and ac-compliance-verifier is invoked during Phase 4.5 and Phase 5.5 of every TDD workflow</given>
  <when>The refactored ac-compliance-verifier.md is reviewed</when>
  <then>The core file contains an "Observation Capture (MANDATORY)" section with the standard observation schema (7 categories: friction, success, pattern, gap, idea, bug, warning), severity levels (low, medium, high), optional files array, and explicit Write() instructions for persisting observations</then>
  <verification>
    <source_files>
      <file hint="Observation section">src/claude/agents/ac-compliance-verifier.md</file>
    </source_files>
    <test_file>tests/STORY-334/test_ac5_observation_capture.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Operational Copy Synchronization

```xml
<acceptance_criteria id="AC6" implements="SOURCE-TREE-MIRROR">
  <given>DevForgeAI maintains dual locations per source-tree.md: src/claude/agents/ (source) and .claude/agents/ (operational)</given>
  <when>The refactoring is complete</when>
  <then>Both `src/claude/agents/ac-compliance-verifier.md` and `.claude/agents/ac-compliance-verifier.md` are identical, AND both reference directories `src/claude/agents/ac-compliance-verifier/references/` and `.claude/agents/ac-compliance-verifier/references/` contain identical files</then>
  <verification>
    <source_files>
      <file hint="Source core">src/claude/agents/ac-compliance-verifier.md</file>
      <file hint="Operational core">.claude/agents/ac-compliance-verifier.md</file>
      <file hint="Source references">src/claude/agents/ac-compliance-verifier/references/</file>
      <file hint="Operational references">.claude/agents/ac-compliance-verifier/references/</file>
    </source_files>
    <test_file>tests/STORY-334/test_ac6_sync_verification.sh</test_file>
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
      name: "ac-compliance-verifier.md (core)"
      file_path: "src/claude/agents/ac-compliance-verifier.md"
      purpose: "Subagent for fresh-context acceptance criteria verification in Phase 4.5/5.5"
      required_keys:
        - key: "YAML frontmatter"
          type: "yaml_block"
          required: true
          validation: "Must contain name, description, tools (Read, Grep, Glob), model"
          test_requirement: "Test: YAML parse succeeds, required fields present"
        - key: "Purpose section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Purpose header exists"
        - key: "When Invoked section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## When Invoked header exists"
        - key: "Fresh-Context Technique section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Fresh-Context Technique header exists"
        - key: "Core Verification Workflow section"
          type: "markdown_section"
          required: true
          test_requirement: "Test: ## Core Verification Workflow header exists"
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
          description: "All 9 required sections present"
          testable: true
          test_requirement: "Test: Grep for all 9 section headers"
          priority: "Critical"
        - id: "CORE-003"
          description: "Reference loading uses explicit Read() syntax"
          testable: true
          test_requirement: "Test: Grep for Read(file_path=\"src/claude/agents/ac-compliance-verifier/references/"
          priority: "High"

    - type: "Configuration"
      name: "ac-compliance-verifier references"
      file_path: "src/claude/agents/ac-compliance-verifier/references/"
      purpose: "Extracted documentation for progressive disclosure"
      required_keys:
        - key: "xml-parsing-protocol.md"
          type: "file"
          required: true
          description: "EPIC-046 XML AC format, given/when/then extraction"
          test_requirement: "Test: File exists and contains XML parsing rules"
        - key: "verification-workflow.md"
          type: "file"
          required: true
          description: "Phase 4.5/5.5 execution steps, evidence collection"
          test_requirement: "Test: File exists and contains workflow steps"
        - key: "scoring-methodology.md"
          type: "file"
          required: true
          description: "Evidence evaluation, confidence levels, scoring rules"
          test_requirement: "Test: File exists and contains scoring methodology"
        - key: "report-generation.md"
          type: "file"
          required: true
          description: "JSON report format, gap documentation, output structure"
          test_requirement: "Test: File exists and contains report format"
        - key: "verification-hints.md"
          type: "file"
          required: false
          description: "Optional: source_files element processing, test file mapping"
          test_requirement: "Test: If file exists, contains verification hints"
      requirements:
        - id: "REF-001"
          description: "4-6 reference files in references/ directory"
          testable: true
          test_requirement: "Test: Count files in references/ is between 4 and 6"
          priority: "Critical"
        - id: "REF-002"
          description: "All reference files use lowercase-hyphen naming"
          testable: true
          test_requirement: "Test: ls references/ | grep -vE '^[a-z][a-z0-9-]*\\.md$' returns 0 matches"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Fresh-context technique must be enforced - no prior knowledge of coding details"
      trigger: "When ac-compliance-verifier begins verification"
      validation: "Core file explicitly states fresh-context requirement"
      error_handling: "If prior context detected, warn and proceed with caution flag"
      test_requirement: "Test: Fresh-context section exists and contains explicit instructions"
      priority: "Critical"
    - id: "BR-002"
      rule: "XML AC parsing must follow EPIC-046 schema"
      trigger: "When parsing story acceptance criteria"
      validation: "Extract given/when/then from XML blocks, not legacy markdown"
      error_handling: "If XML AC blocks not found, mark story as non-compliant"
      test_requirement: "Test: XML parsing protocol correctly extracts all three elements"
      priority: "Critical"
    - id: "BR-003"
      rule: "Verification report must be generated in JSON format"
      trigger: "When verification workflow completes"
      validation: "JSON output follows documented schema"
      error_handling: "Invalid JSON triggers validation error"
      test_requirement: "Test: Generated report is valid JSON with required fields"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Token consumption for core file load reduced by 60%+"
      metric: "Core file <= 15,000 tokens (vs ~46,000 original)"
      test_requirement: "Test: Estimate tokens from line count (4 chars/token avg)"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "100% backward compatibility with existing invocations"
      metric: "0 breaking changes to Task(subagent_type=\"ac-compliance-verifier\") calls"
      test_requirement: "Test: Existing invocation patterns still work"
      priority: "Critical"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Single source of truth maintained"
      metric: "src/ and .claude/ copies are identical (diff = 0)"
      test_requirement: "Test: diff -r src/claude/agents/ac-compliance-verifier .claude/agents/ac-compliance-verifier returns empty"
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
- Core file load: <= 15,000 tokens (vs ~46,000 tokens for current 1,165 lines)
- Target reduction: >= 60% compared to original
- Selective loading: Only load references needed for specific scenario
- Reference loading latency: < 100ms per file

**Verification Impact:**
- ac-compliance-verifier is invoked twice per TDD workflow (Phase 4.5 and Phase 5.5)
- 60% token reduction per invocation = significant cumulative savings

---

### Security

**No sensitive data:** Reference files must not contain API keys, secrets, or credentials
**File paths:** All reference pointers use paths relative to project root
**No execution vectors:** Reference files are documentation only (Markdown)
**Fresh-context security:** Verification must not be influenced by prior context

---

### Reliability

**Graceful degradation:** If a reference file is missing, core file provides inline fallback guidance
**Backward compatible:** 100% of existing `Task(subagent_type="ac-compliance-verifier", ...)` invocations work unchanged
**Self-contained core:** Core file is functional for basic verification without references
**No silent failures:** Reference loading failures must log visible warnings

---

### Maintainability

**Single source of truth:** `src/claude/agents/` is source, `.claude/agents/` is mirror
**Reference isolation:** Each reference file covers one topic (single responsibility)
**Cross-reference consistency:** All reference pointers in core file point to files that exist
**Update path clear:** When verification functionality changes, clear which reference file to update

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
2. **AC2 - Reference Directory:** Verify 4-6 files exist with correct naming
3. **AC3 - Functionality:** Verify all verification features documented (XML parsing, evidence collection, scoring)
4. **AC4 - Reference Loading:** Verify Read() calls present for all references
5. **AC5 - Observation Capture:** Verify 7 categories and observation schema present
6. **AC6 - Sync:** Verify src/ and .claude/ are identical

### Edge Cases

1. **XML AC Block Detection:** Multiple AC blocks in single story handled correctly
2. **Missing Given/When/Then:** Incomplete AC blocks flagged appropriately
3. **Verification Hints Present:** source_files element processed correctly
4. **Verification Hints Absent:** Graceful handling when no hints provided
5. **Reference File Missing:** Fallback guidance provided
6. **Phase 4.5 vs 5.5:** Different verification contexts handled correctly

---

## Acceptance Criteria Verification Checklist

### AC#1: Core File Size Compliance

- [x] Original file analyzed (1,165 lines) - **Phase:** 2 - **Evidence:** wc -l output shows 1,165 lines
- [x] Required sections identified (9 total) - **Phase:** 2 - **Evidence:** YAML frontmatter, Purpose, When Invoked, Fresh-Context Technique, Core Verification Workflow, Success Criteria, Error Handling, Reference Loading, Observation Capture
- [x] Core file refactored to <= 300 lines - **Phase:** 3 - **Evidence:** wc -l shows 202 lines
- [x] All 9 required sections present - **Phase:** 4 - **Evidence:** Grep validation passed

### AC#2: Reference Directory Structure

- [x] Directory created at src/claude/agents/ac-compliance-verifier/references/ - **Phase:** 3 - **Evidence:** Directory exists
- [x] 4-6 reference files created - **Phase:** 3 - **Evidence:** 4 files (xml-parsing-protocol.md, verification-workflow.md, scoring-methodology.md, report-generation.md)
- [x] All files use lowercase-hyphen naming - **Phase:** 4 - **Evidence:** ls validation passed

### AC#3: Functionality Preservation

- [x] Fresh-context technique documented - **Phase:** 5 - **Evidence:** Core file lines 28-46
- [x] XML parsing protocol documented - **Phase:** 5 - **Evidence:** xml-parsing-protocol.md (165 lines)
- [x] Verification workflow documented - **Phase:** 5 - **Evidence:** verification-workflow.md (359 lines)
- [x] Scoring methodology documented - **Phase:** 5 - **Evidence:** scoring-methodology.md (230 lines)
- [x] Report generation documented - **Phase:** 5 - **Evidence:** report-generation.md (190 lines)

### AC#4: Reference Loading Pattern

- [x] Reference Loading section exists - **Phase:** 3 - **Evidence:** ## Reference Loading header present
- [x] Read() calls present for each reference - **Phase:** 4 - **Evidence:** 10 Read() calls found

### AC#5: Observation Capture Section

- [x] Observation Capture section exists - **Phase:** 3 - **Evidence:** ## Observation Capture header present
- [x] 7 categories present - **Phase:** 4 - **Evidence:** friction, success, pattern, gap, idea, bug, warning all present

### AC#6: Operational Copy Synchronization

- [x] src/ core matches .claude/ core - **Phase:** 5 - **Evidence:** diff returns no differences
- [x] src/ references match .claude/ references - **Phase:** 5 - **Evidence:** diff -rq shows 4 matching files

---

**Checklist Progress:** 18/18 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Core ac-compliance-verifier.md refactored to <= 300 lines
- [x] references/ directory created with 4-6 files
- [x] All required sections present in core file
- [x] Reference Loading section with Read() calls
- [x] Observation Capture section with 7 categories
- [x] src/ and .claude/ copies synchronized

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases handled (XML parsing, missing hints, etc.)
- [x] No functionality regression (all verification features work)
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

- [x] Core ac-compliance-verifier.md refactored to <= 300 lines - Completed: 202 lines (83% reduction from 1,165)
- [x] references/ directory created with 4-6 files - Completed: 4 files (xml-parsing-protocol.md, verification-workflow.md, scoring-methodology.md, report-generation.md)
- [x] All required sections present in core file - Completed: 9 sections verified present
- [x] Reference Loading section with Read() calls - Completed: 10 Read() calls for 4 references
- [x] Observation Capture section with 7 categories - Completed: friction, success, pattern, gap, idea, bug, warning
- [x] src/ and .claude/ copies synchronized - Completed: Both locations have identical core + 4 references
- [x] All 6 acceptance criteria have passing tests - Completed: 6/6 tests GREEN
- [x] Edge cases handled (XML parsing, missing hints, etc.) - Completed: Documented in reference files
- [x] No functionality regression (all verification features work) - Completed: Integration tests passed
- [x] Token reduction >= 60% verified - Completed: 83% reduction achieved
- [x] Test: Core file line count <= 300 - Completed: test-ac1-core-file-size.sh PASSED
- [x] Test: Reference directory structure valid - Completed: test-ac2-reference-directory.sh PASSED
- [x] Test: Functionality preservation checklist - Completed: test-ac3-functionality-preservation.sh PASSED
- [x] Test: Reference loading pattern present - Completed: test-ac4-reference-loading.sh PASSED
- [x] Test: Observation capture schema complete - Completed: test-ac5-observation-capture.sh PASSED
- [x] Test: Sync between src/ and .claude/ - Completed: test-ac6-sync-verification.sh PASSED
- [x] Reference files documented (one topic per file) - Completed: 4 single-topic reference files
- [x] Core file condensed workflow clear - Completed: Core file has clear step-by-step workflow
- [x] Reference loading instructions explicit - Completed: ## Reference Loading section with context guidance

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-30 10:00 | claude/story-requirements-analyst | Created | Story created from EPIC-053 Feature 4 | STORY-334.story.md |
| 2026-01-31 12:00 | claude/dev | Dev Complete | Refactored ac-compliance-verifier.md with progressive disclosure | src/claude/agents/ac-compliance-verifier.md, src/claude/agents/ac-compliance-verifier/references/*.md, .claude/agents/ac-compliance-verifier.md, .claude/agents/ac-compliance-verifier/references/*.md, tests/STORY-334/*.sh |
| 2026-01-31 12:37 | claude/qa-result-interpreter | QA Deep | PASSED: 6/6 tests, 100% traceability, 2/2 validators | - |
| 2026-01-31 12:45 | claude/qa | QA Failed | REVERTED: code-reviewer found CRITICAL path issue - 8 Read() calls reference src/claude/agents/ instead of .claude/agents/ | .claude/agents/ac-compliance-verifier.md |
| 2026-01-31 13:15 | claude/dev | Remediation | Fixed 8 CRITICAL path violations: Changed all Read() paths from src/claude/agents/ to .claude/agents/ | .claude/agents/ac-compliance-verifier.md, src/claude/agents/ac-compliance-verifier.md |
| 2026-01-31 13:50 | claude/qa-result-interpreter | QA Deep | PASSED: 6/6 tests, 100% traceability, 2/2 validators (code-reviewer, security-auditor) | - |

## Notes

**Design Decisions:**
- 4-6 reference files provide good balance for ac-compliance-verifier scope
- Core file targets 200-250 lines to leave buffer under 300-line limit
- Fresh-context technique remains in core (critical for all invocations)
- XML parsing gets dedicated reference due to EPIC-046 complexity

**Extraction Strategy:**
1. **xml-parsing-protocol.md** - EPIC-046 XML AC format, extraction rules (~300 lines)
2. **verification-workflow.md** - Phase 4.5/5.5 execution steps, evidence collection (~350 lines)
3. **scoring-methodology.md** - Evidence evaluation, confidence levels (~200 lines)
4. **report-generation.md** - JSON report format, gap documentation (~150 lines)
5. **verification-hints.md** - Optional: source_files processing (~100 lines)

**Total extracted:** ~1,100 lines → Core file ~200 lines (fits 300-line target with margin)

**Related Stories:**
- EPIC-046: AC Compliance Verification System (feature preserved)
- STORY-330: Constitutional update (prerequisite)

**Related ADRs:**
- [ADR-012: Subagent Progressive Disclosure Architecture](../adrs/ADR-012-subagent-progressive-disclosure.md)

**References:**
- EPIC-053: Subagent Progressive Disclosure Refactoring
- RESEARCH-006: Subagent Progressive Disclosure Analysis

---

Story Template Version: 2.7
Last Updated: 2026-01-30
