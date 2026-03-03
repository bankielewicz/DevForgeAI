# /create-stories-from-rca - Extended Reference Documentation

Supplementary documentation for the `/create-stories-from-rca` command. The command file contains core workflow logic; this file contains detailed documentation, templates, and constraints.

---

## Full Help Text

```
/create-stories-from-rca - Create user stories from RCA recommendations

USAGE:
    /create-stories-from-rca RCA-NNN [--threshold HOURS]
    /create-stories-from-rca --help | help

ARGUMENTS:
    RCA-NNN         Required. RCA document ID (e.g., RCA-022). Case-insensitive.

OPTIONS:
    --threshold N   Filter recommendations with effort >= N hours
    --help, help    Display this help message

PROCESS:
    1. Parse RCA document and extract recommendations
    2. Filter by effort threshold and sort by priority
    3. Display summary table for interactive selection
    4. Create stories for selected recommendations
    5. Update RCA document with story links

RELATED COMMANDS:
    /rca            Create new RCA document
    /create-story   Create individual story
    /brainstorm     Transform business ideas
    /dev            Start story implementation
```

---

## Error Message Templates

```
ERROR_MISSING_RCA_ID:
    "❌ RCA ID required"
    "Usage: /create-stories-from-rca RCA-NNN"
    "Available RCAs:"

ERROR_RCA_NOT_FOUND:
    "❌ RCA not found: ${RCA_ID}"
    "Available RCAs:"

ERROR_INVALID_FORMAT:
    "❌ Invalid RCA format"
    "Expected: RCA-NNN (where NNN are 3 digits)"
```

---

## Phase Orchestration Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                  /create-stories-from-rca Workflow               │
│                    (4 Main Orchestration Phases)                 │
└─────────────────────────────────────────────────────────────────┘

Phase 1-5: RCA PARSING (STORY-155)
  ├─ Input: RCA ID (e.g., RCA-022)
  ├─ Process: Parse document, extract recommendations
  ├─ Output: Structured recommendation list
  └─ Reference: parsing-workflow.md

       ↓

Phase 6-9: INTERACTIVE SELECTION (STORY-156)
  ├─ Input: Parsed recommendations
  ├─ Process: Present to user, get selection
  ├─ Output: Selected recommendations
  └─ Reference: selection-workflow.md

       ↓

Phase 10: BATCH STORY CREATION (STORY-157)
  ├─ Input: Selected recommendations
  ├─ Process: Create stories with context
  ├─ Output: Array of created story IDs
  └─ Reference: batch-creation-workflow.md

       ↓

Phase 11: RCA-STORY LINKING (STORY-158)
  ├─ Input: Created story IDs
  ├─ Process: Update RCA document with links
  ├─ Output: Updated RCA with traceability
  └─ Reference: linking-workflow.md
```

| Phase | Component | Story | Role |
|-------|-----------|-------|------|
| 1-5 | RCA Parser | STORY-155 | Parse RCA and extract recommendations |
| 6-9 | Selection | STORY-156 | Interactive recommendation selection |
| 10 | Batch Creator | STORY-157 | Create stories in batch mode |
| 11 | Linker | STORY-158 | Link stories back to RCA document |

---

## Business Rules & Constraints

| Rule | Constraint | Implementation | Phase |
|------|-----------|-----------------|-------|
| BR-001: Effort Threshold | Filter recommendations with effort >= threshold hours | Applied in Phase 1-5 parsing | Parsing |
| BR-002: Priority Sorting | Sort recommendations by priority: CRITICAL > HIGH > MEDIUM > LOW | Applied in Phase 1-5 parsing | Parsing |
| BR-003: Story Points Mapping | 1 story point = 4 hours of effort | Used in batch creation | Phase 10 |
| BR-004: Failure Isolation | Continue processing remaining items on individual failures | Applied throughout workflow | All Phases |
| BR-005: Size Limit | Command file < 15,000 characters (lean orchestration) | Design constraint | File |
| BR-006: Case Normalization | Accept case-insensitive RCA IDs (rca-022 → RCA-022) | Applied in argument parsing | Parsing |
| BR-007: File Existence | Verify RCA file exists before processing | Check in argument parsing | Parsing |

---

## Edge Cases

| Edge Case | Behavior |
|-----------|----------|
| Missing frontmatter | Extract ID from filename |
| No recommendations | Display message, exit |
| All filtered | "No recommendations meet threshold" |
| Invalid REC ID | Log warning, ignore |

---

## Error Handling

| Error Type | Handling |
|------------|----------|
| Validation Error | Log, continue to next |
| Skill Error | Log, continue to next |
| ID Conflict | Increment, retry once |

---

## Implementation Reference Files

All detailed phase workflows are documented in dedicated reference files for maintainability and modularity.

### Phase Reference Files

| Phase | Component | File | Purpose |
|-------|-----------|------|---------|
| 1-5 | RCA Parser | `references/create-stories-from-rca/parsing-workflow.md` | RCA parsing, extraction, filtering algorithm |
| 6-9 | Selection | `references/create-stories-from-rca/selection-workflow.md` | Interactive user selection process |
| 10 | Batch Creator | `references/create-stories-from-rca/batch-creation-workflow.md` | Story batch creation and context mapping |
| 11 | Linker | `references/create-stories-from-rca/linking-workflow.md` | RCA document update and story linking |

**Note:** All reference files are located at: `.claude/commands/references/create-stories-from-rca/`

---

**Version:** 2.0 - Lean Orchestration Reference | **Source:** Extracted from create-stories-from-rca.md v1.0
