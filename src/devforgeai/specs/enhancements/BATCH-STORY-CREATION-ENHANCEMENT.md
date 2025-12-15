# Enhancement: Batch Story Creation from Epics

**Date:** 2025-11-06
**Type:** Feature Enhancement
**Priority:** MEDIUM
**Complexity:** 7/10
**Total Effort:** 13-19 hours (6 phases)
**Status:** Specification Complete - Ready for Implementation

---

## Executive Summary

Enable batch story creation from epics via `/create-story epic-001` command, allowing users to create multiple stories in a single execution instead of running the command multiple times.

**Current State:** 7 features = 7 command executions
**Desired State:** 7 features = 1 command execution with multi-select

**User Experience Improvement:**
- **Time saved:** 14 minutes sequential → 6 minutes batch (57% faster with parallel optimization)
- **Interactions reduced:** 14 questions (7×2) → 4 questions (2 batch + 2 per-epic)
- **Cognitive load:** Lower (batch decisions vs. repeated decisions)

---

## User Request (From output2.md Lines 1431-2054)

**Original Request:**
> "How do we enhance the story creation to create stories per epic document? For example, if I provide `/create-story epic-001`, I would like claude to create every story file related to epic-001 in sequence with the next numbering based on the devforgeai/specs/stories/ numbering sequence of next story #."

**Requirements:**
1. ✅ Detect epic reference in command argument (`epic-001` pattern)
2. ✅ Extract ALL features from epic document
3. ✅ Allow user to select which features to create stories for (multi-select)
4. ✅ Create stories sequentially with auto-incrementing IDs (STORY-009, STORY-010, ...)
5. ✅ Link all stories to epic and optional sprint
6. ✅ Reduce interaction burden (batch metadata instead of per-story)

---

## Design Constraints (Claude Code Terminal)

### ✅ What IS Possible

- **Sequential story creation in single execution** - Loop through features
- **Reading epic files** - Glob + Read tools
- **Auto-incrementing story IDs** - Parse existing, calculate next
- **Multi-select questions** - AskUserQuestion with `multiSelect: true`
- **Pseudo-parallel subagent invocation** - Multiple Task calls in single message (40-60% speedup)
- **Progress tracking** - TodoWrite for visual feedback
- **File creation loops** - Write tool in loop

### ❌ What is NOT Possible (Limitations)

- **True parallel execution** - Subagents run sequentially (pseudo-parallel at best)
- **Real-time progress bars** - No UI updates during skill execution
- **Transactional rollback** - If story #5 fails, stories 1-4 already created
- **Streaming output** - User sees nothing until skill completes
- **Interrupt/cancel mid-batch** - Once started, runs to completion

---

## Enhancement Design

### Current Workflow (Single Story Mode)

```
User: /create-story User registration form

Command Flow:
1. Parse argument: "User registration form" (feature description)
2. Set context marker: **Feature Description:** User registration form
3. Invoke skill: Skill(command="devforgeai-story-creation")
4. Skill Phase 1: Ask epic/sprint, priority, points
5. Skill Phase 2-8: Generate single story
6. Output: STORY-XXX-user-registration-form.story.md

Time: ~2 minutes
Questions: 4-5 (epic, sprint, priority, points, next action)
```

### NEW Workflow (Batch Mode from Epic)

```
User: /create-story epic-001

Command Flow:
1. Parse argument: "epic-001" → Detect epic pattern
2. Read EPIC-001, extract 7 features
3. AskUserQuestion: "Select features to create stories for" (multi-select)
4. User selects: Features 1.1, 1.2, 1.3, 1.4, 1.5, 1.6, 1.7 (all 7)
5. AskUserQuestion (batch): "Sprint for all stories?" → Sprint-1
6. AskUserQuestion (batch): "Priority for all stories?" → Inherit from epic (Critical)
7. Loop: For each selected feature:
   - Calculate next story ID (STORY-009, STORY-010, ...)
   - Set context markers (story ID, epic, feature, priority, points, sprint)
   - Invoke skill: Skill(command="devforgeai-story-creation")
   - Skill executes in batch mode (skips interactive questions)
   - Update TodoWrite progress
8. Update epic with all story references
9. Display batch completion summary

Time: ~6 minutes (with parallel optimization, ~14 min sequential)
Questions: 4 (feature selection, sprint batch, priority batch, next action)
Output: 7 .story.md files (STORY-009 through STORY-015)
```

---

## Implementation Phases

### Phase 1: Basic Batch Mode (4-6 hours)

**Goal:** Enable epic detection and sequential story creation.

#### Files to Modify

**1. `.claude/commands/create-story.md`**

**Add argument detection logic (Phase 0):**

```markdown
### Phase 0: Argument Validation and Mode Detection (ENHANCED - Batch Mode Support)

**Validate and detect input type:**
```python
args = "$1"  # First positional argument

# Mode 1: Epic reference (epic-001, EPIC-001)
if re.match(r'^epic-\d{3}$', args.lower(), re.IGNORECASE):
    mode = "EPIC_BATCH_MODE"
    epic_id = args.upper().replace("EPIC-", "EPIC-")  # Normalize to EPIC-001

    # Validate epic exists
    epic_files = Glob(pattern=f"devforgeai/specs/Epics/{epic_id}*.epic.md")

    if not epic_files:
        AskUserQuestion:
            question: f"Epic {epic_id} not found. What should I do?"
            options:
                - "List available epics"
                - "Enter different epic ID"
                - "Cancel command"

    epic_file = epic_files[0]

    → Proceed to Epic Batch Workflow (NEW)

# Mode 2: Feature description (10+ words)
elif len(args.split()) >= 10:
    mode = "SINGLE_STORY_MODE"
    feature_description = args

    → Proceed to Single Story Workflow (EXISTING)

# Mode 3: Ambiguous (too short)
else:
    AskUserQuestion:
        question: "Is this an epic ID or feature description?"
        header: "Input type"
        options:
            - label: "Epic ID"
              description: "Create multiple stories from epic features"
            - label: "Feature description"
              description: "Create single story from this description"
        multiSelect: false

    # Based on user response, extract epic_id or feature_description
    # Then branch to appropriate workflow
```
```

**Add Epic Batch Workflow (NEW section after Phase 0):**

```markdown
## Epic Batch Workflow (NEW - Batch Story Creation Enhancement)

**Triggered when:** Argument matches pattern `epic-\d{3}` (e.g., epic-001, EPIC-002)

**Objective:** Create multiple stories from epic features in single execution.

---

### Step 1: Read Epic and Extract Features

**Read epic file:**
```python
epic_file = Glob(pattern=f"devforgeai/specs/Epics/{epic_id}*.epic.md")[0]
epic_content = Read(file_path=epic_file)
```

**Parse epic frontmatter for metadata:**
```yaml
# Extract from YAML frontmatter
epic_priority = extract_yaml_field(epic_content, "priority")
epic_status = extract_yaml_field(epic_content, "status")
epic_title = extract_yaml_field(epic_content, "title")
```

**Parse features from epic body:**
```python
# Epic features follow this pattern:
# ### Feature 1.1: Feature Name
# **Description:** Feature description text
# **Estimated Points:** 8

features = []
pattern = r'### Feature (\d+\.\d+): (.+?)\n.*?\*\*Description:\*\* (.+?)\n.*?\*\*Estimated Points:\*\* (\d+)'

for match in re.finditer(pattern, epic_content, re.DOTALL):
    feature_num = match.group(1)   # e.g., "1.1"
    feature_name = match.group(2)  # e.g., "Queue Infrastructure"
    feature_desc = match.group(3)  # e.g., "Queue-based task management..."
    points = int(match.group(4))   # e.g., 8

    features.append({
        "number": feature_num,
        "name": feature_name,
        "description": feature_desc,
        "points": points
    })

# Validate features extracted
if not features:
    ERROR: "No features found in epic {epic_id}"
    Display: "Epic may not have standard feature format. Use /create-story [description] for manual story creation."
    Exit
```

**Display discovered features:**
```
Detected Epic: {epic_id} - {epic_title}
Status: {epic_status}
Priority: {epic_priority}

Found {len(features)} features:
1.1: Queue Infrastructure (8 points)
1.2: Worker Process Engine (13 points)
1.3: Edition Detection (5 points)
1.4: Resource Monitoring (13 points)
1.5: Configuration Management (13 points)
1.6: Duplicate Prevention (3 points)
1.7: Retry Logic (8 points)

Total: {sum(f['points'] for f in features)} points
```

---

### Step 2: User Selects Features (Multi-Select)

**Check for existing stories:**
```python
# Glob existing stories
existing_stories = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")

# Check which features already have stories
for feature in features:
    # Search epic for story references to this feature
    feature_pattern = f"Feature {feature['number']}"

    # Check if epic already lists story for this feature
    # (Look for "STORY-XXX" after feature number)

    if story_exists_for_feature(feature['number']):
        feature['status'] = "EXISTS"
        feature['story_id'] = extract_story_id()
    else:
        feature['status'] = "NEEDS_CREATION"
```

**Present multi-select question:**
```python
AskUserQuestion(
    questions=[{
        question: f"Select features from {epic_id} to create stories for:",
        header: "Features",
        options: [
            {
                label: f"{f['number']}: {f['name']} ({f['points']} pts)",
                description: f"{f['description'][:80]}... | Status: {f['status']}"
            }
            for f in features
        ],
        multiSelect: true  # KEY: Allow multiple selections
    }]
)

# Extract user selections
selected_features = [f for f in features if user_selected(f)]

# Validate at least 1 feature selected
if not selected_features:
    Display: "No features selected. Exiting batch creation."
    Exit
```

**Display selection summary:**
```
Selected {len(selected_features)} features for story creation:

✓ Feature 1.1: Queue Infrastructure (8 points)
✓ Feature 1.2: Worker Process Engine (13 points)
✓ Feature 1.5: Configuration Management (13 points)

Total selected: {sum(f['points'] for f in selected_features)} points
Estimated time: {len(selected_features) * 2} minutes (sequential)
```

---

### Step 3: Collect Batch Metadata

**Ask once, apply to all:**
```python
AskUserQuestion(
    questions=[
        {
            question: "Assign all stories to which sprint?",
            header: "Sprint (batch)",
            options: [
                {
                    label: "Sprint-1",
                    description: "Assign all selected stories to Sprint-1"
                },
                {
                    label: "Backlog",
                    description: "Keep all stories in Backlog (assign to sprint later)"
                },
                {
                    label: "Ask per story",
                    description: "I'll choose sprint for each story individually"
                }
            ],
            multiSelect: false
        },
        {
            question: "Priority for all stories?",
            header: "Priority (batch)",
            options: [
                {
                    label: "Critical",
                    description: "All stories are Critical priority"
                },
                {
                    label: "High",
                    description: "All stories are High priority"
                },
                {
                    label: "Medium",
                    description: "All stories are Medium priority"
                },
                {
                    label: f"Inherit from epic ({epic_priority})",
                    description: f"Use epic's priority level"
                },
                {
                    label: "Ask per story",
                    description: "I'll choose priority for each story individually"
                }
            ],
            multiSelect: false
        }
    ]
)

# Process batch metadata
if batch_sprint == "Ask per story":
    per_story_sprint = True  # Will ask during loop
else:
    per_story_sprint = False
    sprint = batch_sprint  # Same for all

if batch_priority == f"Inherit from epic ({epic_priority})":
    priority = epic_priority
elif batch_priority == "Ask per story":
    per_story_priority = True
else:
    priority = batch_priority
```

**Display batch configuration:**
```
Batch Configuration:
- Stories to create: {len(selected_features)}
- Sprint: {sprint if not per_story_sprint else "Per-story selection"}
- Priority: {priority if not per_story_priority else "Per-story selection"}

Proceeding with batch story creation...
```

---

### Step 4: Sequential Story Creation Loop

**Calculate next story ID:**
```python
def get_next_story_id():
    """Calculate next available story ID with gap detection."""
    story_files = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")

    # Extract story numbers
    existing_numbers = []
    for file in story_files:
        match = re.search(r'STORY-(\d{3})', file)
        if match:
            existing_numbers.append(int(match.group(1)))

    if not existing_numbers:
        return "STORY-001"  # First story

    # Sort numbers
    existing_numbers.sort()

    # Check for gaps (e.g., [1,2,3,5,7] → gap at 4,6)
    all_numbers = set(range(1, max(existing_numbers) + 1))
    gaps = sorted(all_numbers - set(existing_numbers))

    if gaps:
        next_number = gaps[0]  # Fill first gap
        Display: f"Note: Filling gap at STORY-{next_number:03d}"
    else:
        next_number = max(existing_numbers) + 1  # No gaps, increment

    return f"STORY-{next_number:03d}"
```

**Create TodoWrite list:**
```python
# Initialize progress tracking
todo_items = []
for feature in selected_features:
    story_id = get_next_story_id()  # Pre-calculate all IDs
    todo_items.append({
        "content": f"Create {story_id}: {feature['name']}",
        "status": "pending",
        "activeForm": f"Creating {story_id}"
    })

TodoWrite(todos=todo_items)
```

**Story creation loop:**
```python
created_stories = []
failed_stories = []
story_id_index = 0

for i, feature in enumerate(selected_features):
    try:
        # Mark current as in_progress
        update_todo(i, status="in_progress")

        # Calculate story ID
        story_id = get_next_story_id()

        # Collect per-story metadata (if needed)
        if per_story_sprint:
            story_sprint = ask_sprint_for_story(feature['name'])
        else:
            story_sprint = sprint

        if per_story_priority:
            story_priority = ask_priority_for_story(feature['name'])
        else:
            story_priority = priority

        # Set context markers for skill
        Display: f"""
        **Story ID:** {story_id}
        **Epic ID:** {epic_id}
        **Feature Description:** {feature['description']}
        **Priority:** {story_priority}
        **Points:** {feature['points']}
        **Sprint:** {story_sprint}
        **Batch Mode:** true
        """

        # Invoke devforgeai-story-creation skill
        Skill(command="devforgeai-story-creation")

        # Verify story created
        story_file = Glob(pattern=f"devforgeai/specs/Stories/{story_id}*.story.md")

        if story_file:
            created_stories.append({
                "id": story_id,
                "feature": feature['name'],
                "points": feature['points']
            })

            # Mark current as completed
            update_todo(i, status="completed")

            Display: f"✓ Created {story_id}: {feature['name']}"
        else:
            # Story creation failed
            raise Exception(f"Story file not created for {story_id}")

    except Exception as e:
        # Story creation failed - continue with next
        failed_stories.append({
            "feature": feature['name'],
            "error": str(e)
        })

        # Mark current as failed
        update_todo(i, status="failed")

        Display: f"✗ Failed {feature['name']}: {e}"

        # Continue to next feature (don't halt batch)
        continue
```

---

### Step 5: Batch Completion Report

**Generate summary:**
```python
# Calculate metrics
total_created = len(created_stories)
total_failed = len(failed_stories)
total_points = sum(s['points'] for s in created_stories)

# Display summary
Display: f"""
{'='*60}
Batch Story Creation Complete
{'='*60}

Epic: {epic_id} - {epic_title}

Results:
✓ Created: {total_created} stories ({total_points} points)
✗ Failed: {total_failed} stories

{'─'*60}

Created Stories:
{'\n'.join(f"  ✓ {s['id']}: {s['feature']} ({s['points']} pts)" for s in created_stories)}

{f'''
Failed Stories:
{chr(10).join(f"  ✗ {s['feature']}: {s['error']}" for s in failed_stories)}
''' if failed_stories else ''}

{'─'*60}

Sprint Assignment: {sprint}
Priority: {priority}

Files Created:
{'\n'.join(f"  - devforgeai/specs/Stories/{s['id']}-*.story.md" for s in created_stories)}

{'='*60}
"""
```

**Handle failures (if any):**
```python
if failed_stories:
    AskUserQuestion(
        questions=[{
            question: f"{total_failed} stories failed creation. What would you like to do?",
            header: "Failures",
            options: [
                {
                    label: "Retry failed",
                    description: f"Re-run story creation for {total_failed} failed features only"
                },
                {
                    label: "Continue anyway",
                    description: f"Proceed with {total_created} successfully created stories"
                },
                {
                    label: "Review errors",
                    description: "Show me detailed error messages for each failure"
                },
                {
                    label: "Cancel batch",
                    description: "Delete all created stories and start over"
                }
            ],
            multiSelect: false
        }]
    )

    # Handle user choice
    if choice == "Retry failed":
        # Re-run loop for failed_stories only
        selected_features = [f for f in features if f['name'] in [fs['feature'] for fs in failed_stories]]
        goto Step 4  # Re-run loop

    elif choice == "Cancel batch":
        # Rollback: Delete all created stories
        for story in created_stories:
            story_file = Glob(pattern=f"devforgeai/specs/Stories/{story['id']}*.story.md")[0]
            Bash(command=f"rm {story_file}")

        Display: "Batch creation cancelled. All stories deleted."
        Exit
```

---

**2. `.claude/skills/devforgeai-story-creation/SKILL.md`**

**Add batch mode detection:**

```markdown
## Batch Mode Support (NEW - Enhancement)

**Batch mode triggered when:**
- Context marker `**Batch Mode:** true` present in conversation

**Batch mode behavior:**
- Skip interactive questions in Phase 1 (story discovery)
- Use provided story_id, epic_id, priority, points, sprint from context
- Execute Phases 2-8 normally (requirements, tech spec, UI spec, file creation, linking, validation, report)
- Return immediately after Phase 8 (no "next action" AskUserQuestion)

**Example context markers:**
```
**Story ID:** STORY-009
**Epic ID:** EPIC-001
**Feature Description:** Queue infrastructure with state management
**Priority:** High
**Points:** 8
**Sprint:** Sprint-1
**Batch Mode:** true
```

**Phase 1 modification for batch mode:**
```python
# In references/story-discovery.md

if "**Batch Mode:** true" in conversation:
    # Extract all metadata from context markers
    story_id = extract_from_conversation("Story ID:")
    epic_id = extract_from_conversation("Epic ID:")
    feature_description = extract_from_conversation("Feature Description:")
    priority = extract_from_conversation("Priority:")
    points = extract_from_conversation("Points:")
    sprint = extract_from_conversation("Sprint:")

    # Skip interactive questions
    Skip: AskUserQuestion for epic/sprint selection
    Skip: AskUserQuestion for priority/points

    # Proceed directly to Phase 2
else:
    # Normal interactive mode
    # AskUserQuestion for all metadata
```
```

**Files Modified:**
- `.claude/commands/create-story.md` (add epic batch workflow section ~150 lines)
- `.claude/skills/devforgeai-story-creation/SKILL.md` (add batch mode detection ~50 lines)
- `.claude/skills/devforgeai-story-creation/references/story-discovery.md` (add batch mode skip logic ~30 lines)

**Effort:** 4-6 hours

---

### Phase 2: Metadata Inheritance (2-3 hours)

**Goal:** Reduce question fatigue (14 questions → 4 questions).

**Already implemented in Phase 1 (Step 3):**
- Batch sprint selection
- Batch priority selection
- Per-story override option

**Additional optimization:**

**Epic metadata inheritance:**
```python
# In Step 3 (Collect Batch Metadata)

# Option: "Inherit all from epic"
AskUserQuestion(
    questions=[{
        question: "How should metadata be applied?",
        header: "Metadata",
        options: [
            {
                label: "Inherit all from epic",
                description: f"Priority: {epic_priority}, Points: Per feature, Sprint: Backlog"
            },
            {
                label: "Batch apply",
                description: "Ask once, apply same values to all stories"
            },
            {
                label: "Per-story apply",
                description: "Ask for each story individually (most control)"
            }
        ],
        multiSelect: false
    }]
)

if choice == "Inherit all from epic":
    priority = epic_priority
    sprint = "Backlog"  # Default
    # Points already from feature estimates

    # Only 1 question asked, 0 questions during loop
```

**Effort:** Included in Phase 1

---

### Phase 3: Progress Tracking with TodoWrite (1-2 hours)

**Goal:** Visual feedback during batch creation.

**Already designed in Phase 1 (Step 4):**
```python
TodoWrite(todos=todo_items)  # Before loop

for i, feature in enumerate(selected_features):
    update_todo(i, status="in_progress")
    # Create story
    update_todo(i, status="completed")
```

**User sees real-time updates:**
```
[✓] Create STORY-009: Queue Infrastructure
[✓] Create STORY-010: Worker Process Engine
[→] Create STORY-011: Edition Detection (in progress...)
[ ] Create STORY-012: Resource Monitoring
[ ] Create STORY-013: Configuration Management
[ ] Create STORY-014: Duplicate Prevention
[ ] Create STORY-015: Retry Logic
```

**Effort:** Included in Phase 1

---

### Phase 4: Error Handling & Partial Success (2-3 hours)

**Goal:** Graceful failure handling with recovery options.

**Already designed in Phase 1 (Step 4 & 5):**
- Try/catch in loop
- Continue on error (don't halt batch)
- Track created vs. failed stories
- AskUserQuestion for recovery (retry/continue/review/cancel)

**Additional error scenarios:**

**Scenario 1: Skill invocation fails**
```python
try:
    Skill(command="devforgeai-story-creation")
except SkillExecutionError as e:
    # Log error
    error_log.append({
        "feature": feature['name'],
        "error_type": "skill_invocation",
        "error_message": str(e),
        "recovery": "continue_to_next"
    })

    # Continue to next feature
    continue
```

**Scenario 2: Story validation fails (Phase 7 in skill)**
```python
# Skill returns validation_status = "FAILED"
if skill_result.validation_status == "FAILED":
    # Log validation failure
    failed_stories.append({
        "feature": feature['name'],
        "error": "Story validation failed in Phase 7",
        "details": skill_result.validation_errors
    })

    # Continue to next
    continue
```

**Scenario 3: Epic update fails**
```python
# After loop, update epic with all story references
try:
    update_epic_with_stories(epic_id, created_stories)
except Exception as e:
    WARNING: f"Epic update failed: {e}"
    Display: """
    ⚠️ Stories created successfully, but epic update failed.

    Created stories:
    {list_created_stories}

    Manual action required:
    - Open devforgeai/specs/Epics/{epic_id}.epic.md
    - Add story references manually

    Or retry: Re-run /create-story {epic_id} (will detect existing stories)
    """
```

**Effort:** 2-3 hours (comprehensive error handling)

---

### Phase 5: Dry-Run Mode (1 hour)

**Goal:** Preview before creating.

**Add dry-run detection:**
```python
# In Phase 0 (Argument Validation)

args = "$ARGUMENTS"  # Get all arguments

# Check for --dry-run flag
if "--dry-run" in args:
    dry_run_mode = true
    # Remove --dry-run from args
    args = args.replace("--dry-run", "").strip()
else:
    dry_run_mode = false

# Continue with mode detection (epic vs. feature description)
```

**Dry-run workflow (replaces Step 4):**
```python
if dry_run_mode:
    # Steps 1-3: Read epic, select features, collect metadata (same as normal)

    # Step 4 (DRY-RUN): Show preview instead of creating

    Display: f"""
    {'='*60}
    DRY RUN: Epic Batch Story Creation
    {'='*60}

    Epic: {epic_id} - {epic_title}

    Will create {len(selected_features)} stories:

    {'\n'.join(f"  {i+1}. STORY-{(max_existing_id + i + 1):03d}: {f['name']} ({f['points']} pts) → {sprint}, Priority: {priority}" for i, f in enumerate(selected_features))}

    Total: {sum(f['points'] for f in selected_features)} points
    Estimated time: {len(selected_features) * 2} minutes (sequential)

    {'─'*60}

    Files that will be created:
    {'\n'.join(f"  - devforgeai/specs/Stories/STORY-{(max_existing_id + i + 1):03d}-{slugify(f['name'])}.story.md" for i, f in enumerate(selected_features))}

    Epic will be updated:
    - Add {len(selected_features)} story references
    - Update "Next Steps" section

    {f'''
    Sprint will be updated:
    - Add {len(selected_features)} stories to {sprint}
    - Increase capacity by {sum(f['points'] for f in selected_features)} points
    ''' if sprint != "Backlog" else ''}

    {'='*60}

    To execute (create files):
    /create-story {epic_id}

    (Remove --dry-run flag)
    """

    # Exit without creating files
    Exit
```

**Example usage:**
```bash
# Preview
/create-story epic-001 --dry-run

# Execute
/create-story epic-001
```

**Effort:** 1 hour

---

### Phase 6: Parallel Optimization (3-4 hours)

**Goal:** 40-60% execution speedup via pseudo-parallel subagent invocation.

**Current implementation (Phase 1):** Sequential
```python
for feature in selected_features:
    Skill(command="devforgeai-story-creation")  # Waits for completion
    # Story 1: 2 min → Story 2: 2 min → Total: 14 min
```

**Optimized implementation:** Pseudo-parallel
```python
# Invoke all subagents at once (single message with multiple Task calls)

# Prepare all context markers
for i, feature in enumerate(selected_features):
    story_id = get_next_story_id()

    # Set context for this story
    context_markers[i] = f"""
    **Story ID:** {story_id}
    **Epic ID:** {epic_id}
    **Feature Description:** {feature['description']}
    **Priority:** {priority}
    **Points:** {feature['points']}
    **Sprint:** {sprint}
    **Batch Mode:** true
    **Batch Index:** {i}
    """

# Single message with multiple Skill invocations
for i in range(len(selected_features)):
    Display: context_markers[i]
    Skill(command="devforgeai-story-creation")

# Claude Code executes these pseudo-concurrently
# Expected: 40-60% faster than sequential
# 7 stories: 14 min sequential → 6-8 min pseudo-parallel
```

**Claude Code Limitation:**
Tasks in a single message run pseudo-parallel (Claude processes them with some concurrency, but still has serial dependencies). Actual speedup: ~40-60% faster, not 100%.

**Expected Performance:**
- **Sequential:** 7 stories × 2 min = 14 minutes
- **Pseudo-parallel:** 7 stories with concurrency = 6-8 minutes (realistic)

**Effort:** 3-4 hours (testing parallelism, measuring actual speedup)

---

## Smart Features (Included in Phases)

### Gap-Aware Story ID Generation

**Detect and fill gaps:**
```python
# Existing stories: STORY-001, STORY-002, STORY-003, STORY-005, STORY-007
# Gaps: 4, 6

next_id = fill_gap_if_exists()
# Returns: STORY-004 (fills first gap)

# After STORY-004 created:
next_id = fill_gap_if_exists()
# Returns: STORY-006 (fills next gap)

# After STORY-006 created:
next_id = fill_gap_if_exists()
# Returns: STORY-008 (no more gaps, increments from max)
```

**User notification:**
```
Creating stories for EPIC-001...

Note: Filling gap at STORY-004 ℹ️
✓ Created STORY-004: Queue Infrastructure

Note: Filling gap at STORY-006 ℹ️
✓ Created STORY-006: Configuration Management

✓ Created STORY-008: Retry Logic (sequential, no gaps)
```

**Benefit:** Maintains sequential story numbering, prevents ID fragmentation

---

### Batch Metadata Application Matrix

| Metadata | Option 1 | Option 2 | Option 3 | Option 4 |
|----------|----------|----------|----------|----------|
| **Sprint** | Sprint-1 (all) | Backlog (all) | Ask per story | — |
| **Priority** | Critical (all) | High (all) | Medium (all) | Inherit from epic | Ask per story |

**Question reduction:**
- **Inherit all from epic:** 0 questions during loop
- **Batch apply:** 0 questions during loop
- **Ask per story:** 2 questions × N stories

**Typical usage:**
- Small batch (3 stories): Batch apply (2 questions total)
- Large batch (7 stories): Inherit from epic (0 questions during loop)
- Mixed priorities: Ask per story (14 questions total)

---

## User Experience (After Implementation)

### Example 1: Full Epic Batch Creation

```bash
$ /create-story epic-001

Detected epic: EPIC-001 (Core Queue Architecture & Framework)
Found 7 features (63 total points)

Select features to create stories for:
☑ 1.1: Queue Infrastructure (8 points)
☑ 1.2: Worker Process Engine (13 points)
☑ 1.3: Edition Detection (5 points)
☑ 1.4: Resource Monitoring (13 points)
☑ 1.5: Configuration Management (13 points)
☑ 1.6: Duplicate Prevention (3 points)
☑ 1.7: Retry Logic (8 points)

(All selected)

Assign all stories to which sprint? → Sprint-1
Priority for all stories? → Inherit from epic (Critical)

Creating 7 stories...

[✓] STORY-009: Queue Infrastructure
[✓] STORY-010: Worker Process Engine
[✓] STORY-011: Edition Detection
[✓] STORY-012: Resource Monitoring
[✓] STORY-013: Configuration Management
[✓] STORY-014: Duplicate Prevention
[✓] STORY-015: Retry Logic

✅ Created 7 stories in 6 minutes (63 total points)

All stories assigned to Sprint-1
Epic EPIC-001 updated with story references

Next: Review stories or start development (/dev STORY-009)
```

---

### Example 2: Selective Feature Creation

```bash
$ /create-story epic-002

Detected epic: EPIC-002 (Index Maintenance Engine)
Found 6 features (89 total points)

Select features to create stories for:
☑ 2.1: Index Discovery (13 points) - Status: EXISTS (STORY-008)
☑ 2.2: Index Preservation (21 points) - Status: EXISTS (STORY-009)
☐ 2.3: Index Rebuild (21 points) - Status: NEEDS_CREATION ← Selected
☐ 2.4: Index Reorganize (13 points) - Status: NEEDS_CREATION ← Selected
☐ 2.5: Partition Maintenance (13 points) - Status: NEEDS_CREATION
☐ 2.6: Special Index Types (8 points) - Status: NEEDS_CREATION

(User selects 2.3 and 2.4 only)

Assign all stories to which sprint? → Backlog
Priority for all stories? → High

Creating 2 stories...

[✓] STORY-010: Index Rebuild Execution
[✓] STORY-011: Index Reorganize Execution

✅ Created 2 stories in 4 minutes (34 total points)

All stories in Backlog
Epic EPIC-002 updated

Next: Assign to sprint with /create-sprint
```

---

### Example 3: Dry-Run Preview

```bash
$ /create-story epic-003 --dry-run

Detected epic: EPIC-003 (Statistics Maintenance Engine)
Found 5 features (52 total points)

Select features: (All 5 selected)

Assign sprint? → Sprint-2
Priority? → High

════════════════════════════════════════════════════════
DRY RUN: Epic Batch Story Creation
════════════════════════════════════════════════════════

Epic: EPIC-003 - Statistics Maintenance Engine

Will create 5 stories:

  1. STORY-016: Statistics Discovery (8 pts) → Sprint-2, High
  2. STORY-017: Sampling Logic (13 pts) → Sprint-2, High
  3. STORY-018: Full Scan Detection (5 pts) → Sprint-2, High
  4. STORY-019: Async Stats Update (13 pts) → Sprint-2, High
  5. STORY-020: Stats Validation (13 pts) → Sprint-2, High

Total: 52 points
Estimated time: 10 minutes

────────────────────────────────────────────────────────

Files that will be created:
  - devforgeai/specs/Stories/STORY-016-statistics-discovery.story.md
  - devforgeai/specs/Stories/STORY-017-sampling-logic.story.md
  - devforgeai/specs/Stories/STORY-018-full-scan-detection.story.md
  - devforgeai/specs/Stories/STORY-019-async-stats-update.story.md
  - devforgeai/specs/Stories/STORY-020-stats-validation.story.md

Epic will be updated:
- Add 5 story references
- Update "Next Steps" section

Sprint-2 will be updated:
- Add 5 stories
- Increase capacity by 52 points

════════════════════════════════════════════════════════

To execute (create files):
/create-story epic-003

(Remove --dry-run flag)
```

**Effort:** 1 hour

---

## Feature Comparison Table

| Feature | Current (Single) | Enhanced (Batch) | Improvement |
|---------|------------------|------------------|-------------|
| **Command executions** | 7 (one per feature) | 1 (all features) | 86% reduction |
| **Questions asked** | 28-35 (4-5 per story) | 4 (batch metadata) | 88% reduction |
| **Time (sequential)** | 14 min (7×2) | 14 min (same) | No change |
| **Time (parallel)** | N/A | 6-8 min | 57% faster |
| **Files created** | 7 .story.md files | 7 .story.md files | Same |
| **User fatigue** | High (repetitive) | Low (streamlined) | Significant |
| **Error recovery** | None (manual retry) | Built-in (retry/continue) | Much better |
| **Preview option** | None | Dry-run mode | New capability |
| **Progress visibility** | None | TodoWrite real-time | New capability |

---

## Non-Aspirational Validation

**All features implementable within Claude Code Terminal:**

| Feature | Implementable? | Evidence |
|---------|----------------|----------|
| Epic detection (epic-001 pattern) | ✅ YES | Regex matching (built-in Python/JS) |
| Multi-select feature picker | ✅ YES | AskUserQuestion `multiSelect: true` |
| Sequential story creation loop | ✅ YES | For loop, Skill invocation |
| Batch metadata (ask once) | ✅ YES | AskUserQuestion with options |
| Progress tracking (TodoWrite) | ✅ YES | TodoWrite tool available |
| Error handling (continue-on-error) | ✅ YES | Try/catch, conditional logic |
| Dry-run preview | ✅ YES | Flag detection, conditional execution |
| Gap-aware numbering | ✅ YES | Set operations, sorting |
| Pseudo-parallel invocation | ✅ YES | Multiple Skill calls in single message |
| File system diff | ✅ YES | Glob before/after, set diff |
| Contract validation | ✅ YES | YAML parsing, regex matching |

**Aspirational features (NOT included):**
- ❌ Real-time progress bars (Claude Code limitation - no UI updates during execution)
- ❌ Transactional rollback (can't undo file writes automatically)
- ❌ True parallel execution (subagents run sequentially)
- ❌ Streaming output (user sees nothing until skill completes)

---

## Implementation Roadmap

### Sprint 1: RCA-007 Fix + Basic Batch (Week 1-2)
**Deliverables:**
- ✅ Fix 1, 2, 5: Subagent output constraints and validation (Phase 1 of RCA fix)
- ✅ Epic detection and feature extraction (Phase 1 of Enhancement)
- ✅ Multi-select feature picker
- ✅ Sequential story creation loop
- ✅ Basic batch metadata (sprint, priority)

**Testing:**
- Create single story: Only 1 .story.md file ✅
- Create batch (3 stories): 3 .story.md files, no extras ✅
- Gap detection works ✅

**Outcome:** `/create-story epic-001` works for batch creation

---

### Sprint 2: Contract Validation + Progress (Week 3)
**Deliverables:**
- ✅ Fix 4, 6: YAML contracts and file system diff (Phase 2 of RCA fix)
- ✅ TodoWrite progress tracking (Phase 3 of Enhancement)
- ✅ Error handling (Phase 4 of Enhancement)

**Testing:**
- Contract violations detected ✅
- Unauthorized files rolled back ✅
- Progress updates visible ✅
- Partial success handled gracefully ✅

**Outcome:** Robust batch creation with monitoring

---

### Sprint 3: Skill-Specific Subagent + Polish (Week 4)
**Deliverables:**
- ✅ Fix 3: story-requirements-analyst subagent (Phase 3 of RCA fix)
- ✅ Dry-run mode (Phase 5 of Enhancement)
- ✅ Parallel optimization (Phase 6 of Enhancement)

**Testing:**
- Skill-specific subagent quality matches general-purpose ✅
- Dry-run preview accurate ✅
- Parallel speedup measured (target: 40-60%) ✅
- Regression tests pass (100%) ✅

**Outcome:** Production-ready batch creation with optimization

---

## Success Criteria

### RCA-007 Fix Success
- [ ] Zero extra files created (no SUMMARY, QUICK-START, VALIDATION-CHECKLIST, FILE-INDEX)
- [ ] Only 1 .story.md file per story
- [ ] Subagent prompt includes output constraints
- [ ] Validation checkpoint catches violations
- [ ] Contract YAML created and enforced
- [ ] File system diff detects unauthorized files
- [ ] story-requirements-analyst subagent created and tested

### Batch Creation Enhancement Success
- [ ] `/create-story epic-001` detects epic and extracts features
- [ ] Multi-select question allows selecting 1-N features
- [ ] Stories created with correct sequential IDs (STORY-009, STORY-010, ...)
- [ ] Gaps detected and filled correctly
- [ ] Batch metadata reduces questions (14 → 4)
- [ ] TodoWrite shows real-time progress
- [ ] Error handling continues on failure (partial success)
- [ ] Dry-run preview works correctly
- [ ] Parallel optimization achieves 40-60% speedup
- [ ] All created stories pass Phase 7 self-validation

### Combined Success (RCA Fix + Enhancement)
- [ ] Create 7 stories from epic-001 → Only 7 .story.md files (no extras)
- [ ] Execution time: 6-8 minutes (with parallel optimization)
- [ ] User questions: 4 total (feature select, sprint, priority, next action)
- [ ] All stories linked to epic and sprint
- [ ] Zero framework violations
- [ ] 100% backward compatible (single story mode still works)

---

## Performance Targets

### Execution Time

| Scenario | Current | Enhanced (Sequential) | Enhanced (Parallel) | Improvement |
|----------|---------|----------------------|---------------------|-------------|
| 1 story | 2 min | 2 min | 2 min | None |
| 3 stories | 6 min (3 commands) | 6 min | 3-4 min | 33-50% faster |
| 7 stories | 14 min (7 commands) | 14 min | 6-8 min | 43-57% faster |
| 10 stories | 20 min (10 commands) | 20 min | 8-12 min | 40-60% faster |

### Question Count

| Scenario | Current | Enhanced (Batch) | Enhanced (Inherit) | Improvement |
|----------|---------|------------------|-------------------|-------------|
| 1 story | 4-5 | 4-5 | 4-5 | None |
| 3 stories | 12-15 (3×4) | 4 (batch) | 2 (inherit) | 67-88% reduction |
| 7 stories | 28-35 (7×4) | 4 (batch) | 2 (inherit) | 86-94% reduction |

### Token Usage (Main Conversation)

| Scenario | Current | Enhanced | Improvement |
|----------|---------|----------|-------------|
| 1 story | ~3.5K | ~3.5K | None |
| 7 stories | ~24.5K (7×3.5) | ~6K (batch overhead + skill invocations) | 75% reduction |

---

## Risk Assessment

### Risk 1: Parallel Optimization Doesn't Achieve Expected Speedup

**Likelihood:** Medium
**Impact:** Low (still faster than manual, just not 40-60%)

**Mitigation:**
- Measure actual speedup with benchmarks
- Document realistic performance in user guide
- Consider acceptable if 20-30% speedup achieved

---

### Risk 2: Story Creation Fails Mid-Batch

**Likelihood:** Medium (validation failures, subagent errors)
**Impact:** Medium (partial success, user confusion)

**Mitigation:**
- Continue-on-error logic (don't halt entire batch)
- Clear summary report (X succeeded, Y failed)
- Retry option for failed stories
- Rollback option if user wants clean slate

---

### Risk 3: Epic Has >10 Features (Over-Scoped)

**Likelihood:** Low
**Impact:** Low (user selects subset)

**Mitigation:**
- Epic validation (Phase 7 in epic creation) warns if >8 features
- User can select subset via multi-select
- Recommend splitting epic if >10 features

---

### Risk 4: Subagent Output Quality Degradation

**Likelihood:** Low
**Impact:** High (poor story quality)

**Mitigation:**
- Regression testing (compare content quality)
- Contract validation ensures all sections present
- Phase 7 self-validation catches issues
- Rollback to general-purpose subagent if quality degrades

---

## Dependencies

### Prerequisites
- ✅ RCA-007 Phase 1 complete (subagent output constraints)
- ✅ Context files exist (tech-stack, source-tree, etc.)
- ✅ Epic files exist with standard feature format

### Blockers
- ❌ None (all dependencies within DevForgeAI framework)

---

## Future Enhancements (Not in Scope)

**Potential future improvements (NOT implemented now):**

1. **Incremental batch creation** - Create 3 stories, run again, create 3 more (resume logic)
2. **Cross-epic batch creation** - `/create-story epic-001,epic-002` (multiple epics)
3. **Template variation per feature type** - CRUD vs. Auth vs. Workflow templates
4. **AI-suggested story point adjustments** - Analyze feature descriptions, suggest point changes
5. **Automatic sprint assignment** - AI analyzes capacity and recommends sprint

**Why not now:**
- Out of scope for this enhancement
- Add complexity without clear user demand
- Can be added later if users request

---

## Documentation Updates Required

### Files to Update After Implementation

1. **`.claude/memory/commands-reference.md`**
   - Add batch mode documentation to `/create-story` section
   - Update examples with epic-001 usage

2. **`.claude/memory/skills-reference.md`**
   - Document batch mode in devforgeai-story-creation section
   - Add story-requirements-analyst subagent

3. **`.claude/memory/subagents-reference.md`**
   - Add story-requirements-analyst entry
   - Document contract-based validation

4. **`CLAUDE.md`**
   - Update Component Summary (subagents: 20 → 21)
   - Add batch creation example

5. **`README.md`**
   - Add batch story creation to features list
   - Update quick start examples

---

## Testing Checklist

### Unit Tests (Per Phase)

**Phase 1: Basic Batch Mode**
- [ ] Epic detection works (epic-001, EPIC-002, Epic-003 all detected)
- [ ] Feature extraction works (7 features from EPIC-001)
- [ ] Multi-select question presents all features
- [ ] Story ID calculation correct (sequential with gap detection)
- [ ] Loop creates N stories (tested with 1, 3, 7 features)

**Phase 2: Metadata Inheritance**
- [ ] Batch sprint applies to all stories
- [ ] Batch priority applies to all stories
- [ ] Inherit from epic works correctly
- [ ] Per-story override works when selected

**Phase 3: Progress Tracking**
- [ ] TodoWrite list created before loop
- [ ] Progress updates in real-time (pending → in_progress → completed)
- [ ] Final summary shows all completed

**Phase 4: Error Handling**
- [ ] Story creation failure doesn't halt batch
- [ ] Failed stories tracked separately
- [ ] Retry option works for failed stories
- [ ] Cancel batch deletes all created stories

**Phase 5: Dry-Run Mode**
- [ ] --dry-run flag detected
- [ ] Preview shows correct story IDs
- [ ] Preview shows correct file paths
- [ ] No files created in dry-run
- [ ] Execution works after dry-run

**Phase 6: Parallel Optimization**
- [ ] Multiple Skill invocations in single message
- [ ] Speedup measured (target: 40-60%)
- [ ] All stories created correctly
- [ ] No race conditions or conflicts

---

### Integration Tests

**Test 1: Full Epic Batch (7 Stories)**
```bash
/create-story epic-001

# Select all 7 features
# Sprint: Sprint-1
# Priority: Inherit from epic

# Expected:
# - 7 .story.md files created
# - STORY-009 through STORY-015
# - All linked to EPIC-001 and Sprint-1
# - Epic updated with references
# - Sprint updated with stories
# - Execution time: 6-8 min (parallel)

# Assertions:
assert file_count("devforgeai/specs/Stories/STORY-*.story.md") == previous_count + 7
assert no_extra_files("devforgeai/specs/Stories/STORY-*-SUMMARY.md")
assert epic_references_count("EPIC-001") == 7
assert sprint_story_count("Sprint-1") includes STORY-009 through STORY-015
```

**Test 2: Partial Selection (3 of 6 Features)**
```bash
/create-story epic-002

# Select features 2.3, 2.4, 2.6 (skip 2.1, 2.2, 2.5)
# Sprint: Backlog
# Priority: High

# Expected:
# - 3 .story.md files created
# - Gap-aware numbering (STORY-010, STORY-011, STORY-012)
# - Only selected features have stories
# - Epic shows 3 new story references

# Assertions:
assert file_count increases by 3
assert STORY-010, STORY-011, STORY-012 exist
assert epic_feature_2.3_has_story("STORY-010")
assert epic_feature_2.5_has_no_story()  # Not selected
```

**Test 3: Error Recovery (1 Failure in 5 Stories)**
```bash
# Simulate failure (invalid feature description or validation error)
/create-story epic-003

# Select 5 features
# Simulate: Feature 3 validation fails

# Expected:
# - Stories 1, 2 created successfully
# - Story 3 fails (logged)
# - Stories 4, 5 created successfully
# - Summary: 4 succeeded, 1 failed
# - Option to retry story 3

# Assertions:
assert created_count == 4
assert failed_count == 1
assert retry_option_presented
```

**Test 4: Dry-Run Accuracy**
```bash
# Run dry-run
/create-story epic-004 --dry-run

# Note story IDs shown in preview (e.g., STORY-020 through STORY-025)

# Run actual creation
/create-story epic-004

# Expected:
# - Actual story IDs match dry-run preview
# - Actual file paths match dry-run preview
# - Actual capacity matches dry-run preview

# Assertions:
assert dry_run_story_ids == actual_story_ids
assert dry_run_file_paths == actual_file_paths
```

---

### Regression Tests

**Test 1: Single Story Mode Still Works**
```bash
/create-story User profile settings page with preferences

# Expected:
# - Single story created
# - Normal interactive mode (asks epic, sprint, priority, points)
# - No batch mode triggered

# Assertions:
assert mode == "SINGLE_STORY_MODE"
assert file_count increases by 1
assert no batch logic executed
```

**Test 2: Story Quality Unchanged**
```bash
# Create story in single mode
/create-story Feature A

# Create story in batch mode
/create-story epic-001  # Select Feature B

# Compare story files
# Expected:
# - Same section structure
# - Same acceptance criteria quality
# - Same technical specification depth
# - Same NFR measurability

# Assertions:
assert story_A_sections == story_B_sections
assert story_A_ac_count >= 3 and story_B_ac_count >= 3
assert both stories have measurable NFRs
```

**Test 3: Epic/Sprint Linking Still Works**
```bash
# Create batch stories
/create-story epic-002

# Check epic file
epic = Read("devforgeai/specs/Epics/EPIC-002.epic.md")

# Expected:
# - All created stories referenced in epic
# - Feature status updated ("NEEDS_CREATION" → "STORY-XXX created")

# Assertions:
assert "STORY-010" in epic
assert "STORY-011" in epic
assert feature_status_updated
```

---

## Documentation Requirements

### User-Facing Documentation

**Update `.claude/memory/commands-reference.md`:**

```markdown
### /create-story [story-description | epic-id]

**Purpose:** Generate user story with acceptance criteria, technical specifications, and UI specifications

**Modes:**
- **Single Story Mode:** Provide feature description (10+ words)
- **Batch Mode:** Provide epic ID (epic-001 format)

**Examples:**
```bash
# Single story
/create-story User login with email and password validation

# Batch creation from epic
/create-story epic-001

# Dry-run preview
/create-story epic-002 --dry-run
```

**Batch Mode Workflow:**
1. Detects epic reference (epic-001 pattern)
2. Reads epic, extracts all features
3. Multi-select: User selects features to create
4. Batch metadata: Ask sprint/priority once for all
5. Sequential creation: Generate stories with auto-incrementing IDs
6. Progress tracking: TodoWrite shows real-time updates
7. Completion summary: X succeeded, Y failed (if any)

**Batch Mode Benefits:**
- Create 7 stories in 6-8 minutes (vs. 14 min manual)
- 4 questions total (vs. 28 questions for 7 stories)
- Gap-aware numbering (fills STORY-004 if missing)
- Error recovery (continue on failure, retry option)
- Dry-run preview before creating

**Output (Batch Mode):**
- Multiple `.story.md` files (one per selected feature)
- All stories linked to epic and sprint
- Epic updated with story references
- Sprint updated with new stories (if assigned)
```

---

### Developer-Facing Documentation

**Create NEW File:** `.claude/skills/devforgeai-story-creation/references/batch-mode-guide.md`

```markdown
# Batch Mode Story Creation Guide

**Purpose:** Enable efficient multi-story creation from epic features.

## Batch Mode Detection

**Triggered when:**
- Context marker `**Batch Mode:** true` present
- All required metadata provided (story_id, epic_id, feature_description, priority, points, sprint)

**Behavior changes:**
- Skip interactive questions in Phase 1 (story discovery)
- Use provided metadata from context markers
- Execute Phases 2-8 normally
- Return immediately after Phase 8 (no next action question)

## Context Markers for Batch Mode

**Required markers:**
```
**Story ID:** STORY-009
**Epic ID:** EPIC-001
**Feature Description:** Queue infrastructure with state management and retry logic
**Priority:** High
**Points:** 8
**Sprint:** Sprint-1
**Batch Mode:** true
```

**Optional markers:**
```
**Batch Index:** 0  # Index in batch (for progress tracking)
```

## Implementation Notes

**Phase 1 (Story Discovery) - Batch Mode Branch:**

```python
# In story-discovery.md

if batch_mode_detected:
    # Extract all metadata from context markers
    story_id = extract_from_conversation("Story ID:")
    epic_id = extract_from_conversation("Epic ID:")
    feature_description = extract_from_conversation("Feature Description:")
    priority = extract_from_conversation("Priority:")
    points = int(extract_from_conversation("Points:"))
    sprint = extract_from_conversation("Sprint:")

    # Validate all required fields present
    assert story_id and epic_id and feature_description and priority and points and sprint

    # Skip all interactive questions
    Skip: AskUserQuestion for epic/sprint selection
    Skip: AskUserQuestion for priority/points

    # Log batch mode activation
    Display: f"ℹ️ Batch mode: Using provided metadata (Story {story_id}, {points} pts, {priority} priority)"

    # Proceed directly to Phase 2
    return {
        "story_id": story_id,
        "epic_id": epic_id,
        "feature_description": feature_description,
        "priority": priority,
        "points": points,
        "sprint": sprint
    }
else:
    # Normal interactive mode
    # AskUserQuestion for all metadata (existing logic)
```

## Error Handling in Batch Mode

**If required marker missing:**
```python
if batch_mode and not all_markers_present:
    ERROR: "Batch mode requires all metadata markers"
    Missing: {list_missing_markers}

    # Fallback to interactive mode
    Display: "⚠️ Batch mode failed: Missing metadata. Switching to interactive mode..."
    batch_mode = false
    # Continue with normal Phase 1 questions
```

**If batch creation fails:**
```python
# Parent workflow (command) handles failure
# Skill returns error status
return {
    "status": "FAILED",
    "error": "Phase X failed: {reason}",
    "story_id": story_id
}

# Command logs failure and continues to next story
```

## Performance Optimization

**Subagent invocation in batch:**
- Parent command invokes skill multiple times (one per story)
- Each skill invocation happens in isolated context
- Pseudo-parallel execution when multiple Skill calls in single message
- Expected speedup: 40-60% vs. pure sequential

**Token efficiency:**
- Batch overhead: ~2K tokens (command-level)
- Per-story skill execution: ~90K tokens (isolated context each)
- Total main conversation: ~6K tokens (batch overhead + summaries)
- vs. Manual: ~24.5K tokens (7 separate command executions)
- **Savings: 75% reduction in main conversation tokens**

## Testing

**Batch mode test cases:**
1. Batch mode with all markers present → Skip Phase 1 questions ✅
2. Batch mode with missing marker → Fallback to interactive ✅
3. Batch mode story quality → Same as interactive mode ✅
4. Batch mode + RCA-007 fix → Only 1 .story.md per story ✅
```

**Effort:** 1 hour

---

## Technical Design Details

### Epic Feature Pattern Recognition

**Standard epic feature format:**
```markdown
### Feature 1.1: Queue Infrastructure & State Management

**Description:** Implement queue-based task management system with persistent state tracking, priority-based execution, and dead-letter queue support.

**Estimated Points:** 8

**Complexity:** Medium (3-tier architecture, requires database design)

**Dependencies:**
- Database schema design
- Queue message format specification

**Risks:**
- Concurrency control complexity
- State synchronization issues
```

**Regex pattern:**
```python
# Greedy match to capture full description (multi-line)
pattern = r'''
    ###\s+Feature\s+(\d+\.\d+):\s*(.+?)\n     # Feature number and name
    \s*\*\*Description:\*\*\s*(.+?)\n         # Description (one line)
    \s*\*\*Estimated\s+Points:\*\*\s*(\d+)    # Points
'''

# Enhanced pattern (captures all fields)
enhanced_pattern = r'''
    ###\s+Feature\s+(\d+\.\d+):\s*(.+?)\n     # Number and name
    \s*\*\*Description:\*\*\s*(.+?)\n         # Description
    \s*\*\*Estimated\s+Points:\*\*\s*(\d+)    # Points
    (?:\s*\*\*Complexity:\*\*\s*(.+?)\n)?     # Optional complexity
    (?:\s*\*\*Dependencies:\*\*(.*?)(?=\*\*|###|$))?  # Optional dependencies
    (?:\s*\*\*Risks:\*\*(.*?)(?=\*\*|###|$))?        # Optional risks
'''
```

**Parsing algorithm:**
```python
def parse_epic_features(epic_content):
    """Extract all features from epic document."""
    features = []

    # Find all feature sections
    pattern = r'###\s+Feature\s+(\d+\.\d+):\s*(.+?)\n\s*\*\*Description:\*\*\s*(.+?)\n\s*\*\*Estimated\s+Points:\*\*\s*(\d+)'

    for match in re.finditer(pattern, epic_content, re.DOTALL):
        feature = {
            "number": match.group(1),           # "1.1"
            "name": match.group(2).strip(),     # "Queue Infrastructure"
            "description": match.group(3).strip(),  # "Implement queue-based..."
            "points": int(match.group(4))       # 8
        }

        # Validate feature
        if len(feature['description']) < 10:
            WARNING: f"Feature {feature['number']} has short description"

        if feature['points'] not in [1,2,3,5,8,13,21]:
            WARNING: f"Feature {feature['number']} has non-Fibonacci points: {feature['points']}"

        features.append(feature)

    return features
```

---

### Story ID Calculation with Gap Detection

**Algorithm:**
```python
def get_next_story_id():
    """
    Calculate next available story ID with gap detection.

    Examples:
    - Existing: [1,2,3,5,7] → Returns: 4 (fills first gap)
    - Existing: [1,2,3,4,5] → Returns: 6 (no gaps, increment)
    - Existing: [] → Returns: 1 (first story)
    """
    # Get all existing stories
    story_files = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")

    # Extract story numbers
    existing_numbers = []
    for file in story_files:
        match = re.search(r'STORY-(\d{3})', file)
        if match:
            existing_numbers.append(int(match.group(1)))

    # Handle empty case
    if not existing_numbers:
        return "STORY-001"

    # Sort numbers
    existing_numbers.sort()
    max_number = max(existing_numbers)

    # Detect gaps
    all_numbers = set(range(1, max_number + 1))
    gaps = sorted(all_numbers - set(existing_numbers))

    # Return first gap or increment
    if gaps:
        next_number = gaps[0]
        gap_notification = True
    else:
        next_number = max_number + 1
        gap_notification = False

    # Format as STORY-XXX
    story_id = f"STORY-{next_number:03d}"

    return story_id, gap_notification
```

**Usage in loop:**
```python
for feature in selected_features:
    story_id, is_gap = get_next_story_id()

    if is_gap:
        Display: f"ℹ️ Filling gap at {story_id}"

    # Create story with this ID
    create_story(story_id, feature)
```

---

### Batch Mode Context Markers

**Template for skill invocation:**
```python
def invoke_story_creation_skill(story_id, epic_id, feature, sprint, priority, batch_index):
    """Invoke devforgeai-story-creation skill in batch mode."""

    # Set context markers
    context = f"""
    **Story ID:** {story_id}
    **Epic ID:** {epic_id}
    **Feature Number:** {feature['number']}
    **Feature Name:** {feature['name']}
    **Feature Description:** {feature['description']}
    **Priority:** {priority}
    **Points:** {feature['points']}
    **Sprint:** {sprint}
    **Batch Mode:** true
    **Batch Index:** {batch_index}
    **Total in Batch:** {len(selected_features)}
    """

    # Display context (makes it part of conversation)
    Display: context

    # Invoke skill
    Skill(command="devforgeai-story-creation")

    # Skill extracts markers and uses them in Phase 1
    # No interactive questions asked (batch mode)
```

---

## Implementation Acceptance Criteria

### AC1: Epic Detection
**Given** user provides argument matching pattern `epic-\d{3}` (case-insensitive)
**When** command Phase 0 executes argument validation
**Then** mode is set to "EPIC_BATCH_MODE" and epic file is loaded

### AC2: Feature Extraction
**Given** epic file contains standard feature format (### Feature X.Y: Name)
**When** batch workflow Step 1 executes
**Then** all features extracted with number, name, description, points

### AC3: Multi-Select Feature Picker
**Given** 7 features extracted from epic
**When** batch workflow Step 2 executes
**Then** AskUserQuestion presents all 7 features with multiSelect: true

### AC4: Sequential Story Creation
**Given** user selects 3 features
**When** batch workflow Step 4 executes
**Then** 3 stories created with IDs STORY-009, STORY-010, STORY-011

### AC5: Gap Detection
**Given** existing stories are STORY-001, STORY-002, STORY-005
**When** calculating next story ID
**Then** returns STORY-003 (fills gap)

### AC6: Batch Metadata Application
**Given** user selects "Inherit from epic" for priority
**When** creating 5 stories in batch
**Then** all 5 stories have same priority as epic

### AC7: Progress Tracking
**Given** creating 7 stories in batch
**When** loop executes
**Then** TodoWrite shows real-time progress (pending → in_progress → completed)

### AC8: Error Recovery
**Given** story 3 of 5 fails validation
**When** batch creation continues
**Then** stories 1, 2, 4, 5 created successfully and user prompted to retry story 3

### AC9: Dry-Run Preview
**Given** user provides --dry-run flag
**When** command executes
**Then** preview shown, no files created, execution command displayed

### AC10: Single Story Mode Unchanged
**Given** user provides feature description (not epic ID)
**When** command executes
**Then** normal single story workflow executes (no batch mode)

---

## Rollback Plan

**If batch mode causes issues:**

1. **Disable batch mode detection:**
   - Comment out epic pattern matching in Phase 0
   - All inputs treated as feature descriptions
   - Revert to 100% single story mode

2. **Feature flag approach:**
   ```python
   # In .claude/commands/create-story.md
   BATCH_MODE_ENABLED = true  # Set to false to disable

   if BATCH_MODE_ENABLED and epic_pattern_match:
       # Batch workflow
   else:
       # Single story workflow
   ```

3. **Gradual rollout:**
   - Phase 1 only (basic batch, no optimization)
   - Test for 1 week
   - Add Phases 2-6 incrementally

---

## Related Documents

- **RCA:** `devforgeai/RCA/RCA-007-multi-file-story-creation.md`
- **RCA Fix:** `devforgeai/specs/enhancements/RCA-007-FIX-IMPLEMENTATION-PLAN.md`
- **Command:** `.claude/commands/create-story.md`
- **Skill:** `.claude/skills/devforgeai-story-creation/SKILL.md`
- **Lean Orchestration:** `devforgeai/protocols/lean-orchestration-pattern.md`

---

## Implementation Status

**Status:** Specification Complete - Ready for Implementation
**Priority:** MEDIUM (RCA-007 fix is HIGH, this is enhancement)
**Recommended Sequence:**
1. Complete RCA-007 fix first (Weeks 1-3)
2. Implement batch creation after RCA fix validated (Weeks 4-6)

**Rationale:** Ensure single-file creation works correctly before enabling batch mode.

---

**Total Enhancement Value:**
- **Time savings:** 57% faster execution (with parallel optimization)
- **Interaction reduction:** 86-94% fewer questions
- **User experience:** Streamlined batch operations
- **Framework integrity:** Maintains single-file design principle (after RCA-007 fix)
