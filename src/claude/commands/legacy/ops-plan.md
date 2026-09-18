---
description: Launch the operations planning workflow (standalone or project-anchored)
argument-hint: [--standalone] flag to force standalone mode
model: sonnet
allowed-tools: AskUserQuestion, Read, Skill, Glob
execution-mode: immediate
---

# /ops-plan - Operations Planning Workflow

Invoke the operating-business skill to guide operational execution planning. This command detects project context and delegates all business logic to the skill.

---

## Mode Overview

**Standalone mode** - Run without a DevForgeAI project. Produces general operational guidance that you can apply to any venture.

**Project-anchored mode** - Run inside a DevForgeAI project. Detects the project automatically and offers /release integration so outputs link directly into your project workflow.

---

## Command Workflow

### Phase 0: Argument Parsing and Mode Detection

**Step 0.1: Parse arguments**

```
STANDALONE_FLAG = false

FOR arg in $ARGUMENTS:
    IF arg == "--standalone":
        STANDALONE_FLAG = true
```

**Step 0.2: Detect DevForgeAI project context**

Project detection uses directory presence only. Check whether the devforgeai/ directory exists in the current working directory using the Glob tool.

```
IF STANDALONE_FLAG == true:
    SET MODE = "standalone"
    Display: "Mode: Standalone (override via --standalone flag)"
ELSE:
    context_check = Glob(pattern="devforgeai/specs/context/*.md")

    IF context_check is not empty:
        SET MODE = "project-anchored"
        Display: "Mode: Project-Anchored (devforgeai/ directory detected)"
    ELSE:
        SET MODE = "standalone"
        Display: "Mode: Standalone (no devforgeai/ directory detected - fallback to standalone mode)"
```

No git commands or network calls are used for detection.

---

### Phase 1: Project Integration (Project-Anchored Only)

When MODE == "project-anchored", offer /release integration.

```
IF MODE == "project-anchored":
    Display: "DevForgeAI project detected."
    Display: "Operations outputs can be linked to devforgeai/specs/business/operations/ for release integration."

    AskUserQuestion(questions=[{
        question: "Link operations outputs to your DevForgeAI project for /release integration?",
        header: "Release Integration",
        options: [
            {label: "Yes - link to devforgeai/specs/business/operations/", description: "Outputs saved to project for release workflow"},
            {label: "No - keep outputs standalone", description: "Outputs displayed but not saved to project"}
        ],
        multiSelect: false
    }])
```

---

### Phase 2: Invoke Operating-Business Skill

Delegate all business logic to the operating-business skill.

```
Display: "Delegating to operating-business skill..."

Skill(skill="operating-business")
```

The command is a thin invoker. All menu presentation, sub-skill orchestration, and reference loading is handled by the operating-business skill.

---

## Error Handling

If the operating-business skill is not found, display an error suggesting the user verify the skill exists at `src/claude/skills/operating-business/SKILL.md`.

When no project is detected, the command falls back to standalone mode gracefully without error.
