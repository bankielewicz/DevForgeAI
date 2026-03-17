---
description: Generate architectural context files for project
argument-hint: [project-name]
model: opus
allowed-tools: Read, Write, Edit, Glob, Grep, Skill, Task, AskUserQuestion
---

# Create Context Command

Generates the 6 architectural context files that define project constraints and standards.

## Lean Orchestration Enforcement

**DO NOT (before skill invocation):**
- Do not perform context file generation, validation, or architecture review
- Do not invoke subagents directly (skill handles architect-reviewer)
- Do not generate design system files (skill handles UI detection)

**DO (command responsibilities only):**
- Check for existing context files (pre-flight)
- Ensure git repository has initial commit
- Invoke skill immediately after pre-flight

---

## Arguments

- `project-name` (optional): Name of the project (defaults to current directory name)

---

## Phase 1: Pre-Flight Check

**Check for existing context:**

```
Glob(pattern="devforgeai/specs/context/*.md")
```

**If context files exist:**
- Use `AskUserQuestion` with options:
  - Overwrite all existing files
  - Merge with existing files (preserve custom changes)
  - Abort and exit

**If abort selected:**
- Exit with message: "Context creation cancelled. Existing files preserved."

---

## Phase 2: Git Repository Initialization Check

Check if repository has commits by examining the environment context.

**If git repository exists but no commits yet:**

1. Create initial commit with framework files:
```
Bash(git add .claude/ devforgeai/ devforgeai/specs/ CLAUDE.md README.md)
Bash(git commit -m "chore: Initialize DevForgeAI framework structure")
```

**If commit creation fails:** Continue anyway — /dev command will handle empty repos gracefully.

---

## Phase 3: Invoke Architecture Skill

```
Skill(command="designing-systems")
```

The skill owns the complete workflow: context discovery, file generation, ADR creation, technical specs, validation, prompt alignment, domain reference generation, architecture review, design system generation, post-creation validation, and success reporting (Phases 1-10).

After skill invocation, the skill's SKILL.md expands inline — YOU execute the skill's phases sequentially.

---

## Error Handling

| Error | Resolution |
|-------|------------|
| Context files already exist | AskUserQuestion: Overwrite / Merge / Abort |
| Skill invocation failed | Verify `.claude/skills/designing-systems/SKILL.md` exists |
| Validation failed | Skill reports issues and prompts for resolution |

---

## Integration Points

**Invokes:** `designing-systems` skill (all phases)

**Prerequisites:** None (entry point for new projects)

**Enables:** `/create-epic`, `/create-sprint`, `/dev`, all development workflows

**Related:** `/create-epic` (create epics after context), `/dev` (implement stories)

---

### Feedback Hook (STORY-030)

After skill completes successfully, triggers optional feedback (non-blocking).

See `devforgeai/protocols/hook-integration-pattern.md` for implementation pattern.
