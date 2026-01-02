---
id: STORY-219
title: Create Shared Reference Document Auto-Load Utility
type: enhancement
epic: EPIC-033
priority: MEDIUM
points: 2
status: Backlog
created: 2025-01-01
source: RCA-021 REC-5
depends_on:
  - STORY-215
---

# STORY-219: Create Shared Reference Document Auto-Load Utility

## User Story

**As a** DevForgeAI skill developer,
**I want** a shared utility for Phase 0 reference file loading,
**So that** all skills follow a consistent pattern and new skills don't reinvent the loading logic.

## Background

RCA-021 identified that multiple skills require loading reference files in Phase 0, but this pattern is not automated. Each skill duplicates the logic. A shared utility eliminates code duplication and standardizes the reference loading pattern across the framework.

**Source RCA:** `devforgeai/RCA/RCA-021-qa-skill-phases-skipped.md`

**Benefits:**
- Eliminates code duplication across skills
- Standardizes Phase 0 Step 0.N implementation
- Single source of truth for reference loading
- Easy to add new skills without reinventing pattern

## Acceptance Criteria

### AC-1: Shared Utility File Created

**Given** the need for consistent reference loading
**When** the utility is created
**Then** it exists at `.claude/skills/shared-phase-0-loader.md`

---

### AC-2: Utility Supports devforgeai-qa

**Given** the utility file
**When** called with skill_name="devforgeai-qa" and mode="deep"
**Then** it loads `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md`

---

### AC-3: Utility Supports devforgeai-development

**Given** the utility file
**When** called with skill_name="devforgeai-development" and mode="deep"
**Then** it loads `.claude/skills/devforgeai-development/references/tdd-deep-workflow.md` (if exists)

---

### AC-4: Consistent Pattern Documented

**Given** the utility file
**When** loading references for any skill
**Then** the pattern is:
```
IF skill == "devforgeai-{X}" AND mode == "deep":
    reference_path = ".claude/skills/devforgeai-{X}/references/{X}-deep-workflow.md"
    Read(file_path=reference_path)
    Display: "✓ {X} deep mode workflow reference loaded"
```

---

### AC-5: Light Mode Support

**Given** the utility file
**When** mode="light"
**Then** either:
- No reference files loaded (light workflow inline in SKILL.md), OR
- Light-specific reference file loaded if exists

## Technical Specification

### Files to Create

| File | Description |
|------|-------------|
| `.claude/skills/shared-phase-0-loader.md` | Reusable Phase 0 reference loading utility |

### File Location

Per source-tree.md: `.claude/skills/` is the correct location for skill-related utilities.

### Utility File Content

```markdown
# Shared Phase 0 Reference Loader

Reusable utility for loading phase workflow reference files in Phase 0 setup.

## Usage Pattern

Each skill's Phase 0 should call this loader:

```
Skill: Reference file loading for Phase 0
Params:
  skill_name: "devforgeai-qa"  // or any skill name
  mode: "deep"  // "light" or "deep"

Execute: Load appropriate reference files
```

## Implementation

Load based on skill and mode:

**devforgeai-qa:**
- Light mode: No reference files (light workflow inline in SKILL.md)
- Deep mode: Load `.claude/skills/devforgeai-qa/references/deep-validation-workflow.md`

**devforgeai-development:**
- Light mode: Load `.claude/skills/devforgeai-development/references/tdd-light-workflow.md` (if exists)
- Deep mode: Load `.claude/skills/devforgeai-development/references/tdd-deep-workflow.md`

**Pattern:**
```
IF skill == "devforgeai-{X}" AND mode == "deep":
    reference_path = ".claude/skills/devforgeai-{X}/references/{X}-deep-workflow.md"
    Read(file_path=reference_path)
    Display: "✓ {X} deep mode workflow reference loaded"
```

## Benefits

- Eliminates code duplication across skills
- Standardizes Phase 0 Step 0.N implementation
- Single source of truth for reference loading
- Easy to add new skills without reinventing pattern

## Future Skills

When creating new skill, use this pattern:
1. Create `references/{skill-name}-deep-workflow.md`
2. In Phase 0 Step 0.N, call the loader utility
3. No need to duplicate Read/Load logic
```

### Skill Updates Required

After utility creation, update these skills to use it:
1. devforgeai-qa SKILL.md (Phase 0 Step 0.5)
2. devforgeai-development SKILL.md (Phase 0 if applicable)
3. devforgeai-orchestration SKILL.md (if applicable)

## Definition of Done

### Implementation
- [ ] shared-phase-0-loader.md file created
- [ ] devforgeai-qa reference path documented
- [ ] devforgeai-development reference path documented
- [ ] Pattern template documented
- [ ] Future skill guidance included

### Testing
- [ ] Create new test skill with Phase 0
- [ ] Use shared loader utility pattern
- [ ] Run new skill with deep mode
- [ ] Verify: Reference files load correctly
- [ ] Success criteria: Works across different skills

### Documentation
- [ ] Update RCA-021 Implementation Checklist with status

## Effort Estimate

- **Points:** 2
- **Estimated Hours:** 45 minutes
  - Create utility file: 20 minutes
  - Refactor devforgeai-qa Phase 0: 10 minutes
  - Refactor devforgeai-development Phase 0: 10 minutes
  - Testing: 5 minutes

## Related

- **RCA:** RCA-021-qa-skill-phases-skipped.md
- **Recommendation:** REC-5 (MEDIUM - Reference Document Auto-Load Utility)
- **Dependency:** STORY-215 (REC-1 mental model documentation must be in place first)
- **Skills to Update:** devforgeai-qa, devforgeai-development, devforgeai-orchestration

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-021 REC-5 |
