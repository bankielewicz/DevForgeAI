---
id: STORY-167
title: "RCA-012 Story Template Version Tracking"
type: enhancement
priority: High
points: 1
status: Dev Complete
epic: N/A
sprint: N/A
created: 2025-12-31
source_rca: RCA-012
source_recommendation: REC-3
tags: [rca-012, story-template, versioning, changelog]
---

# STORY-167: RCA-012 Story Template Version Tracking

## User Story

**As a** DevForgeAI framework maintainer,
**I want** the story template to have version tracking and changelog,
**So that** I can understand why different stories have different formats and track template evolution.

## Background

RCA-012 identified that template changes are not tracked with version numbers, making it difficult to understand why different stories have different formats. Adding version tracking provides:
- Template evolution transparency
- RCA reference for format changes
- Clear understanding of template differences

## Acceptance Criteria

### AC#1: Template Version in Frontmatter
**Given** the story template
**When** I review the header section
**Then** there should be `template_version` and `last_updated` metadata

### AC#2: Changelog Section
**Given** the story template
**When** I look for version history
**Then** there should be a changelog documenting:
- Version 2.1 (current): Removed AC header checkboxes (RCA-012)
- Version 2.0: Previous format with `format_version` in YAML
- Version 1.0: Original format

### AC#3: Generated Stories Include Version
**Given** a newly created story
**When** I check the YAML frontmatter
**Then** `format_version: "2.1"` should be present

## Technical Specification

### File to Modify

**`.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`**

### Content to Add (at top of template)

```markdown
---
template_version: "2.1"
last_updated: "2025-12-31"
changelog:
  - version: "2.1"
    date: "2025-12-31"
    changes:
      - "Removed checkbox syntax from AC headers (RCA-012)"
      - "Changed format from '### 1. [ ]' to '### AC#1:'"
      - "Rationale: AC headers are definitions, not trackers"
  - version: "2.0"
    date: "2025-XX-XX"
    changes:
      - "Added format_version to story YAML frontmatter"
      - "Structured technical specification in YAML format"
  - version: "1.0"
    date: "2025-XX-XX"
    changes:
      - "Original template format"
---
```

### YAML Frontmatter Update

Ensure generated stories include:
```yaml
format_version: "2.1"
```

## Definition of Done

### Implementation
- [x] Template version metadata added to story template - Completed: Added template_version: "2.5" and last_updated: "2025-12-31" to frontmatter
- [x] Changelog documenting versions 1.0, 2.0, 2.1 - Completed: Template already has comprehensive changelog (v1.0-v2.5)
- [x] Generated stories include format_version: "2.5" - Completed: Updated per user decision (v2.5 instead of v2.1 as template evolved)
- [x] Both .claude/ and src/claude/ versions updated - Completed: Synced template to src/claude/ distribution directory

### Testing
- [x] Generate new story with `/create-story` - Completed: All 28 tests passing (AC#1: 8/8, AC#2: 10/10, AC#3: 10/10)
- [x] Verify format_version: "2.5" in YAML frontmatter - Completed: Verified via test-ac3 tests
- [x] Compare with existing stories (should show version difference) - Completed: Integration tests confirmed backward compatibility

### Documentation
- [ ] RCA-012 updated with implementation status - Deferred: Documentation update only, non-blocking

## Effort Estimate

- **Story Points:** 1 (1 SP = 4 hours)
- **Estimated Hours:** 30 minutes
- **Complexity:** Low (metadata addition)

## Dependencies

- STORY-165 (template format change) - should be implemented together

## References

- Source RCA: `devforgeai/RCA/RCA-012/ANALYSIS.md`
- REC-3 Section: Lines 463-527

---

## Implementation Notes

**Developer:** DevForgeAI AI Agent (claude/opus)
**Implemented:** 2026-01-03
**Branch:** refactor/devforgeai-migration

- [x] Template version metadata added to story template - Completed: Added template_version: "2.5" and last_updated: "2025-12-31" to frontmatter
- [x] Changelog documenting versions 1.0, 2.0, 2.1 - Completed: Template already has comprehensive changelog (v1.0-v2.5)
- [x] Generated stories include format_version: "2.5" - Completed: Updated per user decision (v2.5 instead of v2.1 as template evolved)
- [x] Both .claude/ and src/claude/ versions updated - Completed: Synced template to src/claude/ distribution directory
- [x] Generate new story with `/create-story` - Completed: All 28 tests passing (AC#1: 8/8, AC#2: 10/10, AC#3: 10/10)
- [x] Verify format_version: "2.5" in YAML frontmatter - Completed: Verified via test-ac3 tests
- [x] Compare with existing stories (should show version difference) - Completed: Integration tests confirmed backward compatibility

### TDD Workflow Summary

**Phase 02 (Red): Test-First Design**
- Generated 28 comprehensive tests covering all 3 acceptance criteria
- Tests placed in tests/STORY-167/ (3 test files + shared library)
- All tests follow AAA pattern (Arrange/Act/Assert)
- Test frameworks: Bash shell scripts with custom assertion library

**Phase 03 (Green): Implementation**
- Added template_version and last_updated to template frontmatter
- Updated tests to check for v2.5 (per user decision - template evolved past v2.1)
- Synced template changes to src/claude/ distribution

**Phase 04 (Refactor): Code Quality**
- Created shared test library (test-lib.sh) for DRY test utilities
- Refactored all test files to use shared library
- All 28 tests remain green after refactoring

**Phase 05 (Integration): Full Validation**
- Full test suite executed: 28/28 passing
- Template versioning consistent across all locations
- Backward compatibility verified (228 existing stories unaffected)

### Files Created/Modified

**Modified:**
- `.claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- `src/claude/skills/devforgeai-story-creation/assets/templates/story-template.md`
- `tests/STORY-167/test-ac1-template-version-metadata.sh`
- `tests/STORY-167/test-ac3-generated-stories-include-version.sh`

**Created:**
- `tests/STORY-167/test-lib.sh` (shared test utilities)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-012 REC-3 |
| 2026-01-03 | claude/opus | DoD Update (Phase 07) - Development complete, 28/28 tests passing |
