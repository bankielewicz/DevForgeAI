---
name: claude-code-terminal-expert
description: |
  Expert knowledge base for Claude Code Terminal — the CLI tool itself, not coding tasks.
  MUST use this skill whenever the user asks about Claude Code features, configuration,
  setup, or troubleshooting. This includes: keyboard shortcuts not working (Option key,
  Alt+P, Shift+Enter, Ctrl+B), creating or configuring subagents/skills/commands/plugins,
  setting up hooks (PreToolUse, PostToolUse, HTTP hooks), installing or debugging MCP
  servers, GitHub Actions or GitLab CI/CD integration for PR reviews, switching models
  mid-conversation, undoing or rewinding Claude's changes, proxy/network configuration,
  permission modes, memory and CLAUDE.md setup, the /batch /simplify /debug bundled skills,
  git worktrees, agent teams, remote control, headless mode, or ANY question where the user
  is asking about how Claude Code works rather than asking Claude Code to do coding work.
  When in doubt about whether a question is about Claude Code itself vs. a coding task,
  prefer triggering this skill — it will not interfere with coding-focused responses.
license: MIT
compatibility: "Claude Code v2.1.x (tested on v2.1.69)"
metadata:
  author: DevForgeAI
  version: "4.0.0"
  category: knowledge-infrastructure
  last-updated: "2026-03-05"
  agent-skills-spec-version: "1.0"
  topics:
    - subagents
    - skills
    - slash-commands
    - plugins
    - mcp-servers
    - hooks
    - configuration
    - ci-cd
    - agent-skills-specification
    - task-management
    - keybindings
    - agent-teams
    - remote-control
    - worktrees
    - auto-memory
    - bundled-skills
    - fast-mode
allowed-tools:
  - Read
  - Grep
  - Glob
  - WebFetch
  - WebSearch
---

# Claude Code Terminal Expert

Provide comprehensive, authoritative knowledge about Claude Code Terminal's complete feature set, enabling users to leverage all available capabilities effectively.

---

## When to Use This Skill

**Feature Discovery:** "Can Claude Code do...?", "How do I use [feature]?", "What features are available?"

**Component Creation:** Creating subagents, skills, slash commands, plugins, hooks

**Configuration:** Settings, models, permissions, MCP servers, CI/CD, network/proxy

**Troubleshooting:** Installation issues, errors, performance problems

**Integration:** GitHub Actions, GitLab CI/CD, headless mode, DevContainers, hooks

---

## Core Features Overview

### 1. Subagents

Specialized AI workers with isolated context windows for domain-specific tasks.

- Custom system prompts and tool restrictions
- Project-level (`.claude/agents/`) or user-level (`~/.claude/agents/`)
- Built-in types: **Explore** (read-only, Haiku), **Plan** (research), **general-purpose** (full tools)
- **`isolation: worktree`** — run in isolated git worktree with auto-cleanup
- **`background: true`** — always run as background task
- **`memory: user|project|local`** — persistent cross-session learning
- **`skills`** field — preload skill content into subagent context
- **`permissionMode`** — `default`, `acceptEdits`, `dontAsk`, `bypassPermissions`, `plan`
- **`hooks`** — lifecycle hooks scoped to subagent execution
- **`maxTurns`** — limit agentic turns
- Cannot spawn other subagents (no nesting)

**Quick start:** `/agents` command or create `.claude/agents/my-agent.md`

**Details:** `references/core-features.md` (Section 1)

---

### 2. Skills

Modular capabilities Claude automatically uses based on context, following the [Agent Skills](https://agentskills.io) open standard.

- YAML frontmatter + Markdown instructions in `SKILL.md`
- Progressive disclosure: metadata (always) -> instructions (on trigger) -> resources (on demand)
- **`context: fork`** — run in isolated subagent context
- **`agent`** field — specify which subagent type executes the skill
- **`disable-model-invocation: true`** — user-only invocation (prevents auto-trigger)
- **`user-invocable: false`** — model-only invocation (hidden from `/` menu)
- **`${CLAUDE_SKILL_DIR}`** — reference files relative to skill directory
- **`allowed-tools`** — restrict tool access during skill execution
- **`hooks`** — lifecycle hooks scoped to skill
- **`!`command`** syntax** — inject dynamic shell output into skill content
- Arguments via `$ARGUMENTS`, `$ARGUMENTS[N]`, or `$N` shorthand

**Quick start:** Create `.claude/skills/my-skill/SKILL.md` with frontmatter

**Details:** `references/core-features.md` (Section 2)

---

### 3. Slash Commands & Bundled Skills

User-invoked workflows via `/command` syntax. Commands and skills are now unified — `.claude/commands/` files still work but skills are recommended.

**Built-in commands (50+):** `/help`, `/clear`, `/compact`, `/config`, `/model`, `/agents`, `/mcp`, `/hooks`, `/plugin`, `/memory`, `/rewind`, `/rename`, `/resume`, `/stats`, `/cost`, `/usage`, `/copy`, `/diff`, `/doctor`, `/export`, `/fork`, `/fast`, `/context`, `/desktop`, `/review`, `/security-review`, `/pr-comments`, `/insights`, `/keybindings`, `/vim`, `/theme`, `/permissions`, `/plan`, `/skills`, `/tasks`, `/terminal-setup`, `/remote-control`, `/statusline`, `/sandbox`, and more.

**Bundled skills:**
- **`/simplify`** — reviews changed files for reuse/quality/efficiency, spawns 3 parallel review agents
- **`/batch <instruction>`** — orchestrates large-scale parallel changes across codebase using git worktrees
- **`/debug [description]`** — troubleshoots session issues by reading debug logs
- **`/claude-api`** — loads Claude API reference for your project's language

**Details:** `references/core-features.md` (Section 3)

---

### 4. Plugins

Bundled extensions containing commands, agents, skills, hooks, and MCP servers.

- Marketplace-based distribution
- Team-wide installation via `settings.json`
- **`git-subdir`** source type for subdirectories within git repos
- Custom npm registries and version pinning
- **`/reload-plugins`** — activate changes without restart
- Plugins can ship default `settings.json`

**Details:** `references/core-features.md` (Section 4)

---

### 5. MCP Servers

Model Context Protocol servers connecting Claude to external services (GitHub, Jira, Figma, Stripe, etc.).

- HTTP, SSE, or stdio transports
- OAuth authentication with step-up auth and discovery caching
- Project, user, or local scope
- **`oauth.authServerMetadataUrl`** config option
- Binary content handling (PDFs, Office docs, audio)

**Quick start:** `claude mcp add --transport http <name> <url>`

**Details:** `references/core-features.md` (Section 5)

---

### 6. Hooks

Shell commands, HTTP endpoints, or LLM prompts executed at lifecycle events.

**Event types (11):** `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `WorktreeCreate`, `WorktreeRemove`, `Notification`, `lastAssistantMessage`

- **HTTP hooks** — POST JSON to URLs instead of running shell commands
- **Prompt hooks** — LLM-evaluated hooks for complex decisions
- **MCP tool hooks** — hooks on MCP tool calls
- Command-based hooks with matcher patterns
- Exit code 2 blocks operations
- Hooks in skills and agents via frontmatter

**Quick start:** `/hooks` command

**Details:** `references/integration-patterns.md` (Section 3)

---

### 7. Configuration & Memory

Multi-level settings hierarchy: enterprise -> CLI -> local -> project -> user.

- **Auto-memory** — Claude automatically saves useful context (manage with `/memory`)
- 5-level memory hierarchy (Enterprise -> Project -> Rules -> User -> Local)
- `.claude/rules/` for modular, conditional rules with `paths:` frontmatter
- Import syntax `@path/to/file` (max 5 hops)
- Managed settings via macOS plist or Windows Registry
- `settings.json` at multiple scopes

**Details:** `references/configuration-guide.md`

---

### 8. CI/CD Integration

Automated Claude Code in GitHub Actions and GitLab CI/CD.

- **GitHub Actions:** `@claude` mentions in PRs/issues, `/install-github-app`
- **GitLab CI/CD:** Automated MR creation and reviews
- AWS Bedrock and Google Vertex support
- Headless mode (`claude -p`) for automation

**Details:** `references/integration-patterns.md`

---

### 9. Background Tasks & Worktrees

- `Ctrl+B` — move running command to background (Tmux: press twice)
- `Ctrl+F` — kill all background agents (two-press confirm)
- `!` prefix — bash mode (run commands without Claude interpretation)
- **`--worktree` (`-w`)** flag — isolated git worktree sessions
- `TaskOutput` tool to retrieve background results
- Auto-cleanup on session exit

---

### 10. Checkpoints & Rewind

- Auto-saves code state before each edit
- `Esc Esc` — rewind/summarize menu
- `/rewind` — restore code and/or conversation
- 30-day retention, persists across sessions
- Does NOT track bash/external changes

---

### 11. Sessions & History

- `/rename` — name sessions; `/resume` — resume by name/ID
- `/stats` — usage stats, streaks, model preferences
- `/fork` — fork conversation at current point
- `Ctrl+R` — reverse search command history
- History stored per working directory
- History-based autocomplete for `!` bash commands

---

### 12. Model Selection

- `Alt+P` / `Option+P` — quick model switch mid-prompt
- Aliases: `opus`, `sonnet`, `haiku`, `default`
- `/fast` — toggle fast mode
- Extended context: `[1m]` suffix for 1M token window
- Effort level display and adjustment via `/model`
- `Alt+T` / `Option+T` — toggle extended thinking

---

### 13. Agent Teams

For sustained parallelism across separate sessions (beyond subagents).

- Multiple agents working in parallel with independent contexts
- Communication across separate sessions
- Use when work exceeds single context window

**Details:** See `references/core-features.md` (Section 6)

---

### 14. Remote Control

- `claude remote-control` / `/remote-control` (`/rc`)
- Control terminal session from claude.ai
- Optional `--name` argument for custom session titles
- `/remote-env` — configure default remote environment

---

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `Ctrl+C` | Cancel input/generation |
| `Ctrl+B` | Background running task (Tmux: press twice) |
| `Ctrl+F` | Kill all background agents (press twice) |
| `Ctrl+T` | Toggle task list |
| `Ctrl+G` | Open prompt in text editor |
| `Ctrl+R` | Reverse search history |
| `Ctrl+O` | Toggle verbose output |
| `Ctrl+L` | Clear terminal screen |
| `Ctrl+V` | Paste image from clipboard |
| `Esc Esc` | Rewind/summarize menu |
| `Alt+P` / `Option+P` | Switch model |
| `Alt+T` / `Option+T` | Toggle extended thinking |
| `Shift+Tab` / `Alt+M` | Cycle permission modes |
| `Tab` | Accept prompt suggestion |
| `@` | File path autocomplete |
| `!` | Bash mode prefix |
| `/` | Command/skill prefix |
| `\` + `Enter` | Multiline input |
| `?` | Show available shortcuts |

---

## Quick Input Reference

| Prefix | What it does |
|--------|-------------|
| `/command` | Invoke built-in command or skill |
| `! command` | Run bash directly (output added to context) |
| `@path` | File path mention with autocomplete |

---

## Progressive Disclosure Strategy

Load reference files as needed based on the user's question:

| Category | Reference File |
|----------|---------------|
| Subagents, Skills, Commands, Plugins, MCP | `references/core-features.md` |
| Settings, Models, CLI, Permissions, Memory | `references/configuration-guide.md` |
| CI/CD, Hooks, Automation, Headless | `references/integration-patterns.md` |
| Errors, Installation, Performance | `references/troubleshooting-guide.md` |
| Sandboxing, Networking, Security | `references/advanced-features.md` |
| Workflows, Efficiency, Prompting | `references/best-practices.md` |
| Official documentation URLs | `references/documentation-urls.md` |
| Component comparison table | `assets/comparison-matrix.md` |
| Full keyboard/command reference | `assets/quick-reference.md` |

---

## Self-Updating Mechanism

When documentation may be outdated (user reports missing feature, new release):

1. Fetch latest from official docs (see `references/documentation-urls.md` for URLs)
2. Compare with current reference file
3. Update reference file with new content
4. Notify user of what was updated

---

## Version History

- v4.0 (2026-03-05): Major update to v2.1.69 — added auto-memory, bundled skills, agent teams, remote control, fast mode, worktree isolation, persistent agent memory, HTTP/prompt hooks, skill `context:fork`, `${CLAUDE_SKILL_DIR}`, 20+ new commands, restructured SKILL.md from 750 to ~430 lines
- v3.1 (2026-01-29): v2.1.23 update — task management, keybindings, autocomplete
- v3.0 (2026-01-18): Agent Skills Specification compliance
- v2.0 (2025-12-20): December 2025 features — background tasks, checkpoints, sessions
- v1.0 (2025-11-06): Initial creation
