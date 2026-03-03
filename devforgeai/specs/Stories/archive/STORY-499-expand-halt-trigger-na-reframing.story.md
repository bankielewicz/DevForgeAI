---
id: STORY-499
title: Expand Halt Trigger to Cover "Not Applicable" Reframing
type: feature
epic: null
sprint: Backlog
status: QA Approved
points: 1
depends_on: []
priority: Medium
advisory: false
assigned_to: ""
created: 2026-02-24
format_version: "2.9"
source_rca: RCA-041
source_recommendation: REC-3
---

# Story: Expand Halt Trigger to Cover "Not Applicable" Reframing

## Description

**As a** DevForgeAI framework maintainer,
**I want** the halt trigger in system-prompt-core.md expanded to cover "abbreviate" and "not applicable" reframing of phase skips,
**so that** LLM executors cannot bypass phase enforcement by cognitively reframing skipping as declaring a phase "N/A" — closing the cognitive loophole identified in RCA-041 Why #3.

## Provenance

```xml
<provenance>
  <origin document="RCA-041" section="5-whys-analysis">
    <quote>"The action was reframed as 'not applicable' rather than 'skipping.' The halt trigger's language ('skip a workflow phase') didn't capture this cognitive bypass."</quote>
    <line_reference>lines 33-34</line_reference>
    <quantified_impact>9 of 10 release phases skipped without audit trail in a single session</quantified_impact>
  </origin>

  <decision rationale="defense-in-depth-with-structural-enforcement">
    <selected>Expand halt trigger language to cover skip, abbreviate, and "not applicable" — complements STORY-497 structural marker enforcement</selected>
    <rejected alternative="structural-enforcement-only">
      Structural enforcement alone (STORY-497) catches violations at runtime but does not prevent the intent to skip from forming. Language-level triggers provide earlier interception.
    </rejected>
    <trade_off>Slightly longer halt trigger text in system prompt (~80 bytes) for broader bypass coverage</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### XML Acceptance Criteria Format

Use the following XML schema for each acceptance criterion:

```xml
<acceptance_criteria id="AC1" implements="COMP-XXX,COMP-YYY">
  <given>Initial context or precondition</given>
  <when>Action or event being tested</when>
  <then>Expected outcome or result</then>
</acceptance_criteria>
```

### AC#1: Halt Trigger Text Updated in Operational File

```xml
<acceptance_criteria id="AC1" implements="SVC-001">
  <given>The file .claude/system-prompt-core.md contains the halt trigger "WHEN about to skip a workflow phase THEN HALT and complete the current phase first." on line 44</given>
  <when>The STORY-499 change is applied</when>
  <then>Line 44 reads: "WHEN about to skip, abbreviate, or declare 'not applicable' for any workflow phase THEN HALT — load the phase reference file first, then evaluate applicability." and no other halt trigger lines are modified.</then>
  <verification>
    <source_files>
      <file hint="Operational system prompt">.claude/system-prompt-core.md</file>
    </source_files>
    <test_file>tests/STORY-499/test_ac1_halt_trigger_operational.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Halt Trigger Text Updated in Source File (Dual-Path Parity)

```xml
<acceptance_criteria id="AC2" implements="SVC-002">
  <given>The file src/claude/system-prompt-core.md contains the same halt trigger on line 44</given>
  <when>The STORY-499 change is applied</when>
  <then>The halt trigger text in src/claude/system-prompt-core.md is identical (byte-for-byte) to the text in .claude/system-prompt-core.md line 44</then>
  <verification>
    <source_files>
      <file hint="Source system prompt">src/claude/system-prompt-core.md</file>
    </source_files>
    <test_file>tests/STORY-499/test_ac2_halt_trigger_source.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Original Skip Coverage Preserved

```xml
<acceptance_criteria id="AC3">
  <given>The updated halt trigger text</given>
  <when>The text is inspected</when>
  <then>The word "skip" is still present in the trigger (backward compatibility) and the trigger covers exactly three bypass patterns: skip, abbreviate, and declare "not applicable"</then>
</acceptance_criteria>
```

---

### AC#4: Prescriptive Action Includes Reference File Loading

```xml
<acceptance_criteria id="AC4">
  <given>The updated halt trigger fires</given>
  <when>An LLM executor encounters the halt</when>
  <then>The trigger text prescribes loading the phase reference file before evaluating applicability (not just halting)</then>
</acceptance_criteria>
```

---

### Source Files Guidance

The `<source_files>` element provides hints to the ac-compliance-verifier about where implementation code is located.

**Source Files for This Story:**
- `.claude/system-prompt-core.md` — Operational halt trigger (line 44)
- `src/claude/system-prompt-core.md` — Source halt trigger (line 44, dual-path mirror)

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "System Prompt Halt Trigger Expansion"
      file_path: ".claude/system-prompt-core.md"
      purpose: "Expand phase-skip halt trigger to cover N/A reframing"
      requirements:
        - id: "SVC-001"
          description: "Replace narrow 'skip' trigger with expanded trigger covering skip, abbreviate, and 'not applicable'"
          testable: true
          test_requirement: "Test: Grep line 44 for all three keywords (skip, abbreviate, not applicable)"
          priority: "Medium"
        - id: "SVC-002"
          description: "Apply identical change to src/claude/system-prompt-core.md (dual-path parity)"
          testable: true
          test_requirement: "Test: diff .claude/system-prompt-core.md src/claude/system-prompt-core.md exits 0 for halt_triggers block"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "Halt trigger must fire on any form of phase bypass: skip, abbreviate, declare N/A"
      trigger: "LLM executor attempts to bypass a workflow phase"
      validation: "Halt trigger text contains all three bypass patterns"
      error_handling: "HALT workflow and require phase reference loading"
      test_requirement: "Test: Verify trigger text contains 'skip', 'abbreviate', and 'not applicable'"
      priority: "Medium"
    - id: "BR-002"
      rule: "Dual-path files must remain in sync after modification"
      trigger: "Any modification to .claude/system-prompt-core.md"
      validation: "src/ mirror contains identical content"
      error_handling: "Block commit if files diverge"
      test_requirement: "Test: diff between operational and source files returns exit code 0"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Halt trigger text"
    limitation: "Cannot cover every possible synonym for skipping (e.g., 'irrelevant', 'unnecessary', 'does not apply'). Only covers the three terms identified in RCA-041."
    decision: "workaround:Future RCAs may expand the list if new synonyms emerge. STORY-497 structural enforcement provides runtime backup."
    discovered_phase: "Architecture"
    impact: "Low - structural enforcement (STORY-497) catches any bypass regardless of language used"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Zero runtime impact: halt triggers are prompt text parsed at context load, no computation involved

**Throughput:**
- File size increase: less than 100 bytes (single line expansion)

**Performance Test:**
- Verify file size delta is < 100 bytes

---

### Security

**Authentication:**
- None required (framework configuration file)

**Authorization:**
- None required

**Data Protection:**
- No sensitive data introduced
- No secrets or credentials in trigger text

**Security Testing:**
- [ ] No hardcoded secrets
- [ ] No new file paths or permissions required

---

### Scalability

**Horizontal Scaling:**
- Not applicable (static configuration file)

**Database:**
- Not applicable

**Caching:**
- Not applicable

---

### Reliability

**Error Handling:**
- Dual-path parity enforced via AC2 prevents silent divergence
- Backward compatible: existing "skip" detection unchanged (superset expansion only)

**Retry Logic:**
- Not applicable (one-time configuration change)

**Monitoring:**
- Post-change: Grep both files for expanded trigger text to verify

---

### Observability

**Logging:**
- Not applicable (no runtime component)

**Metrics:**
- Not applicable

**Tracing:**
- Not applicable

---

## Dependencies

### Prerequisite Stories

No prerequisite stories required:
- This story is independent and can start immediately
- Complements STORY-497 (phase markers) but does not depend on it

### External Dependencies

No external dependencies.

### Technology Dependencies

No new packages or versions required:
- Uses existing Edit tool for file modification
- Uses existing Grep tool for verification

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Both files updated with expanded trigger text, old trigger text absent
2. **Edge Cases:**
   - Only one file updated (should fail AC2)
   - Trigger text has smart quotes instead of straight quotes
   - Other halt triggers accidentally modified
3. **Error Cases:**
   - Old trigger text still present after change (incomplete replacement)
   - Line 44 content doesn't match expected new text

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **Dual-Path Parity:** diff between .claude/ and src/ files returns exit code 0 for halt_triggers block
2. **Halt Trigger Count:** Same number of halt triggers before and after change

---

### E2E Tests (If Applicable)

Not applicable for this configuration change.

---

## Acceptance Criteria Verification Checklist

**Purpose:** Real-time progress tracking during TDD implementation.

**Tracking Mechanisms:**
- **TodoWrite:** Phase-level tracking (AI monitors workflow position)
- **AC Checklist:** AC sub-item tracking (user sees granular progress) ← YOU ARE HERE
- **Definition of Done:** Official completion record (quality gate validation)

### AC#1: Halt Trigger Text Updated in Operational File

- [x] Old trigger text replaced in .claude/system-prompt-core.md - **Phase:** 3 - **Evidence:** Edit tool output
- [x] New trigger text contains "skip, abbreviate, or declare" - **Phase:** 3 - **Evidence:** Grep verification
- [x] No other halt triggers modified - **Phase:** 3 - **Evidence:** diff of non-line-44 content

### AC#2: Halt Trigger Text Updated in Source File

- [x] Old trigger text replaced in src/claude/system-prompt-core.md - **Phase:** 3 - **Evidence:** Edit tool output
- [x] Byte-for-byte parity with operational file on line 44 - **Phase:** 5 - **Evidence:** diff output

### AC#3: Original Skip Coverage Preserved

- [x] Word "skip" present in updated trigger - **Phase:** 3 - **Evidence:** Grep verification
- [x] Three bypass patterns present: skip, abbreviate, not applicable - **Phase:** 3 - **Evidence:** Grep verification

### AC#4: Prescriptive Action Includes Reference File Loading

- [x] Trigger text includes "load the phase reference file first" - **Phase:** 3 - **Evidence:** Grep verification

---

**Checklist Progress:** 7/7 items complete (100%)

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

- [x] Halt trigger text updated in .claude/system-prompt-core.md line 44 - Completed: Replaced narrow "skip" trigger with expanded text covering skip, abbreviate, and "not applicable" bypass patterns
- [x] Halt trigger text updated in src/claude/system-prompt-core.md line 44 - Completed: Identical edit applied to source mirror file
- [x] Both files contain identical expanded trigger text - Completed: Byte-for-byte parity verified via grep and AC#2 test suite
- [x] No other halt triggers modified in either file - Completed: Lines 42, 43, 45, 46, 47 unchanged; 6 total triggers maintained
- [x] All 4 acceptance criteria have passing tests - Completed: 33 assertions across 4 test suites, all passing
- [x] Edge cases covered (smart quotes, single-file update, accidental modification) - Completed: Tests verify exact text, old text absence, parity, and trigger count
- [x] Dual-path parity verified via diff - Completed: AC#2 test verifies line 44 identical in both files
- [x] Unit tests for trigger text content in .claude/system-prompt-core.md - Completed: test_ac1_halt_trigger_operational.sh (8 assertions)
- [x] Unit tests for trigger text content in src/claude/system-prompt-core.md - Completed: test_ac2_halt_trigger_source.sh (9 assertions)
- [x] Integration test for dual-path parity (diff exit code 0) - Completed: AC#2 includes block-level parity test (lines 39-48)
- [x] RCA-041 updated with STORY-499 link for REC-3 - Completed: REC-3 checklist item marked [x] in RCA-041
- [x] Change log updated in this story file - Completed: Change log updated with implementation details

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-24

## Definition of Done

### Implementation
- [x] Halt trigger text updated in .claude/system-prompt-core.md line 44
- [x] Halt trigger text updated in src/claude/system-prompt-core.md line 44
- [x] Both files contain identical expanded trigger text
- [x] No other halt triggers modified in either file

### Quality
- [x] All 4 acceptance criteria have passing tests
- [x] Edge cases covered (smart quotes, single-file update, accidental modification)
- [x] Dual-path parity verified via diff

### Testing
- [x] Unit tests for trigger text content in .claude/system-prompt-core.md
- [x] Unit tests for trigger text content in src/claude/system-prompt-core.md
- [x] Integration test for dual-path parity (diff exit code 0)

### Documentation
- [x] RCA-041 updated with STORY-499 link for REC-3
- [x] Change log updated in this story file

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✓ Complete | Git validated, 6 context files loaded, tech stack verified |
| 02 Red | ✓ Complete | 33 assertions across 4 test suites, all FAILING (expected) |
| 03 Green | ✓ Complete | Line 44 updated in both files, 33/33 assertions PASSING |
| 04 Refactor | ✓ Complete | Code review APPROVED, no refactoring changes needed |
| 4.5 AC Verify | ✓ Complete | 4/4 ACs PASS with HIGH confidence |
| 05 Integration | ✓ Complete | Dual-path parity verified, 33/33 passing |
| 5.5 AC Verify | ✓ Complete | 4/4 ACs PASS (second verification) |
| 06 Deferral | ✓ Complete | 0 deferrals — all DoD items achievable |
| 07 DoD Update | ✓ Complete | 12/12 DoD items marked [x], status → Dev Complete |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| .claude/system-prompt-core.md | Modified | Line 44 |
| src/claude/system-prompt-core.md | Modified | Line 44 |
| tests/STORY-499/test_ac1_halt_trigger_operational.sh | Created | ~80 |
| tests/STORY-499/test_ac2_halt_trigger_source.sh | Created | ~90 |
| tests/STORY-499/test_ac3_skip_coverage.sh | Created | ~80 |
| tests/STORY-499/test_ac4_prescriptive_action.sh | Created | ~80 |
| tests/STORY-499/run_all_tests.sh | Created | ~50 |
| devforgeai/RCA/RCA-041*.md | Modified | Line 220 |

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-24 | /create-stories-from-rca + devforgeai-story-creation | Created | Story created from RCA-041 REC-3 | STORY-499 |
| 2026-02-24 | DevForgeAI AI Agent | /dev TDD Complete | Expanded halt trigger text in both dual-path files. 4 ACs verified, 33 assertions passing, 0 deferrals. | .claude/system-prompt-core.md, src/claude/system-prompt-core.md, tests/STORY-499/*, devforgeai/RCA/RCA-041*.md |
| 2026-02-24 | .claude/qa-result-interpreter | QA Deep | PASSED: 33/33 tests, 0 critical/high violations, 3/3 validators passed | devforgeai/qa/reports/STORY-499-qa-report.md |

## Notes

**Source:** RCA-041 (Release Skill Phase Skip Violation), REC-3 (MEDIUM priority)

**Defense-in-Depth Strategy:**
- STORY-497 (REC-1, CRITICAL): Structural enforcement via phase markers — catches violations at runtime
- STORY-498 (REC-2, HIGH): Library crate adaptive path — documents legitimate skip paths
- **STORY-499 (REC-3, MEDIUM): Halt trigger expansion — prevents the intent to skip from forming (this story)**

**Backward Compatibility - Acceptance Criteria Format:**
> **Legacy markdown AC format (Given/When/Then bullets) is NOT supported by automated verification.**
> The ac-compliance-verifier subagent requires XML `<acceptance_criteria>` blocks to parse and verify ACs.

**Design Decisions:**
- Chose straight double quotes (`"`) for "not applicable" to avoid encoding issues across editors
- Expanded existing trigger line rather than adding a new trigger to maintain halt_triggers section structure

**Open Questions:**
- None

**Related ADRs:**
- None required (text expansion within existing pattern)

**References:**
- RCA-041: `devforgeai/RCA/RCA-041-release-skill-phase-skip-violation.md`
- STORY-497: Phase Marker Protocol (structural enforcement complement)
- STORY-498: Library Crate Adaptive Path (documented skip paths)

---

Story Template Version: 2.9
Last Updated: 2026-02-24
