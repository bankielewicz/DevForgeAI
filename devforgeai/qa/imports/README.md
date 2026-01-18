# QA Report Imports

This directory contains QA gap files imported from external projects for framework enhancement analysis.

## Purpose

Import QA reports from other projects using DevForgeAI to:
1. Identify common patterns across projects
2. Create framework improvement stories
3. Learn from external project QA findings

## How to Import

### Step 1: Copy Gap Files

Copy `*-gaps.json` files from external projects:

```bash
# From external project
cp /path/to/project/devforgeai/qa/reports/*-gaps.json \
   /path/to/DevForgeAI2/devforgeai/qa/imports/

# Or copy specific story
cp /path/to/project/devforgeai/qa/reports/STORY-004-gaps.json \
   devforgeai/qa/imports/treelint-STORY-004-gaps.json
```

### Step 2: (Optional) Copy QA Reports

Copy corresponding markdown reports for context:

```bash
cp /path/to/project/devforgeai/qa/reports/*-qa-report.md \
   devforgeai/qa/imports/
```

### Step 3: Run Review Command

```bash
/review-qa-reports --source imports
```

## File Naming Convention

When importing, prefix files with project name for clarity:

| Original | Imported |
|----------|----------|
| `STORY-004-gaps.json` | `treelint-STORY-004-gaps.json` |
| `STORY-007-qa-report.md` | `myproject-STORY-007-qa-report.md` |

## Expected File Format

Gap files must follow the standard DevForgeAI QA gap schema:

```json
{
  "story_id": "STORY-XXX",
  "qa_result": "FAILED|PASSED",
  "coverage_gaps": [...],
  "anti_pattern_violations": [...],
  "remediation_sequence": [...]
}
```

See `devforgeai/qa/reports/` for examples from this project.

## Processing

Imported files are processed by `/review-qa-reports --source imports`:
- Parsed and validated
- Gaps aggregated and prioritized
- Selected gaps converted to stories
- Stories target DevForgeAI framework improvement

## Notes

- Imported files are NOT modified (source updates disabled for imports)
- Stories created reference the imported gap file as source
- RCA files should go in `devforgeai/RCA/imports/` instead
