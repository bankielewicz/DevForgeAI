# Parameter Extraction Algorithm

## Context Markers

The `/document` command sets these context markers before invoking the skill:

| Marker | Type | Default | Description |
|--------|------|---------|-------------|
| `$STORY_ID` | string | empty | Story identifier (STORY-NNN) |
| `$DOC_TYPE` | string | "readme" | Documentation type to generate |
| `$MODE` | string | "greenfield" | Generation mode |
| `$EXPORT_FORMAT` | string | "markdown" | Output format |
| `$AUDIT_MODE` | string | null | Audit mode (only "dryrun" valid) |
| `$AUDIT_FIX` | boolean | false | Whether to apply audit fixes |
| `$FINDING_FILTER` | string | "all" | Specific finding ID (F-NNN) or "all" |

## Extraction Methods (in priority order)

### Method 1: Read from Command Context Markers
The `/document` command parses arguments and sets explicit context markers in the conversation. Look for patterns:
```
**Story ID:** STORY-NNN
**Documentation Type:** TYPE
**Mode:** MODE
**Export Format:** FORMAT
**Audit Mode:** AUDIT_MODE
**Audit Fix:** true/false
**Finding Filter:** FILTER
```

### Method 2: Search for File Reference Pattern
```
Grep(pattern="devforgeai/specs/Stories/STORY-[0-9]+", conversation_context)
```
Extract story ID from the file path if found.

### Method 3: Search for Explicit Statement
```
Grep(pattern="Story ID: STORY-[0-9]+", conversation_context)
```

### Method 4: Grep Conversation for Pattern
```
Grep(pattern="STORY-[0-9]+", conversation_context)
```
Use first match if unambiguous.

## Validation Rules

| Parameter | Valid Values | Validation |
|-----------|-------------|------------|
| `$STORY_ID` | STORY-NNN or empty | Must match `STORY-[0-9]+` pattern |
| `$DOC_TYPE` | readme, api, architecture, developer-guide, troubleshooting, roadmap, contributing, changelog, all | Must be in allowed list |
| `$MODE` | greenfield, brownfield | Must be one of two values |
| `$EXPORT_FORMAT` | markdown, html, pdf | Must be in allowed list |
| `$AUDIT_MODE` | dryrun or null | Only "dryrun" is supported |
| `$AUDIT_FIX` | true, false | Boolean |
| `$FINDING_FILTER` | F-NNN or "all" | Must match `F-[0-9]+` or be "all" |

## Default Resolution

```
IF $STORY_ID provided AND no type specified:
    $DOC_TYPE = "readme"
    $MODE = "greenfield"

IF no $STORY_ID AND no mode specified:
    $MODE = "brownfield"
    $DOC_TYPE = "all"

IF $AUDIT_MODE set:
    Override all other parameters -- audit path only

IF $AUDIT_FIX set:
    Override all other parameters -- fix path only
```
