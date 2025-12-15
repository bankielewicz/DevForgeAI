# Upgrade Troubleshooting Guide

Diagnose and resolve common DevForgeAI upgrade issues.

---

## Quick Diagnostics

### Check Current Version

```bash
cat devforgeai/.version.json
```

Expected output:
```json
{
  "version": "1.0.0",
  "installed_at": "2025-12-06T12:00:00Z",
  "mode": "fresh_install"
}
```

### Check Upgrade Logs

```bash
ls -la devforgeai/logs/upgrade-*.log
cat devforgeai/logs/upgrade-latest.log
```

### Check Backup Status

```bash
ls -la devforgeai/backups/
```

---

## Common Issues

### 1. Upgrade Fails: "Lock file exists"

**Symptom:**
```
Error: Upgrade already in progress (lock file exists)
```

**Cause:** A previous upgrade was interrupted, leaving a lock file.

**Solution:**
```bash
# Remove lock file (only if no upgrade is running)
rm devforgeai/.upgrade.lock

# Retry upgrade
devforgeai upgrade
```

**Prevention:** Always let upgrades complete. Don't interrupt with Ctrl+C.

---

### 2. Upgrade Fails: "Backup creation failed"

**Symptom:**
```
Error: Backup creation failed: [Errno 28] No space left on device
```

**Cause:** Insufficient disk space for backup.

**Solution:**
```bash
# Check disk space
df -h .

# Clean old backups (keep last 3)
ls -t devforgeai/backups/ | tail -n +4 | xargs -I {} rm -rf devforgeai/backups/{}

# Retry upgrade
devforgeai upgrade
```

**Prevention:** Ensure at least 200MB free space before upgrading.

---

### 3. Migration Script Fails

**Symptom:**
```
Error: Migration v1.0.0-to-v1.1.0 failed: FileNotFoundError
```

**Cause:** Migration script expected a file that doesn't exist.

**Solution:**
```bash
# Check upgrade log for details
cat devforgeai/logs/upgrade-*.log | grep -A5 "Migration failed"

# If rollback succeeded, system is safe
# Check version
cat devforgeai/.version.json
```

**If rollback failed:**
```bash
# List available backups
ls devforgeai/backups/

# Manually restore from backup
devforgeai rollback --backup=devforgeai/backups/v1.0.0-20251206120000/
```

---

### 4. Validation Fails After Migration

**Symptom:**
```
Error: Post-migration validation failed: Missing file devforgeai/config/settings.json
```

**Cause:** Migration didn't create expected files, or files were deleted.

**Solution:**
```bash
# System should auto-rollback
# Verify version reverted
cat devforgeai/.version.json

# If still showing new version, manual rollback needed
devforgeai rollback
```

**Report:** File an issue with the upgrade log attached.

---

### 5. Upgrade Hangs (No Progress)

**Symptom:** Upgrade process shows no progress for >5 minutes.

**Cause:** Migration script stuck in infinite loop or waiting for input.

**Solution:**
```bash
# Check for running processes
ps aux | grep devforgeai

# If upgrade process exists, wait or kill
kill -SIGTERM <pid>

# Check for lock file
ls devforgeai/.upgrade.lock

# If lock exists and no process running, remove it
rm devforgeai/.upgrade.lock
```

**Prevention:** Migration scripts should have timeout handling.

---

### 6. Version Mismatch After Upgrade

**Symptom:**
```
# Expected v1.1.0 but showing v1.0.0
cat devforgeai/.version.json
{"version": "1.0.0", ...}
```

**Cause:** Version file wasn't updated, or rollback occurred silently.

**Solution:**
```bash
# Check upgrade log
cat devforgeai/logs/upgrade-*.log | tail -50

# If rollback occurred, log will show reason
grep -i "rollback" devforgeai/logs/upgrade-*.log
```

---

### 7. Permission Denied Errors

**Symptom:**
```
Error: [Errno 13] Permission denied: 'devforgeai/config/settings.json'
```

**Cause:** File permissions prevent modification.

**Solution:**
```bash
# Check ownership
ls -la devforgeai/

# Fix permissions (if you own the files)
chmod -R u+rw devforgeai/

# Or run with appropriate user
sudo chown -R $(whoami) devforgeai/
```

---

### 8. Corrupted Version File

**Symptom:**
```
Error: Failed to parse version file: JSONDecodeError
```

**Cause:** `.version.json` file is corrupted or malformed.

**Solution:**
```bash
# Check file contents
cat devforgeai/.version.json

# If corrupted, restore from backup
cp devforgeai/backups/latest/devforgeai/.version.json devforgeai/.version.json

# If no backup, recreate manually
cat > devforgeai/.version.json << 'EOF'
{
  "version": "1.0.0",
  "installed_at": "2025-12-06T00:00:00Z",
  "mode": "fresh_install"
}
EOF
```

---

## Rollback Procedures

### Automatic Rollback

The upgrade system automatically rolls back on:
- Migration script failure
- Validation failure
- Any unhandled exception

Check if rollback occurred:
```bash
grep -i "rollback" devforgeai/logs/upgrade-*.log
```

### Manual Rollback

If automatic rollback failed:

```bash
# List backups
ls -la devforgeai/backups/

# Rollback to specific backup
devforgeai rollback --backup=devforgeai/backups/v1.0.0-20251206120000/

# Verify rollback
cat devforgeai/.version.json
```

### Emergency Rollback

If `devforgeai rollback` doesn't work:

```bash
# Find latest backup
BACKUP=$(ls -td devforgeai/backups/* | head -1)

# Manually restore
rm -rf .devforgeai .claude CLAUDE.md
cp -r "$BACKUP/.devforgeai" .
cp -r "$BACKUP/.claude" .
cp "$BACKUP/CLAUDE.md" .

# Verify
cat devforgeai/.version.json
```

---

## Upgrade Logs

### Log Location

```
devforgeai/logs/upgrade-YYYYMMDDHHMMSS.log
```

### Log Contents

Each upgrade log contains:
- Start time and version transition
- Backup creation status
- Migration scripts discovered
- Migration execution results (pass/fail per script)
- Validation results
- Final status (success/failed/rolled_back)
- Duration

### Reading Logs

```bash
# Latest upgrade log
cat devforgeai/logs/$(ls -t devforgeai/logs/upgrade-*.log | head -1)

# Search for errors
grep -i "error\|fail\|exception" devforgeai/logs/upgrade-*.log

# Search for specific migration
grep "v1.0.0-to-v1.1.0" devforgeai/logs/upgrade-*.log
```

---

## Getting Help

### Information to Collect

Before reporting an issue, gather:

1. **Version info:**
   ```bash
   cat devforgeai/.version.json
   ```

2. **Upgrade log:**
   ```bash
   cat devforgeai/logs/upgrade-*.log
   ```

3. **System info:**
   ```bash
   uname -a
   python3 --version
   ```

4. **Backup status:**
   ```bash
   ls -la devforgeai/backups/
   ```

### Reporting Issues

File issues at: https://github.com/anthropics/devforgeai/issues

Include:
- Description of what you tried
- Expected vs actual behavior
- Collected information above
- Steps to reproduce

---

## Prevention Tips

1. **Always backup before upgrading** (automatic, but verify)
2. **Check disk space** (200MB minimum recommended)
3. **Don't interrupt upgrades** (let them complete or rollback)
4. **Review release notes** before major upgrades
5. **Test upgrades in staging** for production systems
6. **Keep backups** (default retention: 5 backups)

---

**Version:** 1.0
**Last Updated:** 2025-12-06
**Story:** STORY-078
