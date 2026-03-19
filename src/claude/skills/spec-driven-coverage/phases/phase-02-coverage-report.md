# Phase 02: Coverage Report

**Purpose:** Run the coverage report generator script and prepare structured report data with statistics per epic.

**Mode:** validate only (skip this phase for detect and create modes)

**Pre-Flight:** Verify Phase 01 completed and gap_data is available.

---

## Step 2.1: Verify Phase 01 Completion

**EXECUTE:**
Check that gap_data from Phase 01 is available in working memory.

**VERIFY:**
- gap_data object exists
- gap_data.total_features is populated
- If gap_data is missing: HALT — Phase 01 did not complete correctly

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=02 --step=2.1 --project-root=. 2>&1")
```

---

## Step 2.2: Run Coverage Report Generator

**EXECUTE:**
```
Bash(command="devforgeai/epic-coverage/generate-report.sh 2>&1")
```

This script generates coverage reports in terminal, markdown, and JSON formats with historical tracking. It executes 8 internal phases:
1. Parse Epics — extract metadata and features
2. Parse Stories — build story-to-epic mapping
3. Calculate Statistics — compute coverage percentages (BR-002 applied)
4. Generate Terminal Output — colored per-epic breakdown
5. Generate Markdown Report — timestamped report
6. Generate JSON Export — structured data with actionable steps
7. Generate Actionable Next Steps — top 10 /create-story commands
8. Persist History — append to coverage-history.json

**VERIFY:**
- Command executed successfully (exit code 0)
- Output contains coverage statistics
- If script not found (exit code 127): Continue with gap_data from Phase 01 (report generator is supplementary)

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=02 --step=2.2 --project-root=. 2>&1")
```

---

## Step 2.3: Parse Report Statistics

**EXECUTE:**
Extract per-epic statistics from the report generator output:

```
report_data = {
    epics: [
        {
            epic_id: "EPIC-NNN",
            total_features: <integer>,
            covered_features: <integer>,
            coverage_percentage: <float>,
            status_breakdown: {
                released: <count>,
                qa_approved: <count>,
                dev_complete: <count>,
                in_progress: <count>,
                backlog: <count>
            }
        }
    ],
    framework_summary: {
        total_epics: <integer>,
        total_features: <integer>,
        total_covered: <integer>,
        overall_coverage: <float>
    }
}
```

Merge report_data with gap_data from Phase 01 for comprehensive coverage view.

**VERIFY:**
- report_data.epics is a non-empty array (for all-epics mode) or contains the target epic (for single-epic mode)
- report_data.framework_summary.overall_coverage is between 0.0 and 100.0

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=02 --step=2.3 --project-root=. 2>&1")
```

---

## Step 2.4: Prepare Display Data

**EXECUTE:**
Combine gap_data and report_data into a unified display_data object for Phase 03:

```
display_data = {
    mode: "single-epic" | "all-epics",
    epic_id: EPIC_ID,
    gap_data: gap_data,
    report_data: report_data,
    visual_indicators: {
        green_threshold: 100,    # 100% coverage
        yellow_threshold: 50,    # 50-99% coverage
        red_threshold: 0         # <50% coverage
    }
}
```

**VERIFY:**
- display_data object is populated
- display_data.mode matches EPIC_ID (single-epic if specific ID, all-epics if "all")

**RECORD:**
```
Bash(command="devforgeai-validate phase-record ${IDENTIFIER} --phase=02 --step=2.4 --project-root=. 2>&1")
```

---

## Phase 02 Completion

**EXECUTE:**
```
Bash(command="devforgeai-validate phase-complete ${IDENTIFIER} --phase=02 --project-root=. 2>&1")
```

**VERIFY:**
- Exit code 0 or 2 (backward compatibility)

**NEXT:** Proceed to Phase 03 (Display Formatting)
