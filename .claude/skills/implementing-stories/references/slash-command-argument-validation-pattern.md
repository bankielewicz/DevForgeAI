# Slash Command Argument Validation Pattern

**Purpose:** Defensive argument validation for DevForgeAI slash commands
**Version:** 1.0 | **Status:** Production Ready

---

## Core Principle

When user input is unclear or malformed, ASK for clarification (AskUserQuestion) rather than failing silently or assuming intent. Aligns with framework's "Ask, Don't Assume" rule.

---

## Standard Phase 01: Argument Validation

Add as first phase to all slash commands accepting story IDs or structured arguments.

### Step 1: Extract Story ID

```
STORY_ID = $1
```

**Format:** `STORY-NNN` (numeric). **Regex:** `^STORY-[0-9]+$`

---

### Step 2: Validate Story ID Format

```
IF $1 is empty:
  AskUserQuestion:
  Question: "No story ID provided. Which story should I process?"
  Header: "Story ID Required"
  Options:
    - "List stories in [appropriate status]"
    - "Show correct command syntax"
    - "Cancel command"
  multiSelect: false

IF $1 does NOT match pattern "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I process?"
  Header: "Story ID Format"
  Options:
    - "Try to extract STORY-NNN from: $1"
    - "List all available stories"
    - "Show correct format examples"
  multiSelect: false

  Extract STORY_ID based on user response
```

**Common malformed inputs and auto-extraction:**
- `story-001` (lowercase) -> `STORY-001`
- `STORY001` (missing dash) -> `STORY-001`
- `001` (missing prefix) -> `STORY-001`
- `my-feature` (wrong format) -> Ask user which story

---

### Step 3: Validate Story File Exists

```
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no matches found:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story Not Found"
  Options:
    - "List all available stories"
    - "Create ${STORY_ID} (run /create-story first)"
    - "I meant a different story (let me re-enter)"
    - "Cancel command"
  multiSelect: false

  Handle based on user selection:
  - "List all": Glob("devforgeai/specs/Stories/*.md"), display list, ask which one
  - "Create": Exit with message to run /create-story
  - "Different story": Ask for correct story ID
  - "Cancel": Exit gracefully

IF multiple matches found:
  AskUserQuestion:
  Question: "Multiple files match ${STORY_ID}. Which one?"
  Header: "Story Selection"
  Options: [List each matched filename]
  multiSelect: false
  STORY_FILE = user selection

ELSE:
  STORY_FILE = matched file path
```

---

### Step 4: Parse Optional Arguments

#### Pattern A: Mode Argument (for /qa command)

Valid modes: `deep`, `light`

```
IF $2 provided:
  IF $2 in ["deep", "light"]:
    MODE = $2

  ELSE IF $2 starts with "--mode=":
    EXTRACTED_MODE = substring after "--mode="
    IF EXTRACTED_MODE in ["deep", "light"]:
      MODE = EXTRACTED_MODE
      Note to user: "Flag syntax (--mode=) not needed. Use: /qa STORY-001 deep"
    ELSE:
      AskUserQuestion: [Select deep or light with descriptions]

  ELSE IF $2 starts with "--":
    AskUserQuestion:
    Question: "Unknown flag: $2. Which validation mode did you want?"
    Header: "QA Mode"
    Options:
      - "deep (comprehensive validation)"
      - "light (quick checks)"
      - "Show correct /qa syntax"
    multiSelect: false
    Note to user: "Flags not needed. Use: /qa STORY-001 deep"

  ELSE:
    AskUserQuestion: [Select deep or light -- unknown value]

ELSE:
  # No mode provided - default based on story status
  IF story status == "Dev Complete":
    MODE = "deep"
    Note: "Defaulting to deep validation (story is Dev Complete)"
  ELSE IF story status == "In Development":
    MODE = "light"
    Note: "Defaulting to light validation (story in development)"
  ELSE:
    AskUserQuestion: [Select deep or light]
```

#### Pattern B: Environment Argument (for /release command)

Valid environments: `staging`, `production` (also accepts `prod`, `stage` as aliases)

Follows same structure as Pattern A with these specifics:
- Normalize aliases: `prod` -> `production`, `stage` -> `staging`
- Flag format: `--env=`
- Default when omitted: `staging` (safe default)
- Education note: `"Flags not needed. Use: /release STORY-001 production"`

```
IF $2 provided:
  IF $2 in ["staging", "production", "prod", "stage"]:
    ENVIRONMENT = normalize($2)
  ELSE IF $2 starts with "--env=":
    Extract and validate, educate on flag syntax
  ELSE IF $2 starts with "--":
    AskUserQuestion: [Select staging or production]
  ELSE:
    AskUserQuestion: [Select staging or production]
ELSE:
  ENVIRONMENT = "staging"
  Note: "Defaulting to staging. Use '/release STORY-001 production' for production."
```

---

### Step 5: Display Validation Summary

```
✓ Story ID: ${STORY_ID}
✓ Story file: ${STORY_FILE}
✓ Validation mode: ${MODE}        # if applicable
✓ Environment: ${ENVIRONMENT}      # if applicable
✓ Proceeding with command execution...
```

---

## Implementation Example: /dev Command

```markdown
### Phase 01: Argument Validation

**Extract story ID:**
STORY_ID = $1

**Validate format:**
IF $1 does NOT match "STORY-[0-9]+":
  AskUserQuestion:
  Question: "Story ID '$1' doesn't match format STORY-NNN. What story should I develop?"
  Header: "Story ID"
  Options:
    - "List stories in Ready for Dev status"
    - "List stories in Backlog status"
    - "Show correct /dev syntax"
  multiSelect: false

**Validate file exists:**
Glob(pattern="devforgeai/specs/Stories/${STORY_ID}*.story.md")

IF no matches:
  AskUserQuestion:
  Question: "Story ${STORY_ID} not found. What should I do?"
  Header: "Story Not Found"
  Options:
    - "List all available stories"
    - "Create ${STORY_ID} (run /create-story first)"
    - "Cancel command"
  multiSelect: false

**Validation summary:**
✓ Story ID: ${STORY_ID}
✓ Story file: ${STORY_FILE}
✓ Proceeding with development...
```

---

## Test Cases

| # | Input | Behavior | Result |
|---|-------|----------|--------|
| 1 | `/qa STORY-001 deep` | No interaction, executes immediately | Smooth execution |
| 2 | `/qa STORY-001 --mode=deep` | Extracts mode, educates on syntax | Works + user learns |
| 3 | `/qa story-001 deep` | Detects malformed ID, offers extraction | Recovers from typo |
| 4 | `/dev STORY-999` | Valid format but file not found, lists available stories | User discovers correct ID |
| 5 | `/release STORY-001 --unknown-flag` | Unknown flag, asks for environment selection | Handles gracefully |

**Representative flow (Test Case 3):**
```
> /qa story-001 deep

  Story ID 'story-001' doesn't match format STORY-NNN.
  What story should I validate?
  [] Try to extract STORY-NNN from: story-001
  [] List stories in Dev Complete status

  [User selects: Try to extract]

  ✓ Story ID: STORY-001 (extracted)
  ✓ Mode: deep
  ✓ Proceeding with QA validation...
```

---

## Integration with Skills

After Phase 01 validation, the command has validated STORY_ID, MODE/ENVIRONMENT, and loaded story content via @file.

**Skill invocation pattern:**

```markdown
### Phase N: Invoke [Skill Name] Skill

**Context for skill:**
- Story content loaded via @file reference
- Story ID: ${STORY_ID}
- Validation mode: ${MODE}          # if applicable
- Environment: ${ENVIRONMENT}        # if applicable

**Invoke skill (no arguments):**
Skill(command="skill-name")

Note: Skill extracts story ID from conversation context (YAML frontmatter)
and mode/environment from explicit statement above.
```

---

## Applicability

**Use Phase 01 when:** Command accepts story IDs or structured arguments, has optional arguments, invokes Skills, or is user-facing.

**Skip Phase 01 when:** Command takes only free-form text, has no arguments, or is internal-only.

---

## Implementation Checklist

- [ ] Extract story ID using $1
- [ ] Validate format (regex: `^STORY-[0-9]+$`)
- [ ] Validate story file exists (Glob)
- [ ] Parse optional arguments with flag handling
- [ ] AskUserQuestion for all ambiguous input
- [ ] Educational notes for incorrect syntax
- [ ] Display validation summary before proceeding
- [ ] Handle all error cases (missing ID, file not found, invalid mode/env)

---

## Related Documentation

| Category | Files |
|----------|-------|
| Official | `devforgeai/specs/Terminal/slash-commands.md`, `devforgeai/specs/claude-skills.md` |
| Framework | `CLAUDE.md`, `devforgeai/specs/context/anti-patterns.md`, `.claude/memory/skills-reference.md` |
| RCA Context | `devforgeai/specs/enhancements/RCA-005-skill-parameter-passing.md`, `devforgeai/specs/enhancements/RCA-005-command-audit.md`, `devforgeai/specs/enhancements/RCA-005-slash-command-parameter-fix-plan.md` |

---

**Origin:** v1.0 (2025-11-02) from RCA-005 findings. Applied to 5 commands: dev, qa, release, orchestrate, create-ui.
