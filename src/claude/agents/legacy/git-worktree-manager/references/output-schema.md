# Git Worktree Manager - Output Format Reference

## Expected Output Format

```json
{
  "status": "SUCCESS|WARNING|ERROR",
  "platform": "linux|macos|windows|wsl",
  "story_worktree": {
    "exists": boolean,
    "path": "../devforgeai-story-091/",
    "branch": "story-091",
    "action_needed": "CREATE|RESUME|REPAIR|NONE"
  },
  "idle_worktrees": [
    {
      "path": "../devforgeai-story-031/",
      "name": "devforgeai-story-031",
      "days_idle": 8,
      "last_activity": "2025-12-07T14:23:00Z"
    }
  ],
  "active_count": 3,
  "limit_reached": false,
  "config": {
    "cleanup_threshold_days": 7,
    "max_worktrees": 5,
    "location_pattern": "../devforgeai-story-{id}/"
  },
  "timestamp": "2025-12-15T15:50:00Z"
}
```

## Output Format Detail

The subagent produces structured JSON output with the following schema:

**Primary Artifacts:**
- `stdout`: Complete JSON response (status, worktree data, idle detection, config, timestamp)
- Exit Code 0: Success or recoverable warning
- Exit Code 1: Fatal error (Git not available, version incompatible, config invalid)

**Data Structure:**
- status: "SUCCESS" | "WARNING" | "ERROR"
- platform: "linux" | "macos" | "windows" | "wsl"
- story_worktree: Object with {exists, path, branch, action_needed}
- idle_worktrees: Array of idle worktree objects
- active_count: Integer count of active worktrees
- limit_reached: Boolean indicating if max concurrent limit hit
- config: Echo of effective configuration settings
- timestamp: ISO8601 timestamp of execution

**Consumption by /dev command:**
- Parse JSON response and extract story_worktree.action_needed
- Use path for cd/checkout operations
- Use branch for git worktree add command
- Use idle_worktrees for cleanup recommendations
- Log status for user visibility
