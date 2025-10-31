# Claude Code Terminal Documentation

## Overview

This directory contains comprehensive research and documentation about Claude Code Terminal, Anthropic's official CLI tool for AI-powered software development.

**Official Website**: https://www.claude.com/product/claude-code

**Official Documentation**: https://docs.claude.com/en/docs/claude-code/

## Quick Start

### Installation

```bash
npm install -g @anthropic-ai/claude-code
```

**Requirements**: Node.js 18+

### Basic Usage

```bash
# Start interactive session
claude

# Quick query
claude -p "Review auth.ts for security issues"

# Continue previous session
claude -c
```

## Documentation Index

### 1. [Plan Usage Policy](./plan-usage-policy.md)

Learn about Claude Code's pricing tiers, usage policies, and cost optimization strategies.

**Key Topics**:
- Free, Professional, and Enterprise tiers
- API usage and rate limits
- Cost optimization techniques
- Third-party provider support (AWS Bedrock, Google Vertex AI)
- Fair use guidelines
- Security considerations

**Read this to**: Understand pricing, plan your usage budget, and configure alternative providers.

---

### 2. [Slash Commands](./slash-commands.md)

Master slash commands for controlling Claude Code's behavior and creating custom workflows.

**Key Topics**:
- Built-in commands (`/help`, `/review`, `/model`, etc.)
- Creating custom commands
- Argument placeholders and file referencing
- Command namespacing
- MCP slash commands
- Best practices

**Read this to**: Create custom workflows, automate repetitive tasks, and extend Claude Code's capabilities.

---

### 3. [Sub-Agents](./sub-agents.md)

Understand how to create and use specialized AI assistants for specific tasks.

**Key Topics**:
- What are sub-agents
- Creating project and user-level agents
- Configuration and tool access
- Common sub-agent types (reviewer, debugger, test engineer)
- Invocation methods
- Best practices

**Read this to**: Delegate specialized tasks, preserve context, and build reusable AI workflows.

---

### 4. [Output Styles](./output-styles.md)

Customize Claude Code's communication style for different use cases.

**Key Topics**:
- Built-in styles (default, explanatory, learning)
- Creating custom output styles
- Use cases and examples
- Comparison with other features
- Team collaboration styles

**Read this to**: Adapt Claude's behavior for learning, teaching, debugging, or specific project needs.

---

### 5. [Hooks Guide](./hooks-guide.md)

Learn how to automate workflows with hooks that execute at specific lifecycle points.

**Key Topics**:
- Hook events (PreToolUse, PostToolUse, SessionStart, etc.)
- Creating hooks
- Common examples (auto-formatting, testing, notifications)
- Matcher patterns
- Security considerations
- Best practices

**Read this to**: Automate code formatting, run tests automatically, enforce policies, and create custom workflows.

---

### 6. [Hooks Reference](./hooks-reference.md)

Complete technical reference for all available hooks, parameters, and configurations.

**Key Topics**:
- All hook events with parameters
- Matcher pattern reference
- Environment variables
- Response formats
- Error handling
- Performance optimization
- Security best practices

**Read this to**: Get detailed technical specifications for implementing advanced hook configurations.

---

### 7. [GitHub Actions Integration](./github-actions.md)

Integrate Claude Code into GitHub workflows for automated development.

**Key Topics**:
- Quick setup and manual installation
- Basic workflow configuration
- Features (auto PR creation, @claude mentions, code review)
- Advanced workflows
- Alternative cloud providers
- Security and best practices

**Read this to**: Automate feature implementation, code reviews, and bug fixes in GitHub repositories.

---

### 8. [GitLab CI/CD Integration](./gitlab-ci-cd.md)

Use Claude Code in GitLab pipelines for continuous AI-assisted development.

**Key Topics**:
- Setup for GitLab.com and self-hosted
- Pipeline configuration
- Cloud provider configurations
- Multi-stage AI pipelines
- Permission modes
- Security considerations

**Read this to**: Implement AI-powered CI/CD pipelines in GitLab projects.

---

### 9. [Model Context Protocol (MCP)](./mcp.md)

Extend Claude Code with external tools, databases, and services via MCP.

**Key Topics**:
- What is MCP
- Popular integrations (GitHub, Sentry, Notion, Figma, PostgreSQL)
- Server types (stdio, SSE, HTTP)
- Installation and configuration
- Creating custom MCP servers
- Security considerations

**Read this to**: Connect Claude Code to issue trackers, monitoring tools, databases, design tools, and more.

---

### 10. [Settings](./settings.md)

Configure Claude Code behavior, permissions, and integrations.

**Key Topics**:
- Settings hierarchy and file locations
- Configuration options (model, permissions, environment variables)
- Hooks, subagents, and MCP configuration
- Permission patterns
- Best practices
- Security considerations

**Read this to**: Customize Claude Code for your workflow, team, and security requirements.

---

### 11. [VS Code Integration](./vs-code.md)

Use Claude Code directly in Visual Studio Code with the official extension.

**Key Topics**:
- Installation and requirements
- Features (sidebar, plan mode, auto-accept, @-mentions)
- Configuration
- Third-party providers
- Workflows and use cases
- Limitations (beta)

**Read this to**: Bring Claude Code into your VS Code editor for seamless AI-assisted development.

---

### 12. [Model Configuration](./model-config.md)

Select and configure the right Claude model for your tasks.

**Key Topics**:
- Available models (Sonnet, Opus, Haiku, extended context)
- Configuration methods
- Model selection guide
- Cost optimization
- Task-specific model configuration
- Custom model mappings

**Read this to**: Choose the right model for each task and optimize API costs.

---

### 13. [CLI Reference](./cli-reference.md)

Complete command-line interface reference for Claude Code.

**Key Topics**:
- All commands and flags
- Examples and use cases
- Environment variables
- Interactive commands
- Exit codes
- Advanced usage (piping, scripting, automation)

**Read this to**: Master the Claude Code CLI for scripting, automation, and power-user workflows.

---

### 14. [Checkpointing](./checkpointing.md)

Use Claude Code's automatic checkpointing for experimentation and recovery.

**Key Topics**:
- What is checkpointing
- How it works
- Restore options
- Common use cases
- Limitations
- Checkpointing vs Git
- Best practices

**Read this to**: Safely experiment with changes, compare approaches, and recover from mistakes.

---

## Quick Reference

### Common Commands

| Command | Description |
|---------|-------------|
| `claude` | Start interactive session |
| `claude -p "query"` | Quick query, then exit |
| `claude -c` | Continue last session |
| `claude update` | Update to latest version |
| `/help` | Show help |
| `/model <name>` | Change model |
| `/review` | Request code review |
| `/rewind` | Access checkpoints |
| `/clear` | Clear conversation |

### Essential Slash Commands

| Command | Purpose |
|---------|---------|
| `/help` | Get help |
| `/clear` | Clear history |
| `/model opus` | Switch to Opus model |
| `/review` | Code review |
| `/rewind` | Access checkpoints |
| `/status` | Show current status |
| `/agents` | Configure sub-agents |
| `/mcp` | Configure MCP servers |

### Model Selection

| Model | Use Case |
|-------|----------|
| `sonnet` | Daily development (default) |
| `opus` | Complex reasoning, architecture |
| `haiku` | Simple tasks, fast execution |
| `sonnet[1m]` | Large codebase analysis |
| `opusplan` | Planning + execution |

### Permission Modes

| Mode | Description |
|------|-------------|
| `readOnly` | Read files only |
| `acceptEdits` | Edit files (recommended) |
| `acceptAll` | Full access (use with caution) |

## Learning Path

### Beginner

1. **Start Here**: [Plan Usage Policy](./plan-usage-policy.md)
2. **Learn Basics**: [CLI Reference](./cli-reference.md)
3. **First Steps**: [Slash Commands](./slash-commands.md)
4. **Choose Model**: [Model Configuration](./model-config.md)

### Intermediate

5. **Customize Behavior**: [Output Styles](./output-styles.md)
6. **Configure Settings**: [Settings](./settings.md)
7. **Try Checkpoints**: [Checkpointing](./checkpointing.md)
8. **Use VS Code**: [VS Code Integration](./vs-code.md)

### Advanced

9. **Create Agents**: [Sub-Agents](./sub-agents.md)
10. **Automate Workflows**: [Hooks Guide](./hooks-guide.md)
11. **Integrate Tools**: [Model Context Protocol](./mcp.md)
12. **CI/CD Integration**: [GitHub Actions](./github-actions.md) or [GitLab CI/CD](./gitlab-ci-cd.md)

### Expert

13. **Deep Dive Hooks**: [Hooks Reference](./hooks-reference.md)
14. **Advanced Settings**: [Settings](./settings.md) (advanced sections)
15. **Custom MCP Servers**: [MCP](./mcp.md) (creating custom servers)
16. **Complex Workflows**: Combine all features

## Use Case Guide

### Code Review

- **Primary Docs**: [Slash Commands](./slash-commands.md), [Sub-Agents](./sub-agents.md)
- **Features**: `/review` command, code-reviewer subagent
- **Integration**: [GitHub Actions](./github-actions.md)

### Feature Development

- **Primary Docs**: [Model Configuration](./model-config.md), [Checkpointing](./checkpointing.md)
- **Features**: TDD workflow, checkpoint experimentation
- **Integration**: [VS Code](./vs-code.md) for IDE workflow

### Bug Fixing

- **Primary Docs**: [MCP](./mcp.md), [Sub-Agents](./sub-agents.md)
- **Features**: Sentry integration, debugger subagent
- **Tools**: Error monitoring, debugging workflows

### Refactoring

- **Primary Docs**: [Checkpointing](./checkpointing.md), [Hooks Guide](./hooks-guide.md)
- **Features**: Safe experimentation, auto-testing hooks
- **Safety**: Checkpoint before/after, automated tests

### Documentation

- **Primary Docs**: [Output Styles](./output-styles.md), [Sub-Agents](./sub-agents.md)
- **Features**: Documentation-first output style, doc-writer subagent
- **Automation**: Hooks for automatic doc updates

### Testing

- **Primary Docs**: [Hooks Guide](./hooks-guide.md), [Sub-Agents](./sub-agents.md)
- **Features**: Auto-test hooks, test-engineer subagent
- **Integration**: Post-edit test execution

### CI/CD Automation

- **Primary Docs**: [GitHub Actions](./github-actions.md), [GitLab CI/CD](./gitlab-ci-cd.md)
- **Features**: Automated PR creation, issue implementation
- **Security**: Permission modes, branch protection

### Large Codebase Work

- **Primary Docs**: [Model Configuration](./model-config.md), [MCP](./mcp.md)
- **Features**: `sonnet[1m]` extended context, database MCP servers
- **Integration**: Issue tracker integration

## Troubleshooting Quick Links

| Issue | See Documentation |
|-------|-------------------|
| Installation problems | [CLI Reference](./cli-reference.md) |
| API key issues | [Plan Usage Policy](./plan-usage-policy.md), [Settings](./settings.md) |
| Permission errors | [Settings](./settings.md) (permissions section) |
| Model selection | [Model Configuration](./model-config.md) |
| Hook not working | [Hooks Reference](./hooks-reference.md) (troubleshooting) |
| Subagent issues | [Sub-Agents](./sub-agents.md) (troubleshooting) |
| MCP connection errors | [MCP](./mcp.md) (troubleshooting) |
| Checkpoint restore failed | [Checkpointing](./checkpointing.md) (troubleshooting) |
| VS Code extension issues | [VS Code Integration](./vs-code.md) (troubleshooting) |
| CI/CD pipeline failures | [GitHub Actions](./github-actions.md) or [GitLab CI/CD](./gitlab-ci-cd.md) |

## External Resources

### Official Links

- **Product Page**: https://www.claude.com/product/claude-code
- **Documentation**: https://docs.claude.com/en/docs/claude-code/
- **GitHub Repository**: https://github.com/anthropics/claude-code
- **NPM Package**: https://www.npmjs.com/package/@anthropic-ai/claude-code

### Community

- **GitHub Issues**: https://github.com/anthropics/claude-code/issues
- **Discord**: (Check official documentation for link)
- **Examples**: https://github.com/anthropics/claude-code-examples

### Related Documentation

- **Anthropic API**: https://docs.anthropic.com/
- **MCP Specification**: https://modelcontextprotocol.io/
- **Claude Models**: https://www.anthropic.com/models

## Contributing to This Documentation

This research documentation was created on 2025-10-09 based on official Claude Code documentation.

To update:
1. Check official docs for changes
2. Update relevant markdown files
3. Update this index if new topics added
4. Maintain consistent formatting

## Version Information

- **Documentation Version**: 1.0
- **Last Updated**: 2025-10-09
- **Claude Code Version**: Current as of documentation date
- **Sources**: Official Claude Code documentation (https://docs.claude.com/en/docs/claude-code/)

## Need Help?

1. **Search this index** for your topic
2. **Read the relevant documentation** in detail
3. **Check troubleshooting sections** in each document
4. **Consult official documentation** for latest updates
5. **Report issues** on GitHub if you find bugs

---

**Happy Coding with Claude Code!** 🚀