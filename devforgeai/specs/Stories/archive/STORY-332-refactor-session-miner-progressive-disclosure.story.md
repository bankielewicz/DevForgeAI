---
id: STORY-332
title: Refactor session-miner.md with Progressive Disclosure
type: refactor
epic: EPIC-053
sprint: Sprint-2
status: QA Approved
points: 3
depends_on: ["STORY-330"]
priority: High
assigned_to: TBD
created: 2026-01-29
format_version: "2.7"
---

# Story: Refactor session-miner.md with Progressive Disclosure

## Description

**As a** DevForgeAI framework maintainer,
**I want** session-miner.md refactored from 1,860 lines to a core file of 300 lines or fewer with extracted reference documentation,
**so that** token consumption per subagent invocation is reduced by 60%+ while maintaining full session mining functionality for EPIC-034 insights.

## Provenance

```xml
<provenance>
  <origin document="EPIC-053" section="Feature 2: Refactor session-miner.md">
    <quote>"Lines: 1,860 → ≤300 (core) + references/. Problem: 372% over maximum. Solution: Extract workflow-specific documentation to references. Business Value: Second highest impact"</quote>
    <line_reference>lines 70-75</line_reference>
    <quantified_impact>1,860 → ≤300 lines = 84% reduction in core file, 60%+ token savings per invocation</quantified_impact>
  </origin>

  <decision rationale="progressive-disclosure-pattern">
    <selected>Extract documentation to references/ subdirectory per ADR-012 pattern</selected>
    <rejected alternative="split-into-multiple-subagents">Would fragment session mining functionality</rejected>
    <rejected alternative="truncate-documentation">Would lose critical error categorization and analysis workflows</rejected>
    <trade_off>5-8 reference files to maintain, but 60-80% token reduction per invocation</trade_off>
  </decision>

  <hypothesis id="H1" validation="line-count-measurement" success_criteria="Core file ≤300 lines with all session mining functionality preserved">
    Progressive disclosure will enable constitutional compliance while maintaining full session data mining capabilities
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Core File Size Compliance

```xml
<acceptance_criteria id="AC1" implements="ADR-012-CORE-SIZE">
  <given>The current session-miner.md file has 1,860 lines (372% over the 500-line constitutional maximum)</given>
  <when>The refactoring is complete</when>
  <then>The core src/claude/agents/session-miner.md file contains 300 lines or fewer, with all MANDATORY sections: YAML frontmatter, Purpose, When Invoked, Core Workflow, Success Criteria, Error Handling, Reference Loading, and Observation Capture</then>
  <verification>
    <source_files>
      <file hint="Refactored core subagent">src/claude/agents/session-miner.md</file>
    </source_files>
    <test_file>tests/STORY-332/test_ac1_core_file_size.sh</test_file>
    <coverage_threshold>100</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Reference Directory Structure

```xml
<acceptance_criteria id="AC2" implements="ADR-012-DIR-STRUCTURE">
  <given>The progressive disclosure pattern defined in ADR-012 requires extracted documentation in a references subdirectory</given>
  <when>The reference files are created</when>
  <then>Directory src/claude/agents/session-miner/references/ exists with 5-8 reference files covering: parsing-workflow.md, query-patterns.md, output-formats.md, error-handling.md, session-analysis.md, and additional topic-specific references as needed</then>
  <verification>
    <source_files>
      <file hint="Reference directory">src/claude/agents/session-miner/references/</file>
    </source_files>
    <test_file>tests/STORY-332/test_ac2_reference_directory.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Reference Loading Instructions

```xml
<acceptance_criteria id="AC3" implements="ADR-012-REF-LOADING">
  <given>The core session-miner.md file must instruct invokers how to load detailed documentation</given>
  <when>A subagent consumer needs detailed workflow information</when>
  <then>The core file contains a "Reference Loading" section with explicit Read() instructions for each major feature (parsing, error categorization, N-gram analysis, anti-pattern mining), using paths like src/claude/agents/session-miner/references/{topic}.md</then>
  <verification>
    <source_files>
      <file hint="Reference loading section">src/claude/agents/session-miner.md</file>
    </source_files>
    <test_file>tests/STORY-332/test_ac3_reference_loading.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Functionality Preservation (No Regression)

```xml
<acceptance_criteria id="AC4" implements="ADR-012-NO-REGRESSION">
  <given>Session-miner provides SessionEntry parsing, pagination, error categorization (STORY-229), N-gram analysis (STORY-226), and anti-pattern mining (STORY-231)</given>
  <when>The refactoring is complete</when>
  <then>All existing functionality is documented across core file and references with no algorithm, workflow, or data model removed, and all integration points with downstream stories (STORY-222 through STORY-231) remain documented</then>
  <verification>
    <source_files>
      <file hint="Refactored core">src/claude/agents/session-miner.md</file>
      <file hint="Reference files">src/claude/agents/session-miner/references/*.md</file>
    </source_files>
    <test_file>tests/STORY-332/test_ac4_functionality_preservation.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Observation Capture Section (EPIC-052 Compliance)

```xml
<acceptance_criteria id="AC5" implements="EPIC-052-OBSERVATION">
  <given>EPIC-052 mandates that all high-frequency subagents include Observation Capture sections</given>
  <when>The core file is created</when>
  <then>The core session-miner.md includes a complete "Observation Capture (MANDATORY)" section with the standard observation schema (7 categories: friction, success, pattern, gap, idea, bug, warning), severity levels, and the 3-step workflow (Construct JSON, Write to Disk, Verify Write)</then>
  <verification>
    <source_files>
      <file hint="Observation section">src/claude/agents/session-miner.md</file>
    </source_files>
    <test_file>tests/STORY-332/test_ac5_observation_capture.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Operational Copy Synchronization

```xml
<acceptance_criteria id="AC6" implements="SOURCE-TREE-MIRROR">
  <given>DevForgeAI maintains operational copies in .claude/ that mirror src/claude/</given>
  <when>The refactoring is complete</when>
  <then>Both src/claude/agents/session-miner.md and .claude/agents/session-miner.md are identical, AND both reference directories contain identical files with zero differences in a recursive diff</then>
  <verification>
    <source_files>
      <file hint="Source core">src/claude/agents/session-miner.md</file>
      <file hint="Operational core">.claude/agents/session-miner.md</file>
      <file hint="Source references">src/claude/agents/session-miner/references/</file>
      <file hint="Operational references">.claude/agents/session-miner/references/</file>
    </source_files>
    <test_file>tests/STORY-332/test_ac6_sync_verification.sh</test_file>
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
      name: "session-miner.md (core)"
      file_path: "src/claude/agents/session-miner.md"
      purpose: "Subagent for parsing and mining Claude Code history.jsonl session data"
      required_keys:
        - key: "YAML frontmatter"
          type: "yaml_block"
          required: true
          validation: "Must contain name, description, tools, model, proactive_triggers"
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
          test_requirement: "Test: Grep for Read(file_path=\"src/claude/agents/session-miner/references/"
          priority: "High"

    - type: "Configuration"
      name: "session-miner references"
      file_path: "src/claude/agents/session-miner/references/"
      purpose: "Extracted documentation for progressive disclosure"
      required_keys:
        - key: "parsing-workflow.md"
          type: "file"
          required: true
          description: "JSON Lines parsing workflow, SessionEntry extraction, pagination"
          test_requirement: "Test: File exists and contains Steps 1-6 parsing workflow"
        - key: "query-patterns.md"
          type: "file"
          required: true
          description: "Query and extraction pattern documentation"
          test_requirement: "Test: File exists and is valid markdown"
        - key: "output-formats.md"
          type: "file"
          required: true
          description: "SessionEntry schema, response structures"
          test_requirement: "Test: File exists and contains JSON schema examples"
        - key: "error-handling.md"
          type: "file"
          required: true
          description: "STORY-229 error categorization, ErrorEntry model"
          test_requirement: "Test: File exists and contains error classification rules"
        - key: "session-analysis.md"
          type: "file"
          required: true
          description: "STORY-226 N-gram sequence analysis"
          test_requirement: "Test: File exists and contains bigram/trigram extraction"
      requirements:
        - id: "REF-001"
          description: "5-8 reference files in references/ directory"
          testable: true
          test_requirement: "Test: Count files in references/ is between 5 and 8"
          priority: "Critical"
        - id: "REF-002"
          description: "All reference files use kebab-case naming"
          testable: true
          test_requirement: "Test: ls references/ | grep -v '^[a-z][a-z0-9-]*\\.md$' returns 0 matches"
          priority: "High"
        - id: "REF-003"
          description: "Each reference file has YAML frontmatter with parent field"
          testable: true
          test_requirement: "Test: Each file contains 'parent: session-miner' in frontmatter"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Error categorization logic from STORY-229 must be fully preserved in error-handling.md"
      trigger: "When extracting error categorization documentation"
      validation: "ErrorEntry model, classification rules, and severity assignment all present"
      error_handling: "Missing categorization logic blocks completion"
      test_requirement: "Test: error-handling.md contains all STORY-229 specifications"
      priority: "Critical"
    - id: "BR-002"
      rule: "N-gram analysis workflow from STORY-226 must be fully preserved in session-analysis.md"
      trigger: "When extracting session analysis documentation"
      validation: "Bigram/trigram extraction, success rate calculation, top patterns report"
      error_handling: "Missing analysis steps blocks completion"
      test_requirement: "Test: session-analysis.md contains all STORY-226 specifications"
      priority: "High"
    - id: "BR-003"
      rule: "Pagination parameters for large file processing must remain accessible"
      trigger: "When processing 86MB+ history.jsonl files"
      validation: "Chunked processing workflow documented in parsing-workflow.md"
      error_handling: "Missing pagination logic causes large file processing failure"
      test_requirement: "Test: parsing-workflow.md contains pagination loop examples"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Token consumption for core file load reduced by 60%+"
      metric: "Core file <= 12,000 characters (vs ~74,400 original)"
      test_requirement: "Test: wc -c returns <= 12000 for core file"
      priority: "High"
    - id: "NFR-002"
      category: "Reliability"
      requirement: "100% backward compatibility with existing invocations"
      metric: "0 breaking changes to Task(subagent_type=\"session-miner\") calls"
      test_requirement: "Test: Existing invocation patterns still work"
      priority: "Critical"
    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Single source of truth maintained"
      metric: "src/ and .claude/ copies are identical (diff = 0)"
      test_requirement: "Test: diff -r src/claude/agents/session-miner .claude/agents/session-miner returns empty"
      priority: "High"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Large file processing unchanged"
      metric: "86MB file processing completes in <30 seconds (unchanged from current)"
      test_requirement: "Test: Processing time for large files within bounds"
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
- Core file load: <= 12,000 characters (vs ~74,400 characters for current 1,860 lines)
- Target reduction: >= 60% compared to original
- Reference loading: Additional tokens per reference file loaded on-demand
- Large file processing: 86MB history.jsonl in <30 seconds (unchanged)

---

### Security

**No sensitive data:** Session-miner performs read-only operations on history.jsonl
**Reference files:** Inherit same access controls as parent subagent
**No credentials:** No API keys, secrets, or credentials in any files

---

### Reliability

**Zero regression:** All existing session-miner functionality must work identically
**Complete references:** No truncated algorithms or partial workflows
**Observation Capture:** Non-blocking (failures logged but don't halt execution)

---

### Maintainability

**Single source of truth:** `src/claude/agents/` is source, `.claude/agents/` is mirror
**Reference isolation:** Each reference file covers one topic (single responsibility)
**Independent maintenance:** Reference files can be updated without core file changes

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
2. **AC2 - Reference Directory:** Verify 5-8 files exist with correct naming
3. **AC3 - Reference Loading:** Verify Read() calls present for all references
4. **AC4 - Functionality:** Verify all session mining features documented
5. **AC5 - Observation Capture:** Verify 7 categories and 3-step workflow present
6. **AC6 - Sync:** Verify src/ and .claude/ are identical

### Edge Cases

1. **Error Categorization Split:** STORY-229 (435 lines) extracted to error-handling.md
2. **Anti-Pattern Mining Split:** STORY-231 (856 lines) extracted to dedicated reference
3. **Cross-Reference Integrity:** SessionEntry model accessible from multiple references
4. **Pagination API:** Large file processing examples remain accessible
5. **N-gram Analysis:** STORY-226 workflow extracted to session-analysis.md
6. **Unicode Handling:** Edge case handling preserved in references

---

## Acceptance Criteria Verification Checklist

### AC#1: Core File Size Compliance

- [x] Original file analyzed (1,860 lines) - **Phase:** 2 - **Evidence:** wc -l output confirms 1,860 lines
- [x] Required sections identified (8 total) - **Phase:** 2 - **Evidence:** YAML, Purpose, When Invoked, Workflow, Success Criteria, Error Handling, Reference Loading, Observation Capture
- [x] Core file refactored to <= 300 lines - **Phase:** 3 - **Evidence:** 233 lines (wc -l output)
- [x] All 8 required sections present - **Phase:** 4 - **Evidence:** Grep validation passed

### AC#2: Reference Directory Structure

- [x] Directory created at src/claude/agents/session-miner/references/ - **Phase:** 3 - **Evidence:** ls output
- [x] 5-8 reference files created - **Phase:** 3 - **Evidence:** 6 files
- [x] All files use kebab-case naming - **Phase:** 4 - **Evidence:** ls validation passed

### AC#3: Reference Loading Instructions

- [x] Reference Loading section exists - **Phase:** 3 - **Evidence:** Lines 85-128
- [x] Read() calls present for each reference - **Phase:** 4 - **Evidence:** 6 Read() calls found

### AC#4: Functionality Preservation

- [x] SessionEntry parsing documented - **Phase:** 5 - **Evidence:** parsing-workflow.md (281 lines)
- [x] Error categorization documented - **Phase:** 5 - **Evidence:** error-handling.md (351 lines)
- [x] N-gram analysis documented - **Phase:** 5 - **Evidence:** session-analysis.md (293 lines)
- [x] Anti-pattern mining documented - **Phase:** 5 - **Evidence:** anti-pattern-mining.md (461 lines)

### AC#5: Observation Capture Section

- [x] Observation Capture section exists - **Phase:** 3 - **Evidence:** Lines 182-211
- [x] 7 categories present - **Phase:** 4 - **Evidence:** friction, success, pattern, gap, idea, bug, warning
- [x] 3-step workflow documented - **Phase:** 4 - **Evidence:** Construct JSON, Write to Disk, Verify Write

### AC#6: Operational Copy Synchronization

- [x] src/ core matches .claude/ core - **Phase:** 5 - **Evidence:** diff returns empty
- [x] src/ references match .claude/ references - **Phase:** 5 - **Evidence:** diff -r returns empty

---

**Checklist Progress:** 18/18 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Core session-miner.md refactored to <= 300 lines
- [x] references/ directory created with 5-8 files
- [x] All required sections present in core file
- [x] Reference Loading section with Read() calls
- [x] Observation Capture section with 7 categories
- [x] src/ and .claude/ copies synchronized

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases handled (error categorization, N-gram analysis, etc.)
- [x] No functionality regression (all session mining features work)
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

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-29 09:30 | claude/story-requirements-analyst | Created | Story created from EPIC-053 Feature 2 | STORY-332.story.md |
| 2026-01-30 | claude/opus | Development Complete | TDD workflow complete, all 6 ACs verified | session-miner.md, references/*.md |
| 2026-01-30 | claude/qa-result-interpreter | QA Deep | PASSED: 40/40 tests, 0 violations, 2/2 validators | STORY-332-qa-report.md |

## Implementation Notes

- [x] Core session-miner.md refactored to <= 300 lines - Completed: 233 lines (87.5% reduction from 1,860 lines)
- [x] references/ directory created with 5-8 files - Completed: 6 reference files (1,903 lines total)
- [x] All required sections present in core file - Completed: All 8 MANDATORY sections verified
- [x] Reference Loading section with Read() calls - Completed: 6 explicit Read() calls documented
- [x] Observation Capture section with 7 categories - Completed: friction, success, pattern, gap, idea, bug, warning
- [x] src/ and .claude/ copies synchronized - Completed: diff returns empty for core and references
- [x] All 6 acceptance criteria have passing tests - Completed: 40 tests across 7 test files
- [x] Edge cases handled (error categorization, N-gram analysis, etc.) - Completed: STORY-229, STORY-226, STORY-231 features preserved
- [x] No functionality regression (all session mining features work) - Completed: integration-tester verified
- [x] Token reduction >= 60% verified - Completed: 87% reduction (~74,400 -> ~9,300 chars)
- [x] Test: Core file line count <= 300 - Completed: test_ac1_core_file_size.sh PASSED
- [x] Test: Reference directory structure valid - Completed: test_ac2_reference_directory.sh PASSED
- [x] Test: Functionality preservation checklist - Completed: test_ac4_functionality_preservation.sh PASSED
- [x] Test: Reference loading pattern present - Completed: test_ac3_reference_loading.sh PASSED
- [x] Test: Observation capture schema complete - Completed: test_ac5_observation_capture.sh PASSED
- [x] Test: Sync between src/ and .claude/ - Completed: test_ac6_sync_verification.sh PASSED
- [x] Reference files documented (one topic per file) - Completed: 6 files, each single-topic
- [x] Core file condensed workflow clear - Completed: 5-phase workflow in Core Workflow section
- [x] Reference loading instructions explicit - Completed: Table + Read() examples in Reference Loading section

**TDD Workflow Summary:**
- Phase 02 (Red): 7 test files generated with 40 test cases
- Phase 03 (Green): Implementation already complete from prior session
- Phase 04 (Refactor): No changes needed, clean implementation
- Phase 05 (Integration): All integration points verified

## Notes

**Design Decisions:**
- 5-8 reference files provide good balance for session-miner scope
- Core file targets 200-250 lines to leave buffer under 300-line limit
- Error categorization (STORY-229) gets dedicated reference due to complexity
- N-gram analysis (STORY-226) gets dedicated reference for discoverability

**Extraction Strategy:**
1. **parsing-workflow.md** - JSON Lines parsing, SessionEntry extraction, pagination (400+ lines)
2. **query-patterns.md** - Query and extraction patterns (200+ lines)
3. **output-formats.md** - Response schemas, success/error structures (150+ lines)
4. **error-handling.md** - STORY-229 error categorization complete (435+ lines)
5. **session-analysis.md** - STORY-226 N-gram sequence analysis (120+ lines)
6. **anti-pattern-mining.md** - STORY-231 anti-pattern detection (400+ lines)

**Related Stories:**
- STORY-222 through STORY-231: Session mining integration points
- STORY-330: Constitutional update (prerequisite)

**Related ADRs:**
- [ADR-012: Subagent Progressive Disclosure Architecture](../adrs/ADR-012-subagent-progressive-disclosure.md)

**References:**
- EPIC-053: Subagent Progressive Disclosure Refactoring
- EPIC-034: Session Mining Insights (consuming epic)
- RESEARCH-006: Subagent Progressive Disclosure Analysis

---

Story Template Version: 2.7
Last Updated: 2026-01-29
