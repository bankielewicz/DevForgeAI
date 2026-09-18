<!-- MIRRORED FROM qa-validation.md LINES 26-28 - KEEP IN SYNC -->
<!-- Thresholds: business-logic=95%, application=85%, infrastructure=80% -->

# Coverage Planning Reference

Reference documentation for Phase 02 Step 2.2 (Coverage Planning) and Phase 04 Step 2b (Coverage Drift Detection).

This file documents:
- Layer classification rules for target files (Table 1)
- Target file extraction parser order (Table 2)
- Error-branch test estimation heuristic (Table 3)
- fallback_reason enum and classification_source enum
- coverage-plan.json schema (Table 5)
- Fallback modes and backward-compatibility contract

---

## Classification Rules

Table 1 maps every target file path to exactly one layer and one threshold. Rows are evaluated in order — the FIRST match wins, except under the straddle rule described below.

| Row | Pattern | Layer | Threshold | classification_source |
|-----|---------|-------|-----------|-----------------------|
| 1 | `src/core/**` | business-logic | 95 | path-rule-1 |
| 2 | `src/domain/**` | business-logic | 95 | path-rule-2 |
| 3 | `src/services/**` | business-logic | 95 | path-rule-3 |
| 4 | `src/claude/scripts/devforgeai_cli/validators/**` | business-logic | 95 | path-rule-4 |
| 5 | `src/claude/scripts/devforgeai_cli/commands/**` | application | 85 | path-rule-5 |
| 6 | `src/claude/scripts/devforgeai_cli/feedback/**` | application | 85 | path-rule-6 |
| 7 | `src/claude/scripts/devforgeai_cli/cli.py` | application | 85 | path-rule-7 |
| 8 | `src/claude/scripts/devforgeai_cli/**` | application | 85 | path-rule-8 |
| 9 | `src/adapters/**` | infrastructure | 80 | path-rule-9 |
| 10 | `src/infrastructure/**` | infrastructure | 80 | path-rule-10 |
| 11 | `src/repositories/**` | infrastructure | 80 | path-rule-11 |
| 12 | `src/claude/hooks/**` | infrastructure | 80 | path-rule-12 |
| 13 | `*.md` | n/a | n/a | skip: non-code-file |
| 14 | `tests/**` | n/a | n/a | skip: test files |
| 15 | Any other | application (default) | 85 | default-application |

### Straddle Rule (stricter threshold wins)

When a file path matches two rules in rows 1-12, pick the STRICTER (higher) threshold — the row with the larger threshold value wins, regardless of row order. This is the straddle rule.

Example: a file under `src/claude/scripts/devforgeai_cli/validators/` matches both row 4 (business-logic, 95%) and row 8 (application, 85%) because the validators path is nested under the devforgeai_cli directory. Row 4 wins because stricter 95% beats 85%. The classification_source for this file is `path-rule-4`.

Summary: first match wins for unrelated rules, stricter threshold wins when two rows straddle the same path.

### classification_source enum

The `classification_source` field on every target entry MUST be one of:

- `"path-rule-N"` — matched one of rows 1-12 above (N is the row number)
- `"technical-spec-layer-field"` — layer was explicitly declared in the story technical specification `layer:` field
- `"default-application"` — matched row 15 (catch-all default application/85%)
- `"user-override"` — user provided a manual classification override

### Default / Catch-all Rule

Row 15 is the default catch-all: any file that does not match rows 1-14 is classified as application/85% with `classification_source = "default-application"`. This guarantees every source file has a classification.

---

## Target File Extraction Parser Order

Table 2 defines the ordered parser chain for `extract_target_files(story_content)`. Parsers run in order — the FIRST non-empty result wins.

| Order | Parser | Description |
|-------|--------|-------------|
| 1 | YAML fence parser | Parse a fenced ```yaml block containing `technical_specification:` key with `file_path:` entries |
| 2 | Markdown Table parser | Parse a markdown table whose header row contains "Source Files Guidance" or a `\| File \|` column |
| 3 | Files Created/Modified parser | Parse the `### Files Created/Modified` section bullet list |
| 4 | DoD inline backtick parser | Scan the DoD section for inline backtick paths ending in `.py`, `.md`, `.ts`, `.js`, or `.sh` |
| 5 | Fallback | Return `targets=[]` with `fallback_reason="target-extraction-failed"` |

### Parser 1: YAML Fence

Parser 1 scans for a YAML fence with `technical_specification` and extracts every `file_path` entry. Example source:

```
technical_specification:
  files:
    - file_path: src/core/example.py
      layer: business-logic
```

### Parser 2: Markdown Table

Parser 2 scans for a markdown table with a "Source Files Guidance" header or a `| File |` column and extracts paths from the File column.

### Parser 3: Files Created/Modified Section

Parser 3 reads the `### Files Created/Modified` heading and collects bullet list entries under it.

### Parser 4: DoD Inline Backticks

Parser 4 scans the Definition of Done section for inline backticks enclosing file paths with approved extensions (`.py`, `.md`, `.ts`, `.js`, `.sh`).

### Parser 5: Fallback

If parsers 1-4 produce an empty result, return `targets=[]` and set `fallback_reason="target-extraction-failed"`.

### fallback_reason enum

The `fallback_reason` top-level field MUST be one of:

- `null` — plan generated normally (targets[] is non-empty)
- `"target-extraction-failed"` — all parsers returned an empty list
- `"no-layer-classifiable-files"` — parsers returned files but every file was filtered out (rows 13-14 skip rules)
- `"story-file-unreadable"` — the story file could not be read
- `"user-requested-fallback"` — user override requested explicit fallback mode

---

## Error Branch Estimation (Table 3)

The required number of error-branch tests for a target file is computed by the clamp formula:

```
base = 2 + edge_cases + functions
required_error_branch_tests = clamp(base, 2, 8)
```

Equivalently:

```
required_error_branch_tests = max(2, min(8, base))
```

Where:
- `base = 2` is the starting value (minimum 2 error-branch tests per file)
- `edge_cases` is the number of edge cases listed in the story for this file
- `functions` is the count of functions declared in the technical specification for this file
- `clamp(base, 2, 8)` enforces a floor of 2 and a ceiling of 8 error-branch tests per file

The clamp floor of 2 guarantees a minimum of 2 error-branch tests even for trivial files. The clamp ceiling of 8 (maximum 8) prevents runaway test generation for files with many functions or edge cases.

### Examples

- Simple file: `base = 2 + 0 edge_cases + 0 functions = 2` → `clamp(2, 2, 8) = 2`
- Typical file: `base = 2 + 1 edge_case + 3 functions = 6` → `clamp(6, 2, 8) = 6`
- Complex file: `base = 2 + 5 edge_cases + 10 functions = 17` → `clamp(17, 2, 8) = 8`

---

## JSON Schema

Table 5: `coverage-plan.json` canonical schema. The plan file is written by Phase 02 Step 2.2 to `tmp/${STORY_ID}/coverage-plan.json` and consumed by test-automator and Phase 04 drift detection.

```json
{
  "$schema": "coverage-plan-v1",
  "story_id": "STORY-NNN",
  "generated_at": "2026-04-10T12:00:00Z",
  "fallback_reason": null,
  "targets": [
    {
      "file": "src/claude/scripts/devforgeai_cli/commands/example.py",
      "layer": "application",
      "threshold_pct": 85,
      "required_error_branch_tests": 5,
      "classification_source": "path-rule-8"
    }
  ],
  "total_expected_coverage_pct": 85.0,
  "plan_version": "1.0"
}
```

### Required Top-Level Fields (7)

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `$schema` | string | yes | Schema version identifier, always `"coverage-plan-v1"` |
| `story_id` | string | yes | Story identifier (e.g., `"STORY-NNN"`) |
| `generated_at` | string (ISO 8601) | yes | UTC timestamp when the plan was generated |
| `fallback_reason` | string or null | yes | Null when plan generated normally; enum value when in fallback mode |
| `targets` | array of target entries | yes | List of target files with classification and thresholds |
| `total_expected_coverage_pct` | number or null | yes | Arithmetic mean of target threshold_pct values; null when targets=[] |
| `plan_version` | string | yes | Plan schema version, always `"1.0"` |

### Required Target Entry Fields (5)

Each entry in the `targets[]` array MUST contain these fields:

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `file` | string | yes | Relative file path of the target |
| `layer` | string | yes | One of `"business-logic"`, `"application"`, `"infrastructure"` |
| `threshold_pct` | integer | yes | Coverage threshold percentage from the layer mapping |
| `required_error_branch_tests` | integer | yes | Number of error-branch tests required (clamp result) |
| `classification_source` | string | yes | One of the enum values documented above |

---

## Fallback Modes

This section documents the fallback contracts required by the AC#3 backward-compatibility guarantee.

### When Fallback Engages

Fallback mode engages when:

1. The story file cannot be read (`fallback_reason = "story-file-unreadable"`)
2. Every parser in Table 2 returns an empty list (`fallback_reason = "target-extraction-failed"`)
3. Every extracted file is filtered out by skip rules rows 13-14 (`fallback_reason = "no-layer-classifiable-files"`)
4. User explicitly requests fallback (`fallback_reason = "user-requested-fallback"`)

### Fallback Plan Example

In fallback mode, the plan is still written to `tmp/${STORY_ID}/coverage-plan.json` with `targets=[]` and a non-null `fallback_reason`:

```json
{
  "$schema": "coverage-plan-v1",
  "story_id": "STORY-NNN",
  "generated_at": "2026-04-10T12:00:00Z",
  "fallback_reason": "no-layer-classifiable-files",
  "targets": [],
  "total_expected_coverage_pct": null,
  "plan_version": "1.0"
}
```

### Consumer Behavior in Fallback Mode

- **test-automator**: When `targets=[]`, fall back to pre-STORY-632 AC-driven test generation. Do NOT HALT. Do NOT refuse to run.
- **Phase 04 drift detection**: When `targets=[]` or the plan file is missing, skip drift detection and fall back to the current ADR-010 threshold-based behavior.
- **ADR-010**: Unchanged. Coverage threshold enforcement remains a CRITICAL blocker regardless of whether a coverage plan exists. Drift detection is ADDITIVE and OBSERVATIONAL — it does not replace ADR-010 blocking behavior.

### Backward Compatibility Contract

A missing or empty `coverage-plan.json` MUST NOT break the existing dev workflow. Stories authored before STORY-632 have no `technical_specification` YAML and may trip Parser 5 (fallback). The result is a fallback plan with `targets=[]` and the workflow proceeds identically to pre-STORY-632 behavior.
