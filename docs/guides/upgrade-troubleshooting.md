# Upgrade Troubleshooting Guide

## Overview

This guide helps you diagnose and fix issues that may occur during DevForgeAI version upgrades. Use this guide when an upgrade fails or behaves unexpectedly.

## Quick Diagnosis

### Step 1: Check Upgrade Status

```bash
# View current installed version
cat .devforgeai/.version.json

# Check upgrade logs
tail -50 .devforgeai/logs/upgrade-*.log

# List available backups
ls -lh .devforgeai/backups/
```

### Step 2: Identify Issue Category

**Upgrade hangs or stops:**
- Issue category: Performance/Timeout
- Diagnostics: Check logs, monitor disk space
- Solution: See "Upgrade Process Hangs" section

**Upgrade completes but shows errors:**
- Issue category: Validation Failure
- Diagnostics: Check validation report in logs
- Solution: See "Validation Failures" section

**Upgrade fails and rolls back automatically:**
- Issue category: Migration Failure
- Diagnostics: Check migration script output
- Solution: See "Migration Failures" section

**Files missing or corrupted after upgrade:**
- Issue category: Data Loss
- Diagnostics: Check backup integrity
- Solution: See "Data Loss Prevention" section

## Common Error Messages and Solutions

### Error: "Insufficient disk space for backup"

**Message:**
```
ERROR: Insufficient disk space for backup
Required: 500 MB, Available: 250 MB
```

**Cause:**
- Not enough free disk space to create backup before upgrade

**Solution:**

1. **Free up disk space:**
   ```bash
   # Remove old backups (keeping current version only)
   rm -rf .devforgeai/backups/*/

   # Clear package cache if available
   # npm cache clean --force  (if Node.js project)
   # pip cache purge          (if Python project)
   ```

2. **Verify space freed:**
   ```bash
   df -h | grep -E "/$|/home"
   ```

3. **Retry upgrade:**
   ```bash
   bash install.sh upgrade
   ```

**Prevention:**
- Check disk space before major upgrades
- Run `devforgeai backup cleanup` periodically
- Monitor backup directory size

---

### Error: "Migration script failed with exit code X"

**Message:**
```
ERROR: Migration script failed: migrations/v1.0.0-to-v1.1.0.py
Exit code: 1
Output: [migration script output]
```

**Cause:**
- Migration script encountered error during execution
- Common causes:
  - Required files not found
  - Permission denied
  - Configuration corruption

**Solution:**

1. **Check migration script logs:**
   ```bash
   tail -100 .devforgeai/logs/upgrade-*.log | grep -A 10 "Migration script"
   ```

2. **Verify required files exist:**
   ```bash
   # Common files required by migrations
   ls -la .devforgeai/
   ls -la .claude/
   ls -la .ai_docs/
   ```

3. **Check file permissions:**
   ```bash
   # Ensure files are readable/writable
   chmod -R 755 .devforgeai/
   chmod -R 755 .claude/
   ```

4. **Restore from backup and retry:**
   ```bash
   # Restore most recent backup
   bash install.sh restore latest

   # Retry upgrade
   bash install.sh upgrade
   ```

**Prevention:**
- Run migrations in test environment first
- Ensure file permissions correct before upgrade
- Keep DevForgeAI on expected version

---

### Error: "Validation failed: Expected file not found"

**Message:**
```
ERROR: Validation failed
Check failed: Expected file missing: .claude/skills/new-skill/SKILL.md
```

**Cause:**
- Migration completed but expected output files not created
- Indicates migration script incomplete or corrupted

**Solution:**

1. **Check backup is valid:**
   ```bash
   # Verify backup manifest
   cat .devforgeai/backups/vX.Y.Z-{timestamp}/backup-manifest.json
   ```

2. **Restore from backup:**
   ```bash
   bash install.sh restore .devforgeai/backups/vX.Y.Z-{timestamp}/
   ```

3. **Check for partial upgrade artifacts:**
   ```bash
   # Look for .tmp or .bak files
   find . -name "*.tmp" -o -name "*.bak" | head -20

   # Remove any incomplete files
   find . -name "*.tmp" -delete
   ```

4. **Contact support with:**
   - Upgrade log file (.devforgeai/logs/upgrade-*.log)
   - Current version (cat .devforgeai/.version.json)
   - Source version you attempted to upgrade from

---

### Error: "Backup restoration failed"

**Message:**
```
ERROR: Backup restoration failed
Could not restore file: .claude/agents/test-automator.md
Reason: Permission denied
```

**Cause:**
- Cannot write files to restore locations
- File permissions issue or read-only filesystem

**Solution:**

1. **Check filesystem read/write permissions:**
   ```bash
   # Test write permission in target directory
   touch .devforgeai/test-write.tmp && rm .devforgeai/test-write.tmp
   if [ $? -ne 0 ]; then
       echo "Write permission denied!"
   fi
   ```

2. **Fix directory permissions:**
   ```bash
   # Make directories writable
   chmod -R u+w .devforgeai/
   chmod -R u+w .claude/
   chmod -R u+w .ai_docs/
   ```

3. **Check for running processes:**
   ```bash
   # Ensure no processes holding locks on files
   lsof 2>/dev/null | grep "\.devforgeai\|\.claude" | awk '{print $2}' | sort | uniq
   ```

4. **Retry restoration:**
   ```bash
   bash install.sh restore .devforgeai/backups/vX.Y.Z-{timestamp}/
   ```

---

### Error: "Version metadata corrupted"

**Message:**
```
ERROR: Cannot parse .devforgeai/.version.json
JSON decode error at line 5
```

**Cause:**
- Version metadata file corrupted or incomplete
- Unexpected shutdown during upgrade

**Solution:**

1. **Backup corrupted file:**
   ```bash
   cp .devforgeai/.version.json .devforgeai/.version.json.corrupted
   ```

2. **Restore from backup metadata:**
   ```bash
   # Extract version info from backup manifest
   cat .devforgeai/backups/vX.Y.Z-{timestamp}/backup-manifest.json | jq '.version'
   ```

3. **Recreate version file:**
   ```bash
   cat > .devforgeai/.version.json <<'EOF'
   {
     "version": "X.Y.Z",
     "installed_at": "2025-01-01T00:00:00Z",
     "upgraded_from": "A.B.C",
     "upgrade_timestamp": "2025-01-01T00:00:00Z",
     "migrations_applied": []
   }
   EOF
   ```

4. **Verify file is valid JSON:**
   ```bash
   python3 -m json.tool .devforgeai/.version.json > /dev/null && echo "Valid JSON"
   ```

---

## Upgrade Process Hangs

### Symptoms

- Installation appears stuck with no progress
- Last log message is 5+ minutes old
- Process still running (check `ps aux`)

### Diagnosis

```bash
# Check if process still running
ps aux | grep install
ps aux | grep upgrade

# Check last log update time
stat .devforgeai/logs/upgrade-*.log | grep Modify

# Monitor system resources
top -b -n 1 | head -20
```

### Solutions

#### Solution 1: Network Timeout (if downloading files)

**If upgrade downloads new files:**

```bash
# Check network connectivity
ping -c 3 github.com

# Increase network timeout
timeout 600 bash install.sh upgrade
```

#### Solution 2: Disk I/O Bottleneck

**If backup/restore is slow with large files:**

```bash
# Check disk performance
iostat -x 1 5

# Monitor backup progress
du -sh .devforgeai/backups/*/
```

**Fix:**
- Let backup complete (can take time for large installations)
- Monitor disk usage to ensure progress continues
- If stuck >5 minutes with no disk activity, restart

#### Solution 3: Migration Script Infinite Loop

**If migration script appears stuck:**

```bash
# Kill stuck process (last resort)
pkill -f "upgrade"

# Check what was executing
tail -20 .devforgeai/logs/upgrade-*.log

# Restore from backup
bash install.sh restore latest
```

## Backup Restoration Procedures

### Manual Restore to Specific Backup

```bash
# List available backups
ls -lh .devforgeai/backups/

# Get backup timestamp you want to restore
# Format: vX.Y.Z-YYYYMMDD-HHMMSS

# Restore specific backup
bash install.sh restore .devforgeai/backups/v1.0.0-20250101-120000/
```

### Verify Backup Before Restoring

```bash
# Check backup manifest
BACKUP_DIR=".devforgeai/backups/v1.0.0-20250101-120000"

# Verify manifest exists and is valid JSON
python3 -m json.tool "$BACKUP_DIR/backup-manifest.json" > /dev/null

# Check backup size
du -sh "$BACKUP_DIR"

# List files in backup (first 20)
ls -la "$BACKUP_DIR" | head -20
```

### Restore Individual Files from Backup

```bash
# If you only need to restore specific files

BACKUP_DIR=".devforgeai/backups/v1.0.0-20250101-120000"

# Restore single file
cp "$BACKUP_DIR/.claude/agents/test-automator.md" ".claude/agents/test-automator.md"

# Restore directory
cp -r "$BACKUP_DIR/devforgeai/context" "devforgeai/context"
```

## Manual Rollback Steps

Use this if automatic rollback didn't work or you need manual control:

### Step 1: Identify Most Recent Backup

```bash
# List backups with details
ls -lth .devforgeai/backups/ | head -5

# Use most recent (first in list)
BACKUP_ID="v1.0.0-20250101-120000"
```

### Step 2: Stop Any Running Processes

```bash
# Kill any upgrade/installation processes
pkill -f install.sh
pkill -f upgrade
pkill -f migration

# Wait 5 seconds
sleep 5

# Verify no processes running
ps aux | grep -E "install|upgrade|migration" | grep -v grep
```

### Step 3: Backup Current State (for debugging)

```bash
# Create debug snapshot before rollback
DEBUG_DIR=".devforgeai/rollback-debug-$(date +%s)"
mkdir -p "$DEBUG_DIR"

# Copy current state for investigation
cp .devforgeai/.version.json "$DEBUG_DIR/"
cp .devforgeai/logs/upgrade-*.log "$DEBUG_DIR/" 2>/dev/null

echo "Debug files saved to: $DEBUG_DIR"
```

### Step 4: Restore from Backup

```bash
BACKUP_DIR=".devforgeai/backups/$BACKUP_ID"

# Restore all DevForgeAI files
cp -r "$BACKUP_DIR/.devforgeai"/* ".devforgeai/"
cp -r "$BACKUP_DIR/.claude"/* ".claude/"
[ -f "$BACKUP_DIR/CLAUDE.md" ] && cp "$BACKUP_DIR/CLAUDE.md" "CLAUDE.md"

echo "Restoration complete"
```

### Step 5: Verify Restoration

```bash
# Check version restored to correct version
cat .devforgeai/.version.json

# Verify key files exist
[ -f ".devforgeai/.version.json" ] && echo "✓ Version file present"
[ -d ".claude/" ] && echo "✓ .claude directory present"
[ -d ".devforgeai/" ] && echo "✓ .devforgeai directory present"

# Git status should show no unexpected changes
git status
```

## Interpreting Log Files

### Log Location

```bash
# Upgrade logs stored here
ls -lh .devforgeai/logs/upgrade-*.log

# View recent upgrade log
tail -100 .devforgeai/logs/upgrade-$(ls -t .devforgeai/logs/upgrade-*.log | head -1 | xargs basename | sed 's/upgrade-//').log
```

### Log Format

```
2025-01-01T12:00:00Z [INFO] Starting upgrade from v1.0.0 to v1.1.0
2025-01-01T12:00:01Z [INFO] Creating backup...
2025-01-01T12:00:15Z [INFO] Backup created: .devforgeai/backups/v1.0.0-20250101-120000/
2025-01-01T12:00:16Z [INFO] Running migration: migrations/v1.0.0-to-v1.1.0.py
2025-01-01T12:00:20Z [INFO] Migration completed successfully
2025-01-01T12:00:21Z [INFO] Validating migration...
2025-01-01T12:00:25Z [ERROR] Validation failed: Expected file not found
2025-01-01T12:00:25Z [INFO] Triggering rollback...
2025-01-01T12:00:35Z [INFO] Rollback completed
2025-01-01T12:00:35Z [INFO] Upgrade failed
```

### Key Log Sections

**Success markers:**
```
[INFO] Upgrade completed successfully
[INFO] Version metadata updated to X.Y.Z
```

**Failure markers:**
```
[ERROR] Migration failed
[ERROR] Validation failed
[ERROR] Backup creation failed
```

**Recovery markers:**
```
[INFO] Triggering rollback
[INFO] Rollback completed successfully
```

### Searching Logs

```bash
# Find error messages
grep ERROR .devforgeai/logs/upgrade-*.log

# Find specific migration output
grep "migration/v1.0.0" .devforgeai/logs/upgrade-*.log

# Find lines around error (context)
grep -A 5 -B 5 ERROR .devforgeai/logs/upgrade-*.log

# Count errors
grep -c ERROR .devforgeai/logs/upgrade-*.log
```

## Data Loss Prevention

### Backup Verification

Before deleting old backups:

```bash
# Verify backup integrity
BACKUP_DIR=".devforgeai/backups/v1.0.0-20250101-120000"

# 1. Check manifest exists and is valid JSON
python3 -c "import json; json.load(open('$BACKUP_DIR/backup-manifest.json'))" && echo "✓ Manifest valid"

# 2. Verify file count
EXPECTED_FILES=$(python3 -c "import json; m = json.load(open('$BACKUP_DIR/backup-manifest.json')); print(len(m.get('files', [])))")
ACTUAL_FILES=$(find "$BACKUP_DIR" -type f | wc -l)
echo "Expected files: $EXPECTED_FILES, Actual files: $ACTUAL_FILES"

# 3. Check backup size reasonable
du -sh "$BACKUP_DIR"
```

### Pre-Upgrade Checklist

Before starting upgrade:

```bash
# Check current version
echo "Current version:"
cat .devforgeai/.version.json | python3 -m json.tool

# Verify upgrade path is valid
echo "Source package version:"
cat VERSION.txt  # or similar in package being installed

# Ensure sufficient disk space
echo "Disk space available:"
df -h .

# Backup user data outside DevForgeAI
cp -r .ai_docs/ .ai_docs.backup-$(date +%s)/
```

### Post-Upgrade Verification

After upgrade completes:

```bash
# Verify version updated
cat .devforgeai/.version.json

# Check all key files present
ls -la devforgeai/context/
ls -la .claude/skills/
ls -la .ai_docs/

# Quick sanity check: try running a command
# (this depends on your framework)
python3 -c "import os; os.path.exists('.devforgeai')" && echo "✓ Framework accessible"
```

## When to Contact Support

### Provide This Information

If you need support, gather this information first:

```bash
# 1. Version information
cat .devforgeai/.version.json

# 2. Full upgrade log
cat .devforgeai/logs/upgrade-*.log

# 3. System information
uname -a
df -h

# 4. List of backups
ls -lh .devforgeai/backups/

# 5. Git status
git status
git log --oneline -10

# Export to file for sharing
{
  echo "=== Version Info ==="
  cat .devforgeai/.version.json
  echo ""
  echo "=== Recent Logs ==="
  tail -100 .devforgeai/logs/upgrade-*.log
  echo ""
  echo "=== System Info ==="
  uname -a
  df -h
  echo ""
  echo "=== Backups ==="
  ls -lh .devforgeai/backups/
} > upgrade-diagnostics.txt

echo "Diagnostics saved to: upgrade-diagnostics.txt"
```

### Support Channels

- **GitHub Issues:** Report upgrade bugs
- **Documentation:** Check troubleshooting guide (this file)
- **Logs:** Always include upgrade logs
- **Backup:** Ensure backup available for investigation

## FAQ

### Q: Can I cancel an upgrade in progress?

**A:** Yes, but with caution:
```bash
# Send interrupt signal
Ctrl+C

# Check if process stopped
ps aux | grep upgrade

# If still running
pkill -f install.sh

# Automatic rollback should trigger
# If not, manually restore from backup
```

### Q: Will upgrading delete my stories?

**A:** No. User data in `.ai_docs/` is never modified by upgrades. Only DevForgeAI framework files are updated.

### Q: How long should an upgrade take?

**A:**
- Small upgrade (patch): 1-2 minutes
- Medium upgrade (minor): 2-5 minutes
- Large upgrade (major with migrations): 5-15 minutes

If taking >30 minutes, check logs or interrupt and restore.

### Q: Can I upgrade multiple versions at once?

**A:** Yes. Upgrade scripts handle multi-version upgrades by running intermediate migrations:
```
v1.0.0 → v1.2.0 runs: v1.0→v1.1, then v1.1→v1.2
```

### Q: What if backup is corrupted?

**A:** You still have the original installation. Restart from current state. Corrupted backups are replaced on next successful upgrade.

### Q: How often should I clean up old backups?

**A:** By default, 5 backups are retained. Cleanup happens automatically when limit exceeded. To manual cleanup:
```bash
# Keep only most recent backup
ls -t .devforgeai/backups/ | tail -n +2 | xargs -I {} rm -rf ".devforgeai/backups/{}"
```

## Related Documentation

- [Backup Management Guide](backup-management.md)
- [Migration Script Authoring Guide](migration-script-authoring.md)
- [STORY-078: Upgrade Mode with Migration Scripts](../../devforgeai/specs/Stories/STORY-078-upgrade-mode-migration-scripts.story.md)
