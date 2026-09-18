---
id: STORY-TEST-V27
title: Mid-evolution v2.7 illustrative example
epic: EPIC-TEST
sprint: Backlog
status: Backlog
points: 5
depends_on: []
priority: Medium
assigned_to: Test
created: 2026-01-21
format_version: "2.7"
---

# Story: Mid-Evolution v2.7 Illustrative Example

> **Reference example** for `template-version-validation.md` Worked Example 2. Has Provenance (added in v2.7) but still uses markdown AC, lacks Implementation Guide (added in v3.0), and lacks v3.1 frontmatter fields. Expected detection: ~16 `template/*` findings.

## Description

**As a** developer,
**I want** a mid-evolution-format story,
**so that** drift between v2.7 and v3.1 can be detected with partial-section coverage.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-TEST" section="goals">
    <quote>"Test the v2.7 to v3.1 delta"</quote>
    <line_reference>lines 1-3</line_reference>
    <quantified_impact>Detects ~9 missing sections, ~7 missing frontmatter fields, 2 markdown ACs</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC1: First criterion

**Given** condition A is met,
**When** event B occurs,
**Then** outcome C is observed.

### AC2: Second criterion

**Given** condition X is met,
**When** event Y occurs,
**Then** outcome Z is observed.

## Definition of Done

- [ ] Implementation complete
- [ ] Tests passing
- [ ] Documentation updated

## Notes

Illustrative reference example for the template-upgrade detection rules. Not part of the live story corpus.
