---
name: story-discovery-from-recommendations
description: FROM_RECOMMENDATIONS mode flow for Phase 01 — ingest qa-recommendations.md, interactively select recs, emit batch-mode context markers
version: "1.0"
---

# Story Discovery — FROM_RECOMMENDATIONS Mode

Triggered when `/create-story --from-recommendations=STORY-NNN` is invoked. The command sets 4 context markers (`$MODE = FROM_RECOMMENDATIONS`, `$SOURCE_STORY_ID`, `$REC_IDS_FLAG`, `$INCLUDE_BLOCKING`); everything else — status check, HALT gates, severity filter, interactive selection, full-entry fetch, epic resolution, mapping, feature_description rendering, marker emission — happens here.

## Purpose

Transform selected `REC-STORY-NNN-{C|H|M|L}-NNN` entries from `devforgeai/qa/recommendations/{SOURCE_STORY_ID}-qa-recommendations.md` into batch-mode context markers consumed by spec-driven-stories Phases 02-06. This enables follow-up hardening stories to be generated with zero-drift provenance back to the QA cycle that surfaced the recommendations.

---

## Cold-Start Self-Sufficiency Guarantee

This reference requires ONLY three on-disk artifacts — **no session memory, no prior chat context**:

1. `devforgeai/qa/recommendations/${SOURCE_STORY_ID}-qa-recommendations.md` (emitted by `/qa` Phase 05)
2. `devforgeai/specs/Stories/${SOURCE_STORY_ID}*.story.md` (the source story)
3. `devforgeai-validate` CLI installed and on PATH

If any is absent, the appropriate HALT gate below fires with a specific remediation message. A fresh Claude Code session that only has the copy-pastable command string from `devforgeai/qa/reports/${SOURCE_STORY_ID}-next-steps.md` can reproduce the exact same output as a warm-start run.

---

## Zero-Ambiguity Ingestion Contract (qa-output-fidelity.md Rule 16 alignment)

For every REC entry fetched via `qa-recommendations-get`, the following fields **MUST** be populated with non-placeholder values:

**Required fields:** `id`, `severity`, `provenance`, `title`, `file`, `category`, `estimated_effort_minutes`, `verification.command`, `verification.expected`
**Required remediation (exactly one, never both):**
- either `before_code` + `after_code` (both non-null), OR
- `remediation_steps` (non-empty list)

**Prohibited values** (fail-fast triggers):
- Any required field exactly equal to `"TBD"`, `"TODO"`, `"various"`, `"N/A"`, or empty string `""` (unless schema explicitly allows null for that field).

**Fidelity HALT:** If any required field is missing OR carries a prohibited value:

```
HALT: "(fidelity) REC-${rec_id}: field '${field_path}' is ${actual_value}. Regenerate via /qa ${SOURCE_STORY_ID} deep."
```

No defaults, no aspirational filling, no graceful degradation. Bad data upstream is fixed in `/qa` regeneration, not papered over downstream.

---

## Prerequisite Context Markers (set by /create-story command)

| Marker | Required | Example | Notes |
|---|---|---|---|
| `$MODE` | yes | `FROM_RECOMMENDATIONS` | Dispatches Phase 01 to this reference |
| `$SOURCE_STORY_ID` | yes | `STORY-648` | Must match `^STORY-\d+$` |
| `$REC_IDS_FLAG` | no | `REC-STORY-648-M-001,REC-STORY-648-L-001` or `null` | If null → interactive selection |
| `$INCLUDE_BLOCKING` | yes | `false` (default) / `true` | When false, CRITICAL + HIGH recs are filtered out of candidates |

---

## Phase 00 Session ID Generation (FROM_RECOMMENDATIONS Mode — NO `story-preflight STORY-NNN`)

FROM_RECOMMENDATIONS mode does NOT call `devforgeai-validate story-preflight` with `$SOURCE_STORY_ID`. The `story-preflight` CLI accepts only `EPIC-NNN` (batch mode) or a 10+ word feature description (single-story mode) — passing `STORY-NNN` returns exit 2 with `"Invalid argument: 'STORY-NNN'. Expected EPIC-NNN ..."`. Do NOT use that CLI for session ID generation in this mode.

**Instead, generate the session ID deterministically from today's date:**

```
today = current date (YYYY-MM-DD)
existing_sessions = Glob(pattern="devforgeai/workflows/SC-${today}-*.checkpoint.json")

IF existing_sessions is empty:
    $SESSION_ID = "SC-${today}-001"
ELSE:
    # Find the highest NNN among today's sessions, ignoring completed ones if any.
    max_seq = max(parse_seq(basename(f)) for f in existing_sessions)   # e.g. 001
    $SESSION_ID = f"SC-${today}-{format(max_seq + 1, 03d)}"
```

Pattern: `SC-YYYY-MM-DD-NNN`. Do NOT rely on the skill's ambient fallback logic — emit the session ID here, explicitly.

Immediately after generating `$SESSION_ID`, initialize the workflow:

```
Bash("devforgeai-validate phase-init ${SESSION_ID} --workflow=stories --project-root=.")
```

This creates `devforgeai/workflows/${SESSION_ID}-stories-phase-state.json` and the checkpoint file. Other modes (SINGLE_STORY, EPIC_BATCH) get their session ID from `story-preflight.next_session_id`; FROM_RECOMMENDATIONS takes this direct path because its preflight needs differ (see Step R.5).

---

## Workflow

### Step R.1: Status Check + HALT Gates (a), (b)

EXECUTE:

```
status = Bash(
  command="devforgeai-validate qa-recommendations-status \
           --story-id=${SOURCE_STORY_ID} --project-root=. --format=json"
)

IF status exit != 0:
    HALT: "(cli error) qa-recommendations-status exit ${status.exit}: ${status.stderr}"

parsed = json.loads(status.stdout)

IF parsed.exists == false:
    HALT: "(a) No qa-recommendations.md for ${SOURCE_STORY_ID}.
          Run /qa ${SOURCE_STORY_ID} deep first to generate recommendations."

IF parsed.open_count == 0:
    HALT: "(b) All recommendations closed for ${SOURCE_STORY_ID}. Nothing to convert.
          If you intended to reopen, regenerate via /qa ${SOURCE_STORY_ID} deep."
```

VERIFY: `parsed.exists == true`, `parsed.open_count > 0`, and `parsed.open_rec_ids` is a non-empty list of REC-ID strings.

---

### Step R.2: Severity Filter (+ HALT (f))

EXECUTE:

```
candidates = parsed.open_rec_ids                                   # list[str]
by_severity = parsed.by_severity                                    # {CRITICAL: N, HIGH: N, MEDIUM: N, LOW: N}

IF $INCLUDE_BLOCKING == false:
    # Default policy: exclude Blocking (CRITICAL/HIGH). Those should be
    # fixed in-cycle via /dev --fix, not deferred to follow-up stories.
    candidates = [r for r in candidates if severity_of(r) in ("MEDIUM", "LOW")]

IF candidates is empty:
    IF $INCLUDE_BLOCKING == false AND (by_severity.CRITICAL + by_severity.HIGH) > 0:
        HALT: "(f) Only Blocking recs are open for ${SOURCE_STORY_ID}.
              Run /dev ${SOURCE_STORY_ID} --fix to close them in-cycle,
              OR re-invoke with --include-blocking to override (not recommended)."
    ELSE:
        HALT: "(f) No candidate recommendations after severity filter."
```

The helper `severity_of(rec_id)` parses the severity initial from the REC-ID pattern `REC-STORY-\d+-[CHML]-\d+` (C→CRITICAL, H→HIGH, M→MEDIUM, L→LOW).

---

### Step R.3: Selection (+ HALT (c), (d))

EXECUTE:

```
IF $REC_IDS_FLAG is not null:
    # Explicit subset supplied on command line (non-interactive).
    requested = split(REC_IDS_FLAG, ",")
    target_rec_ids = [r for r in requested if r in candidates]

    IF target_rec_ids is empty:
        HALT: "(d) --rec-ids produced empty intersection with candidates.
              Requested: ${requested}
              Candidates: ${candidates}
              Blocking recs are filtered unless --include-blocking is set."
ELSE:
    # Interactive multi-select. One option per candidate REC.
    AskUserQuestion(
        question: "Select recommendations to bundle (${SOURCE_STORY_ID}, cycle ${parsed.current_cycle}):",
        header: "Recommendations",
        multiSelect: true,
        options: [
          for each rec_id in candidates:
            {
              label: "${rec_id} [${severity_of(rec_id)}] — ${title from qa-recommendations-get}",
              description: "${file}:${lines} — est ${estimated_effort_minutes}min"
            }
        ]
    )

    target_rec_ids = user selections

    IF target_rec_ids is empty:
        HALT: "(c) No recommendations selected — cancelled."
```

Note: the interactive path may pre-fetch rec titles via `qa-recommendations-get` so the option labels are fully informative. A lightweight fetch (only `title`/`file`/`severity`) is acceptable; the full fidelity validation in Step R.4 is authoritative.

---

### Step R.4: Full Entry Fetch + Fidelity Validation (+ HALT (d), (e), (fidelity))

EXECUTE:

```
entries_json = Bash(
  command="devforgeai-validate qa-recommendations-get \
           --story-id=${SOURCE_STORY_ID} \
           --rec-ids=${join(target_rec_ids, ',')} \
           --project-root=. --format=json"
)

IF entries_json.exit == 1:
    parsed_err = json.loads(entries_json.stdout)
    HALT: "(d) REC-IDs not found: ${parsed_err.missing_rec_ids}.
          File: devforgeai/qa/recommendations/${SOURCE_STORY_ID}-qa-recommendations.md"

IF entries_json.exit == 2:
    HALT: "(e) Cannot parse qa-recommendations.md: ${entries_json.stderr}.
          Fix YAML or re-run /qa ${SOURCE_STORY_ID} deep."

entries = json.loads(entries_json.stdout).entries

# Zero-Ambiguity Ingestion Contract enforcement — one REC at a time.
PROHIBITED_VALUES = {"TBD", "TODO", "various", "N/A", ""}
REQUIRED_FIELDS = [
    "id", "severity", "provenance", "title", "file",
    "category", "estimated_effort_minutes",
    "verification.command", "verification.expected"
]

FOR each entry in entries:
    FOR each field_path in REQUIRED_FIELDS:
        value = resolve(entry, field_path)                          # nested dot lookup
        IF value is None OR value in PROHIBITED_VALUES:
            HALT: "(fidelity) REC-${entry.id}: field '${field_path}' is ${value}.
                  Regenerate via /qa ${SOURCE_STORY_ID} deep."

    # Remediation XOR — exactly one of the two remediation shapes.
    has_code_pair = (entry.before_code is not None) AND (entry.after_code is not None)
    has_steps     = (entry.remediation_steps is not None) AND (len(entry.remediation_steps) > 0)

    IF NOT (has_code_pair XOR has_steps):
        HALT: "(fidelity) REC-${entry.id}: must have either (before_code+after_code) OR remediation_steps.
              Regenerate via /qa ${SOURCE_STORY_ID} deep."
```

VERIFY: every `entries[i]` satisfies all fidelity constraints above. Any violation halts before any state change.

---

### Step R.5: Source Story Resolution

EXECUTE:

```
source_story_files = Glob(pattern="devforgeai/specs/Stories/${SOURCE_STORY_ID}*.story.md")

IF source_story_files is empty:
    HALT: "(g) Source story file missing for ${SOURCE_STORY_ID}.
          Expected under devforgeai/specs/Stories/."

source_story_file = source_story_files[0]

# Read epic assignment from the source story's YAML frontmatter.
epic_line = Grep(
  pattern="^epic:", path=source_story_file, output_mode="content"
)
source_epic = extract EPIC-NNN from epic_line
              (null if field is "null" / "None" / missing / placeholder)

# Allocate the next STORY-NNN id.
# CRITICAL: story-preflight accepts only EPIC-NNN or a 10+ word description.
# It does NOT accept STORY-NNN. Branch on source_epic accordingly.
IF source_epic matches ^EPIC-\d+$:
    # Source story is epic-assigned — delegate to story-preflight which scans
    # the epic's coverage table + all STORY-* files for the true next id.
    preflight = Bash(
      command="devforgeai-validate story-preflight \
               ${source_epic} --project-root=. --format=json"
    )
    NEW_STORY_ID = preflight.next_story_id
ELSE:
    # Source story is standalone (epic: null). Fall back to a direct scan of
    # the Stories directory + archive for the highest STORY-NNN id + 1.
    # Do NOT call story-preflight with SOURCE_STORY_ID — that will exit 2.
    all_stories = Glob(pattern="devforgeai/specs/Stories/STORY-*.story.md")
    archived    = Glob(pattern="devforgeai/specs/Stories/archive/STORY-*.story.md")
    max_seq = max(
      parse_story_number(basename(f))
      for f in (all_stories + archived)
    )
    NEW_STORY_ID = f"STORY-{format(max_seq + 1, 03d)}"
```

VERIFY: `NEW_STORY_ID` matches `^STORY-\d+$` and is strictly greater than `SOURCE_STORY_ID`'s numeric suffix. If `source_epic` is null, `NEW_STORY_ID` was derived from filesystem scan and no CLI call was made.

---

### Step R.6: Mapping (consult gap-to-story-mapping.md tables)

EXECUTE:

```
# Severity → Priority (mirrors gap-to-story-mapping.md)
severities = [e.severity for e in entries]
IF any(s in {"CRITICAL","HIGH"} for s in severities): priority = "High"
ELIF any(s == "MEDIUM" for s in severities):          priority = "Medium"
ELSE:                                                  priority = "Low"

# Effort → Points (Fibonacci mapping)
total_minutes = sum(e.estimated_effort_minutes for e in entries)
IF total_minutes <= 15:   points = 1
ELIF total_minutes <= 30: points = 2
ELIF total_minutes <= 60: points = 3
ELIF total_minutes <= 120: points = 5
ELIF total_minutes <= 240: points = 8
ELSE:                      points = 13

is_advisory = all(e.severity in {"MEDIUM", "LOW"} for e in entries)
slug_prefix = "advisory-" if is_advisory else ""

# Bundle title — describes scope, not individual recs.
distinct_files = set(e.file for e in entries)
IF len(distinct_files) == 1:
    scope = basename(distinct_files.first)
    bundle_title = "Hardening of ${scope} — ${len(entries)} recs from ${SOURCE_STORY_ID}"
ELSE:
    bundle_title = "Hardening bundle — ${len(entries)} recs from ${SOURCE_STORY_ID}"
```

VERIFY: `priority ∈ {High, Medium, Low}`; `points ∈ {1, 2, 3, 5, 8, 13}`; `is_advisory ∈ {true, false}`; `bundle_title` non-empty.

---

### Step R.7: Render feature_description (structured, authoritative)

EXECUTE:

Build a multi-REC structured block that Phase 02's requirements-analyst subagent consumes verbatim. **Every REC becomes ONE AC.** Verification commands and before/after code blocks are authoritative — they must be preserved exactly.

```
feature_description = """
Consolidated remediation of ${len(entries)} QA recommendations surfaced for ${SOURCE_STORY_ID}
(cycle ${parsed.current_cycle}). Each REC below becomes one AC. Verification commands and
before/after code blocks are AUTHORITATIVE and must be preserved verbatim.

"""

FOR each e in entries:
    feature_description += """
## ${e.id} — ${e.title} (${e.category}, ${e.severity}, ${e.file}:${e.lines or e.line}, ${e.estimated_effort_minutes}min)

description: ${e.description verbatim}

verification.command:  ${e.verification.command}
verification.expected: ${e.verification.expected}

"""
    IF e.before_code and e.after_code:
        feature_description += """
before_code:
```${guess_ext_from(e.file)}
${e.before_code}
```

after_code:
```${guess_ext_from(e.file)}
${e.after_code}
```
"""
    ELSE:
        feature_description += "remediation_steps:\n"
        FOR step in e.remediation_steps:
            feature_description += f"  - {step}\n"
```

VERIFY: `feature_description` contains one `## REC-` section per entry, all with non-empty verification command and expected.

---

### Step R.8: Emit Batch-Mode Context Markers

EXECUTE: emit ALL of the following markers. Phase 01 downstream steps and Phases 02–06 consume them.

```
**Batch Mode:** true
**Story ID:** ${NEW_STORY_ID}
**Epic ID:** ${source_epic or null}
**Sprint:** Backlog
**Priority:** ${priority}
**Points:** ${points}
**Type:** refactor
**Feature Name:** ${bundle_title}
**Feature Description:**
${feature_description}
**From Recommendations:** true
**Source Recommendations File:** devforgeai/qa/recommendations/${SOURCE_STORY_ID}-qa-recommendations.md
**Source Recommendation IDs:** ${join(target_rec_ids, ',')}
**Source Story:** ${SOURCE_STORY_ID}
**Cycle Recorded:** ${parsed.current_cycle}
**Is Advisory:** ${is_advisory}
**Story Filename Prefix:** ${slug_prefix}
```

VERIFY: all 15 markers emitted. `Feature Description` is multi-line (one section per REC).

---

## Downstream Phase Integration

| Phase | Behavior |
|---|---|
| 02 (Requirements Analysis) | Subagent prompt carries conditional instruction when `From Recommendations: true`. Each REC entry → one AC with verification.expected quoted verbatim in Then clause. |
| 05 (Story File Creation) | Frontmatter emits `from_recommendations: true`, `source_recommendations: [...]`, `cycle_recorded: N`, `advisory: ${is_advisory}`, `source_story: STORY-NNN`, `source_devarch: devforgeai/qa/recommendations/STORY-NNN-qa-recommendations.md`. Filename begins `STORY-NNN-${slug_prefix}<slug>.story.md`. |
| 06 (Epic/Sprint Linking) | New Step calls `devforgeai-validate qa-recommendations-link` to annotate the source recommendations file with `implemented_in: ${NEW_STORY_ID}`. |

---

## HALT Gate Summary

| Gate | Trigger | Message prefix |
|---|---|---|
| (a) | qa-recommendations-status.exists == false | `(a) No qa-recommendations.md for ${SOURCE_STORY_ID}` |
| (b) | qa-recommendations-status.open_count == 0 | `(b) All recommendations closed` |
| (c) | Interactive selection returned 0 | `(c) No recommendations selected — cancelled` |
| (d) | --rec-ids not in candidates, or get returned missing | `(d) REC-IDs not found` |
| (e) | qa-recommendations-get exit 2 (IO/parse) | `(e) Cannot parse qa-recommendations.md` |
| (f) | candidates empty after severity filter | `(f) Only Blocking recs are open` |
| (g) | Source story file missing | `(g) Source story file missing for ${SOURCE_STORY_ID}` |
| (fidelity) | Required field missing or prohibited value | `(fidelity) REC-${id}: field '${path}' is ${value}` |

All HALTs fire BEFORE any state change — no partial mutations, no orphan files.
