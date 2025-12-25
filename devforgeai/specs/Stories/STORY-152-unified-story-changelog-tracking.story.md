---
id: STORY-152
title: Unified Story Change Log Tracking with Subagent Attribution
type: feature
epic: null
sprint: Backlog
priority: Medium
points: 8
depends_on: []
status: Backlog
assigned_to: null
created: 2025-12-24
updated: 2025-12-24
format_version: "2.4"
tags: [framework, traceability, changelog, audit-trail]
---

# Unified Story Change Log Tracking with Subagent Attribution

## Description

**As a** framework maintainer and skill developer,
**I want** to track all story modifications through a unified, mandatory Change Log section with subagent attribution,
**So that** I can audit who made what changes at what time and maintain transparent modification history across all DevForgeAI skills and workflows.

### Problem Statement

- Current `## Workflow Status` section in story template has only 4 checkboxes
- Dev agent inconsistently adds expanded Status History table (seen in STORY-131)
- No consistent tracking of who (subagent) did what and when
- Need formalized, mandatory tracking with subagent attribution

### Solution

Replace `## Workflow Status` with unified `## Change Log` section that:
- Tracks both workflow state transitions AND file edits
- Attributes each entry to specific subagent (e.g., `claude/test-automator`)
- Uses shared reference file to ensure consistency across all skills
- Provides project-level CHANGELOG.md with story ID references

---

## Acceptance Criteria

### AC#1: Story Template Updated with Change Log Section

**Given** the story template at `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md` contains the current "## Workflow Status" section with 4 checkboxes
**When** a developer creates a new story using the updated template
**Then** the "## Workflow Status" section is replaced with "## Change Log" containing:
- `**Current Status:** Backlog` header
- Table with columns: Date | Author | Phase/Action | Change | Files Affected
- Initial entry with author `claude/story-requirements-analyst` and action "Created"

---

### AC#2: Shared Changelog Reference Guide Created

**Given** the changelog-update-guide.md file is created at `.claude/references/changelog-update-guide.md`
**When** devforgeai-development, devforgeai-qa, and devforgeai-release skills execute their workflows
**Then** each skill references this shared guide and appends entries with consistent format where author matches pattern `^(claude/[a-z-]+|user/[a-zA-Z0-9_-]+|claude/opus)$`

---

### AC#3: devforgeai-development Skill Appends Changelog Entries

**Given** a developer runs `/dev STORY-XXX` to implement a story
**When** each TDD phase completes (Red, Green, Refactor, Integration, DoD Update, Git)
**Then** the skill appends a Change Log entry with:
- Correct subagent author (e.g., `claude/test-automator` for Red phase)
- Phase/Action description (e.g., "Red (Phase 02)")
- Change summary (e.g., "Tests for AC#1-3")
- Files affected list

---

### AC#4: devforgeai-qa Skill Appends Changelog Entry

**Given** a QA validator runs `/qa STORY-XXX` on a story
**When** QA validation completes (passed or failed)
**Then** the devforgeai-qa skill appends a Change Log entry with:
- Author: `claude/qa-result-interpreter`
- Phase/Action: "QA {mode}" (Light or Deep)
- Change: "{result}: Coverage {pct}%, {violations} violations"

---

### AC#5: devforgeai-release Skill Appends Changelog and Archives Story

**Given** a story transitions from QA Approved to Released status via `/release STORY-XXX`
**When** the devforgeai-release skill completes release workflow
**Then** the skill:
- Appends final Change Log entry with author `claude/deployment-engineer`
- Updates `**Current Status:**` to "Released"
- Moves story file to `devforgeai/specs/Stories/archive/` subdirectory
- Updates project CHANGELOG.md with story reference

---

### AC#6: Project CHANGELOG.md Created with Keep a Changelog Format

**Given** CHANGELOG.md does not exist at project root
**When** the first story is released after this feature implementation
**Then** CHANGELOG.md is created with:
- Keep a Changelog v1.1.0 compliant format
- Sections: `## [Unreleased]`, `## [X.Y.Z] - YYYY-MM-DD`
- Story entries format: `- Feature description ([STORY-XXX])`
- Reference links at bottom: `[STORY-XXX]: devforgeai/specs/Stories/archive/STORY-XXX.story.md`

---

### AC#7: Backward Compatible with Existing Stories

**Given** an existing story without `## Change Log` section is edited by any skill
**When** the skill attempts to append a changelog entry
**Then** the skill:
- Detects missing Change Log section
- Creates the section with initial "Story Migrated" entry
- Appends the new entry normally
- Preserves all existing story content

---

## Technical Specification

```yaml
technical_specification:
  format_version: "2.0"

  reference_files:
    plan_file: ".claude/plans/refactored-bouncing-widget.md"
    story_template: ".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
    dev_skill: ".claude/skills/devforgeai-development/SKILL.md"
    qa_skill: ".claude/skills/devforgeai-qa/SKILL.md"
    release_skill: ".claude/skills/devforgeai-release/SKILL.md"
    dod_workflow: ".claude/skills/devforgeai-development/references/dod-update-workflow.md"
    release_docs: ".claude/skills/devforgeai-release/references/release-documentation.md"
    source_tree: "devforgeai/specs/context/source-tree.md"

  components:
    - type: "Configuration"
      name: "ChangelogUpdateGuide"
      file_path: ".claude/references/changelog-update-guide.md"
      create: true
      requirements:
        - id: "CFG-001"
          description: "Define Change Log table format with 5 columns: Date | Author | Phase/Action | Change | Files Affected"
          testable: true
          test_requirement: "Reference guide contains exact markdown table format"
          priority: "Critical"
        - id: "CFG-002"
          description: "Specify author attribution patterns (claude/{subagent}, user/{name}, claude/opus)"
          testable: true
          test_requirement: "Guide lists all valid author format examples with regex pattern"
          priority: "Critical"
        - id: "CFG-003"
          description: "Provide Edit tool snippets for appending entries"
          testable: true
          test_requirement: "Each skill can copy append logic from guide"
          priority: "High"
        - id: "CFG-004"
          description: "Document timestamp format and Current Status update procedure"
          testable: true
          test_requirement: "Format: YYYY-MM-DD HH:MM documented with example"
          priority: "High"

    - type: "DataModel"
      name: "ChangeLogEntry"
      file_path: "In story template"
      requirements:
        - id: "DM-001"
          description: "Markdown table row with 5 columns (Date, Author, Phase/Action, Change, Files Affected)"
          testable: true
          test_requirement: "Each column parseable from story file"
          priority: "Critical"
        - id: "DM-002"
          description: "Author validation: matches pattern ^(claude/[a-z-]+|user/[a-zA-Z0-9_-]+|claude/opus)$"
          testable: true
          test_requirement: "Regex validates author field"
          priority: "High"
        - id: "DM-003"
          description: "Change field: max 100 characters for readability"
          testable: true
          test_requirement: "Long descriptions truncated with ellipsis"
          priority: "Medium"

    - type: "Service"
      name: "StoryTemplateUpdate"
      file_path: ".claude/skills/devforgeai-story-creation/assets/templates/story-template.md"
      requirements:
        - id: "SVC-001"
          description: "Replace ## Workflow Status section with ## Change Log"
          testable: true
          test_requirement: "Template contains '## Change Log' header, not '## Workflow Status'"
          priority: "Critical"
        - id: "SVC-002"
          description: "Include Current Status field and initial table structure"
          testable: true
          test_requirement: "Template contains '**Current Status:** Backlog' and table headers"
          priority: "Critical"
        - id: "SVC-003"
          description: "Update template version to 2.5"
          testable: true
          test_requirement: "Template changelog shows v2.5 entry"
          priority: "High"

    - type: "Service"
      name: "DevSkillChangelogIntegration"
      file_path: ".claude/skills/devforgeai-development/SKILL.md"
      requirements:
        - id: "DEV-001"
          description: "Add changelog append instruction after each TDD phase"
          testable: true
          test_requirement: "SKILL.md contains 'Append to ## Change Log' instruction at each phase"
          priority: "Critical"
        - id: "DEV-002"
          description: "Reference changelog-update-guide.md for format consistency"
          testable: true
          test_requirement: "SKILL.md contains Read() call to changelog guide"
          priority: "High"
        - id: "DEV-003"
          description: "Update dod-update-workflow.md Step 4 to use Change Log"
          testable: true
          test_requirement: "Step 4 edits '## Change Log' not '## Workflow Status'"
          priority: "Critical"

    - type: "Service"
      name: "QASkillChangelogIntegration"
      file_path: ".claude/skills/devforgeai-qa/SKILL.md"
      requirements:
        - id: "QA-001"
          description: "Add changelog append at Phase 3.4 (Story File Update)"
          testable: true
          test_requirement: "SKILL.md Phase 3.4 contains changelog append instruction"
          priority: "Critical"
        - id: "QA-002"
          description: "Include QA result, coverage, and violations in entry"
          testable: true
          test_requirement: "Changelog entry format includes '{result}: Coverage {pct}%'"
          priority: "High"

    - type: "Service"
      name: "ReleaseSkillChangelogIntegration"
      file_path: ".claude/skills/devforgeai-release/SKILL.md"
      requirements:
        - id: "REL-001"
          description: "Add changelog append at Phase 5 Step 2"
          testable: true
          test_requirement: "SKILL.md Phase 5 contains changelog append instruction"
          priority: "Critical"
        - id: "REL-002"
          description: "Archive story to devforgeai/specs/Stories/archive/"
          testable: true
          test_requirement: "release-documentation.md contains archive step"
          priority: "High"
        - id: "REL-003"
          description: "Update project CHANGELOG.md with story reference"
          testable: true
          test_requirement: "Release workflow updates CHANGELOG.md"
          priority: "High"

    - type: "Repository"
      name: "ProjectChangelog"
      file_path: "CHANGELOG.md"
      create: true
      requirements:
        - id: "REPO-001"
          description: "Keep a Changelog v1.1.0 compliant format"
          testable: true
          test_requirement: "CHANGELOG.md contains [Unreleased] section header"
          priority: "Critical"
        - id: "REPO-002"
          description: "Story ID references with links to archive paths"
          testable: true
          test_requirement: "Links follow format [STORY-XXX]: devforgeai/specs/Stories/archive/..."
          priority: "High"

  business_rules:
    - id: "BR-001"
      description: "Every story file edit by a skill must append a changelog entry"
      enforcement: "Skill workflow instructions"
      test_requirement: "Run /dev, verify changelog entries for each phase"
    - id: "BR-002"
      description: "Author attribution must identify specific subagent, not generic 'claude'"
      enforcement: "Changelog guide validation"
      test_requirement: "No entries with author 'claude' (must be claude/{subagent})"
    - id: "BR-003"
      description: "Existing stories without Change Log get section on first edit"
      enforcement: "Backward compatibility check in each skill"
      test_requirement: "Edit old story, verify Change Log section created"

  non_functional_requirements:
    - id: "NFR-001"
      category: "Performance"
      description: "Change Log append operation < 100ms per append"
      metric: "File read + table row append + file write time"
      threshold: "100ms"
    - id: "NFR-002"
      category: "Maintainability"
      description: "Single source of truth for changelog format"
      metric: "Number of places defining changelog format"
      threshold: "1 (changelog-update-guide.md only)"
    - id: "NFR-003"
      category: "Scalability"
      description: "Story file size impact < 2KB for Change Log section"
      metric: "Size of Change Log section with 50 entries"
      threshold: "< 2KB"
```

---

## Test Strategy

### Unit Tests

**Coverage Target:** 95% for changelog logic

**Test Cases:**

1. **test_changelog_entry_format** - Verify entry matches expected format
2. **test_author_validation_valid** - Accept valid author patterns
3. **test_author_validation_invalid** - Reject invalid author patterns
4. **test_backward_compat_migration** - Verify old stories get Change Log
5. **test_current_status_update** - Verify status field updates correctly
6. **test_changelog_append_order** - Verify entries in chronological order

### Integration Tests

**Coverage Target:** 85%

**Test Scenarios:**

1. **test_dev_workflow_changelog** - Run /dev, verify all phase entries
2. **test_qa_workflow_changelog** - Run /qa, verify QA result entry
3. **test_release_workflow_changelog** - Run /release, verify archive and CHANGELOG.md
4. **test_full_lifecycle** - Create → Dev → QA → Release, verify complete changelog

---

## Acceptance Criteria Verification Checklist

### AC#1: Story Template Updated with Change Log Section

- [ ] Template contains `## Change Log` section - **Phase:** 02 - **Evidence:** story-template.md
- [ ] `## Workflow Status` section removed - **Phase:** 02 - **Evidence:** grep returns no match
- [ ] Initial entry format correct - **Phase:** 02 - **Evidence:** template validation test

### AC#2: Shared Changelog Reference Guide Created

- [ ] File created at `.claude/references/changelog-update-guide.md` - **Phase:** 02 - **Evidence:** file exists
- [ ] Contains format specification - **Phase:** 02 - **Evidence:** content validation
- [ ] Contains author pattern regex - **Phase:** 02 - **Evidence:** grep for regex pattern

### AC#3: devforgeai-development Skill Appends Changelog Entries

- [ ] SKILL.md updated with changelog append logic - **Phase:** 03 - **Evidence:** grep SKILL.md
- [ ] dod-update-workflow.md Step 4 updated - **Phase:** 03 - **Evidence:** content check
- [ ] Each phase has author attribution - **Phase:** 03 - **Evidence:** skill review

### AC#4: devforgeai-qa Skill Appends Changelog Entry

- [ ] Phase 3.4 updated with changelog append - **Phase:** 03 - **Evidence:** grep SKILL.md
- [ ] QA result format documented - **Phase:** 03 - **Evidence:** content check

### AC#5: devforgeai-release Skill Appends Changelog and Archives Story

- [ ] SKILL.md updated with changelog append - **Phase:** 03 - **Evidence:** grep SKILL.md
- [ ] Archive workflow documented - **Phase:** 03 - **Evidence:** release-documentation.md
- [ ] CHANGELOG.md update logic added - **Phase:** 03 - **Evidence:** content check

### AC#6: Project CHANGELOG.md Created with Keep a Changelog Format

- [ ] CHANGELOG.md template created - **Phase:** 03 - **Evidence:** file exists
- [ ] Keep a Changelog format verified - **Phase:** 05 - **Evidence:** format validation

### AC#7: Backward Compatible with Existing Stories

- [ ] Migration logic documented in guide - **Phase:** 02 - **Evidence:** guide content
- [ ] Skills check for missing section - **Phase:** 03 - **Evidence:** skill logic review
- [ ] Test with existing story passes - **Phase:** 05 - **Evidence:** integration test

---

## Definition of Done

### Implementation
- [ ] Shared changelog reference guide created at `.claude/references/changelog-update-guide.md`
- [ ] Story template updated: `## Workflow Status` replaced with `## Change Log`
- [ ] Template version incremented to 2.5 with changelog entry
- [ ] devforgeai-story-creation SKILL.md references changelog guide
- [ ] devforgeai-development SKILL.md updated with changelog append at each phase
- [ ] dod-update-workflow.md Step 4 updated to use Change Log
- [ ] devforgeai-qa SKILL.md updated with changelog append at Phase 3.4
- [ ] devforgeai-release SKILL.md updated with changelog append and archive workflow
- [ ] release-documentation.md updated with archive step
- [ ] source-tree.md updated with archive/ directory
- [ ] Project CHANGELOG.md created with Keep a Changelog format

### Quality
- [ ] All 7 acceptance criteria have passing tests
- [ ] Edge cases covered (backward compatibility, missing section)
- [ ] Author pattern validation enforced
- [ ] NFRs met (append < 100ms, single source of truth)
- [ ] Code coverage >95% for changelog logic

### Testing
- [ ] Unit tests for changelog entry format
- [ ] Unit tests for author validation
- [ ] Integration test for /dev workflow
- [ ] Integration test for /qa workflow
- [ ] Integration test for /release workflow
- [ ] Backward compatibility test with existing story

### Documentation
- [ ] Changelog guide documents all formats and patterns
- [ ] Template changelog documents v2.5 changes
- [ ] Skills reference the shared guide

---

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2025-12-24 | claude/story-requirements-analyst | Created | Story created | STORY-152.story.md |
| 2025-12-24 | claude/story-requirements-analyst | Backlog | Initial status | - |

---

## Notes

**Design Decisions:**
- Unified section chosen over separate Workflow Status + Change Log (per user preference)
- Shared reference file prevents format duplication across 4 skills
- Keep a Changelog format for project CHANGELOG.md (industry standard)

**Related Plan:**
- `.claude/plans/refactored-bouncing-widget.md` - Complete implementation plan

**References:**
- [Keep a Changelog](https://keepachangelog.com/en/1.1.0/)
- STORY-131 (showed inconsistent Status History implementation)
