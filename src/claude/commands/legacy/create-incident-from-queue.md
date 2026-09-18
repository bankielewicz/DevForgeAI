---
name: create-incident-from-queue
description: Create GitHub incidents from the aggregated AI-analysis recommendations queue
argument-hint: "[--priority=high|medium|low] [--rec-ids=ID1,ID2] [--limit=N] [--feasible-only] [--help]"
model: opus
allowed-tools: Read, Glob, Grep, AskUserQuestion, Skill
---

# /create-incident-from-queue — Create GH Incidents from Aggregated Recommendations Queue

Parse the aggregated AI-analysis recommendations queue (`devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json`), select recs interactively, draft and post GitHub issues to bankielewicz/DevForgeAI via the `github-incident-from-feedback` skill, then link the posted issues back into the queue JSON in place.

**Component Orchestration:** Parse → Filter+Select → Draft+Approve+Post (skill) → Link (skill, in-place)

**Architectural constraint:** This command never calls `gh` directly. All GitHub-issue logic is owned by the `github-incident-from-feedback` skill. The slash command is a thin orchestrator.

**Quality bar — non-negotiable.** Every posted issue must be **full-fidelity, zero-ambiguity, and non-aspirational** (concrete files / functions / configs, before-and-after stated explicitly, AC as objectively verifiable checklist, test plan with exact commands, out-of-scope enumerated, prohibited language rejected). This bar is enforced by the skill's embedded `Github-incident-template.md` drafting prompt and its mandatory preview-and-approval gate — recs that fail the bar do not get posted. This command inherits the bar by delegating.

**Sibling pathways:** `/create-incident-from-rca RCA-NNN` (RCA source), `/create-incident-from-recommendations STORY-NNN` (QA-recs source), `/create-incident-from-feedback <ENTRY-ID>` (per-entry AI-analysis source). All four share the embedded `Github-incident-template.md` asset (byte-identical) but consume different upstream document formats.

**Authorizing context:** Replaces the retired `/recommendations-triage` command (which routed the same queue to story creation instead of GitHub issues). ADR-077 authorizes the skill; this command extends the 3-sibling pattern to a 4th source.

---

## Usage

```bash
/create-incident-from-queue
/create-incident-from-queue --priority=high
/create-incident-from-queue --priority=high --limit=10
/create-incident-from-queue --rec-ids=QUEUE-2026-0403-001,QUEUE-2026-0410-001
/create-incident-from-queue --feasible-only
/create-incident-from-queue --help
```

By default, ALL recommendations in the queue are eligible. Pass `--priority=high|medium|low` to filter by priority bucket, `--feasible-only` to include only `feasible_in_claude_code: true` recs, `--limit=N` to cap the candidate list, or `--rec-ids=` for exact selection.

---

## Argument Parsing

```
SOURCE_FILE = "devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json"   # FIXED — no override

IF "--help" in $ARGUMENTS OR first arg == "help":
    Display: "Usage: /create-incident-from-queue [--priority=high|medium|low] [--rec-ids=ID1,ID2] [--limit=N] [--feasible-only]"
    Display: "  Source (fixed): ${SOURCE_FILE}"
    Display: "  --priority=<bucket>     Filter by priority bucket (high|medium|low — matches the queue's bucketed schema)"
    Display: "  --rec-ids=<id,id,...>   Exact match on queue rec IDs (e.g., QUEUE-2026-0403-001)"
    Display: "  --limit=<N>             Cap candidate list to N recs after filtering"
    Display: "  --feasible-only         Include only recs with feasible_in_claude_code: true"
    HALT

IF NOT Glob(SOURCE_FILE):
    Display: "❌ Recommendations queue not found at ${SOURCE_FILE}"
    Display: "   The queue is populated by /dev Phase 09 framework-analyst output."
    Display: "   Run /dev on a story to generate recommendations, then retry."
    HALT

PRIORITY_FILTER = parse_value_after("--priority=")     # high|medium|low (lowercase, matches queue bucket names)
REC_IDS_RAW     = parse_value_after("--rec-ids=")      # comma-list of queue rec ids (e.g., "QUEUE-2026-0403-001,QUEUE-2026-0410-001")
LIMIT           = parse_value_after("--limit=")        # integer or empty
FEASIBLE_ONLY   = "--feasible-only" in $ARGUMENTS

REC_IDS_LIST = REC_IDS_RAW.split(",") with whitespace stripped (or empty)

IF PRIORITY_FILTER not empty AND PRIORITY_FILTER NOT IN {"high","medium","low"}:
    Display: "❌ Invalid --priority: ${PRIORITY_FILTER}"
    Display: "   Expected: high | medium | low (lowercase — matches queue bucket names)"
    HALT

IF LIMIT not empty AND NOT LIMIT.is_positive_integer():
    Display: "❌ Invalid --limit: ${LIMIT}"
    Display: "   Expected: positive integer"
    HALT

IF REC_IDS_LIST not empty:
    FOR rec_id in REC_IDS_LIST:
        IF NOT rec_id matches "^QUEUE-\\d{4}-\\d{4}-\\d{3}$":
            Display: "⚠ Warning — --rec-ids entry does not match expected queue ID shape: ${rec_id}"
            Display: "   Expected format: QUEUE-YYYY-MMDD-NNN"
            Display: "   Continuing — will fail at selection if no rec has this exact id."
```

---

## Phase 1-5: Queue Parsing + Schema Adaptation

The queue JSON shape:

```json
{
  "version": "1.0",
  "description": "Prioritized queue of AI-generated recommendations",
  "last_updated": "YYYY-MM-DD",
  "recommendations": {
    "high":   [ {id, title, source_story, source_date, description, affected_files[], implementation_code, effort_estimate, feasible_in_claude_code}, ... ],
    "medium": [ ... ],
    "low":    [ ... ]
  }
}
```

```
Read(SOURCE_FILE) → parse as JSON → bind as `queue_doc`

IF "recommendations" not in queue_doc:
    Display: "❌ Queue file lacks 'recommendations' key: ${SOURCE_FILE}"
    HALT

bucketed_recs = queue_doc["recommendations"]
IF NOT (isinstance(bucketed_recs, dict) AND any(k in bucketed_recs for k in ["high","medium","low"])):
    Display: "❌ Queue 'recommendations' must be an object with high/medium/low keys."
    HALT

# Flatten + tag with priority + adapt schema to match what the skill expects
# (skill consumes 'implementation_notes'; queue uses 'implementation_code' — map it)
selected_recommendations_pool = []
FOR priority in ["high", "medium", "low"]:
    FOR rec in bucketed_recs.get(priority, []):
        selected_recommendations_pool.append({
            # Schema fields the skill consumes (matched to per-entry ai-analysis shape)
            "id":                     rec.get("id"),                          # native queue id (e.g., QUEUE-2026-0403-001) — no synthesis
            "description":            rec.get("description", "").strip(),
            "affected_files":         rec.get("affected_files", []),
            "implementation_notes":   rec.get("implementation_code", "").strip(),   # map: queue uses implementation_code, skill expects implementation_notes
            "priority":               priority,
            "feasible_in_claude_code": rec.get("feasible_in_claude_code"),

            # Queue-specific fields the skill MAY surface in the issue body via the embedded template
            "title":                  rec.get("title", "").strip(),           # queue has a title; per-entry recs synthesize one
            "source_story":           rec.get("source_story"),                # provenance (which story produced this rec)
            "source_date":            rec.get("source_date"),                 # provenance (when produced)
            "source_srfd":            rec.get("source_srfd"),                 # optional SRFD reference if STORY-571/572 enrichment applied
            "effort_estimate":        rec.get("effort_estimate"),

            # Idempotency hint — if the queue rec already has a posted_as marker, surface for skill
            "_already_posted":        rec.get("posted_as"),
        })

IF selected_recommendations_pool empty:
    Display: "ℹ No recommendations found in queue (all 3 priority buckets are empty)."
    Display: "   Run /dev on a story to populate the queue."
    HALT

Display: "Loaded ${len(selected_recommendations_pool)} recommendations from queue (high:${len(bucketed_recs.get('high',[]))} / medium:${len(bucketed_recs.get('medium',[]))} / low:${len(bucketed_recs.get('low',[]))})"
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

# Step 6.3: --limit cap (applied AFTER priority + feasible filters, BEFORE --rec-ids selection)
IF LIMIT not empty:
    candidate = candidate[:int(LIMIT)]

IF candidate empty:
    Display: "ℹ No recommendations match the filters."
    HALT

# Step 6.4: --rec-ids filter (exact match — skips prompt)
IF REC_IDS_LIST not empty:
    selected_recommendations = [r for r in candidate if r["id"] in REC_IDS_LIST]

    missing = [id for id in REC_IDS_LIST if id NOT IN [r["id"] for r in selected_recommendations]]
    IF missing not empty:
        Display: "❌ Requested rec IDs not found (or filtered out) in queue: ${missing}"
        HALT
ELSE:
    # Step 6.5: Interactive multi-select
    # Display grouped by priority (HIGH first), with a "bulk" option
    AskUserQuestion(
        question: "Which recommendations to convert into GitHub issues?",
        header: "Select",
        multiSelect: true,
        options: [
            "All ${len(candidate)} recommendations (Recommended)",
            # Per-rec rows showing priority, id, title (queue has titles; preferred over description-truncated), feasibility, effort estimate
            "[${rec.priority.upper()}] ${rec.id} — ${rec.title or rec.description[:60]}… (feasible:${rec.feasible_in_claude_code}, effort:${rec.effort_estimate})",
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

Delegated entirely to the `github-incident-from-feedback` skill. The slash command does NOT format issue bodies, does NOT invoke the `gh` CLI, does NOT manage approval prompts. The skill owns all of that and its embedded `Github-incident-template.md` enforces the quality bar.

```
Skill(command="github-incident-from-feedback", args="--batch")
```

**Inputs the skill consumes** (via shared context):
- `SOURCE_FILE` = `devforgeai/feedback/ai-analysis/aggregated/recommendations-queue.json` (fixed for this command)
- `selected_recommendations` — from Phase 6-9 (schema-adapted to match the skill's expected shape; `implementation_code` already remapped to `implementation_notes`; queue-only fields like `title`, `source_story`, `source_date`, `effort_estimate` available for the template to surface)
- `repo` — hardcoded `bankielewicz/DevForgeAI` constant in the skill (BR-007)

**Outputs the skill returns** (consumed by Phase 11):

```
results = [
  { rec_id: "QUEUE-2026-0403-001", issue_number: 96, issue_url: "https://github.com/bankielewicz/DevForgeAI/issues/96", status: "success", error_message: null },
  { rec_id: "QUEUE-2026-0410-001", issue_number: null, issue_url: null, status: "failed", error_message: "label X missing" }
]
```

The skill internally runs 6 phases:
1. Setup (validate inputs, gh auth check, idempotency detection via `posted_as` markers in `SOURCE_FILE`)
2. Drafting (apply embedded template; queue recs include both `title` and `description`, so title maps directly to `# <Imperative title>`; `affected_files[]` → `## Files to change`; `implementation_notes` → `## Required behavior`; `source_story`+`source_date` surface in `## Context`)
3. Summary preview (compact table with priority column; show bucket-grouped layout matching queue)
4. Drill-down approval loop (user picks: post-all / inspect / subset / cancel)
5. Post (the gh CLI invocation hardcodes `--repo bankielewicz/DevForgeAI`; on success, writes `posted_as` block into the matching queue rec in place — link-back lives inside the skill, BR-010)
6. Result (return to caller)

The slash command treats this as a single black-box delegation.

---

## Phase 11: Final Summary

The skill owns in-place queue link-back, so this slash command does NOT re-edit `SOURCE_FILE`. Phase 11 is a simple final summary for the user:

```
success = [r for r in results if r.status == "success"]
failed  = [r for r in results if r.status == "failed"]
skipped = [r for r in results if r.status == "skipped"]

Display:
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"  /create-incident-from-queue — Summary"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"✅ Posted:   ${len(success)}"
FOR r in success:
    Display: "   • ${r.rec_id} → Issue-${r.issue_number} — ${r.issue_url}"
"❌ Failed:   ${len(failed)}"
FOR r in failed:
    Display: "   • ${r.rec_id}: ${r.error_message}"
"⏭ Skipped:  ${len(skipped)}"
FOR r in skipped:
    Display: "   • ${r.rec_id}: ${r.error_message} (likely already posted — see queue JSON)"
"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
"Queue link-back applied to: ${SOURCE_FILE} (in-place posted_as blocks per successful rec)"
```

---

## Error Handling

Validation errors, gh auth failures, label-missing errors, network failures, and per-issue failures are all handled with **failure isolation** — a failure on rec N does NOT block rec N+1. The `github-incident-from-feedback` skill's Phase 5 handles posting errors and Phase 6 reports them.

| Error | Resolution |
|-------|-----------|
| Queue file not found | Run `/dev` to populate the queue |
| Queue has no recommendations | No work to do — exit gracefully |
| Invalid `--priority` value | HALT with usage message |
| Invalid `--limit` value | HALT with usage message |
| `--rec-ids` references non-existent rec | HALT and list missing ids |
| `gh auth` not configured | Skill's setup phase HALTs |
| Issue post fails for one rec | Continue with the next (failure isolation) |

---

## Success Criteria

- [ ] Queue JSON parsed; bucketed recs flattened with priority tags
- [ ] Schema adapted (`implementation_code` → `implementation_notes`) for skill compatibility
- [ ] Filters applied (`--priority`, `--feasible-only`, `--limit`, default all-eligible)
- [ ] Recommendations selected (`--rec-ids` honored OR multi-select prompt)
- [ ] Issues drafted with full template fidelity (skill BR-015) and quality bar enforced (full-fidelity / zero-ambiguity / non-aspirational)
- [ ] User approval explicitly captured before any post (skill Phase 4)
- [ ] Issues posted via skill with `--repo bankielewicz/DevForgeAI` hardcoded (BR-007)
- [ ] Queue JSON updated in place with `posted_as` per successful post (skill BR-010)
- [ ] Failure isolation: per-issue failures don't block batch (BR-004)
- [ ] Idempotency: re-runs detect `posted_as` markers and skip (skill BR-009)

---

## Integration

**Invoked by:** User via `/create-incident-from-queue [--filters]`. Auto-suggested in `/dev` Phase 10 result when the queue has HIGH-priority items (see `dev-result-interpreter.md`).

**Invokes:** `github-incident-from-feedback` skill (Phase 10).

**Updates:** Aggregated queue JSON (in-place via skill Phase 5.3), GitHub issues (via skill).

**Reference:** Skill SKILL.md — `.claude/skills/github-incident-from-feedback/SKILL.md`. Quality bar — `.claude/skills/github-incident-from-feedback/assets/templates/Github-incident-template.md`.

---

## Migration Note

This command **replaces the retired `/recommendations-triage` command**, which previously routed the same queue to story creation (via `spec-driven-feedback` triage mode → `/create-story`). Per user direction, AI-analysis recommendations now route to **GitHub issues**, not stories. The `triage` type and its `triage-workflow.md` reference were removed from `spec-driven-feedback` in the same change.

```bash
# Old (removed)
/recommendations-triage --priority=high --limit=5
# → routed selected recs to /create-story (in-repo story files)

# New
/create-incident-from-queue --priority=high --limit=5
# → routes selected recs to GitHub issues (full-fidelity, zero-ambiguity, non-aspirational)
```

The selection UI is preserved; only the destination changed.

---

**Version:** 1.0 — Lean Orchestration | **Pattern:** Command delegates issue creation to skill (4th sibling: alongside `/create-incident-from-rca`, `/create-incident-from-recommendations`, `/create-incident-from-feedback`)
