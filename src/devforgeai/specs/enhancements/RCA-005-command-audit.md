# RCA-005: Slash Command Audit
**Date:** 2025-11-02
**Purpose:** Document current state of all 9 slash commands for parameter passing analysis

---

## Audit Summary

| Command | Uses Skill? | Skill Invocation Pattern | Uses @file? | @file Pattern | Parameters Expected | Fix Required? |
|---------|-------------|-------------------------|-------------|---------------|---------------------|---------------|
| create-context | ✅ Yes | `Skill(command="devforgeai-architecture")` | ❌ No | N/A | [project-name] | ❌ No - Correct |
| create-epic | ❌ No | N/A (uses Task tool) | ❌ No | N/A | [epic-name] | ❌ No - Correct |
| create-sprint | ❌ No | N/A (no Skill/Task) | ❌ No | N/A | [sprint-name] | ❌ No - Correct |
| create-story | ❌ No | N/A (uses Task tool) | ❌ No | N/A | [feature-description] | ❌ No - Correct |
| create-ui | ✅ Yes | `Skill(command="devforgeai-ui-generator --story=${STORY_ID}")` | ❌ No | N/A | [STORY-ID or description] | ✅ **YES - BROKEN** |
| dev | ✅ Yes | `Skill(command="devforgeai-development --story=$ARGUMENTS")` | ✅ Yes | `@.ai_docs/Stories/$ARGUMENTS.story.md` | [STORY-ID] | ✅ **YES - BROKEN** |
| ideate | ✅ Yes | `Skill(command="devforgeai-ideation")` | ❌ No | N/A | [business-idea] | ❌ No - Correct |
| orchestrate | ✅ Yes | 4 invocations with `--story=$ARGUMENTS --env=X` | ✅ Yes | `@.ai_docs/Stories/$ARGUMENTS.story.md` | [STORY-ID] | ✅ **YES - BROKEN** |
| qa | ✅ Yes | `Skill(command="devforgeai-qa --mode={MODE} --story={STORY-ID}")` | ✅ Yes | `@.ai_docs/Stories/$ARGUMENTS.story.md` | [STORY-ID] [--mode] | ✅ **YES - BROKEN** |
| release | ✅ Yes | `Skill(command="devforgeai-release --story={STORY-ID} --env={env}")` | ✅ Yes | `@.ai_docs/Stories/$ARGUMENTS.story.md` | [STORY-ID] [--env] | ✅ **YES - BROKEN** |

---

## Broken Commands (5 of 9)

### 1. create-ui
- **File:** `.claude/commands/create-ui.md`
- **Line 114:** `Skill(command="devforgeai-ui-generator --story=${STORY_ID}")`
- **Line 119:** `Skill(command="devforgeai-ui-generator --description=\"${COMPONENT_DESCRIPTION}\"")`
- **Problem:** Skills cannot accept `--story` or `--description` parameters
- **Fix Complexity:** Medium
- **@file issue:** No (doesn't use @file)

### 2. dev
- **File:** `.claude/commands/dev.md`
- **Line 14:** `@.ai_docs/Stories/$ARGUMENTS.story.md`
- **Line 150:** `Skill(command="devforgeai-development --story=$ARGUMENTS")`
- **Problem 1:** @file uses $ARGUMENTS (includes flags in path)
- **Problem 2:** Skill cannot accept `--story` parameter
- **Fix Complexity:** Simple
- **Needs Phase 0:** Yes (argument validation)

### 3. orchestrate
- **File:** `.claude/commands/orchestrate.md`
- **Line 14:** `@.ai_docs/Stories/$ARGUMENTS.story.md`
- **Line 78:** `Skill(command="devforgeai-development --story=$ARGUMENTS")`
- **Line 126:** `Skill(command="devforgeai-qa --mode=deep --story=$ARGUMENTS")`
- **Line 173:** `Skill(command="devforgeai-release --story=$ARGUMENTS --env=staging")`
- **Line 217:** `Skill(command="devforgeai-release --story=$ARGUMENTS --env=production")`
- **Problem 1:** @file uses $ARGUMENTS (includes flags in path)
- **Problem 2:** 4 Skill invocations with parameters (all broken)
- **Fix Complexity:** Complex (most invocations)
- **Needs Phase 0:** Yes (argument validation)

### 4. qa
- **File:** `.claude/commands/qa.md`
- **Line 16:** `@.ai_docs/Stories/$ARGUMENTS.story.md`
- **Line 51:** `Skill(command="devforgeai-qa --mode={MODE} --story={STORY-ID}")`
- **Problem 1:** @file uses $ARGUMENTS (includes flags like --mode=deep in path)
- **Problem 2:** Skill cannot accept `--mode` or `--story` parameters
- **Fix Complexity:** Medium
- **Needs Phase 0:** Yes (mode parsing + validation)

### 5. release
- **File:** `.claude/commands/release.md`
- **Line 17:** `@.ai_docs/Stories/$ARGUMENTS.story.md`
- **Line 163:** `Skill(command="devforgeai-release --story={STORY-ID} --env={env}")`
- **Problem 1:** @file uses $ARGUMENTS (includes flags like --env=production in path)
- **Problem 2:** Skill cannot accept `--story` or `--env` parameters
- **Fix Complexity:** Medium
- **Needs Phase 0:** Yes (environment parsing + validation)

---

## Correct Commands (4 of 9)

### 1. create-context ✅
- Uses Skill correctly: `Skill(command="devforgeai-architecture")` (no arguments)
- No @file references
- No parameter passing issues

### 2. create-epic ✅
- Uses Task tool (not Skill)
- No @file references
- No parameter passing issues

### 3. create-sprint ✅
- Uses native tools only (Read, Write, Edit, Glob)
- No Skill invocations
- No @file references
- No parameter passing issues

### 4. create-story ✅
- Uses Task tool (not Skill)
- No @file references
- No parameter passing issues

### 5. ideate ✅
- Uses Skill correctly: `Skill(command="devforgeai-ideation")` (no arguments)
- No @file references
- No parameter passing issues

---

## Total Issues Found

**@file References Using $ARGUMENTS:** 4
- dev.md line 14
- orchestrate.md line 14
- qa.md line 16
- release.md line 17

**Skill Invocations with Arguments:** 11 total
- create-ui.md: 2 invocations
- dev.md: 1 invocation
- orchestrate.md: 4 invocations (most complex)
- qa.md: 1 invocation
- release.md: 1 invocation

**Incorrect argument-hint:** 2
- qa.md: Shows `[--mode=light|deep]` (flag syntax)
- release.md: Shows `[--env=staging|production]` (flag syntax)

**Total Fixes Required:** 17 (4 @file + 11 Skill + 2 argument-hint)

---

## Fix Pattern Summary

### Pattern 1: Fix @file References (4 fixes)
```markdown
# BEFORE (BROKEN):
@.ai_docs/Stories/$ARGUMENTS.story.md

# AFTER (FIXED):
@.ai_docs/Stories/$1.story.md
```

### Pattern 2: Remove Skill Arguments (11 fixes)
```markdown
# BEFORE (BROKEN):
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")

# AFTER (FIXED):
**Story:** @.ai_docs/Stories/$1.story.md
**Validation Mode:** deep

Skill(command="devforgeai-qa")
```

### Pattern 3: Update argument-hint (2 fixes)
```markdown
# BEFORE (MISLEADING):
argument-hint: [STORY-ID] [--mode=light|deep]

# AFTER (CORRECT):
argument-hint: [STORY-ID] [mode]
# Mode: 'deep' or 'light' (no -- prefix)
```

### Pattern 4: Add Phase 0 Validation (5 commands)
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

**Parse optional arguments (mode/environment):**
IF $2 starts with "--":
  # Flag syntax - educate user while parsing
  AskUserQuestion:
  Question: "Detected flag syntax: $2. Which mode/environment?"
  Header: "Validation Mode"
  Options:
    - "deep (comprehensive)"
    - "light (quick)"
  multiSelect: false

  Note: "Flag syntax not needed. Use: /qa STORY-001 deep"
```

---

## Audit Conclusion

**Framework Status:** 55% of commands broken (5 of 9)
**Root Cause:** Assumption that Skills accept CLI-style parameters
**Impact:** Core workflows non-functional (dev, qa, release, orchestrate, create-ui)
**Solution:** 17 specific fixes across 5 commands + 4 skills + 3 docs

**Next:** Proceed to Phase 1.2 (Create RCA-005 root cause document)
