---
name: story-discovery
description: Phase 1 reference for story ID generation, epic/sprint context discovery, and metadata collection
version: "2.0"
---

# Phase 1: Story Discovery & Context

This phase generates story ID, discovers epic/sprint context, and collects metadata.

## Overview

Story creation begins with discovery: assigning a unique ID, determining relationships to epics/sprints, and gathering essential metadata through user interaction.

**Execution Modes:**
- **Interactive Mode:** Ask user questions for all metadata (normal)
- **Batch Mode:** Extract metadata from context markers (batch creation from epics)

---

## Epic Batch Workflow (Steps 0.1-0.6)

When invoked with **Mode:** EPIC_BATCH marker, the skill performs feature extraction, multi-select, and batch story creation directly. These steps run BEFORE Step 1.0.

---

## Step 0.1: Batch Mode Detection

**Objective:** Detect EPIC_BATCH mode marker and extract Epic ID from conversation context

**Check for EPIC_BATCH mode marker:**
```
if conversation contains "**Mode:** EPIC_BATCH":
    # Batch mode detected - check for required Epic ID
    if conversation contains "**Epic ID:** EPIC-":
        BATCH_MODE = "epic_batch"
        EPIC_ID = extract_from_conversation("**Epic ID:**")
        # Validate Epic ID format
        if not re.match(r'^EPIC-\d{3}$', EPIC_ID):
            Display: "⚠️ Invalid Epic ID format: {EPIC_ID}. Expected EPIC-NNN."
            → Fallback to Step 1.0 (Interactive Mode)
        else:
            Display: "ℹ️ EPIC_BATCH mode detected for {EPIC_ID}"
            → Proceed to Step 0.2 (Feature Extraction)
    else:
        # EPIC_BATCH marker present but Epic ID missing
        Display: """
        ⚠️ EPIC_BATCH mode requires **Epic ID:** marker

        Missing: **Epic ID:** EPIC-NNN

        Fallback: Switching to interactive mode
        """
        BATCH_MODE = false
        → Fallback to Step 1.0 (Interactive Mode)
else:
    # No EPIC_BATCH marker - proceed to existing batch mode detection
    → Proceed to Step 1.0 (Detect Execution Mode)
```

**Fallback Path:** If markers incomplete, fall back to Step 1.0 for interactive or standard batch mode.

---

## Step 0.2: Extract Features from Epic

**Objective:** Locate epic file and extract all features with metadata

**Find epic file:**
```
epic_pattern = f"devforgeai/specs/Epics/{EPIC_ID}*.epic.md"
epic_files = Glob(pattern=epic_pattern)

if not epic_files:
    Display: f"""
    ⚠️ Epic file not found: {epic_pattern}

    Fallback: Switching to interactive single story mode
    """
    BATCH_MODE = false
    → Fallback to Step 1.1 (Interactive Mode)

epic_file = epic_files[0]  # First match
```

**Read and parse epic content:**
```
epic_content = Read(file_path=epic_file)

# Extract features using ### Feature headers
# Pattern: ### Feature N: Feature Name
# or: ### Feature: Feature Name
features = []
feature_regex = r'### Feature\s*(\d+)?:?\s*(.+?)(?:\n|\r\n)([\s\S]*?)(?=### Feature|## |$)'

for match in re.finditer(feature_regex, epic_content):
    feature_num = match.group(1) or str(len(features) + 1)
    feature_name = match.group(2).strip()
    feature_desc = match.group(3).strip()[:500]  # Limit description length

    features.append({
        "number": feature_num,
        "name": feature_name,
        "description": feature_desc
    })

if not features:
    Display: f"""
    ⚠️ No features found in {epic_file}

    Expected format: ### Feature N: Feature Name

    Options:
    - Add features to epic file
    - Enter feature description manually
    """

    AskUserQuestion:
      Question: "No features found. How would you like to proceed?"
      Options:
        - "Enter description manually" → Fallback to Step 1.1
        - "Abort batch creation"
    → Handle user choice

Display: f"✓ Extracted {len(features)} features from {EPIC_ID}"
```

---

## Step 0.3: Multi-Select Features

**Objective:** Present features for user selection (unless pre-selected in context)

**Check for pre-selected features:**
```
if conversation contains "**Selected Features:**":
    # Features already specified in context
    pre_selected = extract_from_conversation("**Selected Features:**")
    selected_features = parse_feature_list(pre_selected)

    Display: f"ℹ️ Using pre-selected features: {selected_features}"
    → Proceed to Step 0.4 (Metadata Collection)
```

**Present features via AskUserQuestion:**
```
feature_options = []
for f in features:
    # Truncate description to 100 chars for display
    truncated_desc = f["description"][:100] + "..." if len(f["description"]) > 100 else f["description"]

    feature_options.append({
        "label": f"Feature {f['number']}: {f['name']}",
        "description": truncated_desc
    })

AskUserQuestion(
  questions=[{
    question: f"Select features to create stories for ({len(features)} available)",
    header: "Feature selection",
    options: feature_options,
    multiSelect: true
  }]
)

# Process user selection
if not selected_features or len(selected_features) == 0:
    Display: "⚠️ No features selected. Please select at least one feature."
    → Re-prompt with same AskUserQuestion

Display: f"✓ {len(selected_features)} feature(s) selected for story creation"
```

---

## Step 0.4: Batch Metadata Collection

**Objective:** Collect default metadata to apply to all selected stories

**Collect sprint assignment:**
```
sprint_files = Glob(pattern="devforgeai/specs/Sprints/Sprint-*.md")

sprint_options = [
    {"label": "Backlog", "description": "Not assigned to any sprint yet"}
]
for sprint in sprint_files:
    sprint_options.append({
        "label": extract_sprint_id(sprint),
        "description": "Active sprint"
    })

AskUserQuestion(
  questions=[{
    question: "Assign all stories to which sprint?",
    header: "Sprint",
    options: sprint_options,
    multiSelect: false
  }]
)

DEFAULT_SPRINT = user_selection  # "Backlog" or "Sprint-N"
```

**Collect default priority:**
```
AskUserQuestion(
  questions=[{
    question: "Default priority for batch stories?",
    header: "Priority",
    options: [
      {"label": "Critical", "description": "Blocking other work"},
      {"label": "High", "description": "Important for upcoming release"},
      {"label": "Medium", "description": "Should be done soon"},
      {"label": "Low", "description": "Nice to have"}
    ],
    multiSelect: false
  }]
)

DEFAULT_PRIORITY = user_selection
```

**Collect default story points:**
```
AskUserQuestion(
  questions=[{
    question: "Default story points for batch? (can override per-story)",
    header: "Points",
    options: [
      {"label": "1", "description": "Trivial - few hours"},
      {"label": "2", "description": "Simple - half day"},
      {"label": "3", "description": "Standard - 1 day"},
      {"label": "5", "description": "Complex - 2-3 days"},
      {"label": "8", "description": "Very complex - 3-5 days"},
      {"label": "13", "description": "Extremely complex - consider splitting"}
    ],
    multiSelect: false
  }]
)

DEFAULT_POINTS = int(user_selection)

Display: f"""
✓ Batch defaults configured:
  - Sprint: {DEFAULT_SPRINT}
  - Priority: {DEFAULT_PRIORITY}
  - Points: {DEFAULT_POINTS}
"""
```

---

## Step 0.5: Create Loop Context for Batch

**Objective:** Iterate over selected features and create stories

**Initialize tracking:**
```
created_stories = []  # Successfully created
failed_stories = []   # Failed with reasons
batch_total = len(selected_features)
batch_index = 0
```

**Loop over selected features:**
```
FOR each feature in selected_features:
    batch_index += 1

    Display: f"""
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    Creating story {batch_index}/{batch_total}
    Feature: {feature['name']}
    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
    """

    TRY:
        # Step 0.5.1: Generate unique STORY-NNN ID
        # (Reuses Step 1.2 gap-aware logic - recalculates each iteration)
        story_id = generate_next_story_id()  # Uses gap-aware logic from Step 1.2

        # Step 0.5.2: Set batch context markers for Phases 2-7
        batch_context = f"""
        **Batch Mode:** true
        **Story ID:** {story_id}
        **Epic ID:** {EPIC_ID}
        **Feature Number:** {feature['number']}
        **Feature Name:** {feature['name']}
        **Feature Description:** {feature['description']}
        **Priority:** {DEFAULT_PRIORITY}
        **Points:** {DEFAULT_POINTS}
        **Sprint:** {DEFAULT_SPRINT}
        **Batch Index:** {batch_index}/{batch_total}
        """

        # Step 0.5.3: Execute Phases 2-7 for this story
        # Phase 2: Requirements Analysis
        # Phase 3: Acceptance Criteria Creation
        # Phase 4: Technical Specification
        # Phase 5: UI Specification (if applicable)
        # Phase 6: Story File Generation
        # Phase 7: Self-Validation

        → Execute Phase 2 with batch_context markers
        → Execute Phases 3-7 sequentially

        # Step 0.5.4: Record success
        story_file = f"devforgeai/specs/Stories/{story_id}-{slugify(feature['name'])}.story.md"
        created_stories.append({
            "story_id": story_id,
            "feature": feature['name'],
            "file_path": story_file
        })

        Display: f"✓ Created {story_id}: {feature['name']}"

    EXCEPT Exception as e:
        # Step 0.5.5: Failure isolation - continue with next feature
        failed_stories.append({
            "feature": feature['name'],
            "feature_number": feature['number'],
            "reason": str(e),
            "step": "Phase 2-7"
        })

        Display: f"✗ Failed to create story for Feature {feature['number']}: {e}"

        # Continue to next feature (failure isolation per BR-004)
        continue
```

---

## Step 0.6: Return Batch Summary

**Objective:** Generate summary of batch creation results

**Generate summary:**
```
batch_summary = {
    "total_attempted": batch_total,
    "created_count": len(created_stories),
    "failed_count": len(failed_stories),
    "created_stories": created_stories,
    "failed_stories": failed_stories
}

Display: f"""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Batch Story Creation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Total Attempted: {batch_total}
Successfully Created: {len(created_stories)}
Failed: {len(failed_stories)}
"""

# List created stories
if created_stories:
    Display: """
    ✓ Created Stories:
    """
    for story in created_stories:
        Display: f"    - {story['story_id']}: {story['feature']}"
        Display: f"      File: {story['file_path']}"

# List failures with reasons
if failed_stories:
    Display: """
    ✗ Failed Stories:
    """
    for failure in failed_stories:
        Display: f"    - Feature {failure['feature_number']}: {failure['feature']}"
        Display: f"      Reason: {failure['reason']}"

# Suggested next actions
Display: """

Suggested Next Actions:
"""
if created_stories:
    Display: f"  • Run /dev {created_stories[0]['story_id']} to implement first story"
if failed_stories:
    Display: "  • Review failed features and retry individually with /create-story"
if len(created_stories) > 1:
    Display: "  • Use /create-sprint to organize stories into sprints"

Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

**Return to command:**
```
return batch_summary
# Command receives summary and displays to user
```

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
story_files = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")

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

## Step 1.3: Discover Epic Context

**Objective:** Find and associate story with epic (if applicable)

**Find available epics:**
```
epic_files = Glob(pattern="devforgeai/specs/Epics/EPIC-*.epic.md")

epic_options = []
for epic_file in epic_files:
    # Read frontmatter only (first 20 lines)
    content = Read(file_path=epic_file, limit=20)

    # Extract: id, title, status
    epic_options.append({
        "label": "{id}: {title}",
        "description": "Status: {status}, Features: {feature_count}"
    })
```

**Ask user for epic association:**
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

**Result:** epic_id (or null if standalone)

---

## Step 1.4: Discover Sprint Context

**Objective:** Find and assign story to sprint (or backlog)

**Find available sprints:**
```
sprint_files = Glob(pattern="devforgeai/specs/Sprints/Sprint-*.md")

sprint_options = []
for sprint_file in sprint_files:
    content = Read(file_path=sprint_file, limit=30)

    sprint_options.append({
        "label": "{sprint_id}",
        "description": "Dates: {start} - {end}, Capacity: {points} points"
    })
```

**Ask user for sprint association:**
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

**Result:** sprint_id (or "Backlog")

---

## Step 1.5: Collect Story Metadata

**Objective:** Gather priority and story points via user questions

**Ask for priority:**
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

**Ask for story points:**
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

**If user selects 13 points:**
```
WARNING: Story might be too large (13 points)

Recommend splitting into smaller stories (3-5 points each)

Proceed anyway or split?
```

**Metadata collected:**
- story_id (generated)
- epic_id (user selected or null)
- sprint_id (user selected or "Backlog")
- priority (Critical/High/Medium/Low)
- points (1/2/3/5/8/13)

---

## Step 1.6: Collect Story Dependencies (OPTIONAL)

**Objective:** Collect optional story dependencies for parallel development workflows

**Interactive Mode:**

```
AskUserQuestion(
  questions=[{
    question: "Does this story depend on other stories that must complete first? (optional)",
    header: "Dependencies",
    options: [
      {
        label: "None (Recommended)",
        description: "No dependencies - story can start immediately"
      },
      {
        label: "Enter dependencies",
        description: "Specify STORY-IDs this story depends on"
      }
    ],
    multiSelect: false
  }]
)
```

**If user selects "Enter dependencies":**

```
AskUserQuestion(
  questions=[{
    question: "Enter dependent story IDs (comma-separated, e.g., STORY-044, STORY-045)",
    header: "Dependency IDs",
    text: true
  }]
)
```

**Normalization Logic:**

```python
def normalize_depends_on_input(input):
    # None/empty → []
    if input is None or input == "" or input.lower() == "none":
        return []

    # Already array → validate and return
    if isinstance(input, list):
        return validate_and_filter(input)

    # Parse comma/space-separated string
    ids = re.split(r'[,\s]+', input.strip())
    validated = []

    for id in ids:
        cleaned = id.strip().upper()
        if re.match(r'^STORY-\d{3,4}$', cleaned):
            validated.append(cleaned)
        else:
            Display: f"⚠️ Invalid format '{id}' - expected STORY-NNN. Skipping."

    return validated
```

**Validation Warnings:**

```
IF depends_on is not empty:
    FOR each story_id in depends_on:
        story_files = Glob(pattern=f"devforgeai/specs/Stories/{story_id}*.story.md")
        IF not story_files:
            Display: f"⚠️ Note: {story_id} not found. Dependency recorded."
```

**Batch Mode Integration:**

In batch mode (Step 1.0.1), extract from context markers:

```
DEPENDS_ON = extract_from_conversation("**Depends On:**")
IF DEPENDS_ON:
    depends_on = normalize_depends_on_input(DEPENDS_ON)
ELSE:
    depends_on = []
```

**Result:** `depends_on` array (empty `[]` if no dependencies)

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
- depends_on: Array of STORY-IDs or [] (from Step 1.6)
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
