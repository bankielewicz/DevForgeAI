# Feedback File Persistence - Configuration Guide

**Version:** 1.0.0
**Date:** 2025-11-11
**Story:** STORY-013 (Feedback File Persistence with Atomic Writes)

---

## Overview

This guide explains how to configure feedback file persistence behavior in DevForgeAI. Configuration is **optional** - the system works with sensible defaults if no configuration is provided.

---

## Configuration File Location

**Default location:** `.devforgeai/config.yaml`

**Alternative locations (checked in order):**
1. `$DEVFORGEAI_CONFIG` environment variable
2. `.devforgeai/config.yaml` (project root)
3. `~/.devforgeai/config.yaml` (user home)
4. Hardcoded defaults (no configuration file)

---

## Configuration Schema

### Complete Configuration Example

```yaml
feedback:
  persistence:
    # Directory organization strategy
    organization: chronological  # Options: chronological, by-operation, by-status, nested

    # Subdirectory creation (applies if organization != chronological)
    subdirectories:
      by_operation: false  # Create /command/, /skill/, /subagent/, /workflow/
      by_status: false     # Create /success/, /failure/, /partial/, /skipped/

    # File retention policy
    retention:
      enabled: false       # Archive/delete old feedback
      max_age_days: 90     # Delete feedback older than 90 days
      keep_archived: true  # Move to .devforgeai/feedback/archived/ instead of delete

    # Permission settings
    permissions:
      mode: 0600           # Unix file permissions (octal)
      enforce: true        # Fail if permissions cannot be set (strict mode)

    # Base path customization (advanced)
    base_path: .devforgeai  # Root directory for feedback storage
```

---

## Configuration Sections

### 1. Organization Strategy

Controls directory structure for feedback files.

**Option: `chronological` (Default)**

```yaml
feedback:
  persistence:
    organization: chronological
```

**Behavior:**
- All feedback files in single directory: `.devforgeai/feedback/sessions/`
- Files sorted chronologically by filename
- Simplest structure, minimal directories

**Use when:**
- Feedback volume is low (<1,000 files)
- Simple chronological review is sufficient
- Minimal directory structure preferred

**Directory structure:**
```
.devforgeai/feedback/sessions/
├── 2025-11-07T10-30-00-command-success.md
├── 2025-11-07T10-35-15-skill-success.md
├── 2025-11-11T14-30-00-workflow-success.md
└── ...
```

---

**Option: `by-operation`**

```yaml
feedback:
  persistence:
    organization: by-operation
```

**Behavior:**
- Feedback organized by operation type
- Subdirectories: `command/`, `skill/`, `subagent/`, `workflow/`
- Easy to analyze feedback per operation type

**Use when:**
- Want to analyze command vs skill vs subagent feedback separately
- Feedback volume is moderate (1,000-10,000 files)

**Directory structure:**
```
.devforgeai/feedback/sessions/
├── command/
│   ├── 2025-11-07T10-30-00-command-success.md
│   └── 2025-11-11T14-30-00-command-failure.md
├── skill/
│   └── 2025-11-07T10-35-15-skill-success.md
├── subagent/
│   └── 2025-11-11T09-00-00-subagent-success.md
└── workflow/
    └── 2025-11-11T14-45-00-workflow-partial.md
```

---

**Option: `by-status`**

```yaml
feedback:
  persistence:
    organization: by-status
```

**Behavior:**
- Feedback organized by completion status
- Subdirectories: `success/`, `failure/`, `partial/`, `skipped/`
- Easy to find and investigate failures

**Use when:**
- Need to quickly access failure feedback for debugging
- Want to separate successful vs failed operations
- Failure investigation is primary use case

**Directory structure:**
```
.devforgeai/feedback/sessions/
├── success/
│   ├── 2025-11-07T10-30-00-command-success.md
│   └── 2025-11-07T10-35-15-skill-success.md
├── failure/
│   ├── 2025-11-11T14-30-00-command-failure.md
│   └── 2025-11-11T15-00-00-skill-failure.md
├── partial/
│   └── 2025-11-11T14-40-00-workflow-partial.md
└── skipped/
    └── 2025-11-11T14-45-00-command-skipped.md
```

---

**Option: `nested`**

```yaml
feedback:
  persistence:
    organization: nested
```

**Behavior:**
- Feedback organized by BOTH operation type AND status
- Two-level hierarchy: `{operation-type}/{status}/`
- Maximum filtering capability

**Use when:**
- Feedback volume is high (10,000+ files)
- Need detailed filtering (e.g., "show me all failed commands")
- Want to analyze patterns (e.g., "which skills fail most often?")

**Directory structure:**
```
.devforgeai/feedback/sessions/
├── command/
│   ├── success/
│   │   └── 2025-11-07T10-30-00-command-success.md
│   ├── failure/
│   │   └── 2025-11-11T14-30-00-command-failure.md
│   ├── partial/
│   └── skipped/
├── skill/
│   ├── success/
│   │   └── 2025-11-07T10-35-15-skill-success.md
│   ├── failure/
│   └── partial/
├── subagent/
│   └── success/
│       └── 2025-11-11T09-00-00-subagent-success.md
└── workflow/
    ├── success/
    ├── failure/
    ├── partial/
    │   └── 2025-11-11T14-45-00-workflow-partial.md
    └── skipped/
```

---

### 2. Retention Policy

Controls automatic cleanup of old feedback files.

**Default (No Retention):**
```yaml
feedback:
  persistence:
    retention:
      enabled: false  # Never delete feedback
```

**Behavior:** Feedback files accumulate indefinitely (manual cleanup required)

---

**With Retention (Archive Mode):**
```yaml
feedback:
  persistence:
    retention:
      enabled: true
      max_age_days: 90
      keep_archived: true
```

**Behavior:**
- Feedback older than 90 days moved to `.devforgeai/feedback/archived/`
- Original files deleted from `sessions/`
- Archived files preserved for historical analysis

**Directory structure:**
```
.devforgeai/feedback/
├── sessions/              ← Active (< 90 days)
│   └── 2025-11-11T*.md
└── archived/              ← Historical (> 90 days)
    ├── 2025-08-01T*.md
    └── 2025-07-15T*.md
```

---

**With Retention (Delete Mode):**
```yaml
feedback:
  persistence:
    retention:
      enabled: true
      max_age_days: 30
      keep_archived: false  # Permanently delete old feedback
```

**Behavior:**
- Feedback older than 30 days permanently deleted
- No archival, no recovery possible
- Use for compliance (e.g., GDPR data retention limits)

**⚠️ Warning:** Irreversible data deletion. Consider archival mode instead.

---

### 3. Permission Settings

Controls file and directory permissions (Unix only).

**Default (Restrictive):**
```yaml
feedback:
  persistence:
    permissions:
      mode: 0600           # Owner read/write only
      enforce: true        # Fail if chmod impossible
```

**Behavior:**
- Files: `0600` (user rw, group/other none)
- Directories: `0700` (user rwx, group/other none)
- Strict mode: Fails if permissions cannot be set

---

**Permissive Mode:**
```yaml
feedback:
  persistence:
    permissions:
      mode: 0644           # Owner rw, group/other read
      enforce: false       # Continue if chmod fails
```

**Behavior:**
- Files: `0644` (readable by all users)
- If chmod fails (containers, Windows), continues anyway
- Use when feedback is non-sensitive or filesystem doesn't support permissions

---

**Custom Permissions:**
```yaml
feedback:
  persistence:
    permissions:
      mode: 0640           # Owner rw, group read, other none
      enforce: true
```

**Common permission modes:**
- `0600`: Owner only (most secure)
- `0640`: Owner + group (team shared)
- `0644`: World-readable (public)
- `0400`: Read-only (immutable)

---

### 4. Base Path Customization (Advanced)

**Default:**
```yaml
feedback:
  persistence:
    base_path: .devforgeai
```

**Custom location:**
```yaml
feedback:
  persistence:
    base_path: /var/lib/devforgeai  # Absolute path
```

**Relative to project:**
```yaml
feedback:
  persistence:
    base_path: ./build/feedback  # Relative path
```

**Use when:**
- Feedback on separate volume (performance, space)
- Compliance requires specific storage location
- Integration with external monitoring systems

---

## Default Configuration

If no configuration file exists, these defaults are used:

```yaml
feedback:
  persistence:
    organization: chronological
    subdirectories:
      by_operation: false
      by_status: false
    retention:
      enabled: false
      max_age_days: 90
      keep_archived: true
    permissions:
      mode: 0600
      enforce: false  # Don't fail on Windows/containers
    base_path: .devforgeai
```

---

## Configuration Precedence

**Order of precedence (highest to lowest):**

1. **Runtime parameter** (highest priority)
   ```python
   persist_feedback_session(..., config={"organization": "by-status"})
   ```

2. **Environment variable**
   ```bash
   export DEVFORGEAI_FEEDBACK_ORGANIZATION=by-operation
   ```

3. **Project config file**
   ```yaml
   # .devforgeai/config.yaml
   feedback:
     persistence:
       organization: nested
   ```

4. **User config file**
   ```yaml
   # ~/.devforgeai/config.yaml
   feedback:
     persistence:
       organization: by-status
   ```

5. **Hardcoded defaults** (lowest priority)
   ```python
   DEFAULT_ORGANIZATION = "chronological"
   ```

---

## Configuration Examples

### Example 1: Development Environment

**Goal:** Simple chronological feedback, no cleanup, permissive permissions

```yaml
feedback:
  persistence:
    organization: chronological
    retention:
      enabled: false
    permissions:
      mode: 0600
      enforce: false  # Don't fail in containers
```

---

### Example 2: Production Environment

**Goal:** Organized by status, 30-day retention, strict permissions

```yaml
feedback:
  persistence:
    organization: by-status
    retention:
      enabled: true
      max_age_days: 30
      keep_archived: true
    permissions:
      mode: 0600
      enforce: true  # Fail if chmod impossible (security-critical)
```

---

### Example 3: CI/CD Environment

**Goal:** Nested organization, archive after 7 days, custom location

```yaml
feedback:
  persistence:
    organization: nested
    retention:
      enabled: true
      max_age_days: 7       # Short retention for CI
      keep_archived: true
    permissions:
      mode: 0644            # World-readable for CI logs
      enforce: false
    base_path: /var/ci/devforgeai/feedback
```

---

### Example 4: Compliance (GDPR)

**Goal:** Delete after 30 days (no archival), strict permissions

```yaml
feedback:
  persistence:
    organization: by-operation
    retention:
      enabled: true
      max_age_days: 30
      keep_archived: false  # Permanent deletion
    permissions:
      mode: 0600
      enforce: true
```

---

## Configuration Validation

### Valid Configuration

```yaml
feedback:
  persistence:
    organization: chronological  # ✅ Valid value
    permissions:
      mode: 0600  # ✅ Valid octal
      enforce: true  # ✅ Valid boolean
```

---

### Invalid Configuration (Falls Back to Defaults)

```yaml
feedback:
  persistence:
    organization: by-date  # ❌ Invalid (not in whitelist)
    # Falls back to: chronological

    permissions:
      mode: 777  # ❌ Invalid (missing octal prefix 0o)
      # Falls back to: 0600

      enforce: "yes"  # ❌ Invalid (not boolean)
      # Falls back to: false
```

**Error logging:**
```
[WARN] Invalid organization strategy 'by-date', falling back to 'chronological'
[WARN] Invalid permission mode '777', falling back to 0600
[WARN] Invalid enforce value 'yes', falling back to false
```

---

## Environment Variable Overrides

### Supported Variables

```bash
# Organization strategy
export DEVFORGEAI_FEEDBACK_ORGANIZATION=by-status

# Retention enabled
export DEVFORGEAI_FEEDBACK_RETENTION_ENABLED=true
export DEVFORGEAI_FEEDBACK_RETENTION_MAX_AGE_DAYS=60

# Permissions
export DEVFORGEAI_FEEDBACK_PERMISSIONS_MODE=0640
export DEVFORGEAI_FEEDBACK_PERMISSIONS_ENFORCE=false

# Base path
export DEVFORGEAI_FEEDBACK_BASE_PATH=/custom/path
```

**Use when:**
- Different configuration per environment (dev/staging/prod)
- CI/CD needs to override project defaults
- Testing different configurations without modifying files

---

## Runtime Configuration

### Programmatic Override

```python
from src.feedback_persistence import persist_feedback_session

# Custom configuration for this operation only
custom_config = {
    "organization": "by-status",
    "permissions": {
        "mode": 0640,
        "enforce": False
    }
}

result = persist_feedback_session(
    ...,
    config=custom_config  # ← Overrides file/env config
)
```

**Use when:**
- Specific operation needs different configuration
- Testing configuration changes
- Temporary override without modifying config file

---

## Organization Strategy Deep Dive

### Choosing the Right Strategy

| Strategy | Files | Depth | Use Case | Pros | Cons |
|----------|-------|-------|----------|------|------|
| **chronological** | <1K | Flat | Simple projects | Fast, minimal dirs | Hard to filter |
| **by-operation** | 1K-10K | 1-level | Medium projects | Filter by type | Still some clutter |
| **by-status** | 1K-10K | 1-level | Debugging focus | Find failures fast | Less granular |
| **nested** | 10K+ | 2-level | Large projects | Maximum filtering | More complex |

### Migration Between Strategies

**Scenario:** Change from `chronological` to `by-status`

**Steps:**
1. Update configuration
2. Run migration script (moves existing files)
3. New feedback uses new strategy automatically

**Migration script:**
```bash
#!/bin/bash
# migrate-feedback-organization.sh

SOURCE=".devforgeai/feedback/sessions"
TARGET=".devforgeai/feedback/sessions"

for file in $SOURCE/*.md; do
  # Extract status from filename
  status=$(echo "$file" | grep -oP '(?<=-)(?:success|failure|partial|skipped)(?=\.md)')

  # Create status directory
  mkdir -p "$TARGET/$status"

  # Move file
  mv "$file" "$TARGET/$status/"
done
```

---

## Retention Policy Implementation

### Automatic Cleanup

**When retention is enabled:**
```yaml
retention:
  enabled: true
  max_age_days: 90
```

**Behavior:**
- Cleanup runs: On application startup, daily at midnight, manually triggered
- Files checked: All `*.md` files in feedback/sessions/
- Age calculation: Current date - file timestamp (from filename)
- Action: Move to archived/ or delete (per `keep_archived` setting)

**Example:**
```
Current date: 2025-11-11
max_age_days: 90

File: 2025-08-01T10-00-00-command-success.md
Age: 102 days (2025-11-11 minus 2025-08-01)
Action: ARCHIVE (102 > 90)

File: 2025-10-15T14-00-00-skill-success.md
Age: 27 days
Action: KEEP (27 < 90)
```

---

### Manual Cleanup

**Cleanup command:**
```bash
# Run retention cleanup manually
python3 -c "from src.feedback_persistence import cleanup_old_feedback; \
    deleted = cleanup_old_feedback(max_age_days=90); \
    print(f'Cleaned up {deleted} old feedback files')"
```

**Dry-run mode:**
```bash
# See what would be deleted without actually deleting
python3 -c "from src.feedback_persistence import cleanup_old_feedback; \
    deleted = cleanup_old_feedback(max_age_days=90, dry_run=True); \
    print(f'Would delete {deleted} files')"
```

---

## Permission Settings Deep Dive

### Unix Permission Modes

**Octal notation:**
```
0600 = -rw-------  (Owner: rw, Group: none, Other: none)
0640 = -rw-r-----  (Owner: rw, Group: r, Other: none)
0644 = -rw-r--r--  (Owner: rw, Group: r, Other: r)
0400 = -r--------  (Owner: r, Group: none, Other: none)
```

**Breakdown:**
```
0600
 ╷╷╷
 ││└─ Other (0 = no permissions)
 │└── Group (0 = no permissions)
 └─── Owner (6 = 4+2 = read+write)
```

---

### Directory Permissions

**Default directory mode:** `0700`

```
0700 = drwx------  (Owner: rwx, Group: none, Other: none)
 ╷╷╷
 ││└─ Other (0 = no access)
 │└── Group (0 = no access)
 └─── Owner (7 = 4+2+1 = read+write+execute)
```

**Why execute (`x`) on directories?**
- Required to traverse directory (cd into it)
- Required to list directory contents
- Without `x`: Directory unusable even with `r` permission

---

### Enforce Mode

**Strict (`enforce: true`):**
```yaml
permissions:
  enforce: true
```

**Behavior:**
- If chmod fails → raise exception (operation fails)
- Use when: Security-critical environments
- Drawback: May fail in containers or restrictive environments

**Permissive (`enforce: false`):**
```yaml
permissions:
  enforce: false
```

**Behavior:**
- If chmod fails → log warning, continue operation
- Use when: Cross-platform compatibility important
- Drawback: Files may have insecure permissions

---

## Configuration Testing

### Test Configuration Loading

```python
from src.feedback_persistence import load_config

# Test default config
config = load_config()
assert config["organization"] == "chronological"

# Test custom config
config = load_config(config_path=".devforgeai/config.yaml")
assert config["organization"] in ["chronological", "by-operation", "by-status", "nested"]
```

### Test Configuration Override

```python
# Environment variable override
os.environ["DEVFORGEAI_FEEDBACK_ORGANIZATION"] = "by-status"
config = load_config()
assert config["organization"] == "by-status"
```

---

## Best Practices

### ✅ DO

1. **Start with defaults** (no config file)
   - Add configuration only when needed
   - Defaults work well for most projects

2. **Use environment variables for deployment**
   - Dev: Default configuration
   - Staging: `DEVFORGEAI_FEEDBACK_ORGANIZATION=by-status`
   - Prod: `DEVFORGEAI_FEEDBACK_ORGANIZATION=nested`

3. **Enable retention for long-running projects**
   - Prevents unbounded feedback accumulation
   - Archive mode preserves historical data

4. **Use restrictive permissions (0600)**
   - Feedback may contain sensitive information
   - Principle of least privilege

### ❌ DON'T

1. **Don't use world-writable permissions**
   ```yaml
   mode: 0666  # ❌ Security risk
   ```

2. **Don't set `max_age_days` too low**
   ```yaml
   max_age_days: 1  # ❌ May delete useful recent feedback
   ```

3. **Don't use absolute paths without planning**
   ```yaml
   base_path: /tmp/feedback  # ❌ May be cleared on reboot
   ```

4. **Don't enable enforcement in containers**
   ```yaml
   enforce: true  # ❌ May fail in Docker/K8s
   ```

---

## Troubleshooting

### Issue: Configuration Not Applied

**Check precedence:**
```bash
# 1. Environment variables override config file
env | grep DEVFORGEAI_FEEDBACK

# 2. Verify config file exists and is valid YAML
cat .devforgeai/config.yaml | python3 -m yaml

# 3. Check runtime override
# Look for config parameter in persist_feedback_session() call
```

---

### Issue: Permission Denied

**Symptoms:** `OSError: Permission denied` when writing feedback

**Resolution:**
```bash
# Check directory permissions
ls -ld .devforgeai/feedback/sessions/

# Fix directory permissions
chmod 0700 .devforgeai/feedback/sessions/

# Or: Set enforce: false to continue without chmod
```

---

### Issue: Files Not Being Archived

**Symptoms:** Old files remain after retention period

**Diagnosis:**
```bash
# Check retention enabled
grep -A 3 "retention:" .devforgeai/config.yaml

# Check if cleanup runs
# Look for cleanup logs in application output
```

**Resolution:**
```yaml
# Enable retention
retention:
  enabled: true  # ← Must be true
  max_age_days: 90
```

---

## Related Documentation

- **Filename Format:** `feedback-persistence-filename-spec.md`
- **Atomic Writes:** `feedback-persistence-atomic-writes.md`
- **Directory Layouts:** `feedback-persistence-directory-layouts.md`
- **Error Reference:** `feedback-persistence-error-reference.md`
- **Edge Cases:** `feedback-persistence-edge-cases.md`

---

## Changelog

- **v1.0.0 (2025-11-11):** Initial configuration guide
  - Organization strategies documented
  - Retention policy explained
  - Permission settings detailed
  - Best practices established

---

**This guide is authoritative for all DevForgeAI feedback persistence configuration.**
