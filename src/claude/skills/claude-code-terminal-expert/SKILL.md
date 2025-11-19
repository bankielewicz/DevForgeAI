---
name: claude-code-terminal-expert
description: Comprehensive expert knowledge of Claude Code Terminal features, configuration, and capabilities. Use when users ask about Claude Code functionality ("Can Claude Code...?", "Does Claude Code have...?"), creating subagents/skills/commands/plugins, configuring settings/models/permissions, installing MCP servers, setting up hooks/automation, CI/CD integration, troubleshooting issues, or any Claude Code Terminal questions. Provides authoritative guidance on all terminal features.
model: claude-sonnet-4-5-20250929
---

# Claude Code Terminal Expert

**Purpose:** Provide comprehensive, authoritative knowledge about Claude Code Terminal's complete feature set, enabling users to leverage all available capabilities effectively.

---

## ⚠️ EXECUTION MODEL: This Skill Expands Inline

**After invocation, YOU (Claude) execute these instructions phase by phase.**

**When you invoke this skill:**
1. This SKILL.md content is now in your conversation
2. You execute each phase sequentially
3. You display results as you work through phases
4. You complete with success/failure report

**Do NOT:**
- ❌ Wait passively for skill to "return results"
- ❌ Assume skill is executing elsewhere
- ❌ Stop workflow after invocation

**Proceed to "When to Use This Skill" section below and begin execution.**

---

## When to Use This Skill

Invoke this skill when users ask about:

**Feature Discovery:**
- "Can Claude Code do...?" / "Does Claude Code have...?"
- "How do I use [feature] in Claude Code?"
- "What features are available in Claude Code Terminal?"

**Component Creation:**
- Creating custom subagents, skills, or slash commands
- Developing plugins or marketplaces
- Setting up hooks for automation

**Configuration:**
- Configuring settings, models, or permissions
- Installing and managing MCP servers
- Setting up CI/CD integrations
- Network and proxy configuration

**Troubleshooting:**
- Installation issues (WSL, npm, authentication)
- Performance problems or errors
- Feature not working as expected

**Integration:**
- GitHub Actions or GitLab CI/CD setup
- Headless mode automation
- DevContainer configuration
- Hook-based workflows

---

## Core Claude Code Terminal Features

### 1. Subagents (Specialized AI Workers)

**What they are:** Pre-configured AI personalities with isolated context windows for specialized tasks

**Key capabilities:**
- Operate in separate contexts (preserve main conversation)
- Custom system prompts and tool access
- Automatic or explicit invocation
- Project-level (`.claude/agents/`) or user-level (`~/.claude/agents/`)

**When to use:** Complex tasks requiring domain expertise (code review, debugging, security audits)

**Quick start:** `/agents` command → Create New Agent → Define purpose and tools

**Details:** See `references/core-features.md` (Section 1)

---

### 2. Skills (Model-Invoked Capabilities)

**What they are:** Modular capabilities that Claude automatically uses based on context

**Key capabilities:**
- YAML frontmatter + Markdown instructions
- Progressive disclosure (3 levels: metadata → instructions → resources)
- Model-invoked (Claude decides when to use)
- Cannot accept command parameters (context-based only)

**When to use:** Reusable workflows, domain expertise, team-shared utilities

**Quick start:** Create `.claude/skills/my-skill/SKILL.md` with frontmatter

**Details:** See `references/core-features.md` (Section 2)

---

### 3. Slash Commands (User-Invoked Workflows)

**What they are:** Markdown files containing instructions for Claude to follow

**Key capabilities:**
- User-invoked (explicit `/command` syntax)
- Support arguments via `$ARGUMENTS`, `$1`, `$2`
- YAML frontmatter for model, tools, hints
- Character budget: 15,000 chars limit

**When to use:** Frequently-used prompts, project-specific workflows

**Quick start:** Create `.claude/commands/my-command.md`

**Built-in commands:** `/help`, `/clear`, `/model`, `/agents`, `/mcp`, `/config`, 30+ total

**Details:** See `references/core-features.md` (Section 3)

---

### 4. Plugins (Bundled Extensions)

**What they are:** Packages containing commands, agents, skills, hooks, and MCP servers

**Key capabilities:**
- Marketplace-based distribution
- Team-wide installation via settings.json
- Components auto-discovered by Claude Code
- Version management and updates

**When to use:** Sharing utilities across projects, team collaboration

**Quick start:** `/plugin` command → Install from marketplace

**Details:** See `references/core-features.md` (Section 4)

---

### 5. MCP Servers (External Tool Integration)

**What they are:** Model Context Protocol servers connecting Claude to external services

**Key capabilities:**
- 40+ available servers (GitHub, Jira, Figma, Stripe, etc.)
- HTTP, SSE, or stdio transports
- OAuth authentication support
- Project, user, or local scope

**When to use:** Accessing external APIs, databases, or services

**Quick start:** `claude mcp add --transport http <name> <url>`

**Details:** See `references/core-features.md` (Section 5)

---

### 6. Hooks (Event-Driven Automation)

**What they are:** Shell commands executed at specific lifecycle events

**Key capabilities:**
- 9 event types (PreToolUse, PostToolUse, Stop, SessionStart, etc.)
- Command-based or LLM prompt-based evaluation
- Can block operations (exit code 2)
- Matcher patterns for selective triggering

**When to use:** Auto-formatting, logging, notifications, security checks

**Quick start:** `/hooks` command → Configure event and matcher

**Details:** See `references/integration-patterns.md` (Section 3)

---

### 7. Configuration System

**What it is:** Multi-level settings hierarchy (enterprise → CLI → local → project → user)

**Key capabilities:**
- settings.json files at multiple scopes
- Permission management (allow/ask/deny)
- Model selection and aliases
- Environment variable configuration

**When to use:** Customizing Claude Code behavior, team standards

**Quick start:** `/config` command or edit `~/.claude/settings.json`

**Details:** See `references/configuration-guide.md`

---

### 8. CI/CD Integration

**What it is:** Automated Claude Code execution in GitHub Actions and GitLab CI/CD

**Key capabilities:**
- GitHub Actions: `@claude` mentions in PRs/issues
- GitLab CI/CD: Automated MR creation and reviews
- AWS Bedrock and Google Vertex support
- Headless mode for automation

**When to use:** Code review automation, PR generation, scheduled tasks

**Quick start:** `/install-github-app` or add workflow YAML

**Details:** See `references/integration-patterns.md`

---

## Progressive Disclosure Strategy

**Load reference files as needed:**

1. **Core Features** - When asked about subagents, skills, commands, plugins, or MCP
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/core-features.md")
   ```

2. **Configuration** - When asked about settings, models, CLI options, permissions
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/configuration-guide.md")
   ```

3. **Integration** - When asked about CI/CD, hooks, automation, headless mode
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/integration-patterns.md")
   ```

4. **Troubleshooting** - When asked about errors, installation issues, performance
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/troubleshooting-guide.md")
   ```

5. **Advanced** - When asked about sandboxing, networking, monitoring, security
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/advanced-features.md")
   ```

6. **Best Practices** - When asked about workflows, efficiency, prompt engineering
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/best-practices.md")
   ```

**Quick References:**
```
Read(file_path=".claude/skills/claude-code-terminal-expert/assets/quick-reference.md")
Read(file_path=".claude/skills/claude-code-terminal-expert/assets/comparison-matrix.md")
```

---

## Self-Updating Mechanism

**When documentation may be outdated:**
- User reports feature not documented
- User asks about new features
- Documentation seems inconsistent with behavior

**Update procedure:**

1. **Fetch latest docs from official sources:**
   ```
   WebFetch(url="https://code.claude.com/docs/en/[topic]", prompt="Extract complete documentation...")
   ```

2. **Compare with current reference file:**
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/[relevant-file].md")
   # Compare content, identify gaps
   ```

3. **Update reference file with new content:**
   ```
   Edit(file_path=".claude/skills/claude-code-terminal-expert/references/[relevant-file].md",
        old_string="[outdated section]",
        new_string="[updated content from web]")
   ```

4. **Verify update:**
   ```
   Read(file_path=".claude/skills/claude-code-terminal-expert/references/[relevant-file].md")
   # Confirm changes applied correctly
   ```

5. **Notify user:**
   ```
   "✅ Updated [section] in [file] with latest documentation from code.claude.com"
   ```

**Documentation URLs by topic:**
- Subagents: https://code.claude.com/docs/en/sub-agents
- Skills: https://code.claude.com/docs/en/skills
- Slash Commands: https://code.claude.com/docs/en/slash-commands
- Plugins: https://code.claude.com/docs/en/plugins
- Plugin Reference: https://code.claude.com/docs/en/plugins-reference
- Plugin Marketplaces: https://code.claude.com/docs/en/plugin-marketplaces
- MCP: https://code.claude.com/docs/en/mcp
- Settings: https://code.claude.com/docs/en/settings
- Model Config: https://code.claude.com/docs/en/model-config
- CLI Reference: https://code.claude.com/docs/en/cli-reference
- Hooks Guide: https://code.claude.com/docs/en/hooks-guide
- Hooks Reference: https://code.claude.com/docs/en/hooks
- GitHub Actions: https://code.claude.com/docs/en/github-actions
- GitLab CI/CD: https://code.claude.com/docs/en/gitlab-ci-cd
- Headless Mode: https://code.claude.com/docs/en/headless
- Checkpointing: https://code.claude.com/docs/en/checkpointing
- Output Styles: https://code.claude.com/docs/en/output-styles
- Sandboxing: https://code.claude.com/docs/en/sandboxing
- Security: https://code.claude.com/docs/en/security
- Network Config: https://code.claude.com/docs/en/network-config
- Data Usage: https://code.claude.com/docs/en/data-usage
- Monitoring: https://code.claude.com/docs/en/monitoring-usage
- Costs: https://code.claude.com/docs/en/costs
- DevContainer: https://code.claude.com/docs/en/devcontainer
- Statusline: https://code.claude.com/docs/en/statusline
- Memory: https://code.claude.com/docs/en/memory
- Interactive Mode: https://code.claude.com/docs/en/interactive-mode
- Terminal Config: https://code.claude.com/docs/en/terminal-config
- Troubleshooting: https://code.claude.com/docs/en/troubleshooting

---

## Quick Reference

**Common Questions:**
- "How do I create a subagent?" → Section 1 + core-features.md
- "What's the difference between skills and commands?" → comparison-matrix.md
- "How do I set up GitHub Actions?" → integration-patterns.md
- "Claude Code isn't responding, what do I do?" → troubleshooting-guide.md
- "How do I configure permissions?" → configuration-guide.md
- "What MCP servers are available?" → core-features.md (Section 5)

**Keyboard Shortcuts:**
- `Ctrl+C` - Cancel generation
- `Esc Esc` - Rewind conversation/code
- `Tab` - Toggle extended thinking
- `Shift+Tab` - Switch permission modes
- See `assets/quick-reference.md` for complete list

**Built-in Commands:**
- `/help` - List all commands
- `/agents` - Manage subagents
- `/mcp` - Manage MCP servers
- `/config` - Open settings
- See `assets/quick-reference.md` for complete list

---

## Usage Pattern

**Step 1: Identify user's question category**
- Core features → Load core-features.md
- Configuration → Load configuration-guide.md
- Integration/automation → Load integration-patterns.md
- Problems/errors → Load troubleshooting-guide.md
- Advanced topics → Load advanced-features.md
- Best practices → Load best-practices.md

**Step 2: Load appropriate reference file(s)**
- Use Read tool to load specific section
- Provide comprehensive, accurate answer from documentation
- Include code examples from reference files

**Step 3: Suggest related topics**
- Point to other relevant sections
- Recommend next steps or related features

---

## Maintenance Protocol

**Quarterly Review (Every 3 months):**
1. Check code.claude.com for new features or documentation updates
2. Update reference files with latest content
3. Add new features to appropriate sections
4. Update version history in this file

**User-Reported Gaps:**
1. User mentions feature not documented
2. Fetch latest docs from relevant URL
3. Update appropriate reference file
4. Confirm update with user

**Version History:**
- v1.0 (2025-11-06): Initial creation, migrated 15,788 lines from .ai_docs/Terminal/
- [Future versions track updates]

---

## Token Efficiency

**This skill:**
- SKILL.md: ~2,000 tokens (lightweight discovery)
- Reference files: Load only as needed (3,500-2,800 tokens each)
- Progressive disclosure: Prevents context overflow

**Best practices:**
- Load single reference file per query when possible
- Use quick-reference.md for simple lookups
- Load multiple references only for cross-cutting questions

---

## Integration with DevForgeAI Framework

**This skill complements DevForgeAI by:**
- Providing Claude Code Terminal expertise
- Enabling self-service feature discovery
- Reducing "Claude doesn't know this feature" friction
- Supporting framework automation with terminal knowledge

**Not a replacement for:**
- DevForgeAI workflow skills (ideation, development, qa, release)
- Framework-specific guidance (see CLAUDE.md)
- Project architecture decisions

---

## Quick Start Examples

**Example 1: Creating a subagent**
```
User: "How do I create a code reviewer subagent?"
Action: Load references/core-features.md (Section 1)
Response: [Detailed steps with YAML frontmatter example]
```

**Example 2: Setting up GitHub Actions**
```
User: "I want Claude Code to review my PRs automatically"
Action: Load references/integration-patterns.md (Section 1)
Response: [Complete GitHub Actions setup with workflow YAML]
```

**Example 3: Troubleshooting**
```
User: "Claude Code keeps asking for permissions, how do I fix this?"
Action: Load references/configuration-guide.md (Permissions section)
Response: [Permission configuration guidance with settings.json examples]
```

**Example 4: Feature comparison**
```
User: "What's the difference between skills and slash commands?"
Action: Load assets/comparison-matrix.md
Response: [Comparison table with use cases]
```

---

## Remember

**Authoritative Source:** All guidance comes from official code.claude.com documentation
**Always Current:** Self-updating mechanism ensures accuracy
**Progressive Disclosure:** Load only necessary reference files
**Complete Coverage:** 8 core features + configuration + integration + troubleshooting
**DevForgeAI Integration:** Complements framework with terminal expertise
