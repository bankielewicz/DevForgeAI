# Domain Routing Table

Maps user question patterns to specific reference files for mandatory loading in Phase 02.

---

## Routing Rules

### Domain 1: Components (subagents, skills, commands, plugins, MCP, agent teams)

**Keywords:** subagent, agent, skill, SKILL.md, command, slash command, plugin, MCP, server, model context protocol, agent team, `/agents`, `/skills`, `/plugin`, `/mcp`

**Primary Reference:** `references/core-features.md`

**Sections to focus on:** Match keyword to section number:
- "subagent" / "agent" -> Section 1: Subagents
- "skill" / "SKILL.md" -> Section 2: Skills
- "command" / "slash" -> Section 3: Slash Commands & Bundled Skills
- "plugin" -> Section 4: Plugins
- "MCP" / "model context protocol" -> Section 5: MCP Servers
- "agent team" -> Section 6: Agent Teams

---

### Domain 2: Configuration (settings, models, permissions, memory, rules)

**Keywords:** setting, config, model, permission, memory, CLAUDE.md, rules, `.claude/`, auto-memory, `/config`, `/model`, `/memory`, `/permissions`, `/settings`, `settings.json`, hierarchy, enterprise, managed

**Primary Reference:** `references/configuration-guide.md`

---

### Domain 3: Integration (CI/CD, hooks, GitHub Actions, GitLab, automation)

**Keywords:** CI, CD, CI/CD, hook, hooks, GitHub Actions, GitLab, headless, automation, DevContainers, remote control, `PreToolUse`, `PostToolUse`, `SessionStart`, `SessionEnd`, `SubagentStart`, `SubagentStop`, `Stop`, `Notification`, HTTP hook, prompt hook, `/hooks`, webhook

**Primary Reference:** `references/integration-patterns.md`

---

### Domain 4: Troubleshooting (errors, installation, performance issues)

**Keywords:** error, not working, can't, won't, fails, broken, issue, help, install, npm, permission denied, crash, slow, hang, freeze, timeout, debug, `/doctor`, `/debug`, diagnostic, WSL

**Primary Reference:** `references/troubleshooting-guide.md`

---

### Domain 5: Advanced (sandboxing, networking, security, enterprise)

**Keywords:** sandbox, network, proxy, security, monitoring, container, isolation, firewall, certificate, SSL, TLS, telemetry, OpenTelemetry, analytics, privacy, compliance, enterprise, HIPAA, SOC, `/sandbox`

**Primary Reference:** `references/advanced-features.md`

---

### Domain 6: Best Practices (workflows, efficiency, prompting)

**Keywords:** workflow, efficiency, best practice, optimize, tips, patterns, token, token efficiency, native tools, plan mode, system prompt, performance, speed, `/fast`

**Primary Reference:** `references/best-practices.md`

---

### Domain 7: Reference (shortcuts, command lists, cheat sheets, comparisons)

**Keywords:** shortcut, keyboard, key binding, keybinding, command list, cheat sheet, reference card, comparison, compare, difference between, vs, versus, which one, when to use

**Primary References:**
- `assets/quick-reference.md`
- `assets/comparison-matrix.md`

---

### Domain 8: Prompt Engineering

**Keywords:** prompt, prompting, chain of thought, XML tags, role, multishot, few-shot, system prompt, extended thinking, long context, prompt template, prompt engineering, give claude a role

**Primary Reference:** Load selectively from `references/prompt-engineering/`:
- **General overview:** `overview.md` or `pompt-engineering-overview.md`
- **Chain of thought:** `chain-of-thought.md`
- **XML tags:** `use-xml-tags.md`
- **Roles:** `give-claude-a-role.md`
- **Examples/multishot:** `Use-examples-multishot prompting-to-guide-Claudes-behavior.md`
- **Extended thinking:** `extended-thinking-tips.md`
- **Long context:** `long-context-tips.md`
- **Prompt generation:** `prompt-generator.md`
- **Prompt improvement:** `prompt-improver.md`
- **Complex prompts:** `chain-complex-prompts.md`
- **Clarity:** `be-clear-and-direct.md`
- **Building skills:** `The-Complete-Guide-to-Building-Skills-for-Claude.md`
- **Templates:** `user-prompt-templates.md`

Load `overview.md` PLUS 1-2 files most relevant to $QUESTION keywords.

---

### Domain 9: Skills Specification (Agent Skills spec, SKILL.md format)

**Keywords:** agent skills spec, SKILL.md format, frontmatter, skill specification, agentskills.io, skill packaging, `.skill` file, skill creation, skill structure

**Primary Reference:** Load selectively from `references/skills/`:
- **Full specification:** `agent-skills-spec.md`
- **Overview:** `overview.md`
- **Quick start:** `quick-start.md`
- **Best practices:** `best-practices.md`
- **Enterprise:** `skills-for-enterprise.md`
- **API usage:** `using-agent-skills-with-the-api.md`
- **Clarity:** `be-clear-and-direct.md`

Load `overview.md` or `agent-skills-spec.md` PLUS 1-2 files most relevant to $QUESTION.

---

## Multi-Domain Resolution

If a question matches keywords from 2 or more domains, load ALL matched primary reference files.

**Examples:**
- "How do I configure MCP servers for CI/CD?" -> Domain 1 (components) + Domain 3 (integration) -> load `core-features.md` + `integration-patterns.md`
- "Troubleshooting subagent permission errors" -> Domain 4 (troubleshooting) + Domain 1 (components) -> load `troubleshooting-guide.md` + `core-features.md`
- "Best practices for writing skills" -> Domain 6 (best-practices) + Domain 9 (skills-spec) -> load `best-practices.md` + `references/skills/best-practices.md`

**Maximum references per question:** 3 primary reference files. If more than 3 domains match, prioritize by keyword match strength (exact match > partial match > tangential match).

---

## Fallback Behavior

If NO domain matches (zero keyword hits from any domain):
- Default to Domain 1: Components
- Load `references/core-features.md`
- This provides the broadest coverage of Claude Code features

---

## Routing Verification

After classification, verify the result makes sense:

```
IF $DOMAINS contains "troubleshooting" AND user is NOT reporting a problem:
    Remove "troubleshooting" from $DOMAINS
    (Words like "can't" may trigger troubleshooting for non-troubleshooting questions)

IF $DOMAINS.length == 0 after verification:
    Apply fallback behavior
```
