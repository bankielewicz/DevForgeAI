# Phase 01: Pre-Flight Validation

**Purpose:** Comprehensive validation before TDD workflow begins. This phase ensures all prerequisites are met.

**Execution:** Before Phase 02 (Red phase) starts

**Token Cost:** ~6,000 tokens when loaded

---

## Phase Progress Indicator

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Phase 01/10: Pre-Flight Validation (0% → 10% complete)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Display this indicator at the start of Phase 01 execution.**

---

## Overview

Phase 01 executes 9 validation steps before proceeding to TDD implementation. This prevents starting work in an invalid environment.

**Steps:**
1. Validate Git repository status
2. **Git Worktree Auto-Management** (STORY-091)
2.5. **Dependency Graph Validation** (STORY-093) - NEW
3. Adapt TDD workflow based on Git availability
4. File-based change tracking template (if no Git)
5. Validate context files exist
6. Load story specification
7. Validate spec vs context files
8. Detect and validate technology stack
9. Detect previous QA failures

---

## Step 0.1: Validate Git Repository Status [MANDATORY]

**Invoke git-validator subagent to check Git availability:**

```
Task(
  subagent_type="git-validator",
  description="Validate Git repository status",
  prompt="Check the Git repository status for the current directory.

  Validate:
  1. Is Git installed and accessible?
  2. Is this directory a Git repository?
  3. Are there existing commits?
  4. What is the current branch?
  5. Are there uncommitted changes?

  Return JSON with Git status, assessment, and recommendations.

  CRITICAL: Always provide fallback strategy if Git unavailable - DevForgeAI must adapt gracefully."
)
```

**Parse subagent JSON response:**

```javascript
result = parse_json(subagent_output)

# Extract workflow configuration
GIT_AVAILABLE = result["git_status"]["installed"] AND result["git_status"]["repository_exists"]
WORKFLOW_MODE = result["assessment"]["workflow_mode"]  # "full", "partial", or "fallback"
CAN_COMMIT = result["assessment"]["can_commit"]
CURRENT_BRANCH = result["git_status"]["current_branch"]
UNCOMMITTED_CHANGES = result["git_status"]["uncommitted_changes"]

# Display status to user
IF WORKFLOW_MODE == "full":
    Display: "✓ Git repository validated - full workflow enabled"
    Display: "  - Repository: Initialized with {result['git_status']['commit_count']} commits"
    Display: "  - Branch: {CURRENT_BRANCH}"
    Display: "  - Uncommitted changes: {UNCOMMITTED_CHANGES}"

    IF UNCOMMITTED_CHANGES > 0:
        Display: "  ⚠️  Warning: {UNCOMMITTED_CHANGES} uncommitted changes detected"
        Display: "  Recommendation: Commit or stash before proceeding"

ELIF WORKFLOW_MODE == "partial":
    Display: "⚠ Git repository needs initial commit"
    Display: "  Repository initialized but no commits yet"
    Display: "  Recommendation:"
    FOR cmd in result["recommendations"]["commands"]:
        Display: "    {cmd}"

ELIF WORKFLOW_MODE == "fallback":
    IF result["git_status"]["installed"]:
        Display: "⚠ Git available but repository not initialized"
        Display: "  To enable full workflow:"
        FOR cmd in result["recommendations"]["commands"]:
            Display: "    {cmd}"
    ELSE:
        Display: "⚠ Git not installed - file-based workflow enabled"
        Display: "  Changes will be tracked in:"
        Display: "    devforgeai/stories/{STORY-ID}/changes/"

    Display: ""
    Display: "  Fallback mode active (limited version control features)"

# Store flags for workflow adaptation
$GIT_AVAILABLE = GIT_AVAILABLE
$WORKFLOW_MODE = WORKFLOW_MODE
$CAN_COMMIT = CAN_COMMIT
```

**Token cost:** ~500 tokens in main conversation (~3,000 in isolated subagent context)

**Benefits:**
- Context isolation (Git checks in separate context window)
- Reusable validation (other skills can use git-validator)
- Framework-aware (subagent understands fallback strategies)
- Structured output (JSON parsing vs text interpretation)

---

## Step 0.1.5: User Consent for Git State Changes [MANDATORY IF uncommitted > 10] (RCA-008)

**CRITICAL: This step prevents autonomous file hiding (RCA-008 incident - 2025-11-13).**

**When to execute:** After git-validator returns results from Step 0.1

**Trigger condition:**
- `uncommitted_changes > 10` OR
- `untracked_files > 0` (if git-validator provides this data)

**Purpose:** Obtain explicit user consent before any git operation that would hide/modify files, preventing the autonomous stashing incident where 21 story files were hidden without user knowledge.

**Implementation:**

```
IF git_validator_result["git_status"]["uncommitted_changes"] > 10 OR
   (git_validator_result["file_analysis"] AND git_validator_result["file_analysis"]["untracked_files"] > 0):

    # Extract counts from git-validator result
    total_changes = git_validator_result["git_status"]["uncommitted_changes"]

    # If git-validator provides file_analysis (Phase 2 enhancement), use it
    IF git_validator_result["file_analysis"] exists:
        untracked_count = git_validator_result["file_analysis"]["untracked_files"]
        modified_count = git_validator_result["file_analysis"]["modified_files"]
        file_breakdown = git_validator_result["file_analysis"]["file_breakdown"]
    ELSE:
        # Fallback: Calculate ourselves
        untracked_count = count uncommitted files marked "??" in git status
        modified_count = total_changes - untracked_count
        file_breakdown = null

    # Display status summary box
    Display: ""
    Display: "╔═══════════════════════════════════════════════════════════════╗"
    Display: "║  ⚠️  UNCOMMITTED CHANGES DETECTED                             ║"
    Display: "╠═══════════════════════════════════════════════════════════════╣"
    Display: "║                                                               ║"
    Display: "║  Total files: {total_changes}                                ║"

    IF untracked_count > 0 AND modified_count > 0:
        Display: "║    • {modified_count} modified files (tracked by git)        ║"
        Display: "║    • {untracked_count} untracked files (new, not in git)     ║"
    ELIF untracked_count > 0:
        Display: "║    • {untracked_count} untracked files (new, not in git)     ║"
    ELSE:
        Display: "║    • {modified_count} modified files                         ║"

    # Display file breakdown if available (Phase 2 enhancement)
    IF file_breakdown exists AND file_breakdown is not empty:
        Display: "║                                                               ║"
        Display: "║  Breakdown:                                                   ║"

        IF file_breakdown["story_files"] > 0:
            Display: "║    • {file_breakdown.story_files} story files (.story.md)    ║"
            Display: "║      ⚠️  User-created content - should not be hidden         ║"

        IF file_breakdown["python_cache"] > 0:
            Display: "║    • {file_breakdown.python_cache} Python cache files        ║"

        IF file_breakdown["config_files"] > 0:
            Display: "║    • {file_breakdown.config_files} config files              ║"

        IF file_breakdown["documentation"] > 0:
            Display: "║    • {file_breakdown.documentation} documentation files      ║"

        IF file_breakdown["code"] > 0:
            Display: "║    • {file_breakdown.code} code files                        ║"

        IF file_breakdown["other"] > 0:
            Display: "║    • {file_breakdown.other} other files                      ║"

    Display: "║                                                               ║"
    Display: "║  The development workflow can proceed in multiple ways:       ║"
    Display: "║                                                               ║"
    Display: "╚═══════════════════════════════════════════════════════════════╝"
    Display: ""

    # Ask user for strategy
    AskUserQuestion(
        questions=[{
            question: "How should we handle these uncommitted changes?",
            header: "Git Strategy",
            multiSelect: false,
            options: [
                {
                    label: "Continue anyway (safe - file-based tracking)",
                    description: "Proceed without touching git. Framework uses file-based change tracking in devforgeai/stories/{STORY-ID}/changes/. All your files stay visible."
                },
                {
                    label: "Stash ONLY modified files, keep untracked visible ⭐ Recommended",
                    description: "Hide {modified_count} modified (tracked) files in stash, but keep {untracked_count} untracked files visible. Best of both worlds - clean tracked files, preserve new content."
                },
                {
                    label: "Show me the files first",
                    description: "Display list of all {total_changes} files so I can review what would be affected. I'll be asked again after seeing the list."
                },
                {
                    label: "Commit my changes first",
                    description: "Pause development. I'll commit these changes manually, then re-run /dev {STORY-ID}."
                },
                {
                    label: "Stash ALL files (modified + untracked) - Advanced",
                    description: "⚠️ Hide ALL {total_changes} files including {untracked_count} untracked. Requires 'git stash pop' to restore. Use with caution."
                }
            ]
        }]
    )

    # Handle user response
    SWITCH user_response_answers["Git Strategy"]:

        CASE "Continue anyway (safe - file-based tracking)":
            SET workflow_mode = "file-based"
            Display: "✅ Proceeding with file-based tracking. Your files remain visible."
            Display: "   Changes will be tracked in devforgeai/stories/{STORY-ID}/changes/"
            Display: ""
            # Continue to Step 0.2 (adapt workflow)

        CASE "Stash ONLY modified files, keep untracked visible ⭐ Recommended":
            Display: ""
            Display: "Stashing {modified_count} modified files (keeping {untracked_count} untracked files visible)..."
            Display: ""

            # Use git stash WITHOUT --include-untracked flag
            # This is the KEY: default git stash behavior preserves untracked files
            Bash(
                command="git stash push -m 'WIP: Modified files only (by /dev {STORY-ID} at $(date +%Y-%m-%d_%H:%M:%S))'",
                description="Stash modified files only, preserve untracked"
            )

            # Verify untracked files still visible
            Bash(command="git status --short | grep '^??' | wc -l || echo '0'", description="Count remaining untracked files")
            remaining_untracked = result

            Display: ""
            Display: "✅ Stashed {modified_count} modified files to stash@{0}"
            Display: "✅ {remaining_untracked} untracked files remain visible"

            IF file_breakdown AND file_breakdown["story_files"] > 0:
                Display: "   (includes {file_breakdown.story_files} story files)"

            Display: ""
            Display: "To restore modified files later:"
            Display: "  git stash pop"
            Display: ""

            SET workflow_mode = "git"
            # Continue to Step 0.2

        CASE "Show me the files first":
            Display: ""
            Display: "Files that would be affected by git operations:"
            Display: ""
            Bash(command="git status --short", description="Show uncommitted files")
            Display: ""
            Display: "File status codes:"
            Display: "  M  = Modified (tracked files with changes)"
            Display: "  ?? = Untracked (new files not yet in git)"
            Display: "  D  = Deleted"
            Display: "  A  = Added (staged for commit)"
            Display: ""

            # Re-ask the question with file context now visible
            AskUserQuestion(
                questions=[{
                    question: "Now that you've seen the files, how should we proceed?",
                    header: "Git Strategy",
                    multiSelect: false,
                    options: [
                        {
                            label: "Continue anyway (safe - file-based tracking)",
                            description: "Proceed without touching git. All {total_changes} files stay visible."
                        },
                        {
                            label: "Stash ONLY modified files, keep untracked visible ⭐ Recommended",
                            description: "Hide modified files, keep untracked files visible. Preserves story files and new content."
                        },
                        {
                            label: "Commit my changes first",
                            description: "Pause development. I'll commit these changes manually."
                        },
                        {
                            label: "Stash ALL files (modified + untracked) - Advanced",
                            description: "⚠️ Hide ALL files temporarily. Requires 'git stash pop' to restore."
                        }
                    ]
                }]
            )
            # Handle response recursively (will hit one of the other cases)

        CASE "Commit my changes first":
            Display: ""
            Display: "╔═══════════════════════════════════════════════════════════════╗"
            Display: "║  📝 RECOMMENDED WORKFLOW                                      ║"
            Display: "╠═══════════════════════════════════════════════════════════════╣"
            Display: "║                                                               ║"
            Display: "║  1. Review your changes:                                      ║"
            Display: "║     git status                                                ║"
            Display: "║     git diff                                                  ║"
            Display: "║                                                               ║"
            Display: "║  2. Stage all changes:                                        ║"
            Display: "║     git add .                                                 ║"
            Display: "║                                                               ║"
            Display: "║  3. Commit with descriptive message:                          ║"
            Display: "║     git commit -m \"WIP: Checkpoint before {STORY-ID}\"       ║"
            Display: "║                                                               ║"
            Display: "║  4. Re-run development:                                       ║"
            Display: "║     /dev {STORY-ID}                                           ║"
            Display: "║                                                               ║"
            Display: "╚═══════════════════════════════════════════════════════════════╝"
            Display: ""
            HALT execution with message: "Development paused. Commit changes and re-run /dev {STORY-ID}."
            Exit workflow

        CASE "Stash ALL files (modified + untracked) - Advanced":
            # Delegate to Step 0.1.6 (Stash Warning Workflow)
            # This is implemented in Story 1.2
            Display: ""
            Display: "Proceeding to stash warning workflow..."
            Display: ""
            # GOTO Step 0.1.6 (will be added in Story 1.2)
            INVOKE: Step 0.1.6 (Stash Warning and Confirmation)

ELSE:
    # No uncommitted changes, or below threshold
    Display: "✓ Working tree: Clean (or below threshold)"
    # Continue to Step 0.2
```

**Success Criteria:**
- User ALWAYS prompted when uncommitted_changes > 10 or untracked_files > 0
- User can see file list before deciding (via "Show me files first" option)
- "Continue anyway" option preserves all files via file-based tracking
- "Commit first" provides clear instructions and HALTS workflow
- "Stash" delegates to Step 0.1.6 warning workflow (implemented in Story 1.2)
- No files ever hidden without explicit user confirmation

**Token cost:** ~1,500 tokens (includes AskUserQuestion and display logic)

**Rationale:** RCA-008 incident (2025-11-13) occurred when AI agent autonomously ran `git stash --include-untracked` without user consent, hiding 21 user-created story files. This checkpoint ensures user always knows what will happen before any git operation executes.

---

## Step 0.1.6: Stash Warning and Confirmation [MANDATORY IF user selects stash] (RCA-008)

**When to execute:** User selected "Stash changes (advanced)" in Step 0.1.5

**Purpose:** Provide clear warning about file visibility consequences before stashing untracked files

**Implementation:**

```
# Called from Step 0.1.5 when user selects "Stash changes (advanced)"

# Get file counts from git-validator result (or calculate)
total_files = git_validator_result["git_status"]["uncommitted_changes"]

IF git_validator_result["file_analysis"] exists:
    untracked_count = git_validator_result["file_analysis"]["untracked_files"]
    modified_count = git_validator_result["file_analysis"]["modified_files"]
ELSE:
    # Fallback: Count ourselves
    Bash(command="git status --short | grep '^??' | wc -l", description="Count untracked files")
    untracked_count = result
    modified_count = total_files - untracked_count

# Show detailed file breakdown
IF untracked_count > 0:
    Display: ""
    Display: "Preparing to show untracked files that would be stashed..."
    Display: ""

    # Show first 10 untracked files
    Bash(command="git status --short | grep '^??' | head -10", description="Show untracked files")

    IF untracked_count > 10:
        Display: ""
        Display: "... and {untracked_count - 10} more untracked files"
        Display: ""

    # Check for story files specifically
    Bash(command="git status --short | grep '^??' | grep -c 'STORY-' || echo '0'", description="Count story files")
    story_file_count = result

    IF story_file_count > 0:
        Display: ""
        Display: "⚠️  {story_file_count} STORY files detected in untracked files:"
        Display: ""
        Bash(command="git status --short | grep '^??' | grep 'STORY-'", description="Show story files")
        Display: ""

# Display warning box
Display: ""
Display: "╔═══════════════════════════════════════════════════════════════╗"
Display: "║  ⚠️  WARNING: STASHING {total_files} FILES                    ║"
Display: "╠═══════════════════════════════════════════════════════════════╣"
Display: "║                                                               ║"
Display: "║  What 'git stash' does:                                       ║"
Display: "║    • Temporarily HIDES files from your filesystem             ║"
Display: "║    • Files are stored in git's stash storage                  ║"
Display: "║    • They are NOT deleted (recoverable)                       ║"
Display: "║    • They will NOT be visible until you restore them          ║"
Display: "║                                                               ║"

IF untracked_count > 0:
    Display: "║  ⚠️  {untracked_count} UNTRACKED FILES WILL BE HIDDEN:        ║"
    Display: "║    These are NEW files you created that aren't in git yet.    ║"
    IF story_file_count > 0:
        Display: "║    This includes {story_file_count} STORY files!              ║"
    Display: "║                                                               ║"

Display: "║  To recover stashed files later:                              ║"
Display: "║    git stash pop        # Restores and removes from stash     ║"
Display: "║    git stash apply      # Restores but keeps in stash         ║"
Display: "║                                                               ║"
Display: "║  To preview what's stashed:                                   ║"
Display: "║    git stash show stash@{0} --name-only                      ║"
Display: "║                                                               ║"
Display: "╚═══════════════════════════════════════════════════════════════╝"
Display: ""

# Second confirmation required for safety
AskUserQuestion(
    questions=[{
        question: "Are you SURE you want to stash {total_files} files (including {untracked_count} untracked)?",
        header: "Confirm Stash",
        multiSelect: false,
        options: [
            {
                label: "Yes, stash them (I understand they'll be hidden)",
                description: "Proceed with stashing. Files will be recoverable with 'git stash pop'."
            },
            {
                label: "No, continue without stashing instead",
                description: "Cancel stashing. Use file-based tracking instead. All files stay visible."
            },
            {
                label: "No, let me commit them first",
                description: "Cancel development. I'll commit these files properly before re-running /dev."
            }
        ]
    }]
)

# Handle confirmation response
SWITCH confirmation_response_answers["Confirm Stash"]:

    CASE "Yes, stash them (I understand they'll be hidden)":
        Display: "Executing git stash..."
        Display: ""

        # Execute stash with clear message
        current_timestamp = current date/time
        Bash(
            command="git stash push -m 'WIP: Stashed by /dev {STORY-ID} at {current_timestamp}' --include-untracked",
            description="Stash all changes including untracked files"
        )

        Display: ""
        Display: "✅ Stashed {total_files} files to stash@{0}"
        Display: ""
        Display: "╔═══════════════════════════════════════════════════════════════╗"
        Display: "║  📝 IMPORTANT: TO RESTORE YOUR FILES                          ║"
        Display: "╠═══════════════════════════════════════════════════════════════╣"
        Display: "║                                                               ║"
        Display: "║  After this development session completes, run:               ║"
        Display: "║                                                               ║"
        Display: "║    git stash pop                                              ║"
        Display: "║                                                               ║"
        Display: "║  This will restore your {total_files} files.                 ║"
        Display: "║                                                               ║"
        Display: "╚═══════════════════════════════════════════════════════════════╝"
        Display: ""

        SET workflow_mode = "git"
        RETURN workflow_mode to Step 0.1.5

    CASE "No, continue without stashing instead":
        Display: "✅ Cancelled stashing. Proceeding with file-based tracking."
        Display: "   All {total_files} files remain visible."
        Display: ""

        SET workflow_mode = "file-based"
        RETURN workflow_mode to Step 0.1.5

    CASE "No, let me commit them first":
        Display: "✅ Cancelled stashing. Development paused."
        Display: ""
        Display: "Please commit your changes:"
        Display: "  git add ."
        Display: "  git commit -m 'WIP: Checkpoint before {STORY-ID}'"
        Display: ""
        Display: "Then re-run: /dev {STORY-ID}"
        Display: ""

        HALT execution
        Exit workflow
```

**Success Criteria:**
- Warning box displays BEFORE stashing
- User sees list of files that will be hidden (first 10 untracked shown)
- Story files explicitly called out if present (with count)
- Recovery commands shown before AND after stashing
- Double confirmation required (Step 0.1.5 asks once, Step 0.1.6 confirms again)
- User can cancel and choose file-based tracking instead (via "No, continue without stashing")
- User can cancel and commit first (via "No, let me commit them first")

**Token cost:** ~2,000 tokens (includes file listing, warning box, second AskUserQuestion)

**Rationale:** The RCA-008 incident showed users don't understand git stash behavior with `--include-untracked`. This double-confirmation with clear warnings prevents accidental file hiding.

---

## Step 0.2: Git Worktree Auto-Management [CONDITIONAL - IF $GIT_AVAILABLE == true]

**Purpose:** Automatically create and manage Git worktrees for parallel story development (STORY-091).

**When to execute:** Only when Git is available ($GIT_AVAILABLE == true) AND worktree management is enabled in config.

**Pre-check: Configuration enabled flag:**

```
# Load parallel.yaml config
config_path = "devforgeai/config/parallel.yaml"

IF file_exists(config_path):
    config = load_yaml(config_path)
ELSE:
    config = {enabled: true}  # Default enabled

IF config.enabled == false:
    Display: "Worktree management disabled via config - using branch-only workflow"
    SKIP to Step 0.3
    RETURN
```

**Invoke git-worktree-manager subagent:**

```
Task(
  subagent_type="git-worktree-manager",
  description="Manage worktree for ${STORY_ID}",
  prompt="Manage Git worktree for story ${STORY_ID}.

    Configuration: devforgeai/config/parallel.yaml

    Tasks:
    1. Load configuration (threshold, max, pattern)
    2. Check for existing worktree for this story
    3. Scan all worktrees for idle detection
    4. Validate integrity if worktree exists
    5. Determine required action

    Return JSON with status and actions."
)
```

**Parse subagent response and handle actions:**

```javascript
result = parse_json(subagent_output)

// Handle story-specific worktree
IF result.story_worktree.action_needed == "CREATE":
    // Create new worktree
    path = result.story_worktree.path
    branch = result.story_worktree.branch
    Bash(command="git worktree add ${path} -b ${branch}", description="Create story worktree")
    Display: "Created worktree: ${path} (branch: ${branch})"
    $WORKTREE_PATH = path

ELIF result.story_worktree.action_needed == "RESUME":
    path = result.story_worktree.path
    Display: "Resuming in existing worktree: ${path}"
    $WORKTREE_PATH = path

ELIF result.story_worktree.action_needed == "REPAIR":
    // Corrupted worktree detected
    path = result.story_worktree.path
    Display: "⚠ Corrupted worktree detected at ${path}"
    AskUserQuestion(
      questions=[{
        question: "Worktree at ${path} appears corrupted. How to proceed?",
        header: "Repair",
        options: [
          { label: "Delete and recreate", description: "Remove corrupted worktree, create fresh one" },
          { label: "Keep and continue", description: "Attempt to use existing (may have issues)" }
        ],
        multiSelect: false
      }]
    )

// Handle idle worktrees (if any detected)
IF result.idle_worktrees.length > 0:
    idle_count = result.idle_worktrees.length
    threshold = result.config.cleanup_threshold_days

    Display: "Found ${idle_count} idle worktrees (>${threshold} days):"
    FOR wt in result.idle_worktrees:
        Display: "  - ${wt.path} (idle ${wt.days_idle} days)"

    // Present 3-option cleanup prompt (AC#3)
    AskUserQuestion(
      questions=[{
        question: "How would you like to handle idle worktrees?",
        header: "Cleanup",
        options: [
          { label: "Resume Development", description: "Keep all worktrees, continue" },
          { label: "Fresh Start", description: "Delete current story worktree, create new" },
          { label: "Delete Old", description: "Delete idle worktrees not matching current story" }
        ],
        multiSelect: false
      }]
    )

    // Execute user selection
    SWITCH user_selection:
      CASE "Resume Development":
        // No action, continue
        Display: "✓ Keeping all worktrees"
      CASE "Fresh Start":
        Bash(command="git worktree remove ${$WORKTREE_PATH} --force", description="Remove current worktree")
        Bash(command="git worktree add ${path} -b ${branch}", description="Create fresh worktree")
        Display: "✓ Fresh worktree created"
      CASE "Delete Old":
        FOR idle_wt in result.idle_worktrees:
          IF idle_wt.path != $WORKTREE_PATH:
            Bash(command="git worktree remove ${idle_wt.path}", description="Remove idle worktree")
        Display: "✓ Deleted ${idle_count} idle worktrees"

// Handle max worktree limit (AC#7)
IF result.limit_reached AND result.story_worktree.action_needed == "CREATE":
    max = result.config.max_worktrees
    Display: "Maximum worktrees (${max}) reached."
    Display: "Active worktrees:"
    FOR wt in result.all_worktrees:
        Display: "  - ${wt.path} (last activity: ${wt.last_activity})"

    AskUserQuestion(
      questions=[{
        question: "Delete an existing worktree to continue?",
        header: "Limit Reached",
        options: result.all_worktrees.map(wt => ({
          label: wt.name,
          description: "Last activity: ${wt.last_activity}"
        })),
        multiSelect: false
      }]
    )

    // Delete selected worktree, then create new one
```

**Token cost:** ~2,500 tokens (subagent call + response handling)

**References:**
- Subagent: `.claude/agents/git-worktree-manager.md`
- Configuration: `devforgeai/config/parallel.yaml`
- Schema: `devforgeai/config/parallel.schema.json`

---

## Step 0.2.5: Dependency Graph Validation [MANDATORY]

**Purpose:** Validate story dependencies before TDD workflow begins (STORY-093).

**When to execute:** After git-worktree-manager (Step 0.2), before workflow adaptation (Step 0.3).

**Pre-check: Empty depends_on optimization:**

```
# Check if story has any dependencies
# (Extracted from story frontmatter already loaded in conversation)
IF depends_on is empty OR depends_on == []:
    Display: "✓ No dependencies declared - skipping dependency validation"
    SKIP to Step 0.3
    RETURN
```

**Invoke dependency-graph-analyzer subagent:**

```
Task(
  subagent_type="dependency-graph-analyzer",
  description="Validate dependencies for ${STORY_ID}",
  prompt="Analyze dependencies for story ${STORY_ID}.

    Story path: devforgeai/specs/Stories/

    Tasks:
    1. Extract depends_on from story frontmatter
    2. Build dependency graph with transitive resolution
    3. Detect circular dependencies
    4. Validate all dependency statuses
    5. Generate chain visualization

    Return JSON with validation results.
    BLOCKING: Return blocking=true if any dependency is invalid."
)
```

**Parse subagent response:**

```javascript
result = parse_json(subagent_output)

IF result.status == "PASS":
    Display: "✓ Dependency validation passed"
    Display: "  Dependencies: {result.dependencies.total_count}"
    Display: ""
    Display: result.chain_visualization
    Display: ""
    // Continue to Step 0.3

ELIF result.status == "BLOCKED":
    // Check for --force flag
    IF $FORCE_FLAG == true:
        // Log bypass to audit file
        timestamp = current_datetime_iso()
        log_path = ".devforgeai/logs/dependency-bypass-{timestamp}.log"

        Write(
            file_path=log_path,
            content="""# Dependency Bypass Log
Timestamp: {timestamp}
Story: {STORY_ID}
Bypassed Dependencies:
{json.dumps(result.validation.failures, indent=2)}
User: Requested via --force flag
"""
        )

        Display: "⚠️  DEPENDENCY CHECK BYPASSED (--force flag)"
        Display: ""
        Display: "The following dependency issues were bypassed:"
        FOR failure in result.validation.failures:
            Display: "  • {failure.message}"
        Display: ""
        Display: "Bypass logged to: {log_path}"
        Display: ""
        Display: "Proceeding to Step 0.3..."
        // Continue to Step 0.3

    ELSE:
        // Block execution
        Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        Display: "❌ DEPENDENCY VALIDATION FAILED"
        Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        Display: ""

        IF result.validation.cycle_detected:
            Display: "🔄 CIRCULAR DEPENDENCY DETECTED"
            Display: ""
            Display: "Cycle: {' → '.join(result.validation.cycle_path)}"
            Display: ""
            Display: "Resolution: Remove circular reference in one of the story files."

        ELIF result.validation.missing.length > 0:
            Display: "❓ MISSING DEPENDENCIES"
            Display: ""
            FOR dep in result.validation.missing:
                Display: "  • {dep} - Story file not found"
            Display: ""
            Display: "Resolution: Create the missing story files or remove the dependency."

        ELSE:
            Display: "⏳ DEPENDENCIES NOT READY"
            Display: ""
            FOR failure in result.validation.failures:
                Display: "  • {failure.message}"
                IF failure.suggestion:
                    Display: "    → {failure.suggestion}"
            Display: ""

        Display: ""
        Display: "Dependency chain:"
        Display: result.chain_visualization
        Display: ""
        Display: "Options:"
        Display: "  1. Complete dependent stories first"
        Display: "  2. Run with --force flag to bypass (not recommended):"
        Display: "     /dev {STORY_ID} --force"
        Display: ""
        Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

        HALT workflow (do not proceed to Step 0.3)

ELIF result.status == "ERROR":
    Display: "❌ Dependency analysis error: {result.error}"
    Display: "Proceeding with caution..."
    // Continue to Step 0.3 (graceful degradation)
```

**Token cost:** ~2,500 tokens (subagent call + response handling)

**References:**
- Subagent: `.claude/agents/dependency-graph-analyzer.md`
- Implementation: `src/dependency_graph_analyzer.py`
- Story: STORY-093 - Dependency Graph Enforcement with Transitive Resolution

---

## Step 0.2.6: File Overlap Detection [CONDITIONAL]

**Purpose:** Detect file overlaps with parallel stories before TDD workflow begins (STORY-094).

**When to execute:** After dependency-graph-analyzer (Step 0.2.5), before workflow adaptation (Step 0.3).

**Pre-check: Has technical_specification optimization:**

```
# Check if story has technical_specification section
# (Story content already loaded in conversation)
IF technical_specification section is empty OR not present:
    Display: "ℹ️ No technical_specification - skipping spec-based overlap detection"
    Display: "   Post-flight git-based detection will still run after Phase 3"
    $FILE_OVERLAP_PRE_FLIGHT = false
    SKIP to Step 0.3
    RETURN
```

**Invoke file-overlap-detector subagent:**

```
Task(
  subagent_type="file-overlap-detector",
  description="Detect file overlaps for ${STORY_ID}",
  prompt="Analyze file overlaps for story ${STORY_ID}.

    Mode: pre-flight
    Story path: devforgeai/specs/Stories/

    Tasks:
    1. Parse technical_specification from target story
    2. Extract all file_path values from components
    3. Scan stories with status 'In Development'
    4. Detect overlapping files
    5. Filter out depends_on story overlaps
    6. Generate recommendations

    Return JSON with overlap analysis.
    WARNING: Return status=WARNING if overlaps detected
    BLOCKING: Return status=BLOCKED if >= 10 files overlap"
)
```

**Parse subagent response:**

```javascript
result = parse_json(subagent_output)

IF result.status == "PASS":
    Display: "✓ File overlap check passed"
    Display: "  No overlapping files with parallel stories"
    $FILE_OVERLAP_PRE_FLIGHT = true
    // Continue to Step 0.3

ELIF result.status == "WARNING":
    // Overlaps detected but below blocking threshold
    Display: "⚠️ FILE OVERLAPS DETECTED"
    Display: ""
    Display: "Overlapping files found with parallel story/stories:"

    FOR story_id, files in result.overlaps:
        Display: "  • {story_id}: {files.length} file(s)"
        FOR file in files:
            Display: "    - {file}"
    Display: ""

    // Interactive prompt (AC#2)
    AskUserQuestion(
        questions=[{
            question: "File overlap detected. How would you like to proceed?",
            header: "Overlap Warning",
            multiSelect: false,
            options: [
                {
                    label: "Yes - Proceed",
                    description: "Continue with development (accept overlap risk)"
                },
                {
                    label: "No - Cancel",
                    description: "Cancel development to resolve overlap"
                },
                {
                    label: "Review - Show detailed report",
                    description: "View full overlap report before deciding"
                }
            ]
        }]
    )

    SWITCH user_response:
        CASE "Yes - Proceed":
            Display: "✓ Proceeding with acknowledged overlaps"
            $FILE_OVERLAP_PRE_FLIGHT = true
            // Continue to Step 0.3

        CASE "No - Cancel":
            Display: "Development cancelled due to file overlaps"
            HALT workflow

        CASE "Review - Show detailed report":
            Read(file_path=result.report_path)
            // Display report content
            // Re-ask question after review

ELIF result.status == "BLOCKED":
    // >= blocking_threshold overlaps
    Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Display: "❌ FILE OVERLAP DETECTION - BLOCKED"
    Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    Display: ""
    Display: "Severe file overlap detected ({result.overlap_count} files)"
    Display: ""
    FOR rec in result.recommendations:
        Display: "  • {rec}"
    Display: ""
    Display: "Report saved to: {result.report_path}"
    Display: ""

    IF $FORCE_FLAG == true:
        // Log bypass
        timestamp = current_datetime_iso()
        log_path = ".devforgeai/logs/overlap-bypass-{timestamp}.log"

        Write(
            file_path=log_path,
            content="""# File Overlap Bypass Log
Timestamp: {timestamp}
Story: {STORY_ID}
Overlaps bypassed: {result.overlap_count}
Overlapping stories:
{json.dumps(result.overlaps, indent=2)}
User: Requested via --force flag
"""
        )

        Display: "⚠️ FILE OVERLAP CHECK BYPASSED (--force flag)"
        Display: "Bypass logged to: {log_path}"
        $FILE_OVERLAP_PRE_FLIGHT = true
        // Continue to Step 0.3

    ELSE:
        Display: "To bypass (not recommended):"
        Display: "  /dev {STORY_ID} --force"
        Display: ""
        Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        HALT workflow

ELIF result.status == "ERROR":
    Display: "⚠️ File overlap analysis error: {result.error}"
    Display: "Proceeding with caution (spec-based detection skipped)..."
    $FILE_OVERLAP_PRE_FLIGHT = false
    // Continue to Step 0.3 (graceful degradation)
```

**Token cost:** ~2,000 tokens (subagent call + response handling)

**References:**
- Subagent: `.claude/agents/file-overlap-detector.md`
- Implementation: `src/file_overlap_detector.py`
- Story: STORY-094 - File Overlap Detection with Hybrid Analysis

---

## Step 0.3: Adapt TDD Workflow Based on Git Availability [MANDATORY]

**Workflow adaptations apply throughout all phases:**

**IF WORKFLOW_MODE == "file_based":**

- **Phase 01 (Context Validation):**
  - ✅ Check context files (same as git_based)
  - ✅ Validate story structure (same as git_based)
  - ⚠️ SKIP: Git status checks
  - ⚠️ SKIP: Branch validation

- **Phase 02-05 (Red/Green/Refactor/Integration):**
  - ✅ All TDD phases execute normally (test generation, implementation, refactoring)
  - ✅ All test execution works identically
  - ⚠️ SKIP: Any Git commands in these phases (if present)

- **Phase 08 (Git Workflow):**
  - ⚠️ REPLACE: Git commit workflow → File-based change tracking (see Step c.)

**IF WORKFLOW_MODE == "git_based":**
  - ✅ All phases execute normally with full Git integration

---

## Step 0.4: File-Based Change Tracking [MANDATORY IF WORKFLOW_MODE == "file_based"]

**ONLY executed when WORKFLOW_MODE == "file_based"**

This replaces Phase 08 (Git Workflow) with file-based artifact tracking.

**Implementation (executed in Phase 08 when Git unavailable):**

```markdown
### Phase 08 Alternative: File-Based Change Tracking

**ONLY when GIT_AVAILABLE == false**

#### Step 1: Create Change Documentation Directory

```
# Create story-specific changes directory
IF not exists devforgeai/stories/${STORY_ID}/changes/:
    # Use native Write tool to create directory marker
    Write(
        file_path="devforgeai/stories/${STORY_ID}/changes/.gitkeep",
        content="# Change tracking directory for ${STORY_ID}\n"
    )
```

#### Step 2: Generate Change Manifest

```
# Generate timestamp
TIMESTAMP = {current_datetime in ISO8601 format}

# List modified files (manual tracking since no Git)
# Developer must identify changed files from implementation work

Write(
    file_path="devforgeai/stories/${STORY_ID}/changes/implementation-${TIMESTAMP}.md",
    content="""# Implementation Changes - ${STORY_ID}

**Timestamp:** ${TIMESTAMP}
**Story:** ${STORY_TITLE}
**Phase:** Dev Complete
**Workflow Mode:** File-Based (Git not available)

## Files Created

${list_files_created_during_implementation}

## Files Modified

${list_files_modified_during_implementation}

## Files Deleted

${list_files_deleted_if_any}

## Test Results

- Total Tests: ${total_tests}
- Passed: ${passed_tests}
- Failed: ${failed_tests}
- Coverage: ${coverage_percentage}%

## Acceptance Criteria Status

${copy_acceptance_criteria_completion_status_from_story}

## Implementation Notes

${implementation_summary_from_story_Implementation_Notes_section}

## Next Steps

To enable full version control:
1. Initialize Git: git init
2. Add files: git add .
3. Create initial commit: git commit -m "Initial commit"
4. Re-run /dev to use Git-based workflow
"""
)

Display: "✓ File-based change manifest created"
Display: "  Location: devforgeai/stories/${STORY_ID}/changes/implementation-${TIMESTAMP}.md"
```

#### Step 3: Update Story File with Change Reference

```
Read(file_path="devforgeai/specs/Stories/${STORY_ID}.story.md")

# Add to Workflow History section
Edit(
    file_path="devforgeai/specs/Stories/${STORY_ID}.story.md",
    old_string="## Workflow History",
    new_string="""## Workflow History

### Development Complete - ${TIMESTAMP} (File-Based)
- **Status:** Dev Complete
- **Workflow Mode:** File-Based (Git not available)
- **Changes:** devforgeai/stories/${STORY_ID}/changes/implementation-${TIMESTAMP}.md
- **Tests:** ${passed_tests}/${total_tests} passing (${coverage_percentage}% coverage)
- **Note:** Git not available - changes tracked in story artifacts

{preserve existing workflow history below}
"""
)

Display: "✓ Story file updated with file-based tracking reference"
```

#### Step 4: Display Completion Summary

```
Display:
"┌─────────────────────────────────────────────────────────────────┐
│ ✅ Development Complete (File-Based Workflow)                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│ Story: ${STORY_ID} - ${STORY_TITLE}                            │
│ Status: Dev Complete                                            │
│                                                                 │
│ Tests: ${passed_tests}/${total_tests} passing                  │
│ Coverage: ${coverage_percentage}%                               │
│                                                                 │
│ Changes tracked in:                                             │
│   devforgeai/stories/${STORY_ID}/changes/implementation-...   │
│                                                                 │
│ Git Integration: Not Available                                  │
│                                                                 │
│ To enable Git workflow:                                         │
│   git init                                                      │
│   git add .                                                     │
│   git commit -m 'Initial commit'                               │
│   Then re-run: /dev ${STORY_ID}                                │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘"
```
```

**Benefits of file-based tracking:**
- Enables DevForgeAI in non-Git environments
- Maintains traceability through file artifacts
- Same TDD workflow, different tracking mechanism
- Clear path to Git migration when ready

---

## Step 0.5: Validate Context Files Exist [MANDATORY]

**Check for all 6 DevForgeAI context files:**

```
Read all 6 context files in PARALLEL:
- Read(file_path="devforgeai/specs/context/tech-stack.md")
- Read(file_path="devforgeai/specs/context/source-tree.md")
- Read(file_path="devforgeai/specs/context/dependencies.md")
- Read(file_path="devforgeai/specs/context/coding-standards.md")
- Read(file_path="devforgeai/specs/context/architecture-constraints.md")
- Read(file_path="devforgeai/specs/context/anti-patterns.md")
```

**If ANY file is missing:**

```
Display: "❌ Context files missing - architecture setup required"
Display: "  Missing files prevent development (would cause technical debt from assumptions)"
Display: ""
Display: "Invoking devforgeai-architecture skill to create context files..."

Skill(command="devforgeai-architecture")

Display: "✓ Architecture skill completed"
Display: "Re-validating context files..."

# Re-read context files after architecture skill completes
[Execute same parallel Read operations above]
```

**STOP development until all context files exist.** This prevents technical debt from ambiguous assumptions.

**Token cost:** ~2,000 tokens (6 files × ~300 tokens each, read in parallel)

---

## Step 0.6: Load Story Specification [MANDATORY]

**Story already loaded via @file reference from slash command.**

The story file was loaded by the `/dev` command via:
```
@devforgeai/specs/Stories/STORY-XXX.story.md
```

**Verify story content accessible:**
- [ ] YAML frontmatter with id, title, status, epic, sprint
- [ ] Acceptance criteria section exists
- [ ] Technical specification section exists
- [ ] Non-functional requirements documented

**If story content not available in conversation:**
```
HALT with error:
"Story file not loaded in conversation context.

Expected: Story loaded via @file reference from /dev command
Actual: No story content found

Please ensure /dev command properly loads story file before invoking this skill."
```

---

## Step 0.7: Validate Spec vs Context Files [MANDATORY]

**Check for conflicts between story requirements and context file constraints:**

From story Technical Specification section, extract:
- Required technologies (languages, frameworks, libraries)
- Required patterns (architectures, designs)
- File locations (where code should be placed)

Compare against:
- tech-stack.md (locked technologies)
- architecture-constraints.md (design patterns)
- source-tree.md (file placement rules)

**If conflicts detected → Use AskUserQuestion:**

```
Question: "Spec requires [X], but tech-stack.md specifies [Y]. Which is correct?"
Header: "Spec conflict"
options:
  - label: "Follow tech-stack.md (use [Y])"
    description: "Maintain consistency with existing architecture"
  - label: "Update tech-stack.md (use [X] + create ADR)"
    description: "Document architecture change in ADR and update tech-stack.md"
multiSelect: false
```

**After user response:**
- If "Update tech-stack.md" chosen:
  - Create ADR documenting technology decision
  - Update tech-stack.md
  - Proceed with development
- If "Follow tech-stack.md" chosen:
  - Proceed with development using tech-stack.md technologies

**Token cost:** ~1,000 tokens (conflict detection) + ~3,000 (if AskUserQuestion needed)

---

## Step 0.8: Detect and Validate Technology Stack [MANDATORY]

**Invoke tech-stack-detector subagent to detect technologies and validate against tech-stack.md:**

```
Task(
  subagent_type="tech-stack-detector",
  description="Detect and validate tech stack",
  prompt="Analyze the project structure in the current directory.

  Detect:
  1. Primary programming language
  2. Framework/runtime
  3. Test framework
  4. Build tool
  5. Package manager

  Then validate against devforgeai/specs/context/tech-stack.md if it exists.

  Return JSON with detected technologies, validation results, and recommended commands.

  CRITICAL: If conflicts found between detected and specified technologies, provide clear resolution options."
)
```

**Parse subagent JSON response:**

```javascript
result = parse_json(subagent_output)

# Extract detected technologies
LANGUAGE = result["detected"]["language"]["primary"]
FRAMEWORK = result["detected"]["framework"]["name"]
TEST_FRAMEWORK = result["detected"]["test_framework"]["primary"]

# Extract workflow commands (CRITICAL - used in subsequent phases)
TEST_COMMAND = result["commands"]["test"]
TEST_COVERAGE_COMMAND = result["commands"]["test_coverage"]
BUILD_COMMAND = result["commands"]["build"]
INSTALL_COMMAND = result["commands"]["install"]

# Check validation status
VALIDATION_STATUS = result["validation"]["status"]

IF VALIDATION_STATUS == "PASS":
    Display: "✓ Technology stack validated"
    Display: "  - Language: {LANGUAGE}"
    Display: "  - Framework: {FRAMEWORK}"
    Display: "  - Test framework: {TEST_FRAMEWORK}"
    Display: "  - Test command: {TEST_COMMAND}"

ELIF VALIDATION_STATUS == "FAIL":
    # CRITICAL conflicts detected - HALT
    Display: "❌ Technology stack validation FAILED"
    Display: "Conflicts detected between project and tech-stack.md"

    FOR conflict in result["validation"]["conflicts"]:
        IF conflict["severity"] == "CRITICAL":
            # Use AskUserQuestion to resolve
            AskUserQuestion:
                question: "Project uses {conflict['detected']} but tech-stack.md specifies {conflict['specified']}. How to resolve?"
                header: "Tech Conflict"
                options:
                    - label: "Follow spec (update project)"
                      description: "Change project to use {conflict['specified']}"
                    - label: "Update spec (create ADR)"
                      description: "Update tech-stack.md, document in ADR"
                multiSelect: false

            # Handle user response
            IF "Update spec" chosen:
                # Create ADR, update tech-stack.md, re-validate

ELIF VALIDATION_STATUS == "ERROR":
    IF result["validation"]["context_missing"]:
        # tech-stack.md not found - invoke architecture skill
        Display: "❌ tech-stack.md not found"
        Display: "Invoking devforgeai-architecture skill..."
        Skill(command="devforgeai-architecture")

        # After architecture completes, re-run tech-stack-detector
        # [Re-invoke Task with same parameters]

# Store commands for Phases 1-5
$TEST_COMMAND = TEST_COMMAND
$TEST_COVERAGE_COMMAND = TEST_COVERAGE_COMMAND
$BUILD_COMMAND = BUILD_COMMAND
```

**Token cost:** ~700 tokens in skill context (~8,000 in isolated subagent context)

---

## Step 0.9: Detect Previous QA Failures [MANDATORY]

**Check if story has failed QA due to deferral or other issues:**

```
# Search for QA reports for this story
Glob(pattern="devforgeai/qa/reports/${STORY_ID}-qa-report*.md")

IF reports found:
    # Read most recent report
    reports_sorted = sort_by_timestamp(reports)
    latest_report = reports_sorted[0]

    Read(file_path=latest_report)

    # Parse QA status
    IF report contains "Status: FAILED":
        # Extract failure type
        IF report contains "Deferral Validation FAILED":
            # Deferral-specific failure
            Display: "⚠ Previous QA failed due to deferral issues"
            Display: "  QA Report: {latest_report}"
            Display: ""

            # Extract deferral violations from report
            Grep(
                pattern="- \\[ \\] .* - (Deferred to|Blocked by|Out of scope)",
                path=latest_report,
                output_mode="content",
                -n=true
            )

            Display: "Development will focus on resolving deferral issues."
            Display: "The 'Handling QA Deferral Failures' workflow will guide resolution."
            Display: ""

            # Set flag for later use
            $QA_DEFERRAL_FAILURE = true
            $QA_FAILURE_REPORT = latest_report

        ELIF report contains "Coverage Below Threshold":
            Display: "⚠ Previous QA failed due to coverage issues"
            Display: "  Focus: Increase test coverage"
            $QA_COVERAGE_FAILURE = true

        ELIF report contains "Anti-Pattern Violations":
            Display: "⚠ Previous QA failed due to anti-patterns"
            Display: "  Focus: Refactor to remove violations"
            $QA_ANTIPATTERN_FAILURE = true

        ELSE:
            Display: "⚠ Previous QA failed (review report for details)"
            Display: "  Report: {latest_report}"
            $QA_GENERIC_FAILURE = true

    ELIF report contains "Status: PASSED":
        # QA already passed - unusual to be in Dev again
        Display: "Note: QA already passed for this story"
        Display: "  Proceeding with development (may be enhancement or bug fix)"
        $QA_PASSED = true

ELSE:
    # No QA reports found - first development iteration
    Display: "✓ First development iteration (no previous QA attempts)"
    $QA_FIRST_ITERATION = true
```

**Token cost:** ~1,500 tokens (Glob + Read + Grep + parsing)

**Use in subsequent phases:**
- If `$QA_DEFERRAL_FAILURE == true` → Invoke "Handling QA Deferral Failures" workflow
- If `$QA_COVERAGE_FAILURE == true` → Focus on test coverage in Phase 02
- If `$QA_ANTIPATTERN_FAILURE == true` → Extra validation in Phase 04 (Refactor)

---

## Step 0.9.5: Load Structured Gap Data (gaps.json) [IF QA FAILED]

**Purpose:** Parse machine-readable gap data for targeted remediation workflow.

**When to execute:** After Step 0.9 detects `$QA_COVERAGE_FAILURE`, `$QA_ANTIPATTERN_FAILURE`, or `$QA_DEFERRAL_FAILURE`

```
# Check if structured gap export exists
gaps_file = "devforgeai/qa/reports/${STORY_ID}-gaps.json"

Glob(pattern=gaps_file)

IF gaps_file EXISTS:
    Display: ""
    Display: "╔═══════════════════════════════════════════════════════════════╗"
    Display: "║  📊 STRUCTURED GAP DATA DETECTED                              ║"
    Display: "╠═══════════════════════════════════════════════════════════════╣"
    Display: "║                                                               ║"
    Display: "║  QA-Dev Integration: ACTIVE                                   ║"
    Display: "║  Gap file: {gaps_file}                                        ║"
    Display: "║                                                               ║"
    Display: "║  Development will enter REMEDIATION MODE:                     ║"
    Display: "║  • Targeted test generation for specific gaps                 ║"
    Display: "║  • Focus on coverage failures by file                         ║"
    Display: "║  • Suggested tests provided                                   ║"
    Display: "║                                                               ║"
    Display: "╚═══════════════════════════════════════════════════════════════╝"
    Display: ""

    # Read and parse gaps.json
    Read(file_path=gaps_file)
    gaps_data = parse_json(file_content)

    # Build $QA_COVERAGE_GAPS array for Phase 02 consumption
    $QA_COVERAGE_GAPS = []

    FOR EACH gap in gaps_data.coverage_gaps:
        gap_entry = {
            "file": gap.file,
            "layer": gap.layer,
            "current_coverage": gap.current_coverage,
            "target_coverage": gap.target_coverage,
            "gap_percentage": gap.gap_percentage,
            "uncovered_line_count": gap.uncovered_line_count,
            "suggested_tests": gap.suggested_tests
        }
        $QA_COVERAGE_GAPS.append(gap_entry)

    # Build $QA_ANTIPATTERN_GAPS for Phase 04 consumption
    $QA_ANTIPATTERN_GAPS = gaps_data.anti_pattern_violations

    # Build $QA_DEFERRAL_GAPS for Phase 06 consumption
    $QA_DEFERRAL_GAPS = gaps_data.deferral_issues

    # Display summary
    Display: "Gap Summary:"
    Display: ""

    IF $QA_COVERAGE_GAPS.count > 0:
        Display: "📉 Coverage Gaps: {$QA_COVERAGE_GAPS.count} files below threshold"
        FOR EACH gap in $QA_COVERAGE_GAPS:
            Display: "   • {gap.file}: {gap.current_coverage}% → need {gap.target_coverage}% (gap: {gap.gap_percentage}%)"
            Display: "     Suggested tests:"
            FOR EACH test in gap.suggested_tests:
                Display: "       - {test}"
        Display: ""

    IF $QA_ANTIPATTERN_GAPS.count > 0:
        Display: "⚠️  Anti-Pattern Violations: {$QA_ANTIPATTERN_GAPS.count} issues to resolve"
        FOR EACH violation in $QA_ANTIPATTERN_GAPS:
            Display: "   • {violation.file}:{violation.line} - {violation.type} ({violation.severity})"
        Display: ""

    IF $QA_DEFERRAL_GAPS.count > 0:
        Display: "📋 Deferral Issues: {$QA_DEFERRAL_GAPS.count} items need resolution"
        FOR EACH deferral in $QA_DEFERRAL_GAPS:
            Display: "   • {deferral.item}: {deferral.violation_type}"
        Display: ""

    # Set remediation mode flag
    $REMEDIATION_MODE = true
    Display: "✅ Remediation mode enabled - see qa-remediation-workflow.md for targeted workflow"
    Display: ""

ELSE:
    # No gaps.json - use legacy markdown parsing (Step 0.8 results)
    Display: "ℹ️  No structured gap data (gaps.json) found"
    Display: "   Using legacy QA report parsing for failure context"
    Display: "   (To enable targeted remediation, re-run /qa {STORY_ID})"
    Display: ""
    $REMEDIATION_MODE = false
```

**Token cost:** ~800 tokens (Glob + Read + JSON parse + display)

**Variables set for Phases 1-5:**
- `$QA_COVERAGE_GAPS` - Array of coverage gap objects with file:line targets
- `$QA_ANTIPATTERN_GAPS` - Array of anti-pattern violations with remediation
- `$QA_DEFERRAL_GAPS` - Array of deferral issues with required actions
- `$REMEDIATION_MODE` - Boolean flag for targeted workflow

**Use in subsequent phases:**
- Phase 02: Pass `$QA_COVERAGE_GAPS` to test-automator for targeted test generation
- Phase 04: Pass `$QA_ANTIPATTERN_GAPS` to refactoring-specialist for targeted fixes
- Phase 06: Pre-load `$QA_DEFERRAL_GAPS` for deferral resolution

**See also:** `qa-remediation-workflow.md` for detailed remediation mode workflow

---

## ✅ PHASE 01 COMPLETION CHECKPOINT

**Before proceeding to Phase 02 (Test-First Design), verify ALL pre-flight validations passed:**

### Mandatory Steps Executed

- [ ] **Step 0.1:** git-validator subagent invoked, Git status assessed
- [ ] **Step 0.1.5:** User consent obtained (if uncommitted changes > 10)
- [ ] **Step 0.1.6:** Stash warnings shown (if user selected stash)
- [ ] **Step 0.2:** Git Worktree Auto-Management (if Git available + enabled)
- [ ] **Step 0.2.5:** Dependency Graph Validation (STORY-093) - validated or --force bypassed
- [ ] **Step 0.3:** Workflow mode determined (git-based or file-based)
- [ ] **Step 0.4:** File-based tracking setup (if WORKFLOW_MODE == "file_based")
- [ ] **Step 0.5:** All 6 context files validated (exist and non-empty)
- [ ] **Step 0.6:** Story specification loaded (via @file reference)
- [ ] **Step 0.7:** Spec vs. context conflicts resolved (via AskUserQuestion if conflicts)
- [ ] **Step 0.8:** tech-stack-detector invoked, technologies validated
- [ ] **Step 0.9:** Previous QA failures detected (recovery mode if needed)
- [ ] **Step 0.9.5:** Structured gap data loaded (if gaps.json exists)

### Variables Set for Phases 02-08

- [ ] `$GIT_AVAILABLE` = true/false
- [ ] `$WORKFLOW_MODE` = "full" / "partial" / "fallback"
- [ ] `$CAN_COMMIT` = true/false
- [ ] `$WORKTREE_PATH` = (worktree path, if created)
- [ ] `$TEST_COMMAND` = (pytest / npm test / dotnet test / etc.)
- [ ] `$TEST_COVERAGE_COMMAND` = (with coverage flags)
- [ ] `$BUILD_COMMAND` = (language-specific build command)
- [ ] `$QA_*_FAILURE` = Boolean flags (if QA failure detected)
- [ ] `$REMEDIATION_MODE` = true/false (if gaps.json loaded)
- [ ] `$QA_COVERAGE_GAPS` = Array (if gaps.json has coverage gaps)
- [ ] `$QA_ANTIPATTERN_GAPS` = Array (if gaps.json has anti-patterns)
- [ ] `$QA_DEFERRAL_GAPS` = Array (if gaps.json has deferrals)

### Success Criteria

- [ ] All 6 context files exist
- [ ] No conflicts between story spec and context files
- [ ] Technology stack detected and validated
- [ ] Test commands identified and executable
- [ ] Git workflow mode determined
- [ ] User consented to git operations (if applicable)
- [ ] Ready to begin TDD workflow

### Checkpoint Validation

**IF ANY ITEM UNCHECKED:**
```
❌ PHASE 01 INCOMPLETE - Review missing steps above
⚠️  DO NOT PROCEED TO PHASE 02 until all checkpoints pass
⚠️  Missing validations will cause failures in later phases

Common issues:
  - Context files missing → Run /create-context
  - Git not initialized → Initialize git or use file-based mode
  - Spec conflicts → Resolve via AskUserQuestion
  - Tech stack mismatch → Update tech-stack.md or adjust story
```

**IF ALL ITEMS CHECKED:**
```
✅ PHASE 01 COMPLETE - All Pre-Flight Validations Passed

Variables set: {count} variables configured
Context files: 6/6 validated
Git mode: {WORKFLOW_MODE}
Test framework: {TEST_COMMAND}

Ready to begin TDD cycle.

**Update Progress Tracker:**
Mark "Execute Phase 01" todo as "completed"

**See Also:**
- `tdd-red-phase.md` - Phase 02 workflow (test generation)
- `parameter-extraction.md` - Story ID extraction details
- `ambiguity-protocol.md` - When to use AskUserQuestion

Next: Load tdd-red-phase.md and execute Phase 02 (Test-First Design - Red Phase)
```
