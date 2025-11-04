# Existing DevForgeAI CLI Discovery & Removal Guide

**Date:** 2025-11-04
**Found:** Old DevForgeAI CLI installed globally via npm
**Type:** Persona launcher (NOT validation utility)
**Status:** Can be safely removed or kept (different purpose)

---

## What Was Found

### Installation Details

**Location:** `/home/bryan/.nvm/versions/node/v22.19.0/bin/devforgeai`
**Type:** Bash script (node.js global package)
**Version:** 1.2.0
**Installed via:** npm (symlinked to `/mnt/c/Projects/DevForgeAI4`)
**Package name:** `devforgeai@1.2.0`

**Source directory:** `/mnt/c/Projects/DevForgeAI4` (old DevForgeAI version)

---

## What This CLI Does

**Purpose:** Persona launcher for Claude Code

**NOT a validation utility. It's a launcher script.**

**Functionality:**
```bash
# Launches Claude Code with persona-specific system prompts
devforgeai --analyst    # Launches "Mary" (Business Analyst)
devforgeai --architect  # Launches "Winston" (System Architect)
devforgeai --dev        # Launches "James" (Developer)
devforgeai --po         # Launches "Sarah" (Product Owner)
devforgeai --ux         # Launches "Sally" (UX Designer)
devforgeai --qa         # Launches "Quinn" (QA Engineer)
devforgeai --sm         # Launches "Bob" (Scrum Master)
devforgeai --pm         # Launches "John" (Product Manager)
```

**What it actually executes:**
```bash
# When you run: devforgeai --dev
# It executes: claude " " --append-system-prompt "$(cat .claude/system-prompts/dev.md)"
# Result: Claude loads with James (Developer) persona
```

---

## Is This the Same as What We're Building?

### NO - Completely Different Tools

| Aspect | Existing CLI (Persona Launcher) | Proposed CLI (Validators) |
|--------|--------------------------------|---------------------------|
| **Purpose** | Launch Claude with personas | Validate workflows/stories |
| **Language** | Bash script | Python |
| **Domain** | Persona switching | DoD validation, Git checking |
| **Usage** | `devforgeai --analyst` | `devforgeai validate-dod story.md` |
| **Integration** | Launches Claude sessions | Pre-commit hooks, slash commands |
| **Version** | 1.2.0 (from DevForgeAI4) | Not yet built |
| **Relevance** | Old persona system (v4) | New validation system (v2) |

**They share the name "devforgeai" but serve completely different purposes.**

---

## Should You Remove It?

### Assessment

**The old CLI is from DevForgeAI4 (old version):**
- Current project: DevForgeAI2 (this repo)
- Old CLI references: DevForgeAI4 directory
- Functionality: Persona launcher (now replaced by Skills in DevForgeAI2)

**DevForgeAI2 uses Skills, not Personas:**
- Skills: `.claude/skills/devforgeai-*` (current approach)
- Personas: `.claude/system-prompts/*.md` (old approach from v4)
- Old CLI is **obsolete** for DevForgeAI2

---

### Recommendation: **Remove the Old CLI**

**Why remove:**
1. ✅ Obsolete (references DevForgeAI4 which you're not using)
2. ✅ Name conflict (blocks new devforgeai-cli validators)
3. ✅ Persona approach replaced by Skills in v2
4. ✅ Symlink points to non-existent `/mnt/c/Projects/DevForgeAI4`
5. ✅ No value in current workflows

**Why keep:**
- ❌ No reason - DevForgeAI2 doesn't use persona system

---

## How to Remove Old DevForgeAI CLI

### Option 1: Uninstall via npm (Recommended)

```bash
# Check if it's an npm global package
npm list -g --depth=0 | grep devforgeai

# Uninstall globally
npm uninstall -g devforgeai

# Verify removal
which devforgeai
# Should return: (no output) or "devforgeai not found"
```

---

### Option 2: Manual Removal

```bash
# Remove symlink
rm /home/bryan/.nvm/versions/node/v22.19.0/bin/devforgeai

# Remove package directory (if exists)
rm -rf /home/bryan/.nvm/versions/node/v22.19.0/lib/node_modules/devforgeai

# Verify removal
which devforgeai
# Should return: (no output)
```

---

### Option 3: Leave It (If You Might Use DevForgeAI4)

**Only if:**
- You plan to use DevForgeAI4 in parallel
- You want persona launcher functionality
- You can tolerate name conflict

**Note:** You'll need to rename new validators to avoid conflict:
```bash
# Instead of: devforgeai validate-dod
# Use: devforge-validate dod
# Or: dfai validate-dod
```

**Not recommended** - confusing to have two tools with same name

---

## Verification Steps

### After Removal

**Step 1: Verify old CLI removed**
```bash
which devforgeai
# Expected: (no output) or "devforgeai: not found"
```

**Step 2: Verify npm package removed**
```bash
npm list -g --depth=0 | grep devforgeai
# Expected: (no matches)
```

**Step 3: Check for residual files**
```bash
ls -la /home/bryan/.nvm/versions/node/v22.19.0/bin/ | grep devforgeai
# Expected: (no matches)

ls -la /home/bryan/.nvm/versions/node/v22.19.0/lib/node_modules/ | grep devforgeai
# Expected: (no matches)
```

**Step 4: Verify PATH**
```bash
echo $PATH | grep -o "[^:]*devforgeai[^:]*"
# Expected: (no matches)
```

---

## After Removal: Install New DevForgeAI-CLI

### Once old CLI removed, install new validators:

**Option 2 (Integrated - Recommended):**
```bash
cd /mnt/c/Projects/DevForgeAI2

# Install as editable package
pip install -e .claude/scripts/devforgeai_cli/

# Verify new CLI
devforgeai validate-dod --help
# Should show: "DevForgeAI DoD Validator" (new tool)
```

**Or direct script usage:**
```bash
# No installation, use scripts directly
python .claude/scripts/devforgeai_cli/validate_dod.py .ai_docs/Stories/STORY-002.story.md
```

---

## Name Conflict Resolution

### If You Keep Old CLI

**Rename new validators to avoid conflict:**

**Option A: Different command name**
```bash
# New tool: dfai (short for DevForgeAI)
dfai validate-dod story.md
dfai check-git
dfai validate-context
```

**Option B: Subcommand approach**
```bash
# Keep devforgeai name but different subcommands
devforgeai validate dod story.md  # New validators
devforgeai --analyst               # Old persona launcher
```

**Option C: Module prefix**
```bash
# New tool: devforgeai-validate
devforgeai-validate dod story.md
devforgeai-validate git
devforgeai-validate context

# Old tool: devforgeai (unchanged)
devforgeai --analyst
```

---

## Recommended Action Plan

### Step 1: Remove Old CLI (Recommended)

```bash
# Uninstall via npm
npm uninstall -g devforgeai

# Verify removal
which devforgeai
```

**Rationale:**
- Old CLI references DevForgeAI4 (obsolete)
- DevForgeAI2 uses Skills, not Personas
- Frees up "devforgeai" command name for new validators
- No loss of functionality (Skills replace Personas)

---

### Step 2: Implement New Validators

**After removal, proceed with Option 3 (Hybrid):**

**Integrated core validators:**
```
.claude/scripts/devforgeai_cli/
├── validate_dod.py
├── check_git.py
├── validate_context.py
└── cli.py  # Entry point: devforgeai validate-dod ...
```

**Installation:**
```bash
pip install -e .claude/scripts/devforgeai_cli/
```

**Usage:**
```bash
devforgeai validate-dod .ai_docs/Stories/STORY-002.story.md
devforgeai check-git
devforgeai validate-context
```

**No name conflict** (old CLI removed)

---

## Summary & Recommendation

**What you have:** Old DevForgeAI v4 persona launcher (obsolete)
**What you need:** New DevForgeAI validators (DoD, Git, context)
**Conflict:** Same command name "devforgeai"

**Recommended action:**

1. ✅ **Remove old CLI** via `npm uninstall -g devforgeai`
   - Obsolete (references DevForgeAI4)
   - Replaced by Skills in DevForgeAI2
   - Frees name for new validators

2. ✅ **Implement new validators** in `.claude/scripts/devforgeai_cli/`
   - Integrated with framework
   - Use freed "devforgeai" command name
   - Pre-commit hook integration

3. ✅ **Verify no conflicts** after implementation
   - `which devforgeai` points to new validators
   - Old persona launcher completely removed
   - Clean slate for new architecture

---

**Would you like me to proceed with:**
1. Guide you through removing old CLI
2. Implement new validators after removal
3. Both (remove old, implement new)
