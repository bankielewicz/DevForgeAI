---
description: Audit commands for hybrid command/skill violations (excessive code before Skill invocation)
argument-hint: (no arguments required)
model: haiku
allowed-tools: Bash
---

# /audit-hybrid - Audit Command/Skill Hybrid Violations

Detects commands with excessive code blocks before `Skill()` invocation, which may indicate hybrid violations where manual workflow steps are documented instead of delegating to skills.

**Source:** RCA-038, STORY-410

---

## Command Workflow

### Phase 0: Run Audit Script

```bash
bash .claude/scripts/audit-command-skill-overlap.sh
```

### Phase 1: Display Results

Display the script output above. The script categorizes each command as:

- ❌ **Violation** — More than 4 code blocks before `Skill()` invocation
- ✅ **Clean** — 4 or fewer code blocks before `Skill()` invocation
- ⚠️ **Warning** — No `Skill()` invocation found in command

Exit code 0 means all commands are clean. Exit code 1 means violations were detected.

If violations are found, recommend reviewing the flagged commands and refactoring to move workflow logic into skills.
