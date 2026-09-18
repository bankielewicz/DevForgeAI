# Git Worktree Manager - Examples

---

## Example 1: Worktree Needs Creation

```
Task(
  subagent_type="git-worktree-manager",
  description="Check worktree status for STORY-091",
  prompt="Manage Git worktree for story STORY-091. Load config from devforgeai/config/parallel.yaml. Return JSON with status and actions."
)
```

**Expected Response:**
```json
{
  "status": "SUCCESS",
  "platform": "linux",
  "story_worktree": {
    "exists": false,
    "path": "../devforgeai-story-091/",
    "branch": "story-091",
    "action_needed": "CREATE"
  },
  "idle_worktrees": [],
  "active_count": 2,
  "limit_reached": false,
  "config": {
    "cleanup_threshold_days": 7,
    "max_worktrees": 5,
    "location_pattern": "../devforgeai-story-{id}/"
  },
  "timestamp": "2026-02-13T10:30:00Z"
}
```

**/dev command action:** Execute `git worktree add ../devforgeai-story-091/ -b story-091`

### Example 2: Limit Reached with Idle Detection

```
Task(
  subagent_type="git-worktree-manager",
  description="Check worktree status for STORY-125",
  prompt="Manage Git worktree for story STORY-125. Configuration at devforgeai/config/parallel.yaml. Return JSON with action and idle recommendations."
)
```

**Expected Response:**
```json
{
  "status": "WARNING",
  "platform": "linux",
  "story_worktree": {
    "exists": false,
    "path": "../devforgeai-story-125/",
    "branch": "story-125",
    "action_needed": "CREATE"
  },
  "idle_worktrees": [
    {
      "path": "../devforgeai-story-031/",
      "name": "devforgeai-story-031",
      "days_idle": 8,
      "last_activity": "2026-02-05T14:23:00Z"
    }
  ],
  "active_count": 5,
  "limit_reached": true,
  "config": {
    "cleanup_threshold_days": 7,
    "max_worktrees": 5,
    "location_pattern": "../devforgeai-story-{id}/"
  },
  "timestamp": "2026-02-13T10:35:00Z"
}
```

**/dev command action:** Report limit reached, recommend cleaning devforgeai-story-031 before creating new worktree

---

**Created:** 2025-12-15
**Story:** STORY-091 - Git Worktree Auto-Management
**Status:** Phase 03 Implementation
**Migrated to v2.0.0:** 2026-02-13
