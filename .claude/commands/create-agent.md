---
description: Create DevForgeAI-aware Claude Code subagent
argument-hint: [name] [options]
model: sonnet
allowed-tools: Read, Glob, Grep, Skill, Task, AskUserQuestion
---

# /create-agent - DevForgeAI Subagent Creation

Create Claude Code subagents following DevForgeAI framework patterns and official Claude Code best practices.

---

## Quick Reference

```bash
# Guided mode (recommended)
/create-agent my-reviewer

# Domain mode
/create-agent backend-architect --domain=backend

# Template mode
/create-agent code-reviewer --template=code-reviewer

# Custom spec mode
/create-agent custom-agent --spec=specs/my-spec.md
```

**Domains:** backend, frontend, qa, security, deployment, architecture, documentation
**Templates:** code-reviewer, test-automator, documentation-writer, deployment-coordinator, requirements-analyst

---

## Command Workflow

### Phase 0: Argument Validation and Mode Detection

**Validate subagent name:**
```
IF $1 empty OR $1 NOT match "[a-z][a-z0-9-]*":
  AskUserQuestion:
    Question: "What should the subagent be named? (lowercase-with-hyphens)"
    Header: "Name"
    Options:
      - "Let me type a name"
      - "Cancel"
    multiSelect: false

  Extract NAME from response
  Validate format
ELSE:
  NAME = $1
```

**Detect mode:**
```
MODE = "guided"  # Default

IF $2 starts with "--template=":
  MODE = "template"
  TEMPLATE_NAME = substring after "="
  Validate template exists in .claude/skills/agent-generator/templates/

ELSE IF $2 starts with "--domain=":
  MODE = "domain"
  DOMAIN = substring after "="
  Validate DOMAIN in [backend, frontend, qa, security, deployment, architecture, documentation]

ELSE IF $2 starts with "--spec=":
  MODE = "custom"
  SPEC_FILE = substring after "="
  Validate file exists

ELSE IF $2 provided:
  Report: "Unknown option: $2"
  AskUserQuestion for mode selection
```

**Check existing:**
```
Glob(pattern=".claude/agents/${NAME}.md")

IF found:
  AskUserQuestion:
    Question: "Subagent '${NAME}' exists. Overwrite?"
    Header: "Exists"
    Options:
      - "Overwrite"
      - "Rename"
      - "Cancel"
    multiSelect: false
```

**Summary:**
```
✓ Name: ${NAME}
✓ Mode: ${MODE}
✓ Proceeding...
```

---

### Phase 1: Load Claude Code Guidance

**Invoke skill for official patterns:**
```
Skill(command="claude-code-terminal-expert")

# Skill loads official Claude Code subagent patterns
# Provides: file format, YAML fields, tool selection, model guidelines
```

---

### Phase 2: Set Context Markers

**Prepare for agent-generator:**
```
**Subagent Name:** ${NAME}
**Creation Mode:** ${MODE}
**Framework:** DevForgeAI
**Claude Code Guidance:** Available (from skill)

IF MODE == "template":
  **Template:** ${TEMPLATE_NAME}
ELSE IF MODE == "domain":
  **Domain:** ${DOMAIN}
ELSE IF MODE == "custom":
  **Spec File:** ${SPEC_FILE}
```

---

### Phase 3: Invoke agent-generator

**Delegate to subagent:**
```
Task(
  subagent_type="agent-generator",
  description="Generate ${NAME} subagent",
  prompt="Generate DevForgeAI-aware Claude Code subagent '${NAME}' in ${MODE} mode.

Context markers in conversation:
- Subagent Name: ${NAME}
- Creation Mode: ${MODE}
- Claude Code patterns loaded from skill
- Framework: DevForgeAI

Requirements:
- Use Phase 0 loaded references (Claude Code patterns, CLAUDE.md, lean-orchestration if needed)
- Execute ${MODE} mode workflow
- Generate framework-aware system prompt
- Run Step 3.6 validation (12-point framework compliance)
- Generate reference file if needed (Step 4.5)
- Return structured report

Return:
- Generated files (paths, line counts)
- Validation results (12-point compliance)
- Integration guidance
- Next steps
"
)
```

---

### Phase 4: Display Results

**Output agent-generator report:**
```
Report: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Report: "✅ Subagent Generation Complete"
Report: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

Display: result.generated_files
Display: result.validation
Display: result.integration
```

---

### Phase 5: Next Steps

**Guide user:**
```
Report: "📋 Next Steps:"
Report: "1. Restart terminal to load subagent"
Report: "2. Verify: /agents (should show '${NAME}')"
Report: "3. Test: Use ${NAME} subagent to [task]"
IF result.has_reference:
  Report: "4. Review: ${result.reference_path}"
Report: ""
Report: "✅ Subagent '${NAME}' created!"
```

---

## Error Handling

### Invalid Name
```
Report: "❌ Name must be lowercase-with-hyphens"
Examples: code-reviewer, test-automator
AskUserQuestion for correction
```

### Template Not Found
```
Report: "❌ Template '${TEMPLATE_NAME}' not found"
List available templates
AskUserQuestion: Use guided mode or cancel?
```

### Invalid Domain
```
Report: "❌ Unknown domain: ${DOMAIN}"
List: backend, frontend, qa, security, deployment, architecture, documentation
AskUserQuestion for valid domain
```

### Spec File Missing
```
Report: "❌ Spec file not found: ${SPEC_FILE}"
AskUserQuestion: Guided mode, correct path, or cancel?
```

### Generation Failed
```
Report: "❌ Generation failed"
Display: error_details
AskUserQuestion: Show details, retry guided, or cancel?
```

---

## Success Criteria

- [ ] Subagent file created (.claude/agents/${NAME}.md)
- [ ] Reference file created (if applicable)
- [ ] Validation passed (12/12 checks)
- [ ] User guided on next steps
- [ ] Character budget <15K
- [ ] Token usage <5K main conversation

---

## Integration

**Invokes:**
- claude-code-terminal-expert skill (official patterns)
- agent-generator subagent v2.0 (generation + validation)

**Created subagents work with:**
- All DevForgeAI skills (framework-aware integration)
- Claude Code workflows (official pattern compliance)

**Use cases:**
- Custom subagents for project needs
- Command refactoring subagents (lean orchestration)
- Domain-specific subagents (backend, frontend, qa, etc.)
- Team workflow automation

---

## Performance

**Token Budget:**
- Command overhead: ~4K tokens
- Skill (isolated): ~2K tokens
- Subagent (isolated): ~30-50K tokens
- **Main conversation: ~4K** (92% isolated)

**Execution Time:**
- Guided: ~2-3 min
- Template: ~1-2 min
- Domain: ~1-2 min
- Custom: ~1-2 min

**Character Count:** 8,147 (54% of 15K budget) ✅ COMPLIANT
