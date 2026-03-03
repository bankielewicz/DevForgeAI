---
id: STORY-434
title: Unify Complexity Scoring Systems
type: refactor
epic: EPIC-068
sprint: Sprint-1
status: QA Approved
points: 3
depends_on: ["STORY-432", "STORY-433"]
priority: High
advisory: false
assigned_to: Unassigned
created: 2026-02-17
format_version: "2.9"
---

# Story: Unify Complexity Scoring Systems

## Description

**As a** DevForgeAI framework maintainer,
**I want** to merge the two incompatible complexity scoring scales (ideation's 0-60 scale and orchestration's 0-10 scale) into a single unified scoring system owned by the architecture skill,
**so that** there is one authoritative complexity assessment used across all workflow stages — eliminating conflicting scores for the same epic.

**Business Context:**
After STORY-432 (F1) and STORY-433 (F2) migrate all epic-related files into architecture, the architecture skill will own three files with conflicting scoring systems: `technical-assessment-guide.md` (0-10 scale from orchestration), `complexity-assessment-workflow.md` (0-60 scale from ideation), and `complexity-assessment-matrix.md` (0-60 scale from ideation). This story resolves the conflict by designing and implementing a single unified scale. Additionally, overlapping feature decomposition content between `epic-decomposition-workflow.md` (from ideation) and `feature-decomposition-patterns.md` (from orchestration) must be merged into one authoritative file.

## Provenance

```xml
<provenance>
  <origin document="EPIC-068" section="Feature 3">
    <quote>"Resolve incompatible scoring scales — ideation uses 0-60 (4 dimensions: Functional 0-20, Technical 0-20, Team/Org 0-10, NFR 0-10) while orchestration uses 0-10 (5 bands: Trivial/Low/Moderate/High/Critical). Merge into single unified scoring system owned by architecture."</quote>
    <line_reference>lines 92-97</line_reference>
    <quantified_impact>3 conflicting reference files unified; 2 overlapping decomposition files merged into 1</quantified_impact>
  </origin>

  <decision rationale="eliminate-conflicting-assessments">
    <selected>Merge into single unified scoring system under architecture skill</selected>
    <rejected alternative="keep-both-scales">
      Dual scoring creates conflicting complexity assessments for the same epic; downstream tools cannot reconcile 0-60 vs 0-10
    </rejected>
    <trade_off>Unified scale may lose granularity from one system; compensated by preserving dimensionality from 0-60 while mapping to clear tier bands</trade_off>
  </decision>

  <stakeholder role="Framework Maintainer" goal="single-source-of-truth">
    <quote>"One authoritative complexity score per epic, no conflicting assessments"</quote>
    <source>EPIC-068, Feature 3 User Value</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Unified Scoring Scale Defined

```xml
<acceptance_criteria id="AC1" implements="UNIFY-001">
  <given>The architecture skill contains two incompatible scoring systems after F1/F2 migrations (0-10 from orchestration, 0-60 from ideation)</given>
  <when>The unified scoring system is designed</when>
  <then>A single scoring system is defined that: (a) preserves the 4-dimension structure from ideation (Functional, Technical, Team/Org, NFR), (b) maps to clear tier labels from orchestration (Trivial, Low, Moderate, High, Critical), and (c) has a single numeric range with unambiguous tier boundaries</then>
  <verification>
    <source_files>
      <file hint="Ideation complexity workflow">src/claude/skills/designing-systems/references/complexity-assessment-workflow.md</file>
      <file hint="Ideation complexity matrix">src/claude/skills/designing-systems/references/complexity-assessment-matrix.md</file>
      <file hint="Orchestration technical assessment">src/claude/skills/designing-systems/references/technical-assessment-guide.md</file>
    </source_files>
    <test_file>tests/STORY-434/test_ac1_unified_scale.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Complexity Assessment Files Consolidated

```xml
<acceptance_criteria id="AC2" implements="UNIFY-002">
  <given>Three files contain overlapping complexity scoring content</given>
  <when>The consolidation is complete</when>
  <then>Complexity scoring is consolidated into exactly 2 files: (a) a unified complexity-assessment-workflow.md (scoring procedure) and (b) a unified complexity-assessment-matrix.md (detailed rubric with examples). The technical-assessment-guide.md scoring section is replaced with a reference pointer to the unified files.</then>
  <verification>
    <source_files>
      <file hint="Unified workflow">src/claude/skills/designing-systems/references/complexity-assessment-workflow.md</file>
      <file hint="Unified matrix">src/claude/skills/designing-systems/references/complexity-assessment-matrix.md</file>
      <file hint="Updated assessment guide">src/claude/skills/designing-systems/references/technical-assessment-guide.md</file>
    </source_files>
    <test_file>tests/STORY-434/test_ac2_file_consolidation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Feature Decomposition Content Merged

```xml
<acceptance_criteria id="AC3" implements="MERGE-001">
  <given>Two files contain overlapping feature decomposition content: epic-decomposition-workflow.md (from ideation) and feature-decomposition-patterns.md (from orchestration)</given>
  <when>The merge is complete</when>
  <then>A single authoritative feature-decomposition.md exists in architecture references that combines: (a) the decomposition process from epic-decomposition-workflow.md, (b) the domain patterns from feature-decomposition-patterns.md, and (c) no duplicate content remains</then>
  <verification>
    <source_files>
      <file hint="Ideation decomposition">src/claude/skills/designing-systems/references/epic-decomposition-workflow.md</file>
      <file hint="Orchestration decomposition">src/claude/skills/designing-systems/references/feature-decomposition-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-434/test_ac3_decomposition_merge.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Tier Mapping Backward Compatible

```xml
<acceptance_criteria id="AC4" implements="COMPAT-001">
  <given>Existing references in the codebase use the old scoring labels (0-10 bands OR 0-60 tiers)</given>
  <when>The unified scoring system is implemented</when>
  <then>A mapping table is documented in the unified files that maps both legacy scales to the new unified scale, enabling existing references to be interpreted correctly during the transition period</then>
  <verification>
    <source_files>
      <file hint="Unified matrix with mapping">src/claude/skills/designing-systems/references/complexity-assessment-matrix.md</file>
    </source_files>
    <test_file>tests/STORY-434/test_ac4_backward_compatibility.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: No Duplicate Scoring or Decomposition Files Remain

```xml
<acceptance_criteria id="AC5" implements="CLEANUP-001">
  <given>The unification and merge are complete</given>
  <when>The architecture references directory is inspected</when>
  <then>No redundant files exist: (a) no separate epic-decomposition-workflow.md AND feature-decomposition-patterns.md (merged into one), (b) technical-assessment-guide.md no longer contains a full scoring rubric (references the unified files instead), (c) zero content duplication across complexity files</then>
  <verification>
    <source_files>
      <file hint="Architecture references">src/claude/skills/designing-systems/references/</file>
    </source_files>
    <test_file>tests/STORY-434/test_ac5_no_duplicates.py</test_file>
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
      name: "Scoring Scale Unification"
      file_path: "N/A - documentation refactor"
      purpose: "Define the unified complexity scoring system"
      required_keys:
        - key: "current_scales"
          type: "object"
          example: |
            orchestration_scale:
              range: 0-10
              bands: [Trivial(0-2), Low(3-4), Moderate(5-6), High(7-8), Critical(9-10)]
              dimensions: 1 (overall)
              source: technical-assessment-guide.md
            ideation_scale:
              range: 0-60
              tiers: [Simple(0-15), Moderate(16-30), Complex(31-45), Enterprise(46-60)]
              dimensions: 4 (Functional 0-20, Technical 0-20, Team/Org 0-10, NFR 0-10)
              source: complexity-assessment-matrix.md
          required: true
          test_requirement: "Test: Verify both scales are documented before unification"
        - key: "unified_scale"
          type: "object"
          example: |
            range: 0-60
            dimensions: 4 (preserved from ideation)
            tier_labels: 5 (preserved from orchestration)
            tiers:
              - Trivial: 0-10
              - Low: 11-20
              - Moderate: 21-35
              - High: 36-50
              - Critical: 51-60
          required: true
          test_requirement: "Test: Verify unified scale covers full range with no gaps or overlaps"

    - type: "Configuration"
      name: "Feature Decomposition Merge"
      file_path: "N/A - documentation refactor"
      purpose: "Merge overlapping decomposition content"
      required_keys:
        - key: "source_files"
          type: "array"
          example: |
            - epic-decomposition-workflow.md (309 lines) — process steps
            - feature-decomposition-patterns.md (903 lines) — domain patterns
          required: true
          test_requirement: "Test: Both source files exist and contain decomposition content"
        - key: "target_file"
          type: "string"
          example: "feature-decomposition.md"
          required: true
          test_requirement: "Test: Merged file contains content from both sources"

  business_rules:
    - id: "BR-001"
      rule: "Unified scale must preserve 4-dimension scoring from ideation (most granular)"
      trigger: "When designing unified scale"
      validation: "Unified scale has Functional, Technical, Team/Org, and NFR dimensions"
      error_handling: "HALT if any dimension dropped without user approval"
      test_requirement: "Test: Verify all 4 dimensions present in unified workflow"
      priority: "Critical"

    - id: "BR-002"
      rule: "Unified scale must map to labeled tiers (human-readable bands)"
      trigger: "When defining tier boundaries"
      validation: "Each tier has a name, numeric range, and description"
      error_handling: "HALT if tier boundaries have gaps or overlaps"
      test_requirement: "Test: Verify tier ranges cover 0-60 with no gaps or overlaps"
      priority: "Critical"

    - id: "BR-003"
      rule: "Legacy scale mapping must be provided for backward compatibility"
      trigger: "When unified scale is finalized"
      validation: "Mapping table converts both 0-10 and 0-60 to unified scale"
      error_handling: "Log warning if any legacy value has ambiguous mapping"
      test_requirement: "Test: Map all legacy values, verify each maps to exactly one tier"
      priority: "High"

    - id: "BR-004"
      rule: "Feature decomposition merge must preserve all domain patterns"
      trigger: "When merging decomposition files"
      validation: "All domain patterns from feature-decomposition-patterns.md present in merged file"
      error_handling: "HALT if any domain pattern is lost"
      test_requirement: "Test: List domain patterns before/after, verify count matches"
      priority: "High"

    - id: "BR-005"
      rule: "Merged files must be under 1,000 lines each (progressive disclosure target)"
      trigger: "After merge completion"
      validation: "Line count for each output file < 1,000"
      error_handling: "If over limit, split into workflow file + detailed appendix"
      test_requirement: "Test: Count lines in output files, verify < 1,000"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "All content from both scoring systems must be preserved or explicitly documented as removed"
      metric: "100% content traceability (every section in source files maps to unified output or documented removal reason)"
      test_requirement: "Test: Section-by-section comparison of inputs vs outputs"
      priority: "Critical"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Unified scoring procedure must complete in reasonable time"
      metric: "Scoring workflow ≤ 5 minutes per epic (same as current ideation timing)"
      test_requirement: "Test: Review unified workflow step count, estimate time"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Scoring Scale Unification"
    limitation: "The two scales measure different things at different granularity levels — a true mathematical mapping between 0-10 and 0-60 is impossible because they evaluate different dimensions"
    decision: "workaround:Preserve 0-60 range with 4 dimensions from ideation (most granular) and apply 5-tier naming from orchestration (most human-readable)"
    discovered_phase: "Architecture"
    impact: "Some legacy 0-10 scores will need manual re-assessment against the new 4-dimension rubric; cannot be auto-converted"

  - id: TL-002
    component: "Feature Decomposition Merge"
    limitation: "epic-decomposition-workflow.md focuses on process (step-by-step workflow) while feature-decomposition-patterns.md focuses on domain patterns (e-commerce, SaaS, etc.) — they are complementary, not duplicative"
    decision: "workaround:Create single file with two major sections: Process (from epic-decomposition-workflow) and Domain Patterns (from feature-decomposition-patterns)"
    discovered_phase: "Architecture"
    impact: "Merged file may exceed 1,000 lines (309 + 903 = ~1,212) requiring careful trimming or appendix split"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Not applicable** - This is a one-time content unification, not a runtime feature.

---

### Security

**No security impact** - Skill reference documentation only.

---

### Scalability

**Not applicable** - Content change, no runtime scaling concerns.

---

### Reliability

**Content Traceability:**
- Every section in source files must map to the unified output or have a documented removal reason
- Legacy scale mapping table provides conversion path for existing references

**Error Handling:**
- HALT if any scoring dimension is dropped without explicit user approval
- HALT if tier boundaries have gaps or overlaps
- HALT if merged decomposition file loses domain patterns

---

### Observability

**Logging:**
- Document which sections from each source file went where in the unified output
- Log any content removed with justification

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-432:** Move Epic Creation References from Orchestration → Architecture
  - **Why:** `technical-assessment-guide.md` and `feature-decomposition-patterns.md` must be in architecture before unification
  - **Status:** Backlog

- [ ] **STORY-433:** Move Epic Analysis References from Ideation → Architecture
  - **Why:** `complexity-assessment-workflow.md`, `complexity-assessment-matrix.md`, and `epic-decomposition-workflow.md` must be in architecture before unification
  - **Status:** Backlog

### External Dependencies

None.

### Technology Dependencies

None — uses only native Claude Code tools (Read, Write, Edit).

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for scoring unification logic

**Test Scenarios:**
1. **Happy Path:** Unified scale has 4 dimensions, 5 tiers, no gaps, no overlaps
2. **Edge Cases:**
   - Boundary values between tiers (e.g., score of exactly 10 — which tier?)
   - Legacy 0-10 values that fall between unified tiers
   - Feature decomposition merged file approaches 1,000-line limit
3. **Error Cases:**
   - Tier range gap (e.g., 0-15, 20-35 — gap at 16-19)
   - Missing dimension in unified workflow
   - Domain pattern lost during merge

---

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**
1. **End-to-End:** Unified scoring files work with architecture skill workflow
2. **Legacy Mapping:** Both 0-10 and 0-60 scores convert correctly to unified tiers
3. **Decomposition Merge:** Merged file contains all domain patterns from both sources

---

## Acceptance Criteria Verification Checklist

### AC#1: Unified Scoring Scale Defined

- [x] 4 dimensions defined (Functional, Technical, Team/Org, NFR) - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac1_unified_scale.py
- [x] 5 tiers defined with labels - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac1_unified_scale.py
- [x] Tier boundaries cover full range with no gaps or overlaps - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac1_unified_scale.py
- [x] Single numeric range documented - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac1_unified_scale.py

### AC#2: Complexity Assessment Files Consolidated

- [x] complexity-assessment-workflow.md updated with unified procedure - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac2_file_consolidation.py
- [x] complexity-assessment-matrix.md updated with unified rubric - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac2_file_consolidation.py
- [x] technical-assessment-guide.md scoring section replaced with pointer - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac2_file_consolidation.py

### AC#3: Feature Decomposition Content Merged

- [x] Process sections merged from epic-decomposition-workflow.md - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac3_decomposition_merge.py
- [x] Domain patterns preserved from feature-decomposition-patterns.md - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac3_decomposition_merge.py
- [x] Single authoritative file created - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac3_decomposition_merge.py
- [x] Redundant source files removed - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac3_decomposition_merge.py

### AC#4: Tier Mapping Backward Compatible

- [x] 0-10 → unified mapping table documented - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac4_backward_compatibility.py
- [x] 0-60 → unified mapping table documented - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac4_backward_compatibility.py
- [x] Each legacy value maps to exactly one unified tier - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac4_backward_compatibility.py

### AC#5: No Duplicate Scoring or Decomposition Files Remain

- [x] No separate overlapping decomposition files - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac5_no_duplicates.py
- [x] No duplicate scoring rubrics - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac5_no_duplicates.py
- [x] Zero content duplication across complexity files - **Phase:** 3 - **Evidence:** tests/STORY-434/test_ac5_no_duplicates.py

---

**Checklist Progress:** 19/19 items complete (100%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: src/claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-17

- [x] Unified scoring scale designed with 4 dimensions and 5 tiers - Completed: Defined Trivial (0-10), Low (11-20), Moderate (21-35), High (36-50), Critical (51-60) with 4 dimensions (Functional 0-20, Technical 0-20, Team/Org 0-10, NFR 0-10)
- [x] complexity-assessment-workflow.md rewritten with unified procedure - Completed: Added Unified Complexity Scoring System section with 5 tiers and scoring procedure
- [x] complexity-assessment-matrix.md rewritten with unified rubric and examples - Completed: Added Unified Tier Definitions table, machine-readable tier ranges, and preserved detailed dimension breakdowns
- [x] technical-assessment-guide.md scoring section replaced with reference pointer - Completed: Removed full 0-10 rubric, added Complexity Scoring Reference section pointing to unified files
- [x] Feature decomposition files merged into single authoritative file - Completed: Created feature-decomposition.md (465 lines) combining process workflow and domain patterns
- [x] Redundant source files removed after merge - Completed: Deleted epic-decomposition-workflow.md and feature-decomposition-patterns.md
- [x] All 5 acceptance criteria have passing tests - Completed: 47 unit tests + 18 integration tests all pass
- [x] Tier boundaries verified: no gaps, no overlaps across full range - Completed: Test suite validates contiguous ranges 0-60
- [x] All 4 dimensions preserved from ideation scale - Completed: Functional, Technical, Team/Org, NFR all present
- [x] All domain patterns preserved from decomposition merge - Completed: 6 patterns (CRUD, Auth, API, Workflow, E-Commerce, SaaS) in merged file
- [x] Legacy mapping table verified: both 0-10 and 0-60 convert unambiguously - Completed: Mapping tables with each legacy value mapping to exactly one unified tier
- [x] Unit test: test_ac1_unified_scale.py passes - Completed: 15 tests pass
- [x] Unit test: test_ac2_file_consolidation.py passes - Completed: 10 tests pass
- [x] Unit test: test_ac3_decomposition_merge.py passes - Completed: 11 tests pass
- [x] Unit test: test_ac4_backward_compatibility.py passes - Completed: 6 tests pass
- [x] Unit test: test_ac5_no_duplicates.py passes - Completed: 5 tests pass
- [x] Story changelog updated - Completed: Change log updated with implementation details
- [x] Unified scale design rationale documented in Notes - Completed: Design decisions in Notes section
- [x] Legacy mapping table documented for transition period - Completed: Legacy Scale Mapping section in complexity-assessment-matrix.md

## Definition of Done

### Implementation
- [x] Unified scoring scale designed with 4 dimensions and 5 tiers
- [x] complexity-assessment-workflow.md rewritten with unified procedure
- [x] complexity-assessment-matrix.md rewritten with unified rubric and examples
- [x] technical-assessment-guide.md scoring section replaced with reference pointer
- [x] Feature decomposition files merged into single authoritative file
- [x] Redundant source files removed after merge

### Quality
- [x] All 5 acceptance criteria have passing tests
- [x] Tier boundaries verified: no gaps, no overlaps across full range
- [x] All 4 dimensions preserved from ideation scale
- [x] All domain patterns preserved from decomposition merge
- [x] Legacy mapping table verified: both 0-10 and 0-60 convert unambiguously

### Testing
- [x] Unit test: test_ac1_unified_scale.py passes
- [x] Unit test: test_ac2_file_consolidation.py passes
- [x] Unit test: test_ac3_decomposition_merge.py passes
- [x] Unit test: test_ac4_backward_compatibility.py passes
- [x] Unit test: test_ac5_no_duplicates.py passes

### Documentation
- [x] Story changelog updated
- [x] Unified scale design rationale documented in Notes
- [x] Legacy mapping table documented for transition period

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech-stack detected |
| 02 Test-First (Red) | ✅ Complete | 47 tests generated, 20 FAILED + 8 ERROR (correct RED state) |
| 03 Implementation (Green) | ✅ Complete | 47/47 tests passing |
| 04 Refactoring | ✅ Complete | Merge lineage comment added, code review completed |
| 04.5 AC Verification | ✅ Complete | All 5 ACs verified HIGH confidence |
| 05 Integration | ✅ Complete | 65/65 tests passing (47 unit + 18 integration) |
| 05.5 AC Verification | ✅ Complete | Post-integration verification passed |
| 06 Deferral | ✅ Complete | No deferrals needed |
| 07 DoD Update | ✅ Complete | All DoD items marked complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/designing-systems/references/complexity-assessment-matrix.md | Modified | ~690 |
| src/claude/skills/designing-systems/references/complexity-assessment-workflow.md | Modified | ~365 |
| src/claude/skills/designing-systems/references/technical-assessment-guide.md | Modified | ~220 |
| src/claude/skills/designing-systems/references/feature-decomposition.md | Created | ~465 |
| src/claude/skills/designing-systems/references/epic-decomposition-workflow.md | Deleted | 0 |
| src/claude/skills/designing-systems/references/feature-decomposition-patterns.md | Deleted | 0 |
| tests/STORY-434/test_ac1_unified_scale.py | Created | ~168 |
| tests/STORY-434/test_ac2_file_consolidation.py | Created | ~134 |
| tests/STORY-434/test_ac3_decomposition_merge.py | Created | ~147 |
| tests/STORY-434/test_ac4_backward_compatibility.py | Created | ~118 |
| tests/STORY-434/test_ac5_no_duplicates.py | Created | ~108 |
| tests/STORY-434/test_integration_cross_file_consistency.py | Created | ~237 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-17 12:00 | devforgeai-story-creation | Created | Story created from EPIC-068 Feature 3 | STORY-434-unify-complexity-scoring-systems.story.md |
| 2026-02-18 01:00 | DevForgeAI AI Agent | Dev Complete | Unified scoring system implemented, decomposition files merged, all 47 tests passing | 6 source files + 6 test files |
| 2026-02-18 03:15 | .claude/qa-result-interpreter | QA Deep | PASSED: 65/65 tests, 2/2 validators, 0 violations | devforgeai/qa/reports/STORY-434-qa-report.md |

## Notes

**Design Decisions:**
- Preserve 0-60 range (ideation) as the unified range — it has higher granularity
- Apply 5-tier naming (orchestration) — Trivial, Low, Moderate, High, Critical are more descriptive than Simple/Moderate/Complex/Enterprise
- Keep 4-dimension scoring (ideation) — provides structured evaluation rather than subjective overall score
- Proposed unified tier boundaries:
  - **Trivial:** 0-10 (maps to old 0-2 on orchestration scale, or Tier 1 on ideation scale)
  - **Low:** 11-20 (maps to old 3-4, partial Tier 1-2)
  - **Moderate:** 21-35 (maps to old 5-6, Tier 2-3)
  - **High:** 36-50 (maps to old 7-8, Tier 3-4)
  - **Critical:** 51-60 (maps to old 9-10, Tier 4)

**Scoring Comparison (Current State):**

| Aspect | Orchestration (0-10) | Ideation (0-60) |
|--------|---------------------|-----------------|
| Range | 0-10 | 0-60 |
| Dimensions | 1 (overall) | 4 (Functional, Technical, Team/Org, NFR) |
| Tiers | 5 bands | 4 tiers |
| Labels | Trivial/Low/Moderate/High/Critical | Simple/Moderate/Complex/Enterprise |
| Source File | technical-assessment-guide.md | complexity-assessment-matrix.md |

**Feature Decomposition Overlap:**
- `epic-decomposition-workflow.md` (309 lines): Step-by-step process, epic identification, feature grouping
- `feature-decomposition-patterns.md` (903 lines): Domain patterns (e-commerce, SaaS, etc.), decomposition principles, sizing
- These are **complementary** (process vs patterns), not truly duplicative — merge into sections of single file

**Scope Boundaries:**
- This story unifies scoring content — it does NOT update SKILL.md phase references
- Architecture SKILL.md Phase 6 addition is Feature 5 (separate story)
- Ideation SKILL.md slimming is Feature 7 (separate story)

**Related ADRs:**
- [ADR-019: Skill Responsibility Restructure](../adrs/ADR-019-skill-responsibility-restructure.md)

**References:**
- EPIC-068: Skill Responsibility Restructure & ADR-017 Rename Migration
- EPIC-068 Feature 3: Lines 92-97

---

Story Template Version: 2.9
Last Updated: 2026-02-17
