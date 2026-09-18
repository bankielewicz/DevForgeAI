---
id: STORY-TEST-V31
title: Compliant v3.1 illustrative example
type: feature
epic: EPIC-TEST
sprint: Backlog
status: Backlog
points: 3
depends_on: []
priority: Medium
advisory: false
source_gap: null
source_story: null
from_recommendations: false
source_recommendations: null
cycle_recorded: null
assigned_to: Test
created: 2026-04-22
format_version: "3.1"
---

# Story: Compliant v3.1 Illustrative Example

> **Reference example** for `template-version-validation.md` Worked Example 3. Fully compliant with template v3.1 — used to demonstrate idempotency. Expected detection: ZERO `template/*` findings (idempotency filter fires before any detection rule runs).

## Description

**As a** developer,
**I want** a fully-compliant test reference,
**so that** idempotency of the template-version validator can be verified.

## Provenance

```xml
<provenance>
  <origin document="BRAINSTORM-TEST" section="goals">
    <quote>"Verify the validator emits zero findings on a compliant story"</quote>
    <line_reference>lines 1-3</line_reference>
    <quantified_impact>Idempotency check: re-running /validate-stories produces no new findings</quantified_impact>
  </origin>
</provenance>
```

## Acceptance Criteria

### AC#1: First criterion

```xml
<acceptance_criteria id="AC1">
  <given>A compliant story file</given>
  <when>/validate-stories Phase 2 is invoked</when>
  <then>Zero template/* findings are emitted</then>
  <verification>
    <source_files>
      <file>src/claude/skills/spec-driven-stories/references/template-version-validation.md</file>
    </source_files>
    <test_file>n/a (reference example, not a live test)</test_file>
  </verification>
</acceptance_criteria>
```

## Technical Specification

This is an illustrative reference example. The full technical specification of `/fix-story --upgrade` lives in `/home/bryan/.claude/plans/rippling-mixing-stallman.md`.

## Implementation Guide

### Architecture Decisions

The validator reads the canonical template's SECTION_MANIFEST at every Phase 2 invocation, never hardcoding the target version.

### Cross-Cutting Concerns

Pre-flight grandfather filter (status: QA Approved | Released) and idempotency filter (story_version >= canonical) short-circuit the scan before any detection rule runs.

### Implementation Sequence

Apply detection rules in order: Rule 1 (missing_section) -> Rule 2 (legacy_format) -> Rule 3 (derivable frontmatter) -> Rule 4 (ambiguous frontmatter) -> Rule 5 (legacy_workflow_status) -> Rule 6 (informal_dependency) -> Rule 7 (marker recognition flag) -> Rule Z (version_drift umbrella).

### Task Prompt Templates

None for this illustrative example.

### Anti-Patterns

None for this illustrative example.

### Patterns and References

See template-version-validation.md for the authoritative rules.

## Technical Limitations

```yaml
limitations: []
```

## Non-Functional Requirements (NFRs)

### Performance

Detection rules are O(story-size) per story; canonical template + manifest read once per Phase 2 invocation.

### Security

Read-only on story files during detection. Phase 03 fix application uses explicit Edit() with old_string/new_string.

### Scalability

Scales linearly with story count in scope. Bulk runs invoke /fix-story per audit file.

### Reliability

Each finding carries a verification check used by Phase 04. Failed verifications surface to user via AskUserQuestion.

### Observability

Findings recorded in audit file Section 4; checkpoint state persisted at tmp/.remediation-checkpoint-${SESSION_ID}.yaml.

## Dependencies

### Prerequisite Stories

None.

### External Dependencies

None.

### Technology Dependencies

None beyond standard Claude Code tools (Read, Edit, Write, Grep, AskUserQuestion).

## Test Strategy

### Unit Tests

N/A for an illustrative example.

### Integration Tests

N/A for an illustrative example. The plan §9 specifies a manual Phase 2 walk-through against this example to confirm zero findings.

## Acceptance Criteria Verification Checklist

**Real-time AC progress tracker. Update sub-items as TDD phases complete.**

- [ ] AC#1: First criterion
  - [ ] Red phase: failing test written
  - [ ] Green phase: implementation passing test
  - [ ] Refactor phase: code cleaned

## Edge Cases

(Not applicable for an illustrative example.)

## Definition of Done

### Implementation

- [ ] Implementation complete

### Quality

- [ ] Tests passing

### Testing

- [ ] Coverage threshold met

### Documentation

- [ ] Docs updated

## Change Log

**Current Status:** Backlog

| Date | Author | Phase/Action | Change | Files Affected |
|------|--------|--------------|--------|----------------|
| 2026-04-22 | test | Created | Example created for template-upgrade plan §3.4 | (this file) |

## Notes

Illustrative reference example for template-upgrade idempotency. Not part of the live story corpus.
