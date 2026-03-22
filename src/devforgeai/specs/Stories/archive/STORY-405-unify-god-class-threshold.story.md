---
id: STORY-405
title: Unify God Class Threshold to >20 Methods
type: refactor
epic: EPIC-063
sprint: Backlog
status: QA Approved
priority: Medium
points: 1
created: 2026-02-08
updated: 2026-02-10
assignee: claude
tags: [framework, anti-pattern, consistency, threshold, refactor]
source_recommendation: REC-369-001
template_version: "2.8"
---

# STORY-405: Unify God Class Threshold to >20 Methods

## Description

Unify the god class detection threshold to >20 methods across BOTH Treelint and legacy Grep detection modes in anti-pattern-scanner.md, eliminating inconsistent flagging.

<!-- provenance>
  <origin document="EPIC-063" section="Feature 7">
    <quote>This inconsistency means the same class triggers a god class warning in Grep mode but passes cleanly in Treelint mode</quote>
    <line_reference>lines 437-481</line_reference>
  </origin>
  <decision rationale="Treelint's AST-aware threshold is authoritative">
    <selected>Unify Grep threshold to match Treelint (>20)</selected>
    <rejected>Lower Treelint threshold to match Grep (>15)</rejected>
    <trade_off>Consistency vs detection sensitivity</trade_off>
  </decision>
</provenance -->

## User Story

**As a** framework maintainer responsible for anti-pattern detection consistency,
**I want** the legacy Grep god class detection threshold unified from >15 methods to >20 methods to match the Treelint AST-aware threshold,
**So that** both detection modes produce identical results for the same codebase, eliminating false positive god class warnings for classes with 16-20 methods when scanned via Grep fallback.

## Acceptance Criteria

<acceptance_criteria id="AC1" title="Legacy Grep god class method threshold updated to >20">
  <given>The anti-pattern-scanner.md file contains the Phase 5 Check 1 (God Object Detection) with a legacy Grep threshold of >15 methods</given>
  <when>The threshold value is updated</when>
  <then>All references to the god class method threshold read ">20 methods" instead of ">15 methods"</then>
  <verification>
    <method>Grep anti-pattern-scanner.md for "15 methods", verify 0 matches</method>
    <expected_result>No references to >15 threshold remain</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/anti-pattern-scanner.md" hint="Lines 115, 391"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC2" title="Treelint god class threshold remains unchanged at >20">
  <given>The Treelint detection mode uses a >20 method threshold</given>
  <when>The legacy Grep threshold is updated</when>
  <then>The Treelint threshold remains exactly ">20 methods per class" with zero modifications</then>
  <verification>
    <method>Verify Treelint patterns file unchanged</method>
    <expected_result>No changes to Treelint detection logic</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/code-reviewer/references/treelint-review-patterns.md" hint="Line 34: >20 methods"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC3" title="Both detection modes produce identical results">
  <given>A class with exactly 18 public methods exists</given>
  <when>The anti-pattern scanner runs in Treelint mode AND legacy Grep mode</when>
  <then>Both modes return the same result: no god class violation (18 is not >20)</then>
  <verification>
    <method>Test with 18-method class in both modes</method>
    <expected_result>Both modes: no violation</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/anti-pattern-scanner.md" hint="Phase 5 detection logic"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC4" title="Inline comment documents alignment rationale">
  <given>The god class method threshold has been updated to >20</given>
  <when>The change is reviewed</when>
  <then>An inline HTML comment `<!-- Threshold unified to >20 per REC-369-001 to match Treelint mode -->` is present adjacent to each updated threshold</then>
  <verification>
    <method>Grep for "REC-369-001" in modified files</method>
    <expected_result>Comment present at each threshold location</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/anti-pattern-scanner.md" hint="Add inline comment"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC5" title="No other thresholds are modified">
  <given>The anti-pattern-scanner contains multiple detection thresholds</given>
  <when>The god class method threshold is updated</when>
  <then>All other thresholds remain unchanged: line count >300, long method >50 lines, magic numbers unmodified</then>
  <verification>
    <method>Verify only method threshold changed, not line/other thresholds</method>
    <expected_result>Only >15 → >20 changes, all other thresholds intact</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/agents/anti-pattern-scanner.md" hint="Other thresholds unchanged"/>
  </source_files>
</acceptance_criteria>

## Technical Specification

### Component Overview

| Component | Type | Description |
|-----------|------|-------------|
| anti-pattern-scanner.md | Configuration | Update god class threshold from >15 to >20 |

### Technical Details

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Configuration
      name: God Class Threshold Unification
      file_path: src/claude/agents/anti-pattern-scanner.md
      description: Unify god class method threshold to >20 across both detection modes
      dependencies:
        - src/claude/agents/anti-pattern-scanner/references/phase5-code-smells.md
        - src/claude/agents/anti-pattern-scanner/references/phase1-context-loading.md
      test_requirement: All >15 method references changed to >20

  business_rules:
    - rule: Method count threshold
      description: Threshold is strictly > 20 (21+ triggers violation)
      test_requirement: Class with 20 methods passes, 21 triggers violation

    - rule: Line count threshold unchanged
      description: God class line count remains > 300
      test_requirement: Line threshold still 300 after change

  non_functional_requirements:
    - category: Performance
      requirement: No execution time impact
      metric: Documentation-only change (4-6 lines)
      test_requirement: Scanner execution unchanged
```

### Files to Modify

| File | Line | Current | New |
|------|------|---------|-----|
| `src/claude/agents/anti-pattern-scanner.md` | 115 | >15 methods | >20 methods |
| `src/claude/agents/anti-pattern-scanner.md` | 391 | >15 methods | >20 methods |
| `src/claude/agents/anti-pattern-scanner/references/phase5-code-smells.md` | 9 | >15 methods | >20 methods |
| `src/claude/agents/anti-pattern-scanner/references/phase1-context-loading.md` | 94 | >15 methods | >20 methods |

## Edge Cases

1. **Feature 3 extraction already applied:** Threshold may be in reference files. Search both core and reference files.

2. **Downstream references:** QA skill prompt templates may also reference >15. Document as follow-up if out-of-scope.

3. **Output contract example:** Example violation text (line 245) should also be updated.

4. **Exactly 20 methods (boundary):** 20 methods = pass, 21 methods = violation. Both modes must agree.

5. **Mixed-language codebase:** Treelint for .py/.ts, Grep for .cs/.java. Both paths must use >20.

6. **Context summary shortcut path:** Phase 5 detection still uses >20 even when skipping Phase 1.

## Non-Functional Requirements

| Category | Requirement | Metric |
|----------|-------------|--------|
| Performance | Zero impact | Documentation-only, 4-6 lines changed |
| Reliability | Idempotent | Re-applying produces identical results |
| Security | No impact | Threshold change only, no code paths modified |

## Definition of Done

### Implementation
- [x] anti-pattern-scanner.md line 115 updated to >20 methods
- [x] anti-pattern-scanner.md line 205 updated to >20 methods (note: line 391 was incorrect in story spec, actual line is 205)
- [x] phase5-code-smells.md references updated to >20
- [x] phase1-context-loading.md reference updated to >20
- [x] Inline HTML comment added at each threshold
- [x] phase5-treelint-detection.md threshold note updated

### Quality
- [x] All >15 references eliminated (grep returns 0 matches in modified files)
- [x] Treelint threshold unchanged at >20
- [x] Other thresholds (>300 lines, >50 lines) unchanged
- [x] Both modes agree on boundary condition (20 methods = pass)

### Testing
- [x] Grep for "15 methods" returns 0 matches in modified files
- [x] Grep for "REC-369-001" returns match at each threshold
- [x] Treelint patterns file shows no changes (verified unchanged)
- [x] 18-method class: no violation in both modes (verified via threshold logic)
- [x] 21-method class: violation in both modes (verified via threshold logic)

### Documentation
- [x] Inline comment documents rationale per REC-369-001

## Notes

- **Source Recommendation:** REC-369-001 from STORY-369 Phase 09 framework-analyst analysis
- **Root Cause:** Grep and Treelint modes use different thresholds (15 vs 20)
- **Impact:** Eliminates false positives for 16-20 method classes
- **Recommended order:** Implement after Feature 3 (extraction may restructure file)

## Key References

| Reference | Path | Relevance |
|-----------|------|-----------|
| Anti-Pattern Scanner | `src/claude/agents/anti-pattern-scanner.md` | Target file |
| Treelint Review Patterns | `src/claude/agents/code-reviewer/references/treelint-review-patterns.md` | Line 34: Treelint threshold |
| Anti-Patterns Context | `devforgeai/specs/context/anti-patterns.md` | Category 4: Code Smells |

## Implementation Notes

**Developer:** claude
**Implemented:** 2026-02-10
**Branch:** main

- [x] anti-pattern-scanner.md line 115 updated to >20 methods - Completed: Updated Category 4 god object threshold from >15 to >20 with REC-369-001 comment
- [x] anti-pattern-scanner.md line 205 updated to >20 methods (note: line 391 was incorrect in story spec, actual line is 205) - Completed: Updated Phase 5 detection threshold from >15 to >20 with REC-369-001 comment
- [x] phase5-code-smells.md references updated to >20 - Completed: Updated Check 1 heading (line 9) and detection logic (line 17) from >15 to >20
- [x] phase1-context-loading.md reference updated to >20 - Completed: Updated god object thresholds extraction (line 94) from >15 to >20
- [x] Inline HTML comment added at each threshold - Completed: Added `<!-- Threshold unified to >20 per REC-369-001 to match Treelint mode -->` at 7 threshold locations
- [x] phase5-treelint-detection.md threshold note updated - Completed: Updated threshold note to document unified >20 threshold for both detection modes
- [x] All >15 references eliminated (grep returns 0 matches in modified files) - Completed: Verified zero matches via test_ac1_legacy_grep_threshold.sh
- [x] Treelint threshold unchanged at >20 - Completed: Verified treelint-review-patterns.md unchanged via test_ac2_treelint_threshold_unchanged.sh
- [x] Other thresholds (>300 lines, >50 lines) unchanged - Completed: Verified via test_ac5_other_thresholds_unchanged.sh
- [x] Both modes agree on boundary condition (20 methods = pass) - Completed: Verified via test_ac3_identical_detection_results.sh
- [x] Grep for "15 methods" returns 0 matches in modified files - Completed: 4/4 assertions pass in test_ac1
- [x] Grep for "REC-369-001" returns match at each threshold - Completed: 4/4 assertions pass in test_ac4
- [x] Treelint patterns file shows no changes (verified unchanged) - Completed: File verified unchanged
- [x] 18-method class: no violation in both modes (verified via threshold logic) - Completed: Threshold is >20, so 18 methods passes
- [x] 21-method class: violation in both modes (verified via threshold logic) - Completed: Threshold is >20, so 21 methods triggers violation
- [x] Inline comment documents rationale per REC-369-001 - Completed: REC-369-001 comment present at all threshold locations

### Out-of-Scope References
Per Edge Case 2, the following files contain example/illustration references to old thresholds:
- `internet-sleuth-integration/references/repository-archaeology-guide.md` - example violation
- `bundled/` directory - build artifacts, regenerated during release

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/opus | Story Creation | Initial story created from EPIC-063 Feature 7 | STORY-405-unify-god-class-threshold.story.md |
| 2026-02-10 | .claude/qa-result-interpreter | QA Deep | PASSED: 5/5 ACs validated, 0 violations, 2/2 validators | - |
