# Git Worktree Manager - Integration Notes

**Invocation by /dev command:**

```bash
Task(
  subagent_type="git-worktree-manager",
  description="Manage worktree for STORY-091",
  prompt="Manage Git worktree for story STORY-091.
    Configuration: devforgeai/config/parallel.yaml
    Return JSON with status and actions."
)
```

**Response Handling:**

```bash
# Parse JSON response
result=$(Task subagent_type="git-worktree-manager" ...)
status=$(echo "$result" | jq -r '.status')
action=$(echo "$result" | jq -r '.story_worktree.action_needed')
idle_count=$(echo "$result" | jq -r '.idle_worktrees | length')

# Execute based on action
if [ "$action" = "CREATE" ]; then
    git worktree add "$path" -b "$branch"
elif [ "$action" = "RESUME" ]; then
    # Switch to worktree context
    cd "$path"
fi
```
