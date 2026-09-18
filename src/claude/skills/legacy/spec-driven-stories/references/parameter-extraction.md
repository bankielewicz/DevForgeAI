# Parameter Extraction Reference

## Session ID Generation

Session IDs follow the pattern: `SC-YYYY-MM-DD-NNN`

- **SC**: Story Creation prefix
- **YYYY-MM-DD**: Current date
- **NNN**: Zero-padded sequence number (001-999)

### Generation Algorithm

```
1. Glob for existing checkpoints: devforgeai/workflows/checkpoints/SC-*.checkpoint.json
2. Filter to today's date: SC-{today}-*.checkpoint.json
3. Extract sequence numbers from matches
4. Find highest sequence number
5. Increment by 1 (or start at 001 if none exist)
6. Zero-pad to 3 digits
```

## Context Marker Extraction

Context markers are set by the invoking command (e.g., `/create-story`) and appear in the conversation as bold-prefixed lines.

### Extraction Pattern

```
FOR each marker in expected_markers:
  Search conversation for "**{Marker Name}:** {value}"
  Extract value (trimmed, after colon-space)
  Assign to corresponding variable
```

### Required Markers by Mode

| Mode | Required Markers | Optional Markers |
|------|------------------|------------------|
| SINGLE_STORY | Feature Description | Epic ID |
| EPIC_BATCH | Story ID, Epic ID, Feature Description, Feature Number, Feature Name, Priority, Points, Type, Sprint, Batch Mode, Batch Index | Depends On |

### Validation Rules

- `$STORY_ID`: Must match `STORY-\d+` pattern
- `$EPIC_ID`: Must match `EPIC-\d{3}` pattern (if set)
- `$PRIORITY`: Must be one of: Critical, High, Medium, Low
- `$POINTS`: Must be a Fibonacci number: 1, 2, 3, 5, 8, 13
- `$TYPE`: Must be one of: feature, documentation, bugfix, refactor
- `$SPRINT`: Must match `Sprint-\d+` or "Backlog"
- `$BATCH_MODE`: Must be "true" or "false"
- `$BATCH_INDEX`: Must be non-negative integer
