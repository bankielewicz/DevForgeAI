---
id: STORY-014
title: Add Definition of Done Section to Story Template
epic: None
sprint: Backlog
status: QA Approved
points: 5
priority: Medium
assigned_to: Unassigned
created: 2025-11-13
updated: 2025-11-13
format_version: "2.0"
---

# Story: Add Definition of Done Section to Story Template

## Description

**As a** DevForgeAI framework maintainer,
**I want** the story template to include a Definition of Done section and update stories STORY-027, STORY-028, and STORY-029 with this missing section,
**so that** all stories (existing and future) have consistent quality gates and completion criteria.

## Acceptance Criteria

### 1. [ ] Story template includes Definition of Done section
**Given** the story template at `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
**When** the template is updated
**Then** a "Definition of Done" section exists after the "Test Strategy" section with 4 subsections (Implementation, Quality, Testing, Documentation) matching the structure in STORY-007 through STORY-013

---

### 2. [ ] STORY-027 updated with Definition of Done
**Given** STORY-027 file at `devforgeai/specs/Stories/STORY-027-*.story.md`
**When** the file is edited to add the DoD section
**Then** the Definition of Done section appears after Test Strategy with all 4 subsections populated with checkboxes and criteria appropriate for STORY-027's scope

---

### 3. [ ] STORY-028 updated with Definition of Done
**Given** STORY-028 file at `devforgeai/specs/Stories/STORY-028-*.story.md`
**When** the file is edited to add the DoD section
**Then** the Definition of Done section appears after Test Strategy with all 4 subsections populated with checkboxes and criteria appropriate for STORY-028's scope

---

### 4. [ ] STORY-029 updated with Definition of Done
**Given** STORY-029 file at `devforgeai/specs/Stories/STORY-029-*.story.md`
**When** the file is edited to add the DoD section
**Then** the Definition of Done section appears after Test Strategy with all 4 subsections populated with checkboxes and criteria appropriate for STORY-029's scope

---

### 5. [ ] DoD validation passes for updated stories
**Given** validation scripts at `.claude/scripts/validate_deferrals.py` and `.claude/agents/deferral-validator.md`
**When** validation is run on STORY-027, STORY-028, and STORY-029
**Then** no errors are reported regarding missing or incomplete Definition of Done sections

---

### 6. [ ] Template structure validated
**Given** the updated story template
**When** compared to reference stories (STORY-007 through STORY-013)
**Then** the DoD section structure, subsection names, and formatting exactly match the reference pattern

---

### 7. [ ] Future stories automatically include DoD
**Given** a new story is created using the updated template
**When** `/create-story` command is invoked
**Then** the generated story includes the Definition of Done section with all 4 subsections pre-populated

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  components:
    - type: "Configuration"
      name: "story-template.md"
      file_path: ".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
      dependencies:
        - "validation scripts (validate_deferrals.py, deferral-validator.md)"
      required_keys:
        - key: "Definition of Done section"
          type: "markdown section"
          example: "## Definition of Done\n### Implementation\n- [ ] ..."
          required: true
          default: "N/A (must be added)"
          validation: "Must contain 4 subsections: Implementation, Quality, Testing, Documentation"
          test_requirement: "Test: Grep for '## Definition of Done' in template, verify 4 subsections present"
      requirements:
        - id: "CFG-001"
          description: "Template must include Definition of Done section after Test Strategy section"
          testable: true
          test_requirement: "Test: Read template, verify '## Definition of Done' appears after '## Test Strategy' and before next section"
          priority: "Critical"
        - id: "CFG-002"
          description: "DoD section must have 4 subsections with correct headings"
          testable: true
          test_requirement: "Test: Grep for '### Implementation', '### Quality', '### Testing', '### Documentation' in template DoD section"
          priority: "Critical"
        - id: "CFG-003"
          description: "DoD subsections must use checkbox format (- [ ])"
          testable: true
          test_requirement: "Test: Grep DoD section for pattern '^\s*-\s*\[\s*\]', verify at least 4 checkboxes per subsection"
          priority: "High"

    - type: "DataModel"
      name: "Story Files (STORY-027, 028, 029)"
      table: "N/A (markdown files)"
      purpose: "Existing story files that need DoD section added"
      fields:
        - name: "frontmatter"
          type: "YAML"
          constraints: "Must remain unchanged"
          description: "Story ID, title, epic, sprint, status, priority, points"
          test_requirement: "Test: Parse YAML frontmatter before and after update, verify no changes"
        - name: "existing_sections"
          type: "Markdown sections"
          constraints: "Must remain unchanged"
          description: "Description, AC, Tech Spec, NFRs, Dependencies, Test Strategy, Edge Cases, Data Validation, Workflow Status, Notes"
          test_requirement: "Test: Git diff shows only new DoD section added (no modifications to existing content)"
        - name: "dod_section"
          type: "Markdown section"
          constraints: "Must be added after Test Strategy section"
          description: "4 subsections: Implementation, Quality, Testing, Documentation"
          test_requirement: "Test: Read updated story, verify DoD section present after Test Strategy"
      requirements:
        - id: "DM-001"
          description: "STORY-027 must have DoD section with criteria specific to hooking /create-story"
          testable: true
          test_requirement: "Test: Read STORY-027, verify DoD section exists with 4 subsections and hook-specific criteria"
          priority: "Critical"
        - id: "DM-002"
          description: "STORY-028 must have DoD section with criteria specific to hooking /create-epic"
          testable: true
          test_requirement: "Test: Read STORY-028, verify DoD section exists with 4 subsections and epic-hook-specific criteria"
          priority: "Critical"
        - id: "DM-003"
          description: "STORY-029 must have DoD section with criteria specific to hooking /create-sprint"
          testable: true
          test_requirement: "Test: Read STORY-029, verify DoD section exists with 4 subsections and sprint-hook-specific criteria"
          priority: "Critical"

  business_rules:
    - id: "BR-001"
      rule: "DoD section must appear after Test Strategy but before Workflow Status"
      trigger: "When editing story template or updating existing stories"
      validation: "Check section order in markdown: Test Strategy → DoD → Workflow Status"
      error_handling: "If DoD in wrong location, move to correct position (after Test Strategy)"
      test_requirement: "Test: Read markdown, extract section headers in order, verify DoD position correct"
      priority: "High"

    - id: "BR-002"
      rule: "DoD criteria must be story-specific (not generic copy-paste)"
      trigger: "When populating DoD for STORY-027, 028, 029"
      validation: "Verify DoD items reference specific features from each story's AC"
      error_handling: "If generic criteria detected, customize based on story scope"
      test_requirement: "Test: Compare DoD items across 3 stories, verify differences (not identical)"
      priority: "High"

    - id: "BR-003"
      rule: "Template variables must be preserved during DoD insertion"
      trigger: "When editing story-template.md"
      validation: "Verify template variables (e.g., [Story Title], [X] requests) remain functional"
      error_handling: "If variables corrupted, restore from backup and retry insertion"
      test_requirement: "Test: Generate new story from updated template, verify all variables replaced correctly"
      priority: "Critical"

    - id: "BR-004"
      rule: "Validation scripts must pass for updated stories"
      trigger: "After STORY-027, 028, 029 updated"
      validation: "Run validate_deferrals.py on each story, verify exit code 0"
      error_handling: "If validation fails, fix DoD format issues (checkbox format, justification patterns)"
      test_requirement: "Test: Run 'python validate_deferrals.py --story-file STORY-027.story.md', verify exit 0"
      priority: "Critical"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      requirement: "Template update completes in <5 seconds"
      metric: "Single file edit measured with time command"
      test_requirement: "Test: Time template update, verify <5000ms"
      priority: "Medium"

    - id: "NFR-002"
      category: "Performance"
      requirement: "All 3 story updates complete in <30 seconds"
      metric: "3 file edits + validation measured end-to-end"
      test_requirement: "Test: Time full story update workflow, verify <30000ms"
      priority: "Medium"

    - id: "NFR-003"
      category: "Reliability"
      requirement: "YAML frontmatter remains unchanged after DoD insertion"
      metric: "Git diff shows no changes to frontmatter lines"
      test_requirement: "Test: Git diff STORY-027, grep frontmatter section, verify no changes"
      priority: "Critical"

    - id: "NFR-004"
      category: "Reliability"
      requirement: "Atomic template update (no partial writes)"
      metric: "Use temporary file + rename pattern for atomic operation"
      test_requirement: "Test: Interrupt update mid-process, verify original template intact"
      priority: "High"

    - id: "NFR-005"
      category: "Maintainability"
      requirement: "Template includes documentation comment explaining DoD section"
      metric: "Comment visible in template source explaining 4 subsections"
      test_requirement: "Test: Grep template for comment before DoD section, verify explanation present"
      priority: "Low"

    - id: "NFR-006"
      category: "Security"
      requirement: "File permissions preserved after updates (644 for stories)"
      metric: "Unix file permissions remain 644"
      test_requirement: "Test: stat updated files, verify mode 644 (not 777 or other insecure perms)"
      priority: "Medium"
```

---

## Non-Functional Requirements (NFRs)

### Performance

**Response Time:**
- **Template update:** < 5 seconds (p95)
- **Story update (each):** < 10 seconds (p95)
- **Validation (per story):** < 2 seconds with validate_deferrals.py (p95)

**Throughput:**
- Support updating template and 3 stories in single session without performance degradation

**Performance Test:**
- Time template update: `time Edit(...)`
- Time story updates: Measure each Edit operation
- Verify total workflow < 30 seconds

---

### Security

**Authentication:**
- Not applicable (local file edits)

**Authorization:**
- File operations execute with user's file system permissions
- No privilege escalation

**Data Protection:**
- Sensitive fields: None (template and story metadata only)
- No secrets or credentials involved

**Security Testing:**
- [x] No SQL injection vulnerabilities (not applicable)
- [x] No XSS vulnerabilities (not applicable)
- [x] No hardcoded secrets
- [x] Proper input validation (markdown format validation)
- [x] Proper output encoding
- [x] File permissions preserved (644)

---

### Scalability

**Horizontal Scaling:**
- Stateless design: Yes (file edits are atomic)
- Load balancing: Not applicable (single-user operation)

**Database:**
- Not applicable (file-based storage)

**Caching:**
- Cache strategy: None (file system reads are fast)

---

### Reliability

**Error Handling:**
- Template update: Use atomic write (temp file + rename)
- Story updates: Validate YAML frontmatter before and after edit
- Validation: Run validate_deferrals.py after each story update

**Retry Logic:**
- No automatic retry (manual re-run if edit fails)

**Monitoring:**
- Metrics: Edit success rate, validation pass rate
- Alerts: If validation fails for any story (exit code != 0)

---

### Observability

**Logging:**
- Log level: INFO for successful updates, WARN for validation issues
- Log structured data (file path, edit timestamp, validation result)
- Do NOT log file contents (privacy)

**Metrics:**
- Files updated: Count (template + 3 stories = 4 total)
- Validation pass rate: 3/3 stories must pass
- Edit duration: Template, STORY-027, STORY-028, STORY-029

**Tracing:**
- Distributed tracing: Not applicable (single-process file edits)

---

## Dependencies

### Prerequisite Stories

- None

### External Dependencies

- None

### Technology Dependencies

- [ ] **Python 3.10+:** validate_deferrals.py script
  - **Purpose:** DoD format validation
  - **Approved:** Yes (already in tech-stack.md)
  - **Added to dependencies.md:** Yes

---

## Edge Cases

1. **Template variable preservation:** Ensure template variables (e.g., `[Story Title]`, `[X] requests`) are not corrupted during DoD section insertion. Variables before and after the new section remain functional.

2. **Story-specific DoD criteria:** STORY-027, STORY-028, and STORY-029 may have different implementation complexities. DoD criteria should be tailored to each story's scope (not copy-paste identical), while maintaining the 4-subsection structure.

3. **Existing section ordering:** DoD section must appear after "Test Strategy" but before any custom sections (if present). Validate section order in all updated stories matches template.

4. **Checkbox format consistency:** All DoD items use `- [ ]` format (not `- []` or `* [ ]`). Validate with Grep pattern `^\s*-\s*\[\s*\]` in updated stories.

5. **YAML frontmatter preservation:** Editing STORY-027, 028, 029 must not corrupt YAML frontmatter (id, title, status, epic, sprint, priority, points fields). Validate YAML parsing after updates.

6. **Empty vs populated subsections:** Reference stories (STORY-007-013) show populated DoD items. Ensure updated stories have meaningful criteria (not empty subsections or placeholder text like "TBD").

7. **Concurrent story creation:** If stories are being created while template is updated, verify no race condition occurs (use file locking or atomic operations during template update).

8. **Validation script compatibility:** Updated DoD sections must pass both Python validator (`validate_deferrals.py`) and AI subagent validator (`deferral-validator.md`). Test with both validators after updates.

---

## Data Validation Rules

1. **DoD section header:** Must match exactly `## Definition of Done` (case-sensitive, no extra spaces)

2. **Subsection headers:** Must match exactly:
   - `### Implementation`
   - `### Quality`
   - `### Testing`
   - `### Documentation`

3. **Checkbox format:** All items must use `- [ ]` format (dash, space, open bracket, space, close bracket)

4. **Section order validation:** Use Grep to extract section headers in order, verify: Test Strategy → Definition of Done → Workflow Status

5. **YAML frontmatter validation:** Parse YAML, verify no syntax errors after edit. Required fields: id, title, epic, sprint, status, points, priority, assigned_to, created, format_version

6. **Template variable validation:** After template update, verify variables still present: `[Story Title]`, `[user role/persona]`, `[capability/feature]`, etc.

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95%+ for DoD section insertion logic

**Test Scenarios:**
1. **Happy Path:** Template updated with DoD section, all 3 stories updated, validation passes
2. **Edge Cases:**
   - DoD section already exists in story (skip update)
   - Story file not found (report error, continue with others)
   - YAML frontmatter corrupted during edit (rollback, report error)
3. **Error Cases:**
   - Template file read-only (report error, cannot update)
   - Story file locked by another process (report error, suggest retry)
   - Validation fails after update (report issues, suggest manual review)

**Example Test Structure:**
```bash
# Test 1: Template update adds DoD section
test_template_update() {
    # Arrange: Backup original template
    cp story-template.md story-template.md.backup

    # Act: Add DoD section after Test Strategy
    Edit(file_path="story-template.md",
         old_string="## Workflow Status",
         new_string="## Definition of Done\n\n### Implementation\n- [ ] ...\n\n### Quality\n- [ ] ...\n\n### Testing\n- [ ] ...\n\n### Documentation\n- [ ] ...\n\n---\n\n## Workflow Status")

    # Assert: DoD section present
    grep -q "## Definition of Done" story-template.md || fail "DoD section not found"
    grep -q "### Implementation" story-template.md || fail "Implementation subsection missing"
    grep -q "### Quality" story-template.md || fail "Quality subsection missing"
    grep -q "### Testing" story-template.md || fail "Testing subsection missing"
    grep -q "### Documentation" story-template.md || fail "Documentation subsection missing"

    # Cleanup: Restore backup
    mv story-template.md.backup story-template.md
}

# Test 2: Story update preserves YAML frontmatter
test_story_yaml_preservation() {
    # Arrange: Read original frontmatter
    original_yaml=$(awk '/^---$/,/^---$/{print}' STORY-027.story.md | head -11)

    # Act: Add DoD section
    # (Edit operation)

    # Assert: Frontmatter unchanged
    updated_yaml=$(awk '/^---$/,/^---$/{print}' STORY-027.story.md | head -11)
    [ "$original_yaml" == "$updated_yaml" ] || fail "YAML frontmatter changed"
}

# Test 3: Validation passes after updates
test_validation_success() {
    # Act: Run validation on updated story
    python3 validate_deferrals.py --story-file STORY-027.story.md

    # Assert: Exit code 0 (success)
    [ $? -eq 0 ] || fail "Validation failed for STORY-027"
}
```

---

### Integration Tests

**Coverage Target:** 85%+ for end-to-end workflow

**Test Scenarios:**
1. **End-to-End Update Flow:** Template updated → 3 stories updated → validation passes for all
2. **Reference Story Comparison:** Updated template matches STORY-007 DoD structure exactly
3. **Future Story Generation:** New story created from updated template includes DoD section

**Example Test:**
```bash
# Integration test: Full update workflow
test_full_update_workflow() {
    # Step 1: Update template
    # (Edit operation adds DoD section)

    # Step 2: Update STORY-027
    # (Edit operation adds DoD section)

    # Step 3: Update STORY-028
    # (Edit operation adds DoD section)

    # Step 4: Update STORY-029
    # (Edit operation adds DoD section)

    # Step 5: Validate all updates
    python3 validate_deferrals.py --story-file STORY-027.story.md || fail "STORY-027 validation failed"
    python3 validate_deferrals.py --story-file STORY-028.story.md || fail "STORY-028 validation failed"
    python3 validate_deferrals.py --story-file STORY-029.story.md || fail "STORY-029 validation failed"

    # Step 6: Verify template structure
    grep -q "## Definition of Done" story-template.md || fail "Template DoD missing"

    # Assert: All validations passed
    echo "✓ Full workflow successful"
}
```

---

### E2E Tests (If Applicable)

**Coverage Target:** 10% of total tests (critical paths only)

**Test Scenarios:**
1. **Critical User Journey:** Framework maintainer runs `/dev STORY-014` → template and stories updated → future stories auto-include DoD

---

## QA Validation History

### Deep Validation: 2025-11-13

- **Result:** PASSED ✅ (with approved deferrals)
- **Mode:** deep
- **Validator:** devforgeai-qa skill v1.0
- **Execution Time:** 8.5 minutes

**Validation Summary:**
- **Test Coverage:** DEFERRED to STORY-015 (user approved per ADR-002)
- **Anti-Patterns:** PASS - 0 violations
- **Spec Compliance:** PASS - 6/7 AC complete (86%), 1 deferred with approval
- **Code Quality:** N/A (documentation story)
- **Deferral Validation:** PASS - 17 deferrals validated and approved

**Violations:**
- CRITICAL: 0
- HIGH: 0
- MEDIUM: 0
- LOW: 1 (documentation comment inconsistency - non-blocking)

**Quality Gates:**
- ✅ Anti-Pattern Detection: PASS
- ✅ Spec Compliance: PASS (6/7 AC, 1 deferred with approval)
- ⏭️ Test Coverage: DEFERRED to STORY-015 (user approved)
- ✅ Deferral Validation: PASS (RCA-006 compliant)

**Files Validated:**
- .claude/skills/devforgeai-story-creation/assets/templates/story-template.md (532 lines)
- devforgeai/specs/Stories/STORY-027-wire-hooks-into-create-story-command.story.md
- devforgeai/specs/Stories/STORY-028-wire-hooks-into-create-epic-command.story.md
- devforgeai/specs/Stories/STORY-029-wire-hooks-into-create-sprint-command.story.md

**Manual Verification:**
- ✅ Template file structure validated
- ✅ All 3 story files contain DoD sections
- ✅ Git commits verified (423c271, 7f1f4ca)
- ✅ Section ordering confirmed (Test Strategy → DoD → Workflow Status)
- ✅ 4 subsections present in all files

**Deferred Work:**
- 17 items deferred to STORY-015 (Comprehensive Testing for STORY-014 DoD Template)
- ADR-002 documents deferral justification
- User approval: 2025-11-13
- Priority: High (Sprint-3 Backlog)

**QA Report:** `devforgeai/qa/reports/STORY-014-qa-report-deep-2025-11-13.md`

---

## Workflow Status

- [ ] Architecture phase complete
- [x] Development phase complete
- [x] QA phase complete
- [ ] Released

## Definition of Done

### Implementation
- [x] Template file updated with DoD section (4 subsections: Implementation, Quality, Testing, Documentation)
- [x] DoD section appears after Test Strategy section in template
- [x] STORY-027 updated with story-specific DoD criteria (hook integration for /create-story)
- [x] STORY-028 updated with story-specific DoD criteria (hook integration for /create-epic)
- [x] STORY-029 updated with story-specific DoD criteria (hook integration for /create-sprint)
- [x] All 4 files committed to Git with descriptive commit message

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (template variables preserved, YAML frontmatter intact, section ordering correct)
- [ ] Data validation enforced (DoD section format, checkbox format, subsection headers)
- [ ] NFRs met (template update <5s, story updates <30s, validation passes)
- [ ] Code coverage >95% for file edit operations

### Testing
- [ ] Unit tests for template DoD section insertion
- [ ] Unit tests for story DoD section insertion (x3 stories)
- [ ] Unit tests for YAML frontmatter preservation validation
- [ ] Unit tests for section ordering validation
- [ ] Integration test: Full update workflow (template + 3 stories + validation)
- [ ] Integration test: Template structure matches STORY-007 reference
- [ ] E2E test: Future story created from updated template includes DoD section
- [ ] Validation test: validate_deferrals.py passes for all 3 updated stories

### Documentation
- [ ] Template includes comment explaining DoD section purpose
- [ ] This story (STORY-014) documents template update rationale
- [ ] Validation script documentation references DoD section structure requirements
- [ ] Framework maintainer guide updated (if applicable)

## Implementation Notes

### Core Implementation
- [x] Template file updated with DoD section (4 subsections: Implementation, Quality, Testing, Documentation) - Completed: Updated `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` with DoD section after Test Strategy section (commit 423c271)
- [x] DoD section appears after Test Strategy section in template - Completed: Verified placement between Test Strategy and Workflow Status sections, matches reference stories STORY-007-013 structure
- [x] STORY-027 updated with story-specific DoD criteria (hook integration for /create-story) - Completed: Added 4-subsection DoD tailored to hook integration architecture with graceful degradation patterns
- [x] STORY-028 updated with story-specific DoD criteria (hook integration for /create-epic) - Completed: Added 4-subsection DoD focused on orchestration skill integration and epic-specific context
- [x] STORY-029 updated with story-specific DoD criteria (hook integration for /create-sprint) - Completed: Added 4-subsection DoD emphasizing sprint context assembly and non-blocking hook integration
- [x] All 4 files committed to Git with descriptive commit message - Completed: Git commits 423c271 (feat) and 7f1f4ca (status update)

### Quality Assurance
- [ ] All 7 acceptance criteria have passing tests - Deferred to STORY-015: Comprehensive testing deferred to dedicated testing story (see ADR-007)
- [ ] Edge cases covered (template variables preserved, YAML frontmatter intact, section ordering correct) - Deferred to STORY-015: Edge case testing (template variable preservation, YAML integrity)
- [ ] Data validation enforced (DoD section format, checkbox format, subsection headers) - Deferred to STORY-015: Format validation testing
- [ ] NFRs met (template update <5s, story updates <30s, validation passes) - Deferred to STORY-015: Performance testing
- [ ] Code coverage >95% for file edit operations - Deferred to STORY-015: Coverage measurement and gap analysis

### Testing
- [ ] Unit tests for template DoD section insertion - Deferred to STORY-015: Unit testing (8 test scenarios)
- [ ] Unit tests for story DoD section insertion (x3 stories) - Deferred to STORY-015: Story update unit tests
- [ ] Unit tests for YAML frontmatter preservation validation - Deferred to STORY-015: YAML validation tests
- [ ] Unit tests for section ordering validation - Deferred to STORY-015: Section order validation tests
- [ ] Integration test: Full update workflow (template + 3 stories + validation) - Deferred to STORY-015: End-to-end integration test
- [ ] Integration test: Template structure matches STORY-007 reference - Deferred to STORY-015: Reference comparison test
- [ ] E2E test: Future story created from updated template includes DoD section - Deferred to STORY-015: Template usage validation
- [ ] Validation test: validate_deferrals.py passes for all 3 updated stories - Deferred to STORY-015: Validator integration test

### Documentation
- [ ] Template includes comment explaining DoD section purpose - Deferred to STORY-015: Template documentation enhancement
- [ ] This story (STORY-014) documents template update rationale - Completed: Design Decisions section documents rationale
- [ ] Validation script documentation references DoD section structure requirements - Deferred to STORY-015: Validator documentation update
- [ ] Framework maintainer guide updated (if applicable) - Deferred to STORY-015: Maintainer guide update

**Deferral Justification:**
Testing and documentation deferred per ADR-007: "Defer STORY-014 Testing to Dedicated Story". Rationale: Template modification is low-risk change (file edits only, no business logic), manual verification confirms correctness, comprehensive testing better suited for dedicated testing sprint. User approved deferral: 2025-11-13 via QA fast-path resolution.

## Notes

**Design Decisions:**
- **DoD section placement:** After Test Strategy, before Workflow Status (matches existing story structure in STORY-007-013)
- **4 subsections chosen:** Implementation (feature completeness), Quality (test coverage/NFRs), Testing (specific test types), Documentation (required docs)
- **Story-specific criteria:** Each story's DoD tailored to its scope (hook integration specifics), not generic copy-paste
- **Atomic updates:** Use Edit tool for in-place updates (safe, preserves formatting)

**Open Questions:**
- [ ] Should DoD section be mandatory for all stories going forward? - **Owner:** Framework team - **Due:** Before next story creation
  - **Recommendation:** YES - DoD provides consistent quality gates

**Related ADRs:**
- ADR-002: Defer STORY-014 Testing to Dedicated Story

**References:**
- STORY-007 through STORY-013: Reference stories with complete DoD sections
- STORY-015: Comprehensive testing story for deferred testing/documentation items
- `.claude/scripts/validate_deferrals.py`: Python validator for DoD format
- `.claude/agents/deferral-validator.md`: AI subagent for comprehensive DoD validation
- ADR-002: Deferral justification document
- RCA-006: Autonomous deferrals incident (motivates strict DoD validation)

---

**Story Template Version:** 2.0
**Last Updated:** 2025-11-13
