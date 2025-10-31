# Claude Code VS Code Integration

## Overview

Claude Code offers a native Visual Studio Code extension (currently in beta) that brings AI-powered coding assistance directly into your editor. The extension provides a dedicated sidebar, plan mode, auto-accept edits, and full terminal feature parity.

## Requirements

- **Visual Studio Code**: Version 1.98.0 or higher
- **Node.js**: Version 18+ (for Claude Code CLI)
- **Anthropic API Key**: Or AWS Bedrock / Google Vertex AI access

## Installation

### From VS Code Marketplace

1. Open VS Code
2. Go to Extensions (Ctrl+Shift+X or Cmd+Shift+X)
3. Search for "Claude Code"
4. Click "Install"

### Manual Update

```
Cmd/Ctrl + Shift + P → Claude Code: Update
```

## Features

### Dedicated Sidebar Panel

Access Claude via the Spark (✨) icon in the activity bar:

- Full conversation interface
- File context with @-mentions
- Inline code suggestions
- Multiple simultaneous sessions

### Plan Mode with Editing

Enable planning before execution:

1. Ask Claude to create a plan
2. Review and edit the plan
3. Approve to execute
4. Claude implements the plan

### Auto-Accept Edits Mode

Automatically apply Claude's code changes:

- Toggle auto-accept in settings
- Claude makes changes directly
- Review changes in git diff
- Undo if needed

### File Management

Use @-mentions to reference files:

```
@src/api.ts review this file for security issues
@tests/auth.test.ts add more test cases
```

### Keyboard Shortcuts

- **Open Claude**: `Cmd/Ctrl + Shift + P` → "Claude Code: Open"
- **New Chat**: `Cmd/Ctrl + Shift + C`
- **Accept Edit**: `Cmd/Ctrl + Enter`
- **Reject Edit**: `Esc`

### Slash Commands

All terminal slash commands work in VS Code:

```
/help
/model opus
/review
/clear
```

### Multiple Sessions

Work on different tasks in separate conversations:

- Create new chat sessions
- Switch between sessions
- Preserve context per session

## Configuration

### Access Settings

```
Settings → Extensions → Claude Code
```

Or edit `settings.json`:

```
Cmd/Ctrl + Shift + P → Preferences: Open Settings (JSON)
```

### Basic Configuration

```json
{
  "claudeCode.apiKey": "${ANTHROPIC_API_KEY}",
  "claudeCode.model": "sonnet",
  "claudeCode.autoAcceptEdits": false,
  "claudeCode.maxTurns": 20
}
```

### Environment Variables

```json
{
  "claudeCode.env": {
    "NODE_ENV": "development",
    "DEBUG": "true"
  }
}
```

### Permissions

```json
{
  "claudeCode.permissions": {
    "allow": ["Read(*)", "Write(src/**/*)", "Edit(*)"],
    "deny": ["Read(.env*)", "Bash(rm -rf *)"]
  }
}
```

## Third-Party Provider Support

### Amazon Bedrock

```json
{
  "claudeCode.provider": "bedrock",
  "claudeCode.aws.region": "us-east-1",
  "claudeCode.aws.accessKeyId": "${AWS_ACCESS_KEY_ID}",
  "claudeCode.aws.secretAccessKey": "${AWS_SECRET_ACCESS_KEY}"
}
```

### Google Vertex AI

```json
{
  "claudeCode.provider": "vertex",
  "claudeCode.vertex.projectId": "${GCP_PROJECT_ID}",
  "claudeCode.vertex.region": "us-central1",
  "claudeCode.vertex.credentials": "${GOOGLE_CREDENTIALS}"
}
```

## Workflows

### Code Review Workflow

1. Open file to review
2. Open Claude sidebar
3. Type: `@filename review for quality and security`
4. Review suggestions
5. Accept or modify changes

### Feature Implementation

1. Create plan: `Create a login feature with authentication`
2. Review plan
3. Approve plan
4. Claude implements step-by-step
5. Review changes in git diff

### Bug Fixing

1. Reference error: `Fix the error at @src/api.ts:42`
2. Claude analyzes issue
3. Proposes fix
4. Accept or refine
5. Verify fix works

### Test Writing

1. Open implementation file
2. Request: `@src/auth.ts write comprehensive tests`
3. Claude generates test suite
4. Review coverage
5. Add additional test cases

## Integration with VS Code Features

### Source Control

Claude's changes appear in Source Control panel:
- Review diffs before committing
- Revert unwanted changes
- Create commits with descriptive messages

### Terminal Integration

Claude can use VS Code's integrated terminal:
- Run commands
- Execute tests
- Build projects
- Deploy code

### Debug Integration

Use Claude with VS Code debugger:
- Set breakpoints
- Analyze debug output
- Fix issues found while debugging

### Problems Panel

Claude can address issues in Problems panel:
- Fix TypeScript errors
- Resolve linting issues
- Address warnings

## Limitations (Beta)

Some features not yet available in VS Code extension:

- Full MCP server configuration (partial support)
- Complete subagents configuration
- Advanced checkpoint features
- Some advanced CLI shortcuts

Use terminal Claude Code for full feature access.

## Best Practices

### 1. Use Auto-Accept Wisely

Start with auto-accept disabled:

```json
{
  "claudeCode.autoAcceptEdits": false
}
```

Enable only when comfortable with Claude's behavior.

### 2. Leverage @-Mentions

Be specific with file references:

```
# Good
@src/components/Button.tsx add props for size variants

# Less specific
Add button sizes
```

### 3. Use Plan Mode for Complex Changes

For large refactors or new features:
1. Request a plan
2. Review and adjust
3. Execute incrementally
4. Verify each step

### 4. Review Changes in Git

Always check diffs before committing:

```
Source Control panel → Review changes
```

### 5. Use Workspace Settings for Projects

`.vscode/settings.json`:
```json
{
  "claudeCode.model": "sonnet",
  "claudeCode.permissions": {
    "allow": ["Read(*)", "Write(src/**/*)", "Edit(*)"],
    "deny": ["Read(.env*)"]
  }
}
```

Commit to share with team.

## Security Considerations

### Restricted Mode

For untrusted workspaces, VS Code's Restricted Mode applies:

- Limits file access
- Restricts command execution
- Prevents auto-run scripts

Enable Restricted Mode for unfamiliar projects.

### Auto-Edit Risks

Auto-accept mode can make unwanted changes:

- Review all edits before committing
- Use version control
- Test changes thoroughly
- Start with manual approval

### API Key Security

Never commit API keys:

```json
{
  "claudeCode.apiKey": "${ANTHROPIC_API_KEY}"  // Reference env var
}
```

Add to `.gitignore`:
```
.vscode/settings.local.json
```

## Troubleshooting

### Extension Not Loading

1. Check VS Code version (≥1.98.0)
2. Verify extension is enabled
3. Restart VS Code
4. Check extension logs (Output panel)

### API Key Issues

1. Verify key is set correctly
2. Check environment variable exists
3. Test key with terminal Claude Code
4. Regenerate key if needed

### Claude Not Responding

1. Check internet connection
2. Verify API key is valid
3. Check rate limits
4. Review Output panel for errors

### File Context Issues

1. Verify file path in @-mention
2. Check file permissions
3. Ensure file is in workspace
4. Try absolute path

### Performance Issues

1. Limit concurrent sessions
2. Clear old conversations
3. Reduce context size
4. Check system resources

## Advanced Usage

### Custom Keybindings

`keybindings.json`:
```json
[
  {
    "key": "ctrl+alt+c",
    "command": "claudeCode.newChat"
  },
  {
    "key": "ctrl+alt+r",
    "command": "claudeCode.review"
  }
]
```

### Tasks Integration

`.vscode/tasks.json`:
```json
{
  "version": "2.0.0",
  "tasks": [
    {
      "label": "Claude Review",
      "type": "shell",
      "command": "claude -p 'Review current changes'"
    }
  ]
}
```

### Snippets Integration

`.vscode/snippets.code-snippets`:
```json
{
  "Ask Claude": {
    "prefix": "claude",
    "body": [
      "@${TM_FILENAME} $0"
    ],
    "description": "Ask Claude about current file"
  }
}
```

## Comparison: VS Code vs Terminal

| Feature | VS Code Extension | Terminal CLI |
|---------|------------------|--------------|
| **Sidebar UI** | ✅ Yes | ❌ No |
| **@-mentions** | ✅ Yes | ⚠️ Limited |
| **Plan Mode** | ✅ Yes | ✅ Yes |
| **Auto-accept** | ✅ Yes | ❌ No |
| **MCP Servers** | ⚠️ Partial | ✅ Full |
| **Subagents** | ⚠️ Limited | ✅ Full |
| **Checkpoints** | ⚠️ Limited | ✅ Full |
| **Slash Commands** | ✅ Yes | ✅ Yes |
| **Hooks** | ⚠️ Limited | ✅ Full |

## Example Workflows

### Complete Feature in VS Code

1. **Plan**:
   ```
   Create a user authentication system with JWT
   ```

2. **Review Plan**: Edit and approve

3. **Implementation**: Claude creates files and code

4. **Review**: Check diffs in Source Control

5. **Test**:
   ```
   @tests/auth.test.ts review and add edge cases
   ```

6. **Commit**: Via Source Control panel

### Code Review in VS Code

1. **Open PR branch**: Checkout in VS Code

2. **Request Review**:
   ```
   /review
   Review this PR for security, performance, and quality
   ```

3. **Address Issues**: Make suggested changes

4. **Verify**: Run tests, check coverage

5. **Approve**: Ready for merge

## References

- Official Documentation: https://docs.claude.com/en/docs/claude-code/vs-code
- VS Code Marketplace: Search "Claude Code"
- Extension Settings: VS Code Settings → Claude Code
- Keyboard Shortcuts: File → Preferences → Keyboard Shortcuts
- Troubleshooting: Output panel → Claude Code
