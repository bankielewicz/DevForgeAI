# Git Validator - Error Handling Scenarios

Reference for error handling detection and JSON response formats.

---

## Error Handling

### Scenario 1: Git Command Fails

**Detection:** Bash command exits with error, stderr output

**Response:**
```json
{
  "git_status": {
    "installed": false,
    "repository_exists": false,
    "error": "Git command failed: [stderr output]"
  },
  "assessment": {
    "status": "ERROR",
    "workflow_mode": "fallback",
    "warnings": ["Git validation failed - check Git installation"],
    "blockers": []
  },
  "recommendations": {
    "primary_action": "Verify Git installation",
    "commands": ["git --version"],
    "fallback_available": true
  }
}
```

### Scenario 2: Detached HEAD State

**Detection:** `git branch --show-current` returns empty

**Response:**
```json
{
  "git_status": {
    "installed": true,
    "repository_exists": true,
    "initialized": true,
    "commit_count": 25,
    "current_branch": null,
    "detached_head": true
  },
  "assessment": {
    "status": "READY",
    "workflow_mode": "full",
    "warnings": [
      "Repository in detached HEAD state",
      "Recommend checking out a branch before development"
    ]
  },
  "recommendations": {
    "primary_action": "Checkout branch",
    "commands": [
      "git branch  # List branches",
      "git checkout main  # Return to main branch",
      "OR",
      "git checkout -b feature/new-feature  # Create new branch"
    ]
  }
}
```

### Scenario 3: Permission Issues

**Detection:** Git commands fail with "Permission denied"

**Response:**
```json
{
  "git_status": {
    "installed": true,
    "repository_exists": false,
    "error": "Permission denied"
  },
  "assessment": {
    "status": "ERROR",
    "workflow_mode": "fallback",
    "warnings": ["Git permission error"],
    "blockers": ["Insufficient permissions to access .git directory"]
  },
  "recommendations": {
    "primary_action": "Check permissions",
    "commands": [
      "ls -la .git  # Check .git directory permissions",
      "sudo chown -R $USER:$USER .git  # Fix ownership (if appropriate)"
    ],
    "fallback_available": true
  }
}
```
