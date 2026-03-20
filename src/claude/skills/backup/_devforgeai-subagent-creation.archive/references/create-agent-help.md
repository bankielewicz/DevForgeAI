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

## Skill Workflow (6 Phases)

The devforgeai-subagent-creation skill executes:

1. Extract context markers from conversation
2. Load DevForgeAI framework references
3. Load mode-specific templates (if template mode)
4. Prepare specification for agent-generator
5. Invoke agent-generator subagent v2.0 (framework-aware generation)
6. Process and return structured results

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

**Invokes:** claude-code-terminal-expert skill, agent-generator subagent v2.0
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
