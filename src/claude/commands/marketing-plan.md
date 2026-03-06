---
name: marketing-plan
description: Create marketing strategies, positioning frameworks, customer discovery plans, and content strategies for your business.
argument-hint: "[workflow] [--mode=standalone|project]"
---

# /marketing-plan

Invoke the **marketing-business** skill to build structured marketing deliverables.

## Usage

```
/marketing-plan [workflow] [--mode=standalone|project]
```

## Workflow Options

Select a workflow when invoking this command:

| Option | Description |
|--------|-------------|
| **Go-to-Market Strategy** | Channel selection, budget allocation, 30-day launch plan |
| **Positioning** | Positioning and messaging framework with competitive differentiation |
| **Customer Discovery** | Customer interview guides and persona development |
| **Content Strategy** | Content calendar, channel mix, and editorial planning |

## Mode

- `--mode=standalone` — Run without project context (default)
- `--mode=project` — Anchor to current DevForgeAI project, reading tech-stack.md and source-tree.md for product context

When no `--mode` flag is provided, standalone is the default mode.

## Skill Invocation

This command delegates all workflow logic to the marketing-business skill:

```
Skill(command="marketing-business", args="$ARGUMENTS")
```

The skill handles user input gathering, adaptive pacing, session resume, and artifact generation. This command is a thin invoker only.
