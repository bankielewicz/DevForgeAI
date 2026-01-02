---
id: STORY-167
title: "RCA-012 Story Template Version Tracking"
type: enhancement
priority: High
points: 1
status: Backlog
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
- [ ] Template version metadata added to story template
- [ ] Changelog documenting versions 1.0, 2.0, 2.1
- [ ] Generated stories include format_version: "2.1"
- [ ] Both .claude/ and src/claude/ versions updated

### Testing
- [ ] Generate new story with `/create-story`
- [ ] Verify format_version: "2.1" in YAML frontmatter
- [ ] Compare with existing stories (should show version difference)

### Documentation
- [ ] RCA-012 updated with implementation status

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
<!-- Filled in by devforgeai-development skill -->
*To be completed during development*

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-12-31 | /create-stories-from-rca | Story created from RCA-012 REC-3 |
