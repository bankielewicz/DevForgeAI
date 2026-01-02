---
id: STORY-216
title: Add Phase 0 Step 0.5 Enforcement for Deep Mode
type: enhancement
epic: EPIC-033
priority: HIGH
points: 1
status: Backlog
created: 2025-01-01
source: RCA-021 REC-2
depends_on:
  - STORY-215
---

# STORY-216: Add Phase 0 Step 0.5 Enforcement for Deep Mode

## User Story

**As a** DevForgeAI user running /qa in deep mode,
**I want** Phase 0 to enforce that the deep-validation-workflow.md reference file is loaded,
**So that** Claude has visibility into all Phase 1-3 workflow details before executing them.

## Background

RCA-021 identified that SKILL.md's "Load Deep Mode Workflow" step (Step 0.5) is documented but not enforced. Claude can skip it without warning, breaking phase visibility. The deep-validation-workflow.md reference file contains all Phase 1-3 workflow details; without it, Claude is working from abbreviated Phase 0 instructions only.

**Source RCA:** `devforgeai/RCA/RCA-021-qa-skill-phases-skipped.md`

**Evidence:**
- SKILL.md line 77: "Progressive Disclosure: Load `references/deep-validation-workflow.md` once at Phase 0 for deep mode"
- SKILL.md lines 279-281: Step 0.5 explicit Read instruction
- First /qa execution: Did not load this file in Phase 0

## Acceptance Criteria

### AC-1: Phase 0 Completion Enforcement Section Added

**Given** the devforgeai-qa SKILL.md file
**When** Phase 0 Marker Write section completes (after line 281)
**Then** a "Phase 0 Completion Enforcement" subsection exists

---

### AC-2: Deep Mode Workflow Verification Logic

**Given** the Phase 0 Completion Enforcement section
**When** mode == "deep"
**Then** verification logic checks if deep-validation-workflow.md was loaded:
```
IF "deep-validation-workflow.md" NOT loaded in conversation:
    Display: "❌ CRITICAL ERROR: Phase 0 Step 0.5 incomplete"
    HALT: "Cannot proceed to Phase 1 without deep workflow reference"
```

---

### AC-3: Success Path Confirmation

**Given** deep-validation-workflow.md WAS loaded
**When** verification runs
**Then** display: "✓ Deep mode workflow reference verified loaded"

---

### AC-4: Exact Text Added Per RCA-021

**Given** the RCA-021 recommended implementation (lines 215-233)
**When** updating devforgeai-qa SKILL.md
**Then** add the exact text from RCA-021 REC-2:

```markdown
### Phase 0 Completion Enforcement

**Verify deep-validation-workflow.md was loaded (deep mode only):**

```
IF mode == "deep":
    IF "deep-validation-workflow.md" NOT loaded in conversation:
        Display: "❌ CRITICAL ERROR: Phase 0 Step 0.5 incomplete"
        Display: "   Deep validation workflow reference file was not loaded"
        Display: "   Load file: .claude/skills/devforgeai-qa/references/deep-validation-workflow.md"
        HALT: "Cannot proceed to Phase 1 without deep workflow reference"
        Instruction: "Load the reference file manually, then resume /qa {STORY_ID} deep"
    ELSE:
        Display: "✓ Deep mode workflow reference verified loaded"
```

This enforcement prevents Phase 1-3 from executing without complete initialization.
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `.claude/skills/devforgeai-qa/SKILL.md` | Modify | Add Phase 0 Completion Enforcement after Phase 0 Marker Write section |

### Location in SKILL.md

Add after Phase 0 Marker Write section (around line 281):

```
### Phase 0 Marker Write
[existing content]

### Phase 0 Completion Enforcement
[new content here]

### Phase 1 Pre-Flight
[existing content]
```

## Definition of Done

### Implementation
- [ ] Phase 0 Completion Enforcement section added
- [ ] Deep mode verification logic included
- [ ] HALT message with resolution steps included
- [ ] Success confirmation message included

### Testing
- [ ] Intentionally skip reading deep-validation-workflow.md in Phase 0
- [ ] Run: `/qa STORY-001 deep`
- [ ] Verify: HALT message appears preventing Phase 1 execution
- [ ] Manually load file and resume
- [ ] Verify: Phases execute completely
- [ ] Success criteria: Cannot bypass Phase 0 Step 0.5

### Documentation
- [ ] Update RCA-021 Implementation Checklist with status

## Effort Estimate

- **Points:** 1
- **Estimated Hours:** 15 minutes
  - Add enforcement check: 10 minutes
  - Testing: 5 minutes

## Related

- **RCA:** RCA-021-qa-skill-phases-skipped.md
- **Recommendation:** REC-2 (HIGH - Phase 0 Step 0.5 Enforcement for Deep Mode)
- **Dependency:** STORY-215 (REC-1 mental model documentation)
- **Related Stories:** STORY-217 (REC-3), STORY-218 (REC-4), STORY-219 (REC-5)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-021 REC-2 |
