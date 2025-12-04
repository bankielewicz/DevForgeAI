# CLAUDE.md Merge Strategy Guide

This guide explains the 4 merge strategies available when the DevForgeAI installer detects an existing CLAUDE.md file in your project.

## Overview

When installing DevForgeAI into a project that already has a CLAUDE.md file, you'll be prompted to choose how to handle the merge. Each strategy balances preservation of your customizations against ensuring DevForgeAI framework compatibility.

## Merge Strategies

### 1. Auto-Merge (Recommended)

**What it does:**
- Preserves all your custom sections verbatim
- Updates DevForgeAI framework sections to latest version
- Maintains original section positions where possible

**Best for:**
- Projects with custom project-specific instructions in CLAUDE.md
- Users who want framework updates without losing customizations

**How it works:**
1. Creates timestamped backup (e.g., `CLAUDE.md.backup-20251204-143022`)
2. Parses your CLAUDE.md into sections
3. Identifies framework vs user-created sections
4. Replaces framework sections with latest DevForgeAI content
5. Preserves user sections at their original positions

**Example:**
```
Your CLAUDE.md has:
- ## My Custom Rules (user section - PRESERVED)
- ## Critical Rules (framework section - UPDATED)
- ## Project Notes (user section - PRESERVED)
```

### 2. Replace

**What it does:**
- Creates backup of your existing CLAUDE.md
- Overwrites with fresh DevForgeAI template
- Your original content is preserved in backup file

**Best for:**
- Projects where existing CLAUDE.md is outdated or corrupted
- Fresh start with DevForgeAI while keeping backup

**How it works:**
1. Creates timestamped backup
2. Writes DevForgeAI template as new CLAUDE.md
3. Logs backup location for reference

**Note:** You can manually copy sections from backup back into new file.

### 3. Skip

**What it does:**
- Leaves your existing CLAUDE.md completely unchanged
- No backup created (nothing modified)
- Installation continues with other files

**Best for:**
- Projects where CLAUDE.md is managed separately
- Testing installation without affecting existing config
- When you want to manually merge later

### 4. Manual

**What it does:**
- Creates backup of existing CLAUDE.md
- Creates `CLAUDE.md.devforgeai-template` reference file
- You manually merge the two files

**Best for:**
- Complex CLAUDE.md with extensive customizations
- When you want full control over merge process
- When auto-merge detects conflicts

**How it works:**
1. Creates timestamped backup
2. Writes DevForgeAI template to `.devforgeai-template` file
3. Displays merge instructions
4. You compare and merge manually

## Conflict Detection

Auto-merge uses a 70% similarity threshold to detect conflicts:

- **≥70% similar:** No conflict - section is considered unchanged
- **<70% similar:** Conflict detected - you've significantly modified a framework section

When conflicts are detected, auto-merge halts and prompts you to choose:
1. **Keep your version** - Preserve your modifications
2. **Use DevForgeAI version** - Replace with framework content
3. **Manual resolution** - Switch to manual merge strategy

## Backup Files

All strategies (except Skip) create timestamped backups:

```
CLAUDE.md.backup-YYYYMMDD-HHMMSS
```

Example: `CLAUDE.md.backup-20251204-143022`

If multiple backups occur in the same second, a counter is added:
```
CLAUDE.md.backup-20251204-143022-001
```

Backups are verified with SHA256 hash to ensure integrity.

## Recommendations

| Scenario | Recommended Strategy |
|----------|---------------------|
| First time adding DevForgeAI | Auto-Merge |
| Minor customizations | Auto-Merge |
| Extensive customizations | Manual |
| Outdated/broken CLAUDE.md | Replace |
| CI/CD or testing | Skip |
| Conflict during auto-merge | Manual |

## Logging

All merge operations are logged to `install.log` with:
- ISO 8601 timestamp
- Strategy selected
- Action taken
- Backup file path (if created)
- Conflict count (for auto-merge)
- Resolution choices (if conflicts)
- Final status

## See Also

- [Conflict Resolution Instructions](./claudemd-conflict-resolution.md)
- [DevForgeAI Installation Guide](../README.md)
