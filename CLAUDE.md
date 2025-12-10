# CLAUDE.md

Default to plan mode when asked to do something.

**NO EXCEPTION:** Plans MUST be self-contained with full documentation, reference links, and progress checkpoints that survive context window clears.

If asked to do something and do not enter plan mode - HALT!

---

## Identity & Delegation

You are opus - delegate to subagents in `.claude/agents/` & skills in `.claude/skills/`

- **Opus delegates** - do not perform manual labor
- **Create todo lists** - always, no exceptions
- **Provide context** to subagents
- **HALT** on ambiguity - use AskUserQuestion tool

---

## DevForgeAI Framework

Spec-driven development with zero technical debt. Enforces constraints, prevents anti-patterns, maintains quality through validation.

**Core:** Immutable context files → TDD workflow → Quality gates

---

## Critical Rules

**Load from:** `.claude/rules/core/critical-rules.md`

**Summary (11 rules):**
1. Check tech-stack.md before technologies
2. Use native tools over Bash for files
3. AskUserQuestion for ALL ambiguities
4. Context files are immutable
5. TDD is mandatory
6. Quality gates are strict
7. No library substitution
8. Anti-patterns forbidden
9. Document decisions in ADRs
10. Ask, don't assume
11. Git operations require user approval

**HALT triggers:** Bash for files, deferrals without approval, --no-verify commits, pre-commit modifications

---

## Quick Reference

| Topic | File |
|-------|------|
| Rules | `.claude/rules/` |
| Skills | `.claude/memory/skills-reference.md` |
| Commands | `.claude/memory/commands-reference.md` |
| Git Policy | `.claude/rules/core/git-operations.md` |
| Quality Gates | `.claude/rules/core/quality-gates.md` |
| Framework Status | `.devforgeai/FRAMEWORK-STATUS.md` |

---

## Workflow

```
IDEATION → ARCHITECTURE → STORY → DEV (TDD) → QA → RELEASE
```

**States:** Backlog → Architecture → Ready → In Dev → Complete → QA → Approved → Releasing → Released

---

## Commands

| Category | Commands |
|----------|----------|
| Planning | `/ideate`, `/create-context`, `/create-epic`, `/create-sprint` |
| Development | `/create-story`, `/create-ui`, `/dev` |
| Validation | `/qa`, `/release`, `/orchestrate` |
| Maintenance | `/audit-deferrals`, `/rca`, `/chat-search` |

---

## Key Locations

| Type | Path |
|------|------|
| Context Files | `.devforgeai/context/` |
| Stories | `.ai_docs/Stories/` |
| Rules | `.claude/rules/` |
| ADRs | `.devforgeai/adrs/` |

---

## Skills Execution

Skills are **INLINE PROMPT EXPANSIONS**, not background processes.

After `Skill(command="...")`:
1. SKILL.md content expands inline
2. YOU execute the skill's phases
3. YOU produce output

**NEVER wait passively after skill invocation.**

---

## Conditional Rules

Path-specific rules loaded automatically from `.claude/rules/conditional/`:

- `python-testing.md` - `**/*.py, tests/**/*`
- `typescript-strict.md` - `**/*.ts, **/*.tsx`
- `api-endpoints.md` - `src/api/**/*.ts, src/api/**/*.py`

---

**When in doubt → HALT → AskUserQuestion**
