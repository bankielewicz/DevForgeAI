---
id: STORY-342
title: Create Long-Term Memory Layer
type: feature
epic: EPIC-052
sprint: Backlog
status: QA Approved
points: 12
depends_on: ["STORY-339", "STORY-341"]
priority: High
assigned_to: Unassigned
created: 2026-01-30
format_version: "2.7"
---

# Story: Create Long-Term Memory Layer

## Description

**As a** Framework Architect (Claude),
**I want** long-term memory files that accumulate patterns across multiple story completions,
**so that** I can learn from past stories and apply historical context to future TDD iterations.

## Provenance

```xml
<provenance>
  <origin document="EPIC-052" section="Feature 3">
    <quote>"Create cross-story pattern learning files that accumulate insights across multiple story completions."</quote>
    <line_reference>lines 240-358</line_reference>
    <quantified_impact>Cross-story patterns detected and surfaced (3+ occurrence threshold)</quantified_impact>
  </origin>

  <decision rationale="multi-file-separation">
    <selected>Three separate files: tdd-patterns.md, friction-catalog.md, success-patterns.md</selected>
    <rejected alternative="single-patterns-file">
      Single file would become large and harder to parse by category
    </rejected>
    <trade_off>More files to maintain but better organization and faster access</trade_off>
  </decision>

  <stakeholder role="Framework Architect" goal="learn-from-history">
    <quote>"I want long-term memory files to accumulate patterns, so that I can learn from past stories."</quote>
    <source>EPIC-052, User Story 3</source>
  </stakeholder>

  <hypothesis id="H5" validation="pattern-detection" success_criteria="Cross-story patterns detected (3+ occurrences)">
    Multi-layer memory enables learning - long-term layer captures cross-story patterns
  </hypothesis>
</provenance>
```

---

## Acceptance Criteria

### AC#1: ADR Created for Source Tree Update

```xml
<acceptance_criteria id="AC1" implements="COMP-001">
  <given>STORY-339 has completed with ADR approval</given>
  <when>Long-term memory files are created</when>
  <then>Files are placed in .claude/memory/learning/ directory per approved ADR</then>
  <verification>
    <source_files>
      <file hint="ADR document">devforgeai/specs/adrs/ADR-013-memory-directory-structure.md</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac1_adr_prerequisite.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#2: tdd-patterns.md Created

```xml
<acceptance_criteria id="AC2" implements="COMP-002">
  <given>Learning directory exists per ADR</given>
  <when>Story implementation completes</when>
  <then>tdd-patterns.md exists with schema matching EPIC-052 specification</then>
  <verification>
    <source_files>
      <file hint="TDD patterns file">.claude/memory/learning/tdd-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac2_tdd_patterns.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#3: friction-catalog.md Created

```xml
<acceptance_criteria id="AC3" implements="COMP-003">
  <given>Learning directory exists per ADR</given>
  <when>Story implementation completes</when>
  <then>friction-catalog.md exists with schema matching EPIC-052 specification</then>
  <verification>
    <source_files>
      <file hint="Friction catalog file">.claude/memory/learning/friction-catalog.md</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac3_friction_catalog.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#4: success-patterns.md Created

```xml
<acceptance_criteria id="AC4" implements="COMP-004">
  <given>Learning directory exists per ADR</given>
  <when>Story implementation completes</when>
  <then>success-patterns.md exists with schema matching EPIC-052 specification</then>
  <verification>
    <source_files>
      <file hint="Success patterns file">.claude/memory/learning/success-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac4_success_patterns.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#5: Pattern Detection Algorithm Implemented

```xml
<acceptance_criteria id="AC5" implements="COMP-005">
  <given>Session memory contains observations from completed story</given>
  <when>Story reaches QA Approved status</when>
  <then>Pattern detection algorithm extracts and aggregates patterns to long-term memory</then>
  <verification>
    <source_files>
      <file hint="Pattern detection hook">.claude/hooks/post-qa-memory-update.sh</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac5_pattern_detection.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#6: Emerging Patterns Not Surfaced

```xml
<acceptance_criteria id="AC6" implements="COMP-005">
  <given>A pattern has fewer than 3 occurrences</given>
  <when>Pattern files are read by TDD phases</when>
  <then>Pattern is marked as "emerging" and not surfaced to user</then>
  <verification>
    <source_files>
      <file hint="Pattern files">.claude/memory/learning/tdd-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac6_emerging_patterns.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

### AC#7: Confidence Levels Calculated

```xml
<acceptance_criteria id="AC7" implements="COMP-005">
  <given>A pattern exists in long-term memory</given>
  <when>Occurrences are updated</when>
  <then>Confidence level calculated: >=10 = high, >=5 = medium, >=3 = low, <3 = emerging</then>
  <verification>
    <source_files>
      <file hint="Pattern files">.claude/memory/learning/tdd-patterns.md</file>
    </source_files>
    <test_file>tests/STORY-342/test_ac7_confidence_levels.sh</test_file>
  </verification>
</acceptance_criteria>
```

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "DataModel"
      name: "TDD Patterns"
      table: "N/A (Markdown file)"
      purpose: "Cross-story TDD pattern learning"
      fields:
        - name: "pattern_id"
          type: "String"
          constraints: "Required, unique"
          description: "Pattern identifier (hash of category + keywords)"
          test_requirement: "Test: Validate unique pattern IDs"
        - name: "occurrences"
          type: "Integer"
          constraints: "Required, >= 1"
          description: "Number of times pattern observed"
          test_requirement: "Test: Validate occurrence count increments"
        - name: "confidence"
          type: "Enum"
          constraints: "Required, emerging|low|medium|high"
          description: "Confidence level based on occurrences"
          test_requirement: "Test: Validate confidence calculation"
        - name: "last_seen"
          type: "String"
          constraints: "Required, STORY-NNN format"
          description: "Last story where pattern observed"
          test_requirement: "Test: Validate last_seen update"
        - name: "examples"
          type: "Array<String>"
          constraints: "Max 5 items"
          description: "Story IDs showing this pattern"
          test_requirement: "Test: Validate max 5 examples"

    - type: "DataModel"
      name: "Friction Catalog"
      table: "N/A (Markdown file)"
      purpose: "Cross-story friction point tracking"
      fields:
        - name: "friction_id"
          type: "String"
          constraints: "Required, unique"
          description: "Friction identifier"
          test_requirement: "Test: Validate unique friction IDs"
        - name: "avg_resolution_time"
          type: "String"
          constraints: "Optional"
          description: "Average time to resolve this friction"
          test_requirement: "Test: Validate time format"
        - name: "root_cause"
          type: "String"
          constraints: "Required"
          description: "Why this friction occurs"
          test_requirement: "Test: Validate root cause present"
        - name: "solution"
          type: "Array<String>"
          constraints: "Required, 1-5 items"
          description: "Steps to prevent or resolve"
          test_requirement: "Test: Validate solution steps"

    - type: "Configuration"
      name: "post-qa-memory-update.sh"
      file_path: ".claude/hooks/post-qa-memory-update.sh"
      required_keys:
        - key: "Pattern Detection"
          type: "function"
          required: true
          test_requirement: "Test: Hook executes pattern detection"
        - key: "Long-Term Memory Update"
          type: "function"
          required: true
          test_requirement: "Test: Hook updates memory files"

  business_rules:
    - id: "BR-001"
      rule: "Patterns with <3 occurrences are 'emerging' and not surfaced"
      trigger: "Pattern file read for surfacing"
      validation: "Check confidence != 'emerging' before surfacing"
      error_handling: "Skip emerging patterns silently"
      test_requirement: "Test: Verify emerging patterns excluded from surfacing"
      priority: "Critical"
    - id: "BR-002"
      rule: "Confidence levels calculated per threshold"
      trigger: "Pattern occurrence update"
      validation: ">=10 = high, >=5 = medium, >=3 = low, <3 = emerging"
      error_handling: "Default to 'emerging' if count invalid"
      test_requirement: "Test: Verify each confidence threshold"
      priority: "Critical"
    - id: "BR-003"
      rule: "Maximum 5 example stories per pattern"
      trigger: "New story added to pattern examples"
      validation: "examples.length <= 5"
      error_handling: "Remove oldest example, add newest"
      test_requirement: "Test: Verify example rotation at max"
      priority: "Medium"
    - id: "BR-004"
      rule: "Similar patterns (>70% keyword overlap) merged"
      trigger: "New pattern detection"
      validation: "Calculate keyword overlap with existing patterns"
      error_handling: "Merge into existing if >70% overlap"
      test_requirement: "Test: Verify pattern merging"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Storage"
      requirement: "Long-term memory file size capped"
      metric: "50-100KB total for all 3 files"
      test_requirement: "Test: Verify total size under 100KB"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Pattern aggregation time"
      metric: "Pattern detection completes in <500ms"
      test_requirement: "Test: Measure pattern detection time"
      priority: "Medium"
```

---

## Technical Limitations

```yaml
technical_limitations: []
```

---

## Non-Functional Requirements (NFRs)

### Storage

**File Size Limits:**
- tdd-patterns.md: ~30-40KB max
- friction-catalog.md: ~30-40KB max
- success-patterns.md: ~30-40KB max
- Total: 50-100KB capped

**Pruning Strategy:**
- Remove patterns not seen in 30+ stories
- Archive old patterns to learning/archive/

### Performance

**Pattern Detection:**
- Pattern aggregation completes in <500ms
- Runs synchronously after story QA approval

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-339:** Create ADR for Source Tree Memory Directories
  - **Why:** ADR must approve .claude/memory/learning/ directory
  - **Status:** Backlog

- [ ] **STORY-341:** Create Session Memory Layer
  - **Why:** Session memory provides observations to aggregate
  - **Status:** Backlog

### External Dependencies

- [ ] **EPIC-051:** Framework Feedback Capture System
  - **Owner:** DevForgeAI Core
  - **ETA:** Feb 9, 2026
  - **Status:** In Progress
  - **Impact if delayed:** No observations to aggregate into patterns

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for pattern detection and aggregation

**Test Scenarios:**
1. **Happy Path:**
   - First pattern created (occurrences = 1)
   - Existing pattern incremented
   - Confidence level transitions correctly
2. **Edge Cases:**
   - Pattern with exactly 3 occurrences (low threshold)
   - Pattern with exactly 10 occurrences (high threshold)
   - Maximum examples (5) rotation
   - 70% keyword overlap detection
3. **Error Cases:**
   - Empty session memory
   - Malformed observation data
   - File write permission denied

---

## Acceptance Criteria Verification Checklist

### AC#1: ADR Created for Source Tree Update

- [ ] STORY-339 completed - **Phase:** 1 - **Evidence:** Story status check
- [ ] ADR-013 status is "Accepted" - **Phase:** 1 - **Evidence:** ADR file check

### AC#2: tdd-patterns.md Created

- [ ] File exists at .claude/memory/learning/tdd-patterns.md - **Phase:** 3 - **Evidence:** File existence
- [ ] YAML frontmatter valid - **Phase:** 3 - **Evidence:** Schema validation
- [ ] Pattern schema matches spec - **Phase:** 3 - **Evidence:** Schema validation

### AC#3: friction-catalog.md Created

- [ ] File exists at .claude/memory/learning/friction-catalog.md - **Phase:** 3 - **Evidence:** File existence
- [ ] YAML frontmatter valid - **Phase:** 3 - **Evidence:** Schema validation
- [ ] Friction schema matches spec - **Phase:** 3 - **Evidence:** Schema validation

### AC#4: success-patterns.md Created

- [ ] File exists at .claude/memory/learning/success-patterns.md - **Phase:** 3 - **Evidence:** File existence
- [ ] YAML frontmatter valid - **Phase:** 3 - **Evidence:** Schema validation
- [ ] Success schema matches spec - **Phase:** 3 - **Evidence:** Schema validation

### AC#5: Pattern Detection Algorithm Implemented

- [ ] Hook file exists at .claude/hooks/post-qa-memory-update.sh - **Phase:** 3 - **Evidence:** File existence
- [ ] Hook reads session memory - **Phase:** 3 - **Evidence:** Grep for Read pattern
- [ ] Hook updates long-term memory - **Phase:** 3 - **Evidence:** Grep for Edit pattern

### AC#6: Emerging Patterns Not Surfaced

- [ ] Confidence field present in pattern schema - **Phase:** 3 - **Evidence:** Schema check
- [ ] Emerging check in surfacing logic - **Phase:** 5 - **Evidence:** Logic inspection

### AC#7: Confidence Levels Calculated

- [ ] High threshold (>=10) implemented - **Phase:** 3 - **Evidence:** Logic inspection
- [ ] Medium threshold (>=5) implemented - **Phase:** 3 - **Evidence:** Logic inspection
- [ ] Low threshold (>=3) implemented - **Phase:** 3 - **Evidence:** Logic inspection
- [ ] Emerging threshold (<3) implemented - **Phase:** 3 - **Evidence:** Logic inspection

---

**Checklist Progress:** 0/18 items complete (0%)

---

## Definition of Done

### Implementation
- [x] tdd-patterns.md created with schema
- [x] friction-catalog.md created with schema
- [x] success-patterns.md created with schema
- [x] Pattern detection algorithm implemented
- [x] post-qa-memory-update.sh hook created
- [x] Confidence level calculation working
- [x] Pattern merging (70% overlap) working

### Quality
- [x] All 7 acceptance criteria have passing tests
- [x] Edge cases covered (thresholds, max examples)
- [x] Schemas match EPIC-052 specification exactly

### Testing
- [x] Test for AC#1: ADR prerequisite
- [x] Test for AC#2: tdd-patterns.md
- [x] Test for AC#3: friction-catalog.md
- [x] Test for AC#4: success-patterns.md
- [x] Test for AC#5: Pattern detection
- [x] Test for AC#6: Emerging patterns
- [x] Test for AC#7: Confidence levels

### Documentation
- [x] Pattern schemas documented
- [x] Hook registered in hooks.yaml

## Implementation Notes

- [x] tdd-patterns.md created with schema - Completed: 2026-02-02
- [x] friction-catalog.md created with schema - Completed: 2026-02-02
- [x] success-patterns.md created with schema - Completed: 2026-02-02
- [x] Pattern detection algorithm implemented - Completed: 2026-02-02
- [x] post-qa-memory-update.sh hook created - Completed: 2026-02-02
- [x] Confidence level calculation working - Completed: 2026-02-02
- [x] Pattern merging (70% overlap) working - Completed: 2026-02-02
- [x] All 7 acceptance criteria have passing tests - Completed: 2026-02-02
- [x] Edge cases covered (thresholds, max examples) - Completed: 2026-02-02
- [x] Schemas match EPIC-052 specification exactly - Completed: 2026-02-02
- [x] Test for AC#1: ADR prerequisite - Completed: 2026-02-02
- [x] Test for AC#2: tdd-patterns.md - Completed: 2026-02-02
- [x] Test for AC#3: friction-catalog.md - Completed: 2026-02-02
- [x] Test for AC#4: success-patterns.md - Completed: 2026-02-02
- [x] Test for AC#5: Pattern detection - Completed: 2026-02-02
- [x] Test for AC#6: Emerging patterns - Completed: 2026-02-02
- [x] Test for AC#7: Confidence levels - Completed: 2026-02-02
- [x] Pattern schemas documented - Completed: 2026-02-02
- [x] Hook registered in hooks.yaml - Completed: 2026-02-02

**Developer:** DevForgeAI AI Agent
**Implemented:** 2026-02-02

---

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-30 14:30 | claude/create-story | Created | Story created for EPIC-052 Feature 3 | STORY-342.story.md |
| 2026-02-02 12:15 | claude/qa-result-interpreter | QA Deep | PASSED: Coverage 100%, 4 LOW violations | STORY-342-qa-report.md |

## Notes

**tdd-patterns.md Schema (from EPIC-052):**
```markdown
---
last_updated: 2026-01-26T12:00:00Z
total_patterns: 15
version: 1.0
---

# TDD Patterns Learned

## Pattern: clean-tdd-cycle
**Occurrences:** 12
**Confidence:** high (>10 occurrences)
**Last Seen:** STORY-320

**Description:** TDD cycle completes with single iteration per phase

**When to Apply:**
- Story has clear, unambiguous AC
- No external dependencies
- Well-defined input/output contracts

**Examples:**
- STORY-305: Completed all phases in single iteration
- STORY-310: Zero reflections captured (no failures)
```

**Pattern Detection Algorithm (from EPIC-052):**
```
ON story_completion:
  1. Read session memory observations
  2. FOR each observation:
     a. Extract category + note keywords
     b. Hash to pattern_id (category + keyword_hash)
     c. IF pattern_id exists in long-term memory:
        - Increment occurrences
        - Update last_seen
        - Add story to examples (max 5)
     d. ELSE IF similar pattern exists (>70% keyword overlap):
        - Merge into existing pattern
        - Increment occurrences
     e. ELSE:
        - Create new pattern entry
        - Set occurrences = 1
        - Set confidence = emerging
```

**Design Decisions:**
- Three separate files for category separation
- 70% keyword overlap for pattern merging
- Maximum 5 examples per pattern to limit file size

**References:**
- EPIC-052: Framework Feedback Display & Memory System (Feature 3, lines 240-358)
- STORY-339: ADR for memory directories (prerequisite)
- STORY-341: Session memory layer (prerequisite)

---

Story Template Version: 2.7
Last Updated: 2026-01-30
