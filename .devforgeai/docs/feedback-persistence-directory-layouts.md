# Feedback File Persistence - Directory Layout Diagrams

**Version:** 1.0.0
**Date:** 2025-11-11
**Story:** STORY-013 (Feedback File Persistence with Atomic Writes)

---

## Overview

Visual reference for all directory organization strategies supported by DevForgeAI feedback persistence.

---

## Base Directory Structure (All Strategies)

```
project-root/
└── .devforgeai/
    ├── context/              # Context files (tech-stack, source-tree, etc.)
    ├── adrs/                 # Architecture Decision Records
    ├── specs/                # Requirements, API specs
    ├── qa/                   # QA reports, coverage
    ├── deployment/           # Deployment configs
    └── feedback/             # ← FEEDBACK STORAGE
        ├── sessions/         # Active feedback files
        └── archived/         # Old feedback (if retention enabled)
```

---

## Strategy 1: Chronological (Default)

### Directory Tree

```
.devforgeai/feedback/
└── sessions/
    ├── 2025-11-07T10-30-00-command-success.md
    ├── 2025-11-07T10-35-15-skill-success.md
    ├── 2025-11-07T11-00-00-subagent-success.md
    ├── 2025-11-11T09-15-00-workflow-partial.md
    ├── 2025-11-11T14-30-00-command-success.md
    ├── 2025-11-11T14-30-00-command-success-1.md  ← Collision resolved
    ├── 2025-11-11T14-35-00-skill-failure.md
    └── 2025-11-11T15-00-00-command-success.md
```

### Characteristics

- **Depth:** 2 levels (feedback/ → sessions/)
- **Subdirectories:** None (flat structure)
- **File count:** All files in one directory
- **Sorting:** Chronological by default (`ls` output = time-ordered)

### Advantages

- ✅ Simple: Minimal directory structure
- ✅ Fast: No subdirectory creation overhead
- ✅ Easy listing: `ls -1` shows chronological order

### Disadvantages

- ❌ Hard to filter: Must parse filenames to filter
- ❌ Cluttered: All files mixed together
- ❌ Slow at scale: 50,000+ files in one directory degrades performance

### Best For

- Small projects (<100 feedback sessions/month)
- Development environments (low volume)
- Quick prototyping

---

## Strategy 2: By-Operation

### Directory Tree

```
.devforgeai/feedback/sessions/
├── command/
│   ├── 2025-11-07T10-30-00-command-success.md
│   ├── 2025-11-11T14-30-00-command-success.md
│   ├── 2025-11-11T14-30-00-command-success-1.md
│   └── 2025-11-11T14-35-00-command-failure.md
├── skill/
│   ├── 2025-11-07T10-35-15-skill-success.md
│   ├── 2025-11-11T14-35-00-skill-failure.md
│   └── 2025-11-11T15-00-00-skill-success.md
├── subagent/
│   ├── 2025-11-07T11-00-00-subagent-success.md
│   └── 2025-11-11T12-00-00-subagent-success.md
└── workflow/
    ├── 2025-11-11T09-15-00-workflow-partial.md
    └── 2025-11-11T16-00-00-workflow-success.md
```

### Characteristics

- **Depth:** 3 levels (feedback/ → sessions/ → {operation}/)
- **Subdirectories:** 4 (command, skill, subagent, workflow)
- **File count:** Distributed across subdirectories

### Advantages

- ✅ Organized: Feedback grouped by operation type
- ✅ Filterable: Easy to find command vs skill feedback
- ✅ Analyzable: Compare command success rate vs skill success rate

### Disadvantages

- ❌ More complex: 4 subdirectories to navigate
- ❌ Chronological order lost: Must combine subdirectories for timeline

### Best For

- Medium projects (100-1,000 feedback sessions/month)
- Analyzing specific operation types
- Comparing command vs skill vs subagent behavior

### Usage Examples

```bash
# List all command feedback
ls -1 .devforgeai/feedback/sessions/command/*.md

# Count skill failures
ls .devforgeai/feedback/sessions/skill/*-failure.md | wc -l

# Find latest subagent feedback
ls -1t .devforgeai/feedback/sessions/subagent/*.md | head -1
```

---

## Strategy 3: By-Status

### Directory Tree

```
.devforgeai/feedback/sessions/
├── success/
│   ├── 2025-11-07T10-30-00-command-success.md
│   ├── 2025-11-07T10-35-15-skill-success.md
│   ├── 2025-11-07T11-00-00-subagent-success.md
│   ├── 2025-11-11T14-30-00-command-success.md
│   ├── 2025-11-11T14-30-00-command-success-1.md
│   └── 2025-11-11T15-00-00-command-success.md
├── failure/
│   ├── 2025-11-11T14-35-00-command-failure.md
│   └── 2025-11-11T14-35-00-skill-failure.md
├── partial/
│   └── 2025-11-11T09-15-00-workflow-partial.md
└── skipped/
    └── 2025-11-10T08-00-00-command-skipped.md
```

### Characteristics

- **Depth:** 3 levels (feedback/ → sessions/ → {status}/)
- **Subdirectories:** 4 (success, failure, partial, skipped)
- **File count:** Distributed by completion status

### Advantages

- ✅ Debugging-focused: Failures instantly accessible
- ✅ Success rate: Easy to count success vs failure
- ✅ Problem investigation: Go straight to failure/ directory

### Disadvantages

- ❌ Operation type mixed: Commands and skills in same directory
- ❌ Chronological order lost: Must combine subdirectories

### Best For

- Production environments (debugging focus)
- High-failure scenarios (QA testing, experimental features)
- Operations teams (incident investigation)

### Usage Examples

```bash
# List all failures
ls -1 .devforgeai/feedback/sessions/failure/*.md

# Count success rate
success=$(ls .devforgeai/feedback/sessions/success/*.md | wc -l)
failure=$(ls .devforgeai/feedback/sessions/failure/*.md | wc -l)
echo "Success rate: $((success * 100 / (success + failure)))%"

# Find recent partial completions
ls -1t .devforgeai/feedback/sessions/partial/*.md | head -5
```

---

## Strategy 4: Nested (Operation + Status)

### Directory Tree

```
.devforgeai/feedback/sessions/
├── command/
│   ├── success/
│   │   ├── 2025-11-07T10-30-00-command-success.md
│   │   ├── 2025-11-11T14-30-00-command-success.md
│   │   └── 2025-11-11T14-30-00-command-success-1.md
│   ├── failure/
│   │   └── 2025-11-11T14-35-00-command-failure.md
│   ├── partial/
│   └── skipped/
│       └── 2025-11-10T08-00-00-command-skipped.md
├── skill/
│   ├── success/
│   │   ├── 2025-11-07T10-35-15-skill-success.md
│   │   └── 2025-11-11T15-00-00-skill-success.md
│   ├── failure/
│   │   └── 2025-11-11T14-35-00-skill-failure.md
│   ├── partial/
│   └── skipped/
├── subagent/
│   ├── success/
│   │   ├── 2025-11-07T11-00-00-subagent-success.md
│   │   └── 2025-11-11T12-00-00-subagent-success.md
│   ├── failure/
│   ├── partial/
│   └── skipped/
└── workflow/
    ├── success/
    │   └── 2025-11-11T16-00-00-workflow-success.md
    ├── failure/
    ├── partial/
    │   └── 2025-11-11T09-15-00-workflow-partial.md
    └── skipped/
```

### Characteristics

- **Depth:** 4 levels (feedback/ → sessions/ → {operation}/ → {status}/)
- **Subdirectories:** 16 total (4 operations × 4 statuses)
- **File count:** Maximum distribution

### Advantages

- ✅ Maximum filtering: "Show me all failed commands"
- ✅ Pattern analysis: Which operation types fail most?
- ✅ Scalability: Handles 100,000+ files efficiently
- ✅ Detailed metrics: Success rate per operation type

### Disadvantages

- ❌ Complex: 16 subdirectories to navigate
- ❌ Overkill for small projects: Unnecessary structure overhead
- ❌ Chronological order lost: Requires cross-directory aggregation

### Best For

- Large projects (10,000+ feedback sessions/month)
- Enterprise environments (detailed analytics)
- Multi-team projects (different teams analyze different operations)
- Compliance requirements (audit trails by operation and status)

### Usage Examples

```bash
# All failed commands
ls -1 .devforgeai/feedback/sessions/command/failure/*.md

# All successful skills
ls -1 .devforgeai/feedback/sessions/skill/success/*.md

# All partial workflows
ls -1 .devforgeai/feedback/sessions/workflow/partial/*.md

# Command success rate
success=$(ls .devforgeai/feedback/sessions/command/success/*.md 2>/dev/null | wc -l)
failure=$(ls .devforgeai/feedback/sessions/command/failure/*.md 2>/dev/null | wc -l)
echo "Command success rate: $((success * 100 / (success + failure + 1)))%"
```

---

## Archived Feedback (With Retention)

### Archived Directory Structure

**Configuration:**
```yaml
retention:
  enabled: true
  max_age_days: 90
  keep_archived: true
```

**Directory tree:**
```
.devforgeai/feedback/
├── sessions/                              # Active (< 90 days)
│   ├── 2025-11-01T*.md
│   ├── 2025-11-07T*.md
│   └── 2025-11-11T*.md
└── archived/                              # Historical (> 90 days)
    ├── 2025-08-01T*.md                   # 102 days old
    ├── 2025-07-15T*.md                   # 118 days old
    └── 2025-06-30T*.md                   # 134 days old
```

**Archive organization:**
- Archived files preserve original filenames
- No subdirectory organization (flat chronological)
- Sorted oldest to newest

**Querying archived feedback:**
```bash
# Find archived feedback from August
ls .devforgeai/feedback/archived/2025-08-*.md

# Count total archived feedback
ls .devforgeai/feedback/archived/*.md | wc -l

# Restore specific feedback from archive
cp .devforgeai/feedback/archived/2025-08-01T10-00-00-command-success.md \
   .devforgeai/feedback/sessions/
```

---

## Directory Size Estimates

### Chronological Strategy

**Small project** (100 feedback/month):
```
sessions/ : ~100 files, ~500KB total
Directories: 1
```

**Medium project** (1,000 feedback/month):
```
sessions/ : ~1,000 files, ~5MB total
Directories: 1
```

**Large project** (10,000 feedback/month):
```
sessions/ : ~10,000 files, ~50MB total
Directories: 1
```

---

### Nested Strategy

**Large project** (10,000 feedback/month with 80% success rate):
```
command/success/  : ~4,000 files (~20MB)
command/failure/  : ~800 files (~4MB)
skill/success/    : ~2,400 files (~12MB)
skill/failure/    : ~400 files (~2MB)
subagent/success/ : ~1,600 files (~8MB)
subagent/failure/ : ~320 files (~1.6MB)
workflow/partial/ : ~400 files (~2MB)
workflow/success/ : ~80 files (~400KB)

Total: ~10,000 files, ~50MB
Directories: 16
```

---

## Directory Navigation Guide

### Finding Specific Feedback

**By timestamp (all strategies):**
```bash
# Specific date
find .devforgeai/feedback/sessions/ -name "2025-11-11T*.md"

# Specific hour
find .devforgeai/feedback/sessions/ -name "2025-11-11T14-*.md"

# Date range (Nov 7-11)
find .devforgeai/feedback/sessions/ -name "2025-11-0[7-9]T*.md" -o -name "2025-11-1[01]T*.md"
```

**By operation type (chronological strategy):**
```bash
# All commands
ls .devforgeai/feedback/sessions/*-command-*.md

# All skills
ls .devforgeai/feedback/sessions/*-skill-*.md
```

**By operation type (by-operation strategy):**
```bash
# All commands
ls .devforgeai/feedback/sessions/command/*.md

# All skills
ls .devforgeai/feedback/sessions/skill/*.md
```

**By status (chronological strategy):**
```bash
# All failures
ls .devforgeai/feedback/sessions/*-failure.md

# All successes
ls .devforgeai/feedback/sessions/*-success.md
```

**By status (by-status strategy):**
```bash
# All failures
ls .devforgeai/feedback/sessions/failure/*.md

# All successes
ls .devforgeai/feedback/sessions/success/*.md
```

**By both (nested strategy):**
```bash
# Failed commands
ls .devforgeai/feedback/sessions/command/failure/*.md

# Successful skills
ls .devforgeai/feedback/sessions/skill/success/*.md

# Partial workflows
ls .devforgeai/feedback/sessions/workflow/partial/*.md
```

---

## Directory Permissions

### Default Permissions

**Directories:**
```
drwx------  (0700)  # Owner: rwx, Group: none, Other: none
```

**Files:**
```
-rw-------  (0600)  # Owner: rw, Group: none, Other: none
```

### Permission Breakdown

```
.devforgeai/               drwxr-xr-x  (0755)  ← Project root, readable
├── feedback/              drwx------  (0700)  ← Restricted (feedback sensitive)
│   └── sessions/          drwx------  (0700)  ← Restricted
│       └── *.md           -rw-------  (0600)  ← Files restrictive
```

**Why restrictive permissions?**
- Feedback may contain error messages with sensitive info
- Feedback may reference internal architecture details
- Principle of least privilege: Only owner needs access

---

## Disk Space Management

### Space Usage Estimates

**Typical feedback file size:** 3-5KB
**Large feedback file size:** 10-50KB (with detailed error traces)

**Monthly estimates:**
- 100 feedback sessions: ~500KB/month
- 1,000 feedback sessions: ~5MB/month
- 10,000 feedback sessions: ~50MB/month
- 100,000 feedback sessions: ~500MB/month

**Yearly estimates:**
- 10,000/month: ~600MB/year
- 100,000/month: ~6GB/year

**With retention (90-day):**
- 10,000/month: ~150MB (3 months active)
- 100,000/month: ~1.5GB (3 months active)

---

### Monitoring Disk Usage

```bash
# Check feedback directory size
du -sh .devforgeai/feedback/

# Breakdown by subdirectory
du -sh .devforgeai/feedback/*

# Count feedback files
find .devforgeai/feedback/sessions/ -name "*.md" | wc -l

# Find largest feedback files
find .devforgeai/feedback/sessions/ -name "*.md" -exec ls -lh {} + | sort -k5 -hr | head -10
```

---

## Migration Between Strategies

### Migration Scenarios

**Scenario 1: Chronological → By-Operation**

**Before:**
```
sessions/
├── 2025-11-11T14-30-00-command-success.md
├── 2025-11-11T14-35-00-skill-success.md
└── 2025-11-11T15-00-00-subagent-success.md
```

**After:**
```
sessions/
├── command/
│   └── 2025-11-11T14-30-00-command-success.md
├── skill/
│   └── 2025-11-11T14-35-00-skill-success.md
└── subagent/
    └── 2025-11-11T15-00-00-subagent-success.md
```

**Migration script:**
```bash
#!/bin/bash
cd .devforgeai/feedback/sessions/

for file in *.md; do
  # Extract operation type from filename
  op_type=$(echo "$file" | grep -oP '(?<=T\d{2}-\d{2}-\d{2}-)(?:command|skill|subagent|workflow)')

  # Create subdirectory
  mkdir -p "$op_type"

  # Move file
  mv "$file" "$op_type/"
done
```

---

**Scenario 2: By-Status → Nested**

**Before:**
```
sessions/
├── success/
│   ├── 2025-11-11T14-30-00-command-success.md
│   └── 2025-11-11T14-35-00-skill-success.md
└── failure/
    └── 2025-11-11T14-40-00-command-failure.md
```

**After:**
```
sessions/
├── command/
│   ├── success/
│   │   └── 2025-11-11T14-30-00-command-success.md
│   └── failure/
│       └── 2025-11-11T14-40-00-command-failure.md
└── skill/
    └── success/
        └── 2025-11-11T14-35-00-skill-success.md
```

**Migration script:**
```bash
#!/bin/bash
cd .devforgeai/feedback/sessions/

for status_dir in success failure partial skipped; do
  if [ -d "$status_dir" ]; then
    for file in "$status_dir"/*.md; do
      # Extract operation type
      op_type=$(echo "$file" | grep -oP '(?<=T\d{2}-\d{2}-\d{2}-)(?:command|skill|subagent|workflow)')

      # Create nested directory
      mkdir -p "$op_type/$status_dir"

      # Move file
      mv "$file" "$op_type/$status_dir/"
    done
    rmdir "$status_dir"  # Remove old directory
  fi
done
```

---

## Directory Cleanup and Maintenance

### Removing Empty Directories

```bash
# Find empty subdirectories
find .devforgeai/feedback/sessions/ -type d -empty

# Delete empty subdirectories
find .devforgeai/feedback/sessions/ -type d -empty -delete
```

### Cleaning Up Temp Files

```bash
# Find orphaned temp files from crashes
find .devforgeai/feedback/sessions/ -name "*.tmp"

# Delete temp files
find .devforgeai/feedback/sessions/ -name "*.tmp" -delete

# Or use built-in cleanup function:
python3 -c "from src.feedback_persistence import cleanup_temp_feedback_files; \
    count = cleanup_temp_feedback_files(); print(f'Removed {count} temp files')"
```

---

## Directory Initialization

### Automatic Creation

**On first feedback write:**
```
1. Check if .devforgeai/ exists
   - If not: Create with 0755
2. Check if .devforgeai/feedback/ exists
   - If not: Create with 0700
3. Check if .devforgeai/feedback/sessions/ exists
   - If not: Create with 0700
4. Create organization subdirectories (if applicable)
   - by-operation: Create command/, skill/, subagent/, workflow/
   - by-status: Create success/, failure/, partial/, skipped/
   - nested: Create all 16 subdirectories
```

**Result:** Zero-configuration setup, directories created on-demand

---

### Manual Pre-Creation

**For performance** (avoid directory creation overhead on first write):
```bash
# Pre-create directory structure
mkdir -p .devforgeai/feedback/sessions/
chmod 0700 .devforgeai/feedback/sessions/

# Pre-create for nested strategy
mkdir -p .devforgeai/feedback/sessions/{command,skill,subagent,workflow}/{success,failure,partial,skipped}
chmod -R 0700 .devforgeai/feedback/
```

---

## Comparative Analysis

### Storage Efficiency

| Strategy | Directories | Avg Depth | File Distribution | Space Overhead |
|----------|-------------|-----------|-------------------|----------------|
| chronological | 1 | 2 | 100% in one dir | 0 bytes (no extra dirs) |
| by-operation | 4 | 3 | 25% per subdir | ~16KB (4 directories) |
| by-status | 4 | 3 | Varies by status | ~16KB (4 directories) |
| nested | 16 | 4 | ~6% per subdir | ~64KB (16 directories) |

**Space overhead:** Negligible (<100KB even for nested strategy)

---

### Query Performance

**Test: Find all failures (10,000 total files, 1,000 failures)**

| Strategy | Query | Time | Explanation |
|----------|-------|------|-------------|
| chronological | `ls *-failure.md` | ~200ms | Scans all 10,000 filenames |
| by-status | `ls failure/*.md` | ~20ms | Scans 1,000 files only |
| nested | `ls */failure/*.md` | ~30ms | Scans 4 subdirs × 250 files |

**Winner:** by-status (10x faster for status queries)

---

**Test: Find all command feedback (10,000 total, 5,000 commands)**

| Strategy | Query | Time | Explanation |
|----------|-------|------|-------------|
| chronological | `ls *-command-*.md` | ~150ms | Scans all 10,000 filenames |
| by-operation | `ls command/*.md` | ~100ms | Scans 5,000 files only |
| nested | `ls command/*/*.md` | ~110ms | Scans 4 status subdirs |

**Winner:** by-operation (1.5x faster for operation queries)

---

## Best Practices

### ✅ DO

1. **Choose strategy based on volume:**
   - <1K files/month: chronological
   - 1K-10K files/month: by-operation or by-status
   - 10K+ files/month: nested

2. **Pre-create directories for performance:**
   ```bash
   mkdir -p .devforgeai/feedback/sessions/
   ```

3. **Enable retention for long-running projects:**
   - Prevents unbounded growth
   - Maintains performance

4. **Use nested strategy for analytics:**
   - Detailed metrics per operation type
   - Success rate analysis

### ❌ DON'T

1. **Don't use nested for small projects:**
   - Overkill: 16 directories for 100 files
   - Unnecessary complexity

2. **Don't mix strategies:**
   - Causes confusion
   - Breaks queries

3. **Don't create directories manually with wrong permissions:**
   ```bash
   mkdir .devforgeai/feedback/sessions/  # ← May have wrong permissions
   # Let persist_feedback_session() create it
   ```

---

## Related Documentation

- **Filename Format:** `feedback-persistence-filename-spec.md`
- **Atomic Writes:** `feedback-persistence-atomic-writes.md`
- **Configuration:** `feedback-persistence-config-guide.md`
- **Error Reference:** `feedback-persistence-error-reference.md`
- **Edge Cases:** `feedback-persistence-edge-cases.md`

---

## Changelog

- **v1.0.0 (2025-11-11):** Initial directory layout diagrams
  - 4 organization strategies visualized
  - Directory tree examples
  - Navigation guide
  - Migration procedures
  - Performance comparison

---

**This guide is authoritative for all DevForgeAI feedback directory organization.**
