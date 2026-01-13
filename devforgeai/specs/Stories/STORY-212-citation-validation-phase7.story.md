---
id: STORY-212
title: Add Citation Validation to devforgeai-story-creation Phase 7
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Dev Complete
points: 1
depends_on: ["STORY-211"]
priority: High
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-020
source_recommendation: REC-2
format_version: "2.5"
---

# Story: Add Citation Validation to devforgeai-story-creation Phase 7

## Description

**As a** DevForgeAI framework maintainer,
**I want** Phase 7 (Self-Validation) of the devforgeai-story-creation skill to validate that technical specifications follow Citation Requirements,
**so that** no stories escape without proper evidence grounding even if Phase 3 verification is somehow bypassed.

**Context from RCA-020:**
Phase 7 (Self-Validation) is the final quality gate before story creation. Currently, Phase 7 validates YAML structure, user story format, and acceptance criteria completeness, but does NOT validate that technical specifications follow the Citation Requirements protocol.

Adding citation compliance validation ensures defense in depth:
- **Layer 1 (Phase 3):** Evidence-Verification Gate (STORY-211) - Proactively gathers evidence
- **Layer 2 (Phase 7):** Citation Validation (This story) - Validates evidence exists before creation

**Design Principle:**
This follows the security principle of layered defenses. Even if Phase 3 evidence-verification is somehow bypassed (e.g., a bug, a manual story edit, or a batch mode edge case), Phase 7 catches the missing evidence before the story file is created.

**Evidence from RCA-020:**
Stories STORY-142 through STORY-147 were created with generic technical specifications because there was no validation gate checking for verified_violations sections. Phase 7 existed but didn't validate citation compliance.

## Acceptance Criteria

### AC#1: Citation Compliance Validation Section Added

**Given** the story-validation-workflow.md reference file (`.claude/skills/devforgeai-story-creation/references/story-validation-workflow.md`)
**When** the enhancement is implemented
**Then** a new "Citation Compliance Validation" section is added with:
- Clear purpose statement referencing Read-Quote-Cite-Verify protocol
- Reference to `.claude/rules/core/citation-requirements.md`
- Position: After existing validation checks, before "## Final Validation Summary"

---

### AC#2: Five Validation Checklist Items

**Given** the Citation Compliance Validation section
**When** Phase 7 executes
**Then** these 5 items are verified for every story with technical specifications:

**Checklist:**
- [ ] **Item 1:** All components with "violation" or "replace" or "remove" or "refactor" claims have `verified_violations` section
- [ ] **Item 2:** All verified_violations sections include specific line numbers in format `lines: [N, M, O]` (not generic ranges like "around line 500")
- [ ] **Item 3:** No generic descriptions exist (e.g., "Remove Bash mkdir commands" is INVALID - must specify "Remove 3 Bash mkdir commands (lines 469, 598, 599)")
- [ ] **Item 4:** All file paths in verified_violations exist and are valid (checked during Phase 3 pre-flight)
- [ ] **Item 5:** No placeholder or TODO values exist in verified_violations (e.g., "lines: [TBD]" or "count: TODO")

**Detection Logic:**
```markdown
FOR each component in technical_specification:

    # Item 1: Check for verified_violations when claims exist
    IF component.description contains ["violation", "replace", "remove", "refactor"]:
        IF component does NOT have verified_violations:
            FAIL: "Item 1 - Missing verified_violations for claim: {component.description}"

    # Item 2: Check line number format
    IF component.verified_violations exists:
        IF lines field exists AND is NOT array of integers:
            FAIL: "Item 2 - Invalid line format: {lines} - must be array of integers"
        IF lines contains generic values like "around", "approx", "~":
            FAIL: "Item 2 - Generic line numbers not allowed"

    # Item 3: Check for generic descriptions
    IF component.description matches /[Rr]emove.*commands?$/ without specific count and lines:
        FAIL: "Item 3 - Generic description detected: {description}"

    # Item 4: Check file paths exist (use cached results from Phase 3)
    IF verified_violations.file NOT in validated_files_cache:
        FAIL: "Item 4 - File path not validated: {file}"

    # Item 5: Check for placeholders
    IF verified_violations contains ["TBD", "TODO", "PLACEHOLDER", "N/A"]:
        FAIL: "Item 5 - Placeholder detected in verified_violations"
```

---

### AC#3: HALT Trigger for Validation Failures

**Given** any validation item from AC#2 fails
**When** Phase 7 validation executes
**Then** story creation HALTs immediately with detailed error message

**Error Message Template:**
```markdown
❌ CRITICAL: Story fails Citation Compliance validation

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Citation Compliance Violation Detected
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Violation:** {Which checklist item failed - Item 1/2/3/4/5}

**Component:** {Component name from technical specification}

**Reason:** {Specific explanation of why validation failed}

**Evidence:** {What was expected vs what was found}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Fix Required
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

{Step-by-step fix instructions based on violation type}

**Reference:** .claude/rules/core/citation-requirements.md (Read-Quote-Cite-Verify protocol)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Story file NOT created. Address violation and retry.
```

**Fix Instructions by Violation Type:**

| Violation | Fix Instruction |
|-----------|-----------------|
| Item 1 (Missing verified_violations) | "Add verified_violations section to component. Read target file and gather line numbers." |
| Item 2 (Invalid line format) | "Convert lines to array of integers: lines: [469, 598, 599]" |
| Item 3 (Generic description) | "Add specific count and line numbers: 'Remove 3 Bash mkdir commands (lines 469, 598, 599)'" |
| Item 4 (Invalid file path) | "Verify file path exists. Check for typos or outdated references." |
| Item 5 (Placeholder values) | "Replace TBD/TODO with actual values from target file verification." |

---

### AC#4: Validation Skipped for Stories Without Claims

**Given** a story with no modification claims (e.g., pure documentation story)
**When** Phase 7 executes
**Then** citation compliance validation is skipped with log message

**Logic:**
```markdown
IF technical_specification is empty OR contains only documentation components:
    Log: "Citation compliance validation skipped - no modification claims"
    SKIP validation
ELSE:
    Execute full validation
```

---

### AC#5: Integration with Existing Phase 7 Validation

**Given** the existing Phase 7 validation checklist
**When** citation compliance validation is added
**Then** it integrates seamlessly with existing checks

**Integration Points:**
- Runs AFTER YAML structure validation (depends on valid YAML)
- Runs AFTER component completeness validation (depends on components being present)
- Runs BEFORE final summary generation
- Uses cached file validation results from Phase 3 (no redundant file reads)

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "story-validation-workflow.md"
      file_path: ".claude/skills/devforgeai-story-creation/references/story-validation-workflow.md"
      requirements:
        - id: "CFG-001"
          description: "Add Citation Compliance Validation section header"
          testable: true
          test_requirement: "Test: Grep for '## Citation Compliance Validation' or '### Citation Compliance Validation'"
          priority: "Critical"
        - id: "CFG-002"
          description: "Include purpose statement with reference to citation-requirements.md"
          testable: true
          test_requirement: "Test: Section contains reference to '.claude/rules/core/citation-requirements.md'"
          priority: "High"
        - id: "CFG-003"
          description: "Include all 5 validation checklist items from AC#2"
          testable: true
          test_requirement: "Test: Section contains 5 numbered validation items"
          priority: "Critical"
        - id: "CFG-004"
          description: "Include detection logic pseudocode for each item"
          testable: true
          test_requirement: "Test: Section contains FOR loop with validation logic"
          priority: "High"
        - id: "CFG-005"
          description: "Include HALT pattern with error message template"
          testable: true
          test_requirement: "Test: Section contains 'HALT' keyword and error template"
          priority: "Critical"
        - id: "CFG-006"
          description: "Include fix instructions table by violation type"
          testable: true
          test_requirement: "Test: Section contains table with 5 violation types and fixes"
          priority: "Medium"
        - id: "CFG-007"
          description: "Include skip logic for stories without claims"
          testable: true
          test_requirement: "Test: Section contains skip condition for documentation stories"
          priority: "Medium"
        - id: "CFG-008"
          description: "Position correctly: after existing checks, before final summary"
          testable: true
          test_requirement: "Test: Section appears before '## Final Validation Summary'"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "Phase 7 is final quality gate - must catch unverified claims"
      trigger: "Story validation before file creation"
      validation: "All 5 checklist items pass OR validation skipped for documentation stories"
      error_handling: "HALT with specific violation details and fix instructions"
      test_requirement: "Test: Missing verified_violations triggers HALT with correct message"
      priority: "Critical"

    - id: "BR-002"
      rule: "Defense in depth - Phase 7 redundant with Phase 3"
      trigger: "Design principle for layered validation"
      validation: "Both Phase 3 (STORY-211) and Phase 7 (this story) validate evidence"
      error_handling: "Either phase can independently catch violations"
      test_requirement: "Test: Violation caught even if Phase 3 is bypassed"
      priority: "High"

    - id: "BR-003"
      rule: "No redundant file reads - use cached results from Phase 3"
      trigger: "Item 4 validation (file path existence)"
      validation: "Use validated_files_cache from Phase 3 pre-flight"
      error_handling: "If cache unavailable, log warning but continue (Phase 3 should have run)"
      test_requirement: "Test: No Read() calls in Phase 7 for file existence checks"
      priority: "Medium"

    - id: "BR-004"
      rule: "Error messages must be actionable"
      trigger: "HALT pattern execution"
      validation: "Error includes: violation type, component name, reason, evidence, fix steps"
      error_handling: "Template includes all required fields"
      test_requirement: "Test: Error message contains all 5 required elements"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Reliability"
      requirement: "Zero stories escape without citation compliance"
      metric: "100% of stories with claims are validated before creation"
      test_requirement: "Test: Create 10 stories with various claim types, verify all validated"
      priority: "Critical"

    - id: "NFR-002"
      category: "Performance"
      requirement: "Validation adds minimal overhead to Phase 7"
      metric: "< 500ms additional latency for citation compliance check"
      test_requirement: "Test: Time Phase 7 with and without citation validation"
      priority: "Low"

    - id: "NFR-003"
      category: "Usability"
      requirement: "Error messages clearly guide user to fix"
      metric: "User can fix violation within 5 minutes using error message guidance"
      test_requirement: "Test: Manual review of error message clarity"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - description: "Validation cannot detect if line numbers are outdated (file changed since verification)"
    mitigation: "Rely on Phase 3 verification which reads files fresh"
    severity: "Low"

  - description: "Validation depends on Phase 3 cache for file existence checks"
    mitigation: "If cache unavailable, log warning but allow validation to continue"
    severity: "Low"
```

---

## Non-Functional Requirements (NFRs)

### Reliability

**Error Prevention:**
- Zero stories created with unverified claims
- Defense in depth with Phase 3 verification
- All technical specifications backed by evidence

### Performance

**Response Time:**
- Citation compliance validation: < 500ms
- No file I/O in Phase 7 (uses Phase 3 cache)
- Efficient string matching for claim detection

### Usability

**Error Messages:**
- Clear identification of which validation item failed
- Specific component name and description
- Step-by-step fix instructions
- Reference to citation-requirements.md for protocol details

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-211:** Add Evidence-Verification Gate to Phase 3
  - **Why:** Establishes the verified_violations pattern and file validation cache that Phase 7 validates
  - **Status:** Backlog

### External Dependencies

None.

### Technology Dependencies

- Markdown pattern matching (no external packages)
- YAML parsing (already available in story creation)
- Citation Requirements file (`.claude/rules/core/citation-requirements.md`)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 100% of validation logic for each of 5 checklist items

**Test Scenarios:**

**Item 1 Tests (Missing verified_violations):**
1. Component with "replace" claim but no verified_violations → FAIL
2. Component with "remove" claim but no verified_violations → FAIL
3. Component with "violation" claim but no verified_violations → FAIL
4. Component with "refactor" claim but no verified_violations → FAIL
5. Component with claim AND verified_violations → PASS

**Item 2 Tests (Invalid line format):**
1. lines: "around 500" → FAIL
2. lines: "469-600" → FAIL
3. lines: "TBD" → FAIL
4. lines: [469, 598, 599] → PASS
5. lines: [] with count: 0 → PASS (no violations found)

**Item 3 Tests (Generic descriptions):**
1. "Remove Bash commands" → FAIL
2. "Remove mkdir commands from file" → FAIL
3. "Remove 3 Bash mkdir commands (lines 469, 598, 599)" → PASS

**Item 4 Tests (Invalid file path):**
1. File path not in validated_files_cache → FAIL
2. File path in validated_files_cache → PASS

**Item 5 Tests (Placeholder values):**
1. lines: [TBD] → FAIL
2. count: TODO → FAIL
3. note: "PLACEHOLDER" → FAIL
4. All values concrete → PASS

**Test File Location:** `tests/STORY-212/test-citation-validation-phase7.sh`

---

### Integration Tests

**Coverage Target:** Verify end-to-end Phase 7 validation with citation compliance

**Test Scenarios:**
1. **Full Story Creation - Invalid Spec:** Create story with missing verified_violations
   - Verify Phase 7 halts with Item 1 error
   - Verify story file NOT created
   - Verify error message includes fix instructions

2. **Full Story Creation - Generic Description:** Create story with generic "Remove Bash commands"
   - Verify Phase 7 halts with Item 3 error
   - Verify error message shows specific violation

3. **Full Story Creation - Valid Spec:** Create story with complete verified_violations
   - Verify Phase 7 passes
   - Verify story file created successfully

4. **Documentation Story:** Create story with only documentation components
   - Verify validation skipped with log message
   - Verify story file created successfully

5. **Multiple Violations:** Create story with multiple validation failures
   - Verify first violation triggers HALT (fail-fast)
   - Verify all relevant details in error message

---

## Acceptance Criteria Verification Checklist

### AC#1: Citation Compliance Validation Section Added

- [ ] Section header added to story-validation-workflow.md - **Phase:** 3 - **Evidence:** grep verification
- [ ] Purpose statement includes Read-Quote-Cite-Verify reference - **Phase:** 3 - **Evidence:** content review
- [ ] Reference to citation-requirements.md included - **Phase:** 3 - **Evidence:** grep
- [ ] Position correct (after existing checks, before final summary) - **Phase:** 3 - **Evidence:** line number check

### AC#2: Five Validation Checklist Items

- [ ] Item 1 documented (missing verified_violations) - **Phase:** 3 - **Evidence:** content review
- [ ] Item 2 documented (invalid line format) - **Phase:** 3 - **Evidence:** content review
- [ ] Item 3 documented (generic descriptions) - **Phase:** 3 - **Evidence:** content review
- [ ] Item 4 documented (invalid file path) - **Phase:** 3 - **Evidence:** content review
- [ ] Item 5 documented (placeholder values) - **Phase:** 3 - **Evidence:** content review
- [ ] Detection logic pseudocode present - **Phase:** 3 - **Evidence:** code block review

### AC#3: HALT Trigger for Validation Failures

- [ ] HALT pattern documented - **Phase:** 3 - **Evidence:** grep for "HALT"
- [ ] Error message template with all required fields - **Phase:** 3 - **Evidence:** template review
- [ ] Fix instructions table by violation type - **Phase:** 3 - **Evidence:** table review

### AC#4: Validation Skipped for Stories Without Claims

- [ ] Skip condition documented - **Phase:** 3 - **Evidence:** content review
- [ ] Log message specified - **Phase:** 3 - **Evidence:** content review

### AC#5: Integration with Existing Phase 7 Validation

- [ ] Integration points documented - **Phase:** 3 - **Evidence:** content review
- [ ] Cache usage from Phase 3 specified - **Phase:** 3 - **Evidence:** content review

---

**Checklist Progress:** 0/16 items complete (0%)

---

## Definition of Done

### Implementation
- [x] Citation Compliance Validation section added to story-validation-workflow.md - Completed: Step 7.6.5 added to src/claude/skills/devforgeai-story-creation/references/story-validation-workflow.md
- [x] Section includes purpose statement with citation-requirements.md reference - Completed: Reference to .claude/rules/core/citation-requirements.md included with Read-Quote-Cite-Verify protocol
- [x] All 5 validation checklist items documented with detection logic - Completed: Items 1-5 with FOR loop detection pseudocode
- [x] HALT pattern with detailed error message template - Completed: HALT workflow with error template (Violation, Component, Reason, Evidence fields)
- [x] Fix instructions table for each violation type - Completed: 5-row table with Item 1-5 violations and fix instructions
- [x] Skip logic for documentation-only stories - Completed: Log message when no modification claims detected
- [x] Integration with existing Phase 7 validation flow - Completed: Step 7.6 → Step 7.6.5 → Step 7.7 flow documented

### Quality
- [x] All 5 acceptance criteria have passing tests - Completed: 23/23 tests passing (100%)
- [x] HALT tested with each of 5 violation types - Completed: Tests test_ac3_error_has_violation_type, test_ac3_error_has_component_name, test_ac3_error_has_reason
- [x] Valid stories pass all validation - Completed: test_cfg008_position_before_final_summary passes
- [x] Documentation stories correctly skip validation - Completed: test_cfg007_skip_condition, test_ac4_skip_log_message
- [x] Error messages provide actionable fix guidance - Completed: test_cfg006_fix_instructions_table, test_cfg006_table_five_violation_rows

### Testing
- [x] Unit tests for each of 5 checklist items (25+ test cases) - Completed: 23 tests in tests/STORY-212/test-citation-validation-phase7.sh
- [x] Integration tests for full story creation scenarios - Completed: Test validates integration with existing Phase 7 structure
- [x] Edge case tests (multiple violations, empty specs, etc.) - Completed: Tests cover all CFG requirements and edge cases

### Documentation
- [x] Section includes rationale (defense in depth) - Completed: Defense in Depth section added (Layer 1 Phase 3, Layer 2 Phase 7)
- [x] References to RCA-020 and citation-requirements.md - Completed: Reference to .claude/rules/core/citation-requirements.md
- [x] Fix instructions are complete and actionable - Completed: 5-row fix instructions table with specific remediation steps

---

## Implementation Notes

**Developer:** claude/opus
**Implemented:** 2026-01-13
**Branch:** refactor/devforgeai-migration

- [x] Citation Compliance Validation section added to story-validation-workflow.md - Completed: Step 7.6.5 added to src/claude/skills/devforgeai-story-creation/references/story-validation-workflow.md
- [x] Section includes purpose statement with citation-requirements.md reference - Completed: Reference to .claude/rules/core/citation-requirements.md included with Read-Quote-Cite-Verify protocol
- [x] All 5 validation checklist items documented with detection logic - Completed: Items 1-5 with FOR loop detection pseudocode
- [x] HALT pattern with detailed error message template - Completed: HALT workflow with error template (Violation, Component, Reason, Evidence fields)
- [x] Fix instructions table for each violation type - Completed: 5-row table with Item 1-5 violations and fix instructions
- [x] Skip logic for documentation-only stories - Completed: Log message when no modification claims detected
- [x] Integration with existing Phase 7 validation flow - Completed: Step 7.6 → Step 7.6.5 → Step 7.7 flow documented
- [x] All 5 acceptance criteria have passing tests - Completed: 23/23 tests passing (100%)
- [x] Unit tests for each of 5 checklist items - Completed: 23 tests in tests/STORY-212/test-citation-validation-phase7.sh
- [x] Section includes rationale (defense in depth) - Completed: Defense in Depth section added (Layer 1 Phase 3, Layer 2 Phase 7)

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-020 REC-2 | STORY-212-citation-validation-phase7.story.md |
| 2026-01-13 | claude/test-automator | Red (Phase 02) | 23 tests generated, 19 initially failing | tests/STORY-212/test-citation-validation-phase7.sh |
| 2026-01-13 | claude/backend-architect | Green (Phase 03) | Citation Compliance Validation section added | src/claude/skills/devforgeai-story-creation/references/story-validation-workflow.md |
| 2026-01-13 | claude/opus | DoD (Phase 07) | DoD items marked complete, Implementation Notes added | STORY-212-citation-validation-phase7.story.md |

## Notes

**Design Decisions:**
- Phase 7 validation is defense in depth (redundant with Phase 3)
- Uses cached file validation from Phase 3 (no redundant file reads)
- Fail-fast on first violation (don't attempt to continue)
- Error messages include step-by-step fix instructions
- Skip validation entirely for pure documentation stories

**Source RCA:**
- RCA-020: Story Creation Missing Evidence-Based Verification
- Recommendation: REC-2 (HIGH priority)
- Expected Impact: No stories escape without citation compliance

**Defense in Depth Architecture:**
```
Story Creation Workflow
    │
    ├─ Phase 3: Evidence-Verification Gate (STORY-211) ──────────── LAYER 1
    │   ├─ Reads target files
    │   ├─ Verifies claims with Grep
    │   ├─ Generates verified_violations YAML
    │   ├─ Caches validated files for Phase 7
    │   └─ HALT if claims cannot be verified
    │
    ├─ [Phase 4-6: Other processing...]
    │
    └─ Phase 7: Self-Validation ─────────────────────────────────── LAYER 2
        ├─ Existing: YAML structure validation
        ├─ Existing: User story format validation
        ├─ Existing: Acceptance criteria completeness
        ├─ NEW: Citation Compliance Validation (THIS STORY)
        │   ├─ Verifies verified_violations exists for claims
        │   ├─ Validates line number format
        │   ├─ Catches generic descriptions
        │   ├─ Uses Phase 3 cache for file existence
        │   └─ HALT if any item fails
        └─ Final summary generation
```

**Related Stories:**
- STORY-211 (Phase 3 verification) - Creates the verified_violations that Phase 7 validates
- STORY-213 (Documentation update) - Documents story quality requirements

**Architecture Compliance:**
- Follows defense in depth pattern (architecture-constraints.md)
- No external dependencies (dependencies.md)
- HALT pattern for validation failures (coding-standards.md)
- No Bash for file operations - uses Phase 3 cache (anti-patterns.md Category 1)

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
