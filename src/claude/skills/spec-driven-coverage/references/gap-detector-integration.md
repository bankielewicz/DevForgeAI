# Gap Detector Integration

## Overview

The spec-driven-coverage skill invokes two shell scripts for gap detection and report generation. These scripts are operational tools — not modified by the skill — and are invoked via Bash() with restricted allowed-tools patterns.

---

## gap-detector.sh

**Path:** `devforgeai/traceability/gap-detector.sh`
**Story:** STORY-085 (Gap Detection Engine)
**Invocation:**
```
# Single epic:
Bash(command="devforgeai/traceability/gap-detector.sh EPIC-015 2>&1")

# All epics:
Bash(command="devforgeai/traceability/gap-detector.sh 2>&1")
```

**Three Validation Strategies:**
1. **Strategy 1:** Extract epic fields from story YAML frontmatter — builds story-to-epic mapping
2. **Strategy 2:** Parse epic Stories tables — extracts feature numbers, titles, points, status from pipe-delimited tables
3. **Strategy 3:** Cross-validate bidirectional consistency — checks both story→epic and epic→story directions

**Output:** JSON report with:
- `consistency_score` — matched / total relationships
- `story_count` — total stories found
- `mismatch_count` — bidirectional mismatches
- `orphan_count` — stories referencing non-existent epics
- `missing_features` — features in epic with no story
- `total_features` — total features across epics
- `covered_features` — features with matching stories
- `coverage_percentage` — covered / total * 100

**Error Handling:**
- Exit code 0: Success, JSON output on stdout
- Exit code 1: Script error (missing dependencies, file access issues)
- Exit code 127: Script not found — HALT with path error

---

## generate-report.sh

**Path:** `devforgeai/epic-coverage/generate-report.sh`
**Story:** STORY-086 (Coverage Reporting System)
**Invocation:**
```
Bash(command="devforgeai/epic-coverage/generate-report.sh 2>&1")
```

**Eight Internal Phases:**
1. Parse Epics — extract metadata and features from epic files
2. Parse Stories — build story-to-epic mapping
3. Calculate Statistics — compute coverage percentages (BR-002 applied)
4. Generate Terminal Output — colored per-epic breakdown
5. Generate Markdown Report — timestamped report with summary stats
6. Generate JSON Export — structured JSON with actionable steps
7. Generate Actionable Next Steps — top 10 /create-story commands
8. Persist History — append to coverage-history.json (idempotent)

**Output Formats:** terminal (default), markdown, JSON
**Color Coding:** GREEN (100%), YELLOW (50-99%), RED (<50%)

**Error Handling:**
- Exit code 0: Success
- Exit code 1: Script error
- Exit code 127: Script not found — continue without report (report is supplementary to gap detection)

---

## Confidence Scoring

The gap-detector.sh supports confidence scoring integration:
- Low-confidence matches (60-75%) are excluded from coverage counts
- High-confidence matches (>75%) count as covered
- Confidence scoring helps with fuzzy feature-to-story title matching
