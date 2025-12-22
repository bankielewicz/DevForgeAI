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

## Definition of Done

### Implementation
- [ ] CLAUDE.md includes Plan File Convention section
- [ ] devforgeai-development SKILL.md includes plan file search in Phase 0
- [ ] Search algorithm implemented (glob + grep for story ID)
- [ ] Resume prompt added when existing plan found
- [ ] New plan naming convention enforced

### Quality
- [ ] All 5 test cases pass
- [ ] Existing random-named plan files still work
- [ ] No false positives in plan file detection

### Documentation
- [ ] Convention documented in CLAUDE.md
- [ ] Examples of good/bad naming provided

## Out of Scope

- Automatic cleanup of stale plan files
- Plan file versioning or history
- Cross-conversation memory (requires external storage)
