# Parameter Extraction: Context Markers

## Overview

The spec-driven-coverage skill receives its parameters via context markers set by the invoking slash command. These markers appear as bold-labeled lines in the conversation context immediately before the Skill() invocation.

---

## Context Marker Format

Markers follow the pattern:
```
**Label:** value
```

Example:
```
**Epic ID:** EPIC-015
**Mode:** validate
**Prompt Mode:** interactive
```

---

## Required Markers (All Modes)

| Marker | Format | Values | Description |
|--------|--------|--------|-------------|
| `**Epic ID:**` | EPIC-NNN or "all" | Any valid epic ID or literal "all" | Target epic for validation |
| `**Mode:**` | string | validate, detect, create | Determines which phases execute |

---

## Optional Markers (All Modes)

| Marker | Format | Default | Description |
|--------|--------|---------|-------------|
| `**Prompt Mode:**` | string | "interactive" | Controls interactive prompts (interactive, quiet, ci) |

---

## Create-Mode Markers

These markers are required only when Mode == "create":

| Marker | Format | Default | Description |
|--------|--------|---------|-------------|
| `**Sprint:**` | string | "Backlog" | Sprint assignment for created stories |
| `**Priority:**` | string | "Medium" | Priority for created stories |
| `**Points:**` | integer | 5 | Story points for created stories |
| `**Individual Priority:**` | boolean | false | If true, prompt user for priority per story |
| `**Individual Points:**` | boolean | false | If true, prompt user for points per story |
| `**Batch Mode:**` | boolean | true | Always true for create mode |
| `**Batch Total:**` | integer | — | Total number of gaps to create stories for |
| `**Created From:**` | string | — | Command that initiated batch creation |

---

## Extraction Algorithm

1. Scan conversation context backward from the Skill() invocation point
2. For each required marker, extract the value after the colon and space
3. Trim whitespace from extracted values
4. Apply type conversion (string → integer for Batch Total, Points; string → boolean for Individual flags)
5. If a required marker is missing: HALT with error listing the missing marker

---

## Epic ID Normalization (BR-001)

After extraction, normalize the Epic ID:
1. Convert to uppercase: `epic-015` → `EPIC-015`
2. Verify format: Must match `^EPIC-[0-9]{3}$` or be literal "all"
3. If format is invalid: HALT with error "Invalid epic ID format. Expected: EPIC-NNN"
