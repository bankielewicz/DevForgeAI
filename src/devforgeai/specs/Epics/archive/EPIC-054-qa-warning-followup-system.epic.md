---
id: EPIC-054
title: QA Warning Follow-up System
status: Planning
start_date: 2026-01-30
target_date: 2026-02-27
total_points: 21
created: 2026-01-30
updated: 2026-01-30
source_brainstorm: BRAINSTORM-008
source_requirements: qa-warning-followup-requirements.md
complexity_score: 28/60
complexity_tier: "Tier 2: Moderate"
priority: High
---

# Epic: QA Warning Follow-up System

## Business Goal

Eliminate silent technical debt accumulation by ensuring QA warnings (PASS WITH WARNINGS) are persisted, tracked, and actionable through the existing remediation workflow.

**Problem Statement:** DevForgeAI users experience lost QA warnings because gaps.json only captures blocking failures, resulting in untracked technical debt that accumulates silently until discovered in post-hoc report reviews.

**Evidence:**
- 3 of 5 analyzed QA reports had PASS WITH WARNINGS results
- All warnings required manual review to discover
- No structured data exists for remediation workflow
- God Module warnings (1098-line watcher.rs) had no follow-up mechanism

## Success Metrics

| Metric | Current | Target | Measurement |
|--------|---------|--------|-------------|
| Warning capture rate | 0% | 100% | gaps.json generation for PASS WITH WARNINGS |
| Manual discovery effort | 100% | 0% | `/review-qa-reports` shows all automatically |
| Advisory story clarity | N/A | 100% | `[ADVISORY]` prefix + frontmatter flag |
| Backward compatibility | N/A | 100% | Existing gaps.json files work unchanged |

## Scope

### Overview

Extend the gaps.json schema to include non-blocking warnings with a `blocking: boolean` field, enabling unified tracking and automated follow-up story creation through the existing `/review-qa-reports` command.

**Key Changes:**
1. gaps.json generated for ALL QA results (not just failures)
2. `blocking: boolean` field distinguishes severity
3. `/review-qa-reports` shows all gaps by default
4. Advisory stories clearly marked with `[ADVISORY]` prefix

### Features

1. **F1: Schema Extension**
   - Description: Add `blocking: boolean` field to gaps.json schema
   - User Value: Distinguish blocking failures from advisory warnings in structured data
   - Estimated Points: 3 story points

2. **F2: Gap Generation for Warnings**
   - Description: Generate gaps.json for PASS WITH WARNINGS results
   - User Value: Warnings persisted in structured format for remediation workflow
   - Estimated Points: 5 story points

3. **F3: Review Command Enhancement**
   - Description: Update `/review-qa-reports` default to show all gaps
   - User Value: Complete visibility into all QA findings without manual filtering
   - Estimated Points: 5 story points

4. **F4: Blocking Filter Flag**
   - Description: Add `--blocking-only` filter to `/review-qa-reports`
   - User Value: Focus on critical blockers when needed (backward compatible)
   - Estimated Points: 3 story points

5. **F5: Advisory Story Creation**
   - Description: Create advisory stories with `[ADVISORY]` prefix and `advisory: true` frontmatter
   - User Value: Clear identification of non-blocking follow-up work
   - Estimated Points: 5 story points

### Out of Scope

- Dashboard aggregation across stories (Won't Have - high effort, low value)
- Parsing existing markdown reports into gaps.json retroactively (Could Have - defer to future)
- Auto-remediation of warnings (requires separate epic)
- Real-time warning detection during development

## Target Sprints

**Estimated Duration:** 2 sprints / 4 weeks

**Sprint Breakdown:**
- **Sprint 1:** F1 (Schema Extension) + F2 (Gap Generation) - 8 story points
- **Sprint 2:** F3 (Default Show All) + F4 (Filter Flag) + F5 (Advisory Stories) - 13 story points

## Dependencies

### External Dependencies
- None

### Internal Dependencies
- Builds on existing devforgeai-qa skill
- Builds on existing devforgeai-qa-remediation skill
- Builds on existing /review-qa-reports command

### Blocking Issues
- None identified

## Stakeholders

- **Primary User:** Framework developer using DevForgeAI for project development
- **Secondary User:** Framework maintainer developing DevForgeAI itself

## Requirements

### Functional Requirements

#### User Stories

**FR-01: Gap Generation for Warnings**
```
As a developer,
I want gaps.json generated for PASS WITH WARNINGS results,
So that warnings are persisted for follow-up.
```

**Acceptance Criteria:**
- [ ] QA skill generates gaps.json when result is PASS WITH WARNINGS
- [ ] All warning items include `blocking: false` field
- [ ] gaps.json written to `devforgeai/qa/reports/{STORY-ID}-gaps.json`

**FR-02: Schema Extension**
```
As a developer,
I want a `blocking: boolean` field in gaps.json,
So that I can distinguish failures from advisories.
```

**Acceptance Criteria:**
- [ ] Gap schema includes optional `blocking` field (default: true)
- [ ] CRITICAL/HIGH blocking violations have `blocking: true`
- [ ] Non-blocking warnings have `blocking: false`
- [ ] Existing gaps.json files without field work unchanged

**FR-03: Review Command Default**
```
As a developer,
I want `/review-qa-reports` to show all gaps by default,
So that I see the full picture.
```

**Acceptance Criteria:**
- [ ] Default behavior shows both blocking and advisory gaps
- [ ] Clear visual distinction between blocking (🔴) and advisory (🟡)
- [ ] Gap count summary includes breakdown

**FR-04: Blocking Filter Flag**
```
As a developer,
I want to filter gaps by `--blocking-only`,
So that I can focus on blockers when needed.
```

**Acceptance Criteria:**
- [ ] `--blocking-only` flag filters to `blocking: true` gaps only
- [ ] Flag is optional (default shows all)
- [ ] Matches legacy behavior for existing workflows

**FR-05: Advisory Story Creation**
```
As a developer,
I want advisory stories marked with [ADVISORY] prefix and advisory: true frontmatter,
So that they're clearly identified.
```

**Acceptance Criteria:**
- [ ] Story title includes `[ADVISORY]` prefix
- [ ] Frontmatter includes `advisory: true` field
- [ ] Frontmatter includes `source_gap` and `source_story` fields
- [ ] Advisory stories default to `priority: low`

### Non-Functional Requirements

#### Performance
- Gap generation should add <1 second to QA workflow
- `/review-qa-reports` should complete in <5 seconds for 100 stories

#### Backward Compatibility (CRITICAL)
- Existing gaps.json files must work unchanged
- Missing `blocking` field defaults to `true`
- Existing `/review-qa-reports` workflows continue to function

#### Usability
- Clear visual distinction between blocking and advisory gaps
- Consistent prefix `[ADVISORY]` for easy scanning
- Filter flags for focused workflows

### Data Requirements

#### Entity: gaps.json Schema Extension

**Current Schema:**
```json
{
  "story_id": "STORY-XXX",
  "gaps": [
    {
      "id": "GAP-001",
      "severity": "CRITICAL",
      "category": "coverage",
      "description": "...",
      "file": "src/module.py",
      "line": 42
    }
  ]
}
```

**Proposed Schema:**
```json
{
  "story_id": "STORY-XXX",
  "qa_result": "PASS WITH WARNINGS",
  "created": "2026-01-30T10:00:00Z",
  "gaps": [
    {
      "id": "GAP-001",
      "severity": "HIGH",
      "category": "anti-pattern",
      "description": "God Module violation (1098 lines > 500 threshold)",
      "file": "src/watcher.rs",
      "line": 1,
      "blocking": false
    }
  ]
}
```

#### Entity: Story Frontmatter Extension

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| advisory | boolean | No | false | Story is advisory (non-blocking) |
| source_gap | string | No | - | Gap ID that created this story |
| source_story | string | No | - | Story where gap was found |

### Integration Requirements

| Component | Change Required | Impact |
|-----------|-----------------|--------|
| devforgeai-qa/SKILL.md | Generate gaps.json for PASS WITH WARNINGS | Medium |
| devforgeai-qa-remediation/SKILL.md | Handle `blocking: false` gaps | Low |
| /review-qa-reports command | New default, filter flag | Medium |
| Story template | Advisory frontmatter | Low |

## Architecture Considerations

### Complexity Tier
**Tier 2: Moderate Application**
- **Score:** 28/60 points from complexity assessment
- **Rationale:** Multiple skill/command modifications, schema evolution with backward compatibility, integration testing required

### Recommended Architecture Pattern
Schema extension with backward-compatible defaults. Builds on existing QA and remediation workflow patterns.

### Technology Constraints
- No new dependencies (per dependencies.md)
- JSON schema extension only
- Uses existing framework patterns

## Risks & Constraints

### Technical Risks

**Risk 1: Backward Compatibility Break**
- **Description:** Existing gaps.json files may not work with new parsing logic
- **Probability:** Low
- **Impact:** High
- **Mitigation:** Default `blocking: true` for missing field; comprehensive testing

**Risk 2: Advisory Story Noise**
- **Description:** Too many advisory stories could clutter backlog
- **Probability:** Low
- **Impact:** Medium
- **Mitigation:** Auto-create is optional flag, not default

### Business Risks

**Risk 1: Default Change Confusion**
- **Description:** Users expecting old behavior may be surprised by new default
- **Probability:** Medium
- **Impact:** Low
- **Mitigation:** Document clearly in changelog; provide `--blocking-only` flag

### Constraints

**Constraint 1: Backward Compatibility**
- **Description:** Existing gaps.json files must continue to work unchanged
- **Impact:** Schema changes must be additive only
- **Mitigation:** Optional field with sensible default

**Constraint 2: No New Dependencies**
- **Description:** Must use existing framework patterns (per tech-stack.md)
- **Impact:** Cannot add external JSON schema validators
- **Mitigation:** Use existing JSON handling patterns

## Assumptions

1. **A1:** Users will create follow-up stories from warnings (track creation rate post-release)
2. **A2:** Unified file easier to maintain than separate files for warnings vs failures
3. **A3:** Show all by default improves discovery (validate with user feedback)

## Story Breakdown

### Planned Stories

| Story ID | Title | Points | Sprint | Depends On |
|----------|-------|--------|--------|------------|
| STORY-344 | Extend gaps.json schema with blocking field | 3 | 1 | None |
| STORY-345 | Generate gaps.json for PASS WITH WARNINGS | 5 | 1 | STORY-344 |
| STORY-346 | Update /review-qa-reports default to show all | 5 | 2 | STORY-345 |
| STORY-347 | Add --blocking-only filter to /review-qa-reports | 3 | 2 | STORY-346 |
| STORY-348 | Create advisory stories with ADVISORY prefix | 5 | 2 | STORY-346 |

### Story Dependencies

```
STORY-344 (Schema Extension)
    │
    └──► STORY-345 (Gap Generation)
             │
             └──► STORY-346 (Default Show All)
                      │
                      ├──► STORY-347 (Blocking Filter)
                      │
                      └──► STORY-348 (Advisory Stories)
```

## Next Steps

### Immediate Actions
1. Create detailed stories using `/create-story` for each feature
2. Create sprint plan using `/create-sprint`
3. Begin development with schema extension story

### Pre-Development Checklist
- [x] Epic created with full requirements
- [x] Brainstorm session complete (BRAINSTORM-008)
- [x] Requirements specification approved
- [x] Stories created with acceptance criteria (5/5 complete)
- [ ] Sprint 1 planned and scheduled

### Development Workflow
Stories will progress through:
1. **Ready for Dev** → devforgeai-development (TDD implementation)
2. **Dev Complete** → devforgeai-qa (quality validation)
3. **QA Approved** → devforgeai-release (deployment)

## Related Documents

- **Source Brainstorm:** `devforgeai/specs/brainstorms/BRAINSTORM-008-qa-warning-followup.brainstorm.md`
- **Requirements Spec:** `devforgeai/specs/requirements/qa-warning-followup-requirements.md`
- **QA Skill:** `.claude/skills/devforgeai-qa/SKILL.md`
- **QA Remediation Skill:** `.claude/skills/devforgeai-qa-remediation/SKILL.md`
- **Review Command:** `.claude/commands/review-qa-reports.md`
- **Anti-Patterns:** `devforgeai/specs/context/anti-patterns.md`

---

## Change Log

| Date | Change | Author |
|------|--------|--------|
| 2026-01-30 | Epic created from BRAINSTORM-008 and requirements specification | /create-epic |
| 2026-01-30 | STORY-344 created (Extend gaps.json schema with blocking field) | /create-story |
| 2026-01-30 | STORY-345 created (Generate gaps.json for PASS WITH WARNINGS) | /create-story |
| 2026-01-30 | STORY-346 created (Update /review-qa-reports default to show all) | /create-story |
| 2026-01-30 | STORY-347 created (Add --blocking-only filter to /review-qa-reports) | /create-story |
| 2026-01-30 | STORY-348 created (Create advisory stories with ADVISORY prefix) | /create-story |
