# DevForgeAI Installation Guide

Complete installation and setup instructions for DevForgeAI framework.

**Version**: 1.0.1
**Updated**: 2025-11-20

---

## Example:   
```bash
    python3 -m installer install /mnt/c/projects/treelint

    #Or for the wizard (interactive):
    python3 -m installer wizard /mnt/c/projects/treelint

    #Available commands:
    python3 -m installer install /mnt/c/projects/treelint      # Install/upgrade
    python3 -m installer validate /mnt/c/projects/treelint     # Check installation
    python3 -m installer rollback /mnt/c/projects/treelint     # Restore backup
    python3 -m installer uninstall /mnt/c/projects/treelint    # Remove
```

## Prerequisites

Before installing DevForgeAI, ensure you have the following installed:

### Required Software

- **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
- **Git** - [Download Git](https://git-scm.com/downloads)
- **Claude Code Terminal 0.8.0+** - [Install Claude Code](https://code.claude.com/)

### System Requirements

- **Disk Space**: ~50 MB for installation + 100 MB for runtime cache
- **RAM**: 2 GB minimum
- **Internet Connection**: Required for initial setup and AI features

### Verify Prerequisites

```bash
# Check Python version
python3 --version  # Should be 3.8 or higher

# Check Git installation
git --version

# Check Claude Code availability
which claude || echo "Claude Code not in PATH"
```

---

## Installation Modes

DevForgeAI installer supports five installation modes:

| Mode | Use Case | Time | Backup |
|------|----------|------|--------|
| **Fresh** | New installation or clean slate | 2-3 min | N/A |
| **Upgrade** | Update existing installation | 3-4 min | Automatic |
| **Rollback** | Revert to previous version | 1-2 min | Uses existing backups |
| **Validate** | Check installation integrity | 1 min | N/A |
| **Uninstall** | Complete removal | 1 min | Optional |

---

## Fresh Installation

For new DevForgeAI installations on a clean system.

### Step 1: Clone Repository

```bash
git clone https://github.com/bankielewicz/DevForgeAI.git
cd DevForgeAI2
```

### Step 2: Run Fresh Install

```bash
python installer/install.py --mode=fresh --target ~/.claude
```

**Explanation**:
- `--mode=fresh`: Clean installation (skips backups)
- `--target ~/.claude`: Install to `.claude` directory in home folder

### Step 3: Verify Installation

```bash
# Test that .claude/ was populated
ls -la ~/.claude/skills/
ls -la ~/.claude/commands/

# Expected output: Multiple subdirectories for skills and commands
```

### Step 4: Restart Terminal

Close and reopen your Claude Code Terminal to load new slash commands.

```bash
# New terminal should have /dev, /qa, /create-story, etc. available
/help
```

---

## Upgrading

For existing DevForgeAI installations to update to the latest version.

### Step 1: Pull Latest Code

```bash
cd /path/to/DevForgeAI2
git pull origin main
```

### Step 2: Run Upgrade Mode

```bash
python installer/install.py --mode=upgrade --target ~/.claude
```

**What happens**:
1. Automatic backup created: `~/.claude.backup-v1.0.0-YYYYMMDD`
2. New files deployed to `~/.claude`
3. CLAUDE.md merged intelligently (preserves your custom content)
4. Validation runs automatically

### Step 3: Restart Terminal

Close and reopen Claude Code Terminal to load updated commands.

### Upgrade Options

```bash
# Upgrade to specific version
python installer/install.py --mode=upgrade --target ~/.claude --version=1.0.1

# Dry run (see what would change)
python installer/install.py --mode=upgrade --target ~/.claude --dry-run
```

---

## Rollback

If an upgrade causes issues, you can rollback to a previous version.

### Step 1: List Available Backups

```bash
ls ~/.claude.backup-*
# Example output:
# ~/.claude.backup-v1.0.0-20251115
# ~/.claude.backup-v0.9.5-20251101
```

### Step 2: Rollback to Backup

```bash
python installer/install.py --mode=rollback --backup=~/.claude.backup-v1.0.0-20251115
```

### Step 3: Verify Rollback

```bash
cat ~/.claude/version.json
# Should show the rolled-back version
```

### Step 4: Restart Terminal

Close and reopen Claude Code Terminal.

---

## Validation

Check installation integrity without making changes.

```bash
python installer/install.py --mode=validate --target ~/.claude
```

**Validation checks**:
- All required files exist (450+ framework files)
- File integrity (checksums match)
- CLAUDE.md format correct
- Skills and commands loadable
- Version metadata valid

**Example output**:
```
✓ Skills: 8/8 present
✓ Commands: 11/11 present
✓ Subagents: 26/26 present
✓ Context files: 6/6 valid
✓ Installation: VALID
```

---

## Uninstallation

Complete removal of DevForgeAI from your system.

### Option 1: Keep Backups

```bash
# Remove installation but keep backups
rm -rf ~/.claude
```

### Option 2: Complete Removal

```bash
# Remove everything including backups
rm -rf ~/.claude
rm -rf ~/.claude.backup-*
```

### Option 3: Using Installer

```bash
python installer/install.py --mode=uninstall --target ~/.claude

# Prompts for backup deletion confirmation
```

---

## Troubleshooting

#### Issue 1: "Python Not Found"

**Problem**: Running `python` or `python3` returns "command not found".

**Solution**:
```bash
# Check Python installation
which python3

# If not found, install Python 3.8+
# macOS: brew install python@3.8
# Ubuntu: sudo apt install python3.8
# Windows: Download from python.org

# Verify installation
python3 --version
```

---

#### Issue 2: "Permission Denied"

**Problem**: Installation fails with permission errors.

**Solution**:
```bash
# Option 1: Install to user directory (recommended)
python installer/install.py --mode=fresh --target ~/.claude

# Option 2: Fix permissions
chmod +x installer/install.py

# Option 3: Use sudo (not recommended)
sudo python installer/install.py --mode=fresh --target /opt/devforgeai
```

---

#### Issue 3: "Git Not Initialized"

**Problem**: Installer reports "not a git repository".

**Solution**:
```bash
# Initialize git in your project
git init
git add .
git commit -m "Initial commit"

# Then run installer
python installer/install.py --mode=fresh --target ~/.claude
```

---

#### Issue 4: "Backup Failed"

**Problem**: Upgrade mode reports backup creation failed.

**Solution**:
```bash
# Check disk space
df -h ~

# Manual backup before upgrading
cp -r ~/.claude ~/.claude.backup-manual-$(date +%Y%m%d)

# Then upgrade
python installer/install.py --mode=upgrade --target ~/.claude
```

---

#### Issue 5: "Commands Not Loaded"

**Problem**: After installation, slash commands like `/dev` are not available.

**Solution**:
```bash
# Restart Claude Code Terminal completely
# Close all terminal windows
# Reopen Claude Code

# Verify commands loaded
ls ~/.claude/commands/*.md

# Try explicit command
/help

# If still not working, reinstall
python installer/install.py --mode=upgrade --target ~/.claude
```

---

#### Issue 6: "Validation Fails"

**Problem**: Running validation mode reports missing or invalid files.

**Solution**:
```bash
# Check what is failing
python installer/install.py --mode=validate --target ~/.claude

# List actual files
find ~/.claude -type f -name "*.md" | head -20

# Repair with upgrade mode
python installer/install.py --mode=upgrade --target ~/.claude

# Or clean reinstall
rm -rf ~/.claude
python installer/install.py --mode=fresh
```

---

#### Issue 7: "Installer Script Not Found"

**Problem**: `installer/install.py` does not exist in cloned repo.

**Solution**:
```bash
# Verify you are in correct directory
pwd  # Should end in /DevForgeAI2

# Check if installer exists
ls -la installer/

# If missing, try pulling latest
git pull origin main
git checkout installer/install.py

# Verify and try again
python installer/install.py --mode=fresh
```

---

#### Issue 8: "Insufficient Disk Space"

**Problem**: "No space left on device" error.

**Solution**:
```bash
# Check available disk space
df -h ~

# Remove old backups to free space
rm -rf ~/.claude.backup-old-*

# Try installation again
python installer/install.py --mode=fresh

# Monitor installation
du -sh ~/.claude  # Check installation size as it runs
```

---

#### Issue 9: "Invalid JSON in Configuration"

**Problem**: Error about invalid JSON when installing.

**Solution**:
```bash
# Check JSON files
python -m json.tool ~/.claude/version.json

# Backup and remove corrupted file
cp ~/.claude/version.json ~/.claude/version.json.backup
rm ~/.claude/version.json

# Reinstall to recreate
python installer/install.py --mode=upgrade
```

---

#### Issue 10: "Git Merge Conflicts"

**Problem**: `git pull` shows merge conflicts.

**Solution**:
```bash
# Check what is conflicting
git status

# Discard local changes (if safe)
git checkout -- .

# Or stash changes
git stash

# Pull again
git pull origin main
```

---

#### Issue 11: "CLAUDE.md Merge Conflicts"

**Problem**: Installer reports conflicts in CLAUDE.md merge.

**Solution**:
```bash
# Review the conflict markers
cat ~/.claude/CLAUDE.md | grep "<<<<<<" -A 5 -B 5

# Installer pauses and asks for resolution
# Choose: Keep both, Keep yours, Keep installer version, Manual edit

# Or manually resolve
nano ~/.claude/CLAUDE.md
# Remove <<<<<<, ======, >>>>>> markers
# Keep desired content

# Re-run installer
python installer/install.py --mode=upgrade
```

---

#### Issue 12: "Old .claude/ Copy Still Present"

**Problem**: Both manual copy and installer present, causing conflicts.

**Solution**:
```bash
# Remove old manual copy
rm -rf ~/.claude

# Run fresh install with installer
python installer/install.py --mode=fresh --target ~/.claude
```

---

#### Issue 13: "Wrong Python Version"

**Problem**: Installer requires Python 3.8+, but system has older version.

**Solution**:
```bash
# Check current version
python3 --version

# Install Python 3.8+ (Ubuntu example)
sudo apt install python3.8

# Use specific version
python3.8 installer/install.py --mode=fresh
```

---

#### Issue 14: "Missing Dependencies"

**Problem**: Installer fails with module import errors.

**Solution**:
```bash
# Install Python dependencies (if any)
pip3 install -r requirements.txt

# Or ensure Python standard library available
# (installer uses only standard library modules)
```

---

#### Issue 15: "Version Mismatch"

**Problem**: Installed version does not match expected version.

**Solution**:
```bash
# Check current version
cat ~/.claude/version.json

# Check installer version
python installer/install.py --version

# Clean reinstall if mismatch
rm -rf ~/.claude
python installer/install.py --mode=fresh
```

---

## FAQ - Frequently Asked Questions

**Q:** Can I install DevForgeAI in a non-standard location?

**A:** Yes! Use the `--target` flag:

```bash
python installer/install.py --mode=fresh --target ~/my-custom-location/.claude
```

The `--target` path can be anywhere you have write permissions.

---

**Q:** Will installation overwrite my existing work?

**A:** No. The upgrade mode creates automatic backups:

```bash
# Before upgrading
python installer/install.py --mode=upgrade

# Creates backup like:
# ~/.claude.backup-v1.0.0-20251117
```

Your custom work is safe in the backup.

---

**Q:** How do I know what version I have installed?

**A:** Check the version file:

```bash
cat ~/.claude/version.json
# Output: { "version": "1.0.1", "release_date": "2025-11-17" }
```

---

**Q:** Can multiple users share one DevForgeAI installation?

**A:** Not recommended. Each user should install separately:

```bash
# User 1
python installer/install.py --mode=fresh --target ~/.claude

# User 2 (different account)
python installer/install.py --mode=fresh --target ~/.claude
```

Each user gets their own `.claude` directory.

---

**Q:** What if I want to use the old manual copy approach?

**A:** The manual approach still works but is deprecated:

```bash
# Old approach (NOT recommended, deprecated)
cp -r .claude/* ~/.claude/

# New approach (recommended)
python installer/install.py --mode=fresh
```

The old approach will be supported for **at least 6 months** (until May 2026). After v2.0.0, use the installer.

---

**Q:** Can I install multiple versions of DevForgeAI?

**A:** Yes, use different target locations:

```bash
# Install v1.0.1
python installer/install.py --mode=fresh --target ~/.claude-v1.0.1

# Install v1.0.0 (from different branch)
git checkout v1.0.0
python installer/install.py --mode=fresh --target ~/.claude-v1.0.0
```

---

**Q:** What happens to my custom skills during upgrade?

**A:** Custom skills are preserved in backups:

```bash
# Backup contains your custom skills
ls ~/.claude.backup-v1.0.0-20251117/skills/

# After upgrade, merge them back if needed
cp -r ~/.claude.backup-v1.0.0-20251117/skills/my-custom-skill ~/.claude/skills/
```

---

**Q:** How do I completely remove DevForgeAI?

**A:** See Uninstallation section above:

```bash
# Complete removal
rm -rf ~/.claude
rm -rf ~/.claude.backup-*
```

---

**Q:** Can I install on Windows?

**A:** Yes, use PowerShell or Command Prompt:

```powershell
# PowerShell
python installer/install.py --mode=fresh --target "$HOME\.claude"
```

Paths will use backslashes automatically.

---

**Q:** What if installation is interrupted?

**A:** The installer is resumable:

```bash
# If interrupted, retry safely
python installer/install.py --mode=upgrade --target ~/.claude

# Upgrade mode resumes and completes installation
```

---

**Q:** How do I update just the documentation without reinstalling?

**A:** Pull latest code and read the docs directly:

```bash
cd /path/to/DevForgeAI2
git pull origin main

# Documentation is in:
# - README.md (overview)
# - installer/INSTALL.md (installation)
# - MIGRATION-GUIDE.md (migration)
# - ROADMAP.md (roadmap)
```

---

## Support

### Getting Help

- **Documentation**: Check [README.md](../README.md) for framework overview
- **Issues**: Report bugs at [GitHub Issues](https://github.com/your-org/DevForgeAI2/issues)
- **Discussions**: Ask questions in [GitHub Discussions](https://github.com/your-org/DevForgeAI2/discussions)

### Before Reporting Issues

1. ✅ Check this troubleshooting guide
2. ✅ Run validation: `python installer/install.py --mode=validate`
3. ✅ Check version: `cat ~/.claude/version.json`
4. ✅ Review [README.md](../README.md) for framework overview

Happy building with DevForgeAI! 🚀
