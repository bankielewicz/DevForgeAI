# Claude Code Settings

## Overview

Claude Code offers flexible configuration through `settings.json` files at multiple levels, allowing you to customize behavior, control permissions, configure tools, and manage integrations.

## Settings Hierarchy

Settings are applied in order of precedence (highest to lowest):

1. **Enterprise Managed Policies** (highest priority)
2. **Command Line Arguments**
3. **Local Project Settings** (`.claude/settings.local.json`)
4. **Shared Project Settings** (`.claude/settings.json`)
5. **User Settings** (`~/.claude/settings.json`) (lowest priority)

Settings merge together, with higher-priority settings overriding lower-priority ones.

## Settings File Locations

### User-Level Settings

**Location**: `~/.claude/settings.json`

**Purpose**: Personal preferences across all projects

**Example**:
```json
{
  "model": "sonnet",
  "outputStyle": "default",
  "permissions": {
    "allow": ["Read(*)", "Grep(*)", "Glob(*)"]
  }
}
```

### Project-Level Settings (Shared)

**Location**: `.claude/settings.json`

**Purpose**: Team-wide project configuration (committed to git)

**Example**:
```json
{
  "model": "sonnet",
  "permissions": {
    "allow": ["*"],
    "deny": ["Bash(rm -rf *)"]
  },
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Project-Level Settings (Local)

**Location**: `.claude/settings.local.json`

**Purpose**: Personal project settings (not committed)

**Example**:
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_personal_token_123",
    "ANTHROPIC_API_KEY": "sk-ant-personal-key"
  }
}
```

### Enterprise Managed Policies

**Location**: System-specific (OS-dependent)

**Purpose**: Organization-wide controls

**Note**: Set by system administrators

## Configuration Options

### Model Selection

```json
{
  "model": "sonnet"
}
```

**Options**: `default`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opusplan`

### Output Style

```json
{
  "outputStyle": "explanatory"
}
```

**Options**: `default`, `explanatory`, `learning`, or custom style name

### Permissions

Control which tools Claude can use:

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Write(src/**/*)",
      "Edit(*.ts)",
      "Bash(npm *)",
      "Bash(git *)"
    ],
    "ask": [
      "Bash(git push*)",
      "Bash(npm publish*)"
    ],
    "deny": [
      "Read(.env*)",
      "Write(.env*)",
      "Bash(rm -rf *)",
      "Bash(*sudo*)"
    ],
    "additionalDirectories": [
      "../docs/"
    ],
    "defaultMode": "acceptEdits"
  }
}
```

**Permission Modes**:
- `allow`: Tools/commands Claude can use freely
- `ask`: Tools/commands that require user confirmation
- `deny`: Tools/commands that are blocked

**Additional Fields**:
- `additionalDirectories`: Extra directories Claude can access
- `defaultMode`: Default permission mode (`acceptEdits`, `readOnly`, `acceptAll`)
- `disableBypassPermissionsMode`: Disable bypass permissions (`"disable"` or omit)

**Pattern Matching**:
- `*`: Match any
- `Tool(*)`: Match any usage of tool
- `Tool(pattern)`: Match specific files/commands
- Bash rules use prefix matching

### Environment Variables

```json
{
  "env": {
    "NODE_ENV": "development",
    "DEBUG": "true",
    "ANTHROPIC_API_KEY": "${ANTHROPIC_API_KEY}",
    "DATABASE_URL": "postgresql://localhost/dev"
  }
}
```

**Note**: Use `${VAR}` to reference system environment variables

### Hooks

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.ts)",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

### Subagents

```json
{
  "agents": {
    "code-reviewer": {
      "description": "Reviews code for quality and security",
      "prompt": "You are a code review specialist...",
      "tools": ["Read", "Grep", "Glob"],
      "model": "sonnet"
    }
  }
}
```

### MCP Servers

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

### Telemetry

```json
{
  "telemetry": {
    "enabled": false
  }
}
```

### Max Turns

Limit agentic iterations:

```json
{
  "maxTurns": 20
}
```

### Working Directories

```json
{
  "workingDirectories": [
    "/path/to/project",
    "/path/to/another/project"
  ]
}
```

### Status Line

```json
{
  "statusLine": {
    "enabled": true,
    "format": "{{model}} | {{context}} | {{time}}"
  }
}
```

## Complete Example

`.claude/settings.json` (project-level, shared):
```json
{
  "model": "sonnet",
  "outputStyle": "default",
  "maxTurns": 20,

  "permissions": {
    "allow": [
      "Read(*)",
      "Write(src/**/*)",
      "Write(tests/**/*)",
      "Edit(*)",
      "Grep(*)",
      "Glob(*)",
      "Bash(npm *)",
      "Bash(git *)",
      "Bash(node *)"
    ],
    "deny": [
      "Read(.env*)",
      "Write(.env*)",
      "Edit(.env*)",
      "Bash(rm -rf *)",
      "Bash(*sudo*)",
      "Bash(*chmod 777*)"
    ]
  },

  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.{ts,tsx,js,jsx})",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$FILE_PATH\""
          }
        ]
      },
      {
        "matcher": "Edit(src/**/*)",
        "hooks": [
          {
            "type": "command",
            "command": "npm run test:related \"$FILE_PATH\""
          }
        ]
      }
    ]
  },

  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  },

  "agents": {
    "security-reviewer": {
      "description": "Security-focused code reviewer",
      "prompt": "You are a security expert. Review code for OWASP Top 10 vulnerabilities...",
      "tools": ["Read", "Grep", "Glob"],
      "model": "opus"
    }
  },

  "env": {
    "NODE_ENV": "development",
    "LOG_LEVEL": "debug"
  }
}
```

`.claude/settings.local.json` (project-level, personal):
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_myPersonalToken123",
    "ANTHROPIC_API_KEY": "sk-ant-myPersonalKey456"
  },

  "permissions": {
    "allow": [
      "Bash(docker *)"
    ]
  }
}
```

## Permission Patterns

### Allow Everything Except Specific

```json
{
  "permissions": {
    "allow": ["*"],
    "deny": [
      "Bash(rm *)",
      "Bash(sudo *)",
      "Read(.env*)"
    ]
  }
}
```

### Allow Only Specific Tools

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Grep(*)",
      "Glob(*)"
    ]
    // Deny not needed - default denies all
  }
}
```

### File-Specific Permissions

```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(src/**/*.ts)",      // Only TypeScript in src/
      "Write(tests/**/*.test.ts)" // Only test files
    ],
    "deny": [
      "Edit(src/**/*.test.ts)",  // Don't edit test files in src/
      "Write(**/config.json)"     // Don't write config files
    ]
  }
}
```

### Command-Specific Permissions

```json
{
  "permissions": {
    "allow": [
      "Bash(npm test*)",
      "Bash(npm run*)",
      "Bash(git status)",
      "Bash(git diff*)",
      "Bash(git log*)"
    ],
    "deny": [
      "Bash(git push*)",         // Prevent accidental pushes
      "Bash(npm publish*)"        // Prevent publishing
    ]
  }
}
```

## Environment Variable Management

### Reference System Variables

```json
{
  "env": {
    "API_KEY": "${PRODUCTION_API_KEY}",
    "HOME_DIR": "${HOME}",
    "PATH": "${PATH}:/custom/bin"
  }
}
```

### Tool-Specific Variables

```json
{
  "env": {
    "NODE_OPTIONS": "--max-old-space-size=4096",
    "JEST_TIMEOUT": "30000",
    "PRETTIER_CONFIG": ".prettierrc.json"
  }
}
```

## Best Practices

### 1. Use Settings Hierarchy Appropriately

- **User Settings**: Personal preferences (editor style, default model)
- **Project Shared**: Team standards (permissions, hooks)
- **Project Local**: Personal credentials (API keys)

### 2. Never Commit Secrets

```bash
# Add to .gitignore
echo ".claude/settings.local.json" >> .gitignore
```

### 3. Document Project Settings

Create `.claude/README.md`:

```markdown
# Claude Code Configuration

## Required Environment Variables

Set these in `.claude/settings.local.json`:

- `GITHUB_TOKEN`: GitHub personal access token
- `ANTHROPIC_API_KEY`: Anthropic API key

## Configured MCP Servers

- **github**: Issue and PR management
- **sentry**: Error monitoring

## Project Hooks

- Auto-format on edit (Prettier)
- Run related tests on save
```

### 4. Use Deny Lists for Security

```json
{
  "permissions": {
    "allow": ["*"],
    "deny": [
      "Read(.env*)",
      "Read(secrets/*)",
      "Bash(rm -rf *)",
      "Bash(*sudo*)",
      "Bash(curl * | bash)"
    ]
  }
}
```

### 5. Test Settings Changes

```bash
# Test with verbose logging
claude --verbose

# Check effective settings
claude
/status
```

### 6. Version Control Project Settings

```bash
git add .claude/settings.json
git commit -m "Add Claude Code configuration"
```

## Security Considerations

### Principle of Least Privilege

Grant minimal necessary permissions:

```json
{
  "permissions": {
    "allow": [
      "Read(src/**/*)",
      "Read(tests/**/*)",
      "Grep(*)",
      "Glob(*)"
    ]
    // Only reading - safest default
  }
}
```

### Protect Sensitive Files

```json
{
  "permissions": {
    "deny": [
      "Read(.env*)",
      "Read(**/secrets/*)",
      "Read(*.key)",
      "Read(*.pem)",
      "Read(credentials.json)"
    ]
  }
}
```

### Limit Dangerous Commands

```json
{
  "permissions": {
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Bash(chmod 777 *)",
      "Bash(curl * | bash)",
      "Bash(wget * && bash *)"
    ]
  }
}
```

## Troubleshooting

### Settings Not Applied

1. Check settings file syntax (valid JSON)
2. Verify file location is correct
3. Check settings hierarchy (higher priority overrides)
4. Restart Claude Code session
5. Use `claude --verbose` to see loaded settings

### Permission Errors

1. Review `permissions` configuration
2. Check both `allow` and `deny` lists
3. Test patterns match expected files
4. Check for conflicting patterns

### Environment Variables Not Available

1. Verify variable is exported in shell
2. Check syntax: `${VAR_NAME}`
3. Ensure variable exists before Claude Code starts
4. Test with `echo $VAR_NAME` in terminal

### Hooks Not Running

1. Check hooks configuration syntax
2. Verify matcher patterns
3. Test hook command independently
4. Review hook output in logs

## Advanced Configurations

### Role-Based Settings

**Junior Developer**:
```json
{
  "permissions": {
    "allow": [
      "Read(*)",
      "Edit(src/**/*.ts)",
      "Bash(npm test*)"
    ]
  }
}
```

**Senior Developer**:
```json
{
  "permissions": {
    "allow": ["*"],
    "deny": [
      "Bash(git push origin main)",
      "Bash(npm publish)"
    ]
  }
}
```

### Environment-Specific Settings

**Development**:
```json
{
  "env": {
    "NODE_ENV": "development",
    "API_URL": "http://localhost:3000",
    "DEBUG": "true"
  }
}
```

**Production**:
```json
{
  "env": {
    "NODE_ENV": "production",
    "API_URL": "https://api.production.com"
  },
  "permissions": {
    "deny": ["Bash(*deploy*)"]  // Extra caution
  }
}
```

## References

- Official Documentation: https://docs.claude.com/en/docs/claude-code/settings
- Permissions Guide: https://docs.claude.com/en/docs/claude-code/permissions
- Hooks Reference: https://docs.claude.com/en/docs/claude-code/hooks
- MCP Configuration: https://docs.claude.com/en/docs/claude-code/mcp
