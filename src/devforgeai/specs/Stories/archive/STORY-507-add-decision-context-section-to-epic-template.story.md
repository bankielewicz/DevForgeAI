---
id: STORY-507
title: Add "Decision Context" Section to Epic Template
type: feature
epic: N/A
sprint: Sprint-21
status: QA Approved ✅
points: 2
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: Unassigned
created: 2026-02-27
format_version: "2.9"
---

# Story: Add "Decision Context" Section to Epic Template

## Description

**As a** DevForgeAI framework user,
**I want** a "Decision Context" section in the epic template that captures design rationale, rejected alternatives, adversary model, implementation constraints, and key discovery insights,
**so that** fresh Claude sessions creating stories from epics have all the context needed without re-deriving design decisions.

**Source:** RCA-042 REC-1 (Epic Context Loss During Skill-Chain Handoff)
**Root Cause:** 4th occurrence of cross-session context loss (RCA-030, RCA-031, RCA-035, RCA-042)

## Provenance

```xml
<provenance>
  <origin document="RCA-042" section="REC-1">
    <quote>"The DevForgeAI skill-chain handoff protocol treats conversation context as ephemeral and only transfers structured artifacts. There is no Decision Context preservation mechanism."</quote>
    <line_reference>lines 97-135</line_reference>
    <quantified_impact>4th occurrence of same root cause class across RCA-030, RCA-031, RCA-035, RCA-042</quantified_impact>
  </origin>
  <decision rationale="template-section-addition">
    <selected>Add mandatory 13th section to constitutional epic template</selected>
    <rejected alternative="Post-processing enrichment">Would not enforce context capture at creation time</rejected>
    <trade_off>Slightly larger template, but prevents context loss at source</trade_off>
  </decision>
</provenance>
```

## Acceptance Criteria

### AC#1: Decision Context Section Added to Epic Template

```xml
<acceptance_criteria id="AC1">
  <given>The constitutional epic template at .claude/skills/designing-systems/assets/templates/epic-template.md</given>
  <when>The template is read</when>
  <then>A "## Decision Context" section exists with subsections: "### Design Rationale", "### Rejected Alternatives", "### Adversary/Threat Model", "### Implementation Constraints", "### Key Insights from Discovery"</then>
  <verification>
    <source_files>
      <file hint="Epic template">.claude/skills/designing-systems/assets/templates/epic-template.md</file>
    </source_files>
    <test_file>tests/STORY-507/test_ac1_decision_context_section.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#2: Section Placement is Correct

```xml
<acceptance_criteria id="AC2">
  <given>The updated epic template</given>
  <when>The section order is inspected</when>
  <then>"## Decision Context" appears after "## Technical Considerations" and before "## Dependencies"</then>
  <verification>
    <source_files>
      <file hint="Epic template">.claude/skills/designing-systems/assets/templates/epic-template.md</file>
    </source_files>
    <test_file>tests/STORY-507/test_ac2_section_placement.sh</test_file>
  </verification>
</acceptance_criteria>
```

### AC#3: Subsections Have Descriptive Placeholders

```xml
<acceptance_criteria id="AC3">
  <given>The Decision Context section in the template</given>
  <when>Each subsection is inspected</when>
  <then>Each subsection contains bracketed placeholder text explaining what content should go there (e.g., "[WHY were the key technical decisions made?]")</then>
  <verification>
    <source_files>
      <file hint="Epic template">.claude/skills/designing-systems/assets/templates/epic-template.md</file>
    </source_files>
    <test_file>tests/STORY-507/test_ac3_placeholders.sh</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "epic-template.md"
      file_path: ".claude/skills/designing-systems/assets/templates/epic-template.md"
      required_keys:
        - key: "Decision Context section"
          type: "markdown"
          required: true
          test_requirement: "Test: Verify ## Decision Context section exists with 5 subsections"
```

## Technical Limitations

```yaml
technical_limitations: []
```

## Non-Functional Requirements (NFRs)

### Performance
N/A - Template file, no runtime performance impact.

### Security
N/A - No security-sensitive changes.

### Scalability
N/A

### Reliability
N/A

### Observability
N/A

## Dependencies

### Prerequisite Stories
None.

### External Dependencies
None.

### Technology Dependencies
None.

## Test Strategy

### Unit Tests
**Coverage Target:** N/A (template file, tested via grep/content verification)

**Test Scenarios:**
1. **Happy Path:** Template contains Decision Context section with all 5 subsections
2. **Section Order:** Decision Context appears between Technical Considerations and Dependencies
3. **Placeholder Content:** Each subsection has descriptive placeholder text

### Integration Tests
N/A

## Acceptance Criteria Verification Checklist

### AC#1: Decision Context Section Added
- [x] Section header "## Decision Context" present - **Phase:** 3 - **Evidence:** grep verification
- [x] 5 subsections present (Design Rationale, Rejected Alternatives, Adversary/Threat Model, Implementation Constraints, Key Insights from Discovery) - **Phase:** 3 - **Evidence:** grep verification

### AC#2: Section Placement
- [x] Section appears after Technical Considerations - **Phase:** 3 - **Evidence:** line number comparison
- [x] Section appears before Dependencies - **Phase:** 3 - **Evidence:** line number comparison

### AC#3: Placeholders
- [x] Each subsection has bracketed placeholder text - **Phase:** 3 - **Evidence:** grep for bracket patterns

---

**Checklist Progress:** 5/5 items complete (100%)

## Definition of Done

### Implementation
- [x] Decision Context section added to epic template
- [x] Section placed between Technical Considerations and Dependencies
- [x] All 5 subsections have descriptive placeholder text
- [x] Template still valid markdown

### Quality
- [x] All 3 acceptance criteria have passing tests
- [x] No existing epic template sections disrupted

### Testing
- [x] Content verification tests for section presence
- [x] Section order verification tests

### Documentation
- [x] RCA-042 updated with STORY-507 link

## Implementation Notes

- [x] Decision Context section added to epic template - Completed: Added ## Decision Context with 5 subsections to src/claude/skills/designing-systems/assets/templates/epic-template.md
- [x] Section placed between Technical Considerations and Dependencies - Completed: Inserted at line 132, after Technical Considerations (line 109) and before Dependencies (line 154)
- [x] All 5 subsections have descriptive placeholder text - Completed: Each subsection has bracketed [WHY/WHAT...] guidance text
- [x] Template still valid markdown - Completed: All original sections preserved, valid structure verified
- [x] All 3 acceptance criteria have passing tests - Completed: 16/16 tests passing across 3 test files
- [x] No existing epic template sections disrupted - Completed: Integration test verified all 14 sections present
- [x] Content verification tests for section presence - Completed: test_ac1_decision_context_section.sh (6 tests)
- [x] Section order verification tests - Completed: test_ac2_section_placement.sh (5 tests)
- [x] RCA-042 updated with STORY-507 link - Completed: Updated RCA-042 implementation checklist line 317, marked REC-1 as implemented

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-28

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|
| 01 Pre-Flight | ✅ Complete | Git validated, 6 context files loaded, tech stack confirmed |
| 02 Red | ✅ Complete | 16 failing tests across 3 test files |
| 03 Green | ✅ Complete | Decision Context section added, all 16 tests passing |
| 04 Refactor | ✅ Complete | Code review approved, no refactoring needed |
| 4.5 AC Verify | ✅ Complete | 3/3 ACs PASS |
| 05 Integration | ✅ Complete | All original sections preserved, template valid |
| 5.5 AC Verify | ✅ Complete | Final verification 3/3 ACs PASS |

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|
| src/claude/skills/designing-systems/assets/templates/epic-template.md | Modified | +22 lines (Decision Context section) |
| tests/STORY-507/test_ac1_decision_context_section.sh | Created | 62 lines |
| tests/STORY-507/test_ac2_section_placement.sh | Created | 84 lines |
| tests/STORY-507/test_ac3_placeholders.sh | Created | 71 lines |
| tests/STORY-507/run_all_tests.sh | Created | 31 lines |
| tests/STORY-507/integration_results.txt | Created | Integration results |

---

## Change Log

**Current Status:** Dev Complete

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-27 | /create-stories-from-rca | Created | Story created from RCA-042 REC-1 | STORY-507.story.md |

## Notes

**Source RCA:** RCA-042 (Epic Context Loss During Skill-Chain Handoff)
**Source Recommendation:** REC-1: Add "Decision Context" Section to Epic Template

**Design Decisions:**
- Section placed between Technical Considerations and Dependencies per RCA-042 recommendation
- 5 subsections chosen to cover: rationale, alternatives, threats, constraints, insights

---

Story Template Version: 2.9
Last Updated: 2026-02-27
