---
description: Create DevForgeAI-aware Claude Code subagent
argument-hint: [name] [options]
model: opus
allowed-tools: Read, Glob, Grep, Skill, Task, AskUserQuestion
---

# /create-agent - DevForgeAI Subagent Creation

Create Claude Code subagents following DevForgeAI framework patterns.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT generate agent files directly or load templates
- ❌ DO NOT invoke agent-generator subagent (skill handles this)
- ❌ DO NOT perform validation checks (skill handles 12-check validation)

**DO (command responsibilities only):**
- ✅ MUST validate agent name, detect mode, check existing, invoke skill

## Phase 0: Argument Validation and Mode Detection

```
IF $1 empty OR $1 NOT match "[a-z][a-z0-9-]*":
    AskUserQuestion:
        Question: "What should the subagent be named? (lowercase-with-hyphens)"
        Header: "Name"
        Options: ["Let me type a name", "Cancel"]
        multiSelect: false
    Extract NAME; Validate format
ELSE: NAME = $1

MODE = "guided"
IF $2 starts with "--template=": MODE = "template"; TEMPLATE_NAME = value
ELIF $2 starts with "--domain=":
    MODE = "domain"; DOMAIN = value
    IF DOMAIN not in [backend, frontend, qa, security, deployment, architecture, documentation]:
        AskUserQuestion:
            Question: "Unknown domain '${DOMAIN}'. Which domain?"
            Header: "Domain"
            Options: ["backend", "frontend", "qa", "security"]
            multiSelect: false
ELIF $2 starts with "--spec=": MODE = "custom"; SPEC_FILE = value
ELIF $2 provided:
    AskUserQuestion:
        Question: "Unknown option. Which creation mode?"
        Header: "Mode"
        Options: ["Guided (recommended)", "Template-based", "Domain-based", "Custom spec"]
        multiSelect: false

Glob(pattern=".claude/agents/${NAME}.md")
IF found:
    AskUserQuestion:
        Question: "Subagent '${NAME}' exists. What to do?"
        Header: "Exists"
        Options: ["Overwrite", "Rename", "Cancel"]
        multiSelect: false

Display: "✓ Name: ${NAME} | Mode: ${MODE}"
```

## Phase 1: Invoke Skill

**Subagent Name:** ${NAME}
**Creation Mode:** ${MODE}

```
Skill(command="devforgeai-subagent-creation")
```

**Skill handles ALL workflow** including framework references, template selection, agent-generator invocation, validation, and file creation.

## Error Handling

| Error | Resolution |
|-------|------------|
| Invalid name format | Prompt for correction |
| Template not found | AskUserQuestion: Use guided mode or cancel? |
| Invalid domain | AskUserQuestion for valid domain |
| Spec file missing | AskUserQuestion: Guided mode, correct path, or cancel? |
| Generation failed | AskUserQuestion: Show details, retry guided, or cancel? |

## References

- Skill: `.claude/skills/devforgeai-subagent-creation/SKILL.md`
- Help: `.claude/skills/devforgeai-subagent-creation/references/create-agent-help.md`
- Domains: backend, frontend, qa, security, deployment, architecture, documentation
- Templates: code-reviewer, test-automator, documentation-writer, deployment-coordinator, requirements-analyst

**Command follows lean orchestration: Validate → Set markers → Invoke skill**
