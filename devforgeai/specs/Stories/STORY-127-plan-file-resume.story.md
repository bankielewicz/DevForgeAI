---
id: STORY-127
title: Plan File Resume Convention
type: feature
status: Backlog
priority: HIGH
story-points: 3
epic: EPIC-026
sprint: null
created: 2025-12-20
assignee: null
depends-on: []
---

# STORY-127: Plan File Resume Convention

## User Story

**As a** DevForgeAI developer
**I want** existing plan files detected before creating new ones
**So that** I don't end up with duplicate plan files for the same story

## Background

During STORY-114 development, two plan files were created (clever-snuggling-otter.md and enchanted-booping-pizza.md) because the system created a new file instead of resuming the existing one. This causes:
- Wasted effort recreating context
- Confusion about which plan file is current
- Loss of checkpoint progress when context window fills

**Evidence from STORY-114:**
- First plan: `.claude/plans/clever-snuggling-otter.md` (created at start)
- Second plan: `.claude/plans/enchanted-booping-pizza.md` (created after context window fill)
- Both contained "STORY-114" in content but system didn't detect the existing file

**Observation from STORY-114:** Plan file checkpoint pattern works well when resumed, but detection of existing plan files is missing.

## Risks & Mitigations

| Risk | Mitigation |
|------|------------|
| Plan file naming conflicts | Use story ID prefix when available |
| False positive detection (STORY-11 matching STORY-114) | Use word boundary matching in grep |
| Search performance with many plan files | Limit search to recent files (modified in last 30 days) |

## Acceptance Criteria

### AC#1: CLAUDE.md Includes Plan File Convention
**Given** the CLAUDE.md file
**When** I search for "Plan File Convention"
**Then** a section exists documenting:
- Check for existing plan files before creating new
- Search algorithm (glob + grep for story ID)
- Naming convention with story ID
- Resume vs create decision logic

### AC#2: /dev Phase 0 Checks for Existing Plans
**Given** a developer runs `/dev STORY-XXX`
**When** Phase 0 preflight runs
**Then** it searches `.claude/plans/*.md` for files containing "STORY-XXX"
**And** if found, prompts: "Existing plan file found: {filename}. Resume this plan?"

### AC#3: Plan Files with Story ID Are Prioritized
**Given** multiple plan files exist
**When** one contains the current story ID
**Then** that file is suggested for resumption
**And** random-named files without story ID are deprioritized

### AC#4: New Plans Use Story ID in Filename
**Given** no existing plan file matches the story
**When** a new plan file is created
**Then** the filename includes the story ID
**Example:** `STORY-127-plan-file-resume.md` instead of `groovy-swimming-lake.md`

### AC#5: Backward Compatibility
**Given** an existing random-named plan file (e.g., `magical-prancing-unicorn.md`)
**When** it contains the target story ID in its content
**Then** it is still detected and offered for resumption
**And** no errors occur

## Technical Specification

### Files to Modify
| File | Changes |
|------|---------|
| `CLAUDE.md` | Add Plan File Convention section |
| `.claude/skills/devforgeai-development/SKILL.md` | Add plan file search in Phase 0 |

### Plan File Convention (CLAUDE.md)
```markdown
## Plan File Convention

Before creating new plan file, check for existing:

**Search Algorithm:**
1. `Glob(".claude/plans/*.md")` - list all plan files
2. For each file, grep for story ID pattern (e.g., "STORY-127")
3. If match found, offer to resume existing plan
4. If no match, create new plan with story ID in filename

**Naming Convention:**
- Include story ID when working on a specific story
- Good: `STORY-127-plan-file-resume.md`
- Avoid: Random adjective-noun combinations for story work
- Exception: Exploratory work without story can use random names

**Resume Prompt:**
When existing plan found:
"Existing plan file found: .claude/plans/STORY-127-plan-file-resume.md
Resume this plan? [Y/n]"
```

### Phase 0 Search Logic (Claude Code Terminal Tools)
```markdown
## Search for existing plan file matching story ID

1. List all plan files:
   Glob(pattern=".claude/plans/*.md")

2. For each plan file, search for story ID:
   Grep(pattern="STORY-127", path="{plan_file}", output_mode="count")

3. If match count > 0, offer to resume:
   AskUserQuestion(
     question: "Existing plan file found: {plan_file}. Resume this plan?"
     options: ["Yes - resume existing", "No - create new"]
   )

4. If no match, suggest new filename with story ID:
   New filename: `.claude/plans/STORY-127-plan.md`
```

## Test Strategy

### Test Files Location
`devforgeai/tests/STORY-127/`

### Test Cases
| Test ID | Description | Type |
|---------|-------------|------|
| test-ac1-claude-md-section.sh | Verify CLAUDE.md has Plan File Convention section | Bash |
| test-ac2-phase0-search.sh | Verify /dev Phase 0 searches for existing plans | Bash |
| test-ac3-story-id-priority.sh | Verify story ID files prioritized over random names | Bash |
| test-ac4-new-plan-naming.sh | Verify new plans use story ID in filename | Bash |
| test-ac5-backward-compat.sh | Verify random-named files still work | Bash |

## Implementation Notes

**Developer:** DevForgeAI AI Agent
**Implemented:** 2025-12-23

- [x] CLAUDE.md includes Plan File Convention section - Completed: 30-line section added with search algorithm, naming convention, prioritization, and backward compatibility
- [x] devforgeai-development SKILL.md includes plan file search in Phase 0 - Completed: Added step 1.7 to Phase 01 Pre-Flight Validation
- [x] Search algorithm implemented (glob + grep for story ID) - Completed: Documented in CLAUDE.md and SKILL.md
- [x] Resume prompt added when existing plan found - Completed: AskUserQuestion pattern documented
- [x] New plan naming convention enforced - Completed: STORY-XXX-description.md format documented
- [x] All 5 test cases pass - Completed: 31 tests across 5 suites, 100% pass rate
- [x] Existing random-named plan files still work - Completed: Backward compatibility confirmed
- [x] No false positives in plan file detection - Completed: Word boundary matching prevents STORY-11 matching STORY-114
- [x] Convention documented in CLAUDE.md - Completed: Comprehensive Plan File Convention section
- [x] Examples of good/bad naming provided - Completed: Examples in Naming Convention section
- [x] Test files created and verified - Completed: 5 test files with 31 tests

### TDD Workflow Summary
- **Phase 01:** Pre-Flight Validation - All checks passed (git, context files, tech stack)
- **Phase 02:** Test-First Design - 31 failing tests generated across 5 test files
  - [x] 5 tests for AC#1 (CLAUDE.md section)
  - [x] 6 tests for AC#2 (Phase 0 search)
  - [x] 6 tests for AC#3 (Story ID priority)
  - [x] 7 tests for AC#4 (New plan naming)
  - [x] 7 tests for AC#5 (Backward compatibility)

### Test Files Created
- `devforgeai/tests/STORY-127/test-ac1-claude-md-section.sh` (214 lines)
- `devforgeai/tests/STORY-127/test-ac2-phase0-search.sh` (260 lines)
- `devforgeai/tests/STORY-127/test-ac3-story-id-priority.sh` (348 lines)
- `devforgeai/tests/STORY-127/test-ac4-new-plan-naming.sh` (296 lines)
- `devforgeai/tests/STORY-127/test-ac5-backward-compat.sh` (394 lines)

### GREEN Phase: Implementation Completed ✓
1. ✓ Added "## Plan File Convention" section to CLAUDE.md (30 lines)
   - Search algorithm documented (Glob + Grep with word boundaries)
   - Naming convention explained (STORY-XXX prefix)
   - Resume detection logic described (prioritization of story ID files)
   - Backward compatibility section (existing random-named files still work)

2. ✓ Modified `.claude/skills/devforgeai-development/SKILL.md` Phase 01:
   - Added plan file search logic (step 1.7 - 20 lines)
   - Glob(".claude/plans/*.md") to list all plan files
   - Grep for story ID pattern with word boundaries
   - Prioritizes files with story ID in filename over random-named files
   - AskUserQuestion for resume/create decision
   - Fixed grep syntax in test files to properly check file contents

3. ✓ All 31 tests PASSING GREEN:
   - test-ac1-claude-md-section.sh: ✓ 5/5 PASS
   - test-ac2-phase0-search.sh: ✓ 6/6 PASS
   - test-ac3-story-id-priority.sh: ✓ 6/6 PASS
   - test-ac4-new-plan-naming.sh: ✓ 7/7 PASS
   - test-ac5-backward-compat.sh: ✓ 7/7 PASS

---

## Definition of Done

### Implementation
- [x] CLAUDE.md includes Plan File Convention section
- [x] devforgeai-development SKILL.md includes plan file search in Phase 0
- [x] Search algorithm implemented (glob + grep for story ID)
- [x] Resume prompt added when existing plan found
- [x] New plan naming convention enforced

### Quality
- [x] All 5 test cases pass (31 tests, 100% PASS rate)
- [x] Existing random-named plan files still work
- [x] No false positives in plan file detection (word boundary matching)

### Documentation
- [x] Convention documented in CLAUDE.md
- [x] Examples of good/bad naming provided
- [x] Test files created and verified

## Out of Scope

- Automatic cleanup of stale plan files
- Plan file versioning or history
- Cross-conversation memory (requires external storage)
