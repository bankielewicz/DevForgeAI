# Create Epic - Help & Reference

**Source:** Extracted from `/create-epic` command for lean orchestration compliance (STORY-461)

---

## Quick Reference

```bash
# Create epic with interactive workflow
/create-epic User Authentication System

# Create epic for e-commerce platform
/create-epic Payment Processing Overhaul

# Create epic for analytics
/create-epic Real-time Analytics Dashboard
```

---

## Schema Validation (STORY-301)

When create-epic receives ideation output from the /ideate workflow, validate against schema:

- **PASSED:** Proceed with full context preservation
- **WARN:** Proceed with degraded context preservation (legacy document)
- **FAILED:** HALT workflow with schema errors and recommended action

**Schema file:** `.claude/skills/spec-driven-architecture/references/skill-output-schemas.yaml`

---

## Context Preservation Validation (STORY-299)

After epic creation, the skill invokes context-preservation-validator to validate:
- Epic-to-brainstorm linkage via `source_brainstorm` field
- Brainstorm file existence verification
- Non-blocking by default (displays warning if linkage missing or broken)

---

## Epic Creation Workflow (Executed by Skill)

The spec-driven-architecture skill executes 8-phase epic creation:

1. **Epic Discovery** - Generate EPIC-ID, check for duplicate names via Grep, handle duplicates via AskUserQuestion
2. **Context Gathering** - Collect epic goal, timeline, priority, business value, stakeholders, success criteria (4 interactive AskUserQuestion flows)
3. **Feature Decomposition** - Invoke requirements-analyst subagent to generate 3-8 features, interactive review loop (accept/remove/add/modify)
4. **Technical Assessment** - Invoke architect-reviewer subagent for complexity scoring (0-10), risk identification, validate against context files
5. **Epic File Creation** - Load epic-template.md, populate with gathered data, write to devforgeai/specs/Epics/{EPIC-ID}.epic.md
6. **Requirements Specification** - Optional: Ask if user wants detailed requirements spec
7. **Validation & Self-Healing** - Execute 9 validation checks, self-heal correctable issues, HALT on critical failures
8. **Completion Summary** - Return structured JSON summary for display

**Reference files loaded progressively by skill:**
- epic-management.md (496 lines - Phases 1-2)
- feature-decomposition-patterns.md (850 lines - Phase 3)
- technical-assessment-guide.md (900 lines - Phase 4)
- epic-template.md (265 lines - Phase 5)
- epic-validation-checklist.md (800 lines - Phase 7)

**Subagents invoked by skill:**
- requirements-analyst (feature decomposition, optional requirements spec)
- architect-reviewer (technical assessment)

---

## Display Results Format

```
✅ Epic Created Successfully

Epic Details:
  📋 ID: {epic_id}
  🎯 Title: {epic_name}
  🏆 Priority: {priority}
  📊 Business Value: {business_value}
  📅 Timeline: {timeline}

Features: {feature_count} features identified
  {for each feature:
    ✨ {feature.name} - {feature.complexity}
  }

Technical Assessment:
  🔧 Complexity Score: {complexity_score}/10
  ⚠️ Key Risks: {risk_count} identified
  📦 Prerequisites: {prerequisite_count}
  {if technology_conflicts:
    ⚠️ ADR Required: {adr_topics}
  }

Files Created:
  📁 {epic_file_path}
  {if requirements_created:
    📁 {requirements_file_path}
  }

{validation_note}
```

**If validation warnings:**
```
⚠️ Validation Warnings:
  - {warning_1} (self-healed)
  - {warning_2} (self-healed)

Epic created successfully but review warnings before implementation.
```

---

## Next Steps Guidance

```
Next Steps:
  1. Review epic document: {epic_file_path}
  2. {if greenfield_mode:
       ⚠️ Create architectural context: /create-context {project-name}
     }
  3. {if adr_required:
       ⚠️ Create ADRs for technology decisions: {adr_topics}
     }
  4. Create sprint: /create-sprint {sprint-number}
  5. Break features into stories during sprint planning
  6. Implement stories: /dev {STORY-ID}
```

**Greenfield project guidance:**
```
📝 Greenfield Project Detected:
- No context files found (devforgeai/specs/context/*.md)
- Create architectural context before implementation
- Run: /create-context {project-name}
```

**High complexity guidance (score > 7):**
```
⚠️ High Complexity Epic ({complexity_score}/10):
- Consider breaking into smaller initiatives
- Review during sprint planning
```

**Over-scoped guidance (> 8 features):**
```
⚠️ Over-Scoped Epic ({feature_count} features):
- Recommended: 3-8 features per epic
- Consider splitting into multiple epics
```

---

## Error Handling Details

### Error: Invalid Epic Name
**Condition:** Empty, too short (<10 chars), too long (>100 chars), or invalid characters
**Action:** Phase 0 validation with clear error message and examples
**No fallback:** HALT with validation error

### Error: Skill Invocation Failed
**Condition:** spec-driven-architecture skill returns error
**Action:**
```
❌ Epic creation failed

The architecture skill encountered an issue:
  {skill_error_message}

Suggested actions:
  {skill_recovery_steps}

If error persists, check:
  1. Skill exists: .claude/skills/spec-driven-architecture/SKILL.md
  2. Reference files exist: .claude/skills/spec-driven-architecture/references/
  3. Context markers set correctly
```

### Error: Epic Validation Failed
**Condition:** Critical failures during Phase 7 validation
**Action:**
```
❌ Epic Validation Failed

Critical issues prevent epic creation:
  {validation_failures}

Self-healing attempted:
  {self_healed_issues}

Epic NOT created. Resolve critical issues:
  {failure_remediation_steps}

Retry: /create-epic {epic_name}
```

---

## Success Criteria

- [x] Epic name validated (format, length)
- [x] Context markers set correctly
- [x] Skill invoked successfully
- [x] Results displayed from skill output
- [x] Next steps guidance provided
- [x] Zero business logic in command
- [x] Single skill invocation only

---

## Integration

**Invoked by:** User via `/create-epic [epic-name]`
**Invokes:** spec-driven-architecture skill (epic creation mode)
**Skill invokes:** requirements-analyst, architect-reviewer subagents
**Prerequisites:** None (can create epics before context files exist)
**Enables:** /create-sprint, Epic → Sprint → Story workflow
**Creates:** devforgeai/specs/Epics/{EPIC-ID}.epic.md, optional devforgeai/specs/requirements/{EPIC-ID}-requirements.md

---

## Performance

| Component | Tokens |
|-----------|--------|
| Command overhead | ~2,000 |
| Skill execution (isolated) | ~125,000-146,000 |
| Total main conversation | ~2,000 |

**Execution Time:** Epic creation 3-5 min, with requirements 5-7 min
