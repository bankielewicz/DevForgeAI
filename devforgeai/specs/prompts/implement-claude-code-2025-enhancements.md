# AI Implementation Prompt: Claude Code 2025 Enhancements for DevForgeAI

**Purpose:** This prompt provides full context for Claude to implement the Claude Code 2025 enhancements to the DevForgeAI framework in a new session.

**Branch:** `feat/claude-code-2025-enhancements` (already created)

---

## PROMPT START

You are implementing Phase 1 of a multi-phase enhancement plan to apply Claude Code 2025 features to the DevForgeAI framework.

### Critical Instructions

1. **Read the full plan first:** `/home/bryan/.claude/plans/devforgeai-claude-code-enhancements.md`
2. **You are on branch:** `feat/claude-code-2025-enhancements`
3. **Update the plan file** after completing each phase by marking checkboxes `[x]`
4. **Create a todo list** to track your progress through each phase
5. **Commit after each phase** with message format: `feat(rules): Phase N - description`

### Phase 1 Task: Create `.claude/rules/` Directory Structure

Create the following directory structure with all files:

```
/mnt/c/Projects/DevForgeAI2/.claude/rules/
├── README.md
├── core/
│   ├── critical-rules.md
│   ├── git-operations.md
│   └── quality-gates.md
├── workflow/
│   ├── tdd-workflow.md
│   ├── story-lifecycle.md
│   └── qa-validation.md
├── security/
│   ├── no-hardcoded-secrets.md
│   └── input-validation.md
├── conditional/
│   ├── python-testing.md
│   ├── typescript-strict.md
│   ├── api-endpoints.md
│   └── story-files.md
└── devforgeai-integration.md
```

### File Content Source

All file contents are specified in the plan file at `/home/bryan/.claude/plans/devforgeai-claude-code-enhancements.md` under "Phase 1: Create `.claude/rules/` Directory Structure" → "File Contents".

### Implementation Steps

1. **Create todo list** with all 12 files to create
2. **Create directories:**
   ```bash
   mkdir -p .claude/rules/core .claude/rules/workflow .claude/rules/security .claude/rules/conditional
   ```
3. **Create each file** using the Write tool with content from the plan
4. **Verify creation:**
   ```bash
   find .claude/rules -name "*.md" | wc -l
   # Expected: 12
   ```
5. **Update plan file** - mark Phase 1 checkbox as `[x]`
6. **Commit:**
   ```bash
   git add .claude/rules/
   git commit -m "feat(rules): Phase 1 - Create .claude/rules/ directory structure with 12 rule files"
   ```

### Verification Checklist

After Phase 1, verify:
- [ ] 12 markdown files created in `.claude/rules/`
- [ ] 4 conditional rules have `paths:` frontmatter
- [ ] README.md explains the rules system
- [ ] All files have version metadata in frontmatter
- [ ] Plan file updated with `[x]` for Phase 1

### After Phase 1 Completion

Ask the user: "Phase 1 complete. Would you like me to continue with Phase 2 (Extract critical rules from CLAUDE.md) or stop here?"

### Reference Links

- Claude Code Rules: https://code.claude.com/docs/en/memory
- Plan file: `/home/bryan/.claude/plans/devforgeai-claude-code-enhancements.md`
- Project root: `/mnt/c/Projects/DevForgeAI2`

### Context Files to Read If Needed

- Current CLAUDE.md: `/mnt/c/Projects/DevForgeAI2/CLAUDE.md`
- Git operations policy: `/mnt/c/Projects/DevForgeAI2/.claude/memory/git-operations-policy.md`
- Existing settings: `/mnt/c/Projects/DevForgeAI2/.claude/settings.json`

---

## PROMPT END

---

## Usage Instructions

Copy everything between "PROMPT START" and "PROMPT END" and paste it as your first message in a new Claude Code session.

Claude will:
1. Read the plan file
2. Create a todo list
3. Implement Phase 1
4. Update the plan with progress
5. Commit the changes
6. Ask if you want to continue to Phase 2

---

## Full 8-Phase Overview

| Phase | Description | Files Changed |
|-------|-------------|---------------|
| 1 | Create `.claude/rules/` directory | 12 new files |
| 2 | Extract critical rules from CLAUDE.md | Update CLAUDE.md |
| 3 | Create conditional path-based rules | Already in Phase 1 |
| 4 | Update subagents with new fields | 10+ subagent files |
| 5 | Refactor CLAUDE.md with imports | CLAUDE.md |
| 6 | Add new hook events | settings.json |
| 7 | Update CLI/scripts with new flags | installer/ files |
| 8 | Validation and documentation | Various |

---

## Resumption Prompt (For Later Phases)

If you need to resume in a new session after Phase 1:

```
Continue implementing the Claude Code 2025 enhancements for DevForgeAI.

1. Read the plan: /home/bryan/.claude/plans/devforgeai-claude-code-enhancements.md
2. Check which phases are complete (marked with [x])
3. Continue with the next incomplete phase
4. Update the plan after completing each phase
5. Commit after each phase

Branch: feat/claude-code-2025-enhancements
```
