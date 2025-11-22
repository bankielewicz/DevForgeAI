# Phase 1: Story Discovery & Context

This phase generates story ID, discovers epic/sprint context, and collects metadata.

## Overview

Story creation begins with discovery: assigning a unique ID, determining relationships to epics/sprints, and gathering essential metadata through user interaction.

**Execution Modes:**
- **Interactive Mode:** Ask user questions for all metadata (normal)
- **Batch Mode:** Extract metadata from context markers (batch creation from epics)

---

## Step 0: Load User Input Guidance Patterns (NEW - Guidance Integration)

**Purpose:** Load guidance patterns before interactive questions to improve question quality and user experience

**Execution:** < 2 seconds (p95), ≤ 1,000 tokens

**Guidance File Path:** `src/claude/skills/devforgeai-ideation/references/user-input-guidance.md`

**Loading Logic:**

```python
def load_user_input_guidance():
    """
    Load guidance patterns for Phase 1 questions.
    Handles batch caching (load once, reuse for stories 2-N).
    """

    global GUIDANCE_CACHE, GUIDANCE_AVAILABLE, LOADED_PATTERNS

    # Check batch mode status
    batch_index = extract_marker("**Batch Index:**") or 0

    if batch_index == 0:
        # First story in batch (or interactive mode): Attempt to load

        log_info("Loading user-input-guidance.md...")

        try:
            # Load guidance file
            guidance_content = Read(
                file_path="src/claude/skills/devforgeai-ideation/references/user-input-guidance.md"
            )

            # Parse patterns (extract ### headings with descriptions)
            patterns = extract_patterns_from_markdown(guidance_content)

            # Normalize pattern names for matching
            normalized_patterns = {
                normalize_pattern_name(name): content
                for name, content in patterns.items()
            }

            # Validate minimum 4 critical patterns present
            if len(normalized_patterns) >= 4:
                GUIDANCE_CACHE = guidance_content
                LOADED_PATTERNS = normalized_patterns
                GUIDANCE_AVAILABLE = True

                log_info(f"Guidance loaded: {len(normalized_patterns)} patterns extracted")
                return True
            else:
                log_warning(f"Insufficient patterns ({len(normalized_patterns)}), using baseline")
                GUIDANCE_AVAILABLE = False
                return False

        except FileNotFoundError:
            log_warning("Guidance file not found, proceeding with baseline logic")
            GUIDANCE_AVAILABLE = False
            return False

        except Exception as e:
            log_error(f"Failed to load guidance: {e}")
            GUIDANCE_AVAILABLE = False
            return False

    else:
        # Subsequent story in batch: Reuse cached guidance

        if GUIDANCE_CACHE and LOADED_PATTERNS:
            log_info(f"Batch mode: Reusing cached guidance (story {batch_index + 1})")
            GUIDANCE_AVAILABLE = True
            return True
        else:
            # Cache miss: Attempt recovery load
            log_warning(f"Guidance cache miss (story {batch_index + 1}), attempting recovery")
            return load_user_input_guidance()  # Recursive: try fresh load


# Execute Step 0
load_user_input_guidance()

# Global flags set for use in Steps 3-5:
# GUIDANCE_AVAILABLE: bool (patterns available for application)
# LOADED_PATTERNS: dict (extracted patterns, keyed by normalized name)
```

**Success Indicators:**
- `GUIDANCE_AVAILABLE = true` (patterns loaded)
- Log message: "Guidance loaded: X patterns extracted"

**Graceful Degradation:**
- If file missing: `GUIDANCE_AVAILABLE = false`, use baseline questions
- If < 4 patterns: `GUIDANCE_AVAILABLE = false`, use baseline questions
- If exception: Catch, log error, set `GUIDANCE_AVAILABLE = false`, continue

**Batch Caching:**
- Story 1 (batch_index=0): Load guidance, cache in GUIDANCE_CACHE
- Stories 2-9 (batch_index>0): Reuse GUIDANCE_CACHE (no re-read)
- Token overhead: ~1,000 tokens for first story, ~0 for stories 2-9
- Amortized: 1,000 tokens / 9 stories = ~111 tokens/story

**See:** `references/user-input-integration-guide.md` Section 2 for batch caching details

---

## Step 1.0: Detect Execution Mode (NEW - Batch Support)

**Check for batch mode marker:**
```
if conversation contains "**Batch Mode:** true":
    BATCH_MODE = true
    → Proceed to Step 1.0.1 (Batch Mode Branch)
else:
    BATCH_MODE = false
    → Proceed to Step 1.1 (Interactive Mode Branch - normal workflow)
```

---

## Step 1.0.1: Batch Mode Branch (NEW)

**Extract all metadata from context markers:**
```
# Required markers
STORY_ID = extract_from_conversation("**Story ID:**")
EPIC_ID = extract_from_conversation("**Epic ID:**")
FEATURE_DESC = extract_from_conversation("**Feature Description:**")
PRIORITY = extract_from_conversation("**Priority:**")
POINTS = extract_from_conversation("**Points:**")
SPRINT = extract_from_conversation("**Sprint:**")

# Optional markers
FEATURE_NUM = extract_from_conversation("**Feature Number:**")
FEATURE_NAME = extract_from_conversation("**Feature Name:**")
BATCH_INDEX = extract_from_conversation("**Batch Index:**")
```

**Validate all required markers present:**
```
required_markers = [STORY_ID, EPIC_ID, FEATURE_DESC, PRIORITY, POINTS, SPRINT]

if not all(required_markers):
    Display: """
    ⚠️ Batch mode requires all metadata markers
    Missing: {list_missing_markers}

    Fallback: Switching to interactive mode to ask questions
    """
    BATCH_MODE = false
    → Proceed to Step 1.1 (Interactive Mode)
```

**Convert Points to integer:**
```
POINTS = int(POINTS)  # "5" → 5

# Validate Fibonacci
if POINTS not in [1, 2, 3, 5, 8, 13, 21]:
    WARNING: f"Non-Fibonacci points: {POINTS}"
```

**Log batch mode activation:**
```
Display: f"""
ℹ️ Batch Mode Activated
- Story: {STORY_ID} (Feature {FEATURE_NUM}: {FEATURE_NAME})
- Epic: {EPIC_ID}
- Priority: {PRIORITY}, Points: {POINTS}, Sprint: {SPRINT}
- Skipping interactive questions (using provided metadata)
"""
```

**Return Phase 1 output (skip all AskUserQuestion flows):**
```
phase1_result = {
    "story_id": STORY_ID,
    "epic_id": EPIC_ID,
    "feature_description": FEATURE_DESC,
    "feature_number": FEATURE_NUM,
    "feature_name": FEATURE_NAME,
    "priority": PRIORITY,
    "points": POINTS,
    "sprint": SPRINT,
    "batch_mode": true,
    "batch_index": BATCH_INDEX
}

→ Proceed directly to Phase 2 (Requirements Analysis)
```

---

## Step 1.1: Feature Description Capture (Interactive Mode)

**Objective:** Extract feature description from conversation context

**Extract feature description from conversation context:**

Look for patterns in conversation:
- "Feature:" or "Feature Description:"
- $ARGUMENTS from /create-story command
- User message describing feature

**If description missing or vague:**
```
AskUserQuestion(
  questions=[{
    question: "Please describe the feature you want to create a story for",
    header: "Feature description",
    options: [
      {
        label: "CRUD operation",
        description: "Create, read, update, or delete data (e.g., manage users, products)"
      },
      {
        label: "Authentication/Authorization",
        description: "Login, signup, permissions, access control"
      },
      {
        label: "Workflow/Process",
        description: "Multi-step process or state transitions (e.g., order processing)"
      },
      {
        label: "Reporting/Analytics",
        description: "Data visualization, reports, dashboards"
      }
    ],
    multiSelect: false
  }]
)
```

Then ask: "Provide detailed description of the {feature_type} feature"

**Minimum requirements:**
- At least 10 words
- Describes WHAT users will do (not HOW to implement)
- Identifies WHO will use it (role/persona)

---

## Step 1.2: Generate Next Story ID (Enhanced - Gap-Aware)

**Objective:** Generate sequential story ID (STORY-NNN format) with gap detection and filling

**Find all existing stories:**
```
story_files = Glob(pattern=".ai_docs/Stories/STORY-*.story.md")

# Parse story numbers from filenames
# Example: STORY-042-user-login.story.md → 42
story_numbers = []
for filename in story_files:
    # Extract number using regex: STORY-(\d{3})
    match = re.search(r'STORY-(\d{3})', filename)
    if match:
        story_numbers.append(int(match.group(1)))

# Sort numbers for gap detection
story_numbers.sort()
```

**Gap-Aware ID Calculation:**
```
if not story_numbers:
    # No existing stories, start at 1
    next_number = 1
    gap_filled = False
else:
    max_number = max(story_numbers)

    # Check for gaps in sequence
    # Example: [1, 2, 3, 5, 7] → gaps at 4, 6
    all_numbers = set(range(1, max_number + 1))
    existing_set = set(story_numbers)
    gaps = sorted(all_numbers - existing_set)

    if gaps:
        # Fill first gap
        next_number = gaps[0]
        gap_filled = True
        Display: f"ℹ️ Filling gap at STORY-{next_number:03d}"
    else:
        # No gaps, increment from max
        next_number = max_number + 1
        gap_filled = False

story_id = f"STORY-{next_number:03d}"
```

**Examples:**
- Existing: [] → Next: STORY-001 (first story)
- Existing: [1, 2, 3] → Next: STORY-004 (sequential, no gaps)
- Existing: [1, 2, 5, 7] → Next: STORY-003 (fills gap at 3)
- After creating STORY-003: [1, 2, 3, 5, 7] → Next: STORY-004 (fills gap at 4)
- After creating STORY-004: [1, 2, 3, 4, 5, 7] → Next: STORY-006 (fills gap at 6)
- After creating STORY-006: [1, 2, 3, 4, 5, 6, 7] → Next: STORY-008 (no gaps, increment)

**ID Format:** STORY-NNN where NNN is zero-padded 3-digit number

**Conflict Detection:**
- Gap filling ensures gaps are filled before incrementing
- Maintains sequential numbering (prevents fragmentation)
- Recalculate ID for each story in batch mode (accounts for just-created stories)

**Track with TodoWrite:**
```
TodoWrite([
  f"Create {story_id}: [feature description]"
])
```

---

## Step 1.3: Discover Epic Context (Enhanced with Guidance Pattern)

**Objective:** Find and associate story with epic (if applicable)

**Guidance Pattern Applied:** Explicit Classification + Bounded Choice

**Find available epics:**
```
epic_files = Glob(pattern=".ai_docs/Epics/EPIC-*.epic.md")

epic_options = []
for epic_file in epic_files:
    # Read frontmatter only (first 20 lines)
    content = Read(file_path=epic_file, limit=20)

    # Extract: id, title, status, feature_count, complexity
    epic_options.append({
        "label": "{id}: {title}",
        "description": "Status: {status} | {feature_count} features | Complexity: {complexity}"
    })
```

**Ask user for epic association (Pattern-Enhanced if Guidance Available):**

**If GUIDANCE_AVAILABLE:**
```
AskUserQuestion(
  questions=[{
    question: "Associate this story with an epic for feature tracking and traceability",
    header: "Epic Linkage - Explicit Classification + Bounded Choice (Pattern-Applied)",
    options: epic_options + [
      {
        label: "None - Standalone Story",
        description: "No epic association (independent work, one-off feature)"
      }
    ],
    multiSelect: false
  }]
)
```

**Else (Baseline):**
```
AskUserQuestion(
  questions=[{
    question: "Which epic does this story belong to?",
    header: "Epic association",
    options: epic_options + [
      {
        label: "None - standalone story",
        description: "This story is not part of any epic"
      }
    ],
    multiSelect: false
  }]
)
```

**Pattern Details:**
- **Explicit Classification:** Epic options grouped by status (Active/Planning) with clear descriptions
- **Bounded Choice:** Present as bounded list (not open-ended "other" field)
- **"None" Option Explicit:** Clear label "None - Standalone Story" with explanation
- **Context Descriptions:** Status, feature count, complexity level for each epic
- **Question Explains Purpose:** "Feature tracking and traceability" helps user understand why epic matters

**See:** `references/user-input-integration-guide.md` Section 6 Example 1 for before/after comparison

**Result:** epic_id (or null if standalone)

---

## Step 1.4: Discover Sprint Context (Enhanced with Guidance Pattern)

**Objective:** Find and assign story to sprint (or backlog)

**Guidance Pattern Applied:** Bounded Choice

**Find available sprints:**
```
sprint_files = Glob(pattern=".ai_docs/Sprints/Sprint-*.md")

# Sort chronologically by start date
sprints_sorted = sort_by_start_date(sprint_files)

sprint_options = []
for sprint_file in sprints_sorted:
    content = Read(file_path=sprint_file, limit=30)

    # Calculate capacity usage
    points_used = extract_metric(content, "points_used")
    points_total = extract_metric(content, "points_capacity")
    percent_used = (points_used / points_total) * 100

    # Capacity indicator (for pattern application)
    if percent_used >= 85:
        capacity_indicator = "LIMITED CAPACITY"
    elif percent_used >= 50:
        capacity_indicator = "GOOD CAPACITY"
    else:
        capacity_indicator = "AVAILABLE"

    sprint_options.append({
        "label": "{sprint_id}: {start} - {end}",
        "description": "{points_used}/{points_total} points used ({percent_used}%) - {capacity_indicator}"
    })
```

**Ask user for sprint association (Pattern-Enhanced if Guidance Available):**

**If GUIDANCE_AVAILABLE:**
```
AskUserQuestion(
  questions=[{
    question: "Assign story to sprint with available capacity",
    header: "Sprint Assignment - Bounded Choice (Pattern-Applied)",
    options: sprint_options + [
      {
        label: "Backlog",
        description: "Not assigned to sprint (default, no deadline)"
      }
    ],
    multiSelect: false
  }]
)
```

**Else (Baseline):**
```
AskUserQuestion(
  questions=[{
    question: "Assign to sprint?",
    header: "Sprint",
    options: sprint_options + [
      {
        label: "Backlog",
        description: "Not assigned to any sprint yet"
      }
    ],
    multiSelect: false
  }]
)
```

**Pattern Details:**
- **Bounded Choice:** Present sprints as bounded list (not open-ended)
- **Capacity Information:** Show points used/capacity and percentage for each sprint
- **Chronological Sorting:** List sprints by start date (soonest first)
- **"Backlog" Option Explicit:** Clear as default option with explanation
- **Visual Indicators:** LIMITED/GOOD/AVAILABLE capacity hints for user decision

**See:** `references/user-input-integration-guide.md` Section 6 Example 2 for before/after comparison

**Result:** sprint_id (or "Backlog")

---

## Step 1.5: Collect Story Metadata (Enhanced with Guidance Patterns)

**Objective:** Gather priority and story points via user questions

**Guidance Patterns Applied:**
- Priority: Explicit Classification
- Points: Fibonacci Bounded Choice

### Priority Selection (Pattern: Explicit Classification)

**If GUIDANCE_AVAILABLE:**
```
AskUserQuestion(
  questions=[{
    question: "Select priority level based on business impact",
    header: "Story Priority - Explicit Classification (Pattern-Applied)",
    options: [
      {
        label: "Critical",
        description: "Blocking other work - must be done immediately "
                    "(blocks team productivity, prevents other features)"
      },
      {
        label: "High",
        description: "Important for current sprint - significant business value "
                    "(high impact, stakeholder priority)"
      },
      {
        label: "Medium",
        description: "Valuable feature - can be deferred if needed "
                    "(standard priority, normal sprint pace)"
      },
      {
        label: "Low",
        description: "Nice to have - deferred without impact "
                    "(low priority, can wait for future sprint)"
      }
    ],
    multiSelect: false
  }]
)
```

**Else (Baseline):**
```
AskUserQuestion(
  questions=[{
    question: "What is the priority of this story?",
    header: "Priority",
    options: [
      {
        label: "Critical",
        description: "Blocking other work, must be done immediately"
      },
      {
        label: "High",
        description: "Important for upcoming release"
      },
      {
        label: "Medium",
        description: "Should be done soon"
      },
      {
        label: "Low",
        description: "Nice to have, can be deferred"
      }
    ],
    multiSelect: false
  }]
)
```

**Pattern Details (Explicit Classification):**
- **Exactly 4 levels:** Critical, High, Medium, Low (no "Other" option)
- **Business Impact Descriptions:** Each level explains impact on team/business
- **Parenthetical Context:** Clarifies what each level means in practice
- **No vague terms:** All descriptions quantified (blocks, stakeholder, standard, deferred)

**See:** `references/user-input-integration-guide.md` Section 6 Example 3 for before/after comparison

### Story Points Selection (Pattern: Fibonacci Bounded Choice)

**If GUIDANCE_AVAILABLE:**
```
AskUserQuestion(
  questions=[{
    question: "Estimate story complexity on Fibonacci scale",
    header: "Story Points - Fibonacci Bounded Choice (Pattern-Applied)",
    options: [
      {
        label: "1 point",
        description: "Trivial - Few hours, minimal complexity "
                    "(straightforward task, well-defined scope)"
      },
      {
        label: "2 points",
        description: "Simple - Half day, straightforward implementation "
                    "(well-understood, low risk)"
      },
      {
        label: "3 points",
        description: "Standard - 1 day, moderate complexity "
                    "(typical story, normal implementation effort)"
      },
      {
        label: "5 points",
        description: "Complex - 2-3 days, multiple components "
                    "(requires design, multiple changes)"
      },
      {
        label: "8 points",
        description: "Very complex - 3-5 days, significant work "
                    "(many unknowns, significant implementation)"
      },
      {
        label: "13 points",
        description: "Extremely complex - Consider splitting story "
                    "(high risk, recommend decomposition)"
      }
    ],
    multiSelect: false
  }]
)
```

**Else (Baseline):**
```
AskUserQuestion(
  questions=[{
    question: "Estimate story complexity (Fibonacci scale)",
    header: "Story points",
    options: [
      {
        label: "1",
        description: "Trivial - Few hours, minimal complexity"
      },
      {
        label: "2",
        description: "Simple - Half day, straightforward implementation"
      },
      {
        label: "3",
        description: "Standard - 1 day, moderate complexity"
      },
      {
        label: "5",
        description: "Complex - 2-3 days, multiple components"
      },
      {
        label: "8",
        description: "Very complex - 3-5 days, significant work"
      },
      {
        label: "13",
        description: "Extremely complex - Consider splitting story"
      }
    ],
    multiSelect: false
  }]
)
```

**If user selects 13 points (Trigger Warning):**
```
if user_selection == "13 points":
    log_warning("13-point story selected - high scope risk")

    AskUserQuestion(
      questions=[{
        question: "13-point stories risk scope creep. Decompose into smaller stories?",
        header: "⚠️ Large Story Risk",
        options: [
          {
            label: "Split into 2-3 stories",
            description: "Recommended: Reduce risk, improve delivery certainty"
          },
          {
            label: "Proceed with 13 points",
            description: "Acknowledge risk, proceed with current scope"
          }
        ],
        multiSelect: false
      }]
    )
```

**Pattern Details (Fibonacci Bounded Choice):**
- **Exactly 6 Fibonacci values:** 1, 2, 3, 5, 8, 13 (no other options)
- **Time Estimates:** Each value includes hours/days estimate
- **Complexity Rationale:** Explains type of complexity for each level
- **Parenthetical Context:** Shows risk/effort indicators
- **13-Point Warning:** Triggers split recommendation for large stories

**See:** `references/user-input-integration-guide.md` Section 6 Example 4 for before/after comparison

**Metadata collected:**
- story_id (generated)
- epic_id (user selected or null)
- sprint_id (user selected or "Backlog")
- priority (Critical/High/Medium/Low) - Enhanced with business impact descriptions
- points (1/2/3/5/8/13) - Enhanced with complexity rationale, warning for 13

---

## Subagent Invocation

None in this phase. Discovery is interactive (AskUserQuestion).

---

## Output

**Phase 1 produces:**
- story_id: STORY-NNN format
- epic_id: EPIC-NNN or null
- sprint_id: Sprint-N or "Backlog"
- priority: Critical/High/Medium/Low
- points: 1/2/3/5/8/13
- feature_description: User-provided text

---

## Error Handling

**Error 1: No existing stories (first story)**
- **Detection:** Glob returns empty list
- **Recovery:** Set next_number = 1, generate STORY-001

**Error 2: Vague feature description**
- **Detection:** Description <10 words or missing WHO/WHAT
- **Recovery:** Re-prompt with AskUserQuestion for more detail

**Error 3: 13-point story selected**
- **Detection:** User selects "13" option
- **Recovery:** Warn about story size, recommend splitting, offer to proceed or cancel

See `error-handling.md` for comprehensive error recovery procedures.

---

## Next Phase

**After Phase 1 completes →** Phase 2: Requirements Analysis

Load `requirements-analysis.md` for Phase 2 workflow.
