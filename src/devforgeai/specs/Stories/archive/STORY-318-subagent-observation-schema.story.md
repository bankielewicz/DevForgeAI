---
id: STORY-318
title: Add Observation Schema to High-Frequency Subagents
type: feature
epic: EPIC-051
sprint: Backlog
status: QA Approved
points: 8
depends_on: []
priority: High
assigned_to: null
created: 2026-01-26
updated: 2026-01-26
format_version: "2.7"
tags: [feedback-system, subagents, observations, EPIC-051]
---

# Story: Add Observation Schema to High-Frequency Subagents

## Description

**As a** Framework Architect (Claude),
**I want** high-frequency subagents to return optional observation data during execution,
**so that** insights about friction points, successes, and patterns are automatically captured without manual reflection or breaking existing invocations.

## Provenance

```xml
<provenance>
  <origin document="devforgeai/specs/brainstorms/BRAINSTORM-007-feedback-system-visibility.brainstorm.md" section="problem-statement">
    <quote>"Framework owners experience inability to see feedback from phases/subagents/workflows because subagents don't return observation data"</quote>
    <line_reference>EPIC-051 lines 37-39</line_reference>
    <quantified_impact>0% observation capture currently vs 80% target</quantified_impact>
  </origin>

  <decision rationale="retrofitting-priority">
    <selected>Add optional observations[] field to 4 high-frequency subagent contracts</selected>
    <rejected alternative="modify-all-subagents">Too broad scope, start with high-frequency subagents only</rejected>
    <trade_off>Limited to 4 subagents initially; may need expansion later</trade_off>
  </decision>

  <stakeholder role="Framework Owner" goal="see-feedback-automatically">
    <quote>"I want subagents to automatically return observations during execution"</quote>
    <source>EPIC-051, User Stories section</source>
  </stakeholder>

  <hypothesis id="H1" validation="observation-count" success_criteria="80% of completed stories have observations[]">
    Adding observation schema will enable automatic data capture without manual reflection
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: test-automator Observations Schema

```xml
<acceptance_criteria id="AC1" implements="SPEC-001">
  <given>The test-automator subagent specification file exists at `.claude/agents/test-automator.md`</given>
  <when>A developer reviews the Output section of the subagent specification</when>
  <then>The file contains a documented `observations:` YAML schema with all 7 category types (friction, success, pattern, gap, idea, bug, warning), severity levels (low, medium, high), and optional files array</then>
  <verification>
    <source_files>
      <file hint="Target subagent spec">.claude/agents/test-automator.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-318/test_ac1_test_automator_schema.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: code-reviewer Observations Schema

```xml
<acceptance_criteria id="AC2" implements="SPEC-002">
  <given>The code-reviewer subagent specification file exists at `.claude/agents/code-reviewer.md`</given>
  <when>A developer reviews the Output section of the subagent specification</when>
  <then>The file contains a documented `observations:` YAML schema with all 7 category types (friction, success, pattern, gap, idea, bug, warning), severity levels (low, medium, high), and optional files array</then>
  <verification>
    <source_files>
      <file hint="Target subagent spec">.claude/agents/code-reviewer.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-318/test_ac2_code_reviewer_schema.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: backend-architect Observations Schema

```xml
<acceptance_criteria id="AC3" implements="SPEC-003">
  <given>The backend-architect subagent specification file exists at `.claude/agents/backend-architect.md`</given>
  <when>A developer reviews the Output section of the subagent specification</when>
  <then>The file contains a documented `observations:` YAML schema with all 7 category types (friction, success, pattern, gap, idea, bug, warning), severity levels (low, medium, high), and optional files array</then>
  <verification>
    <source_files>
      <file hint="Target subagent spec">.claude/agents/backend-architect.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-318/test_ac3_backend_architect_schema.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: ac-compliance-verifier Observations Schema

```xml
<acceptance_criteria id="AC4" implements="SPEC-004">
  <given>The ac-compliance-verifier subagent specification file exists at `.claude/agents/ac-compliance-verifier.md`</given>
  <when>A developer reviews the Output section of the subagent specification</when>
  <then>The file contains a documented `observations:` YAML schema with all 7 category types (friction, success, pattern, gap, idea, bug, warning), severity levels (low, medium, high), and optional files array</then>
  <verification>
    <source_files>
      <file hint="Target subagent spec">.claude/agents/ac-compliance-verifier.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-318/test_ac4_ac_compliance_verifier_schema.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Backward Compatibility (Schema Optional)

```xml
<acceptance_criteria id="AC5" implements="BR-001">
  <given>Any of the 4 modified subagents are invoked WITHOUT returning observations</given>
  <when>The parent skill processes the subagent's response</when>
  <then>The workflow completes successfully without errors (observations field is optional, not required)</then>
  <verification>
    <source_files>
      <file hint="All 4 subagent specs">.claude/agents/test-automator.md</file>
      <file hint="All 4 subagent specs">.claude/agents/code-reviewer.md</file>
      <file hint="All 4 subagent specs">.claude/agents/backend-architect.md</file>
      <file hint="All 4 subagent specs">.claude/agents/ac-compliance-verifier.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-318/test_ac5_backward_compatibility.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Category Documentation Completeness

```xml
<acceptance_criteria id="AC6" implements="SPEC-005">
  <given>All 4 subagent files have been updated with the observations schema</given>
  <when>A developer searches for category documentation in any of the 4 files</when>
  <then>Each file documents all 7 observation categories with clear definitions: friction (pain points), success (things that worked), pattern (recurring approaches), gap (missing features), idea (improvements), bug (defects), warning (potential issues)</then>
  <verification>
    <source_files>
      <file hint="All 4 subagent specs">.claude/agents/test-automator.md</file>
      <file hint="All 4 subagent specs">.claude/agents/code-reviewer.md</file>
      <file hint="All 4 subagent specs">.claude/agents/backend-architect.md</file>
      <file hint="All 4 subagent specs">.claude/agents/ac-compliance-verifier.md</file>
    </source_files>
    <test_file>devforgeai/tests/STORY-318/test_ac6_category_completeness.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Specification"
      name: "test-automator observations schema"
      file_path: ".claude/agents/test-automator.md"
      purpose: "Add optional observations[] field to Output section"
      dependencies: []
      requirements:
        - id: "SPEC-001"
          description: "Add observations YAML schema to Output section"
          testable: true
          test_requirement: "Test: Grep search for 'observations:' in file returns match"
          priority: "Critical"
          implements_ac: ["AC#1"]
        - id: "SPEC-001-B"
          description: "Document all 7 observation categories with definitions"
          testable: true
          test_requirement: "Test: Grep search for each category name returns matches"
          priority: "Critical"
          implements_ac: ["AC#1", "AC#6"]

    - type: "Specification"
      name: "code-reviewer observations schema"
      file_path: ".claude/agents/code-reviewer.md"
      purpose: "Add optional observations[] field to Output section"
      dependencies: []
      requirements:
        - id: "SPEC-002"
          description: "Add observations YAML schema to Output section"
          testable: true
          test_requirement: "Test: Grep search for 'observations:' in file returns match"
          priority: "Critical"
          implements_ac: ["AC#2"]
        - id: "SPEC-002-B"
          description: "Document all 7 observation categories with definitions"
          testable: true
          test_requirement: "Test: Grep search for each category name returns matches"
          priority: "Critical"
          implements_ac: ["AC#2", "AC#6"]

    - type: "Specification"
      name: "backend-architect observations schema"
      file_path: ".claude/agents/backend-architect.md"
      purpose: "Add optional observations[] field to Output section"
      dependencies: []
      requirements:
        - id: "SPEC-003"
          description: "Add observations YAML schema to Output section"
          testable: true
          test_requirement: "Test: Grep search for 'observations:' in file returns match"
          priority: "Critical"
          implements_ac: ["AC#3"]
        - id: "SPEC-003-B"
          description: "Document all 7 observation categories with definitions"
          testable: true
          test_requirement: "Test: Grep search for each category name returns matches"
          priority: "Critical"
          implements_ac: ["AC#3", "AC#6"]

    - type: "Specification"
      name: "ac-compliance-verifier observations schema"
      file_path: ".claude/agents/ac-compliance-verifier.md"
      purpose: "Add optional observations[] field to Output section"
      dependencies: []
      requirements:
        - id: "SPEC-004"
          description: "Add observations YAML schema to Output section"
          testable: true
          test_requirement: "Test: Grep search for 'observations:' in file returns match"
          priority: "Critical"
          implements_ac: ["AC#4"]
        - id: "SPEC-004-B"
          description: "Document all 7 observation categories with definitions"
          testable: true
          test_requirement: "Test: Grep search for each category name returns matches"
          priority: "Critical"
          implements_ac: ["AC#4", "AC#6"]

  business_rules:
    - id: "BR-001"
      rule: "Observations field is optional - subagents must work without returning observations"
      trigger: "When subagent is invoked by parent skill"
      validation: "Existing invocations complete successfully without observations"
      error_handling: "No error if observations[] absent from response"
      test_requirement: "Test: Invoke subagent without observations, verify success"
      priority: "Critical"

    - id: "BR-002"
      rule: "Category must be exactly one of 7 valid enum values"
      trigger: "When observation is returned"
      validation: "Category in [friction, success, pattern, gap, idea, bug, warning]"
      error_handling: "Invalid category logged as warning, observation stored with category='unknown'"
      test_requirement: "Test: Verify all 7 categories documented in schema"
      priority: "High"

    - id: "BR-003"
      rule: "Severity must be exactly one of 3 valid enum values"
      trigger: "When observation is returned"
      validation: "Severity in [low, medium, high]"
      error_handling: "Invalid severity defaults to 'medium'"
      test_requirement: "Test: Verify all 3 severity levels documented in schema"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Schema documentation adds zero runtime overhead"
      metric: "0ms additional execution time (documentation only, no code execution)"
      test_requirement: "Test: N/A - documentation change only"
      priority: "Medium"

    - id: "NFR-002"
      category: "Compatibility"
      requirement: "100% backward compatible with existing subagent invocations"
      metric: "All existing invocations work unchanged"
      test_requirement: "Test: Run existing invocations, verify no errors"
      priority: "Critical"

    - id: "NFR-003"
      category: "Maintainability"
      requirement: "Schema consistency across all 4 subagents"
      metric: "Identical schema text in all 4 files"
      test_requirement: "Test: Compare schema sections across files for exact match"
      priority: "High"
```

### Observation Schema (Standard Text for All 4 Subagents)

The following schema should be added to the Output section of each subagent:

```yaml
# Optional observation output (EPIC-051)
# Subagents may return observations to capture insights during execution.
# This field is OPTIONAL - subagents work normally without it.
observations:
  - category: friction | success | pattern | gap | idea | bug | warning
    note: "Human-readable observation text (10-500 chars)"
    severity: low | medium | high
    files: ["optional/file/paths.md"]  # Files related to observation (0-10 items)

# Category Definitions:
#   friction  - Pain points, workflow interruptions, confusing behavior
#   success   - Things that worked well, positive patterns, effective approaches
#   pattern   - Recurring approaches, common solutions, best practices observed
#   gap       - Missing features, incomplete coverage, unmet needs
#   idea      - Improvement suggestions, enhancement opportunities
#   bug       - Defects found, unexpected behavior, errors encountered
#   warning   - Potential issues, risks, technical debt indicators

# Severity Levels:
#   low    - Minor observation, informational only
#   medium - Notable observation, may warrant attention
#   high   - Significant observation, should be reviewed

# Example:
# observations:
#   - category: friction
#     note: "Coverage analysis took 15 seconds, slowing feedback loop"
#     severity: medium
#     files: ["devforgeai/qa/coverage-report.json"]
#   - category: success
#     note: "AAA test pattern generated clean, readable tests"
#     severity: low
#     files: []
```

---

## Edge Cases & Error Handling

1. **Empty observations array:** When a subagent execution completes with no noteworthy observations to report, the subagent may return an empty `observations: []` array or omit the field entirely. Both approaches must be valid and not cause errors in downstream processing.

2. **Multiple observations per execution:** A single subagent invocation may generate 0-10 observations across different categories (e.g., both a friction point and a success pattern in the same code review). The schema must support arrays with multiple observations, and each observation must be independently valid.

3. **Observations without file references:** Some observations relate to workflow or process issues rather than specific files (e.g., "TDD iteration count higher than expected"). The `files` array must be optional within each observation, defaulting to empty `[]` when not applicable.

4. **Legacy invocations without observations:** Existing automation, scripts, or workflows that parse subagent output must not break when the new observations field is absent. The field is purely additive.

5. **Category boundary cases:** An observation may arguably fit multiple categories (e.g., a bug that also represents a gap). The schema allows only one category per observation; the subagent should choose the most specific/actionable category.

---

## Data Validation Rules

1. **Category field:** Must be exactly one of 7 valid enum values: `friction`, `success`, `pattern`, `gap`, `idea`, `bug`, `warning`. Case-sensitive, lowercase only.

2. **Severity field:** Must be exactly one of 3 valid enum values: `low`, `medium`, `high`. Case-sensitive, lowercase only.

3. **Note field:** Human-readable string, minimum 10 characters, maximum 500 characters. Must be a complete sentence or phrase describing the observation.

4. **Files field:** Array of 0-10 relative file paths (no absolute paths). Each path must use forward slashes. Empty array `[]` is valid.

5. **Observations array:** Array of 0-10 observation objects per subagent invocation. Empty array or field omission both valid.

6. **YAML format:** Observations schema must be valid YAML that can be parsed by standard YAML parsers.

---

## Non-Functional Requirements

### Performance
- Observation schema documentation adds 0 runtime overhead (documentation only, no code execution)
- Schema parsing by consumers: < 10ms per observation object
- No impact on subagent execution time (observations are output, not computed separately)

### Security
- No sensitive data in observations: Observations must not contain API keys, passwords, connection strings, or PII
- File paths in `files[]` array: Relative paths only (no absolute paths that leak system structure)
- Note content: No executable code, SQL, or injection vectors in observation text

### Reliability
- Backward compatible: 100% of existing subagent invocations continue working unchanged
- Graceful degradation: If observation parsing fails in a consumer, it must not block the workflow
- Schema validation: Invalid observations (wrong category, missing note) are logged as warnings, not errors

### Maintainability
- Schema consistency: All 4 subagents use identical observation schema (copy-paste consistency)
- Documentation co-location: Schema documented within same file as subagent specification
- Single source of truth: Category definitions identical across all 4 files (no drift)

---

## Dependencies

### Prerequisite Stories
None - This is a foundational story for EPIC-051.

### External Dependencies
None - Framework-internal changes only.

### Technology Dependencies
None - Documentation-only changes to Markdown specification files.

---

## Test Strategy

### Unit Tests

**Coverage Target:** N/A (documentation-only story)

**Test Scenarios (Structural Validation):**
1. **Schema presence:** Verify each of 4 files contains `observations:` keyword
2. **Category completeness:** Verify all 7 categories documented in each file
3. **Severity completeness:** Verify all 3 severity levels documented in each file
4. **Schema consistency:** Verify schema text is identical across all 4 files

### Integration Tests

**Coverage Target:** N/A (documentation-only story)

**Test Scenarios:**
1. **Backward compatibility:** Invoke each subagent without observations, verify success
2. **Parser validation:** Parse observation schema as YAML, verify structure valid

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation. Check off items as each sub-task completes.

**Usage:** The devforgeai-development skill updates this checklist at the end of each TDD phase (Phases 1-5), providing granular visibility into AC completion progress.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: test-automator Observations Schema

- [ ] `observations:` keyword present in file - **Phase:** 2 - **Evidence:** grep .claude/agents/test-automator.md
- [ ] All 7 category types documented - **Phase:** 2 - **Evidence:** grep for friction, success, pattern, gap, idea, bug, warning
- [ ] Severity levels documented (low, medium, high) - **Phase:** 2 - **Evidence:** grep for severity enum
- [ ] Files array documented as optional - **Phase:** 2 - **Evidence:** grep for files[]

### AC#2: code-reviewer Observations Schema

- [ ] `observations:` keyword present in file - **Phase:** 2 - **Evidence:** grep .claude/agents/code-reviewer.md
- [ ] All 7 category types documented - **Phase:** 2 - **Evidence:** grep for category definitions
- [ ] Severity levels documented - **Phase:** 2 - **Evidence:** grep for severity enum

### AC#3: backend-architect Observations Schema

- [ ] `observations:` keyword present in file - **Phase:** 2 - **Evidence:** grep .claude/agents/backend-architect.md
- [ ] All 7 category types documented - **Phase:** 2 - **Evidence:** grep for category definitions
- [ ] Severity levels documented - **Phase:** 2 - **Evidence:** grep for severity enum

### AC#4: ac-compliance-verifier Observations Schema

- [ ] `observations:` keyword present in file - **Phase:** 2 - **Evidence:** grep .claude/agents/ac-compliance-verifier.md
- [ ] All 7 category types documented - **Phase:** 2 - **Evidence:** grep for category definitions
- [ ] Severity levels documented - **Phase:** 2 - **Evidence:** grep for severity enum

### AC#5: Backward Compatibility

- [ ] Schema marked as optional in documentation - **Phase:** 2 - **Evidence:** "OPTIONAL" keyword in schema
- [ ] No required fields added that would break existing invocations - **Phase:** 2 - **Evidence:** schema review

### AC#6: Category Documentation Completeness

- [ ] friction category defined - **Phase:** 2 - **Evidence:** grep for "friction"
- [ ] success category defined - **Phase:** 2 - **Evidence:** grep for "success"
- [ ] pattern category defined - **Phase:** 2 - **Evidence:** grep for "pattern"
- [ ] gap category defined - **Phase:** 2 - **Evidence:** grep for "gap"
- [ ] idea category defined - **Phase:** 2 - **Evidence:** grep for "idea"
- [ ] bug category defined - **Phase:** 2 - **Evidence:** grep for "bug"
- [ ] warning category defined - **Phase:** 2 - **Evidence:** grep for "warning"

---

**Checklist Progress:** 0/22 items complete (0%)

---

## Definition of Done

### Implementation
- [x] test-automator.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 1663
- [x] code-reviewer.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 727
- [x] backend-architect.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 759
- [x] ac-compliance-verifier.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 1067
- [x] All 7 categories documented with clear definitions in each file - Completed: friction, success, pattern, gap, idea, bug, warning documented in all 4 files
- [x] All 3 severity levels documented in each file - Completed: low, medium, high documented in all 4 files
- [x] Schema marked as optional (backward compatible) - Completed: "OPTIONAL - subagents work normally without it" in all files

### Code Quality
- [x] Schema text is identical across all 4 files - Completed: Verified identical schema structure across all 4 files
- [x] YAML schema is syntactically valid - Completed: Valid YAML structure verified
- [x] Category definitions are clear and unambiguous - Completed: Each category has definition explaining purpose
- [x] No anti-patterns introduced - Completed: Verified by code-reviewer subagent

### Testing
- [x] Structural tests verify schema presence in all 4 files - Completed: 6 tests in devforgeai/tests/STORY-318/
- [x] Structural tests verify all 7 categories documented - Completed: test_ac6_category_completeness.sh verifies all categories
- [x] Structural tests verify schema consistency across files - Completed: Tests check all 4 files for consistency
- [x] All tests passing - Completed: 6/6 tests passing

### Documentation
- [x] Category definitions explain each category's purpose - Completed: Each category has description in schema
- [x] Severity levels explain when to use each - Completed: low/medium/high explained
- [x] Example observation provided in schema - Completed: Example YAML with sample observation in each file
- [x] Schema notes explain optional nature - Completed: "OPTIONAL" marker and explanation in all files

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-01-26
**Branch:** main

- [x] test-automator.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 1663
- [x] code-reviewer.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 727
- [x] backend-architect.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 759
- [x] ac-compliance-verifier.md contains observations schema in Output section - Completed: Added observations schema with all 7 categories at line 1067
- [x] All 7 categories documented with clear definitions in each file - Completed: friction, success, pattern, gap, idea, bug, warning documented in all 4 files
- [x] All 3 severity levels documented in each file - Completed: low, medium, high documented in all 4 files
- [x] Schema marked as optional (backward compatible) - Completed: "OPTIONAL - subagents work normally without it" in all files
- [x] Schema text is identical across all 4 files - Completed: Verified identical schema structure across all 4 files
- [x] YAML schema is syntactically valid - Completed: Valid YAML structure verified
- [x] Category definitions are clear and unambiguous - Completed: Each category has definition explaining purpose
- [x] No anti-patterns introduced - Completed: Verified by code-reviewer subagent
- [x] Structural tests verify schema presence in all 4 files - Completed: 6 tests in devforgeai/tests/STORY-318/
- [x] Structural tests verify all 7 categories documented - Completed: test_ac6_category_completeness.sh verifies all categories
- [x] Structural tests verify schema consistency across files - Completed: Tests check all 4 files for consistency
- [x] All tests passing - Completed: 6/6 tests passing
- [x] Category definitions explain each category's purpose - Completed: Each category has description in schema
- [x] Severity levels explain when to use each - Completed: low/medium/high explained
- [x] Example observation provided in schema - Completed: Example YAML with sample observation in each file
- [x] Schema notes explain optional nature - Completed: "OPTIONAL" marker and explanation in all files

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 6 structural tests covering all 6 acceptance criteria
- Tests placed in devforgeai/tests/STORY-318/
- Test frameworks: Bash/grep structural validation

**Phase 03 (Green): Implementation**
- Added observations schema to all 4 target subagent files
- Schema includes 7 categories, 3 severity levels, optional files array
- All 6 tests passing (100% pass rate)

**Phase 04 (Refactor): Code Quality**
- Code reviewed by refactoring-specialist and code-reviewer subagents
- Schema is consistent across all 4 files
- Light QA validation passed

**Phase 05 (Integration): Full Validation**
- Integration testing verified cross-file consistency
- YAML syntax validated
- No regressions introduced

**Phase 06 (Deferral Challenge): DoD Validation**
- All Definition of Done items completed
- 0 deferrals
- No blockers detected

### Files Modified

**Modified:**
- .claude/agents/test-automator.md (added observations schema)
- .claude/agents/code-reviewer.md (added observations schema)
- .claude/agents/backend-architect.md (added observations schema)
- .claude/agents/ac-compliance-verifier.md (added observations schema)

**Created:**
- devforgeai/tests/STORY-318/test_ac1_test_automator_schema.sh
- devforgeai/tests/STORY-318/test_ac2_code_reviewer_schema.sh
- devforgeai/tests/STORY-318/test_ac3_backend_architect_schema.sh
- devforgeai/tests/STORY-318/test_ac4_ac_compliance_verifier_schema.sh
- devforgeai/tests/STORY-318/test_ac5_backward_compatibility.sh
- devforgeai/tests/STORY-318/test_ac6_category_completeness.sh

### Test Results

- **Total tests:** 6
- **Pass rate:** 100%
- **Execution time:** <1 second

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-26 | claude/story-requirements-analyst | Created | Story created from EPIC-051 Feature 1 | STORY-318-subagent-observation-schema.story.md |
| 2026-01-26 | claude/opus | DoD Update (Phase 07) | Development complete, all 18 DoD items verified | 4 agent files, 6 test files |
| 2026-01-26 | claude/qa-result-interpreter | QA Deep | PASSED: 6/6 tests, 0 violations, 1/1 validators | - |

---

## Notes

**Design Decisions:**
- Schema is identical across all 4 subagents to ensure consistency and easy maintenance
- 7 categories chosen to cover the full spectrum of observation types from EPIC-051 requirements
- Files array is optional to support both file-specific and process-level observations

**Open Questions:**
None - Requirements are fully specified in EPIC-051.

**Related ADRs:**
None - No architectural decisions required.

**References:**
- EPIC-051: Framework Feedback Capture System
- BRAINSTORM-007: Feedback System Visibility

---

Story Template Version: 2.7
Last Updated: 2026-01-26
