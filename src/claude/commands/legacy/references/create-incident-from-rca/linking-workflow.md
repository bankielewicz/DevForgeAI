# Phase 11: RCA-Issue Linking Workflow

**Purpose:** Update RCA document with GitHub issue references for traceability after Phase 10 (issue creation skill) completes.

This is a simple file-edit phase — no GitHub API calls, no `gh` invocations. The slash command runs this directly. Only entries returned with `status == "success"` from the skill are processed.

---

## Entry Gate

```
# Phase 10 must have produced a results array
IF results is empty OR results is undefined:
    HALT - Phase 10 did not return; cannot link.

# Filter to successful posts only
linked_recs = [r for r in results if r.status == "success"]

IF len(linked_recs) == 0:
    Display: "No issues were posted successfully. Nothing to link."
    Display: "  • Failed: ${count(failed)}"
    Display: "  • Skipped: ${count(skipped)}"
    Display: "  • Cancelled: ${count(cancelled)}"
    HALT (gracefully — workflow ends here, no RCA mutation)
```

---

## Step 1: Update Implementation Checklist

The RCA recommendations section uses checklist items: `- [ ] REC-N`. After posting, replace each successful entry with a link to the new issue.

```
FOR result in linked_recs:
    rec_id       = result.rec_id            # e.g., "REC-1"
    issue_number = result.issue_number      # e.g., 42
    issue_url    = result.issue_url         # e.g., "https://github.com/bankielewicz/DevForgeAI/issues/42"

    # Idempotency: skip if already linked (BR-002)
    IF RCA_FILE contains "${rec_id}: See Issue-":
        Display: "  ⚠ ${rec_id} already linked — skipping (idempotency)"
        CONTINUE

    # Update checklist line
    Edit(
        file_path="${RCA_FILE}",
        old_string="- [ ] ${rec_id}",
        new_string="- [ ] ${rec_id}: See Issue-${issue_number} (${issue_url})"
    )
    Display: "  ✓ Updated checklist: ${rec_id} → Issue-${issue_number}"
```

**Why include the URL?** Reading the RCA later, a maintainer can click straight through to the issue without manually constructing the URL. The text fits within reasonable line width (~70 chars for issue #42; longer for 5-digit issue numbers).

---

## Step 2: Add Inline Issue References

Each `### REC-N:` section gets an `**Implemented in:**` line right after the header, mirroring the stories pattern.

```
FOR result in linked_recs:
    rec_id       = result.rec_id
    issue_number = result.issue_number
    issue_url    = result.issue_url

    # Idempotency: skip if inline ref already present
    IF RCA_FILE contains "**Implemented in:** Issue-${issue_number}":
        Display: "  ⚠ Inline reference for Issue-${issue_number} already exists — skipping"
        CONTINUE

    # Find the recommendation header line (the first occurrence)
    header_line = Grep(pattern="^### ${rec_id}:.*$", path="${RCA_FILE}", output_mode="content")[0]

    # Add inline reference after header
    Edit(
        file_path="${RCA_FILE}",
        old_string="${header_line}",
        new_string="${header_line}\n**Implemented in:** Issue-${issue_number} — ${issue_url}"
    )
    Display: "  ✓ Added inline reference: ${rec_id} → Issue-${issue_number}"
```

---

## Step 3: Preserve Original Content

- `Edit` tool performs atomic string replacement
- Only target strings are modified
- All other RCA content (Five Whys, Evidence, frontmatter except status, descriptions, prevention notes) preserved unchanged
- No full-file rewrites

This is critical — RCAs are constitutional documents in DevForgeAI. Inadvertent edits to other sections would constitute drift.

---

## Step 4: Handle Partial Posting

```
total_selected     = len(results)               # Everything Phase 10 attempted
posted_count       = len(linked_recs)           # status == success
failed_count       = count(results where status == "failed")
skipped_count      = count(results where status == "skipped")
cancelled_count    = count(results where status == "cancelled")

Display: ""
Display: "Linking Summary:"
Display: "  ✓ Linked:    ${posted_count} recommendations (issues posted + RCA updated)"
IF failed_count > 0:
    Display: "  ✗ Unlinked:  ${failed_count} recommendations (gh issue create failed)"
IF skipped_count > 0:
    Display: "  ⏭ Skipped:   ${skipped_count} recommendations (user excluded from subset)"
IF cancelled_count > 0:
    Display: "  ⨯ Cancelled: ${cancelled_count} recommendations (user cancelled approval)"
```

Recommendations with `status != "success"` remain marked `- [ ] REC-N` in the RCA (no `Issue-NNN` link). The user can re-run `/create-incident-from-rca RCA-NNN` later to handle them — Phase 1.5 of the skill (idempotency check) will detect the unposted recs and offer to retry.

---

## Step 5: Update RCA Status Field (Conditional)

```
# Determine the total recommendation count from the source RCA file
# (NOT from the results array — that only includes selected recs, but the RCA
# may have additional recs the user chose not to convert this run)

all_recs_in_rca = Grep(pattern="^### REC-[0-9]+:", path="${RCA_FILE}", output_mode="count")

# Count how many now have an Issue link
linked_recs_in_rca = Grep(pattern=": See Issue-[0-9]+", path="${RCA_FILE}", output_mode="count")

IF linked_recs_in_rca == all_recs_in_rca AND all_recs_in_rca > 0:
    # Every rec in this RCA has a posted issue (across one or more runs)
    Edit(
        file_path="${RCA_FILE}",
        old_string="status: OPEN",
        new_string="status: IN_PROGRESS"
    )
    Display: "  ✓ RCA status updated: OPEN → IN_PROGRESS (all recs have issues)"
ELSE:
    Display: "  ○ RCA status unchanged (${linked_recs_in_rca}/${all_recs_in_rca} recs linked)"
```

**Why count from the RCA file (not from `results`)?** Multi-run support. The user might run `/create-incident-from-rca RCA-049` today for 3 of 5 recs, then again next week for the remaining 2. The status update should fire only when ALL recs are linked, regardless of which run posted them.

---

## Step 6: Display Summary

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  RCA-Issue Linking Complete"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  RCA Document: ${RCA_ID}"
Display: "  Linked this run: ${posted_count} issues"
Display: "  RCA status: ${current_status}"
Display: ""
Display: "  Traceability established (this run):"
FOR result in linked_recs:
    Display: "    ${result.rec_id} → Issue-${result.issue_number} — ${result.issue_url}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Business Rules

| Rule | Implementation |
|------|----------------|
| BR-001: Traceability | Each posted issue's URL is embedded in the RCA — bidirectional reference (RCA → Issue via this phase, Issue → RCA via the issue body's "Context" section) |
| BR-002: Idempotency | Skip checklist update if `: See Issue-` already present for the rec; skip inline ref if `**Implemented in:** Issue-N` already present |
| BR-003: Partial Linking | Only process results with `status == "success"`; failed/skipped/cancelled recs stay unlinked |
| BR-004: Status Transition | RCA `status` → IN_PROGRESS only when ALL RCA recs have Issue links (multi-run aware) |
| BR-005: No Full-File Rewrites | Use Edit tool for atomic replacement; preserve all unrelated content |

---

## Validation Checkpoint

Before phase completion, verify:

- [ ] Checklist items updated for all successful posts (Step 1)
- [ ] Inline references added for all successful posts (Step 2)
- [ ] Original RCA content preserved (Step 3)
- [ ] Partial posting handled correctly (Step 4)
- [ ] RCA status field updated appropriately (Step 5)
- [ ] Summary displayed (Step 6)

**IF any checkbox UNCHECKED:** HALT, surface which step failed, do not exit cleanly.

---

## Difference from /create-stories-from-rca's linking

Three intentional changes:

1. **Reference format** — `Issue-NNN (URL)` instead of `STORY-NNN`. The URL is included because issues live on a remote server; without the URL, a future reader has to manually construct it.
2. **Status update timing** — Same logic (all recs linked → IN_PROGRESS), but counts based on `Issue-` matches in the file instead of `STORY-` matches.
3. **Implemented-in marker** — `**Implemented in:** Issue-NNN — URL` instead of `**Implemented in:** STORY-NNN`.

The atomic-edit pattern, idempotency check, and content-preservation guarantees are identical.
