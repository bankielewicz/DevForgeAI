# Claude Code Terminal - Configuration Guide

**Source:** Official documentation from code.claude.com (consolidated 2025-11-06)

**Purpose:** Comprehensive reference for configuring Claude Code Terminal including settings hierarchy, model selection, CLI flags, and permission management.

---

## Table of Contents

1. [Settings System](#section-1-settings-system)
2. [Model Configuration](#section-2-model-configuration)
3. [CLI Reference](#section-3-cli-reference)
4. [Permission Management](#section-4-permission-management)
5. [Quick Reference](#section-5-quick-reference)

---

## Section 1: Settings System

### Overview

Claude Code offers flexible configuration through `settings.json` files at multiple levels, allowing you to customize behavior, control permissions, configure tools, and manage integrations.

### Settings Hierarchy

Settings are applied in order of precedence (highest to lowest):

1. **Enterprise Managed Policies** (highest priority)
2. **Command Line Arguments**
3. **Local Project Settings** (`.claude/settings.local.json`)
4. **Shared Project Settings** (`.claude/settings.json`)
5. **User Settings** (`~/.claude/settings.json`) (lowest priority)

Settings merge together, with higher-priority settings overriding lower-priority ones.

### Settings File Locations

#### User-Level Settings

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

#### Project-Level Settings (Shared)

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

#### Project-Level Settings (Local)

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

#### Enterprise Managed Policies

**Location**: System-specific (OS-dependent)

**Purpose**: Organization-wide controls

**Note**: Set by system administrators

### Configuration Options

#### Model Selection

```json
{
  "model": "sonnet"
}
```

**Options**: `default`, `sonnet`, `opus`, `haiku`, `sonnet[1m]`, `opusplan`

#### Output Style

```json
{
  "outputStyle": "explanatory"
}
```

**Options**: `default`, `explanatory`, `learning`, or custom style name

#### Permissions

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

#### Environment Variables

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

#### Hooks

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

#### Subagents

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

#### MCP Servers

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

#### Telemetry

```json
{
  "telemetry": {
    "enabled": false
  }
}
```

#### Max Turns

Limit agentic iterations:

```json
{
  "maxTurns": 20
}
```

#### Working Directories

```json
{
  "workingDirectories": [
    "/path/to/project",
    "/path/to/another/project"
  ]
}
```

#### Status Line

```json
{
  "statusLine": {
    "enabled": true,
    "format": "{{model}} | {{context}} | {{time}}"
  }
}
```

### Complete Example

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

### Environment Variable Management

#### Reference System Variables

```json
{
  "env": {
    "API_KEY": "${PRODUCTION_API_KEY}",
    "HOME_DIR": "${HOME}",
    "PATH": "${PATH}:/custom/bin"
  }
}
```

#### Tool-Specific Variables

```json
{
  "env": {
    "NODE_OPTIONS": "--max-old-space-size=4096",
    "JEST_TIMEOUT": "30000",
    "PRETTIER_CONFIG": ".prettierrc.json"
  }
}
```

### Best Practices

#### 1. Use Settings Hierarchy Appropriately

- **User Settings**: Personal preferences (editor style, default model)
- **Project Shared**: Team standards (permissions, hooks)
- **Project Local**: Personal credentials (API keys)

#### 2. Never Commit Secrets

```bash
# Add to .gitignore
echo ".claude/settings.local.json" >> .gitignore
```

#### 3. Document Project Settings

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

#### 4. Use Deny Lists for Security

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

#### 5. Test Settings Changes

```bash
# Test with verbose logging
claude --verbose

# Check effective settings
claude
/status
```

#### 6. Version Control Project Settings

```bash
git add .claude/settings.json
git commit -m "Add Claude Code configuration"
```

### Troubleshooting

#### Settings Not Applied

1. Check settings file syntax (valid JSON)
2. Verify file location is correct
3. Check settings hierarchy (higher priority overrides)
4. Restart Claude Code session
5. Use `claude --verbose` to see loaded settings

#### Environment Variables Not Available

1. Verify variable is exported in shell
2. Check syntax: `${VAR_NAME}`
3. Ensure variable exists before Claude Code starts
4. Test with `echo $VAR_NAME` in terminal

#### Hooks Not Running

1. Check hooks configuration syntax
2. Verify matcher patterns
3. Test hook command independently
4. Review hook output in logs

### Advanced Configurations

#### Role-Based Settings

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

#### Environment-Specific Settings

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

---

## Section 2: Model Configuration

### Overview

Claude Code provides flexible model configuration, allowing you to select different Claude models based on task complexity, context requirements, and performance needs.

### Available Model Aliases

#### default
- **Description**: Recommended model for most tasks
- **Current Model**: Typically latest Sonnet
- **Use Case**: General development work
- **Context**: Standard context window

#### sonnet
- **Description**: Latest Sonnet model for daily coding
- **Performance**: Balanced speed and capability
- **Use Case**: Most coding tasks, refactoring, implementation
- **Context**: Standard context window

#### opus
- **Description**: Most capable model for complex reasoning
- **Performance**: Slower but more thorough
- **Use Case**: Complex architecture, difficult debugging, research
- **Context**: Extended context window

#### haiku
- **Description**: Fastest model for simple tasks
- **Performance**: Very fast
- **Use Case**: Quick edits, simple questions, formatting
- **Context**: Smaller context window

#### sonnet[1m]
- **Description**: Sonnet with 1 million token context
- **Performance**: Same as Sonnet
- **Use Case**: Large codebases, extensive context needed
- **Context**: 1 million tokens
- **Note**: May have higher costs

#### opusplan
- **Description**: Automatically switches between Opus and Sonnet
- **Behavior**:
  - **Planning Phase**: Uses Opus for strategic thinking
  - **Execution Phase**: Uses Sonnet for implementation
- **Use Case**: Complex projects requiring both planning and execution
- **Context**: Switches based on phase

### Configuration Methods

Configuration priority (highest to lowest):

1. During session: `/model` command
2. At startup: `--model` flag
3. Environment variable: `ANTHROPIC_MODEL`
4. Settings file: `model` field

#### 1. During Session

Switch models mid-conversation:

```bash
/model opus
/model sonnet
/model haiku
```

Or use model names directly:

```bash
/model claude-opus-4-20250514
/model claude-sonnet-4-20250514
```

#### 2. At Startup

Start with specific model:

```bash
claude --model opus
claude --model sonnet[1m]
claude --model haiku
```

#### 3. Environment Variable

Set default model via environment:

```bash
export ANTHROPIC_MODEL=opus
claude
```

Or for single session:

```bash
ANTHROPIC_MODEL=sonnet[1m] claude
```

#### 4. Settings File

Configure in `settings.json`:

**User settings** (`~/.claude/settings.json`):
```json
{
  "model": "sonnet"
}
```

**Project settings** (`.claude/settings.json`):
```json
{
  "model": "opus"
}
```

### Model Selection Guide

#### When to Use Sonnet (Default)

**Best for**:
- Daily development work
- Feature implementation
- Code refactoring
- Bug fixes
- Test writing
- Documentation

**Example tasks**:
```bash
"Implement user authentication"
"Refactor the database module"
"Write tests for the API endpoints"
```

#### When to Use Opus

**Best for**:
- Complex architecture decisions
- Difficult debugging
- Performance optimization
- Security analysis
- Algorithm design
- Research tasks

**Example tasks**:
```bash
"Design a scalable microservices architecture"
"Debug this complex race condition"
"Optimize this algorithm for better time complexity"
```

#### When to Use Haiku

**Best for**:
- Quick edits
- Simple questions
- Code formatting
- Basic refactoring
- Documentation updates

**Example tasks**:
```bash
"Format this file with Prettier"
"Fix the typo in the README"
"Add JSDoc comments to this function"
```

#### When to Use Sonnet[1m]

**Best for**:
- Large codebase analysis
- Extensive context requirements
- Cross-file refactoring
- Full project reviews
- Migration projects

**Example tasks**:
```bash
"Analyze the entire authentication flow across all files"
"Review security across the whole application"
"Plan a migration from JavaScript to TypeScript"
```

#### When to Use OpusPlan

**Best for**:
- Complex projects with planning phase
- Strategic initiatives
- Large feature development
- System redesigns

**Example workflow**:
```bash
# Opus plans the approach
"Design a comprehensive caching strategy"

# Sonnet implements
# (Automatically switches to Sonnet for execution)
```

### Checking Current Model

#### Using /status Command

```bash
/status
```

Shows current model and configuration.

#### Status Line

Configure status line to always show model:

`.claude/settings.json`:
```json
{
  "statusLine": {
    "enabled": true,
    "format": "{{model}} | {{context}} | {{time}}"
  }
}
```

### Cost Optimization

#### Model Costs (Relative)

- **Haiku**: Lowest cost
- **Sonnet**: Moderate cost
- **Sonnet[1m]**: Higher cost (extended context)
- **Opus**: Highest cost
- **OpusPlan**: Variable (switches between models)

#### Optimization Strategies

##### 1. Use Appropriate Model for Task

```bash
# Simple task - use Haiku
claude --model haiku -p "Format all JS files"

# Complex task - use Opus
claude --model opus -p "Design distributed system architecture"

# Standard task - use Sonnet
claude --model sonnet -p "Implement login feature"
```

##### 2. Switch Models During Session

Start with Sonnet, escalate to Opus if needed:

```bash
claude
# Try with Sonnet first
"Debug this issue"

# If unsuccessful, switch to Opus
/model opus
"Debug this issue with deeper analysis"
```

##### 3. Use OpusPlan for Balanced Cost

```bash
# Opus for planning, Sonnet for execution
claude --model opusplan -p "Build complete authentication system"
```

##### 4. Limit Extended Context

Only use `[1m]` when necessary:

```bash
# Standard context sufficient
claude -p "Review auth.ts"

# Extended context needed
claude --model sonnet[1m] -p "Review entire codebase for security"
```

### Custom Model Mappings

#### Environment Variable Customization

Override model aliases:

```bash
export ANTHROPIC_MODEL_SONNET="claude-sonnet-4-20250514"
export ANTHROPIC_MODEL_OPUS="claude-opus-4-20250514"
export ANTHROPIC_MODEL_HAIKU="claude-haiku-4-20250313"
```

#### Settings File Customization

`.claude/settings.json`:
```json
{
  "modelMappings": {
    "sonnet": "claude-sonnet-4-20250514",
    "opus": "claude-opus-4-20250514",
    "haiku": "claude-haiku-4-20250313"
  }
}
```

### Model-Specific Configuration

#### Subagent Model Configuration

Different models for different subagents:

`.claude/settings.json`:
```json
{
  "agents": {
    "code-reviewer": {
      "description": "Reviews code",
      "model": "opus",
      "prompt": "..."
    },
    "test-writer": {
      "description": "Writes tests",
      "model": "sonnet",
      "prompt": "..."
    },
    "formatter": {
      "description": "Formats code",
      "model": "haiku",
      "prompt": "..."
    }
  }
}
```

#### Task-Specific Models

Use different models for different tasks:

```bash
# Use Opus for architecture
/model opus
"Design the system architecture"

# Switch to Sonnet for implementation
/model sonnet
"Implement the designed architecture"

# Switch to Haiku for cleanup
/model haiku
"Format all files and fix linting issues"
```

### Advanced Usage

#### Conditional Model Selection

Based on project size:

```bash
#!/bin/bash
FILE_COUNT=$(find src -type f | wc -l)

if [ $FILE_COUNT -gt 100 ]; then
  MODEL="sonnet[1m]"
else
  MODEL="sonnet"
fi

claude --model $MODEL
```

#### CI/CD Model Configuration

Use appropriate models in CI/CD:

```yaml
# GitHub Actions
jobs:
  review:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          model: opus  # Thorough review
          prompt: "Review PR for security and quality"

  test:
    runs-on: ubuntu-latest
    steps:
      - uses: anthropics/claude-code-action@v1
        with:
          model: sonnet  # Standard implementation
          prompt: "Add missing tests"
```

#### Model Performance Monitoring

Track model performance:

```bash
#!/bin/bash
echo "Task: $1"
echo "Model: $2"
START_TIME=$(date +%s)

claude --model $2 -p "$1"

END_TIME=$(date +%s)
DURATION=$((END_TIME - START_TIME))
echo "Duration: ${DURATION}s" >> model-performance.log
```

### Troubleshooting

#### Model Not Available

1. Check model name spelling
2. Verify API access to model
3. Check account plan supports model
4. Try using alias instead of full name

#### Unexpected Model Behavior

1. Verify correct model is active (`/status`)
2. Check if model was switched mid-conversation
3. Review model configuration in settings
4. Restart session with explicit model flag

#### Cost Issues

1. Review which models are being used
2. Switch to more cost-effective models
3. Limit use of `[1m]` extended context
4. Use OpusPlan for balanced cost
5. Monitor usage in Anthropic Console

#### Extended Context Not Working

1. Verify using `[1m]` suffix
2. Check model supports extended context
3. Review API plan limits
4. Check context size in `/status`

### Best Practices

#### 1. Start with Sonnet

Default to Sonnet for most tasks:

```bash
# Good default
claude --model sonnet
```

#### 2. Escalate to Opus When Needed

Switch to Opus for complex tasks:

```bash
/model opus
"This is more complex than expected"
```

#### 3. Use Haiku for Simple Tasks

Save costs on simple operations:

```bash
claude --model haiku -p "Fix formatting in all files"
```

#### 4. Document Model Choices

For team projects, document why certain models are configured:

```markdown
# CLAUDE.md

## Model Configuration

- **Default**: Sonnet (daily development)
- **Reviews**: Opus (thorough analysis)
- **Formatting**: Haiku (fast execution)
```

#### 5. Monitor and Optimize

Track usage and optimize:

- Review API usage dashboard
- Identify expensive operations
- Switch to appropriate models
- Set up usage alerts

---

## Section 3: CLI Reference

### CLI Commands

| Command                            | Description                                    | Example                                                            |
| :--------------------------------- | :--------------------------------------------- | :----------------------------------------------------------------- |
| `claude`                           | Start interactive REPL                         | `claude`                                                           |
| `claude "query"`                   | Start REPL with initial prompt                 | `claude "explain this project"`                                    |
| `claude -p "query"`                | Query via SDK, then exit                       | `claude -p "explain this function"`                                |
| `cat file \| claude -p "query"`    | Process piped content                          | `cat logs.txt \| claude -p "explain"`                              |
| `claude -c`                        | Continue most recent conversation              | `claude -c`                                                        |
| `claude -c -p "query"`             | Continue via SDK                               | `claude -c -p "Check for type errors"`                             |
| `claude -r "<session-id>" "query"` | Resume session by ID                           | `claude -r "abc123" "Finish this PR"`                              |
| `claude update`                    | Update to latest version                       | `claude update`                                                    |
| `claude mcp`                       | Configure Model Context Protocol (MCP) servers | See the [Claude Code MCP documentation](/en/docs/claude-code/mcp). |

### CLI Flags

Customize Claude Code's behavior with these command-line flags:

| Flag                             | Description                                                                                                                                              | Example                                                                                            |
| :------------------------------- | :------------------------------------------------------------------------------------------------------------------------------------------------------- | :------------------------------------------------------------------------------------------------- |
| `--add-dir`                      | Add additional working directories for Claude to access (validates each path exists as a directory)                                                      | `claude --add-dir ../apps ../lib`                                                                  |
| `--agents`                       | Define custom [subagents](/en/docs/claude-code/sub-agents) dynamically via JSON (see below for format)                                                   | `claude --agents '{"reviewer":{"description":"Reviews code","prompt":"You are a code reviewer"}}'` |
| `--allowedTools`                 | A list of tools that should be allowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings)    | `"Bash(git log:*)" "Bash(git diff:*)" "Read"`                                                      |
| `--disallowedTools`              | A list of tools that should be disallowed without prompting the user for permission, in addition to [settings.json files](/en/docs/claude-code/settings) | `"Bash(git log:*)" "Bash(git diff:*)" "Edit"`                                                      |
| `--print`, `-p`                  | Print response without interactive mode (see [SDK documentation](/en/docs/claude-code/sdk) for programmatic usage details)                               | `claude -p "query"`                                                                                |
| `--append-system-prompt`         | Append to system prompt (only with `--print`)                                                                                                            | `claude --append-system-prompt "Custom instruction"`                                               |
| `--output-format`                | Specify output format for print mode (options: `text`, `json`, `stream-json`)                                                                            | `claude -p "query" --output-format json`                                                           |
| `--input-format`                 | Specify input format for print mode (options: `text`, `stream-json`)                                                                                     | `claude -p --output-format json --input-format stream-json`                                        |
| `--include-partial-messages`     | Include partial streaming events in output (requires `--print` and `--output-format=stream-json`)                                                        | `claude -p --output-format stream-json --include-partial-messages "query"`                         |
| `--verbose`                      | Enable verbose logging, shows full turn-by-turn output (helpful for debugging in both print and interactive modes)                                       | `claude --verbose`                                                                                 |
| `--max-turns`                    | Limit the number of agentic turns in non-interactive mode                                                                                                | `claude -p --max-turns 3 "query"`                                                                  |
| `--model`                        | Sets the model for the current session with an alias for the latest model (`sonnet` or `opus`) or a model's full name                                    | `claude --model claude-sonnet-4-5-20250929`                                                        |
| `--permission-mode`              | Begin in a specified [permission mode](iam#permission-modes)                                                                                             | `claude --permission-mode plan`                                                                    |
| `--permission-prompt-tool`       | Specify an MCP tool to handle permission prompts in non-interactive mode                                                                                 | `claude -p --permission-prompt-tool mcp_auth_tool "query"`                                         |
| `--resume`                       | Resume a specific session by ID, or by choosing in interactive mode                                                                                      | `claude --resume abc123 "query"`                                                                   |
| `--continue`                     | Load the most recent conversation in the current directory                                                                                               | `claude --continue`                                                                                |
| `--dangerously-skip-permissions` | Skip permission prompts (use with caution)                                                                                                               | `claude --dangerously-skip-permissions`                                                            |

**Tip:** The `--output-format json` flag is particularly useful for scripting and automation, allowing you to parse Claude's responses programmatically.

### Agents Flag Format

The `--agents` flag accepts a JSON object that defines one or more custom subagents. Each subagent requires a unique name (as the key) and a definition object with the following fields:

| Field         | Required | Description                                                                                                     |
| :------------ | :------- | :-------------------------------------------------------------------------------------------------------------- |
| `description` | Yes      | Natural language description of when the subagent should be invoked                                             |
| `prompt`      | Yes      | The system prompt that guides the subagent's behavior                                                           |
| `tools`       | No       | Array of specific tools the subagent can use (e.g., `["Read", "Edit", "Bash"]`). If omitted, inherits all tools |
| `model`       | No       | Model alias to use: `sonnet`, `opus`, or `haiku`. If omitted, uses the default subagent model                   |

Example:

```bash
claude --agents '{
  "code-reviewer": {
    "description": "Expert code reviewer. Use proactively after code changes.",
    "prompt": "You are a senior code reviewer. Focus on code quality, security, and best practices.",
    "tools": ["Read", "Grep", "Glob", "Bash"],
    "model": "sonnet"
  },
  "debugger": {
    "description": "Debugging specialist for errors and test failures.",
    "prompt": "You are an expert debugger. Analyze errors, identify root causes, and provide fixes."
  }
}'
```

For more details on creating and using subagents, see the [subagents documentation](/en/docs/claude-code/sub-agents).

For detailed information about print mode (`-p`) including output formats, streaming, verbose logging, and programmatic usage, see the [SDK documentation](/en/docs/claude-code/sdk).

---

## Section 4: Permission Management

### Permission Patterns

#### Allow Everything Except Specific

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

#### Allow Only Specific Tools

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

#### File-Specific Permissions

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

#### Command-Specific Permissions

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

### Security Considerations

#### Principle of Least Privilege

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

#### Protect Sensitive Files

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

#### Limit Dangerous Commands

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

### Permission Troubleshooting

#### Permission Errors

1. Review `permissions` configuration
2. Check both `allow` and `deny` lists
3. Test patterns match expected files
4. Check for conflicting patterns

### Permission Modes

**defaultMode** options in settings:
- `acceptEdits`: Allow edits (recommended)
- `readOnly`: Read files only
- `acceptAll`: Full access (use with caution)

**CLI flag:**
```bash
claude --permission-mode plan
claude --permission-mode readOnly
claude --permission-mode acceptAll
```

**During session:**
- Permission prompts appear for restricted operations
- Approve or deny on case-by-case basis
- Use `--dangerously-skip-permissions` to bypass (not recommended)

---

## Section 5: Quick Reference

### Common Configuration Tasks

#### Set Default Model

```bash
# Via CLI
claude --model opus

# Via environment
export ANTHROPIC_MODEL=opus

# Via settings
echo '{"model": "opus"}' > ~/.claude/settings.json
```

#### Configure Permissions

```json
{
  "permissions": {
    "allow": ["Read(*)", "Grep(*)", "Glob(*)"],
    "deny": ["Bash(rm -rf *)", "Read(.env*)"]
  }
}
```

#### Add Environment Variables

```json
{
  "env": {
    "API_KEY": "${PRODUCTION_API_KEY}",
    "NODE_ENV": "development"
  }
}
```

#### Create Subagent

```json
{
  "agents": {
    "reviewer": {
      "description": "Code reviewer",
      "prompt": "Review code for quality",
      "tools": ["Read", "Grep"],
      "model": "opus"
    }
  }
}
```

#### Add Hook

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit(*.js)",
        "hooks": [
          {
            "type": "command",
            "command": "prettier --write \"$FILE_PATH\""
          }
        ]
      }
    ]
  }
}
```

#### Configure MCP Server

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

### Model Selection Cheat Sheet

| Task Type | Recommended Model | Reason |
|-----------|------------------|--------|
| Daily coding | `sonnet` | Balanced speed/capability |
| Architecture design | `opus` | Complex reasoning |
| Quick formatting | `haiku` | Fast execution |
| Large codebase | `sonnet[1m]` | Extended context |
| Planning + implementation | `opusplan` | Auto-switches |

### Permission Pattern Examples

```json
{
  "permissions": {
    // Allow everything except dangerous operations
    "allow": ["*"],
    "deny": [
      "Bash(rm -rf *)",
      "Bash(sudo *)",
      "Read(.env*)"
    ]
  }
}
```

```json
{
  "permissions": {
    // Read-only access
    "allow": [
      "Read(*)",
      "Grep(*)",
      "Glob(*)"
    ]
  }
}
```

```json
{
  "permissions": {
    // Development environment
    "allow": [
      "Read(*)",
      "Write(src/**/*)",
      "Edit(*.ts)",
      "Bash(npm *)",
      "Bash(git status)",
      "Bash(git diff*)"
    ],
    "deny": [
      "Bash(git push*)",
      "Read(.env*)"
    ]
  }
}
```

### Common CLI Commands

```bash
# Start interactive session
claude

# Quick query
claude -p "What does this function do?"

# Continue last session
claude -c

# Resume specific session
claude -r abc123

# Use specific model
claude --model opus

# Verbose output
claude --verbose

# JSON output (for scripting)
claude -p "query" --output-format json

# Update Claude Code
claude update
```

### Troubleshooting Quick Checks

| Issue | Quick Fix |
|-------|-----------|
| Settings not applied | Restart session, check JSON syntax |
| Permission denied | Review `permissions` in settings |
| Wrong model | Check `/status`, verify `model` in settings |
| Hook not running | Check matcher pattern, test command independently |
| Environment variable missing | Verify `${VAR}` syntax, check variable exists |
| MCP server not connecting | Check command path, verify environment variables |

### File Locations Reference

| Configuration | Location | Purpose |
|--------------|----------|---------|
| User settings | `~/.claude/settings.json` | Personal preferences |
| Project settings (shared) | `.claude/settings.json` | Team configuration (commit to git) |
| Project settings (local) | `.claude/settings.local.json` | Personal project settings (don't commit) |
| Custom commands | `.claude/commands/*.md` | Project-specific slash commands |
| Output styles | `.claude/outputStyles/*.md` | Custom output styles |

### Settings Priority Order

1. **Enterprise Managed Policies** (highest)
2. **Command Line Arguments** (`--model`, `--allowedTools`, etc.)
3. **Local Project Settings** (`.claude/settings.local.json`)
4. **Shared Project Settings** (`.claude/settings.json`)
5. **User Settings** (`~/.claude/settings.json`) (lowest)

---

## External References

- **Official Documentation**: https://docs.claude.com/en/docs/claude-code/
- **Settings Guide**: https://docs.claude.com/en/docs/claude-code/settings
- **Permissions**: https://docs.claude.com/en/docs/claude-code/permissions
- **Hooks**: https://docs.claude.com/en/docs/claude-code/hooks
- **MCP**: https://docs.claude.com/en/docs/claude-code/mcp
- **Model Specifications**: https://docs.anthropic.com/models
- **API Documentation**: https://docs.anthropic.com/api
- **Pricing**: https://www.anthropic.com/pricing

---

**Configuration consolidation complete - 2025-11-06**
