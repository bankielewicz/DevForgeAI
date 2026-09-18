# Interactive Selection Workflow (Phases 6-9)

Detailed pseudocode for filter logic and interactive recommendation selection.

After Phase 1-5 (parsing) returns a `qa_recs_document.recommendations` array, the slash command applies CLI filters (`--severity`, `--include-blocking`) and either honors `--rec-ids` directly OR shows the user a multi-select prompt. The output (`selected_recommendations`) is the input to Phase 10 (the `github-incident-from-recommendations` skill).

---

## Phase 6.1: Apply Section Visibility Defaults

By default, only `## Advisory Recommendations` are eligible. `## Blocking Recommendations` require `--include-blocking`. `## Deferred Recommendations` are NEVER auto-included — they require explicit `--rec-ids=` selection.

```
candidate = []
FOR rec in qa_recs_document.recommendations:
    IF rec.section == "Deferred":
        # Deferred requires explicit opt-in via --rec-ids
        IF rec.id IN REC_IDS_LIST:
            candidate.append(rec)
        # Otherwise skip silently — the rec was deferred for a documented reason
        continue

    IF rec.section == "Blocking":
        IF INCLUDE_BLOCKING OR rec.id IN REC_IDS_LIST:
            candidate.append(rec)
        # Otherwise skip — Blocking recs are usually addressed via /dev or as a release blocker, not via post-and-defer
        continue

    # Advisory section — default eligible
    candidate.append(rec)
```

---

## Phase 6.2: Apply --severity Filter

```
IF SEVERITY_FILTER not empty:
    before = len(candidate)
    candidate = [r for r in candidate if r.severity == SEVERITY_FILTER]
    after = len(candidate)
    Display: "Filtered by --severity=${SEVERITY_FILTER}: ${before} → ${after}"
```

Example: `--severity=MEDIUM` keeps only MEDIUM recs from the candidate set.

---

## Phase 6.3: Apply --rec-ids Filter (if provided — bypasses prompt)

```
IF REC_IDS_LIST not empty:
    selected_recommendations = [r for r in candidate if r.id IN REC_IDS_LIST]

    # Validate every requested ID was found
    found_ids = {r.id for r in selected_recommendations}
    missing = [rid for rid in REC_IDS_LIST if rid NOT IN found_ids]
    IF missing:
        Display: "❌ Requested rec IDs not found in ${QA_RECS_FILE}:"
        FOR rid in missing:
            Display: "   • ${rid}"
        HALT

    Display: "Selected ${len(selected_recommendations)} recommendation(s) via --rec-ids"

    # Skip Phase 7-8 — user already specified IDs explicitly
    GOTO Phase 9

# Otherwise fall through to interactive selection
```

---

## Phase 7: Display Recommendation Summary Table

```
IF len(candidate) == 0:
    Display: "No recommendations match current filters."
    Display: ""
    Display: "Tip: re-run without --severity to see all candidates,"
    Display: "or pass --include-blocking to include the Blocking section."
    HALT

Display: ""
Display: "┌─────────────────────────┬──────────┬──────────┬──────────────────────────────┬─────────────────────┬────────┐"
Display: "│ REC ID                  │ Severity │ Section  │ Title                        │ File:Line           │ Effort │"
Display: "├─────────────────────────┼──────────┼──────────┼──────────────────────────────┼─────────────────────┼────────┤"

FOR rec in candidate:
    title_disp   = rec.title[:28].ljust(28)
    file_disp    = (rec.file or "—")[:14] + ":" + str(rec.line or rec.line_range or "—")
    file_disp    = file_disp[:19].ljust(19)
    effort_disp  = f"{rec.estimated_effort_minutes}m".rjust(6)
    linked_marker = " 🔗" if rec.posted_as_marker else "  "
    Display: f"│ ${rec.id.ljust(23)} │ ${rec.severity.ljust(8)} │ ${rec.section.ljust(8)} │ ${title_disp}${linked_marker} │ ${file_disp} │ ${effort_disp} │"

Display: "└─────────────────────────┴──────────┴──────────┴──────────────────────────────┴─────────────────────┴────────┘"
Display: ""
IF any(r.posted_as_marker for r in candidate):
    Display: "🔗 = already linked to an issue (skill Phase 1.5 will handle idempotency)"
    Display: ""
```

---

## Phase 8: Interactive Multi-Select

```
options = []

# "All" option first
options.append({
    label: f"All ${len(candidate)} eligible recommendations (Recommended)",
    description: f"Convert all {len(candidate)} candidates into GitHub issues"
})

# Per-rec options
FOR rec in candidate:
    file_loc = f"{rec.file}:{rec.line or rec.line_range[0] if rec.line_range else '—'}"
    options.append({
        label: f"[{rec.severity}] {rec.id} — {rec.title[:40]}",
        description: f"{rec.section} | {file_loc} | {rec.estimated_effort_minutes}m effort"
    })

# "None" option last
options.append({
    label: "None — cancel",
    description: "Exit without creating any issues"
})

AskUserQuestion(
    questions=[{
        question: f"Which recommendations to convert into GitHub issues for {STORY_ID}?",
        header: "Select",
        multiSelect: True,
        options: options
    }]
)
```

---

## Phase 8.1: Handle Selection

```
selected_recommendations = []

IF user picked "None — cancel":
    Display: "No recommendations selected. Exiting."
    HALT (gracefully)

IF user picked "All ${N} eligible recommendations":
    selected_recommendations = candidate
ELSE:
    FOR selection in user_selections:
        IF selection matches "[SEVERITY] REC-STORY-...":
            rec_id = extract REC ID from label
            rec = find_recommendation_by_id(candidate, rec_id)
            IF rec:
                selected_recommendations.append(rec)

    # "Other" custom input — comma-separated REC IDs
    IF user provided custom text:
        custom_ids = parse comma-separated IDs from custom input
        FOR rid in custom_ids:
            IF NOT regex_match(r"^REC-STORY-\d+-[CHML]-\d{3}$", rid):
                Display: f"⚠ Skipping invalid format: {rid}"
                continue
            rec = find_recommendation_by_id(candidate, rid)
            IF rec:
                selected_recommendations.append(rec)
            ELSE:
                Display: f"⚠ Not in candidate set: {rid}"

# Deduplicate (user might pick "All" + individual recs)
selected_recommendations = unique_by_id(selected_recommendations)

IF len(selected_recommendations) == 0:
    Display: "No valid recommendations selected. Re-prompting..."
    GOTO Phase 8

Display: f"Selected {len(selected_recommendations)} recommendation(s) for issue creation"
```

---

## Phase 9: Pass to Issue Creation Skill

```
batch_input = {
    qa_recs_document: {
        story_id: qa_recs_document.story_id,
        qa_cycle: qa_recs_document.qa_cycle,
        qa_recs_file: QA_RECS_FILE
    },
    selected_recommendations: selected_recommendations,
    selection_count: len(selected_recommendations),
    repo: "bankielewicz/DevForgeAI"   # from skill BR-007
}

# Each rec preserves the FULL QA-recs schema. The skill's Phase 2 (Drafting) maps fields to template
# sections per parsing-workflow.md Phase 4: id → draft filename + idempotency key; severity/provenance/
# category → namespaced labels; title → issue title (validated ≤80 chars, imperative); file + line/line_range
# → ## Files to change; before_code/after_code → ## Current behavior / ## Required behavior; remediation_steps
# (if present) → ## Acceptance criteria checklist items; verification.command + expected → ## Test plan;
# estimated_effort_minutes → effort:* bucket label; classification → classification:regression|classification:pre-existing
# label (BR-010); blocking_release → release:blocking label if true (BR-010); posted_as_marker → skill Phase 1.5
# idempotency input.

Display: ""
Display: f"Proceeding to GitHub issue drafting via github-incident-from-recommendations skill ({selection_count} recommendation(s))..."
Display: ""

# Invoke skill (Phase 10)
Skill(command="github-incident-from-recommendations", args="--batch")
```

---

## Edge Cases

| Edge case | Behavior |
|-----------|----------|
| All recs filtered out | HALT with hint to relax filters |
| `--rec-ids` references a rec not in file | HALT with the missing IDs listed |
| `--rec-ids` references a deferred rec | Allowed (explicit opt-in overrides default) |
| `--rec-ids` references a blocking rec | Allowed (explicit opt-in overrides --include-blocking default) |
| `--severity` with `--rec-ids` | `--rec-ids` wins; severity filter does not further restrict the explicit list |
| Single recommendation in candidate | Still display selection prompt (allows cancel) |
| User selects "Other" with custom IDs | Parse, validate format, ignore invalid entries with warning |
| User picks "All" + individual recs | Deduplicate by id; treat as "All" |
| Already-linked rec selected | Allowed; skill Phase 1.5 handles idempotency (skip / repost / cancel prompt) |

---

## Differences from /create-incident-from-rca's selection

- Filter flags: `--threshold HOURS` (RCA, effort) vs `--severity`, `--include-blocking`, `--rec-ids` (here)
- Sort key: Priority (RCA) vs document order preserved (here — sorted by `/qa` upstream)
- Section visibility: all recs eligible (RCA) vs Advisory-default, Blocking opt-in, Deferred explicit-only (here)
- Table columns: 4-col (RCA) vs 6-col with Severity + Section + File:Line (here)
- Custom input format: `REC-1, REC-2` (RCA) vs `REC-STORY-NNN-{C|H|M|L}-NNN` (here)
- Linked indicator: 🔗 marker on already-posted recs (here only)
