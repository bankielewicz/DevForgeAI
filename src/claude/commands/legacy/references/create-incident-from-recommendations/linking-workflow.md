# Phase 11: QA-Recs Linking Workflow

**Purpose:** Record the link-back between each posted GitHub issue and the source QA recommendation for traceability and cross-run idempotency, after Phase 10 (issue creation skill) completes.

This is a simple manifest-write phase — no GitHub API calls, no gh-CLI invocations. The slash command runs this directly. Only entries returned with `status == "success"` from the skill are processed.

The `last_posted_at` frontmatter field and the `## Posting Audit Trail` section are owned by the skill (Phase 6 + BR-014), not by this slash command. This phase records the per-rec `**Posted as:**` link-back to a posting manifest in `tmp/${STORY_ID}/posting-manifest.json`.

**Why a manifest, not an in-place Edit of the QA recs file?** `feedback-artifact-write-gate.sh` (PreToolUse[Edit|Write], ADR-062 D2) blocks any Edit/Write under `devforgeai/qa/recommendations/**` while a workflow is active. An in-place marker insertion was the original design — but it silently failed during the normal /qa → /create-incident-from-recommendations flow (workflow active), and the skill's Phase 1.5 idempotency check then missed the prior posts and produced duplicates. The manifest-link-back pattern mirrors the sibling `github-incident-from-feedback` skill's solution (PR #76 / advisor catch). The QA recs file is unmutated; the manifest is the durable cross-run idempotency source.

---

## Entry Gate

```
# Phase 10 must have produced a results array
IF results is empty OR results is undefined:
    HALT — Phase 10 did not return; cannot link.

# Filter to successful posts only
linked_recs = [r for r in results if r.status == "success"]

IF len(linked_recs) == 0:
    Display: "No issues were posted successfully. Nothing to link in QA recs file."
    Display: "  • Failed:    ${count(failed)}"
    Display: "  • Skipped:   ${count(skipped)} (idempotency or user-excluded)"
    Display: "  • Cancelled: ${count(cancelled)}"
    HALT (gracefully — workflow ends here, no QA-recs mutation)
```

---

## Step 1: Write Per-Rec Link-Back to Posting Manifest

For each successful post, append an entry to `tmp/${STORY_ID}/posting-manifest.json` recording the rec→issue link.

**Manifest path:** `tmp/${STORY_ID}/posting-manifest.json` (per `.claude/rules/workflow/operational-safety.md` Rule 2: project-scoped `tmp/`; never system `/tmp/`).

**Manifest schema** (top-level object; the `links` array is the source of truth; the object is rewritten in full each run to keep the schema stable):

```json
{
  "schema_version": "1.0",
  "story_id": "STORY-661",
  "qa_recs_file": "devforgeai/qa/recommendations/STORY-661-qa-recommendations.md",
  "last_updated": "2026-05-20T19:45:00Z",
  "links": [
    {
      "rec_id": "REC-STORY-661-M-001",
      "issue_number": 42,
      "issue_url": "https://github.com/bankielewicz/DevForgeAI/issues/42",
      "posted_at": "2026-05-20T19:43:11Z"
    }
  ]
}
```

**Pseudocode:**

```
MANIFEST_PATH = f"tmp/{STORY_ID}/posting-manifest.json"
mkdir -p "tmp/{STORY_ID}/"  # Rule 2: project-scoped tmp

# Load existing manifest if present (preserves prior runs' links — idempotency
# across multiple /create-incident-from-recommendations invocations).
IF file_exists(MANIFEST_PATH):
    manifest = json.parse(Read(file_path=MANIFEST_PATH))
ELSE:
    manifest = {
        "schema_version": "1.0",
        "story_id": STORY_ID,
        "qa_recs_file": QA_RECS_FILE,
        "last_updated": null,
        "links": []
    }

# Build a set of rec_ids already linked in the manifest (BR-002 idempotency).
existing_rec_ids = { link["rec_id"] for link in manifest["links"] }

FOR result in linked_recs:
    rec_id       = result.rec_id            # e.g., "REC-STORY-661-M-001"
    issue_number = result.issue_number      # e.g., 42
    issue_url    = result.issue_url         # e.g., "https://github.com/bankielewicz/DevForgeAI/issues/42"

    # Idempotency: skip if rec already linked in manifest (BR-002).
    IF rec_id in existing_rec_ids:
        Display: f"  ⚠ {rec_id} already linked in posting-manifest.json — skipping (idempotency)"
        continue

    manifest["links"].append({
        "rec_id":       rec_id,
        "issue_number": issue_number,
        "issue_url":    issue_url,
        "posted_at":    datetime.now(timezone.utc).isoformat(timespec="seconds")
    })
    Display: f"  ✓ Linked in manifest: {rec_id} → Issue-{issue_number}"

# Single Write of the full manifest object (atomic; preserves any prior links).
manifest["last_updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
Write(file_path=MANIFEST_PATH, content=json.dumps(manifest, indent=2))
```

**Why include the URL in the manifest?** A maintainer (or the skill's next-run Phase 1.5 idempotency check) can resolve `rec_id → issue_url` without round-tripping through GitHub. Adds ~70 bytes per link — negligible.

**The QA recs file is NOT mutated by this phase.** Its content (frontmatter, SECTION_MANIFEST, recs, deferred section, audit trail) is preserved bit-for-bit. The skill's Phase 6 audit trail still owns its own evidence; this phase owns only the link-back manifest.

---

## Step 2: Preserve Original Content

- The QA recs file is **never modified** by Phase 11. (Step 1 writes only to `tmp/${STORY_ID}/posting-manifest.json`.)
- The skill's Phase 6 (`last_posted_at` frontmatter + `## Posting Audit Trail`) is its own concern; this phase does not touch those either.
- The original Edit-based design (pre-PR-with-this-fix) was silently blocked by `feedback-artifact-write-gate.sh` (ADR-062 D2) during active workflows; the manifest pattern eliminates that seam entirely.

QA recs files are inputs to other workflows (review, audit, regeneration). Leaving them unmutated means zero drift risk from Phase 11.

---

## Step 3: Handle Partial Posting

```
total_selected     = len(results)               # Everything Phase 10 attempted
posted_count       = len(linked_recs)           # status == success
failed_count       = count(results where status == "failed")
skipped_count      = count(results where status == "skipped")
cancelled_count    = count(results where status == "cancelled")

Display: ""
Display: "Linking Summary:"
Display: f"  ✓ Linked:    {posted_count} recommendations (issues posted + QA recs marked)"
IF failed_count > 0:
    Display: f"  ✗ Unlinked:  {failed_count} recommendations (gh-CLI invocation failed — see error_message)"
IF skipped_count > 0:
    Display: f"  ⏭ Skipped:   {skipped_count} recommendations (idempotency or user-excluded subset)"
IF cancelled_count > 0:
    Display: f"  ⨯ Cancelled: {cancelled_count} recommendations (user cancelled approval)"
```

Recommendations with `status != "success"` remain unmarked in the QA recs file. The user can re-run `/create-incident-from-recommendations STORY-NNN` later to handle them — Phase 1.5 of the skill (idempotency check) will detect the unmarked recs and offer to retry.

---

## Step 4: Source-RCA Cross-Linking (Conditional, Rare)

Some QA recommendations carry a `source_rca:` pointer in their YAML — meaning the rec originated from an earlier RCA's recommendation that was acted upon and then re-validated by QA. In that case, the RCA file should also reflect the new GitHub issue.

```
FOR result in linked_recs:
    rec = lookup_rec_in_qa_recs_document(result.rec_id)
    IF rec.source_rca:
        rca_id = rec.source_rca         # e.g., "RCA-067"
        rca_rec_id = rec.source_rca_rec_id   # e.g., "REC-3" within the RCA

        # Find the RCA file
        Glob(pattern=f"devforgeai/RCA/{rca_id}*.md")

        # Add a cross-reference line under the source rec section
        Edit(
            file_path=RCA_FILE,
            old_string=f"### {rca_rec_id}:",
            new_string=f"### {rca_rec_id}:\n**Subsequently tracked in:** Issue-{result.issue_number} — {result.issue_url} (via QA cycle of STORY-NNN)\n"
        )
```

This branch is rare and only fires when the QA rec carries a `source_rca:` pointer. Most QA recs are NEW findings without RCA provenance.

---

## Step 5: Validation Checkpoint

Before phase completion, verify:

- [ ] Posting manifest written at `tmp/${STORY_ID}/posting-manifest.json` containing one `links[]` entry per successful post (Step 1)
- [ ] QA recs file content unchanged (Step 2 — Phase 11 never touches the QA recs file under the manifest pattern)
- [ ] Partial posting summary displayed (Step 3)
- [ ] Source-RCA cross-references added if applicable (Step 4)

**IF any checkbox UNCHECKED:** HALT, surface which step failed, do not exit cleanly.

The validation is a static post-condition check:
```
manifest = json.parse(Read(file_path=f"tmp/{STORY_ID}/posting-manifest.json"))
manifest_rec_ids = { link["rec_id"] for link in manifest["links"] }
expected_rec_ids = { r.rec_id for r in linked_recs }

missing = expected_rec_ids - manifest_rec_ids
IF missing:
    Display: f"❌ Manifest missing links for: {missing}"
    HALT
```

---

## Step 6: Display Final Summary

```
Display: ""
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: "  QA Recs ↔ Issue Linking Complete"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
Display: f"  Story:           {STORY_ID}"
Display: f"  QA recs file:    {QA_RECS_FILE}"
Display: f"  Linked this run: {posted_count} issues"
Display: ""
Display: "  Traceability established (this run):"
FOR result in linked_recs:
    Display: f"    {result.rec_id} → Issue-{result.issue_number} — {result.issue_url}"
Display: "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
```

---

## Business Rules

| Rule | Implementation |
|------|----------------|
| BR-001: Traceability | Each posted issue's URL is recorded in `tmp/${STORY_ID}/posting-manifest.json` via a `links[]` entry — bidirectional reference (QA recs → Issue via the manifest, Issue → STORY via the issue body's "Context" section). The skill's Phase 1.5 idempotency check consults this manifest. |
| BR-002: Idempotency | Skip manifest append if `rec_id` already present in `manifest.links[]` |
| BR-003: Partial Linking | Only process results with `status == "success"`; failed/skipped/cancelled recs stay out of the manifest |
| BR-004: Audit-Trail Boundary | This phase does NOT touch `last_posted_at` frontmatter or `## Posting Audit Trail` section — those are owned by the skill (BR-014). Slash-command Phase 11 only writes the per-story posting manifest |
| BR-005: No QA Recs Mutation | This phase writes ONLY to `tmp/${STORY_ID}/posting-manifest.json`. The QA recs file is never modified, sidestepping `feedback-artifact-write-gate.sh` (ADR-062 D2) and ensuring zero drift risk for the QA recs file itself |
| BR-006: Source-RCA Cross-Linking | If a rec has `source_rca:` pointer, also update the source RCA file with `**Subsequently tracked in:** Issue-NNN`. RCA files are under `devforgeai/RCA/` (not gated by ADR-062 D2), so Edit is safe there |

---

## Difference from /create-incident-from-rca's linking

| Dimension | RCA pathway | This pathway |
|-----------|-------------|--------------|
| Marker format | `- [ ] REC-N: See Issue-NNN (URL)` (replaces the checklist line in the RCA file) | `links[]` entry in `tmp/${STORY_ID}/posting-manifest.json` (no QA recs file mutation; see BR-005) |
| Inline ref format | `**Implemented in:** Issue-NNN — URL` under the `### REC-N:` header | Single marker only — QA recs format has no equivalent of RCA's two-place reference |
| Status field update | `status: OPEN → IN_PROGRESS` when ALL recs linked | None — QA recs have no `status:` field; the audit trail (skill BR-014) tracks posting state |
| Multi-run support | Counts `Issue-NNN` matches across the whole RCA file | Idempotency check on per-rec basis; skill Phase 1.5 handles re-runs cleanly |
| Source cross-ref | N/A | `source_rca:` pointer triggers a parallel RCA file update (Step 4) |

The atomic-edit pattern, idempotency check, and content-preservation guarantees are identical between the two pathways.
