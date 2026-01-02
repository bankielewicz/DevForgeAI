---
id: STORY-215
title: Add Pre-Skill Execution Checklist to CLAUDE.md
type: enhancement
epic: EPIC-033
priority: CRITICAL
points: 1
status: Backlog
created: 2025-01-01
source: RCA-021 REC-1
depends_on: []
---

# STORY-215: Add Pre-Skill Execution Checklist to CLAUDE.md

## User Story

**As a** DevForgeAI user invoking skills like /qa or /dev,
**I want** Claude to have an explicit pre-execution checklist for skills,
**So that** Claude understands skill phases are mandatory sequential instructions (not optional reference material).

## Background

RCA-021 identified that Claude's first /qa execution treated skill phases as "optional reference material" instead of "mandatory sequential instructions." While CLAUDE.md has a mental model chart (lines 14-32) and explicit statements like "NEVER wait passively after skill invocation" (line 232), Claude's first execution only partially internalized this model.

**Source RCA:** `devforgeai/RCA/RCA-021-qa-skill-phases-skipped.md`

**Root Cause:** Claude's mental model of skill execution was incomplete. The skill execution model was documented but Claude's first execution fell into a middle ground: Neither fully awaiting (wrong) nor fully executing (also partially wrong).

## Acceptance Criteria

### AC-1: Pre-Skill Execution Checklist Added to CLAUDE.md

**Given** the CLAUDE.md file with skill execution documentation
**When** the "CRITICAL: How Skills Work" section is updated
**Then** a new "Pre-Skill Execution Checklist" subsection exists after the mental model chart

---

### AC-2: Checklist Contains 5 Verification Points

**Given** the Pre-Skill Execution Checklist section
**When** Claude reads it before invoking any skill
**Then** the checklist contains these 5 verification points:
1. Skill contains phases → ALL phases must execute in sequence (not optional)
2. Phase 0 has reference loading → Load reference files in Phase 0 BEFORE Phase 1
3. Phases 1-4 have pre-flight checks → Run pre-flight verification BEFORE phase work
4. Skill says "YOU execute" → Run all steps systematically (not selectively)
5. Mode requested matches execution scope → Deep mode = execute all phases completely

---

### AC-3: Enforcement Pattern Documented

**Given** any checklist item is unclear
**When** Claude is about to invoke a skill
**Then** the checklist instructs: "HALT before invoking skill and ask for clarification with AskUserQuestion tool"

---

### AC-4: Exact Text Added Per RCA-021

**Given** the RCA-021 recommended implementation (lines 153-184)
**When** updating CLAUDE.md
**Then** add the exact text from RCA-021 REC-1:

```markdown
### Pre-Skill Execution Checklist

**Before invoking ANY skill with Skill(command="..."), verify:**

1. **Skill contains phases?**
   - Skills contain phases (Phase 01, Phase 02, etc.)
   - ALL phases must execute in sequence (not optional)
   - If phases exist, you must execute all of them

2. **Phase 0 has reference loading?**
   - Check for "Step 0.N: Load reference files" or similar
   - If deep mode → Load reference files in Phase 0 BEFORE Phase 1 starts
   - Reference files contain complete workflow details needed for later phases

3. **Phases 1-4 have pre-flight checks?**
   - Check each phase for "Pre-Flight: Verify previous phase" section
   - Run pre-flight verification BEFORE executing phase's main work
   - HALT if previous phase not verified complete

4. **Skill says "YOU execute"?**
   - Explicit statements like "YOU execute the skill's phases"
   - This means you run all steps systematically
   - Not a reference to read selectively - mandatory instructions to follow

5. **Mode requested matches execution scope?**
   - Light mode → Execute specified light validation subset
   - Deep mode → Execute all documented phases completely
   - User clarification overrides defaults: If user says "run them all", execute all

**Enforcement:** If any checklist item is unclear, HALT before invoking skill and ask for clarification with AskUserQuestion tool.
```

## Technical Specification

### Files to Modify

| File | Change Type | Description |
|------|-------------|-------------|
| `CLAUDE.md` | Modify | Add Pre-Skill Execution Checklist after line 32 (end of mental model chart) |

### Location in CLAUDE.md

Add after the existing "Skills Execution" section (around line 232):

```
## Skills Execution
[existing content about skills being inline prompt expansions]

### Pre-Skill Execution Checklist
[new content here]
```

## Definition of Done

### Implementation
- [ ] Pre-Skill Execution Checklist section added to CLAUDE.md
- [ ] All 5 verification points documented
- [ ] Enforcement pattern (HALT + AskUserQuestion) included
- [ ] Text matches RCA-021 REC-1 specification

### Testing
- [ ] Create test story STORY-999-test.story.md
- [ ] Run: `/qa STORY-999 deep`
- [ ] Verify: Phase 0 Step 0.5 loads deep-validation-workflow.md
- [ ] Verify: All 5 phases execute completely
- [ ] Success criteria: Zero phase skipping

### Documentation
- [ ] Update RCA-021 Implementation Checklist with status

## Effort Estimate

- **Points:** 1
- **Estimated Hours:** 30 minutes
  - Add checklist to CLAUDE.md: 15 minutes
  - Testing: 15 minutes

## Related

- **RCA:** RCA-021-qa-skill-phases-skipped.md
- **Recommendation:** REC-1 (CRITICAL - Skill Execution Mental Model Enforcement)
- **Related Stories:** STORY-216 (REC-2), STORY-217 (REC-3), STORY-218 (REC-4), STORY-219 (REC-5)

## Change Log

| Date | Author | Change |
|------|--------|--------|
| 2025-01-01 | claude/opus | Story created from RCA-021 REC-1 |
