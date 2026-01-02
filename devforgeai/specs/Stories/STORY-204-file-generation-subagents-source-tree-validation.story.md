---
id: STORY-204
title: Update ALL File-Generation Subagents with source-tree.md Validation
type: enhancement
epic: EPIC-033-framework-enhancement-triage-q4-2025
sprint: Backlog
status: Backlog
points: 3
depends_on: ["STORY-203"]
priority: High
assigned_to: Unassigned
created: 2026-01-01
source_rca: RCA-017
source_recommendation: REC-2
format_version: "2.5"
---

# Story: Update ALL File-Generation Subagents with source-tree.md Validation

## Description

**As a** DevForgeAI framework maintainer,
**I want** ALL subagents that have Write/Edit tools to validate output paths against source-tree.md,
**so that** the source-tree.md constraint violation pattern cannot recur in any file-generation subagent.

**Context from RCA-017:**
The test-automator violation (REC-1) could occur with any subagent that writes files. Multiple subagents have Write/Edit tools but lack source-tree.md validation:
- test-automator (addressed by STORY-203)
- story-requirements-analyst (generates requirements section)
- api-designer (generates API specifications)
- documentation-writer (generates documentation files)
- refactoring-specialist (uses Edit tool)

**Pattern Enforcement:**
source-tree.md is an immutable architectural constraint (Source: devforgeai/specs/context/architecture-constraints.md, lines 81-100). All file-generation operations MUST validate against it BEFORE calling Write() or Edit().

## Acceptance Criteria

### AC#1: Identify All File-Generation Subagents

**Given** the `.claude/agents/` directory
**When** subagents are audited for Write/Edit tool access
**Then** a complete list of file-generation subagents is produced

**Expected Subagents (based on YAML frontmatter `tools:` field):**
1. test-automator - Write (tests) [Covered by STORY-203]
2. story-requirements-analyst - Write (story sections)
3. api-designer - Write (API specs), Edit (contracts)
4. documentation-writer - Write (docs), Edit (docs)
5. refactoring-specialist - Edit (source code)
6. backend-architect - Write (implementation), Edit (code)
7. frontend-developer - Write (components), Edit (code)
8. agent-generator - Write (new subagent files)

---

### AC#2: Add source-tree.md to References Section

**Given** each file-generation subagent identified in AC#1
**When** the enhancement is applied
**Then** source-tree.md is added to the References section with the text:
```markdown
- **Source Tree:** `devforgeai/specs/context/source-tree.md` (file location constraints)
```

---

### AC#3: Add Pre-Generation Validation Section

**Given** each file-generation subagent identified in AC#1
**When** the enhancement is applied
**Then** a "Pre-Generation Validation" section is added BEFORE the first Write() or Edit() call

**Template:**
```markdown
**Pre-Generation Validation:**

Read(file_path="devforgeai/specs/context/source-tree.md")

Determine correct directory for output files:
- Extract directory patterns from source-tree.md
- Validate all planned file_path parameters match constraints

HALT if validation fails:
"""
❌ SOURCE-TREE CONSTRAINT VIOLATION

Output path violates source-tree.md constraint:

Expected directory: {expected_directory}
Attempted location: {file_path}

Fix:
1. Update file_path to match source-tree.md pattern
2. OR update source-tree.md with new location pattern
3. Retry operation
"""
```

---

### AC#4: Apply Pattern to Each Subagent

**Given** the Pre-Generation Validation template from AC#3
**When** applied to each subagent
**Then** the template is customized for each subagent's output type:

| Subagent | Output Type | Validation Pattern |
|----------|-------------|-------------------|
| story-requirements-analyst | Story sections | `devforgeai/specs/Stories/` |
| api-designer | API specs | `devforgeai/specs/analysis/` or `docs/api/` |
| documentation-writer | Documentation | `docs/` or `.claude/memory/` |
| refactoring-specialist | Source code | Per source-tree.md module patterns |
| backend-architect | Implementation | Per source-tree.md module patterns |
| frontend-developer | Components | Per source-tree.md frontend patterns |
| agent-generator | Subagent files | `.claude/agents/` |

---

### AC#5: Verify No Existing Subagents Modified Incorrectly

**Given** the pattern application to all subagents
**When** changes are complete
**Then** existing functionality is preserved:
- All existing tests pass
- No validation logic breaks current workflows
- Output files still generated in correct locations

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "story-requirements-analyst.md"
      file_path: ".claude/agents/story-requirements-analyst.md"
      requirements:
        - id: "CFG-001"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-002"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

    - type: "Configuration"
      name: "api-designer.md"
      file_path: ".claude/agents/api-designer.md"
      requirements:
        - id: "CFG-003"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-004"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

    - type: "Configuration"
      name: "documentation-writer.md"
      file_path: ".claude/agents/documentation-writer.md"
      requirements:
        - id: "CFG-005"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-006"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

    - type: "Configuration"
      name: "refactoring-specialist.md"
      file_path: ".claude/agents/refactoring-specialist.md"
      requirements:
        - id: "CFG-007"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-008"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

    - type: "Configuration"
      name: "backend-architect.md"
      file_path: ".claude/agents/backend-architect.md"
      requirements:
        - id: "CFG-009"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-010"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

    - type: "Configuration"
      name: "frontend-developer.md"
      file_path: ".claude/agents/frontend-developer.md"
      requirements:
        - id: "CFG-011"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-012"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

    - type: "Configuration"
      name: "agent-generator.md"
      file_path: ".claude/agents/agent-generator.md"
      requirements:
        - id: "CFG-013"
          description: "Add source-tree.md to References section"
          testable: true
          test_requirement: "Test: Grep for 'source-tree.md' in References"
          priority: "High"
        - id: "CFG-014"
          description: "Add Pre-Generation Validation section"
          testable: true
          test_requirement: "Test: Grep for 'Pre-Generation Validation' section"
          priority: "High"

  business_rules:
    - id: "BR-001"
      rule: "All file-generation subagents MUST validate against source-tree.md"
      trigger: "Before any Write() or Edit() operation"
      validation: "Pre-Generation Validation section exists and runs"
      error_handling: "HALT with source-tree.md constraint violation message"
      test_requirement: "Test: Each subagent has Pre-Generation Validation"
      priority: "Critical"

    - id: "BR-002"
      rule: "Pattern is consistent across all subagents"
      trigger: "During implementation"
      validation: "Same template structure used for each subagent"
      error_handling: "Review for consistency before merge"
      test_requirement: "Test: All Pre-Generation Validation sections match template"
      priority: "High"

    - id: "BR-003"
      rule: "Existing functionality preserved"
      trigger: "After pattern application"
      validation: "All existing tests pass"
      error_handling: "Regression test failure blocks merge"
      test_requirement: "Test: Run existing test suite for each subagent"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Maintainability"
      requirement: "Pattern is easy to apply to future subagents"
      metric: "< 5 minutes to add validation to new subagent"
      test_requirement: "Test: Time pattern application to new subagent"
      priority: "Medium"

    - id: "NFR-002"
      category: "Consistency"
      requirement: "All subagents use identical validation template"
      metric: "100% template compliance across subagents"
      test_requirement: "Test: Diff validation sections for consistency"
      priority: "High"
```

---

## Technical Limitations

```yaml
technical_limitations:
  - description: "Subagents without Write/Edit tools are excluded from this story"
    mitigation: "Only file-generation subagents require this pattern"
    severity: "Low"
```

---

## Non-Functional Requirements (NFRs)

### Maintainability

**Pattern Consistency:**
- All subagents use identical validation template
- Easy to add pattern to new subagents in future

### Performance

**Minimal Overhead:**
- source-tree.md reading: < 500ms per subagent invocation
- Validation: < 100ms per file path

### Reliability

**Comprehensive Coverage:**
- All 7 file-generation subagents updated
- No subagent can create files in wrong locations

---

## Dependencies

### Prerequisite Stories

- [ ] **STORY-203:** Add source-tree.md Validation to test-automator Phase 2
  - **Why:** Establishes the pattern that will be applied to other subagents
  - **Status:** Backlog

### External Dependencies

None.

### Technology Dependencies

- Claude Code Terminal Read() tool
- Markdown editing (no language-specific code)

---

## Test Strategy

### Unit Tests

**Coverage Target:** Verify pattern presence in each subagent

**Test Scenarios:**
1. Grep each subagent for "source-tree.md" in References
2. Grep each subagent for "Pre-Generation Validation" section
3. Verify HALT pattern present in each validation section

**Test File Location:** `tests/STORY-204/test-subagent-validation-pattern.sh`

---

### Integration Tests

**Coverage Target:** Verify pattern functions correctly

**Test Scenarios:**
1. Invoke documentation-writer with correct path → succeeds
2. Invoke documentation-writer with wrong path → HALT triggered
3. Repeat for each subagent with appropriate test scenario

---

## Acceptance Criteria Verification Checklist

### AC#1: Identify All File-Generation Subagents

- [ ] Audit complete for `.claude/agents/` - **Phase:** 1 - **Evidence:** list of 8 subagents
- [ ] Each subagent's tools verified - **Phase:** 1 - **Evidence:** YAML frontmatter check

### AC#2: Add source-tree.md to References Section

- [ ] story-requirements-analyst.md updated - **Phase:** 3 - **Evidence:** grep
- [ ] api-designer.md updated - **Phase:** 3 - **Evidence:** grep
- [ ] documentation-writer.md updated - **Phase:** 3 - **Evidence:** grep
- [ ] refactoring-specialist.md updated - **Phase:** 3 - **Evidence:** grep
- [ ] backend-architect.md updated - **Phase:** 3 - **Evidence:** grep
- [ ] frontend-developer.md updated - **Phase:** 3 - **Evidence:** grep
- [ ] agent-generator.md updated - **Phase:** 3 - **Evidence:** grep

### AC#3: Add Pre-Generation Validation Section

- [ ] Template defined - **Phase:** 2 - **Evidence:** template content
- [ ] Template includes HALT pattern - **Phase:** 2 - **Evidence:** template content

### AC#4: Apply Pattern to Each Subagent

- [ ] story-requirements-analyst.md validation added - **Phase:** 3 - **Evidence:** grep
- [ ] api-designer.md validation added - **Phase:** 3 - **Evidence:** grep
- [ ] documentation-writer.md validation added - **Phase:** 3 - **Evidence:** grep
- [ ] refactoring-specialist.md validation added - **Phase:** 3 - **Evidence:** grep
- [ ] backend-architect.md validation added - **Phase:** 3 - **Evidence:** grep
- [ ] frontend-developer.md validation added - **Phase:** 3 - **Evidence:** grep
- [ ] agent-generator.md validation added - **Phase:** 3 - **Evidence:** grep

### AC#5: Verify No Existing Subagents Modified Incorrectly

- [ ] Existing test suites pass - **Phase:** 5 - **Evidence:** test output
- [ ] No regressions detected - **Phase:** 5 - **Evidence:** test output

---

**Checklist Progress:** 0/19 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] 7 file-generation subagents identified (excluding test-automator from STORY-203)
- [ ] source-tree.md added to References section of each subagent
- [ ] Pre-Generation Validation section added to each subagent
- [ ] HALT pattern with clear error message in each validation
- [ ] Pattern customized for each subagent's output type

### Quality
- [ ] All 5 acceptance criteria have passing tests
- [ ] Pattern is consistent across all 7 subagents
- [ ] No regressions in existing functionality
- [ ] Error messages provide actionable guidance

### Testing
- [ ] Unit tests verify pattern presence in each subagent
- [ ] Integration tests verify pattern functions correctly
- [ ] Regression tests for existing subagent functionality

### Documentation
- [ ] Each subagent has updated References section
- [ ] Pattern rationale documented (source-tree.md is immutable constraint)

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-01-01 12:00 | claude/devforgeai-story-creation | Created | Story created from RCA-017 REC-2 | STORY-204-file-generation-subagents-source-tree-validation.story.md |

## Notes

**Design Decisions:**
- Pattern applied to all file-generation subagents for comprehensive coverage
- Consistent template ensures maintainability
- Customization per subagent allows appropriate output type validation

**Source RCA:**
- RCA-017: test-automator Source Tree Constraint Violation
- Recommendation: REC-2 (HIGH priority)
- Expected Impact: Prevents source-tree.md violations in ALL file-generation subagents

**Subagent Count:**
- 7 subagents updated by this story (excluding test-automator from STORY-203)
- Total 8 file-generation subagents after both stories complete

**Architecture Compliance:**
- Follows Context File Enforcement pattern (architecture-constraints.md lines 81-100)
- Subagent Design Constraints (architecture-constraints.md lines 46-63)
- Single Responsibility preserved (each subagent's core function unchanged)

---

**Story Template Version:** 2.5
**Last Updated:** 2026-01-01
