---
name: create-incident-from-feedback
description: Create GitHub incidents from AI-analysis feedback recommendations
argument-hint: "<ENTRY-ID|--source=PATH> [--priority=high|medium|low] [--rec-ids=ID1,ID2] [--feasible-only] [--help]"
model: opus
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill
---

# /create-incident-from-feedback — Create GH Incidents from AI-Analysis Feedback

Parse an AI-analysis feedback file (`devforgeai/feedback/ai-analysis/${ENTRY_ID}/...ai-analysis.json` or an arbitrary path via `--source=`), select `ai_analysis.recommendations[]` interactively, draft and post GitHub issues to bankielewicz/DevForgeAI via the `github-incident-from-feedback` skill, then link the posted issues back into the source JSON in place.

**Component Orchestration:** Parse → Filter+Select → Draft+Approve+Post (skill) → Link (skill, in-place)

**Architectural constraint:** This command never calls `gh` directly. All GitHub-issue logic is owned by the `github-incident-from-feedback` skill. The slash command is a thin orchestrator.

**Sibling pathways:** `/create-incident-from-rca RCA-NNN` (RCA source) and `/create-incident-from-recommendations STORY-NNN` (QA-recs source). All three share the embedded `Github-incident-template.md` asset (byte-identical) but consume different upstream document formats.

**Authorizing ADR:** ADR-077.

---

## Usage

```bash
/create-incident-from-feedback EPIC-081
/create-incident-from-feedback STORY-661
/create-incident-from-feedback --source=devforgeai/feedback/ai-analysis/EPIC-081/2026-02-22-epic-creation-ai-analysis.json
/create-incident-from-feedback EPIC-081 --priority=medium
/create-incident-from-feedback EPIC-081 --rec-ids=REC-FB-EPIC-081-M-001,REC-FB-EPIC-081-L-002
/create-incident-from-feedback EPIC-081 --feasible-only
/create-incident-from-feedback --help
```

By default, ALL recommendations in the matched ai-analysis JSON are eligible. Pass `--priority=high|medium|low` to filter by priority, `--feasible-only` to include only `feasible_in_claude_code: true` recs, or `--rec-ids=` for exact selection.

---

## Argument Parsing

```
ARG = first non-flag argument from $ARGUMENTS (or null)

IF "--help" in $ARGUMENTS OR ARG == "help":
    Display: "Usage: /create-incident-from-feedback <ENTRY-ID|--source=PATH> [--priority=...] [--rec-ids=...] [--feasible-only]"
    Display: "  ENTRY-ID is the directory name under devforgeai/feedback/ai-analysis/"
    Display: "    (e.g., STORY-661, EPIC-081, RCA-002, IMPL-FEEDBACK-INDEXER)"
    Display: "  --source=<path> overrides ENTRY-ID resolution; pass the full JSON path directly"
    HALT

SOURCE_FLAG = parse_value_after("--source=")  # e.g., "devforgeai/feedback/ai-analysis/EPIC-081/.../...json"

IF SOURCE_FLAG not empty:
    SOURCE_FILE = SOURCE_FLAG
    # Derive ENTRY_ID from path
    ENTRY_ID = path.basename(path.dirname(SOURCE_FILE))   # e.g., "EPIC-081"
    IF NOT Glob(SOURCE_FILE):
        Display: "❌ Source file not found: ${SOURCE_FILE}"
        HALT
ELSE:
    ENTRY_ID = ARG (or empty)

    IF ENTRY_ID empty:
        Display: "❌ ENTRY ID required (or pass --source=<path>)"
        Display: "Usage: /create-incident-from-feedback <ENTRY-ID|--source=PATH>"
        Display: "Available AI-analysis entries:"
        FOR d in Glob("devforgeai/feedback/ai-analysis/*/"):
            Display: "  • ${path.basename(d)}"
        HALT

    # Resolve to the JSON file under that entry dir — prefer *ai-analysis*.json, else any *.json with "ai_analysis" key
    CANDIDATES = Glob("devforgeai/feedback/ai-analysis/${ENTRY_ID}/*ai-analysis*.json")
    IF CANDIDATES empty:
        # Fall back: any .json file in the entry dir
        CANDIDATES = Glob("devforgeai/feedback/ai-analysis/${ENTRY_ID}/*.json")
        # Filter to ones that contain "ai_analysis" key (use Grep --files-with-matches)
        CANDIDATES = [c for c in CANDIDATES if Grep(pattern='"ai_analysis"', path=c, output_mode="files_with_matches")]

    IF CANDIDATES empty:
        Display: "❌ No ai-analysis JSON found under devforgeai/feedback/ai-analysis/${ENTRY_ID}/"
        HALT
    ELIF len(CANDIDATES) > 1:
        AskUserQuestion: "Multiple ai-analysis files found for ${ENTRY_ID}. Which one?" | options=CANDIDATES
        SOURCE_FILE = (user choice)
    ELSE:
        SOURCE_FILE = CANDIDATES[0]

# Optional flags
PRIORITY_FILTER = parse_value_after("--priority=")     # high|medium|low (lowercase per ai_analysis schema)
REC_IDS_RAW     = parse_value_after("--rec-ids=")      # comma-list of synthesized REC-FB-... ids
FEASIBLE_ONLY   = "--feasible-only" in $ARGUMENTS

REC_IDS_LIST = REC_IDS_RAW.split(",") with whitespace stripped (or empty)

IF PRIORITY_FILTER not empty AND PRIORITY_FILTER NOT IN {"high","medium","low"}:
    Display: "❌ Invalid --priority: ${PRIORITY_FILTER}"
    Display: "   Expected: high | medium | low (lowercase — matches ai_analysis schema)"
    HALT

IF REC_IDS_LIST not empty:
    FOR rec_id in REC_IDS_LIST:
        IF NOT rec_id matches "^REC-FB-[A-Z0-9-]+-[HML]-\\d{3}$":
            Display: "❌ Invalid --rec-ids entry: ${rec_id}"
            Display: "   Expected format: REC-FB-<ENTRY-ID>-{H|M|L}-NNN"
            HALT
```

---

## Phase 1-5: AI-Analysis JSON Parsing + ID Synthesis

The ai-analysis JSON is a single object with an `ai_analysis.recommendations[]` array. Parsing is direct JSON read — no YAML, no markdown sectioning.

```
Read(SOURCE_FILE) → parse as JSON → bind as `source_doc`

IF "ai_analysis" not in source_doc OR "recommendations" not in source_doc["ai_analysis"]:
    Display: "❌ Source file lacks ai_analysis.recommendations: ${SOURCE_FILE}"
    HALT

raw_recs = source_doc["ai_analysis"]["recommendations"]
source_operation = source_doc["ai_analysis"].get("operation")  # e.g., "epic-creation"

# Synthesize stable IDs (raw recs have none)
selected_recommendations_pool = []
priority_counters = {"high": 0, "medium": 0, "low": 0}
FOR (idx, rec) in enumerate(raw_recs):
    priority = rec.get("priority", "medium").lower()
    IF priority not in priority_counters:
        priority = "medium"   # default for malformed
    priority_counters[priority] += 1
    p_letter = {"high":"H", "medium":"M", "low":"L"}[priority]
    rec_id = f"REC-FB-{ENTRY_ID}-{p_letter}-{priority_counters[priority]:03d}"

    selected_recommendations_pool.append({
        "id": rec_id,
        "description":            rec.get("description", "").strip(),
        "affected_files":         rec.get("affected_files", []),
        "implementation_notes":   rec.get("implementation_notes", "").strip(),
        "priority":               priority,
        "feasible_in_claude_code": rec.get("feasible_in_claude_code"),
        "source_operation":       source_operation,
        "source_timestamp":       source_doc["ai_analysis"].get("timestamp"),
        # Idempotency: if the source already has posted_as on this rec, surface it for the skill
        "_already_posted":        rec.get("posted_as"),
    })

IF selected_recommendations_pool empty:
    Display: "ℹ No recommendations found in ${SOURCE_FILE} (empty ai_analysis.recommendations array)."
    HALT
```

---

## Phase 6-9: Filter + Interactive Selection

```
candidate = selected_recommendations_pool

# Step 6.1: --priority filter
IF PRIORITY_FILTER not empty:
    candidate = [r for r in candidate if r["priority"] == PRIORITY_FILTER]

# Step 6.2: --feasible-only filter
IF FEASIBLE_ONLY:
    candidate = [r for r in candidate if r["feasible_in_claude_code"] is True]

# Step 6.3: --rec-ids filter (exact match — skips prompt)
IF REC_IDS_LIST not empty:
    selected_recommendations = [r for r in candidate if r["id"] in REC_IDS_LIST]

    missing = [id for id in REC_IDS_LIST if id NOT IN [r["id"] for r in selected_recommendations]]
    IF missing not empty:
        Display: "❌ Requested rec IDs not found (or filtered out) in ${SOURCE_FILE}: ${missing}"
        HALT
ELSE:
    # Step 6.4: Interactive multi-select
    AskUserQuestion(
        question: "Which recommendations to convert into GitHub issues for ${ENTRY_ID}?",
        header: "Select",
        multiSelect: true,
        options: [
            "All ${len(candidate)} recommendations (Recommended)",
            # Per-rec rows showing priority, ID, description-truncated, feasibility, affected_files count
            "[${priority}] ${rec.id} — ${rec.description[:50]}… (feasible:${rec.feasible_in_claude_code}, files:${len(rec.affected_files)})",
            ...
            "None — cancel"
        ]
    )

    selected_recommendations = (mapped from user choices)

IF selected_recommendations empty OR user chose "None — cancel":
    Display: "No recommendations selected; cancelling."
    HALT gracefully

# Strip the internal _already_posted hint before delegation (skill re-checks via grep)
FOR r in selected_recommendations:
    r.pop("_already_posted", None)
```

---

## Phase 10: Drafting + Approval + Posting (DELEGATE TO SKILL)

Delegated entirely to the `github-incident-from-feedback` skill (see ADR-077). The slash command does NOT format issue bodies, does NOT invoke the gh CLI, does NOT manage approval prompts. The skill owns all of that.

```
Skill(command="github-incident-from-feedback", args="--batch")
```

**Inputs the skill consumes** (via shared context):
- `${ENTRY_ID}`, `${SOURCE_FILE}` — from argument parsing
- `selected_recommendations` — from Phase 6-9 (synthesized-id schema per entry)
- `repo` — hardcoded `bankielewicz/DevForgeAI` constant in the skill (BR-007)

**Outputs the skill returns** (consumed by Phase 11 below):

```
results = [
  { rec_id: "REC-FB-EPIC-081-M-001", issue_number: 42, issue_url: "https://github.com/bankielewicz/DevForgeAI/issues/42", status: "success", error_message: null },
  { rec_id: "REC-FB-EPIC-081-M-002", issue_number: null, issue_url: null, status: "failed", error_message: "label X missing" }
]
```

The skill internally runs 6 phases:
1. Setup (validate inputs, gh auth check, idempotency detection via `posted_as` markers in `${SOURCE_FILE}`)
2. Drafting (apply embedded template; AI-analysis recs are leaner than QA recs — title synthesized from description; ACs/Test plan synthesized; `affected_files[]` maps to `## Files to change`; `implementation_notes` maps to `## Required behavior`)
3. Summary preview (compact table with priority column)
4. Drill-down approval loop (user picks: post-all / inspect / subset / cancel)
5. Post (the gh CLI invocation hardcodes `--repo bankielewicz/DevForgeAI`; on success, writes `posted_as` block into `${SOURCE_FILE}` in place — link-back lives inside the skill, BR-010)
6. Result (return to caller)

The slash command treats this as a single black-box delegation.

---

## Phase 11: Final Summary

The skill owns in-place source-JSON link-back (BR-010), so this slash command does NOT re-edit `${SOURCE_FILE}`. Phase 11 is a simple final summary for the user:

```
success = [r for r in results if r.status == "success"]
failed  = [r for r in results if r.status == "failed"]
skipped = [r for r in results if r.status == "skipped"]

Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  /create-incident-from-feedback ${ENTRY_ID} — Summary"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"✅ Posted:   ${len(success)}"
FOR r in success:
    Display: "   • ${r.rec_id} → Issue-${r.issue_number} — ${r.issue_url}"
"❌ Failed:   ${len(failed)}"
FOR r in failed:
    Display: "   • ${r.rec_id}: ${r.error_message}"
"⏭ Skipped:  ${len(skipped)}"
FOR r in skipped:
    Display: "   • ${r.rec_id}: ${r.error_message}"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"Source link-back applied to: ${SOURCE_FILE} (in-place posted_as blocks)"
```

---

## Error Handling

Validation errors, gh auth failures, label-missing errors, network failures, and per-issue failures are all handled with **failure isolation** — a failure on issue N does NOT block issue N+1. The `github-incident-from-feedback` skill's Phase 5 handles posting errors and Phase 6 reports them.

---

## Success Criteria

- [ ] AI-analysis JSON parsed; `ai_analysis.recommendations[]` extracted
- [ ] Stable rec IDs synthesized (`REC-FB-${ENTRY_ID}-{H|M|L}-NNN`)
- [ ] Filters applied (`--priority`, `--feasible-only`, default all-eligible)
- [ ] Recommendations selected (`--rec-ids` honored OR multi-select prompt)
- [ ] Issues drafted with full template fidelity, including `## Labels` section (skill BR-015)
- [ ] User approval explicitly captured before any post (skill Phase 4)
- [ ] Issues posted via skill with `--repo bankielewicz/DevForgeAI` hardcoded (BR-007)
- [ ] Source JSON updated in place with `posted_as` per successful post (skill BR-010)
- [ ] Failure isolation: per-issue failures don't block batch (BR-004)
- [ ] Idempotency: re-runs detect `posted_as` markers and route skipped recs to `skipped.json` (skill BR-009)

---

## Integration

**Invoked by:** User via `/create-incident-from-feedback <ENTRY-ID|--source=PATH>`
**Invokes:** `github-incident-from-feedback` skill (Phase 10).
**Updates:** Source ai-analysis JSON (in-place via skill Phase 5.3), GitHub issues (via skill).

**Reference:** Skill SKILL.md — `.claude/skills/github-incident-from-feedback/SKILL.md`. ADR — `devforgeai/specs/adrs/ADR-077-github-incident-from-feedback-skill.md`.

---

**Version:** 1.0 — Lean Orchestration | **Pattern:** Command delegates issue creation to skill (siblings: `/create-incident-from-rca`, `/create-incident-from-recommendations`)
