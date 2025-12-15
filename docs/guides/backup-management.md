# Backup Management Guide

## Overview

This guide explains how to manage DevForgeAI backups. Backups are created automatically before upgrades and can also be created manually for disaster recovery.

## Backup Locations

### Automatic Backup Storage

```
.devforgeai/backups/
├── vX.Y.Z-YYYYMMDD-HHMMSS/
│   ├── backup-manifest.json
│   ├── .claude/
│   ├── .devforgeai/
│   ├── CLAUDE.md
│   └── ...
├── vA.B.C-YYYYMMDD-HHMMSS/
│   ├── backup-manifest.json
│   ├── .claude/
│   ├── .devforgeai/
│   └── ...
```

### Backup Directory Naming

Format: `v{VERSION}-{TIMESTAMP}`

**Components:**
- `v{VERSION}`: Version being backed up (e.g., v1.0.0)
- `{TIMESTAMP}`: Creation timestamp (YYYYMMDD-HHMMSS)

**Example:** `v1.0.0-20250101-120000` = Version 1.0.0 backed up on January 1, 2025 at 12:00:00

### What's Included in Backups

**Files included:**
- `.claude/` - All agents and skills
- `.devforgeai/` - Configuration and metadata (except logs)
- `CLAUDE.md` - Project instructions
- `.version.json` - Version metadata

**Files NOT included:**
- `.ai_docs/` - User stories and documentation (user content)
- `.git/` - Git history (use git for version control)
- `node_modules/`, `__pycache__/` - Build artifacts
- `.env` files - Secrets (stored elsewhere)

**Why user content excluded:**
- User files not modified by upgrades
- Reduces backup size significantly
- User content preserved even if upgrade fails

## Backup Retention Policy

### Default Configuration

```json
{
  "backup_retention_count": 5,
  "backup_max_age_days": 90
}
```

**Defaults:**
- Keep last **5 backups** by default
- Delete backups older than **90 days**
- Oldest backups deleted first when limit exceeded

### Retention Behavior

**Scenario: You have 5 backups, upgrade creates new one:**

```
Before upgrade:
  .devforgeai/backups/
  ├── v1.0.0-20241201-100000/
  ├── v1.0.0-20241215-100000/
  ├── v1.0.1-20241220-100000/
  ├── v1.0.1-20241227-100000/
  └── v1.0.2-20250101-100000/

After upgrade (new backup created):
  .devforgeai/backups/
  ├── v1.0.0-20241215-100000/  ← oldest deleted
  ├── v1.0.1-20241220-100000/
  ├── v1.0.1-20241227-100000/
  ├── v1.0.2-20250101-100000/
  └── v1.0.2-20250105-100000/  ← new backup
```

## Backup Manifest

### Manifest Structure

Each backup includes a `backup-manifest.json` file:

```json
{
  "backup_id": "v1.0.0-20250101-120000",
  "version": "1.0.0",
  "created_at": "2025-01-01T12:00:00Z",
  "backup_reason": "UPGRADE",
  "size_bytes": 15728640,
  "file_count": 247,
  "files": [
    {
      "path": ".claude/skills/devforgeai-development/SKILL.md",
      "size_bytes": 45678,
      "checksum_sha256": "abc123def456..."
    },
    {
      "path": ".devforgeai/context/tech-stack.md",
      "size_bytes": 8901,
      "checksum_sha256": "xyz789uvw012..."
    }
  ],
  "backup_status": "SUCCESS"
}
```

### Manifest Fields

| Field | Type | Description |
|-------|------|-------------|
| `backup_id` | String | Unique backup identifier |
| `version` | String | Version that was backed up (semver) |
| `created_at` | ISO 8601 | When backup was created |
| `backup_reason` | Enum | UPGRADE, UNINSTALL, MANUAL |
| `size_bytes` | Integer | Total backup size in bytes |
| `file_count` | Integer | Number of files in backup |
| `files` | Array | List of files with checksums |
| `backup_status` | Enum | SUCCESS, FAILED, INCOMPLETE |

## Automatic Backups

### When Created

Backups are automatically created:

1. **Before Upgrades:**
   - Triggered by `bash install.sh upgrade`
   - Created before any changes made

2. **Before Uninstalls:**
   - Triggered by `bash install.sh uninstall`
   - Allows recovery if uninstall was accidental

### Viewing Automatic Backups

```bash
# List all backups
ls -lh .devforgeai/backups/

# List with sorting by date (newest first)
ls -lht .devforgeai/backups/

# Show backup sizes
du -sh .devforgeai/backups/*/

# Show total backup storage used
du -sh .devforgeai/backups/
```

### Understanding Backup Output

```bash
$ ls -lht .devforgeai/backups/

total 125
drwxr-xr-x 5 user group 4096 Jan  5 12:00 v1.0.2-20250105-120000
drwxr-xr-x 5 user group 4096 Jan  01 12:00 v1.0.2-20250101-100000
drwxr-xr-x 5 user group 4096 Dec 27 15:30 v1.0.1-20241227-153000
drwxr-xr-x 5 user group 4096 Dec 20 09:15 v1.0.1-20241220-091500
drwxr-xr-x 5 user group 4096 Dec 15 14:45 v1.0.0-20241215-144500
```

Newest backup is `v1.0.2-20250105-120000` (top of list).

## Manual Backup Creation

### Create Manual Backup

```bash
# Create backup with custom label
bash install.sh backup-create "pre-major-refactoring"
```

### Manual Backup Example

```bash
# Backup before making major changes
cd /path/to/DevForgeAI

# Create backup
bash install.sh backup-create "before-ai-docs-cleanup"

# Output:
# Backup created: .devforgeai/backups/v1.0.2-20250105-120030/
# Size: 45 MB
# Ready for restore if needed
```

## Restoring from Backup

### List Available Backups

```bash
# Show all backups with version and date
for backup in .devforgeai/backups/*/; do
    version=$(basename "$backup")
    size=$(du -sh "$backup" | cut -f1)
    echo "$version ($size)"
done

# Output:
# v1.0.2-20250105-120000 (45M)
# v1.0.2-20250101-100000 (44M)
# v1.0.1-20241227-153000 (42M)
# v1.0.1-20241220-091500 (41M)
# v1.0.0-20241215-144500 (40M)
```

### Restore to Latest Backup

```bash
# Restore most recent backup
bash install.sh restore latest

# Output:
# Restoring from: .devforgeai/backups/v1.0.2-20250105-120000/
# Restoring files...
# Restoration complete
# Version restored to: v1.0.2
```

### Restore to Specific Backup

```bash
# Restore specific backup by version
backup_id="v1.0.1-20241227-153000"
backup_path=".devforgeai/backups/$backup_id"

bash install.sh restore "$backup_path"

# Output:
# Restoring from: .devforgeai/backups/v1.0.1-20241227-153000/
# Restoring files...
# Restoration complete
# Version restored to: v1.0.1
```

### Restore Single File from Backup

```bash
# Restore specific file from backup
backup_id="v1.0.1-20241227-153000"
source_file=".claude/skills/devforgeai-development/SKILL.md"
destination=".claude/skills/devforgeai-development/SKILL.md"

# Restore single file
cp ".devforgeai/backups/$backup_id/$source_file" "$destination"

# Verify restoration
cat "$destination" | head -5
```

### Restore Entire Directory from Backup

```bash
# Restore entire .claude directory
backup_id="v1.0.1-20241227-153000"

cp -r ".devforgeai/backups/$backup_id/.claude/"* ".claude/"

# Verify restoration
ls -la .claude/
```

## Backup Verification

### Verify Backup Integrity

```bash
# 1. Check manifest is valid JSON
python3 -m json.tool .devforgeai/backups/v1.0.0-20250101-120000/backup-manifest.json > /dev/null
echo $? -eq 0 && echo "✓ Manifest valid"

# 2. Check file count
manifest=".devforgeai/backups/v1.0.0-20250101-120000/backup-manifest.json"
expected_count=$(python3 -c "import json; print(len(json.load(open('$manifest')).get('files', [])))")
actual_count=$(find ".devforgeai/backups/v1.0.0-20250101-120000" -type f ! -name 'backup-manifest.json' | wc -l)
echo "Files: $expected_count expected, $actual_count actual"

# 3. Verify backup size reasonable
du -sh .devforgeai/backups/v1.0.0-20250101-120000/
```

### Verify File Checksums

```bash
# Extract checksums from manifest
manifest=".devforgeai/backups/v1.0.0-20250101-120000/backup-manifest.json"
backup_dir=".devforgeai/backups/v1.0.0-20250101-120000"

# Create checksum file
python3 << 'PYTHON'
import json
with open("$manifest") as f:
    data = json.load(f)
    for file_entry in data['files']:
        path = file_entry['path']
        checksum = file_entry['checksum_sha256']
        print(f"{checksum}  {path}")
PYTHON > /tmp/checksums.txt

# Verify checksums
cd "$backup_dir"
sha256sum -c /tmp/checksums.txt

cd -
```

### Test Restoration (Safety Check)

Before relying on a backup for critical recovery:

```bash
# Create test directory
test_dir=$(mktemp -d)
echo "Testing backup restoration to: $test_dir"

# Copy backup to test location
cp -r .devforgeai/backups/v1.0.0-20250101-120000 "$test_dir/test-restore"

# Verify files copied
ls -la "$test_dir/test-restore/.claude/" | head -10

# Check file count
find "$test_dir/test-restore" -type f | wc -l

# Clean up
rm -rf "$test_dir"
echo "Backup test complete"
```

## Backup Cleanup

### Manual Cleanup - Remove Old Backups

```bash
# List backups (oldest first)
ls -lt .devforgeai/backups/ | tail -10

# Remove specific backup
backup_id="v1.0.0-20241215-144500"
rm -rf ".devforgeai/backups/$backup_id"
echo "Deleted: $backup_id"

# Verify deletion
ls .devforgeai/backups/
```

### Cleanup - Keep Only Recent Backups

```bash
# Keep only 3 most recent backups
# (by default 5 are kept)

backup_count=3
cd .devforgeai/backups/

# Sort by modification time, keep N newest
ls -t | tail -n +$((backup_count+1)) | xargs -r rm -rf

echo "Kept $backup_count most recent backups"
ls -lh
cd -
```

### Cleanup - Remove Backups Older Than Date

```bash
# Remove backups older than 30 days

days_old=30
cutoff_timestamp=$(date -d "$days_old days ago" +%s)

for backup_dir in .devforgeai/backups/*/; do
    backup_date=$(stat "$backup_dir" | grep Modify | awk '{print $2, $3}' | xargs -I {} date -d "{}" +%s)
    if [ "$backup_date" -lt "$cutoff_timestamp" ]; then
        echo "Removing old backup: $(basename $backup_dir)"
        rm -rf "$backup_dir"
    fi
done
```

### Cleanup - Free Disk Space

```bash
# Check current backup storage
echo "Current backup storage:"
du -sh .devforgeai/backups/

# Remove all but most recent backup
cd .devforgeai/backups/
ls -t | tail -n +2 | xargs -r rm -rf
echo "Cleanup complete"
du -sh .
cd -
```

## Storage Requirements

### Backup Size Estimates

| Installation Type | Typical Size | With 5 Backups |
|-------------------|--------------|----------------|
| Minimal | 10-15 MB | 50-75 MB |
| Standard | 30-50 MB | 150-250 MB |
| Large (100+ stories) | 100-200 MB | 500-1000 MB |

### Disk Space Recommendations

- **Before upgrade:** Ensure 2x backup size free (backup + extraction space)
- **Regular operation:** Keep 500 MB free for backups
- **Large installations:** Monitor backup directory, clean up periodically

### Check Available Disk Space

```bash
# Check partition containing .devforgeai
df -h .devforgeai

# Output:
# Filesystem      Size  Used Avail Use% Mounted on
# /dev/sda1       100G   45G   55G  45% /

# Calculate safe upgrade margin
total_free_mb=$(($(df .devforgeai | tail -1 | awk '{print $4}')))
current_backups_mb=$(($(du -s .devforgeai/backups | awk '{print $1}') / 1024))

echo "Free space: ${total_free_mb}MB"
echo "Current backups: ${current_backups_mb}MB"
echo "Safe to upgrade if free > $((current_backups_mb * 3))MB"
```

## Backup Recovery Scenarios

### Scenario 1: Accidental File Deletion

**Problem:** You accidentally deleted `.claude/agents/test-automator.md`

**Solution:**

```bash
# Find backup containing the file
for backup_dir in .devforgeai/backups/*/; do
    if [ -f "$backup_dir/.claude/agents/test-automator.md" ]; then
        echo "Found in: $backup_dir"
        # Restore it
        cp "$backup_dir/.claude/agents/test-automator.md" ".claude/agents/test-automator.md"
        break
    fi
done
```

### Scenario 2: Failed Upgrade (Automatic Rollback)

**Problem:** Upgrade failed and automatic rollback didn't complete

**Solution:**

```bash
# Find backup from before failed upgrade
echo "Backup created before upgrade:"
ls -t .devforgeai/backups/ | head -1

# Manually restore
latest_backup=$(ls -t .devforgeai/backups/ | head -1)
bash install.sh restore ".devforgeai/backups/$latest_backup/"

# Verify restoration
cat .devforgeai/.version.json
```

### Scenario 3: Configuration Corruption

**Problem:** `.devforgeai/config/upgrade-config.json` corrupted

**Solution:**

```bash
# Find most recent backup with valid config
for backup_dir in .devforgeai/backups/*/; do
    config_file="$backup_dir/.devforgeai/config/upgrade-config.json"
    if [ -f "$config_file" ]; then
        # Validate JSON
        python3 -m json.tool "$config_file" > /dev/null 2>&1
        if [ $? -eq 0 ]; then
            echo "Found valid config in: $backup_dir"
            cp "$config_file" ".devforgeai/config/upgrade-config.json"
            break
        fi
    fi
done
```

### Scenario 4: Disk Full - Need to Free Space

**Problem:** Disk full, cannot create new backup, need free space

**Solution:**

```bash
# Check current usage
du -sh .devforgeai/backups/

# Remove old backups (keep 2 most recent)
cd .devforgeai/backups/
ls -t | tail -n +3 | xargs -r rm -rf
echo "Old backups removed"

# Verify freed space
df -h .
```

## Backup Automation

### Automated Backup Schedule (Linux Cron)

```bash
# Edit crontab
crontab -e

# Add weekly backup (Sundays at 2 AM)
0 2 * * 0 cd /path/to/DevForgeAI && bash install.sh backup-create "weekly-backup"

# Add daily backup (disabled by default)
# 0 2 * * * cd /path/to/DevForgeAI && bash install.sh backup-create "daily-backup"
```

### Automated Backup Cleanup

```bash
# Add to crontab to run monthly
# Cleanup old backups, keep only 5 most recent

0 3 1 * * \
  cd /path/to/DevForgeAI && \
  cd .devforgeai/backups && \
  ls -t | tail -n +6 | xargs -r rm -rf
```

## Backup Best Practices

### 1. **Verify Before Relying**
Always test critical backups:
```bash
# Spot check: Can manifest be read?
python3 -m json.tool .devforgeai/backups/*/backup-manifest.json > /dev/null
```

### 2. **Monitor Backup Growth**
```bash
# Monthly check
du -sh .devforgeai/backups/ >> .devforgeai/logs/backup-monitoring.log
```

### 3. **Keep Important Backups**
```bash
# Don't delete backups of major upgrades
# Archive separately if needed
mkdir -p ~/.backups/devforgeai
cp -r .devforgeai/backups/v1.0.0* ~/.backups/devforgeai/
```

### 4. **Test Restoration Procedures**
```bash
# Periodically test that backups actually restore
test_dir=$(mktemp -d)
cp -r .devforgeai/backups/v1.0.0-*/ "$test_dir/" && echo "✓ Backup copyable"
```

### 5. **Document Backup Policy**
Keep note of your backup approach:
```bash
cat > .devforgeai/BACKUP-POLICY.txt <<'EOF'
- Automatic backups: 5 most recent retained
- Manual backups: None created (auto-backup sufficient)
- Retention: 90 days max age
- Tested: 2025-01-05
- Last cleanup: 2025-01-05 (freed 200MB)
EOF
```

## Related Documentation

- [Migration Script Authoring Guide](migration-script-authoring.md)
- [Upgrade Troubleshooting Guide](upgrade-troubleshooting.md)
- [STORY-078: Upgrade Mode with Migration Scripts](../../devforgeai/specs/Stories/STORY-078-upgrade-mode-migration-scripts.story.md)

## Command Reference

### Quick Reference Table

| Task | Command |
|------|---------|
| List backups | `ls -lht .devforgeai/backups/` |
| Backup size | `du -sh .devforgeai/backups/` |
| Create manual backup | `bash install.sh backup-create "label"` |
| Restore latest | `bash install.sh restore latest` |
| Restore specific | `bash install.sh restore .devforgeai/backups/v1.0.0-*` |
| Check manifest | `python3 -m json.tool .devforgeai/backups/*/backup-manifest.json` |
| Verify checksums | See "Verify File Checksums" section |
| Cleanup old backups | `cd .devforgeai/backups && ls -t \| tail -n +6 \| xargs -r rm -rf` |
| Monitor free space | `df -h .` |

## Frequently Asked Questions

### Q: Where are backups stored?

**A:** In `.devforgeai/backups/` directory next to your DevForgeAI installation. Each backup is in its own timestamped directory.

### Q: How much disk space do backups use?

**A:** Depends on installation size. Typical: 30-50 MB per backup. With 5 backups: 150-250 MB total.

### Q: Can I move backups to external drive?

**A:** Yes, but restoration requires backups in `.devforgeai/backups/`. For long-term archival:
```bash
cp -r .devforgeai/backups/v1.0.0-* /external/archive/
```

### Q: What if backup is incomplete?

**A:** Automatic rollback handles this. Manual check:
```bash
backup_status=$(python3 -c "import json; print(json.load(open('.devforgeai/backups/*/backup-manifest.json')).get('backup_status'))")
[ "$backup_status" != "SUCCESS" ] && echo "⚠ Backup incomplete"
```

### Q: Are user stories backed up?

**A:** No. User files (`.ai_docs/`) are never modified by upgrades and not included in backups. This is by design to reduce backup size.

### Q: Can I encrypt backups?

**A:** Not built-in. For sensitive data:
```bash
# Manual encryption (7-Zip with AES-256)
7z a -t7z -p -mhe=on backup.7z .devforgeai/backups/
```

### Q: How do I know if backup is working?

**A:** Check after upgrade:
1. `ls .devforgeai/backups/` shows new backup
2. Backup manifest valid: `python3 -m json.tool .devforgeai/backups/*/backup-manifest.json`
3. File count matches: `find .devforgeai/backups/v*/ -type f | wc -l`
