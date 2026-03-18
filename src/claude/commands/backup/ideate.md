---
description: Transform business idea into structured requirements. Use when exploring a new product concept, defining features for a business problem, or starting greenfield projects.
argument-hint: [business-idea-description]
model: opus
allowed-tools: Read, Glob, AskUserQuestion, Skill
---

# /ideate - Transform Business Idea into Requirements

Entry point for DevForgeAI — transforms business ideas into structured epics and requirements.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- ❌ DO NOT detect project mode (skill Phase 0 handles greenfield/brownfield detection)
- ❌ DO NOT invoke ideation-result-interpreter subagent (skill handles result interpretation)
- ❌ DO NOT invoke feedback hooks via Bash (skill handles hook integration)
- ❌ DO NOT parse or analyze brainstorm file content (skill handles brainstorm processing)

**DO (command responsibilities only):**
- ✅ Check for existing brainstorms and ask user via AskUserQuestion
- ✅ Capture business idea (from args or user prompt)
- ✅ Set context markers (business idea, brainstorm file, project mode hint)
- ✅ Invoke skill immediately after validation

## Phase 0: Brainstorm Auto-Detection

```
brainstorms = Glob(pattern="devforgeai/specs/brainstorms/BRAINSTORM-*.brainstorm.md")
IF brainstorms found:
  Display each: "- {id}: {title} ({confidence})"
  AskUserQuestion:
    Question: "Would you like to use an existing brainstorm as input for ideation?"
    Header: "Brainstorm"
    Options:
      - label: "Yes - use most recent"
        description: "Pre-populate ideation with brainstorm data"
      - label: "Yes - let me choose"
        description: "Select which brainstorm to use"
      - label: "No - start fresh"
        description: "Begin new ideation session"
    multiSelect: false
  # Brainstorm resume decision captured here; skill uses selected path
```

## Phase 1: Capture Business Idea

```
IF $ARGUMENTS has 10+ words: BUSINESS_IDEA = $ARGUMENTS
ELSE: Prompt user for description (what problem, who benefits, what success looks like)
```

## Phase 2: Invoke Skill

```
<ideation-context>
  <business-idea>${BUSINESS_IDEA}</business-idea>
  <brainstorm-file>${selected_brainstorm_path or "none"}</brainstorm-file>
  <project-mode>auto-detect</project-mode>
</ideation-context>

Skill(command="discovering-requirements")
```

Skill handles: project mode detection, 6-phase requirements (10-60 questions), complexity, epics, result interpretation, hooks.

## Phase 3: Display Results

Output `result.display.template` as-is.

## Error Handling

| Error | Recovery |
|-------|----------|
| Skill load failure | Check `.claude/skills/discovering-requirements/SKILL.md` |
| Invocation failed | Verify registration, restart Claude Code |
| Validation failure | Review Phase 6.4 output, re-run `/ideate` |
| User exits | Re-run `/ideate [idea]` |

**Next step:** `/create-epic [epic-name]` to generate epics from requirements.
