---
id: STORY-343
title: Implement Memory Surfacing in TDD Phases
type: feature
epic: EPIC-052
sprint: Backlog
status: QA Approved
points: 6
depends_on: ["STORY-342"]
priority: High
assigned_to: Unassigned
created: 2026-01-30
format_version: "2.7"
---

# Story: Implement Memory Surfacing in TDD Phases

## Description

**As a** Framework Architect (Claude),
**I want** relevant patterns surfaced during TDD phases 02-03,
**so that** I can avoid repeating past mistakes and apply successful patterns to current implementation.

## Provenance

```xml
<provenance>
  <origin document="EPIC-052" section="Feature 4">
    <quote>"Combine session observations with long-term patterns to inform future TDD iterations with historical context."</quote>
    <line_reference>lines 361-424</line_reference>
    <quantified_impact>Fewer repeated friction points over time as patterns are surfaced proactively</quantified_impact>
  </origin>

  <decision rationale="phase-specific-surfacing">
    <selected>Surface TDD patterns in Phase 02, friction warnings in Phase 03</selected>
    <rejected alternative="surface-all-in-phase-01">
      Information overload at Phase 01 would reduce actionability
    </rejected>
    <trade_off>More targeted surfacing but requires reading patterns at multiple phases</trade_off>
  </decision>

  <stakeholder role="Framework Architect" goal="avoid-repeated-mistakes">
    <quote>"I want relevant patterns surfaced during TDD phases, so that I can avoid repeating mistakes."</quote>
    <source>EPIC-052, User Story 4</source>
  </stakeholder>

  <hypothesis id="H6" validation="friction-reduction" success_criteria="Fewer repeated friction points over time">
    Historical context improves TDD success - surfacing patterns prevents known issues
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: Phase 02 Reads TDD Patterns

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>Phase 02 (Test-First) begins for a story</given>
  <when>Phase startup completes</when>
  <then>TDD patterns from .claude/memory/learning/tdd-patterns.md are read</then>
  <verification>
    <source_files>
      <file hint="Phase 02 file">.claude/skills/devforgeai-development/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-343/test_ac1_phase02_reads_patterns.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Phase 02 Surfaces Relevant TDD Patterns

```xml
<acceptance_criteria id="AC2" implements="COMP-001">
  <given>TDD patterns are read and story characteristics are known</given>
  <when>Pattern matching is performed</when>
  <then>Relevant patterns (based on AC keywords, story type) are displayed to user</then>
  <verification>
    <source_files>
      <file hint="Phase 02 file">.claude/skills/devforgeai-development/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-343/test_ac2_phase02_surfaces_patterns.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Phase 03 Reads Friction Catalog

```xml
<acceptance_criteria id="AC3" implements="COMP-002">
  <given>Phase 03 (Implementation) begins for a story</given>
  <when>Phase startup completes</when>
  <then>Friction catalog from .claude/memory/learning/friction-catalog.md is read</then>
  <verification>
    <source_files>
      <file hint="Phase 03 file">.claude/skills/devforgeai-development/phases/phase-03-implementation.md</file>
    </source_files>
    <test_file>tests/STORY-343/test_ac3_phase03_reads_friction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Phase 03 Surfaces Friction Warnings

```xml
<acceptance_criteria id="AC4" implements="COMP-002">
  <given>Friction catalog is read and implementation type is known</given>
  <when>Friction matching is performed</when>
  <then>Relevant friction warnings are displayed with prevention steps</then>
  <verification>
    <source_files>
      <file hint="Phase 03 file">.claude/skills/devforgeai-development/phases/phase-03-implementation.md</file>
    </source_files>
    <test_file>tests/STORY-343/test_ac4_phase03_surfaces_friction.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Only Confident Patterns Surfaced

```xml
<acceptance_criteria id="AC5" implements="COMP-003">
  <given>Patterns exist with various confidence levels</given>
  <when>Patterns are surfaced</when>
  <then>Only patterns with confidence >= low (3+ occurrences) are displayed</then>
  <verification>
    <source_files>
      <file hint="Phase 02 file">.claude/skills/devforgeai-development/phases/phase-02-test-first.md</file>
      <file hint="Phase 03 file">.claude/skills/devforgeai-development/phases/phase-03-implementation.md</file>
    </source_files>
    <test_file>tests/STORY-343/test_ac5_confidence_filter.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Display Format Matches Specification

```xml
<acceptance_criteria id="AC6" implements="COMP-001,COMP-002">
  <given>Patterns are to be surfaced</given>
  <when>Display is rendered</when>
  <then>Display format matches EPIC-052 specification (Unicode box, pattern name, occurrences, recommendation)</then>
  <verification>
    <source_files>
      <file hint="Phase files">.claude/skills/devforgeai-development/phases/phase-02-test-first.md</file>
    </source_files>
    <test_file>tests/STORY-343/test_ac6_display_format.sh</test_file>
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
      name: "phase-02-test-first.md"
      file_path: ".claude/skills/devforgeai-development/phases/phase-02-test-first.md"
      required_keys:
        - key: "Memory Context Section"
          type: "section"
          required: true
          test_requirement: "Test: Grep for 'Memory Context' header"
        - key: "Read tdd-patterns.md"
          type: "instruction"
          required: true
          test_requirement: "Test: Grep for Read() of tdd-patterns.md"
        - key: "Pattern matching logic"
          type: "instruction"
          required: true
          test_requirement: "Test: Grep for pattern matching instructions"
        - key: "Display template"
          type: "code block"
          required: true
          test_requirement: "Test: Grep for 'Relevant TDD Patterns' display"

    - type: "Configuration"
      name: "phase-03-implementation.md"
      file_path: ".claude/skills/devforgeai-development/phases/phase-03-implementation.md"
      required_keys:
        - key: "Friction Awareness Section"
          type: "section"
          required: true
          test_requirement: "Test: Grep for 'Friction Awareness' header"
        - key: "Read friction-catalog.md"
          type: "instruction"
          required: true
          test_requirement: "Test: Grep for Read() of friction-catalog.md"
        - key: "Friction matching logic"
          type: "instruction"
          required: true
          test_requirement: "Test: Grep for friction matching instructions"
        - key: "Warning display template"
          type: "code block"
          required: true
          test_requirement: "Test: Grep for 'Friction Warning' display"

  business_rules:
    - id: "BR-001"
      rule: "Pattern matching uses AC keywords and story type"
      trigger: "Phase 02/03 startup"
      validation: "Keywords extracted from story, matched against pattern triggers"
      error_handling: "If no keywords match, skip surfacing (silent)"
      test_requirement: "Test: Verify keyword extraction and matching"
      priority: "Critical"
    - id: "BR-002"
      rule: "Only confident patterns (>= low) surfaced"
      trigger: "Pattern surfacing"
      validation: "Check confidence field != 'emerging'"
      error_handling: "Skip emerging patterns"
      test_requirement: "Test: Verify emerging patterns excluded"
      priority: "Critical"
    - id: "BR-003"
      rule: "Maximum 3 patterns surfaced per phase"
      trigger: "Pattern surfacing"
      validation: "Limit output to top 3 most relevant"
      error_handling: "Sort by relevance/occurrences, take top 3"
      test_requirement: "Test: Verify max 3 patterns shown"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Memory read minimal overhead"
      metric: "<50ms added to phase startup"
      test_requirement: "Test: Measure phase startup time delta"
      priority: "High"
    - id: "NFR-002"
      category: "Usability"
      requirement: "Pattern display is actionable"
      metric: "Each pattern includes specific recommendation"
      test_requirement: "Test: Verify recommendation present in output"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Memory Read Time:**
- Pattern file read adds <50ms to phase startup
- Matching algorithm completes in <20ms

### Usability

**Actionable Output:**
- Each surfaced pattern includes specific recommendation
- Display uses visual separation (Unicode box drawing)

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-342:** Create Long-Term Memory Layer
  - **Why:** Memory files must exist before surfacing can work
  - **Status:** Backlog

### External Dependencies

- [ ] **EPIC-051:** Framework Feedback Capture System
  - **Owner:** DevForgeAI Core
  - **ETA:** Feb 9, 2026
  - **Status:** In Progress
  - **Impact if delayed:** No patterns accumulated for surfacing

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for pattern matching and surfacing logic

**Test Scenarios:**
1. **Happy Path:**
   - Patterns exist and match story keywords
   - Display format rendered correctly
2. **Edge Cases:**
   - No patterns exist in memory
   - All patterns are "emerging" (none surfaced)
   - More than 3 matching patterns (top 3 shown)
   - Pattern keywords partially match
3. **Error Cases:**
   - Memory file doesn't exist (graceful skip)
   - Malformed pattern data

---

## Acceptance Criteria Verification Checklist

### AC#1: Phase 02 Reads TDD Patterns

- [x] "Memory Context" section added to phase-02-test-first.md - **Phase:** 3 - **Evidence:** Grep for header
- [x] Read() instruction for tdd-patterns.md - **Phase:** 3 - **Evidence:** Grep for Read pattern

### AC#2: Phase 02 Surfaces Relevant TDD Patterns

- [x] Pattern matching logic documented - **Phase:** 3 - **Evidence:** Logic inspection
- [x] Display template with "Relevant TDD Patterns" - **Phase:** 3 - **Evidence:** Grep for display

### AC#3: Phase 03 Reads Friction Catalog

- [x] "Friction Awareness" section added to phase-03-implementation.md - **Phase:** 3 - **Evidence:** Grep for header
- [x] Read() instruction for friction-catalog.md - **Phase:** 3 - **Evidence:** Grep for Read pattern

### AC#4: Phase 03 Surfaces Friction Warnings

- [x] Friction matching logic documented - **Phase:** 3 - **Evidence:** Logic inspection
- [x] Display template with "Friction Warning" - **Phase:** 3 - **Evidence:** Grep for display

### AC#5: Only Confident Patterns Surfaced

- [x] Confidence check in Phase 02 surfacing - **Phase:** 3 - **Evidence:** Logic inspection
- [x] Confidence check in Phase 03 surfacing - **Phase:** 3 - **Evidence:** Logic inspection

### AC#6: Display Format Matches Specification

- [x] Unicode box drawing characters (━) used - **Phase:** 3 - **Evidence:** Grep for ━
- [x] Pattern name displayed - **Phase:** 3 - **Evidence:** Template inspection
- [x] Occurrences displayed - **Phase:** 3 - **Evidence:** Template inspection
- [x] Recommendation displayed - **Phase:** 3 - **Evidence:** Template inspection

---

**Checklist Progress:** 14/14 items complete (100%)

---

## Definition of Done

### Implementation
- [x] phase-02-test-first.md modified with Memory Context section
- [x] phase-03-implementation.md modified with Friction Awareness section
- [x] Pattern matching logic implemented
- [x] Confidence filtering working
- [x] Display templates match specification

### Quality
- [x] All 6 acceptance criteria have passing tests
- [x] Edge cases covered (empty memory, all emerging)
- [x] Display format matches EPIC-052 specification

### Testing
- [x] Test for AC#1: Phase 02 reads patterns
- [x] Test for AC#2: Phase 02 surfaces patterns
- [x] Test for AC#3: Phase 03 reads friction
- [x] Test for AC#4: Phase 03 surfaces warnings
- [x] Test for AC#5: Confidence filtering
- [x] Test for AC#6: Display format

### Documentation
- [x] Phase files updated with surfacing logic
- [x] Changelog entries in modified files

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-03

- [x] phase-02-test-first.md modified with Memory Context section - Completed: Added Memory Context section with Read() for tdd-patterns.md, pattern matching logic, and display template
- [x] phase-03-implementation.md modified with Friction Awareness section - Completed: Added Friction Awareness section with Read() for friction-catalog.md, friction matching logic, and warning display template
- [x] Pattern matching logic implemented - Completed: FOR loop with keyword_match() function matching AC keywords/story type against pattern triggers
- [x] Confidence filtering working - Completed: Filters exclude "emerging" confidence and require >= 3 occurrences in both phase files
- [x] Display templates match specification - Completed: Unicode box drawing (━), pattern name, occurrences, recommendation displayed per EPIC-052
- [x] All 6 acceptance criteria have passing tests - Completed: 6 shell tests covering all ACs with 42 total assertions
- [x] Edge cases covered (empty memory, all emerging) - Completed: Surfacing logic handles empty files gracefully with IF checks
- [x] Display format matches EPIC-052 specification - Completed: Verified against EPIC-052 display templates (lines 396-416)
- [x] Test for AC#1-6: All tests passing - Completed: tests/STORY-343/*.sh with comprehensive assertions

### TDD Workflow Summary

**Phase 02 (Red):** 6 shell tests generated covering all acceptance criteria
**Phase 03 (Green):** Memory Context and Friction Awareness sections added to phase files
**Phase 04 (Refactor):** Code quality verified, patterns consistent across both phase files
**Phase 05 (Integration):** All 6 tests passing (100%), anti-gaming validation passed

### Files Modified

- `.claude/skills/devforgeai-development/phases/phase-02-test-first.md` - Memory Context section
- `.claude/skills/devforgeai-development/phases/phase-03-implementation.md` - Friction Awareness section

### Files Created

- `tests/STORY-343/test_ac1_phase02_reads_patterns.sh`
- `tests/STORY-343/test_ac2_phase02_surfaces_patterns.sh`
- `tests/STORY-343/test_ac3_phase03_reads_friction.sh`
- `tests/STORY-343/test_ac4_phase03_surfaces_friction.sh`
- `tests/STORY-343/test_ac5_confidence_filter.sh`
- `tests/STORY-343/test_ac6_display_format.sh`

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-30 14:30 | claude/create-story | Created | Story created for EPIC-052 Feature 4 | STORY-343.story.md |
| 2026-02-03 | claude/opus | DoD Update (Phase 07) | Development complete, all 6 ACs verified | phase-02-test-first.md, phase-03-implementation.md, tests/STORY-343/*.sh |
| 2026-02-03 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 0 violations, 3/3 validators | - |

## Notes

**Phase 02 Display Template (from EPIC-052):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Relevant TDD Patterns (from long-term memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Pattern: edge-case-gap (8 occurrences, medium confidence)
  → This story involves data validation
  → Recommendation: Add boundary tests explicitly
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Phase 03 Display Template (from EPIC-052):**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Friction Warning (from long-term memory)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Friction: type-mismatch-iteration (6 occurrences)
  → Stories with API responses often have type mismatches
  → Prevention: Verify AC return type before implementing
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Design Decisions:**
- TDD patterns in Phase 02 (before writing tests)
- Friction warnings in Phase 03 (before implementing)
- Maximum 3 patterns per phase to avoid overload

**References:**
- EPIC-052: Framework Feedback Display & Memory System (Feature 4, lines 361-424)
- STORY-342: Long-term memory layer (prerequisite)

---

Story Template Version: 2.7
Last Updated: 2026-01-30
