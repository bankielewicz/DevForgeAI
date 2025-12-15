# Backup Management Guide

Managing DevForgeAI backups for safe upgrades and rollback capabilities.

---

## Overview

DevForgeAI creates backups automatically during:
- Upgrades (before any changes)
- Uninstalls (before removal)
- Manual backup requests

Backups enable instant rollback if something goes wrong.

---

## Backup Location

```
devforgeai/backups/
├── v1.0.0-20251206120000/     # Backup from v1.0.0, timestamp
│   ├── .claude/               # Claude directory backup
│   ├── devforgeai/           # DevForgeAI directory backup
│   ├── CLAUDE.md              # CLAUDE.md backup
│   └── manifest.json          # Backup metadata
├── v1.1.0-20251206130000/     # Another backup
└── ...
```

---

## Backup Contents

Each backup includes:

| Directory/File | Description |
|----------------|-------------|
| `.claude/` | Skills, commands, agents, settings |
| `devforgeai/` | Context files, config, specs, ADRs |
| `CLAUDE.md` | Project instructions |
| `manifest.json` | Backup metadata and checksums |

### Manifest Structure

```json
{
  "backup_id": "v1.0.0-20251206120000",
  "created_at": "2025-12-06T12:00:00Z",
  "reason": "upgrade",
  "from_version": "1.0.0",
  "to_version": "1.1.0",
  "file_count": 450,
  "total_size_bytes": 5242880,
  "backup_integrity_hash": "sha256:abc123...",
  "files": [
    {
      "path": ".claude/settings.json",
      "size": 1024,
      "checksum": "sha256:..."
    }
  ]
}
```

---

## Listing Backups

### View All Backups

```bash
ls -la devforgeai/backups/
```

Output:
```
drwxr-xr-x  4 user  staff  128 Dec  6 12:00 v1.0.0-20251206120000
drwxr-xr-x  4 user  staff  128 Dec  6 13:00 v1.1.0-20251206130000
drwxr-xr-x  4 user  staff  128 Dec  6 14:00 v1.2.0-20251206140000
```

### View Backup Details

```bash
cat devforgeai/backups/v1.0.0-20251206120000/manifest.json | python3 -m json.tool
```

### Count Backups

```bash
ls -d devforgeai/backups/*/ | wc -l
```

---

## Restoring from Backup

### Using DevForgeAI CLI

```bash
# Restore from most recent backup
devforgeai rollback

# Restore from specific backup
devforgeai rollback --backup=devforgeai/backups/v1.0.0-20251206120000/
```

### Manual Restore

If CLI is unavailable:

```bash
# Choose backup to restore
BACKUP="devforgeai/backups/v1.0.0-20251206120000"

# Verify backup integrity
python3 -c "
import json
from pathlib import Path
manifest = json.loads(Path('$BACKUP/manifest.json').read_text())
print(f'Backup: {manifest[\"backup_id\"]}')
print(f'Files: {manifest[\"file_count\"]}')
print(f'Created: {manifest[\"created_at\"]}')
"

# Remove current installation
rm -rf .devforgeai .claude CLAUDE.md

# Restore from backup
cp -r "$BACKUP/.devforgeai" .
cp -r "$BACKUP/.claude" .
cp "$BACKUP/CLAUDE.md" .

# Verify restoration
cat devforgeai/.version.json
```

---

## Creating Manual Backups

### Before Major Changes

```bash
# Create timestamped backup directory
BACKUP_DIR="devforgeai/backups/manual-$(date +%Y%m%d%H%M%S)"
mkdir -p "$BACKUP_DIR"

# Copy files
cp -r .claude "$BACKUP_DIR/"
cp -r .devforgeai "$BACKUP_DIR/"
cp CLAUDE.md "$BACKUP_DIR/" 2>/dev/null || true

# Create manifest
python3 << 'EOF'
import json
from pathlib import Path
from datetime import datetime
import hashlib

backup_dir = Path("$BACKUP_DIR")
files = []
total_size = 0

for f in backup_dir.rglob("*"):
    if f.is_file() and f.name != "manifest.json":
        size = f.stat().st_size
        total_size += size
        files.append({
            "path": str(f.relative_to(backup_dir)),
            "size": size
        })

manifest = {
    "backup_id": backup_dir.name,
    "created_at": datetime.utcnow().isoformat() + "Z",
    "reason": "manual",
    "file_count": len(files),
    "total_size_bytes": total_size,
    "files": files
}

(backup_dir / "manifest.json").write_text(json.dumps(manifest, indent=2))
print(f"Backup created: {backup_dir}")
print(f"Files: {len(files)}, Size: {total_size / 1024 / 1024:.2f} MB")
EOF
```

---

## Cleaning Old Backups

### Retention Policy

Default retention: **5 most recent backups**

### Manual Cleanup

```bash
# Keep only last 5 backups
ls -td devforgeai/backups/*/ | tail -n +6 | xargs rm -rf

# Keep only backups from last 30 days
find devforgeai/backups -maxdepth 1 -type d -mtime +30 -exec rm -rf {} \;

# Remove specific backup
rm -rf devforgeai/backups/v1.0.0-20251206120000/
```

### Check Backup Sizes

```bash
# Total backup storage used
du -sh devforgeai/backups/

# Size per backup
du -sh devforgeai/backups/*/
```

---

## Verifying Backup Integrity

### Check Manifest

```bash
# Verify manifest exists and is valid JSON
python3 -c "
import json
from pathlib import Path
for backup in Path('devforgeai/backups').iterdir():
    manifest_path = backup / 'manifest.json'
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text())
            print(f'✓ {backup.name}: {manifest[\"file_count\"]} files')
        except:
            print(f'✗ {backup.name}: Invalid manifest')
    else:
        print(f'✗ {backup.name}: No manifest')
"
```

### Verify File Counts

```bash
# Compare manifest file count to actual files
BACKUP="devforgeai/backups/v1.0.0-20251206120000"
MANIFEST_COUNT=$(python3 -c "import json; print(json.loads(open('$BACKUP/manifest.json').read())['file_count'])")
ACTUAL_COUNT=$(find "$BACKUP" -type f ! -name "manifest.json" | wc -l)

if [ "$MANIFEST_COUNT" -eq "$ACTUAL_COUNT" ]; then
    echo "✓ File count matches: $ACTUAL_COUNT files"
else
    echo "✗ Mismatch: manifest=$MANIFEST_COUNT, actual=$ACTUAL_COUNT"
fi
```

### Full Integrity Check

```bash
# Verify checksums (if stored in manifest)
python3 << 'EOF'
import json
import hashlib
from pathlib import Path

backup = Path("devforgeai/backups/v1.0.0-20251206120000")
manifest = json.loads((backup / "manifest.json").read_text())

errors = 0
for file_info in manifest.get("files", []):
    file_path = backup / file_info["path"]
    if not file_path.exists():
        print(f"✗ Missing: {file_info['path']}")
        errors += 1
    elif "checksum" in file_info:
        actual = hashlib.sha256(file_path.read_bytes()).hexdigest()
        expected = file_info["checksum"].replace("sha256:", "")
        if actual != expected:
            print(f"✗ Checksum mismatch: {file_info['path']}")
            errors += 1

if errors == 0:
    print(f"✓ All {len(manifest.get('files', []))} files verified")
else:
    print(f"✗ {errors} errors found")
EOF
```

---

## Backup Best Practices

### 1. Verify Before Upgrade

```bash
# Check most recent backup is valid
ls -la devforgeai/backups/ | tail -1
cat devforgeai/backups/*/manifest.json | head -20
```

### 2. Keep Sufficient Backups

Recommended minimums:
- Development: 3 backups
- Staging: 5 backups
- Production: 10 backups

### 3. Monitor Disk Usage

```bash
# Set up alert for backup directory size
BACKUP_SIZE=$(du -sm devforgeai/backups | cut -f1)
if [ "$BACKUP_SIZE" -gt 500 ]; then
    echo "Warning: Backups exceed 500MB ($BACKUP_SIZE MB)"
fi
```

### 4. External Backup

For critical systems, copy backups externally:

```bash
# Sync to external location
rsync -av devforgeai/backups/ /backup/devforgeai/

# Or archive and upload
tar -czf devforgeai-backups-$(date +%Y%m%d).tar.gz devforgeai/backups/
```

### 5. Test Restores Periodically

```bash
# Test restore in temporary directory
TEMP_DIR=$(mktemp -d)
cp -r devforgeai/backups/v1.0.0-20251206120000/* "$TEMP_DIR/"
# Verify files
ls -la "$TEMP_DIR/"
rm -rf "$TEMP_DIR"
```

---

## Troubleshooting

### Backup Creation Fails

**Disk full:**
```bash
df -h .
# Clean old backups
ls -td devforgeai/backups/*/ | tail -n +3 | xargs rm -rf
```

**Permission denied:**
```bash
chmod -R u+rw devforgeai/backups/
```

### Restore Fails

**Backup corrupted:**
```bash
# Try older backup
ls -t devforgeai/backups/
devforgeai rollback --backup=devforgeai/backups/v0.9.0-20251205120000/
```

**Missing files:**
```bash
# Check what's in backup
find devforgeai/backups/v1.0.0-*/ -type f | head -20
```

---

## Configuration

### Backup Settings

Configure in `devforgeai/config/upgrade-config.json`:

```json
{
  "backup_retention_count": 5,
  "backup_timeout_seconds": 30,
  "include_user_content": false,
  "compression_enabled": false
}
```

| Setting | Default | Description |
|---------|---------|-------------|
| `backup_retention_count` | 5 | Number of backups to keep |
| `backup_timeout_seconds` | 30 | Max time for backup creation |
| `include_user_content` | false | Include devforgeai/specs/ in backups |
| `compression_enabled` | false | Compress backup files |

---

**Version:** 1.0
**Last Updated:** 2025-12-06
**Story:** STORY-078
