# Claude Code Model Configuration

## Overview

Claude Code provides flexible model configuration, allowing you to select different Claude models based on task complexity, context requirements, and performance needs.

## Available Model Aliases

### default
- **Description**: Recommended model for most tasks
- **Current Model**: Typically latest Sonnet
- **Use Case**: General development work
- **Context**: Standard context window

### sonnet
- **Description**: Latest Sonnet model for daily coding
- **Performance**: Balanced speed and capability
- **Use Case**: Most coding tasks, refactoring, implementation
- **Context**: Standard context window

### opus
- **Description**: Most capable model for complex reasoning
- **Performance**: Slower but more thorough
- **Use Case**: Complex architecture, difficult debugging, research
- **Context**: Extended context window

### haiku
- **Description**: Fastest model for simple tasks
- **Performance**: Very fast
- **Use Case**: Quick edits, simple questions, formatting
- **Context**: Smaller context window

### sonnet[1m]
- **Description**: Sonnet with 1 million token context
- **Performance**: Same as Sonnet
- **Use Case**: Large codebases, extensive context needed
- **Context**: 1 million tokens
- **Note**: May have higher costs

### opusplan
- **Description**: Automatically switches between Opus and Sonnet
- **Behavior**:
  - **Planning Phase**: Uses Opus for strategic thinking
  - **Execution Phase**: Uses Sonnet for implementation
- **Use Case**: Complex projects requiring both planning and execution
- **Context**: Switches based on phase

## Configuration Methods

Configuration priority (highest to lowest):

1. During session: `/model` command
2. At startup: `--model` flag
3. Environment variable: `ANTHROPIC_MODEL`
4. Settings file: `model` field

### 1. During Session

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

### 2. At Startup

Start with specific model:

```bash
claude --model opus
claude --model sonnet[1m]
claude --model haiku
```

### 3. Environment Variable

Set default model via environment:

```bash
export ANTHROPIC_MODEL=opus
claude
```

Or for single session:

```bash
ANTHROPIC_MODEL=sonnet[1m] claude
```

### 4. Settings File

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

## Model Selection Guide

### When to Use Sonnet (Default)

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

### When to Use Opus

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

### When to Use Haiku

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

### When to Use Sonnet[1m]

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

### When to Use OpusPlan

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

## Checking Current Model

### Using /status Command

```bash
/status
```

Shows current model and configuration.

### Status Line

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

## Cost Optimization

### Model Costs (Relative)

- **Haiku**: Lowest cost
- **Sonnet**: Moderate cost
- **Sonnet[1m]**: Higher cost (extended context)
- **Opus**: Highest cost
- **OpusPlan**: Variable (switches between models)

### Optimization Strategies

#### 1. Use Appropriate Model for Task

```bash
# Simple task - use Haiku
claude --model haiku -p "Format all JS files"

# Complex task - use Opus
claude --model opus -p "Design distributed system architecture"

# Standard task - use Sonnet
claude --model sonnet -p "Implement login feature"
```

#### 2. Switch Models During Session

Start with Sonnet, escalate to Opus if needed:

```bash
claude
# Try with Sonnet first
"Debug this issue"

# If unsuccessful, switch to Opus
/model opus
"Debug this issue with deeper analysis"
```

#### 3. Use OpusPlan for Balanced Cost

```bash
# Opus for planning, Sonnet for execution
claude --model opusplan -p "Build complete authentication system"
```

#### 4. Limit Extended Context

Only use `[1m]` when necessary:

```bash
# Standard context sufficient
claude -p "Review auth.ts"

# Extended context needed
claude --model sonnet[1m] -p "Review entire codebase for security"
```

## Custom Model Mappings

### Environment Variable Customization

Override model aliases:

```bash
export ANTHROPIC_MODEL_SONNET="claude-sonnet-4-20250514"
export ANTHROPIC_MODEL_OPUS="claude-opus-4-20250514"
export ANTHROPIC_MODEL_HAIKU="claude-haiku-4-20250313"
```

### Settings File Customization

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

## Model-Specific Configuration

### Subagent Model Configuration

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

### Task-Specific Models

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

## Advanced Usage

### Conditional Model Selection

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

### CI/CD Model Configuration

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

### Model Performance Monitoring

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

## Troubleshooting

### Model Not Available

1. Check model name spelling
2. Verify API access to model
3. Check account plan supports model
4. Try using alias instead of full name

### Unexpected Model Behavior

1. Verify correct model is active (`/status`)
2. Check if model was switched mid-conversation
3. Review model configuration in settings
4. Restart session with explicit model flag

### Cost Issues

1. Review which models are being used
2. Switch to more cost-effective models
3. Limit use of `[1m]` extended context
4. Use OpusPlan for balanced cost
5. Monitor usage in Anthropic Console

### Extended Context Not Working

1. Verify using `[1m]` suffix
2. Check model supports extended context
3. Review API plan limits
4. Check context size in `/status`

## Best Practices

### 1. Start with Sonnet

Default to Sonnet for most tasks:

```bash
# Good default
claude --model sonnet
```

### 2. Escalate to Opus When Needed

Switch to Opus for complex tasks:

```bash
/model opus
"This is more complex than expected"
```

### 3. Use Haiku for Simple Tasks

Save costs on simple operations:

```bash
claude --model haiku -p "Fix formatting in all files"
```

### 4. Document Model Choices

For team projects, document why certain models are configured:

```markdown
# CLAUDE.md

## Model Configuration

- **Default**: Sonnet (daily development)
- **Reviews**: Opus (thorough analysis)
- **Formatting**: Haiku (fast execution)
```

### 5. Monitor and Optimize

Track usage and optimize:

- Review API usage dashboard
- Identify expensive operations
- Switch to appropriate models
- Set up usage alerts

## References

- Official Documentation: https://docs.claude.com/en/docs/claude-code/model-config
- Model Specifications: https://docs.anthropic.com/models
- Pricing: https://www.anthropic.com/pricing
- API Documentation: https://docs.anthropic.com/api
