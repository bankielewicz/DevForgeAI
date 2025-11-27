---
id: STORY-090
title: Update Story Template to v2.2 with depends_on Field
epic: EPIC-010
sprint: SPRINT-5
status: Ready for Dev
points: 3
priority: Critical
assigned_to: TBD
created: 2025-11-25
format_version: "2.1"
depends_on: []
---

# Story: Update Story Template to v2.2 with depends_on Field

## Description

**As a** DevForgeAI framework developer,
**I want** the story template to include a standardized `depends_on` field in array format,
**so that** all stories can declare dependencies consistently, enabling automated dependency graph enforcement for parallel development workflows.

**Context:** This is a prerequisite story for EPIC-010 (Parallel Story Development). The depends_on field enables Feature 3 (Dependency Graph Enforcement) which blocks /dev execution until all dependencies reach "Dev Complete" or "QA Approved" status.

## Acceptance Criteria

### AC#1: Story Template Updated with depends_on Field

**Given** the story template at `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
**When** a developer examines the YAML frontmatter section
**Then** the template includes a `depends_on: []` field with:
- Default empty array `[]` for stories with no dependencies
- Comment explaining usage: `# Array of STORY-NNN IDs this story depends on`
- Placement after `points:` field and before `status:` field in frontmatter order

---

### AC#2: Format Version Incremented to 2.2

**Given** the story template YAML frontmatter contains a `format_version` field
**When** the template is updated with the depends_on field
**Then** the `format_version` value is changed from `"2.1"` to `"2.2"`
**And** the version string follows semantic versioning format (MAJOR.MINOR)

---

### AC#3: Template Changelog Documents v2.2 Changes

**Given** the story template contains a changelog section (lines 1-58)
**When** the v2.2 update is applied
**Then** a changelog entry exists documenting:
- Version: 2.2
- Date: 2025-11-25
- Change description: "Added depends_on field for EPIC-010 parallel development support"
- Backward compatibility note: "Compatible with v2.1 stories (depends_on field optional for existing stories)"

---

### AC#4: Six Existing Stories Standardized to Array Format

**Given** the following stories exist with potential non-array dependency declarations:
- STORY-044
- STORY-045
- STORY-046
- STORY-047
- STORY-048
- STORY-070
**When** each story file is examined and updated
**Then** each story contains `depends_on:` field in array format:
- Empty dependencies: `depends_on: []`
- Single dependency: `depends_on: ["STORY-NNN"]`
- Multiple dependencies: `depends_on: ["STORY-NNN", "STORY-MMM"]`
**And** no story uses string format (e.g., `depends_on: "STORY-044"`)
**And** no story uses comma-separated format (e.g., `depends_on: STORY-044, STORY-045`)

---

### AC#5: Story-Creation Skill Phase 1 Dependency Question

**Given** the devforgeai-story-creation skill is invoked via `/create-story`
**When** Phase 1 (Information Gathering) executes
**Then** the skill asks an optional question about dependencies:
- Question text: "Does this story depend on other stories? (Enter STORY-IDs or 'none')"
- Question is marked as optional (user can skip)
- Accepts formats: "none", "STORY-044", "STORY-044, STORY-045"
- Normalizes input to array format in generated story frontmatter

---

### AC#6: Operational Directory Sync Complete

**Given** the story template is updated in `src/claude/skills/devforgeai-story-creation/assets/templates/`
**When** the story implementation is complete
**Then** the updated template is synced to `.claude/skills/devforgeai-story-creation/assets/templates/`
**And** both locations contain identical content (verified via diff)

---

### AC#7: Existing Story Content Preservation

**Given** the 6 stories (STORY-044 through STORY-048, STORY-070) contain existing content
**When** the `depends_on` field standardization is applied
**Then** only the frontmatter `depends_on` field is modified
**And** all other frontmatter fields remain unchanged
**And** all story body content (User Story, AC, DoD, etc.) remains unchanged

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    # Configuration Component - Story Template
    - type: "Configuration"
      name: "story-template.md"
      file_path: "src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
      purpose: "Story template with YAML frontmatter defining story structure for all DevForgeAI stories"
      required_keys:
        - key: "depends_on"
          type: "array"
          example: "[]"
          required: true
          default: "[]"
          validation: "Array of STORY-NNN format strings matching ^STORY-\\d{3,4}$"
          test_requirement: "Test: Verify depends_on field exists in template frontmatter and accepts array format"
        - key: "format_version"
          type: "string"
          example: "2.2"
          required: true
          validation: "Semantic version format matching ^\\d+\\.\\d+$"
          test_requirement: "Test: Verify format_version is '2.2' after update"
      requirements:
        - id: "CFG-001"
          description: "Add depends_on field to YAML frontmatter after points field"
          testable: true
          test_requirement: "Test: Parse template YAML, verify depends_on field exists between points and status"
          priority: "Critical"
        - id: "CFG-002"
          description: "Increment format_version from 2.1 to 2.2"
          testable: true
          test_requirement: "Test: Read template, verify format_version equals '2.2'"
          priority: "Critical"
        - id: "CFG-003"
          description: "Add changelog entry documenting v2.2 changes"
          testable: true
          test_requirement: "Test: Verify template contains changelog section with v2.2 entry mentioning depends_on"
          priority: "High"

    # Service Component - Story Creation Skill Enhancement
    - type: "Service"
      name: "devforgeai-story-creation"
      file_path: "src/claude/skills/devforgeai-story-creation/SKILL.md"
      interface: "Skill"
      lifecycle: "On-demand (skill invocation)"
      dependencies:
        - "story-template.md"
        - "story-discovery.md"
      requirements:
        - id: "SVC-001"
          description: "Phase 1 asks optional dependency question during story creation"
          testable: true
          test_requirement: "Test: Invoke /create-story, verify AskUserQuestion includes dependency prompt"
          priority: "High"
        - id: "SVC-002"
          description: "Parse user dependency input into array format"
          testable: true
          test_requirement: "Test: Input 'STORY-044, STORY-045' converts to ['STORY-044', 'STORY-045']"
          priority: "High"
        - id: "SVC-003"
          description: "Handle 'none' input as empty array"
          testable: true
          test_requirement: "Test: Input 'none' converts to []"
          priority: "Medium"

    # Worker Component - Story Standardization Script
    - type: "Worker"
      name: "story-standardization"
      file_path: "src/claude/skills/devforgeai-story-creation/scripts/standardize-depends-on.sh"
      interface: "Bash Script"
      polling_interval_ms: 0
      dependencies:
        - "story-template.md"
      requirements:
        - id: "WKR-001"
          description: "Standardize 6 stories (STORY-044 through STORY-048, STORY-070) to array format"
          testable: true
          test_requirement: "Test: Run script, verify all 6 stories have depends_on: [] or depends_on: ['STORY-NNN'] format"
          priority: "Critical"
        - id: "WKR-002"
          description: "Preserve all existing story content (body unchanged)"
          testable: true
          test_requirement: "Test: Compare story body before/after, verify identical content"
          priority: "Critical"
        - id: "WKR-003"
          description: "Handle missing depends_on field by adding it"
          testable: true
          test_requirement: "Test: Story without depends_on field gets field added"
          priority: "High"
        - id: "WKR-004"
          description: "Skip stories already in correct array format"
          testable: true
          test_requirement: "Test: Story with depends_on: [] remains unchanged"
          priority: "Medium"

  business_rules:
    - id: "BR-001"
      rule: "depends_on field must be YAML array format (not string, not comma-separated)"
      trigger: "Story creation or standardization"
      validation: "Parse YAML, verify type is list/array"
      error_handling: "Convert non-array to array format"
      test_requirement: "Test: Invalid format 'STORY-044' converts to ['STORY-044']"
      priority: "Critical"
    - id: "BR-002"
      rule: "Each dependency in array must match STORY-NNN format (3-4 digits)"
      trigger: "Dependency validation"
      validation: "Regex match ^STORY-\\d{3,4}$"
      error_handling: "Reject invalid format with error message"
      test_requirement: "Test: 'story-044' rejected, 'STORY-044' accepted"
      priority: "High"
    - id: "BR-003"
      rule: "Backward compatibility: Stories without depends_on field remain valid"
      trigger: "Story parsing during /dev, /qa"
      validation: "Treat missing depends_on as empty array"
      error_handling: "No error, default to []"
      test_requirement: "Test: v2.1 story without depends_on parses successfully"
      priority: "High"
    - id: "BR-004"
      rule: "Template sync: src/ changes must be synced to .claude/ operational directory"
      trigger: "Story completion"
      validation: "Diff between src/ and .claude/ versions"
      error_handling: "Copy src/ to .claude/"
      test_requirement: "Test: After sync, diff returns no differences"
      priority: "High"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Story file update time"
      metric: "< 100ms per story file for frontmatter modification"
      test_requirement: "Test: Time story update, verify < 100ms"
      priority: "Medium"
    - id: "NFR-002"
      category: "Performance"
      requirement: "Total standardization time"
      metric: "< 2 seconds for all 6 stories including file I/O"
      test_requirement: "Test: Time full standardization run, verify < 2s"
      priority: "Medium"
    - id: "NFR-003"
      category: "Reliability"
      requirement: "Idempotent operation"
      metric: "Running standardization N times produces identical result"
      test_requirement: "Test: Run standardization twice, verify identical output"
      priority: "High"
    - id: "NFR-004"
      category: "Reliability"
      requirement: "Atomic file updates"
      metric: "Story file either fully updated or unchanged (no partial writes)"
      test_requirement: "Test: Interrupt during write, verify file intact"
      priority: "High"
    - id: "NFR-005"
      category: "Maintainability"
      requirement: "Template changelog documentation"
      metric: "Every version change documented with date, description, and compatibility note"
      test_requirement: "Test: Verify v2.2 changelog entry contains all required fields"
      priority: "Medium"
```

---

## Non-Functional Requirements

### Performance
- Story file update time: < 100ms per story file for frontmatter modification
- Total standardization time: < 2 seconds for all 6 stories including file I/O
- Phase 1 dependency question response processing: < 10ms for input parsing

### Security
- File operations use native Claude tools (Read, Write, Edit) - no shell injection vectors
- No external network calls required for this story
- Story file modifications preserve original file permissions
- Frontmatter parsing uses safe YAML subset (no arbitrary code execution)

### Reliability
- Idempotent operation: Running standardization multiple times produces same result
- Atomic file updates: Story file either fully updated or unchanged (no partial writes)
- Error handling: If one story file fails to update, continue with remaining stories and report failures at end
- Validation before write: Verify YAML frontmatter is valid before writing changes

### Maintainability
- Template changelog enables tracking of version history
- Clear field comments in template explain purpose and usage
- Standardization logic documented in story for future reference
- Backward compatibility: Stories with format_version 2.1 remain valid (depends_on optional)

### Scalability
- Standardization approach works for any number of stories (not hardcoded to 6)
- Array format supports unlimited dependencies per story
- No performance degradation with dependency counts up to 50 per story

---

## Edge Cases

1. **Story with depends_on field already in array format:** If a story (e.g., STORY-070) already has `depends_on: ["STORY-066"]` in correct array format, the standardization process should detect this and skip modification, logging "Already in array format - no change needed."

2. **Story with depends_on field set to null or empty string:** If a story has `depends_on: null` or `depends_on: ""`, the standardization should convert to `depends_on: []` (empty array), not leave as-is.

3. **Story with depends_on field containing invalid STORY-ID:** If a story references a non-existent story (e.g., `depends_on: ["STORY-999"]` where STORY-999 doesn't exist), the standardization should preserve the reference but log a warning: "Warning: STORY-999 referenced but not found in .ai_docs/Stories/". Validation of dependency existence is Feature 3's responsibility.

4. **Story without depends_on field entirely:** If a story was created before v2.2 and lacks a `depends_on` field, the standardization should add `depends_on: []` to the frontmatter in the correct position (after `points:`, before `status:`).

5. **Circular dependency declaration:** If STORY-044 depends on STORY-045 and STORY-045 depends on STORY-044, this story's scope is standardization only. Circular dependency detection is Feature 3's responsibility. The standardization should preserve the declarations as-is.

6. **User enters dependency for non-existent story in /create-story:** When Phase 1 asks about dependencies and user enters "STORY-999" (non-existent), the skill should accept the input and include it in frontmatter, but display a warning: "Note: STORY-999 not found. Dependency will be recorded but may need verification."

---

## Data Validation Rules

1. **depends_on field format:** Must be a YAML array. Valid: `[]`, `["STORY-044"]`, `["STORY-044", "STORY-045"]`. Invalid: `"STORY-044"` (string), `STORY-044, STORY-045` (bare comma-separated), `null`.

2. **STORY-ID format in depends_on array:** Each element must match regex pattern `^STORY-\d{3,4}$`. Examples: "STORY-044" (valid), "STORY-1234" (valid), "story-044" (invalid - lowercase), "STORY-44" (invalid - insufficient digits), "044" (invalid - missing prefix).

3. **format_version field:** Must be string in MAJOR.MINOR format matching regex `^\d+\.\d+$`. Examples: "2.2" (valid), "2.10" (valid), "2" (invalid), "v2.2" (invalid).

4. **Frontmatter field ordering:** The `depends_on` field should appear in this position within frontmatter:
   ```yaml
   id: "STORY-NNN"
   epic: "EPIC-NNN"
   title: "..."
   priority: "..."
   points: N
   depends_on: []        # <-- After points, before status
   status: "..."
   ```

5. **Changelog entry format:** Each changelog entry must contain: version (string), date (YYYY-MM-DD), and description (string, 10-200 characters).

---

## Dependencies

### Prerequisite Stories
None - This is a prerequisite story that blocks Feature 3 (Dependency Graph Enforcement).

### External Dependencies
None

### Technology Dependencies
- YAML parser (built-in to Claude Code tools)
- Git (for version history, no backups needed)

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for business logic

**Test Scenarios:**

1. **Template Update Tests:**
   - Test: Template contains depends_on field in correct position
   - Test: format_version equals "2.2"
   - Test: Changelog contains v2.2 entry

2. **Standardization Tests:**
   - Test: Empty array `depends_on: []` preserved unchanged
   - Test: String format `depends_on: "STORY-044"` converted to `["STORY-044"]`
   - Test: Comma-separated converted to array
   - Test: Null/empty string converted to `[]`
   - Test: Missing field added with default `[]`
   - Test: Story body content unchanged after update

3. **Skill Enhancement Tests:**
   - Test: Phase 1 includes optional dependency question
   - Test: Input "none" normalizes to `[]`
   - Test: Input "STORY-044" normalizes to `["STORY-044"]`
   - Test: Input "STORY-044, STORY-045" normalizes to `["STORY-044", "STORY-045"]`

4. **Validation Tests:**
   - Test: Valid STORY-ID format accepted
   - Test: Invalid format rejected with error
   - Test: Regex validation matches specification

---

### Integration Tests

**Coverage Target:** 85%+ for application layer

**Test Scenarios:**

1. **End-to-End Template Update:**
   - Update template in src/
   - Sync to .claude/
   - Verify both locations identical

2. **Story Standardization Flow:**
   - Run standardization on all 6 stories
   - Verify each has valid depends_on array
   - Verify no content corruption

3. **Create-Story with Dependencies:**
   - Run /create-story
   - Answer dependency question
   - Verify generated story has correct depends_on

---

## Acceptance Criteria Verification Checklist

### AC#1: Story Template Updated with depends_on Field
- [ ] depends_on field exists in template frontmatter - **Phase:** 2 - **Evidence:** story-template.md
- [ ] Default value is empty array [] - **Phase:** 2 - **Evidence:** story-template.md
- [ ] Field positioned after points, before status - **Phase:** 2 - **Evidence:** story-template.md

### AC#2: Format Version Incremented to 2.2
- [ ] format_version value is "2.2" - **Phase:** 2 - **Evidence:** story-template.md
- [ ] Version format is MAJOR.MINOR - **Phase:** 2 - **Evidence:** story-template.md

### AC#3: Template Changelog Documents v2.2 Changes
- [ ] Changelog entry exists for v2.2 - **Phase:** 2 - **Evidence:** story-template.md lines 1-58
- [ ] Entry includes date - **Phase:** 2 - **Evidence:** story-template.md
- [ ] Entry includes description - **Phase:** 2 - **Evidence:** story-template.md
- [ ] Entry includes backward compatibility note - **Phase:** 2 - **Evidence:** story-template.md

### AC#4: Six Existing Stories Standardized to Array Format
- [ ] STORY-044 has array format depends_on - **Phase:** 2 - **Evidence:** STORY-044.story.md
- [ ] STORY-045 has array format depends_on - **Phase:** 2 - **Evidence:** STORY-045.story.md
- [ ] STORY-046 has array format depends_on - **Phase:** 2 - **Evidence:** STORY-046.story.md
- [ ] STORY-047 has array format depends_on - **Phase:** 2 - **Evidence:** STORY-047.story.md
- [ ] STORY-048 has array format depends_on - **Phase:** 2 - **Evidence:** STORY-048.story.md
- [ ] STORY-070 has array format depends_on - **Phase:** 2 - **Evidence:** STORY-070.story.md

### AC#5: Story-Creation Skill Phase 1 Dependency Question
- [ ] Phase 1 includes optional dependency question - **Phase:** 2 - **Evidence:** story-discovery.md
- [ ] Question accepts STORY-ID input - **Phase:** 2 - **Evidence:** story-discovery.md
- [ ] Input normalized to array format - **Phase:** 2 - **Evidence:** story-discovery.md

### AC#6: Operational Directory Sync Complete
- [ ] src/ template synced to .claude/ - **Phase:** 5 - **Evidence:** diff command
- [ ] Both locations contain identical content - **Phase:** 5 - **Evidence:** diff returns 0

### AC#7: Existing Story Content Preservation
- [ ] Story body content unchanged - **Phase:** 2 - **Evidence:** diff before/after
- [ ] Other frontmatter fields unchanged - **Phase:** 2 - **Evidence:** diff before/after

---

**Checklist Progress:** 0/20 items complete (0%)

---

## Definition of Done

### Implementation
- [ ] Template updated with depends_on field in correct position
- [ ] format_version incremented to "2.2"
- [ ] Changelog entry added for v2.2
- [ ] 6 stories standardized to array format (STORY-044, 045, 046, 047, 048, 070)
- [ ] story-discovery.md updated with optional dependency question
- [ ] Input normalization logic implemented
- [ ] src/ to .claude/ sync completed

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (null, empty string, already array, missing field)
- [ ] Data validation enforced (STORY-ID regex, array format)
- [ ] NFRs met (< 100ms per file, idempotent, atomic)
- [ ] Code coverage >95% for standardization logic

### Testing
- [ ] Unit tests for template validation
- [ ] Unit tests for standardization script
- [ ] Unit tests for skill Phase 1 enhancement
- [ ] Integration tests for end-to-end flow
- [ ] Manual verification of 6 standardized stories

### Documentation
- [ ] Template changelog updated with v2.2 entry
- [ ] Story-discovery.md documents dependency question
- [ ] Implementation notes capture design decisions

---

## Workflow Status

- [ ] Architecture phase complete
- [ ] Development phase complete
- [ ] QA phase complete
- [ ] Released

## Workflow History

### 2025-11-27 14:30:00 - Status: Ready for Dev
- Added to SPRINT-5: Parallel Story Development Foundation
- Transitioned from Backlog to Ready for Dev
- Sprint capacity: 45 points
- Priority in sprint: 1 of 7 (Critical - prerequisite story)

---

## Notes

**Design Decisions:**
1. **Array format over string:** Enables multiple dependencies, consistent parsing, and compatibility with Feature 3 dependency graph algorithms
2. **Optional question in Phase 1:** Non-blocking for stories without dependencies, reduces friction for simple stories
3. **Backward compatibility:** Stories without depends_on field remain valid (treated as empty array)
4. **Standardization over migration:** Active update of 6 stories rather than gradual migration ensures consistency for EPIC-010

**Blocks:**
- Feature 3 (Dependency Graph Enforcement with Transitive Resolution) - requires standardized depends_on field

**Related Epic:**
- EPIC-010: Parallel Story Development with CI/CD Integration

**References:**
- `.devforgeai/specs/STRUCTURED-FORMAT-SPECIFICATION.md` - Tech spec schema
- `src/claude/skills/devforgeai-story-creation/references/story-discovery.md` - Phase 1 workflow

---

**Story Template Version:** 2.1
**Created:** 2025-11-25

## Implementation Notes

No implementation yet - story in planning/backlog phase.
