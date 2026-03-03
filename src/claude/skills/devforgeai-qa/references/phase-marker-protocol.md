# Phase Marker Protocol [STORY-126 Enhancement]

**Purpose:** Write marker files after each phase completes to enable sequential verification.

**Constitution Alignment:** All-or-Nothing Principle (architecture-constraints.md line 246)

### Marker File Format

```yaml
# Location: devforgeai/qa/reports/{STORY_ID}/.qa-phase-{N}.marker
phase: {N}
story_id: {STORY_ID}
mode: {MODE}
timestamp: {ISO_8601}
status: complete
```

### Marker Write (End of Each Phase)

```
Write(file_path="devforgeai/qa/reports/{STORY_ID}/.qa-phase-{N}.marker",
      content="phase: {N}\nstory_id: {STORY_ID}\nmode: {MODE}\ntimestamp: {TIMESTAMP}\nstatus: complete")

Display: "✓ Phase {N} marker written"
```

### Pre-Flight Verification (Start of Phases 1-4)

```
Glob(pattern="devforgeai/qa/reports/{STORY_ID}/.qa-phase-{N-1}.marker")

IF NOT found:
    Display: "❌ Phase {N-1} marker not found"
    Display: "   Previous phase may not have completed"
    HALT: "Run phases in sequence. Start from Phase {N-1}"
ELSE:
    Read marker and verify story_id matches
    Display: "✓ Phase {N-1} verified complete"
```
