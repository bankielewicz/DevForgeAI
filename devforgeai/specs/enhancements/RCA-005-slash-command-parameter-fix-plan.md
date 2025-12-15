# RCA-005: Comprehensive Slash Command Parameter Fix Plan

**Issue:** Slash commands use broken parameter passing to Skills (Skills don't accept arguments)
**Date:** 2025-11-02
**Priority:** 🔴 CRITICAL - Framework broken without this fix
**Status:** ⏳ PLAN CREATED - Ready for implementation

---

## Executive Summary

**Problem Discovered:**
1. Slash commands pass arguments to Skills using `Skill(command="name --args")`
2. Skills CANNOT accept parameters (confirmed by official documentation)
3. @file references use `$ARGUMENTS` which includes flags in filenames
4. 5 of 9 slash commands are broken

**Root Cause:**
Framework built on assumption that Skills accept runtime parameters. Research confirms they don't - all parameters must be conveyed through conversation context.

**Solution:**
1. Fix @file references (use $1 instead of $ARGUMENTS)
2. Add AskUserQuestion validation for ambiguous arguments (defensive UX)
3. Remove arguments from Skill invocations
4. Update skills to extract parameters from conversation context
5. Update all documentation to remove aspirational content

**Estimated Effort:** 8-12 hours total
**Impact:** Framework becomes functional and robust

---

## Phase 1: Audit & Documentation (2 hours)

### Task 1.1: Complete Command Audit

**Objective:** Document current state of all 9 slash commands

**Actions:**
1. Read each slash command file
2. Identify Skill invocations with arguments
3. Identify @file references using $ARGUMENTS
4. Document parameter passing patterns
5. Categorize by fix complexity

**Files to audit:**
```
.claude/commands/
├── create-context.md
├── create-epic.md
├── create-sprint.md
├── create-story.md
├── create-ui.md      ← Uses Skill with args
├── dev.md            ← Uses Skill with args
├── ideate.md
├── orchestrate.md    ← Uses Skill with args (4 invocations!)
├── qa.md             ← Uses Skill with args
└── release.md        ← Uses Skill with args
```

**Deliverable:**
- Audit spreadsheet:
  - Command name
  - Uses Skill tool? (Y/N)
  - Skill invocation pattern
  - Uses @file? (Y/N)
  - @file pattern ($ARGUMENTS or $1?)
  - Parameters expected
  - Fix complexity (Simple/Medium/Complex)

**Success criteria:**
- All 9 commands documented
- Broken patterns identified
- Fix priority established

---

### Task 1.2: Create RCA-005 Root Cause Document

**Objective:** Document the 5 Whys analysis and root causes

**File:** `.devforgeai/specs/enhancements/RCA-005-skill-parameter-passing.md`

**Content:**
- Problem statement (3 errors from Codelens session)
- 5 Whys analysis for each error
- Root cause summary
- Official documentation evidence
- Impact assessment
- Solution overview

**Success criteria:**
- Complete RCA document created
- All 3 errors explained
- Root causes traced to architectural assumptions
- Evidence from official docs included

---

## Phase 2: Quick Fixes - @file References (1 hour)

### Task 2.1: Fix @file References in All Commands

**Objective:** Replace $ARGUMENTS with $1 in @file references

**Pattern to fix:**
```markdown
# BEFORE (BROKEN):
**Story:** @devforgeai/specs/Stories/$ARGUMENTS.story.md

# AFTER (FIXED):
**Story:** @devforgeai/specs/Stories/$1.story.md
```

**Files to modify:**
1. `.claude/commands/dev.md` - Line ~14
2. `.claude/commands/qa.md` - Line ~14-18
3. `.claude/commands/release.md` - Line ~14
4. `.claude/commands/orchestrate.md` - Line ~14
5. `.claude/commands/create-ui.md` - Line ~20

**Implementation:**
- Use Edit tool to replace each instance
- Verify @file references load story correctly
- Test with: `/dev STORY-001` (should load story file)

**Success criteria:**
- All @file references use $1 for story ID
- No flags included in file paths
- Story files load without error

---

### Task 2.2: Update argument-hint in Frontmatter

**Objective:** Clarify expected argument format

**Pattern:**
```yaml
# BEFORE (UNCLEAR):
argument-hint: [STORY-ID] [--mode=light|deep]

# AFTER (CLEAR):
argument-hint: [STORY-ID] [mode]
# Note: Use 'deep' or 'light', not --mode=deep
```

**Files to modify:**
- All commands with optional arguments (qa, release, orchestrate)

**Success criteria:**
- Users see correct syntax in autocomplete
- No -- prefix in hints (implies flags work)

---

## Phase 3: Defensive Validation with AskUserQuestion (3 hours)

### Task 3.1: Create Argument Validation Template

**Objective:** Standard validation pattern for all commands

**File:** `.claude/skills/devforgeai-development/references/slash-command-argument-validation-pattern.md` (new)

**Content:**

```markdown
# Slash Command Argument Validation Pattern

## Purpose

Defensive argument validation for slash commands to handle:
- Malformed story IDs
- Unknown flags (--mode=, --env=, etc.)
- Typos and user errors
- Ambiguous input

## Standard Validation Phase

Add as Phase 0 to all slash commands:

### Phase 0: Argument Validation & User Intent Clarification

#### Step 1: Extract Story ID

```
STORY_ID_CANDIDATE = $1

# Expected format: STORY-001, STORY-042, STORY-123
# Regex: ^STORY-[0-9]+$
```

#### Step 2: Validate Story ID Format

```
IF STORY_ID_CANDIDATE matches "^STORY-[0-9]+$":
  ✓ Valid format
  STORY_ID = STORY_ID_CANDIDATE
  Continue to Step 3

ELSE IF STORY_ID_CANDIDATE contains spaces:
  # Example: "STORY-001 --mode=deep" (user included flag)
  ⚠️ Ambiguous input - includes unexpected content

  AskUserQuestion:
  Question: "The argument '$STORY_ID_CANDIDATE' contains spaces or flags. What is the story ID?"
  Header: "Story ID"
  Options:
    - "STORY-001 (first word only)"
    - "STORY-042 (extract STORY-NNN pattern)"
    - "List available stories (I'll choose)"
    - "Show me correct command syntax"
  multiSelect: false

  Extract STORY_ID based on user response

ELSE IF STORY_ID_CANDIDATE contains "--":
  # Example: "--mode=deep" (user forgot story ID)
  ⚠️ Missing story ID

  AskUserQuestion:
  Question: "No story ID provided. Which story should I process?"
  Header: "Story ID"
  Options:
    - "List all stories in Backlog"
    - "List all stories in Dev Complete"
    - "List all stories in current sprint"
    - "Cancel command"
  multiSelect: false

  Extract STORY_ID from user selection

ELSE:
  # Unexpected format (e.g., "story-001", "001", "my-feature")
  ⚠️ Invalid format

  AskUserQuestion:
  Question: "Story ID '$STORY_ID_CANDIDATE' doesn't match expected format (STORY-NNN). What did you mean?"
  Header: "Story ID format"
  Options:
    - "Search for stories containing: $STORY_ID_CANDIDATE"
    - "List all available stories"
    - "Show me correct format examples"
  multiSelect: false
```

#### Step 3: Validate Story File Exists

```
# Use Glob to find story file (handles multiple naming conventions)
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no matches found:
  ⚠️ Story file not found

  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story not found"
  Options:
    - "List all available stories"
    - "Create ${STORY_ID} first (run /create-story)"
    - "I meant a different story (let me re-enter)"
    - "Cancel command"
  multiSelect: false

IF multiple matches found:
  # Example: STORY-001-feature-a.story.md, STORY-001-feature-b.story.md
  ⚠️ Multiple story files match

  AskUserQuestion:
  Question: "Multiple files match ${STORY_ID}. Which one?"
  Header: "Story selection"
  Options:
    [List each matched filename]
  multiSelect: false

  STORY_FILE = user selection

ELSE:
  # Exactly 1 match - perfect
  ✓ Story file found
  STORY_FILE = matched file path
```

#### Step 4: Parse Optional Arguments (Mode, Environment, etc.)

```
# For commands with optional arguments (qa, release, orchestrate)

IF $2 provided:
  SECOND_ARG = $2

  # Check if it's a known value
  IF command is /qa:
    IF $2 in ["deep", "light"]:
      MODE = $2
    ELSE IF $2 starts with "--":
      # User used flag syntax (--mode=deep)
      ⚠️ Flag syntax not supported

      AskUserQuestion:
      Question: "Detected flag syntax: $2. Which mode?"
      Header: "QA Mode"
      Options:
        - "deep (comprehensive validation)"
        - "light (quick checks)"
      multiSelect: false

      MODE = user selection
    ELSE:
      ⚠️ Unknown mode value

      AskUserQuestion:
      Question: "Unknown mode: $2. Which validation mode?"
      Header: "QA Mode"
      Options:
        - "deep (comprehensive validation)"
        - "light (quick checks)"
      multiSelect: false

      MODE = user selection

  IF command is /release:
    IF $2 in ["staging", "production"]:
      ENVIRONMENT = $2
    ELSE:
      AskUserQuestion:
      Question: "Unknown environment: $2. Where should I deploy?"
      Header: "Deployment environment"
      Options:
        - "staging (test environment)"
        - "production (live)"
      multiSelect: false

      ENVIRONMENT = user selection

ELSE:
  # No second argument - use default
  IF command is /qa:
    MODE = "deep"  # Default
  IF command is /release:
    ENVIRONMENT = "staging"  # Default (safe choice)
```

#### Step 5: Display Validation Summary

```
Validation Complete ✓

Story ID: ${STORY_ID}
Story File: ${STORY_FILE}
[Optional] Mode: ${MODE}
[Optional] Environment: ${ENVIRONMENT}

Proceeding with command execution...
```

---

## Example Usage Patterns

### Example 1: Correct Usage (No Interaction)

```bash
> /qa STORY-001 deep

Phase 0: Argument Validation
  ✓ Story ID: STORY-001 (valid format)
  ✓ Story file found: devforgeai/specs/Stories/STORY-001-setup.story.md
  ✓ Mode: deep (valid)
  ✓ Validation complete

Proceeding with deep QA validation...
```

---

### Example 2: User Error - Flag Syntax (Interactive)

```bash
> /qa STORY-001 --mode=deep

Phase 0: Argument Validation
  ✓ Story ID: STORY-001 (valid)
  ⚠️ Flag syntax detected: --mode=deep

  Which validation mode?
  □ deep (comprehensive validation)
  □ light (quick checks)

[User selects: deep]

  ✓ Mode: deep
  ✓ Validation complete

Proceeding with deep QA validation...
```

---

### Example 3: Malformed Input (Interactive)

```bash
> /qa STORY-001 --mode=deep extra-arg

Phase 0: Argument Validation
  ⚠️ Ambiguous input detected

  Arguments provided: ["STORY-001", "--mode=deep", "extra-arg"]
  Expected: [STORY-ID] [mode]

  Should I ignore extra arguments?
  □ Yes - Use STORY-001, mode=deep, ignore "extra-arg"
  □ No - Show me correct syntax
  □ Cancel command

[User selects: Yes]

  ✓ Story ID: STORY-001
  ✓ Mode: deep
  ✓ Extra arguments ignored
  ✓ Validation complete

Proceeding with deep QA validation...
```

---

### Example 4: Missing Story (Interactive)

```bash
> /qa STORY-999

Phase 0: Argument Validation
  ✓ Story ID: STORY-999 (valid format)
  ✗ Story file not found

  Story STORY-999 not found. What should I do?
  □ List all available stories
  □ Create STORY-999 first (run /create-story)
  □ I meant a different story
  □ Cancel command

[User selects: List all available stories]

  Available stories:
  1. STORY-001: Setup Cargo Workspace
  2. STORY-002: Implement CLI Argument Parsing
  3. STORY-003: Add Tree-sitter FFI

  Which story?
  □ STORY-001
  □ STORY-002
  □ STORY-003

[User selects: STORY-001]

  ✓ Story ID: STORY-001
  ✓ Story file: STORY-001-setup-cargo-workspace.story.md
  ✓ Validation complete

Proceeding with deep QA validation...
```

---

## Benefits of AskUserQuestion Validation

### 1. Graceful Error Handling ⭐⭐⭐⭐⭐
- Typos caught and corrected interactively
- Clear options instead of cryptic errors
- Users learn correct syntax through options

### 2. Framework Philosophy Alignment ⭐⭐⭐⭐⭐
- "Ask, Don't Assume" applied to argument parsing
- Evidence-based (user confirms intent)
- No silent failures or wrong assumptions

### 3. Superior User Experience ⭐⭐⭐⭐⭐
- Helpful instead of frustrating
- Multiple-choice (easy to answer)
- Self-documenting (shows correct syntax)

### 4. Defensive Programming ⭐⭐⭐⭐⭐
- Validates before executing
- Catches edge cases early
- Prevents downstream errors

### 5. Backwards Compatible ⭐⭐⭐⭐⭐
- Correct usage: No interaction needed
- Incorrect usage: Asks for clarification
- Degrades gracefully

---

## Detailed Implementation Plan

### Phase 2: Fix Core Commands (3 hours)

#### Task 2.1: Fix /dev Command

**File:** `.claude/commands/dev.md`

**Changes:**

1. **Fix @file reference (Line ~14):**
```markdown
# BEFORE:
**Story:** @devforgeai/specs/Stories/$ARGUMENTS.story.md

# AFTER:
**Story:** @devforgeai/specs/Stories/$1.story.md
```

2. **Add Phase 0: Argument Validation (before current Phase 0):**
```markdown
### Phase 0a: Argument Validation

**Extract story ID:**
STORY_ID = $1

**Validate format:**
IF $1 does NOT match "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I develop?"
  Header: "Story ID"
  Options:
    - "Extract STORY-NNN from: $1"
    - "List stories in Ready for Dev status"
    - "List stories in Backlog"
    - "Show correct /dev syntax"
  multiSelect: false

**Validate file exists:**
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no matches:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story not found"
  Options:
    - "List all available stories"
    - "Create ${STORY_ID} (run /create-story first)"
    - "Cancel command"
  multiSelect: false
```

3. **Fix Skill invocation (Line ~150):**
```markdown
# BEFORE:
Skill(command="devforgeai-development --story=$ARGUMENTS")

# AFTER:
Skill(command="devforgeai-development")
# Story content already loaded via @file reference
# Skill extracts story ID from conversation context
```

**Estimated time:** 30 minutes

---

#### Task 2.2: Fix /qa Command

**File:** `.claude/commands/qa.md`

**Changes:**

1. **Update frontmatter:**
```yaml
# BEFORE:
argument-hint: [STORY-ID] [--mode=light|deep]

# AFTER:
argument-hint: [STORY-ID] [mode]
# Mode: 'deep' or 'light' (no dashes)
```

2. **Fix @file reference:**
```markdown
# BEFORE:
**Story:** @devforgeai/specs/Stories/$ARGUMENTS.story.md

# AFTER:
**Story:** @devforgeai/specs/Stories/$1.story.md
**Mode:** $2 (defaults to "deep" if not provided)
```

3. **Add Phase 0: Argument Validation:**
```markdown
### Phase 0: Argument Validation

**Extract arguments:**
- STORY_ID = $1
- MODE_ARG = $2 (optional)

**Validate story ID:**
[Same validation as /dev - use AskUserQuestion for invalid format]

**Parse mode argument:**
IF $2 provided:
  IF $2 in ["deep", "light"]:
    MODE = $2

  ELSE IF $2 starts with "--mode=":
    # User used flag syntax (educate them)
    EXTRACTED_MODE = substring after "--mode="

    IF EXTRACTED_MODE in ["deep", "light"]:
      MODE = EXTRACTED_MODE

      # Gentle education
      Note to user: "Flag syntax (--mode=) not needed. Use: /qa STORY-001 deep"

    ELSE:
      AskUserQuestion:
      Question: "Unknown mode in flag: $2. Which validation mode?"
      Header: "QA Mode"
      Options:
        - "deep (comprehensive validation ~2 min)"
        - "light (quick checks ~30 sec)"
      multiSelect: false

  ELSE:
    # Unknown value
    AskUserQuestion:
    Question: "Unknown mode: $2. Which validation mode?"
    Header: "QA Mode"
    Options:
      - "deep (comprehensive validation)"
      - "light (quick checks)"
    multiSelect: false

ELSE:
  # No mode provided - use intelligent default
  Read story status from @file context

  IF status == "Dev Complete":
    MODE = "deep"  # Full validation before QA approval
  ELSE IF status == "In Development":
    MODE = "light"  # Quick validation during development
  ELSE:
    # Unclear - ask user
    AskUserQuestion:
    Question: "No mode specified. Which validation?"
    Header: "QA Mode"
    Options:
      - "deep (comprehensive - for Dev Complete stories)"
      - "light (quick - for In Development stories)"
    multiSelect: false
```

4. **Fix Skill invocation:**
```markdown
# BEFORE:
Skill(command="devforgeai-qa --mode={MODE} --story={STORY-ID}")

# AFTER:
**Context for Skill:**
- Story loaded via @file reference above
- Validation mode: {MODE}
- Story ID: {STORY_ID}

Skill(command="devforgeai-qa")

# Skill will read story content from conversation and mode from context
```

**Estimated time:** 45 minutes

---

#### Task 2.3: Fix /release Command

**File:** `.claude/commands/release.md`

**Changes:**

1. **Update frontmatter:**
```yaml
# BEFORE:
argument-hint: [STORY-ID] [--env=staging|production]

# AFTER:
argument-hint: [STORY-ID] [environment]
# Environment: 'staging' or 'production' (no dashes)
```

2. **Fix @file reference:**
```markdown
**Story:** @devforgeai/specs/Stories/$1.story.md
**Environment:** $2 (defaults to "staging" if not provided)
```

3. **Add Phase 0: Argument Validation with environment handling:**
```markdown
### Phase 0: Argument Validation

**Extract arguments:**
- STORY_ID = $1
- ENV_ARG = $2 (optional)

**Validate story ID:**
[Same pattern as /dev and /qa]

**Parse environment argument:**
IF $2 provided:
  IF $2 in ["staging", "production", "prod", "stage"]:
    # Normalize
    IF $2 in ["prod", "production"]:
      ENVIRONMENT = "production"
    ELSE:
      ENVIRONMENT = "staging"

  ELSE IF $2 starts with "--env=":
    EXTRACTED_ENV = substring after "--env="

    IF EXTRACTED_ENV in ["staging", "production"]:
      ENVIRONMENT = EXTRACTED_ENV
      Note: "Flag syntax not needed. Use: /release STORY-001 production"
    ELSE:
      AskUserQuestion:
      Question: "Unknown environment: $2. Where should I deploy?"
      Header: "Deployment target"
      Options:
        - "staging (test environment)"
        - "production (live environment)"
      multiSelect: false

  ELSE:
    AskUserQuestion:
    Question: "Unknown environment: $2. Where should I deploy?"
    Header: "Deployment target"
    Options:
      - "staging (test environment first)"
      - "production (skip staging - risky!)"
    multiSelect: false

ELSE:
  # Default to staging (safe choice)
  ENVIRONMENT = "staging"
  Note: "Defaulting to staging. Use '/release STORY-001 production' for prod."
```

**Estimated time:** 45 minutes

---

#### Task 2.4: Fix /orchestrate Command

**File:** `.claude/commands/orchestrate.md`

**Changes:**

1. **Fix @file reference:**
```markdown
**Story:** @devforgeai/specs/Stories/$1.story.md
```

2. **Add Phase 0: Argument Validation** (same pattern)

3. **Fix 4 Skill invocations:**
```markdown
# Line ~78: BEFORE
Skill(command="devforgeai-development --story=$ARGUMENTS")

# AFTER
Skill(command="devforgeai-development")

# Line ~126: BEFORE
Skill(command="devforgeai-qa --mode=deep --story=$ARGUMENTS")

# AFTER
**QA Mode:** deep
Skill(command="devforgeai-qa")

# Line ~173: BEFORE
Skill(command="devforgeai-release --story=$ARGUMENTS --env=staging")

# AFTER
**Environment:** staging
Skill(command="devforgeai-release")

# Line ~217: BEFORE
Skill(command="devforgeai-release --story=$ARGUMENTS --env=production")

# AFTER
**Environment:** production
Skill(command="devforgeai-release")
```

**Estimated time:** 1 hour (4 invocations + complex logic)

---

#### Task 2.5: Fix /create-ui Command

**File:** `.claude/commands/create-ui.md`

**Changes:**

1. **Fix @file reference** (if present)
2. **Add Phase 0: Argument Validation**
3. **Fix Skill invocations:**
```markdown
# BEFORE:
Skill(command="devforgeai-ui-generator --story=${STORY_ID}")

# AFTER:
Skill(command="devforgeai-ui-generator")
```

**Estimated time:** 30 minutes

---

### Phase 4: Update Skills to Read Context (2 hours)

#### Task 4.1: Update devforgeai-development Skill

**File:** `.claude/skills/devforgeai-development/SKILL.md`

**Add to beginning of skill (after frontmatter):**

```markdown
## Extracting Parameters from Conversation Context

**IMPORTANT:** Skills cannot accept runtime parameters. All information must be extracted from conversation context.

### Story ID Extraction

The slash command loads the story file via @file reference, making story content available in conversation.

**Extract story ID from conversation:**
```
Look for YAML frontmatter in conversation:
  ---
  id: STORY-XXX
  title: ...
  ---

Extract: id field = Story ID

OR search conversation for "Story: STORY-XXX" pattern
OR search for "devforgeai/specs/Stories/STORY-XXX" file reference
```

### Mode/Environment Extraction (if applicable)

**Look for explicit statements in conversation:**
- "Validation Mode: deep" → MODE = deep
- "Environment: staging" → ENVIRONMENT = staging

**If not found, use intelligent defaults:**
- QA mode: Check story status (Dev Complete → deep, In Development → light)
- Release environment: Default to staging (safe choice)

### Validation

Before proceeding with TDD workflow:
- [ ] Story ID extracted from conversation
- [ ] Story content available (via @file load)
- [ ] Acceptance criteria accessible
- [ ] Ready to proceed

**If extraction fails:**
- Grep conversation for "STORY-" pattern
- Read devforgeai/specs/Stories/ directory for context
- As last resort: Use first story found (inform user)
```

**Estimated time:** 30 minutes

---

#### Task 4.2: Update devforgeai-qa Skill

**File:** `.claude/skills/devforgeai-qa/SKILL.md`

**Add context extraction section:**
```markdown
## Parameter Extraction from Conversation

### Story ID
[Same pattern as development skill]

### Validation Mode

**Look for mode in conversation:**
- "Validation Mode: deep" → MODE = deep
- "Validation Mode: light" → MODE = light
- "Mode: deep" → MODE = deep

**If not found:**
- Check story status in conversation:
  - "status: Dev Complete" → MODE = deep (comprehensive)
  - "status: In Development" → MODE = light (quick checks)
- Default: deep (thorough validation)

### Extraction Validation

- [ ] Story ID found
- [ ] Story content available
- [ ] Mode determined
- [ ] Ready for QA phases
```

**Estimated time:** 30 minutes

---

#### Task 4.3: Update devforgeai-release Skill

**File:** `.claude/skills/devforgeai-release/SKILL.md`

**Add context extraction:**
```markdown
## Parameter Extraction

### Story ID
[Same pattern]

### Environment

**Look for environment in conversation:**
- "Environment: staging" → ENV = staging
- "Environment: production" → ENV = production
- "Deploy to production" → ENV = production

**If not found:**
- Default: staging (safe choice)
- Inform user: "Defaulting to staging deployment"

### Deployment Strategy (Optional)

**Look for strategy in conversation:**
- "Strategy: blue-green" → STRATEGY = blue-green
- "Strategy: rolling" → STRATEGY = rolling

**If not found:**
- Read from tech-stack.md or deployment config
- Default: rolling (safest)
```

**Estimated time:** 30 minutes

---

#### Task 4.4: Update devforgeai-ui-generator Skill

**File:** `.claude/skills/devforgeai-ui-generator/SKILL.md`

**Add context extraction:**
```markdown
## Parameter Extraction

### Story ID (Optional)
UI generator can work with or without story:
- With story: Extract story ID from conversation
- Without story: Interactive mode (ask user for component details)

### Component Description (If no story)
Look for: User's description of UI component in conversation
Example: "Create a login form" → COMPONENT = login form
```

**Estimated time:** 30 minutes

---

### Phase 5: Update Documentation (2 hours)

#### Task 5.1: Fix skills-reference.md

**File:** `.claude/memory/skills-reference.md`

**Remove ALL skill invocations with arguments:**
```markdown
# BEFORE (ASPIRATIONAL - WRONG):
Skill(command="devforgeai-development --story=STORY-001")
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")

# AFTER (EVIDENCE-BASED - CORRECT):
# Load story into conversation context first
**Story:** @devforgeai/specs/Stories/STORY-001.story.md

# Invoke skill without arguments
Skill(command="devforgeai-development")

# Skill reads story content from conversation context
```

**Add section:**
```markdown
## CRITICAL: Skills Cannot Accept Parameters

From official Claude documentation:
"Skills CANNOT accept command-line style parameters. All parameters are conveyed through natural language in the conversation."

**How to pass "parameters" to skills:**
1. Load content into conversation (via @file references, Read tool, or text)
2. Set context with explicit statements ("Mode: deep", "Environment: staging")
3. Invoke skill with name only: Skill(command="skill-name")
4. Skill extracts needed information from conversation context
```

**Estimated time:** 30 minutes

---

#### Task 5.2: Fix commands-reference.md

**File:** `.claude/memory/commands-reference.md`

**Update all command syntax examples:**
```markdown
# BEFORE:
/qa [STORY-ID] [--mode=light|deep]

# AFTER:
/qa [STORY-ID] [mode]
# Mode: 'deep' or 'light' (no -- prefix)
# Examples:
  /qa STORY-001           # Defaults to deep
  /qa STORY-001 deep      # Explicit deep
  /qa STORY-001 light     # Explicit light
```

**Add limitations section:**
```markdown
## Slash Command Limitations

**What works:**
- Multiple arguments: /qa STORY-001 deep ✅
- Positional parameters: $1, $2, $3 ✅
- @file with $1: @file/$1.md ✅

**What doesn't work:**
- Flag syntax: /qa --mode=deep STORY-001 ❌
- @file with $ARGUMENTS: @file/$ARGUMENTS.md ❌ (includes all args)
- Skill with arguments: Skill(command="name --arg") ❌
```

**Estimated time:** 30 minutes

---

#### Task 5.3: Update CLAUDE.md

**File:** `CLAUDE.md`

**Add to "Slash Commands" section:**
```markdown
## Slash Commands (User-Facing Workflows)

**Parameter Syntax:**
- Use positional arguments: /command ARG1 ARG2 ARG3
- NOT flag syntax: /command --flag=value ❌
- Access via: $1, $2, $3 in command definition

**Example:**
/qa STORY-001 deep     ✅ Correct
/qa STORY-001 --mode=deep  ⚠️ Works but flag ignored, use: /qa STORY-001 deep
```

**Add to "Working with Skills" section:**
```markdown
## CRITICAL: Skill Invocation Constraints

Skills CANNOT accept parameters at invocation time.

❌ WRONG:
Skill(command="devforgeai-qa --mode=deep --story=STORY-001")

✅ CORRECT:
# Load story and set context first
**Story:** @devforgeai/specs/Stories/STORY-001.story.md
**Mode:** deep

# Invoke skill without arguments
Skill(command="devforgeai-qa")

# Skill extracts story ID and mode from conversation context
```

**Estimated time:** 30 minutes

---

#### Task 5.4: Create Argument Validation Reference

**File:** `.claude/skills/devforgeai-development/references/slash-command-argument-validation-pattern.md` (new)

**Content:**
- Complete validation template (from Task 3.1 above)
- Examples for each validation scenario
- AskUserQuestion patterns
- Error handling best practices
- Integration with skills

**Estimated time:** 30 minutes

---

### Phase 6: Testing & Validation (3 hours)

#### Task 6.1: Create Test Commands

**File 1:** `.claude/commands/test-skill-context.md`
```markdown
---
description: Test if skills can read conversation context
---

# Test: Skill Context Reading

Load test data into context:
**Test Story ID:** STORY-001
**Test Mode:** deep
**Test Environment:** staging

Invoke skill without arguments:
Skill(command="devforgeai-architecture")

Verify: Did skill see the test data above?
```

**File 2:** `.claude/commands/test-arg-validation.md`
```markdown
---
description: Test argument validation with AskUserQuestion
---

# Test: Argument Validation

Try various malformed inputs:
1. Invalid story ID: "story-001" (lowercase)
2. With flags: "STORY-001 --mode=deep"
3. Missing story ID: "--mode=deep"
4. Unknown args: "STORY-001 extra stuff"

Each should trigger AskUserQuestion with helpful options.
```

**Estimated time:** 30 minutes

---

#### Task 6.2: Test Each Fixed Command

**Test matrix:**

| Command | Test Input | Expected Behavior |
|---------|------------|-------------------|
| /dev | STORY-001 | ✓ Load story, invoke skill, execute TDD |
| /dev | STORY-999 | Ask: Story not found, show options |
| /qa | STORY-001 | ✓ Default to deep mode |
| /qa | STORY-001 deep | ✓ Use deep mode |
| /qa | STORY-001 --mode=deep | Ask: Parse mode=deep, educate on syntax |
| /release | STORY-001 | ✓ Default to staging |
| /release | STORY-001 production | ✓ Deploy to production |
| /orchestrate | STORY-001 | ✓ Full lifecycle |
| /create-ui | STORY-001 | ✓ UI generation |

**Create test log:**
`.devforgeai/specs/enhancements/RCA-005-test-results.md`

**Document:**
- Each test scenario
- Actual behavior
- Pass/Fail status
- Screenshots or output samples

**Estimated time:** 2 hours

---

#### Task 6.3: Regression Testing

**Verify fixes don't break existing functionality:**

1. Test commands that weren't broken (create-context, ideate, etc.)
2. Verify @imports still work in CLAUDE.md
3. Verify TodoWrite still works in skills
4. Verify technology detection still works (RCA-002 fix)
5. Verify empty git repo handling still works (RCA-003 fix)

**Success criteria:**
- All previous RCA fixes still working
- No regressions introduced
- New fixes coexist with old fixes

**Estimated time:** 30 minutes

---

### Phase 7: Finalize RCA-005 Documentation (1 hour)

#### Task 7.1: Complete RCA-005 Enhancement Document

**File:** `.devforgeai/specs/enhancements/RCA-005-skill-parameter-passing.md`

**Sections:**
- Problem statement (3 errors from Codelens)
- Complete 5 Whys analysis (all 3 errors + meta-analysis)
- Root cause summary
- Official documentation evidence
- Impact assessment
- All solutions implemented
- Testing results
- Framework lessons learned
- Prevention strategies

**Estimated time:** 30 minutes

---

#### Task 7.2: Create Framework Validation Summary

**File:** `.devforgeai/FRAMEWORK-VALIDATION-SUMMARY.md`

**Content:**
- All 5 RCAs summary
- What was broken, what was fixed
- Current framework status
- Remaining risks
- Testing coverage
- Production readiness assessment

**Estimated time:** 30 minutes

---

## Success Criteria

### Functional Requirements
- [ ] All @file references use $1 (not $ARGUMENTS)
- [ ] All Skill invocations have no arguments
- [ ] All commands include Phase 0 argument validation
- [ ] All commands use AskUserQuestion for ambiguous input
- [ ] Skills document context extraction in SKILL.md
- [ ] All 9 commands tested with real usage

### Quality Requirements
- [ ] No aspirational content in documentation
- [ ] All examples tested and working
- [ ] Error messages are helpful (not cryptic)
- [ ] User experience is smooth (graceful degradation)

### Documentation Requirements
- [ ] RCA-005 document complete
- [ ] All memory files updated
- [ ] CLAUDE.md updated
- [ ] Framework validation summary created
- [ ] Test results documented

---

## Estimated Timeline

**Phase 1: Audit (2 hours)**
- Task 1.1: Command audit (1 hour)
- Task 1.2: RCA-005 skeleton (1 hour)

**Phase 2: Core Fixes (3 hours)**
- Task 2.1: /dev (30 min)
- Task 2.2: /qa (45 min)
- Task 2.3: /release (45 min)
- Task 2.4: /orchestrate (1 hour)
- Task 2.5: /create-ui (30 min)

**Phase 3: Validation Template (included in Phase 2)**

**Phase 4: Skills Update (2 hours)**
- 4 skills × 30 min each

**Phase 5: Documentation (2 hours)**
- 4 docs × 30 min each

**Phase 6: Testing (3 hours)**
- Test commands creation (30 min)
- Command testing (2 hours)
- Regression testing (30 min)

**Phase 7: Finalization (1 hour)**
- RCA-005 completion (30 min)
- Validation summary (30 min)

**Total: 13 hours**

---

## Risk Mitigation

**Risk 1: Skills can't read conversation context effectively**
- Mitigation: Test first (Phase 6 Task 6.1)
- Fallback: Manual workflows (proven to work)

**Risk 2: AskUserQuestion adds too much interaction**
- Mitigation: Only trigger on ambiguous input (correct usage = no questions)
- Benefit: Better UX than silent failure

**Risk 3: Breaking changes affect in-flight work**
- Mitigation: Test all commands before deploying
- Rollback: Keep CLAUDE.md.backup

---

## Implementation Priority

**CRITICAL (Do First):**
1. Phase 2: Fix @file references and Skill invocations (3 hours)
2. Phase 6.2: Test fixed commands (2 hours)

**HIGH (Do Second):**
3. Phase 4: Update skills to read context (2 hours)
4. Phase 5: Update documentation (2 hours)

**MEDIUM (Do Third):**
5. Phase 1: Audit and document (2 hours)
6. Phase 6.1: Create test commands (30 min)
7. Phase 7: Finalize docs (1 hour)

**Can complete CRITICAL work in ~5 hours to restore functionality**

---

## Deliverables

1. **5 Fixed Slash Commands** (dev, qa, release, orchestrate, create-ui)
2. **4 Updated Skills** (development, qa, release, ui-generator)
3. **Argument Validation Template** (reusable pattern)
4. **Updated Documentation** (3 memory files + CLAUDE.md)
5. **Test Suite** (validation commands)
6. **RCA-005 Document** (complete analysis)
7. **Framework Validation Summary** (overall status)

**Total: 13 files modified + 4 files created**

---

## Why This Plan is Comprehensive

### Addresses All 3 Errors

**Error 1: Malformed @file path**
→ Fixed by using $1 instead of $ARGUMENTS

**Error 2: File read failure**
→ Fixed by validation before read + AskUserQuestion

**Error 3: Skill with arguments fails**
→ Fixed by removing arguments + context passing

### Incorporates User's Insight

**Your suggestion:** Use AskUserQuestion for unknown flags
→ Implemented in Phase 0 validation for ALL commands

### Evidence-Based

**All solutions:**
- ✅ Use built-in tools (Edit, AskUserQuestion, Glob)
- ✅ Based on official docs (Skills can't take parameters)
- ✅ Tested pattern (AskUserQuestion proven in ui-generator)
- ✅ No aspirational content

### Follows DevForgeAI Principles

- ✅ "Ask, Don't Assume" - Validates arguments, asks when unclear
- ✅ Evidence-based - Uses official documentation
- ✅ Defensive programming - Validates before executing
- ✅ User-friendly - Helpful errors, clear options

---

**This plan fixes the broken architecture while making it MORE robust through defensive validation. Ready to execute?**