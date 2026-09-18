# Git Validator - Output Format Reference

Complete output format specification with field descriptions for the git-validator JSON response.

---

## Output Format

**git-validator always returns a JSON object with the following structure:**

```json
{
  "git_status": {
    "installed": boolean,
    "repository_exists": boolean,
    "initialized": boolean,
    "commit_count": number,
    "current_branch": string | null,
    "uncommitted_changes": number,
    "detached_head": boolean,
    "error": string | null
  },
  "file_analysis": {
    "modified_files": number,
    "untracked_files": number,
    "deleted_files": number,
    "added_files": number,
    "file_breakdown": {
      "story_files": number,
      "python_cache": number,
      "config_files": number,
      "documentation": number,
      "code": number,
      "other": number
    },
    "notable_untracked": [
      string,
      string
    ]
  },
  "assessment": {
    "status": "READY" | "UNCOMMITTED" | "INIT_REQUIRED" | "NOT_INITIALIZED" | "GIT_MISSING" | "ERROR",
    "workflow_mode": "full" | "partial" | "fallback",
    "can_commit": boolean,
    "can_push": boolean,
    "warnings": [
      string
    ],
    "blockers": [
      string
    ]
  },
  "recommendations": {
    "primary_action": string | null,
    "commands": [
      string
    ],
    "fallback_available": boolean,
    "fallback_description": string
  }
}
```

**Field Descriptions:**

| Field | Type | Meaning |
|-------|------|---------|
| `git_status.installed` | boolean | Git executable found in PATH |
| `git_status.repository_exists` | boolean | `.git/` directory exists in current directory |
| `git_status.initialized` | boolean | Repository is initialized (has HEAD reference) |
| `git_status.commit_count` | number | Number of commits (0 if no commits yet) |
| `git_status.current_branch` | string \| null | Current branch name or null if detached HEAD |
| `git_status.uncommitted_changes` | number | Count of modified/staged/untracked files |
| `git_status.detached_head` | boolean | True if repository in detached HEAD state |
| `assessment.status` | enum | One of: READY, UNCOMMITTED, INIT_REQUIRED, NOT_INITIALIZED, GIT_MISSING, ERROR |
| `assessment.workflow_mode` | enum | full (all Git features), partial (Git but limited), fallback (file-based) |
| `assessment.can_commit` | boolean | Safe to perform `git commit` |
| `assessment.can_push` | boolean | Can push to remote (requires commits) |
| `recommendations.primary_action` | string \| null | Next step user should take (or null if no action needed) |
| `recommendations.commands` | array | Specific bash commands to execute (in order) |
