---
id: STORY-407
title: Document Code Smell Detection Catalog in Anti-Pattern-Scanner Reference
type: documentation
epic: EPIC-064
sprint: SPRINT-13
status: QA Approved
points: 3
depends_on: ["STORY-399", "STORY-400", "STORY-401", "STORY-402", "STORY-403", "STORY-404", "STORY-405", "STORY-406"]
priority: High
advisory: false
assigned_to: TBD
created: 2026-02-13
format_version: "2.9"
---

# Story: Document Code Smell Detection Catalog in Anti-Pattern-Scanner Reference

## Description

**As a** framework maintainer,
**I want** a comprehensive code smell catalog documenting all 11 detection types with thresholds, methods, and remediation guidance,
**so that** detection rules are documented and maintainable across the anti-pattern-scanner Phase 5.

## Provenance

```xml
<provenance>
  <origin document="EPIC-064" section="Feature 5: Documentation and ADR">
    <quote>"Create a comprehensive reference document cataloging all 11 automated code smell types, their thresholds, detection methods, severity levels, and remediation guidance. This serves as the canonical reference for anti-pattern-scanner Phase 5."</quote>
    <line_reference>lines 642-678</line_reference>
    <quantified_impact>Documents complete detection catalog for 11 smell types (+267% from baseline 3)</quantified_impact>
  </origin>

  <decision rationale="reference-file-not-constitutional">
    <selected>Code smell detection rules live in anti-pattern-scanner reference files</selected>
    <rejected alternative="constitutional-anti-patterns-md">anti-patterns.md governs framework behavior, not project code quality</rejected>
    <trade_off>Separation maintains constitutional file stability while enabling smell detection evolution</trade_off>
  </decision>

  <hypothesis id="H1" validation="documentation-completeness" success_criteria="all 11 smell types documented with thresholds and test scenarios">
    Comprehensive catalog will reduce onboarding time for contributors and enable consistent detection behavior
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Code Smell Catalog Reference File Created

```xml
<acceptance_criteria id="AC1" implements="CATALOG-FILE">
  <given>The anti-pattern-scanner Phase 5 detects 11 code smell types</given>
  <when>The code smell catalog reference file is created</when>
  <then>File .claude/agents/anti-pattern-scanner/references/code-smell-catalog.md contains: table of all 11 smell types with name, threshold, severity, detection method (Treelint/Grep), two-stage required flag; detailed sections for each smell with definition, threshold, JSON schema, test scenarios, false positive patterns; cross-references to Fowler's refactoring catalog</then>
  <verification>
    <source_files>
      <file hint="Catalog file">.claude/agents/anti-pattern-scanner/references/code-smell-catalog.md</file>
    </source_files>
    <test_file>tests/STORY-407/test_ac1_catalog_file.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: ADR-018 Created for Catalog Location Decision

```xml
<acceptance_criteria id="AC2" implements="ADR-018">
  <given>Code smell detection rules need a canonical location</given>
  <when>ADR-018 is created</when>
  <then>File devforgeai/specs/adrs/ADR-018-code-smell-catalog-location.md documents: Decision that code smell detection rules live in anti-pattern-scanner reference files (NOT constitutional anti-patterns.md); Rationale citing anti-patterns.md v1.1 line 285 distinction between framework vs project patterns; Impact assessment (no constitutional file modification, no LOCKED status change)</then>
  <verification>
    <source_files>
      <file hint="ADR document">devforgeai/specs/adrs/ADR-018-code-smell-catalog-location.md</file>
    </source_files>
    <test_file>tests/STORY-407/test_ac2_adr_018.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Source-Tree.md Updated to v3.9

```xml
<acceptance_criteria id="AC3" implements="SOURCE-TREE">
  <given>New files have been created (dead-code-detector, code-smell-catalog, ADR-018)</given>
  <when>source-tree.md is updated</when>
  <then>devforgeai/specs/context/source-tree.md version incremented from v3.8 to v3.9 with paths added for: .claude/agents/dead-code-detector.md, .claude/agents/dead-code-detector/references/entry-point-patterns.md, .claude/agents/anti-pattern-scanner/references/code-smell-catalog.md, .claude/agents/anti-pattern-scanner/references/two-stage-filter-patterns.md</then>
  <verification>
    <source_files>
      <file hint="Source tree context">devforgeai/specs/context/source-tree.md</file>
    </source_files>
    <test_file>tests/STORY-407/test_ac3_source_tree.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Anti-Pattern-Scanner Phase 5 Updated with Progressive Disclosure

```xml
<acceptance_criteria id="AC4" implements="PHASE5-UPDATE">
  <given>The code smell catalog reference file exists</given>
  <when>anti-pattern-scanner.md Phase 5 is updated</when>
  <then>.claude/agents/anti-pattern-scanner.md Phase 5 (Code Smells) section includes: Progressive disclosure reference "Load code-smell-catalog.md for full detection procedures"; Updated header listing all 11 smell types (god objects, long methods, magic numbers, data class, long parameter list, commented-out code, orphaned imports, dead code, placeholder code, middle man, message chains)</then>
  <verification>
    <source_files>
      <file hint="Agent definition">.claude/agents/anti-pattern-scanner.md</file>
    </source_files>
    <test_file>tests/STORY-407/test_ac4_phase5_update.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: CLAUDE.md Registry Updated

```xml
<acceptance_criteria id="AC5" implements="REGISTRY-UPDATE">
  <given>dead-code-detector subagent has been created (STORY-403)</given>
  <when>CLAUDE.md subagent registry is updated</when>
  <then>CLAUDE.md subagent registry table includes dead-code-detector entry with description, tools (Read, Bash(treelint:*), Grep, Glob), and proactive triggers</then>
  <verification>
    <source_files>
      <file hint="Registry">CLAUDE.md</file>
    </source_files>
    <test_file>tests/STORY-407/test_ac5_registry.py</test_file>
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
      name: "CodeSmellCatalog"
      file_path: ".claude/agents/anti-pattern-scanner/references/code-smell-catalog.md"
      required_keys:
        - key: "smell_types"
          type: "array"
          example: ["god_object", "long_method", "magic_number", "data_class", "long_parameter_list", "commented_out_code", "orphaned_import", "dead_code", "placeholder_code", "middle_man", "message_chain"]
          required: true
          test_requirement: "Test: Verify catalog contains exactly 11 smell types"
        - key: "per_smell.definition"
          type: "string"
          required: true
          test_requirement: "Test: Verify each smell has a definition section"
        - key: "per_smell.threshold"
          type: "object"
          required: true
          test_requirement: "Test: Verify each smell has threshold(s) documented"
        - key: "per_smell.severity"
          type: "enum"
          required: true
          test_requirement: "Test: Verify severity is CRITICAL, HIGH, MEDIUM, or LOW"
        - key: "per_smell.detection_method"
          type: "enum"
          required: true
          test_requirement: "Test: Verify detection_method is Treelint, Grep, or Hybrid"
        - key: "per_smell.two_stage"
          type: "boolean"
          required: true
          test_requirement: "Test: Verify two_stage flag documented for each smell"
        - key: "per_smell.json_schema"
          type: "object"
          required: true
          test_requirement: "Test: Verify JSON output schema documented for each smell"
        - key: "per_smell.test_scenarios"
          type: "array"
          required: true
          test_requirement: "Test: Verify at least 3 test scenarios per smell"
        - key: "per_smell.false_positives"
          type: "array"
          required: true
          test_requirement: "Test: Verify false positive patterns documented"

    - type: "Configuration"
      name: "ADR-018"
      file_path: "devforgeai/specs/adrs/ADR-018-code-smell-catalog-location.md"
      required_keys:
        - key: "decision"
          type: "string"
          required: true
          test_requirement: "Test: Verify ADR contains Decision section"
        - key: "context"
          type: "string"
          required: true
          test_requirement: "Test: Verify ADR contains Context section"
        - key: "rationale"
          type: "string"
          required: true
          test_requirement: "Test: Verify ADR contains Rationale with anti-patterns.md v1.1 line 285 citation"
        - key: "consequences"
          type: "string"
          required: true
          test_requirement: "Test: Verify ADR documents consequences (no constitutional modification)"

    - type: "Configuration"
      name: "SourceTreeUpdate"
      file_path: "devforgeai/specs/context/source-tree.md"
      required_keys:
        - key: "version"
          type: "string"
          example: "3.9"
          required: true
          test_requirement: "Test: Verify version is 3.9 (incremented from 3.8)"
        - key: "paths.dead_code_detector"
          type: "array"
          required: true
          test_requirement: "Test: Verify dead-code-detector paths present"
        - key: "paths.code_smell_catalog"
          type: "string"
          required: true
          test_requirement: "Test: Verify code-smell-catalog.md path present"
        - key: "paths.two_stage_filter"
          type: "string"
          required: true
          test_requirement: "Test: Verify two-stage-filter-patterns.md path present"

  business_rules:
    - id: "BR-001"
      rule: "11 smell types must be documented in catalog"
      trigger: "Catalog completeness check"
      validation: "Count smell type sections = 11"
      error_handling: "HALT if any smell type missing"
      test_requirement: "Test: Verify catalog contains exactly 11 smell type sections"
      priority: "Critical"
    - id: "BR-002"
      rule: "ADR-018 must cite anti-patterns.md v1.1 line 285"
      trigger: "ADR rationale validation"
      validation: "Rationale section references specific source"
      error_handling: "Flag if citation missing"
      test_requirement: "Test: Verify ADR rationale cites constitutional file"
      priority: "High"
    - id: "BR-003"
      rule: "Source-tree.md version must increment"
      trigger: "Version update validation"
      validation: "Version 3.9 > 3.8"
      error_handling: "HALT if version not incremented"
      test_requirement: "Test: Verify version incremented correctly"
      priority: "High"
    - id: "BR-004"
      rule: "Progressive disclosure reference required in Phase 5"
      trigger: "Anti-pattern-scanner update validation"
      validation: "Phase 5 contains reference to code-smell-catalog.md"
      error_handling: "Flag if reference missing"
      test_requirement: "Test: Verify Phase 5 references catalog file"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Documentation"
      requirement: "Catalog completeness"
      metric: "11 smell types documented with all required fields"
      test_requirement: "Test: Validate all 11 smell types have all required sections"
      priority: "Critical"
    - id: "NFR-002"
      category: "Documentation"
      requirement: "Test scenario coverage"
      metric: "Minimum 3 test scenarios per smell type (33+ total)"
      test_requirement: "Test: Count test scenarios >= 33"
      priority: "High"
    - id: "NFR-003"
      category: "Documentation"
      requirement: "Fowler cross-references"
      metric: "Cross-references to Fowler's refactoring catalog where applicable"
      test_requirement: "Test: Verify Fowler citations for applicable smells"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
# No known limitations - documentation story
```

---

## Non-Functional Requirements (NFRs)

### Documentation Quality

**Completeness:**
- All 11 smell types documented
- Each smell has: definition, threshold, severity, detection method, two-stage flag, JSON schema, test scenarios, false positives

**Consistency:**
- Consistent structure across all smell type sections
- Consistent terminology and formatting

---

## Dependencies

### Prerequisite Stories

- [x] **STORY-399:** Data Class Detection (provides data_class smell definition)
- [x] **STORY-400:** Long Parameter List Detection (provides long_parameter_list smell definition)
- [x] **STORY-401:** Commented-Out Code Detection (provides commented_out_code smell definition, creates two-stage-filter-patterns.md)
- [x] **STORY-402:** Orphaned Import Detection (provides orphaned_import smell definition)
- [x] **STORY-403:** Dead Code Detector (provides dead_code smell definition, creates dead-code-detector subagent)
- [x] **STORY-404:** Placeholder Detection (provides placeholder_code smell definition)
- [x] **STORY-405:** Middle Man Detection (provides middle_man smell definition)
- [x] **STORY-406:** Message Chain Detection (provides message_chain smell definition)

**All 8 prerequisite stories must be completed before this story can execute.**

### Technology Dependencies

None — documentation story.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for validation scripts

**Test Scenarios:**
1. **Catalog Completeness:** Verify all 11 smell types present
2. **Section Structure:** Verify each smell has all required sections
3. **JSON Schema Validation:** Verify JSON schemas are valid
4. **ADR Format:** Verify ADR-018 follows standard format
5. **Source-tree Version:** Verify version incremented to 3.9
6. **Registry Entry:** Verify dead-code-detector in CLAUDE.md

---

## Acceptance Criteria Verification Checklist

### AC#1: Code Smell Catalog Reference File Created

- [x] Catalog file created at correct path - **Phase:** 3
- [x] Summary table with 11 smell types - **Phase:** 3
- [x] Detailed section for each smell type (11 sections) - **Phase:** 3
- [x] Fowler cross-references where applicable - **Phase:** 3

### AC#2: ADR-018 Created for Catalog Location Decision

- [x] ADR file created at correct path - **Phase:** 3
- [x] Decision section present - **Phase:** 3
- [x] Rationale cites anti-patterns.md v1.1 line 285 - **Phase:** 3
- [x] Impact assessment documented - **Phase:** 3

### AC#3: Source-Tree.md Updated to v3.9

- [x] Version incremented from 3.8 to 3.9 - **Phase:** 3
- [x] dead-code-detector paths added - **Phase:** 3
- [x] code-smell-catalog.md path added - **Phase:** 3
- [x] two-stage-filter-patterns.md path added - **Phase:** 3

### AC#4: Anti-Pattern-Scanner Phase 5 Updated with Progressive Disclosure

- [x] Progressive disclosure reference added - **Phase:** 3
- [x] Phase 5 header lists all 11 smell types - **Phase:** 3

### AC#5: CLAUDE.md Registry Updated

- [x] dead-code-detector entry added - **Phase:** 3
- [x] Description, tools, and proactive triggers documented - **Phase:** 3

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] Code smell catalog reference file created with all 11 smell types
- [x] ADR-018 created with decision, context, rationale, consequences
- [x] source-tree.md updated to v3.9 with new paths
- [x] anti-pattern-scanner.md Phase 5 updated with progressive disclosure
- [x] CLAUDE.md registry updated with dead-code-detector

### Quality
- [x] All 5 acceptance criteria have passing validation
- [x] All 11 smell types documented with complete information
- [x] Consistent structure across all smell type sections
- [x] ADR follows standard format

### Testing
- [x] Validation tests for catalog completeness (test_ac1_catalog_file.py)
- [x] Validation tests for ADR format (test_ac2_adr_018.py)
- [x] Validation tests for source-tree version (test_ac3_source_tree.py)
- [x] Validation tests for Phase 5 update (test_ac4_phase5_update.py)
- [x] Validation tests for registry entry (test_ac5_registry.py)

### Documentation
- [x] Code smell catalog is self-documenting
- [x] ADR-018 is self-documenting
- [x] No additional documentation required

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| Phase 02 (Red) | ✅ Complete | 5 test files created, 138 errors + 9 failures confirm RED state |
| Phase 03 (Green) | ✅ Complete | All 152 tests passing, 5 documentation files created/modified |
| Phase 04 (Refactor) | ✅ Complete | ADR renamed 017→018 (collision fix), test file updated, 152 tests still pass |
| Phase 4.5 (AC Verify) | ✅ Complete | All 5 ACs verified PASS with HIGH confidence |
| Phase 05 (Integration) | ✅ Complete | Cross-reference validation passed, all file paths verified |
| Phase 5.5 (AC Verify) | ✅ Complete | Final AC verification passed |
| Phase 06 (Deferral) | ✅ Complete | No deferrals - all items implemented |
| Phase 07 (DoD) | ✅ Complete | All 18 DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| tests/STORY-407/test_ac1_catalog_file.py | Created | Phase 02 |
| tests/STORY-407/test_ac2_adr_018.py | Created | Phase 02 |
| tests/STORY-407/test_ac3_source_tree.py | Created | Phase 02 |
| tests/STORY-407/test_ac4_phase5_update.py | Created | Phase 02 |
| tests/STORY-407/test_ac5_registry.py | Created | Phase 02 |

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-16

- [x] Code smell catalog reference file created with all 11 smell types - Completed: Created .claude/agents/anti-pattern-scanner/references/code-smell-catalog.md with 503 lines documenting all smell types
- [x] ADR-018 created with decision, context, rationale, consequences - Completed: Created devforgeai/specs/adrs/ADR-018-code-smell-catalog-location.md (renamed from ADR-017 due to numbering collision)
- [x] source-tree.md updated to v3.9 with new paths - Completed: Version incremented and 4 paths added
- [x] anti-pattern-scanner.md Phase 5 updated with progressive disclosure - Completed: Phase 5 header lists all 11 smell types with Read() reference
- [x] CLAUDE.md registry updated with dead-code-detector - Completed: Entry added with description, tools, and proactive triggers
- [x] All 5 acceptance criteria have passing validation - Completed: 152 tests pass, AC verification passed twice (Phase 4.5, 5.5)
- [x] All 11 smell types documented with complete information - Completed: Each smell has definition, threshold, severity, detection method, JSON schema, test scenarios, false positives, Fowler reference
- [x] Consistent structure across all smell type sections - Completed: All 11 sections follow identical format
- [x] ADR follows standard format - Completed: ADR-018 has Status, Context, Decision, Rationale, Consequences sections
- [x] Validation tests for catalog completeness (test_ac1_catalog_file.py) - Completed: Created in Phase 02
- [x] Validation tests for ADR format (test_ac2_adr_018.py) - Completed: Created in Phase 02 (renamed from test_ac2_adr_017.py)
- [x] Validation tests for source-tree version (test_ac3_source_tree.py) - Completed: Created in Phase 02
- [x] Validation tests for Phase 5 update (test_ac4_phase5_update.py) - Completed: Created in Phase 02
- [x] Validation tests for registry entry (test_ac5_registry.py) - Completed: Created in Phase 02
- [x] Code smell catalog is self-documenting - Completed: Catalog contains complete documentation for all smell types
- [x] ADR-018 is self-documenting - Completed: ADR explains decision rationale fully
- [x] No additional documentation required - Completed: All documentation embedded in deliverables

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-13 16:00 | .claude/devforgeai-story-creation | Created | Story created from EPIC-064 Feature 5 | STORY-407-document-code-smell-catalog.story.md |
| 2026-02-16 00:25 | .claude/qa-result-interpreter | QA Deep | PASSED: 152 tests pass, 100% traceability, 1/1 validators | - |

## Notes

**Design Decisions:**
- Catalog location in anti-pattern-scanner references (not constitutional file)
- ADR-018 formalizes this architectural decision
- Source-tree.md version increment (3.8 → 3.9) for new paths
- Progressive disclosure reference in Phase 5 maintains agent size limits

**Smell Types to Document (11 total):**
1. God Object (existing) — CRITICAL
2. Long Method (existing) — MEDIUM
3. Magic Number (existing) — MEDIUM
4. Data Class (STORY-399) — MEDIUM
5. Long Parameter List (STORY-400) — MEDIUM
6. Commented-Out Code (STORY-401) — LOW
7. Orphaned Import (STORY-402) — LOW
8. Dead Code (STORY-403) — LOW
9. Placeholder Code (STORY-404) — HIGH
10. Middle Man (STORY-405) — MEDIUM
11. Message Chain (STORY-406) — LOW

**References:**
- EPIC-064: AI-Generated Code Smell Detection Gap Closure (lines 642-678)
- anti-patterns.md v1.1 line 285: Framework vs project patterns distinction
- Fowler's Refactoring Catalog: https://refactoring.guru/refactoring/smells

---

Story Template Version: 2.9
Last Updated: 2026-02-13
