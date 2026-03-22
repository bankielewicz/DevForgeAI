---
id: STORY-403
title: Document Implementation Notes Format in Story Template
type: refactor
epic: EPIC-063
sprint: Backlog
status: QA Approved
priority: Medium
points: 1
created: 2026-02-08
updated: 2026-02-08
assignee: unassigned
tags: [framework, template, documentation, dod, refactor]
source_recommendation: REC-STORY370-004
depends_on: [STORY-399]
template_version: "2.8"
---

# STORY-403: Document Implementation Notes Format in Story Template

## Description

Add format requirement guidance as an HTML comment block in the story template (story-template.md) so developers see Implementation Notes format requirements at point-of-use, not only in a separate reference file.

<!-- provenance>
  <origin document="EPIC-063" section="Feature 5">
    <quote>Developers creating stories or filling in Implementation Notes don't see this critical format requirement at point-of-use</quote>
    <line_reference>lines 329-378</line_reference>
  </origin>
  <decision rationale="Point-of-use guidance prevents format errors">
    <selected>Add HTML comment to story template</selected>
    <rejected>Rely on developers reading separate reference file</rejected>
    <trade_off>Template complexity vs developer experience</trade_off>
  </decision>
</provenance -->

## User Story

**As a** DevForgeAI developer executing the /dev workflow,
**I want** Implementation Notes format requirements documented as an HTML comment directly in the story template's Definition of Done section,
**So that** I see the critical flat-structure requirement at point-of-use and avoid pre-commit validation failures caused by placing DoD items under `###` subsection headers.

## Acceptance Criteria

<acceptance_criteria id="AC1" title="HTML comment block present in story template">
  <given>The story template at `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md`</given>
  <when>A developer opens the template for editing or the `/create-story` skill reads it</when>
  <then>An HTML comment block (`<!-- ... -->`) exists within or immediately adjacent to the `## Definition of Done` section</then>
  <verification>
    <method>Read template, verify HTML comment exists in DoD section area</method>
    <expected_result>Comment block present between DoD and Change Log sections</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md" hint="Lines 796-823 area"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC2" title="Comment explains flat structure requirement">
  <given>The HTML comment block has been added to the story template</given>
  <when>A developer reads the comment content</when>
  <then>The comment explicitly states that DoD items must be placed DIRECTLY under `## Implementation Notes` with NO `###` subsection headers preceding the DoD items</then>
  <verification>
    <method>Read comment content, verify flat structure requirement explained</method>
    <expected_result>Comment states DoD items must be directly under ## header, no ### before</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md" hint="Comment content"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC3" title="Comment references extract_section() validator behavior">
  <given>The HTML comment block has been added to the story template</given>
  <when>A developer reads the comment content</when>
  <then>The comment explains that the `extract_section()` function stops at the first `###` header and DoD items under subsections will not be found</then>
  <verification>
    <method>Grep for "extract_section" in template</method>
    <expected_result>Comment contains explanation of ### header stopping behavior</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md" hint="extract_section explanation"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC4" title="Comment references dod-update-workflow.md">
  <given>The HTML comment block has been added to the story template</given>
  <when>A developer needs the full specification</when>
  <then>The comment includes a reference path to `src/claude/skills/devforgeai-development/references/dod-update-workflow.md`</then>
  <verification>
    <method>Grep for dod-update-workflow.md path in template</method>
    <expected_result>Full reference path present in comment</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-development/references/dod-update-workflow.md" hint="Referenced documentation"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC5" title="Comment is invisible in rendered markdown">
  <given>The HTML comment block uses proper HTML comment syntax (`<!-- ... -->`)</given>
  <when>The story template is rendered as markdown</when>
  <then>The comment block is completely invisible in the rendered output</then>
  <verification>
    <method>Render template, verify comment not visible</method>
    <expected_result>Comment invisible in rendered markdown</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md" hint="HTML comment syntax"/>
  </source_files>
</acceptance_criteria>

<acceptance_criteria id="AC6" title="Template version updated">
  <given>The current story template is at version 2.8</given>
  <when>The HTML comment block is added</when>
  <then>The template version metadata is updated (v2.9 or changelog entry documenting the addition)</then>
  <verification>
    <method>Read frontmatter, verify version updated or changelog entry exists</method>
    <expected_result>Version incremented or changelog documents addition</expected_result>
  </verification>
  <source_files>
    <file path="src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md" hint="Frontmatter lines 1-7"/>
  </source_files>
</acceptance_criteria>

## Technical Specification

### Component Overview

| Component | Type | Description |
|-----------|------|-------------|
| story-template.md | Configuration | Story template (add HTML comment) |

### Technical Details

```yaml
technical_specification:
  version: "2.0"
  components:
    - type: Configuration
      name: story-template-format-guidance
      file_path: src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md
      description: HTML comment with Implementation Notes format requirements
      dependencies: []
      test_requirement: HTML comment exists in DoD section, invisible when rendered

  business_rules:
    - rule: Comment explains flat structure
      description: DoD items must be directly under ## header, no ### subsections before
      test_requirement: Comment explicitly states no ### headers before DoD items

    - rule: Comment references complete documentation
      description: Must include path to dod-update-workflow.md
      test_requirement: Full reference path present in comment

  non_functional_requirements:
    - category: Performance
      requirement: No impact on template processing
      metric: < 500 bytes file size increase
      test_requirement: HTML comment approximately 350-450 characters
```

### HTML Comment Content

```html
<!-- IMPLEMENTATION NOTES FORMAT REQUIREMENT (Critical for pre-commit validation):
When filling in the Implementation Notes section during /dev workflow:
1. DoD items MUST be placed DIRECTLY under "## Implementation Notes" header
2. NO ### subsection headers (like "### Definition of Done Status") before DoD items
3. The extract_section() validator stops at the first ### header it encounters
4. If DoD items are under a ### subsection, the validator cannot find them → commit blocked
5. The ### Additional Notes subsection is OK because it comes AFTER DoD items
See: src/claude/skills/devforgeai-development/references/dod-update-workflow.md for complete details
-->
```

### Files to Modify

| File | Action | Description |
|------|--------|-------------|
| `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md` | Edit | Add HTML comment in DoD section, update version |

## Edge Cases

1. **Comment placement relative to template subsections:** Place before `## Definition of Done` or after the section, not interfering with template subsections.

2. **Stories created from older templates:** Already-created stories won't retroactively gain the comment. This is acceptable.

3. **HTML comment special characters:** Backticks, hash symbols, and parentheses are safe. Avoid `-->` sequence within body.

4. **Multiple HTML comments:** Must not conflict with existing comments. Each block must be self-contained.

5. **Template read by automated tooling:** Comment must not contain placeholder patterns the skill might replace.

## Non-Functional Requirements

| Category | Requirement | Metric |
|----------|-------------|--------|
| Performance | Minimal file size increase | < 500 bytes |
| Reliability | Comment survives template substitution | No corruption during processing |
| Security | No sensitive information | Pure documentation text |

## Definition of Done

### Implementation
- [x] HTML comment block added to story template
- [x] Comment placed in Definition of Done section area
- [x] Comment explains flat structure requirement
- [x] Comment references extract_section() behavior
- [x] Comment references dod-update-workflow.md path
- [x] Template version updated (v2.9 or changelog entry)

### Quality
- [x] HTML comment syntax correct (`<!-- ... -->`)
- [x] Comment invisible when rendered as markdown
- [x] No placeholder patterns in comment text
- [x] Reference path accurate and file exists

### Testing
- [x] Read template, verify comment exists in DoD area
- [x] Grep for "extract_section" in comment
- [x] Grep for dod-update-workflow.md path
- [x] Render template, verify comment invisible
- [x] Verify version updated in frontmatter

### Documentation
- [x] Self-documenting (the story IS the documentation change)

## Implementation Notes

- [x] HTML comment block added to story template - Completed: Added at lines 812-820 of story-template.md
- [x] Comment placed in Definition of Done section area - Completed: Placed immediately before ## Definition of Done at line 822
- [x] Comment explains flat structure requirement - Completed: Lines 814-815 state DIRECTLY under ## header, NO ### subsections
- [x] Comment references extract_section() behavior - Completed: Line 816 explains validator stops at first ### header
- [x] Comment references dod-update-workflow.md path - Completed: Line 819 includes full path src/claude/skills/devforgeai-development/references/dod-update-workflow.md
- [x] Template version updated (v2.9 or changelog entry) - Completed: Version 2.9 in frontmatter, body, footer, plus changelog entry
- [x] HTML comment syntax correct (`<!-- ... -->`) - Completed: Proper open/close tags verified by AC#5 tests
- [x] Comment invisible when rendered as markdown - Completed: Standard HTML comment syntax hides content
- [x] No placeholder patterns in comment text - Completed: Pure documentation text with no ${...} patterns
- [x] Reference path accurate and file exists - Completed: Path verified, dod-update-workflow.md exists
- [x] Read template, verify comment exists in DoD area - Completed: test_ac1_html_comment_present.sh (4/4 passing)
- [x] Grep for "extract_section" in comment - Completed: test_ac3_extract_section_reference.sh (4/4 passing)
- [x] Grep for dod-update-workflow.md path - Completed: test_ac4_dod_workflow_reference.sh (4/4 passing)
- [x] Render template, verify comment invisible - Completed: test_ac5_comment_invisible.sh (4/4 passing)
- [x] Verify version updated in frontmatter - Completed: test_ac6_template_version_updated.sh (4/4 passing)
- [x] Self-documenting (the story IS the documentation change) - Completed: This story documents the Implementation Notes format requirement

### Additional Notes

- Comment placement: Immediately before `## Definition of Done` section (line 822)
- No deferrals - all DoD items completed
- Integration tests confirmed template still works with /create-story skill

## Dependencies

- **STORY-399:** Must be implemented first (fixes the template that this feature documents)

## Notes

- **Source Recommendation:** REC-STORY370-004 from STORY-370 Phase 09 framework-analyst analysis
- **Root Cause:** Format requirements only in separate reference file, not at point-of-use
- **Impact:** Developers see guidance when editing stories

## Key References

| Reference | Path | Relevance |
|-----------|------|-----------|
| Story Template | `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md` | Target file (862 lines) |
| DoD Update Workflow | `src/claude/skills/devforgeai-development/references/dod-update-workflow.md` | Referenced documentation |

## Change Log

**Current Status:** QA Approved

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-02-08 | claude/opus | Story Creation | Initial story created from EPIC-063 Feature 5 | STORY-403-document-impl-notes-format-in-template.story.md |
| 2026-02-09 | claude/opus | /dev TDD | Implemented HTML comment block, updated version to 2.9, all 6 tests passing | story-template.md, tests/STORY-403/*.sh |
| 2026-02-09 | claude/opus | /qa deep | QA Approved: 23/23 tests pass, 6/6 ACs verified, 0 violations, 0 deferrals | STORY-403-qa-report.md |
