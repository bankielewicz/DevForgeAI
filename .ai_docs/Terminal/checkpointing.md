# Claude Code Checkpointing

## Overview

Checkpointing is an automatic tracking and recovery mechanism in Claude Code that allows you to undo changes and revert to previous code states during a session. It provides a "local undo" system for experimentation and mistake recovery.

## What is Checkpointing?

Checkpointing automatically captures your code state before each edit and creates recovery points throughout your Claude Code session. Think of it as a lightweight, session-level version control system.

### Key Features

- **Automatic Capture**: Code state saved before each edit
- **Conversation Checkpoints**: New checkpoint with every user prompt
- **Persistent Storage**: Checkpoints saved across sessions
- **Selective Restore**: Choose to restore code, conversation, or both
- **Automatic Cleanup**: Checkpoints deleted after 30 days

## How It Works

### Checkpoint Creation

Claude Code automatically creates checkpoints:

1. **Before Each Edit**: Before any file modification
2. **On User Prompt**: When you submit a new message
3. **At Session Milestones**: Key points in conversation

### Checkpoint Storage

- **Location**: `.claude/checkpoints/`
- **Format**: Git-like snapshots
- **Retention**: 30 days
- **Scope**: Per-session

## Using Checkpointing

### Access Rewind Menu

Press `Esc` twice or use `/rewind` command:

```bash
# In interactive session
/rewind
```

Or press `Esc` `Esc`

### Restore Options

When you access the rewind menu, you can choose:

1. **Restore Conversation Only**
   - Revert to previous conversation state
   - Keep current code changes
   - Use when: You want to retry a conversation but keep code

2. **Restore Code Only**
   - Revert code to previous state
   - Keep current conversation
   - Use when: You want to undo code changes but keep discussion

3. **Restore Both Code and Conversation**
   - Complete revert to checkpoint
   - Both code and conversation reset
   - Use when: You want to completely undo recent work

### Rewind Workflow

```bash
# Interactive session
claude

> Refactor the authentication module

# Claude makes changes you don't like

# Access rewind
/rewind

# Select checkpoint from menu
> [2 minutes ago] Before "Refactor the authentication module"

# Choose restore option
> Restore both code and conversation

# Now you're back to previous state
> Let's try a different approach to refactoring...
```

## Common Use Cases

### Exploring Alternative Approaches

```bash
# Approach 1
> Implement feature using microservices

# Review results
> Show me the implementation

# Not satisfied, rewind
/rewind
> Restore both

# Approach 2
> Implement feature using monolithic architecture

# Compare and choose best approach
```

### Recovering from Mistakes

```bash
# Make an error
> Delete all test files

# Oh no! Rewind immediately
/rewind
> Restore code only

# Tests are back, conversation continues
> I meant delete only the deprecated tests
```

### Experimenting with Features

```bash
# Try experimental change
> Add caching layer with Redis

# Test it
> Run the tests

# Doesn't work well, revert
/rewind
> Restore code only

# Try different approach
> Add caching layer with in-memory cache
```

### Comparing Implementations

```bash
# Implementation A
> Implement sorting algorithm using quicksort
# Save the code manually (copy or commit)

# Rewind
/rewind

# Implementation B
> Implement sorting algorithm using mergesort
# Compare with saved Implementation A
```

## Limitations

### What Checkpoints Track

✅ **Tracked**:
- File edits via Edit tool
- File creation via Write tool
- Conversation history
- User prompts

❌ **Not Tracked**:
- Bash command changes
- External file modifications
- Changes from other sessions
- Manual file edits outside Claude
- Git operations

### Important Notes

1. **Not a Git Replacement**: Checkpoints are for session-level recovery only
2. **Local Only**: Checkpoints don't sync across machines
3. **Automatic Cleanup**: Deleted after 30 days
4. **No Branching**: Linear history only
5. **Concurrent Sessions**: Each session has independent checkpoints

## Best Practices

### 1. Commit Important Work

Use Git for permanent version control:

```bash
# After achieving good state
> Create a git commit with these changes

# Then continue experimenting
> Now let's try an alternative approach

# Can rewind without losing committed work
/rewind
```

### 2. Create Explicit Checkpoints

Use conversation boundaries:

```bash
# Mark important states with messages
> "Checkpoint: Authentication working"

# Later, easy to identify in rewind menu
/rewind
> [10 minutes ago] "Checkpoint: Authentication working"
```

### 3. Test Before Committing

Use checkpoints to test risky changes:

```bash
# Try risky refactor
> Refactor entire database layer

# Test thoroughly
> Run all tests and check for issues

# If successful, commit
> Create git commit

# If failed, rewind
/rewind
```

### 4. Document Experiments

Keep track of what you're trying:

```bash
> Experiment 1: Trying Redis for caching

# Try it, test it

> Experiment 2: Trying in-memory cache instead

# Use conversation as experiment log
# Easy to find checkpoints for each experiment
```

### 5. Regular Git Commits

Don't rely solely on checkpoints:

```bash
# Every major milestone
> The authentication is complete and tested
> Create a git commit

# Continue with checkpoints for exploration
```

## Advanced Usage

### Checkpoint Inspection

View checkpoint details:

```bash
# List checkpoints
ls .claude/checkpoints/

# Inspect specific checkpoint
cat .claude/checkpoints/checkpoint-123456.json
```

### Manual Checkpoint Management

While automatic, you can manage manually:

```bash
# Clean old checkpoints
find .claude/checkpoints/ -mtime +30 -delete

# Backup important checkpoint
cp .claude/checkpoints/checkpoint-123456.json ./backup/
```

### Checkpoint in Scripts

For automated workflows:

```bash
#!/bin/bash

# Backup before risky operation
CHECKPOINT_DIR=".claude/checkpoints/backup-$(date +%s)"
cp -r .claude/checkpoints/ "$CHECKPOINT_DIR"

# Run risky operation
claude -p "Major refactoring"

# Verify
if npm test; then
  echo "Success! Removing backup"
  rm -rf "$CHECKPOINT_DIR"
else
  echo "Failed! Restoring from backup"
  cp -r "$CHECKPOINT_DIR/"* .claude/checkpoints/
fi
```

## Checkpointing vs Git

| Feature | Checkpointing | Git |
|---------|---------------|-----|
| **Purpose** | Session recovery | Version control |
| **Scope** | Single session | Entire project history |
| **Automatic** | Yes | No (manual commits) |
| **Branching** | No | Yes |
| **Sharing** | No | Yes |
| **Retention** | 30 days | Permanent |
| **Granularity** | Every edit | Manual commits |
| **Use Case** | Experimentation | Long-term history |

### Use Both

Combine for best results:

```bash
# Git for milestones
git commit -m "Feature X complete"

# Checkpoints for exploration
> Try different implementation approaches

# Rewind as needed
/rewind

# Commit final result
git commit -m "Implemented feature X"
```

## Troubleshooting

### Checkpoint Not Available

1. Check if within 30 days
2. Verify `.claude/checkpoints/` exists
3. Check disk space
4. Ensure session had edits
5. Restart Claude Code if needed

### Cannot Restore

1. Verify checkpoint still exists
2. Check file permissions
3. Ensure no external locks on files
4. Close other editors
5. Try different restore option

### Performance Issues

1. Clean old checkpoints
2. Reduce checkpoint frequency (if configurable)
3. Check disk I/O
4. Archive large checkpoint directories

### Conflicts with Git

1. Commit or stash Git changes first
2. Restore from checkpoint
3. Resolve any conflicts
4. Continue work

## Configuration

### Disable Checkpointing

In `settings.json`:

```json
{
  "checkpointing": {
    "enabled": false
  }
}
```

### Adjust Retention

```json
{
  "checkpointing": {
    "retentionDays": 7
  }
}
```

### Checkpoint Location

```json
{
  "checkpointing": {
    "path": "/custom/path/checkpoints"
  }
}
```

## Integration with Other Features

### With Hooks

Hooks run even when rewinding:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*)",
        "hooks": [{
          "type": "command",
          "command": "echo 'Checkpoint created' >> checkpoint-log.txt"
        }]
      }
    ]
  }
}
```

### With Subagents

Each subagent's changes are checkpointed:

```bash
# Subagent makes changes
@code-reviewer refactor authentication

# Can rewind subagent's changes
/rewind
```

### With MCP Servers

Changes via MCP tools are checkpointed:

```bash
# MCP server modifies files
"Use GitHub MCP to update README"

# Can rewind
/rewind
```

## Security Considerations

### Sensitive Data in Checkpoints

Checkpoints capture file content:

- Avoid committing sensitive data
- Clean checkpoints before sharing
- Don't backup to cloud without encryption

### Checkpoint Cleanup

```bash
# Before sharing project
rm -rf .claude/checkpoints/

# Or add to .gitignore
echo ".claude/checkpoints/" >> .gitignore
```

## Quick Reference

| Action | Command/Shortcut |
|--------|------------------|
| Open rewind menu | `Esc` `Esc` or `/rewind` |
| List checkpoints | `ls .claude/checkpoints/` |
| Clean old checkpoints | `find .claude/checkpoints/ -mtime +30 -delete` |
| Disable checkpointing | Set `checkpointing.enabled: false` |
| Change retention | Set `checkpointing.retentionDays` |

## Example Workflows

### Feature Development

```bash
# Start feature
> Implement user login

# Checkpoint automatically created

# Test it
> Run tests

# Not working, rewind
/rewind
> Restore code only

# Try again
> Implement user login with different approach

# Success! Commit
> Create git commit
```

### Bug Fixing

```bash
# Attempt fix
> Fix the authentication bug

# Test
> Run tests

# Made it worse, rewind
/rewind
> Restore both

# Analyze more carefully
> Explain the authentication bug first

# Then fix with better understanding
```

### Refactoring

```bash
# Safe starting point
git commit -m "Before refactoring"

# Try refactor
> Refactor database module

# Review changes
> Show me what changed

# Not good, rewind
/rewind

# Try different approach
> Refactor database module with different strategy

# Good! Commit
git commit -m "Refactored database module"
```

## References

- Official Documentation: https://docs.claude.com/en/docs/claude-code/checkpointing
- Git Integration: https://docs.claude.com/en/docs/claude-code/git
- Session Management: https://docs.claude.com/en/docs/claude-code/sessions
