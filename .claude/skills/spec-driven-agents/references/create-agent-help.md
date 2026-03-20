# Create Agent - Help & Reference

**Source:** Extracted from `/create-agent` command for lean orchestration compliance (STORY-461)

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

## Creation Modes

### Guided Mode (Default)
Interactive workflow that collects all agent parameters through AskUserQuestion prompts. Recommended for new users.

### Template Mode
Uses pre-built templates for common agent types. Faster creation with sensible defaults.

### Domain Mode
Creates agents specialized for a specific domain with appropriate tool restrictions and system prompts.

### Custom Spec Mode
Creates agents from a user-provided specification file with custom requirements.

---

## Skill Workflow (7 Phases)

The spec-driven-agents skill executes with anti-skip enforcement:

0. Initialization (parse args, create checkpoint, handle resume)
1. Framework Context Loading (load framework refs + validation checklist)
2. Requirements Gathering (mode-specific user interaction)
3. Specification Assembly (build complete spec for agent-generator)
4. Agent Generation (delegate to agent-generator subagent v2.0)
5. Validation (independent 12-point compliance check)
6. Result Processing & Handoff (display report, clean up checkpoint)

**Resume:** `/create-agent --resume AGENT-NNN`

---

## Display Results Format

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✅ Subagent Generation Complete
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Generated Files:
  {result.generated_files}

Validation:
  {result.validation}

Integration:
  {result.integration}
```

---

## Next Steps (After Creation)

1. Restart terminal to discover new subagent
2. Verify with `/agents` command
3. Test invocation with sample task
4. Review reference file (if generated)

---

## Error Handling Details

### Invalid Name
```
❌ Name must be lowercase-with-hyphens
Examples: code-reviewer, test-automator
```
→ AskUserQuestion for correction

### Template Not Found
```
❌ Template '${TEMPLATE_NAME}' not found
Available: code-reviewer, test-automator, documentation-writer, deployment-coordinator, requirements-analyst
```
→ AskUserQuestion: Use guided mode or cancel?

### Invalid Domain
```
❌ Unknown domain: ${DOMAIN}
Valid: backend, frontend, qa, security, deployment, architecture, documentation
```
→ AskUserQuestion for valid domain

### Spec File Missing
```
❌ Spec file not found: ${SPEC_FILE}
```
→ AskUserQuestion: Guided mode, correct path, or cancel?

### Generation Failed
```
❌ Generation failed
{error_details}
```
→ AskUserQuestion: Show details, retry guided, or cancel?

---

## Success Criteria

- Subagent file created (`.claude/agents/${NAME}.md`)
- Reference file created (if applicable)
- Validation passed (12/12 checks)
- User guided on next steps

---

## Integration

**Invokes:** agent-generator subagent v2.0 (via spec-driven-agents skill)
**Created subagents work with:** All DevForgeAI skills (framework-aware integration)
**Use cases:** Custom subagents, command refactoring subagents, domain-specific subagents, team workflow automation

---

## Performance

| Component | Tokens |
|-----------|--------|
| Command overhead | ~4K |
| Skill (isolated) | ~2K |
| Subagent (isolated) | ~30-50K |
| Main conversation | ~4K (92% isolated) |

**Execution Time:** Guided ~2-3 min, Template ~1-2 min, Domain ~1-2 min, Custom ~1-2 min
