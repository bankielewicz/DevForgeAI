# RCA-005: Slash Command Parameter Passing Fix - AI Handoff Prompt

**Purpose:** Complete prompt for new Claude Code session to implement RCA-005 fixes
**Context:** 5th RCA from Codelens project revealed slash commands invoke Skills with arguments (doesn't work)
**Priority:** 🔴 CRITICAL - 5 of 9 slash commands are broken
**Estimated Effort:** 13 hours (or 5 hours for critical fixes only)

---

## COPY-PASTE PROMPT FOR NEW CLAUDE SESSION

```
I need you to implement RCA-005 fixes for the DevForgeAI framework. This RCA revealed that slash commands are passing arguments to Skills using Skill(command="name --args") syntax, which doesn't work - Skills cannot accept parameters.

## Context

**What Happened:**
During Codelens project development, user ran `/qa STORY-001 --mode=deep` and encountered 3 errors:

1. **Error 1:** Story file path became "STORY-001 --mode=deep.story.md" (included flag in filename)
2. **Error 2:** File read failed (malformed path)
3. **Error 3:** Skill invocation failed with "Unknown skill: devforgeai-qa --mode=deep --story=STORY-001"

**Root Cause Confirmed:**
Official Claude documentation confirms Skills CANNOT accept runtime parameters. From research:
> "Skills CANNOT accept command-line style parameters like `my-skill --param=value`. All parameters are conveyed through natural language in the conversation."

**Impact:**
- 5 of 9 slash commands are broken (dev, qa, release, orchestrate, create-ui)
- All use pattern: Skill(command="skillname --arguments")
- All have @file references using $ARGUMENTS (includes flags in paths)

**Previous Work:**
- Git commit 7fe155a contains all Phase 3 work + RCA fixes 1-4
- All files backed up and committed
- Ready for RCA-005 implementation

## Your Task

Implement the comprehensive fix plan documented in:
`devforgeai/specs/enhancements/RCA-005-slash-command-parameter-fix-plan.md`

**Read these files for complete context:**
1. `devforgeai/specs/enhancements/RCA-005-slash-command-parameter-fix-plan.md` - Complete implementation plan
2. `.ai_docs/Claude-Skills-Technical-Architecture-and-Parameter-System.md` - Research on Skills
3. `.ai_docs/claude-skills.md` - Official Skills documentation
4. `devforgeai/specs/enhancements/RCA-001-incomplete-epic-generation-enhancements.md` - Previous RCA example
5. `CLAUDE.md` - Framework overview and critical rules

## Critical Constraints

**MUST Follow:**
1. Skills cannot accept parameters - only skill name: `Skill(command="skillname")`
2. Parameters passed via conversation context (story loaded via @file, mode stated explicitly)
3. Use $1, $2, $3 for positional arguments (NOT $ARGUMENTS in @file paths)
4. Add AskUserQuestion validation for ambiguous arguments (user's excellent suggestion)
5. All solutions must be evidence-based (use built-in tools only)
6. Test before documenting (no aspirational content)

## Implementation Approach

**Option A: Full Plan (13 hours total)**
Execute all 7 phases from RCA-005 plan:
- Phase 1: Audit & Documentation (2 hours)
- Phase 2: Fix Core Commands (3 hours)
- Phase 3: Validation Template (included)
- Phase 4: Update Skills (2 hours)
- Phase 5: Update Documentation (2 hours)
- Phase 6: Testing & Validation (3 hours)
- Phase 7: Finalize RCA-005 Docs (1 hour)

**Option B: Critical Fixes Only (5 hours)**
Execute phases 2, 4, 6.2 only:
- Fix @file references ($ARGUMENTS → $1)
- Remove arguments from Skill invocations
- Add Phase 0 argument validation with AskUserQuestion
- Test all 5 affected commands
- Update 4 affected skills

**Recommendation:** Start with Option B (critical fixes), then assess if full plan needed.

## Key Fixes Required

### 1. Fix @file References (All 5 Commands)

**Pattern:**
```markdown
# BEFORE (BROKEN):
**Story:** @devforgeai/specs/Stories/$ARGUMENTS.story.md

# AFTER (FIXED):
**Story:** @devforgeai/specs/Stories/$1.story.md
**Additional Args:** $2, $3 (if needed)
```

**Files:**
- `.claude/commands/dev.md`
- `.claude/commands/qa.md`
- `.claude/commands/release.md`
- `.claude/commands/orchestrate.md`
- `.claude/commands/create-ui.md`

---

### 2. Add Phase 0: Argument Validation (All 5 Commands)

**Pattern (using AskUserQuestion for defensive UX):**
```markdown
### Phase 0: Argument Validation

**Extract story ID:**
STORY_ID = $1

**Validate format:**
IF $1 does NOT match "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I process?"
  Header: "Story ID"
  Options:
    - "Extract STORY-NNN from: $1"
    - "List available stories"
    - "Show correct syntax"
  multiSelect: false

**Validate file exists:**
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no matches:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story not found"
  Options:
    - "List all available stories"
    - "Create ${STORY_ID} first"
    - "Cancel command"
  multiSelect: false

**Parse optional arguments (mode, environment, etc.):**
[Command-specific validation - see plan for details]
```

**Benefits of AskUserQuestion:**
- Catches typos and malformed input
- Educates users on correct syntax
- Graceful degradation (no hard failures)
- Aligns with "Ask, Don't Assume" principle

---

### 3. Fix Skill Invocations (Remove Arguments)

**Pattern:**
```markdown
# BEFORE (BROKEN):
Skill(command="devforgeai-development --story=$ARGUMENTS")
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")

# AFTER (FIXED):
# Story already loaded via @file reference
# Mode/environment stated explicitly in conversation
**Story:** @devforgeai/specs/Stories/$1.story.md
**Mode:** deep

Skill(command="devforgeai-development")
# Skill extracts story ID and mode from conversation context
```

**Files:**
- All 5 commands have 11 total broken Skill invocations to fix

---

### 4. Update Skills to Extract Context

**Add to each skill SKILL.md:**
```markdown
## Extracting Parameters from Conversation Context

**IMPORTANT:** Skills cannot accept runtime parameters. Extract from conversation.

### Story ID Extraction
Look for YAML frontmatter in conversation:
  ---
  id: STORY-XXX
  ---

OR search for "devforgeai/specs/Stories/STORY-XXX" file reference

### Mode/Environment Extraction
Look for explicit statements:
- "Validation Mode: deep"
- "Environment: staging"

If not found, use intelligent defaults based on story status.
```

**Skills to update:**
- `devforgeai-development`
- `devforgeai-qa`
- `devforgeai-release`
- `devforgeai-ui-generator`

---

## Success Criteria

After implementation:
- [ ] All @file references use $1 (not $ARGUMENTS)
- [ ] All Skill invocations have no arguments
- [ ] All 5 commands include Phase 0 argument validation
- [ ] All commands use AskUserQuestion for ambiguous input
- [ ] Skills document context extraction
- [ ] All commands tested and working
- [ ] Documentation updated (no aspirational content)
- [ ] RCA-005 document completed

## Testing Requirements

**Must test each fixed command:**
1. `/dev STORY-001` - Correct usage (should work smoothly)
2. `/dev STORY-999` - Story not found (should ask user)
3. `/qa STORY-001 deep` - Correct usage with mode
4. `/qa STORY-001 --mode=deep` - Flag syntax (should parse and educate)
5. `/release STORY-001` - Default to staging
6. `/release STORY-001 production` - Production deployment
7. `/orchestrate STORY-001` - Full lifecycle

**Document results in:** `devforgeai/specs/enhancements/RCA-005-test-results.md`

## Important Notes

**Framework Philosophy:**
- Evidence-based only (test before documenting)
- Ask, Don't Assume (use AskUserQuestion liberally)
- Defensive programming (validate before executing)

**Token Budget:**
- You have 1M tokens available
- Current usage will start ~40K (CLAUDE.md + memory files)
- Plenty of room for comprehensive fixes

**Quality Over Speed:**
- Take your time
- Test each fix thoroughly
- Document actual behavior (not assumptions)
- Use AskUserQuestion when uncertain

## Files You'll Modify

**Slash Commands (5):**
1. .claude/commands/dev.md
2. .claude/commands/qa.md
3. .claude/commands/release.md
4. .claude/commands/orchestrate.md
5. .claude/commands/create-ui.md

**Skills (4):**
6. .claude/skills/devforgeai-development/SKILL.md
7. .claude/skills/devforgeai-qa/SKILL.md
8. .claude/skills/devforgeai-release/SKILL.md
9. .claude/skills/devforgeai-ui-generator/SKILL.md

**Documentation (3):**
10. .claude/memory/skills-reference.md
11. .claude/memory/commands-reference.md
12. CLAUDE.md

**New Files (2):**
13. .claude/skills/devforgeai-development/references/slash-command-argument-validation-pattern.md
14. devforgeai/specs/enhancements/RCA-005-skill-parameter-passing.md

**Total: 14 files to modify/create**

## Execution Strategy

**Start with critical path:**
1. Read RCA-005 plan thoroughly
2. Fix @file references (15 min)
3. Test one command (/dev) to validate approach
4. If working: Apply pattern to remaining 4 commands
5. Fix Skill invocations
6. Update skills
7. Test all commands
8. Document results

**Use TodoWrite to track progress** - Create todo for each command to fix.

## Questions for You (Before Starting)

If you encounter ambiguity, HALT and use AskUserQuestion:
1. Should you implement full plan (13 hours) or critical fixes only (5 hours)?
2. If Skill invocations still don't work after removing arguments, should you use manual workflows instead?
3. Any other commands besides the 5 identified that might have similar issues?

## Reference Materials

**In this repository:**
- Complete implementation plan: `devforgeai/specs/enhancements/RCA-005-slash-command-parameter-fix-plan.md`
- Previous RCA examples: `devforgeai/specs/enhancements/RCA-001` through `RCA-004`
- Framework documentation: `CLAUDE.md`, `README.md`, `ROADMAP.md`
- Official research: `.ai_docs/Claude-Skills-Technical-Architecture-and-Parameter-System.md`

**Pattern to follow:**
- Same quality as RCA-001 through RCA-004 (all were excellent)
- Evidence-based solutions only
- Comprehensive testing
- Clear documentation

## Start Here

Begin by reading the complete plan:

```
Read(devforgeai/specs/enhancements/RCA-005-slash-command-parameter-fix-plan.md)
```

Then create a TodoWrite list for all tasks and execute systematically.

Good luck! This is critical work that will make DevForgeAI's slash commands actually functional. 🚀
```

---

**End of handoff prompt. Copy everything between the triple backticks above.**
