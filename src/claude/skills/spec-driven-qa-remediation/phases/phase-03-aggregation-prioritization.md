# Phase 03: Aggregation & Prioritization

## Entry Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-check ${SESSION_ID} --workflow=qa-remediation --from=02 --to=03 --project-root=. 2>&1
```

| Exit Code | Action |
|-----------|--------|
| 0 | Phase 02 complete. Proceed. |
| 1 | Phase 02 incomplete. HALT. |
| 2 | Validation error. HALT. |
| 127 | CLI not installed. Proceed without enforcement. |

---

## Contract

| Field | Value |
|-------|-------|
| **PURPOSE** | Deduplicate, score, filter, and sort gaps for processing |
| **REFERENCE** | `references/gap-aggregation-algorithm.md` |
| **STEP COUNT** | 6 mandatory steps |

---

## Phase Exit Criteria

- [ ] `$UNIQUE_GAPS` populated
- [ ] `$FILTERED_GAPS` sorted by score descending
- [ ] `$DEFERRED_GAPS` captured for Phase 07
- [ ] `$GAPS_DEDUPLICATED` count computed
- [ ] `$GAPS_ABOVE_THRESHOLD` count computed
- [ ] Checkpoint updated

IF any unchecked: HALT -- "Phase 03 exit criteria not met"

---

## Reference Loading [MANDATORY]

```
Read(file_path="src/claude/skills/spec-driven-qa-remediation/references/gap-aggregation-algorithm.md")
```

IF Read fails: HALT -- "Phase 03 reference file not loaded. Cannot proceed without gap aggregation algorithm reference."

Do NOT rely on memory of previous reads. Load reference fresh.

---

## Mandatory Steps (6)

### Step 3.1: Load Reference

**EXECUTE:**
```
Read(file_path="src/claude/skills/spec-driven-qa-remediation/references/gap-aggregation-algorithm.md")

Parse and internalize:
  - Deduplication key algorithm
  - Priority score calculation formula
  - Severity weights and type modifiers
  - Filtering logic (severity threshold, blocking-only)
  - Sort order (primary: score descending, secondary: type priority)

Display: "Gap aggregation algorithm reference loaded"
```

**VERIFY:** Reference content loaded and contains deduplication, scoring, and filtering sections.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=03 --step=3.1 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.1")`

---

### Step 3.2: Deduplicate Gaps

**EXECUTE:**
```
$UNIQUE_GAPS = {}
$DUPLICATE_COUNT = 0

FOR each gap in $ALL_GAPS:
    # Generate deduplication key
    normalized_desc = lowercase(strip_whitespace(gap.description))
    dedup_key = "{gap.file}:{gap.type}:{normalized_desc}"

    IF dedup_key in $UNIQUE_GAPS:
        # Merge: keep highest severity
        existing = $UNIQUE_GAPS[dedup_key]
        severity_rank = { "CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1 }

        IF severity_rank[gap.severity] > severity_rank[existing.severity]:
            existing.severity = gap.severity

        # Merge sources
        existing.sources.append({
            source_file: gap.source_file,
            source_story: gap.source_story
        })

        # Increment occurrence count
        existing.occurrences += 1

        # Merge blocking: if ANY source says blocking, it is blocking
        IF gap.blocking == true:
            existing.blocking = true

        $DUPLICATE_COUNT += 1
    ELSE:
        $UNIQUE_GAPS[dedup_key] = {
            ...gap,
            sources: [{
                source_file: gap.source_file,
                source_story: gap.source_story
            }],
            occurrences: 1
        }

$GAPS_DEDUPLICATED = $DUPLICATE_COUNT
$UNIQUE_GAPS_LIST = values($UNIQUE_GAPS)

Display: "Deduplication complete:"
Display: "  Input gaps: ${len($ALL_GAPS)}"
Display: "  Unique gaps: ${len($UNIQUE_GAPS_LIST)}"
Display: "  Duplicates removed: ${GAPS_DEDUPLICATED}"
```

**VERIFY:** `$UNIQUE_GAPS_LIST` has `len($ALL_GAPS) - $GAPS_DEDUPLICATED` entries. No duplicate keys remain.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=03 --step=3.2 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.2")`

---

### Step 3.3: Calculate Priority Scores

**EXECUTE:**
```
# Severity base weights
SEVERITY_WEIGHTS = {
    "CRITICAL": 100,
    "HIGH": 75,
    "MEDIUM": 50,
    "LOW": 25
}

# Type modifiers
TYPE_MODIFIERS = {
    "deferral": 25,
    "anti_pattern": 0,      # Base; security sub-type gets +15 below
    "coverage_gap": 0,      # Base; layer-specific below
    "code_quality": 5       # Complexity modifier
}

FOR each gap in $UNIQUE_GAPS_LIST:
    score = 0

    # 1. Severity base weight
    score += SEVERITY_WEIGHTS[gap.severity]

    # 2. Type modifier
    score += TYPE_MODIFIERS[gap.type]

    # 3. Sub-type modifiers
    IF gap.type == "anti_pattern":
        IF gap.details.type in ["sql_injection", "hardcoded_secret", "xss"]:
            score += 15    # Security anti-pattern bonus

    IF gap.type == "coverage_gap":
        IF gap.details.layer == "Business Logic":
            score += 10    # Business Logic coverage bonus
        ELIF gap.details.layer == "Application":
            score += 5     # Application coverage bonus

    # 4. Occurrence bonus (capped at 10)
    occurrence_bonus = min(gap.occurrences * 2, 10)
    score += occurrence_bonus

    gap.score = score

Display: "Priority scores calculated for ${len($UNIQUE_GAPS_LIST)} gaps"
Display: "  Score range: {min_score} - {max_score}"
```

**VERIFY:** Every entry in `$UNIQUE_GAPS_LIST` has a numeric `score` field > 0.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=03 --step=3.3 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.3")`

---

### Step 3.4: Filter by Severity Threshold

**EXECUTE:**
```
# Severity ordering for threshold comparison
SEVERITY_ORDER = { "CRITICAL": 4, "HIGH": 3, "MEDIUM": 2, "LOW": 1 }
threshold_rank = SEVERITY_ORDER[$MIN_SEVERITY]

$FILTERED_GAPS = []
$DEFERRED_GAPS = []

FOR each gap in $UNIQUE_GAPS_LIST:
    gap_rank = SEVERITY_ORDER[gap.severity]

    IF gap_rank >= threshold_rank:
        $FILTERED_GAPS.append(gap)
    ELSE:
        $DEFERRED_GAPS.append(gap)

$GAPS_ABOVE_THRESHOLD = len($FILTERED_GAPS)

Display: "Severity filter applied (threshold: ${MIN_SEVERITY}):"
Display: "  Above threshold: ${GAPS_ABOVE_THRESHOLD}"
Display: "  Below threshold (deferred): ${len($DEFERRED_GAPS)}"

IF $GAPS_ABOVE_THRESHOLD == 0:
    Display: "Warning: No gaps meet the severity threshold. Consider lowering --min-severity."
    # Not a HALT -- Phase 04 will handle empty selection gracefully
```

**VERIFY:** `$FILTERED_GAPS` + `$DEFERRED_GAPS` == `$UNIQUE_GAPS_LIST` count. Every gap in `$FILTERED_GAPS` has severity >= `$MIN_SEVERITY`. Every gap in `$DEFERRED_GAPS` has severity < `$MIN_SEVERITY`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=03 --step=3.4 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.4")`

---

### Step 3.5: Apply Blocking-Only Filter

**EXECUTE:**
```
$ADVISORY_HIDDEN_COUNT = 0

IF $BLOCKING_ONLY == true:
    $PRE_FILTER_COUNT = len($FILTERED_GAPS)
    $BLOCKING_FILTERED = []

    FOR each gap in $FILTERED_GAPS:
        IF gap.blocking == true:
            $BLOCKING_FILTERED.append(gap)
        ELSE:
            $ADVISORY_HIDDEN_COUNT += 1

    $FILTERED_GAPS = $BLOCKING_FILTERED

    Display: "--blocking-only filter applied (AND logic with severity):"
    Display: "  Before filter: ${PRE_FILTER_COUNT}"
    Display: "  After filter (blocking only): ${len($FILTERED_GAPS)}"
    Display: "  Advisory gaps hidden: ${ADVISORY_HIDDEN_COUNT}"

ELSE:
    Display: "Blocking-only filter: not active (showing all severities)"
    $ADVISORY_HIDDEN_COUNT = 0

# Update count after blocking filter
$GAPS_ABOVE_THRESHOLD = len($FILTERED_GAPS)
```

**VERIFY:** If `$BLOCKING_ONLY == true`: all entries in `$FILTERED_GAPS` have `blocking == true`. `$ADVISORY_HIDDEN_COUNT` reflects count of advisory gaps removed. If `$BLOCKING_ONLY == false`: `$FILTERED_GAPS` unchanged, `$ADVISORY_HIDDEN_COUNT == 0`.

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=03 --step=3.5 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.5")`

---

### Step 3.6: Sort by Score

**EXECUTE:**
```
# Type priority for secondary sort (tiebreaker)
TYPE_PRIORITY = {
    "deferral": 1,        # Highest priority
    "anti_pattern": 2,
    "coverage_gap": 3,
    "code_quality": 4     # Lowest priority
}

# Sort $FILTERED_GAPS
$FILTERED_GAPS = sort($FILTERED_GAPS, key=lambda gap: (
    -gap.score,                       # Primary: score descending
    TYPE_PRIORITY[gap.type]           # Secondary: type priority ascending
))

# Also sort $DEFERRED_GAPS for Phase 07 consumption
$DEFERRED_GAPS = sort($DEFERRED_GAPS, key=lambda gap: (
    -gap.score,
    TYPE_PRIORITY[gap.type]
))

Display: "Gaps sorted by priority score (descending):"
Display: "  Top 5 filtered gaps:"
FOR i, gap in enumerate($FILTERED_GAPS[:5]):
    Display: "    {i+1}. [{gap.severity}] {gap.type} - {gap.description} (score: {gap.score})"

IF len($FILTERED_GAPS) > 5:
    Display: "    ... and ${len($FILTERED_GAPS) - 5} more"
```

**VERIFY:** `$FILTERED_GAPS` is sorted by `score` descending. First entry has highest score. Ties broken by type priority (deferral > anti_pattern > coverage_gap > code_quality).

**RECORD:**
```bash
source .venv/bin/activate && devforgeai-validate phase-record ${SESSION_ID} --workflow=qa-remediation --phase=03 --step=3.6 --project-root=. 2>&1
```
Update checkpoint: `phases["03"].steps_completed.append("3.6")`

---

## Phase Exit Verification

```
Verify all exit criteria:
1. $UNIQUE_GAPS_LIST populated (len >= 1)                -> CHECK
2. $FILTERED_GAPS sorted by score descending             -> CHECK
3. $DEFERRED_GAPS captured for Phase 07                  -> CHECK
4. $GAPS_DEDUPLICATED count computed                     -> CHECK
5. $GAPS_ABOVE_THRESHOLD count computed                  -> CHECK

Update checkpoint:
  progress.current_phase = 3
  progress.phases_completed.append("03")
  phases["03"].status = "completed"

IF any check fails: HALT -- "Phase 03 exit verification failed on: {failed_criteria}"

Display:
"Phase 03 Complete: Aggregation & Prioritization"
"  Unique Gaps: ${len($UNIQUE_GAPS_LIST)}"
"  Duplicates Removed: ${GAPS_DEDUPLICATED}"
"  Above Threshold: ${GAPS_ABOVE_THRESHOLD}"
"  Deferred (below threshold): ${len($DEFERRED_GAPS)}"
"  Advisory Hidden: ${ADVISORY_HIDDEN_COUNT}"
"  Proceeding to Phase 04: Interactive Selection..."
```

## Exit Gate

```bash
source .venv/bin/activate && devforgeai-validate phase-complete ${SESSION_ID} --workflow=qa-remediation --phase=03 --checkpoint-passed --project-root=. 2>&1
# Exit 0: proceed to Phase 04 | Exit 1: HALT
```
