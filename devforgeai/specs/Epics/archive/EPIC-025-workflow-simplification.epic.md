---
id: EPIC-025
title: Workflow Simplification
business-value: Reduce TDD workflow complexity through template extraction and story-type-aware processing
status: Planning
priority: High
complexity-score: 8
architecture-tier: Tier 2 (Standard Application)
created: 2025-12-20
estimated-points: 8
target-sprints: 1
research-reference: STORY-114 observations
related-epics: [EPIC-024]
stories: [STORY-125, STORY-126]
---

# Workflow Simplification

## Business Goal

Reduce complexity in the DevForgeAI TDD workflow by extracting reusable templates from verbose documentation and implementing story-type-aware phase skipping. This addresses observations from STORY-114 development session where documentation-only stories executed unnecessary runtime test phases.

**Success Metrics:**
- Template extraction: 768-line dod-update-workflow.md references 20-line template
- Story type detection: Documentation stories skip integration phase
- Backward compatibility: 100% existing workflows continue to pass
- Developer efficiency: Reduced cognitive load when following TDD workflow

## Features

### Feature 1: DoD Template Extraction (STORY-125)
**Description:** Extract the core Implementation Notes pattern from the verbose dod-update-workflow.md (768 lines) into a minimal template (~20 lines) that can be referenced and validated.

**User Stories (high-level):**
1. As a developer, I want a simple template for Implementation Notes so I don't need to read 768 lines
2. As a developer, I want pre-commit validation against the template format
3. As a developer, I want existing workflows to continue working unchanged

**Estimated Effort:** 3 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| CREATE | `.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md` | Minimal template (~20 lines) |
| MODIFY | `.claude/skills/devforgeai-development/references/dod-update-workflow.md` | Reference the template, reduce duplication |

**Template Structure:**
```markdown
## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** {DATE}
**Branch:** {BRANCH}

### Definition of Done Status

- [x] {item text} - Completed: {evidence}
- [ ] {item text} - Deferred: {justification} (See: {STORY-XXX})
```

**Acceptance Criteria Themes:**
- AC#1: Template file created at specified path (~20 lines max)
- AC#2: dod-update-workflow.md references template for format
- AC#3: Pre-commit hook validates against template format
- AC#4: Existing workflows continue to pass validation

### Feature 2: Story Type Detection & Phase Skipping (STORY-126)
**Description:** Add `type` field to story frontmatter (feature, documentation, bugfix, refactor) with automatic phase skipping based on story type.

**User Stories (high-level):**
1. As a developer, I want documentation stories to skip integration testing
2. As a developer, I want bugfix stories to skip refactoring phase
3. As a developer, I want clear logging when phases are skipped

**Estimated Effort:** 5 story points

**Files to Create/Modify:**
| Action | File Path | Purpose |
|--------|-----------|---------|
| MODIFY | `.claude/skills/devforgeai-story-creation/SKILL.md` | Add type field to story template |
| MODIFY | `.claude/skills/devforgeai-development/SKILL.md` | Add phase-skipping logic based on type |
| MODIFY | `devforgeai/specs/context/coding-standards.md` | Document story types |

**Story Types:**
| Type | Skip Phases | Rationale |
|------|-------------|-----------|
| `feature` | None | Full TDD workflow |
| `documentation` | Phase 05 Integration | No runtime code to test |
| `bugfix` | Phase 04 Refactor | Minimal changes, fix only |
| `refactor` | Phase 02 Red | Tests already exist |

**Acceptance Criteria Themes:**
- AC#1: Story frontmatter supports `type` field (enum: feature, documentation, bugfix, refactor)
- AC#2: /create-story prompts for story type during creation
- AC#3: /dev skips appropriate phases based on story type
- AC#4: Skipped phases logged with reason
- AC#5: Default type is `feature` if not specified (backward compatible)

## Requirements Summary

### Functional Requirements

| ID | Requirement | Priority | Story |
|----|-------------|----------|-------|
| FR-1 | Implementation notes template extracted to separate file | HIGH | STORY-125 |
| FR-2 | dod-update-workflow.md references template instead of inline definition | HIGH | STORY-125 |
| FR-3 | Story frontmatter supports type field with 4 enum values | HIGH | STORY-126 |
| FR-4 | /dev command skips phases based on story type | HIGH | STORY-126 |
| FR-5 | /create-story prompts for story type selection | MEDIUM | STORY-126 |

### Non-Functional Requirements

| ID | Requirement | Target | Story |
|----|-------------|--------|-------|
| NFR-1 | Template file size | <25 lines | STORY-125 |
| NFR-2 | Backward compatibility | 100% existing stories work | STORY-126 |
| NFR-3 | Phase skip logging | Clear console message for each skipped phase | STORY-126 |

## Technical Approach

### Template Reference Pattern
```markdown
<!-- In dod-update-workflow.md -->
## Implementation Notes Format

See template: `.claude/skills/devforgeai-development/assets/templates/implementation-notes-template.md`

Use this template to structure your Implementation Notes section.
```

### Phase Skipping Implementation
```python
# Pseudocode for phase skipping logic
PHASE_SKIP_MAP = {
    "documentation": ["Phase 05 Integration"],
    "bugfix": ["Phase 04 Refactor"],
    "refactor": ["Phase 02 Red"],
    "feature": []  # All phases required
}

def should_skip_phase(story_type: str, phase_name: str) -> bool:
    return phase_name in PHASE_SKIP_MAP.get(story_type, [])
```

## Dependencies

- None external
- STORY-126 benefits from STORY-125 patterns but not blocked by it

## Risks & Mitigations

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| Story type enum needs expansion | Medium | Low | Start with 4 types, add via ADR if needed |
| Template validation too strict | Low | Medium | Include escape hatch for edge cases |
| Phase skip causes test gaps | Low | High | Document when to override default type |

## Sprint Allocation

**Sprint-8 or Sprint-9 (8 points):**
- STORY-125: DoD Template Extraction (3 pts)
- STORY-126: Story Type Detection & Phase Skipping (5 pts)

## Definition of Done

### Epic-Level Completion Criteria
- [ ] Both stories reach Released status
- [ ] Implementation notes template validated by pre-commit hook
- [ ] Story type detection tested with all 4 types
- [ ] Phase skipping logged correctly for non-feature stories
- [ ] Backward compatibility verified with existing stories
