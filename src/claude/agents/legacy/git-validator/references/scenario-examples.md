# Git Validator - Scenario Output Examples

Reference examples for the five Git status scenarios.

---

#### Example 1: Ready State (Best Case)

```json
{
  "git_status": {
    "installed": true,
    "repository_exists": true,
    "initialized": true,
    "commit_count": 42,
    "current_branch": "feature/user-authentication",
    "uncommitted_changes": 0,
    "detached_head": false
  },
  "assessment": {
    "status": "READY",
    "workflow_mode": "full",
    "can_commit": true,
    "can_push": true,
    "warnings": [],
    "blockers": []
  },
  "recommendations": {
    "primary_action": null,
    "commands": [],
    "fallback_available": true,
    "fallback_description": "File-based tracking available but Git preferred"
  }
}
```

#### Example 2: Uncommitted Changes

```json
{
  "git_status": {
    "installed": true,
    "repository_exists": true,
    "initialized": true,
    "commit_count": 15,
    "current_branch": "main",
    "uncommitted_changes": 7,
    "detached_head": false
  },
  "assessment": {
    "status": "UNCOMMITTED",
    "workflow_mode": "full",
    "can_commit": true,
    "can_push": false,
    "warnings": [
      "7 uncommitted changes detected",
      "Recommend committing or stashing before new development"
    ],
    "blockers": []
  },
  "recommendations": {
    "primary_action": "Commit or stash changes",
    "commands": [
      "git status  # Review changes",
      "git add .   # Stage all changes",
      "git commit -m 'WIP: Checkpoint before new feature'",
      "OR",
      "git stash push -m 'Temporary stash'"
    ],
    "fallback_available": true,
    "fallback_description": "Can proceed but recommend cleaning working directory first"
  }
}
```

#### Example 3: Repo Exists, No Commits

```json
{
  "git_status": {
    "installed": true,
    "repository_exists": true,
    "initialized": true,
    "commit_count": 0,
    "current_branch": "main",
    "uncommitted_changes": 0,
    "detached_head": false
  },
  "assessment": {
    "status": "INIT_REQUIRED",
    "workflow_mode": "partial",
    "can_commit": true,
    "can_push": false,
    "warnings": [
      "Git repository initialized but no commits yet"
    ],
    "blockers": [
      "Initial commit required for full Git workflow"
    ]
  },
  "recommendations": {
    "primary_action": "Create initial commit",
    "commands": [
      "git add .",
      "git commit -m 'Initial commit'"
    ],
    "fallback_available": true,
    "fallback_description": "File-based tracking available as alternative"
  }
}
```

#### Example 4: Not Initialized

```json
{
  "git_status": {
    "installed": true,
    "repository_exists": false,
    "initialized": false,
    "commit_count": 0,
    "current_branch": null,
    "uncommitted_changes": 0,
    "detached_head": false
  },
  "assessment": {
    "status": "NOT_INITIALIZED",
    "workflow_mode": "fallback",
    "can_commit": false,
    "can_push": false,
    "warnings": [
      "Directory is not a Git repository"
    ],
    "blockers": [
      "Git repository initialization required for version control"
    ]
  },
  "recommendations": {
    "primary_action": "Initialize Git repository",
    "commands": [
      "git init",
      "git add .",
      "git commit -m 'Initial commit'"
    ],
    "fallback_available": true,
    "fallback_description": "File-based change tracking in devforgeai/stories/{STORY-ID}/changes/"
  }
}
```

#### Example 5: Git Missing

```json
{
  "git_status": {
    "installed": false,
    "repository_exists": false,
    "initialized": false,
    "commit_count": 0,
    "current_branch": null,
    "uncommitted_changes": 0,
    "detached_head": false
  },
  "assessment": {
    "status": "GIT_MISSING",
    "workflow_mode": "fallback",
    "can_commit": false,
    "can_push": false,
    "warnings": [
      "Git is not installed or not accessible"
    ],
    "blockers": [
      "Git installation required for version control features"
    ]
  },
  "recommendations": {
    "primary_action": "Install Git",
    "commands": [
      "# Windows:",
      "winget install Git.Git",
      "",
      "# Linux (Debian/Ubuntu):",
      "sudo apt-get install git",
      "",
      "# macOS:",
      "brew install git"
    ],
    "fallback_available": true,
    "fallback_description": "DevForgeAI can proceed with file-based tracking but Git strongly recommended"
  }
}
```
