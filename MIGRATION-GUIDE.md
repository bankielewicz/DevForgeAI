# DevForgeAI Migration Guide

**For existing users upgrading to v1.0.1 (Production Release)**

This guide explains how to migrate from the old manual `.claude/` copy approach to the new installer-based installation.

**Version**: 1.0.1
**Target Users**: Anyone with DevForgeAI v1.0.0 or earlier
**Migration Time**: ~10 minutes

---

## What's Changing?

### Before (v1.0.0 and earlier)

❌ **Old Workflow** - Manual file copying:

1. Clone repository
2. Manually copy `.claude/` folder contents
3. Edit files in-place
4. Manually manage updates
5. Handle conflicts yourself

```bash
# Old approach (deprecated)
git clone ...
cp src/.claude/* ~/.claude/
# Edit ~/.claude files directly
# Manual updates/merges
```

### After (v1.0.1+)

✅ **New Workflow** - Installer-based management:

1. Clone repository
2. Run automated installer
3. Edit files in `src/` directory
4. Run installer to deploy
5. Automatic backups and rollback

```bash
# New approach (recommended)
git clone ...
python installer/install.py --mode=fresh
# Edit src/ files
# Automatic updates via installer
```

### Key Benefits of New Approach

| Aspect | Old Approach | New Approach |
|--------|--------------|--------------|
| Installation | Manual, error-prone | Automated, verified |
| Updates | Manual merge conflicts | Automated with rollback |
| Backups | Manual backups | Automatic backups |
| Rollback | Manual restoration | One-command rollback |
| Validation | Manual checking | Automated validation |
| Configuration | Edit files directly | Managed by installer |

---

## 7-Step Migration Process

### Step 1: Create Backup

Create a complete backup before starting migration:

```bash
# Backup current installation
cp -r ~/.claude ~/.claude-backup-v1.0.0-$(date +%Y-%m-%d-%H%M%S)

# Verify backup created
ls -la ~/.claude-backup-*

# Expected: Shows backup directory with timestamp
```

**Safety Checklist**:
- [ ] Backup directory created
- [ ] Backup size similar to ~/.claude
- [ ] Backup is readable: `ls ~/.claude-backup-*/skills/ | head`

---

### Step 2: Pull Latest Code

Get the latest DevForgeAI with installer:

```bash
cd /path/to/your/DevForgeAI2

# Update repository
git fetch origin main
git pull origin main

# Verify installer exists
ls -la installer/install.py
```

**If git pull shows conflicts**:

```bash
# Backup your local changes
git stash

# Pull clean
git pull origin main

# Your changes saved (can restore later if needed)
git stash pop
```

---

### Step 3: Run Installer in Upgrade Mode

Execute the new installer to migrate your setup:

```bash
# Run upgrade mode (creates automatic backup)
python installer/install.py --mode=upgrade --target ~/.claude

# Expected output:
# ✅ Creating backup...
# ✅ Installing v1.0.1...
# ✅ Validating installation...
# ✅ Migration complete!
```

**What the installer does**:

1. Detects existing `.claude/` installation
2. Creates automatic backup: `.claude-backup-v1.0.0-2025-11-17`
3. Deploys new v1.0.1 skills and commands
4. Updates configuration files
5. Validates installation integrity

---

### Step 4: Verify Installation Success

Test that the new installation works:

```bash
# List installed commands (should have 11+)
ls ~/.claude/commands/*.md | wc -l

# Check installed version
cat ~/.claude/version.json
# Expected: version 1.0.1

# Verify key files
[ -f ~/.claude/CLAUDE.md ] && echo "✅ CLAUDE.md present"
[ -d ~/.claude/skills ] && echo "✅ skills/ present"
[ -d ~/.claude/commands ] && echo "✅ commands/ present"

# Run validation mode
python installer/install.py --mode=validate --target ~/.claude
```

**Expected Results**:
- ✅ 11+ commands installed
- ✅ Version shows 1.0.1
- ✅ All key files present
- ✅ Validation passes

---

### Step 5: Update Development Workflow

Understand how workflow changes with new approach:

#### New Workflow - Edit in src/, Deploy with Installer

```bash
# 1. Edit framework code in src/ directory
vim src/.claude/skills/devforgeai-development/SKILL.md
vim src/.claude/commands/dev.md

# 2. Test your changes
python installer/install.py --mode=upgrade

# 3. Restart Claude Code Terminal

# 4. Use updated skills
/dev STORY-001
```

#### What Changed

**BEFORE** (manually editing ~/.claude):
```bash
vim ~/.claude/skills/devforgeai-development/SKILL.md  # Edit deployed files
# Changes take effect after terminal restart
```

**AFTER** (edit src/, installer deploys):
```bash
vim src/.claude/skills/devforgeai-development/SKILL.md  # Edit source
python installer/install.py --mode=upgrade  # Deploy changes
# Terminal restart loads new version
```

#### Why This is Better

- **Source control**: Changes in `src/` are version controlled
- **Rollback**: Can revert to previous version easily
- **Separation**: Source (`src/`) separate from deployment (`~/.claude/`)
- **Collaboration**: Easy to share changes via git

---

### Step 6: Test Migration

Verify that everything works with new workflow:

```bash
# Test 1: Create a story
/create-story "Test migration story after upgrade"

# Test 2: Run development cycle
# (if you have a simple test story)
/dev STORY-001

# Test 3: Run quality check
/qa STORY-001

# Test 4: Test installer commands
python installer/install.py --mode=validate
```

**Expected**: All commands work as before, but now with new installer infrastructure.

---

### Step 7: Cleanup Old Files

Clean up old backups and temporary files:

```bash
# List all backups
ls -la ~/.claude* | grep backup

# Keep manual backup, can remove automated ones older than 1 week
rm ~/.claude.backup-v1.0.0-2025-11-10

# Or keep all backups if paranoid (safe)
# They don't interfere with running installation
```

**Recommendation**:
- ✅ Keep at least one manual backup from Step 1
- ✅ Keep automatic backup from installer (recent)
- ❌ Can safely delete older backups after 2 weeks

---

## Safety Checklist

Review before starting migration:

**Pre-Migration**:
- [ ] Running v1.0.0 or earlier (check `cat ~/.claude/version.json`)
- [ ] Have ~200MB disk space free
- [ ] Have time for 10-15 minute process
- [ ] Not in middle of active development

**During Migration**:
- [ ] Backup created in Step 1
- [ ] `git pull` succeeds without conflicts
- [ ] Installer runs successfully in Step 3
- [ ] Validation passes in Step 4

**Post-Migration**:
- [ ] Commands work in Step 6
- [ ] Old and new approaches both work (during transition)
- [ ] Can rollback if issues found

---

## Troubleshooting Migration Issues

### Issue: "installer/install.py not found"

**Problem**: Installer script missing after `git pull`.

**Solution**:
```bash
# Check that you have latest
git fetch origin main
git pull origin main

# Verify file exists
ls -la installer/install.py

# If still missing, may be local git issue
git reset --hard origin/main  # WARNING: Loses local changes!
python installer/install.py --mode=upgrade
```

---

### Issue: "Upgrade fails, want to rollback"

**Problem**: Installer upgrade encountered error.

**Solution**:
```bash
# Option 1: Automatic rollback
python installer/install.py --mode=rollback --backup ~/.claude-backup-v1.0.0-2025-11-17

# Option 2: Manual restoration from Step 1 backup
rm -rf ~/.claude
cp -r ~/.claude-backup-v1.0.0-$(date +%Y-%m-%d)/ ~/.claude

# Test restoration
/dev --help

# Restart terminal and retry upgrade
```

---

### Issue: "Commands not working after migration"

**Problem**: Slash commands like `/create-story` missing or broken.

**Solution**:
```bash
# 1. Restart Claude Code Terminal completely
# Close all terminal windows
# Reopen Claude Code

# 2. Verify commands installed
ls ~/.claude/commands/*.md | wc -l

# 3. If still broken, reinstall
python installer/install.py --mode=upgrade

# 4. Check for conflicting versions
cat ~/.claude/version.json
```

---

### Issue: "Disk space error during migration"

**Problem**: "No space left on device".

**Solution**:
```bash
# Check available space
df -h ~

# Remove old backups to free space
rm ~/.claude.backup-old-* 2>/dev/null

# Remove unnecessary files
rm -rf /tmp/devforgeai-* 2>/dev/null

# Retry migration
python installer/install.py --mode=upgrade
```

---

### Issue: "Git conflicts when pulling"

**Problem**: `git pull` shows merge conflicts.

**Solution**:
```bash
# Option 1: Accept incoming changes (safe if you don't customize src/.claude/)
git checkout --theirs .
git add .
git commit -m "Accept upstream changes"

# Option 2: Keep your changes, merge manually
git merge --abort  # Cancel merge
# Manually resolve conflicts, then retry

# Option 3: Hard reset to remote (WARNING: loses local changes!)
git reset --hard origin/main
```

---

### Issue: "Installation takes too long"

**Problem**: Installer running >5 minutes.

**Solution**:
```bash
# Check if process is still running
ps aux | grep install.py

# View progress (if process is running, this means it's working)
du -sh ~/.claude  # Check directory growing

# Wait up to 10 minutes
# If stuck >15 min, can safely kill:
pkill -f install.py

# Then retry
python installer/install.py --mode=upgrade
```

---

## After Migration

### Customizations

If you customized the old `.claude/` files, you'll need to reapply:

```bash
# 1. Check backup for your customizations
diff ~/.claude ~/.claude-backup-v1.0.0-2025-11-17/

# 2. Find your custom changes
ls ~/.claude-backup-v1.0.0-2025-11-17/skills/

# 3. If you have custom skills, copy them
cp ~/.claude-backup-v1.0.0-2025-11-17/skills/my-custom-skill ~/.claude/skills/

# 4. Or edit in src/ for future customizations
vim src/.claude/skills/my-custom-skill/

# 5. Redeploy
python installer/install.py --mode=upgrade
```

### Continuous Updates

With new workflow, getting updates is easier:

```bash
# Check for updates
git fetch origin main

# See what changed
git diff main...origin/main

# Update and deploy
git pull origin main
python installer/install.py --mode=upgrade

# Restart terminal
```

### Learning New Workflow

Review these documents:

1. **README.md** - Framework overview
2. **INSTALL.md** - Installation details
3. **Workflow Documentation** - In `.devforgeai/` directory

```bash
# Quick reference
cat README.md | head -50
cat installer/INSTALL.md | grep "Installation Modes" -A 10
```

---

## Timeline & Support

### Deprecation Timeline

| Version | Status | Support Until |
|---------|--------|----------------|
| **v1.0.0** | Deprecated | 2026-05-17 (~6 months) |
| **v1.0.1** | **CURRENT** | Future |

### Old Approach (Manual Copy)

The old manual copy approach (manually copying `.claude/`) is **deprecated**:

- ❌ No longer recommended
- ⚠️ Will stop being supported in v2.0.0
- ✅ Still works for next 6 months
- 🔄 Please migrate to installer approach

### Migration is NOT Urgent

**You have 6 months** to complete migration:

```bash
# Timeline
2025-11-17: v1.0.1 released with deprecation notice
2026-05-17: v2.0.0 released, old approach no longer supported
```

The installer approach becomes mandatory in v2.0.0, but you can take your time migrating.

---

## Support & Help

### Getting Help with Migration

If you encounter issues:

1. **Check this guide**: Most issues covered above
2. **Review INSTALL.md**: General installation troubleshooting
3. **Check logs**: `cat ~/.claude/install.log`
4. **Run validation**: `python installer/install.py --mode=validate`
5. **Create issue**: Include diagnostic information

### Asking for Help

When asking for help, include:

```bash
# Diagnostic information
echo "=== Migration Diagnostics ===" > diagnostic.txt
pwd >> diagnostic.txt
git status >> diagnostic.txt
python3 --version >> diagnostic.txt
cat ~/.claude/version.json >> diagnostic.txt
ls ~/.claude-backup-* >> diagnostic.txt
cat ~/.claude/install.log >> diagnostic.txt  # Last 50 lines

# Share diagnostic.txt in GitHub issue
```

---

## Summary

After migration to v1.0.1:

✅ **Installation** is now automated and reproducible
✅ **Updates** are easier with git + installer
✅ **Backups** happen automatically
✅ **Rollback** is one command away
✅ **Collaboration** is easier with source control

**Old way**: Edit `.claude/` directly
**New way**: Edit `src/.claude/`, run installer

The installer does the work of copying files, creating backups, and validating the installation. You focus on editing source files and using the framework.

**Questions?** See the troubleshooting section above or create a GitHub issue.

Happy developing! 🚀
