# Git Validator - Parent Skill Integration

Reference for invoking git-validator from parent skills and parsing responses.

---

## Example Invocations

### From spec-driven-dev Skill:

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

### Response Parsing in Skill:

```
result = parse_json(subagent_output)

# Store workflow mode
WORKFLOW_MODE = result["assessment"]["workflow_mode"]
GIT_AVAILABLE = result["git_status"]["installed"]
CAN_COMMIT = result["assessment"]["can_commit"]

if WORKFLOW_MODE == "full":
    # Enable full Git workflow
    Display: "✓ Git repository detected - full workflow enabled"
    Display: "  - Branch: {result['git_status']['current_branch']}"
    Display: "  - Commits: {result['git_status']['commit_count']}"

    if result["git_status"]["uncommitted_changes"] > 0:
        Display: "  ⚠️  {result['git_status']['uncommitted_changes']} uncommitted changes"
        Display: "  Recommendation: Commit or stash before proceeding"

elif WORKFLOW_MODE == "partial":
    # Git available but needs initial commit
    Display: "⚠ Git repository needs initial commit"
    Display: "  Commands:"
    for cmd in result["recommendations"]["commands"]:
        Display: "    {cmd}"

elif WORKFLOW_MODE == "fallback":
    # File-based tracking
    Display: "⚠ Git not available - using file-based workflow"

    if result["git_status"]["installed"]:
        # Git installed but repo not initialized
        Display: "  Git is installed. To enable full workflow:"
        for cmd in result["recommendations"]["commands"]:
            Display: "    {cmd}"
    else:
        # Git not installed
        Display: "  Git not installed. To install:"
        for cmd in result["recommendations"]["commands"]:
            Display: "    {cmd}"

    Display: ""
    Display: "  Fallback: Changes tracked in story artifacts"
    Display: "  Location: devforgeai/stories/{STORY-ID}/changes/"

# Configure Git workflow based on availability
if CAN_COMMIT:
    # Enable Git operations in subsequent phases
    USE_GIT_COMMITS = true
else:
    # Use file-based change tracking
    USE_GIT_COMMITS = false
```
