# Feedback File Persistence - Filename Format Specification

**Version:** 1.0.0
**Date:** 2025-11-11
**Story:** STORY-013 (Feedback File Persistence with Atomic Writes)

---

## Overview

This document specifies the filename format for feedback session files persisted by the DevForgeAI framework. Filenames are designed to be human-readable, chronologically sortable, and collision-resistant.

---

## Filename Pattern

### Base Format

```
{timestamp}-{operation-type}-{status}[-{counter}].md
```

**Components:**
1. **Timestamp**: ISO 8601 format (filesystem-safe)
2. **Operation Type**: Type of operation that generated feedback
3. **Status**: Completion status of the operation
4. **Counter**: Optional collision resolution suffix
5. **Extension**: Always `.md` (Markdown file)

---

## Component Specifications

### 1. Timestamp Component

**Format:** `YYYY-MM-DDTHH-MM-SS`

**Details:**
- **Date portion**: `YYYY-MM-DD` (year-month-day with hyphens)
- **Time separator**: `T` (ISO 8601 standard)
- **Time portion**: `HH-MM-SS` (hour-minute-second with hyphens, NOT colons)
- **Timezone**: Implicitly UTC (no timezone suffix in filename)
- **Precision**: 1-second granularity

**Why hyphens instead of colons?**
- Colons (`:`) are invalid in Windows filenames
- Hyphens (`-`) work across all platforms (Linux, macOS, Windows)
- Maintains ISO 8601 readability while ensuring cross-platform compatibility

**Examples:**
```
2025-11-11T14-30-00  ← November 11, 2025 at 2:30:00 PM UTC
2025-11-11T09-15-42  ← November 11, 2025 at 9:15:42 AM UTC
2025-12-25T23-59-59  ← December 25, 2025 at 11:59:59 PM UTC
```

**Sortability:**
```bash
# Lexicographic sort = Chronological sort
ls -1 .devforgeai/feedback/sessions/*.md | sort

# Output (oldest to newest):
2025-11-07T10-30-00-command-success.md
2025-11-07T10-35-15-skill-success.md
2025-11-11T14-30-00-workflow-success.md
```

---

### 2. Operation Type Component

**Valid Values:**
- `command` - Feedback from slash command execution (e.g., `/dev`, `/qa`, `/release`)
- `skill` - Feedback from skill execution (e.g., `devforgeai-development`, `devforgeai-qa`)
- `subagent` - Feedback from subagent execution (e.g., `test-automator`, `code-reviewer`)
- `workflow` - Feedback from multi-phase workflow (e.g., `/orchestrate` full lifecycle)

**Case Sensitivity:** Lowercase only (enforced by validation)

**Validation:**
```python
VALID_OPERATION_TYPES = {"command", "skill", "subagent", "workflow"}

if operation_type not in VALID_OPERATION_TYPES:
    raise ValueError(f"Invalid operation_type: {operation_type}")
```

**Examples:**
```
2025-11-11T14-30-00-command-success.md     ← Command feedback
2025-11-11T14-35-00-skill-success.md       ← Skill feedback
2025-11-11T14-40-00-subagent-success.md    ← Subagent feedback
2025-11-11T14-45-00-workflow-partial.md    ← Workflow feedback
```

---

### 3. Status Component

**Valid Values:**
- `success` - Operation completed successfully without errors
- `failure` - Operation failed with blocking errors
- `partial` - Operation partially completed (some steps succeeded, some failed)
- `skipped` - Operation was skipped (prerequisites not met, intentionally bypassed)

**Case Sensitivity:** Lowercase only (enforced by validation)

**Validation:**
```python
VALID_STATUSES = {"success", "failure", "partial", "skipped"}

if status not in VALID_STATUSES:
    raise ValueError(f"Invalid status: {status}")
```

**Examples:**
```
2025-11-11T14-30-00-command-success.md   ← Successful command
2025-11-11T14-35-00-skill-failure.md     ← Failed skill
2025-11-11T14-40-00-subagent-partial.md  ← Partial subagent result
2025-11-11T14-45-00-workflow-skipped.md  ← Skipped workflow
```

---

### 4. Counter Component (Collision Resolution)

**Format:** `-{N}` where N is 1, 2, 3, ...

**When Applied:**
- Automatically appended when filename collision detected
- Collision occurs when same timestamp + operation-type + status combination exists
- Counter increments until unique filename found
- Maximum: 10,000 attempts (then raises RuntimeError)

**Examples:**
```
# First feedback at 14:30:00
2025-11-11T14-30-00-command-success.md

# Second feedback at exactly 14:30:00 (collision!)
2025-11-11T14-30-00-command-success-1.md

# Third feedback at exactly 14:30:00 (another collision!)
2025-11-11T14-30-00-command-success-2.md
```

**Collision Detection Algorithm:**
```python
counter = 0
while target_file.exists() and counter < 10000:
    counter += 1
    filename = f"{base_filename}-{counter}.md"
    target_file = target_dir / filename

if counter >= 10000:
    raise RuntimeError("Too many collisions")
```

---

### 5. Extension Component

**Value:** Always `.md` (Markdown file)

**Rationale:**
- Human-readable format
- Compatible with text editors and IDEs
- Supports YAML frontmatter + Markdown content
- Git-friendly (text diffs, not binary)
- Framework standard (matches `.ai_docs/Stories/*.story.md` pattern)

---

## Complete Filename Examples

### Standard Cases (No Collisions)

```
2025-11-11T14-30-00-command-success.md
2025-11-11T14-30-01-skill-success.md
2025-11-11T14-30-02-subagent-success.md
2025-11-11T14-30-03-workflow-success.md
```

### Collision Cases

```
# Two commands complete in same second
2025-11-11T14-30-00-command-success.md     ← First
2025-11-11T14-30-00-command-success-1.md   ← Second (collision resolved)

# Three skills complete in same second
2025-11-11T15-00-00-skill-success.md       ← First
2025-11-11T15-00-00-skill-success-1.md     ← Second (collision)
2025-11-11T15-00-00-skill-success-2.md     ← Third (collision)
```

### Status Variations

```
2025-11-11T14-30-00-command-success.md     ← Successful
2025-11-11T14-35-00-command-failure.md     ← Failed
2025-11-11T14-40-00-command-partial.md     ← Partial
2025-11-11T14-45-00-command-skipped.md     ← Skipped
```

### All Operation Types

```
2025-11-11T14-30-00-command-success.md     ← /dev command
2025-11-11T14-35-00-skill-success.md       ← devforgeai-qa skill
2025-11-11T14-40-00-subagent-success.md    ← test-automator subagent
2025-11-11T14-45-00-workflow-success.md    ← /orchestrate workflow
```

---

## Filename Validation Rules

### Character Restrictions

**Prohibited characters (path traversal prevention):**
- `../` (parent directory)
- `..\\` (Windows parent directory)
- `/` (directory separator, except in path)
- `\` (Windows directory separator)
- Control characters (ASCII 0-31)
- Null bytes (`\0`)

**Sanitization:**
```python
def _sanitize_filename_component(component: str) -> str:
    """Remove/replace unsafe characters."""
    # Remove path traversal sequences
    component = component.replace("../", "").replace("..\\", "")
    # Remove directory separators
    component = component.replace("/", "-").replace("\\", "-")
    # Remove control characters
    component = "".join(c for c in component if ord(c) >= 32)
    return component
```

### Length Constraints

**Maximum filename length:** 255 characters (filesystem limit)

**Typical length:**
- Timestamp: 19 characters (`2025-11-11T14-30-00`)
- Operation type: 7-9 characters (`command`, `subagent`)
- Status: 6-8 characters (`success`, `failure`)
- Separators: 2 characters (`-`)
- Extension: 3 characters (`.md`)
- **Total**: ~40-50 characters (well under 255 limit)

**With collision counter:**
- Counter: 1-5 characters (`-1`, `-999`, `-9999`)
- **Total**: ~45-60 characters (still well under limit)

---

## Directory Organization Strategies

### Chronological (Default)

**Path Pattern:**
```
.devforgeai/feedback/sessions/{filename}
```

**Example:**
```
.devforgeai/feedback/sessions/
├── 2025-11-07T10-30-00-command-success.md
├── 2025-11-07T10-35-15-skill-success.md
├── 2025-11-11T14-30-00-workflow-success.md
└── ...
```

**Use Case:** Simple chronological listing, default behavior, minimal directory structure

---

### By-Operation

**Path Pattern:**
```
.devforgeai/feedback/sessions/{operation-type}/{filename}
```

**Example:**
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

**Use Case:** Analyze feedback by operation type, filter by command vs skill vs subagent

---

### By-Status

**Path Pattern:**
```
.devforgeai/feedback/sessions/{status}/{filename}
```

**Example:**
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

**Use Case:** Quickly find failures for investigation, review successful operations

---

### Nested (Operation + Status)

**Path Pattern:**
```
.devforgeai/feedback/sessions/{operation-type}/{status}/{filename}
```

**Example:**
```
.devforgeai/feedback/sessions/
├── command/
│   ├── success/
│   │   └── 2025-11-07T10-30-00-command-success.md
│   └── failure/
│       └── 2025-11-11T14-30-00-command-failure.md
├── skill/
│   └── success/
│       └── 2025-11-07T10-35-15-skill-success.md
└── workflow/
    └── partial/
        └── 2025-11-11T14-45-00-workflow-partial.md
```

**Use Case:** Detailed filtering (e.g., "show me all failed commands"), best for large feedback volumes

---

## Filename Parsing

### Extracting Components

**Regular Expression:**
```regex
^(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})-(command|skill|subagent|workflow)-(success|failure|partial|skipped)(?:-(\d+))?\.md$
```

**Capture Groups:**
1. Timestamp
2. Operation type
3. Status
4. Counter (optional)

**Python Example:**
```python
import re

pattern = r'^(\d{4}-\d{2}-\d{2}T\d{2}-\d{2}-\d{2})-(command|skill|subagent|workflow)-(success|failure|partial|skipped)(?:-(\d+))?\.md$'

filename = "2025-11-11T14-30-00-command-success-1.md"
match = re.match(pattern, filename)

if match:
    timestamp = match.group(1)      # "2025-11-11T14-30-00"
    operation = match.group(2)      # "command"
    status = match.group(3)         # "success"
    counter = match.group(4)        # "1" or None
```

### Querying Feedback Files

**Find all feedback for a specific date:**
```bash
ls .devforgeai/feedback/sessions/2025-11-11T*.md
```

**Find all command feedback:**
```bash
ls .devforgeai/feedback/sessions/*-command-*.md
```

**Find all failures:**
```bash
ls .devforgeai/feedback/sessions/*-failure.md
```

**Find feedback from a specific hour:**
```bash
ls .devforgeai/feedback/sessions/2025-11-11T14-*.md
```

---

## Timestamp Conversion

### Filename → ISO 8601 DateTime

**Conversion:**
```python
def filename_to_datetime(filename: str) -> datetime:
    """Convert filename timestamp to datetime object."""
    # Extract timestamp portion
    timestamp_str = filename.split("-")[0:3]
    timestamp_iso = "-".join(timestamp_str).replace("T", "T").replace("-", ":", 2)

    # Parse to datetime
    return datetime.fromisoformat(timestamp_iso)
```

**Example:**
```python
filename = "2025-11-11T14-30-00-command-success.md"
dt = filename_to_datetime(filename)
# Result: datetime(2025, 11, 11, 14, 30, 0, tzinfo=UTC)
```

### DateTime → Filename Timestamp

**Conversion:**
```python
def datetime_to_filename_timestamp(dt: datetime) -> str:
    """Convert datetime to filename-safe timestamp."""
    iso_str = dt.isoformat()  # "2025-11-11T14:30:00+00:00"
    # Replace colons with hyphens, remove timezone
    return iso_str.replace(":", "-").split("+")[0].split(".")[0]
```

**Example:**
```python
from datetime import datetime, timezone

dt = datetime.now(timezone.utc)
timestamp = datetime_to_filename_timestamp(dt)
# Result: "2025-11-11T14-30-00"
```

---

## Collision Handling

### Detection

**Algorithm:**
1. Generate base filename: `{timestamp}-{op-type}-{status}.md`
2. Check if file exists at target path
3. If exists: Collision detected
4. Append counter `-1` and check again
5. Increment counter until unique filename found
6. If counter exceeds 10,000: Raise RuntimeError

### Resolution

**Example collision sequence:**
```python
# Attempt 1: Base filename
filename = "2025-11-11T14-30-00-command-success.md"
# Result: File exists → COLLISION

# Attempt 2: Add counter
filename = "2025-11-11T14-30-00-command-success-1.md"
# Result: File exists → COLLISION

# Attempt 3: Increment counter
filename = "2025-11-11T14-30-00-command-success-2.md"
# Result: File doesn't exist → SUCCESS
```

### Pathological Case

**If 10,000 collisions occur** (extremely unlikely):
```python
raise RuntimeError(
    f"Too many collisions for filename: {base_filename}. "
    f"This suggests a timestamp resolution issue or excessive concurrent writes."
)
```

**Probability:** Essentially zero in real-world usage
- Requires 10,000 operations completing in same second
- DevForgeAI operations typically take seconds to minutes
- Counter limit protects against infinite loops

---

## File System Compatibility

### Cross-Platform Support

| Platform | Supported | Notes |
|----------|-----------|-------|
| **Linux** | ✅ Yes | Full support, native POSIX operations |
| **macOS** | ✅ Yes | Full support, case-insensitive by default |
| **Windows** | ✅ Yes | Hyphens used instead of colons for compatibility |

### Platform-Specific Considerations

**Linux:**
- Case-sensitive filesystem
- `2025-11-11T14-30-00-Command-Success.md` ≠ `2025-11-11T14-30-00-command-success.md`
- Recommendation: Use lowercase only

**macOS:**
- Case-insensitive by default (HFS+, APFS)
- `Command` and `command` treated as same file
- Case-preserving (stores as entered)
- Recommendation: Use lowercase for consistency

**Windows:**
- Case-insensitive filesystem
- Colons (`:`) prohibited in filenames (hence hyphens in time portion)
- Backslashes (`\`) are directory separators
- Recommendation: Use lowercase, avoid special characters

---

## Sorting and Filtering

### Chronological Sorting

**Shell:**
```bash
# Sort oldest to newest
ls -1 .devforgeai/feedback/sessions/*.md | sort

# Sort newest to oldest
ls -1 .devforgeai/feedback/sessions/*.md | sort -r
```

**Python:**
```python
from pathlib import Path

feedback_dir = Path(".devforgeai/feedback/sessions")
files = sorted(feedback_dir.glob("*.md"))  # Oldest first
files_newest = sorted(feedback_dir.glob("*.md"), reverse=True)  # Newest first
```

### Filtering by Criteria

**By Date:**
```python
# All feedback from November 11, 2025
files = feedback_dir.glob("2025-11-11T*.md")
```

**By Operation Type:**
```python
# All command feedback
files = feedback_dir.glob("*-command-*.md")

# All skill feedback
files = feedback_dir.glob("*-skill-*.md")
```

**By Status:**
```python
# All failures
files = feedback_dir.glob("*-failure.md")

# All successes
files = feedback_dir.glob("*-success.md")
```

**By Time Range:**
```python
# All feedback between 14:00 and 15:00
files = feedback_dir.glob("*T14-*.md")
```

---

## Validation and Security

### Filename Security

**Path Traversal Prevention:**
```python
# Prohibited patterns
bad_patterns = ["../", "..\\", "/", "\\"]

for pattern in bad_patterns:
    if pattern in filename_component:
        raise ValueError(f"Path traversal detected: {pattern}")
```

**Example blocked attacks:**
```
../../../etc/passwd             ← Blocked (../ detected)
..\\..\\..\\Windows\\System32   ← Blocked (..\ detected)
/etc/shadow                     ← Blocked (absolute path)
```

### Validation Checklist

Before accepting a filename component:
- [ ] No path traversal sequences (`../`, `..\\`)
- [ ] No absolute paths (`/`, `C:\`)
- [ ] No directory separators in component
- [ ] No control characters (ASCII 0-31)
- [ ] No null bytes
- [ ] Length ≤ 255 characters
- [ ] Matches expected format pattern
- [ ] Operation type in whitelist
- [ ] Status in whitelist

---

## Best Practices

### Timestamp Generation

**✅ DO:**
```python
from datetime import datetime, timezone

# Use UTC timezone
timestamp = datetime.now(timezone.utc).isoformat()
```

**❌ DON'T:**
```python
# Local timezone (ambiguous across systems)
timestamp = datetime.now().isoformat()

# No timezone (assumes UTC but doesn't specify)
timestamp = datetime.utcnow().isoformat()
```

### Collision Handling

**✅ DO:**
```python
# Let the framework handle collisions automatically
result = persist_feedback_session(...)
if result.collision_resolved:
    logger.info(f"Collision resolved: {result.actual_filename}")
```

**❌ DON'T:**
```python
# Manual collision handling (error-prone)
if file_exists:
    filename = f"{filename}-{uuid.uuid4()}.md"  # UUID makes filenames unsortable
```

### Filename Analysis

**✅ DO:**
```python
# Use regex to parse components
match = re.match(pattern, filename)
timestamp = match.group(1)
```

**❌ DON'T:**
```python
# String splitting (fragile)
parts = filename.split("-")
timestamp = parts[0]  # Breaks if collision counter present
```

---

## Migration and Compatibility

### Legacy Filename Formats

If migrating from a different feedback storage system, map old formats to new:

**Example migration:**
```python
# Old format: feedback-2025-11-11-143000-dev-ok.txt
# New format: 2025-11-11T14-30-00-command-success.md

def migrate_filename(old_filename: str) -> str:
    """Convert legacy filename to new format."""
    # Parse old format
    parts = old_filename.split("-")
    date = f"{parts[1]}-{parts[2]}-{parts[3]}"  # 2025-11-11
    time = parts[4]  # 143000
    time_formatted = f"{time[0:2]}-{time[2:4]}-{time[4:6]}"  # 14-30-00

    operation = map_operation(parts[5])  # "dev" → "command"
    status = map_status(parts[6])  # "ok" → "success"

    return f"{date}T{time_formatted}-{operation}-{status}.md"
```

---

## Related Documentation

- **Atomic Write Pattern:** `feedback-persistence-atomic-writes.md`
- **Configuration Guide:** `feedback-persistence-config-guide.md`
- **Directory Layouts:** `feedback-persistence-directory-layouts.md`
- **Error Reference:** `feedback-persistence-error-reference.md`
- **Edge Cases:** `feedback-persistence-edge-cases.md`

---

## Changelog

- **v1.0.0 (2025-11-11):** Initial specification
  - Filename pattern defined
  - Collision resolution algorithm documented
  - Cross-platform compatibility validated
  - Security validation rules established

---

**This specification is authoritative for all DevForgeAI feedback file persistence operations.**
