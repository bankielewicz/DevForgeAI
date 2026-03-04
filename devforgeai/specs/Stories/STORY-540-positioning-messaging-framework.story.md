---
id: STORY-540
title: Positioning & Messaging Framework
type: feature
epic: EPIC-075
sprint: Sprint-25
status: Ready for Dev
points: 3
depends_on: []
priority: High
advisory: false
source_gap: null
source_story: null
assigned_to: DevForgeAI AI Agent
created: 2026-03-03
format_version: "2.9"
---

# Story: Positioning & Messaging Framework

## Description

**As a** product marketer or founder using DevForgeAI,
**I want** a guided positioning workflow within the `marketing-business` skill that generates a positioning statement and audience-segmented key messages,
**so that** I have a structured, reusable marketing foundation document that communicates differentiated value to specific customer segments.

## Provenance

```xml
<provenance>
  <origin document="EPIC-075" section="Feature 2">
    <quote>"Add positioning workflow to marketing-business skill. Generate positioning statement using standard framework (category, differentiation, audience). Create 3-5 key messages for different audience segments."</quote>
    <line_reference>lines 50-54</line_reference>
    <quantified_impact>Creates consistent marketing messaging across 3-5 audience segments</quantified_impact>
  </origin>
  <stakeholder role="Solo Developer" goal="consistent-messaging">
    <quote>"I want help crafting positioning and messaging so that my marketing is consistent and compelling"</quote>
    <source>EPIC-075, User Stories</source>
  </stakeholder>
</provenance>
```

## Acceptance Criteria

### AC#1: Positioning Statement Generation

```xml
<acceptance_criteria id="AC1" implements="CFG-001">
  <given>The marketing-business skill is installed and the user invokes the positioning workflow command</given>
  <when>The workflow runs to completion with valid inputs for category, differentiation, and audience</when>
  <then>A positioning statement is generated following the standard framework: "For [target audience] who [need/problem], [product name] is a [category] that [key benefit/differentiation]. Unlike [alternative], [product name] [primary differentiator]." Written to devforgeai/specs/business/marketing/positioning.md under ## Positioning Statement</then>
  <verification>
    <source_files>
      <file hint="Positioning workflow reference">src/claude/skills/marketing-business/references/positioning-strategy.md</file>
    </source_files>
    <test_file>tests/STORY-540/test_ac1_positioning_statement.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#2: Key Messages Generation

```xml
<acceptance_criteria id="AC2" implements="CFG-002">
  <given>A valid positioning statement has been generated and at least 2 audience segments have been identified</given>
  <when>The key messages generation phase of the positioning workflow executes</when>
  <then>Between 3 and 5 key messages are produced, each mapped to a named audience segment. Each message is <= 50 words, written in plain language. Messages written under ## Key Messages with one subsection per segment (### Segment: [Name])</then>
  <verification>
    <source_files>
      <file hint="Positioning workflow reference">src/claude/skills/marketing-business/references/positioning-strategy.md</file>
    </source_files>
    <test_file>tests/STORY-540/test_ac2_key_messages.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#3: Output File Auto-Creation

```xml
<acceptance_criteria id="AC3" implements="CFG-003">
  <given>The positioning workflow has been invoked and devforgeai/specs/business/marketing/ does not yet exist</given>
  <when>The workflow attempts to write positioning.md to the output path</when>
  <then>The directory is created automatically. The file positioning.md is created with YAML frontmatter (story_id, generated_date, skill fields), ## Positioning Statement section, and ## Key Messages section. User receives confirmation with file path</then>
  <verification>
    <source_files>
      <file hint="Positioning workflow reference">src/claude/skills/marketing-business/references/positioning-strategy.md</file>
    </source_files>
    <test_file>tests/STORY-540/test_ac3_output_creation.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#4: Overwrite Existing Output

```xml
<acceptance_criteria id="AC4" implements="CFG-004">
  <given>positioning.md already exists from a prior run of the positioning workflow</given>
  <when>The positioning workflow is invoked again with updated inputs</when>
  <then>The existing positioning.md is overwritten (not appended) with newly generated content. User shown message indicating update with timestamp of previous and new version</then>
  <verification>
    <source_files>
      <file hint="Positioning workflow reference">src/claude/skills/marketing-business/references/positioning-strategy.md</file>
    </source_files>
    <test_file>tests/STORY-540/test_ac4_overwrite.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### AC#5: File Size Constraints

```xml
<acceptance_criteria id="AC5" implements="CFG-005">
  <given>The positioning workflow source file is implemented in the src/ tree</given>
  <when>The skill file size is measured</when>
  <then>The skill reference file is strictly under 1,000 lines. Any associated command file is strictly under 500 lines. Enforced by automated line-count test</then>
  <verification>
    <source_files>
      <file hint="Positioning workflow reference">src/claude/skills/marketing-business/references/positioning-strategy.md</file>
    </source_files>
    <test_file>tests/STORY-540/test_ac5_line_limits.py</test_file>
    <coverage_threshold>95</coverage_threshold>
  </verification>
</acceptance_criteria>
```

---

### Source Files Guidance

- `src/claude/skills/marketing-business/references/positioning-strategy.md` — Positioning workflow reference
- `devforgeai/specs/business/marketing/positioning.md` — Generated output file

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "positioning-strategy.md"
      file_path: "src/claude/skills/marketing-business/references/positioning-strategy.md"
      required_keys:
        - key: "positioning_framework"
          type: "object"
          example: "Category + Differentiation + Audience → Statement"
          required: true
          validation: "Framework produces statement with all 3 elements"
          test_requirement: "Test: Output contains category, differentiation, and audience elements"
        - key: "message_generator"
          type: "object"
          example: "Audience segments → Key messages (3-5)"
          required: true
          validation: "3-5 messages, each <= 50 words, mapped to named segments"
          test_requirement: "Test: Key messages count between 3-5 with word count enforcement"
        - key: "output_writer"
          type: "object"
          example: "Write to positioning.md with frontmatter"
          required: true
          validation: "File created with YAML frontmatter and required sections"
          test_requirement: "Test: Output file exists with correct structure after workflow"

  business_rules:
    - id: "BR-001"
      rule: "Positioning statement must follow standard 3-element framework (category, differentiation, audience)"
      trigger: "When positioning generation phase completes"
      validation: "Statement contains all 3 framework elements"
      error_handling: "If any element missing, prompt user for missing input"
      test_requirement: "Test: Statement structure matches framework template"
      priority: "Critical"

    - id: "BR-002"
      rule: "Key messages count must be between 3 and 5, each <= 50 words"
      trigger: "When message generation phase completes"
      validation: "Count messages, validate word count per message"
      error_handling: "Truncate messages exceeding 50 words with warning"
      test_requirement: "Test: Message count in range, word counts enforced"
      priority: "Critical"

    - id: "BR-003"
      rule: "Empty audience input blocks workflow with validation error"
      trigger: "When audience field is empty or whitespace-only"
      validation: "Non-empty string after trimming"
      error_handling: "Display validation error, no partial output written"
      test_requirement: "Test: Empty audience produces error, no output file"
      priority: "High"

    - id: "BR-004"
      rule: "More than 5 audience segments truncated to first 5 alphabetically"
      trigger: "When user provides > 5 segments"
      validation: "Segment count <= 5"
      error_handling: "Truncate, notify user of omitted segments"
      test_requirement: "Test: 7 segments input produces 5 messages with truncation notice"
      priority: "Medium"

    - id: "BR-005"
      rule: "Duplicate segment names (case-insensitive) are deduplicated"
      trigger: "When segments contain case-variant duplicates"
      validation: "Case-insensitive uniqueness check"
      error_handling: "Retain first occurrence, notify user"
      test_requirement: "Test: Enterprise and enterprise deduplicated to single segment"
      priority: "Medium"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Positioning statement generation completes within 10 seconds"
      metric: "< 10s on standard developer workstation"
      test_requirement: "Test: Workflow completes within timeout"
      priority: "Medium"

    - id: "NFR-002"
      category: "Reliability"
      requirement: "Idempotent output for identical inputs"
      metric: "Byte-for-byte identical output (excluding timestamp)"
      test_requirement: "Test: Two runs with same input produce identical content"
      priority: "Medium"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "No partial files on failure"
      metric: "Partial file deleted before error shown"
      test_requirement: "Test: Simulated mid-write failure leaves no file"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - id: TL-001
    component: "Positioning Framework"
    limitation: "Template-based positioning, not validated against actual market data"
    decision: "workaround:Label output as framework-generated requiring market validation"
    discovered_phase: "Architecture"
    impact: "Users must validate positioning against real customer feedback"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- Positioning generation: < 10 seconds (p95)
- File write: < 500ms
- Total workflow: < 30 seconds including prompts

---

### Security

**Authentication:**
- None required (local CLI tool)

**Data Protection:**
- No PII, credentials, or API keys in output files
- No external service calls

**Security Testing:**
- [ ] No hardcoded secrets
- [ ] No path traversal
- [ ] Read-only access to context files

---

### Scalability

**Extensibility:**
- Positioning framework customizable via reference file
- Segment limit enforced at 5 for tractability

---

### Reliability

**Error Handling:**
- Empty input validation with clear error messages
- Partial file cleanup on failure
- Idempotent output for identical inputs

---

### Observability

**Logging:**
- Terminal output for each workflow phase
- Warning messages for edge cases (truncation, deduplication)
- Confirmation with file path on success

---

## Dependencies

### Prerequisite Stories

- None — this story has no build dependencies.

### Downstream Consumers

- **STORY-541:** /marketing-plan Command & Skill Assembly
  - **Relationship:** STORY-541 assembles the marketing-business skill that invokes this positioning workflow
  - **Status:** Not Started

### External Dependencies

- None

### Technology Dependencies

- None (pure Markdown skill)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**
1. **Happy Path:** Valid inputs → positioning statement + 3-5 key messages
2. **Edge Cases:**
   - Empty audience input → validation error
   - Single-word differentiation → warning
   - 7 segments → truncation to 5
   - Duplicate segments → deduplication
   - Existing output file → overwrite
3. **Error Cases:**
   - Missing directory → auto-creation
   - File write failure → error message

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**
1. **End-to-End Workflow:** Complete positioning workflow produces valid output
2. **Output Structure:** File contains required sections and frontmatter

---

## Acceptance Criteria Verification Checklist

### AC#1: Positioning Statement Generation

- [ ] Statement follows 3-element framework - **Phase:** 2 - **Evidence:** tests/STORY-540/test_ac1_positioning_statement.py
- [ ] Written to correct section in output file - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac1_positioning_statement.py

### AC#2: Key Messages Generation

- [ ] 3-5 messages generated - **Phase:** 2 - **Evidence:** tests/STORY-540/test_ac2_key_messages.py
- [ ] Each <= 50 words - **Phase:** 2 - **Evidence:** tests/STORY-540/test_ac2_key_messages.py
- [ ] Mapped to named segments - **Phase:** 2 - **Evidence:** tests/STORY-540/test_ac2_key_messages.py

### AC#3: Output File Auto-Creation

- [ ] Directory auto-created - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac3_output_creation.py
- [ ] YAML frontmatter present - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac3_output_creation.py

### AC#4: Overwrite Existing Output

- [ ] Overwrite replaces content - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac4_overwrite.py
- [ ] Timestamp shown to user - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac4_overwrite.py

### AC#5: File Size Constraints

- [ ] Skill file < 1,000 lines - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac5_line_limits.py
- [ ] Command file < 500 lines - **Phase:** 3 - **Evidence:** tests/STORY-540/test_ac5_line_limits.py

---

**Checklist Progress:** 0/11 items complete (0%)

---

<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: .claude/skills/implementing-stories/references/dod-update-workflow.md for complete details
-->

## Implementation Notes

*To be filled during development*

## Definition of Done

### Implementation
- [ ] Positioning strategy reference file created in src/ tree
- [ ] 3-element positioning framework (category, differentiation, audience)
- [ ] Key message generator for 3-5 audience segments
- [ ] Output writer for devforgeai/specs/business/marketing/positioning.md
- [ ] Edge case handlers (empty input, truncation, deduplication, overwrite)

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Edge cases covered (empty audience, single-word differentiation, 7 segments, duplicates, existing file)
- [ ] Skill file under 1,000 lines
- [ ] Code coverage >95% for workflow logic

### Testing
- [ ] Unit tests for positioning statement generation
- [ ] Unit tests for key message generation
- [ ] Unit tests for edge case handling
- [ ] Integration tests for end-to-end workflow
- [ ] Integration tests for output file structure

### Documentation
- [ ] Positioning strategy reference file documented
- [ ] Story file updated with implementation notes

---

### TDD Workflow Summary

| Phase | Status | Details |
|-------|--------|---------|

### Files Created/Modified

| File | Action | Lines |
|------|--------|-------|

---

## Change Log

**Current Status:** Ready for Dev

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-03-03 12:00 | .claude/story-requirements-analyst | Created | Story created from EPIC-075 Feature 2 | STORY-540.story.md |

## Notes

**Design Decisions:**
- Positioning framework uses standard "For [audience] who [need], [product] is a [category]..." template
- Key messages capped at 5 segments for tractability
- Case-insensitive deduplication of segment names

**Open Questions:**
- None

**Related ADRs:**
- None

**References:**
- EPIC-075: Marketing & Customer Acquisition
- BRAINSTORM-011: Business Skills Framework

---

Story Template Version: 2.9
Last Updated: 2026-03-03
