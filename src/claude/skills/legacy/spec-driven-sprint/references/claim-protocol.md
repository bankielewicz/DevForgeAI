# Claim/Release Protocol Reference

Defines the claim algorithm, race rule, degradation, and determinism boundary for the issue claim/release protocol inserted into the core sprint route (Phase 00 Step 5 + Phase 06 Step 2).

---

## Purpose

Two parallel `/spec-sprint` sessions on the same issue proceed silently and collide at PR time. The claim/release protocol prevents this by posting a `/claim` comment at sprint start and `/release` at PR open — giving concurrent sessions a visibility mechanism to yield before doing duplicate work.

---

## Claim Algorithm (Phase 00 Step 5)

1. **Check issue state.** `gh issue view ${ISSUE_NUMBER} --json state,comments` — HALT via AskUserQuestion if the issue is not OPEN. A CLOSED issue signals the work is done.

2. **Active-claim scan.** Scan comments for a `/claim` comment (first token of the comment body is `/claim`) with no later `/release` comment from the same author AND no merged PR linking `Fixes #${ISSUE_NUMBER}` in the same session's timeline. If an active claim is found: HALT/yield, reporting the holder's GitHub username and the claim timestamp. The user decides whether to wait, investigate, or proceed under the existing claim.

3. **Post claim comment** (if no active claim found):
   ```
   /claim — spec-sprint session on branch <branch>, started <UTC ISO 8601 timestamp>. Will /release on PR open or abandonment.
   ```
   Post via `gh issue comment ${ISSUE_NUMBER} --body-file tmp/${ISSUE_ID}/claim-comment.md` (body-file, never inline — string hygiene rule from `references/devforgeai-addendum.md`). Write the claim body to the tmp file before posting.

4. **Race check.** After posting, re-read all comments. The `/claim` comment with the **earliest `created_at` timestamp** wins. If our claim was not the earliest: post `/release — yielding to earlier claim` and HALT. The user may monitor the other session and re-run later.

5. **Write `tmp/${ISSUE_ID}/claim.json`:**
   ```json
   {
     "issue_number": <n>,
     "claimed_at": "<ISO timestamp>",
     "comment_url": "<url>",
     "branch": "<branch>",
     "released": false
   }
   ```

---

## Release (Phase 06 Step 2)

After `gh pr create` succeeds, post:
```
/release — PR #<pr_number> open
```
via `gh issue comment ${ISSUE_NUMBER} --body-file tmp/${ISSUE_ID}/release-comment.md`. Update `claim.json.released = true`.

---

## Race Rule

**Earliest `created_at` wins.** If two sessions post `/claim` within the same second (a network race), both parse the same timestamp — neither can determine it "won". In this rare case, both should display the tie condition and HALT, letting the user decide which session to continue. Do not proceed on a tie without user confirmation.

---

## Degradation

If `gh` is unavailable or unauthenticated when the claim protocol runs:
1. Log: `WARNING: claim protocol skipped (gh unavailable)`
2. Write `tmp/${ISSUE_ID}/claim.json {"skipped": "gh-unavailable"}`
3. Continue with the sprint — the claim protocol is advisory, not a hard gate.

The sprint NEVER fails solely because the claim protocol is unavailable. A missing `claim.json` or `{"skipped":"gh-unavailable"}` is not a gate failure.

---

## Determinism Boundary

The claim protocol is:
- **Network-dependent:** `gh issue comment` and `gh issue view` require live network.
- **Skill-step + artifact:** implemented as Phase 00 Step 5 and a `claim.json` artifact — NOT a CLI gate or hook (PR#433: "claim checks are network-dependent and are skill-step + artifact, NOT a hard hook gate").
- **Not LLM-proof:** a session can technically skip the claim step. The protocol is social (visible to humans via issue comments) rather than machine-enforced.

---

## References

- `phases/phase-00-init.md` Step 5 — claim protocol step
- `phases/phase-06-pr.md` Step 2 — /release post
- `references/devforgeai-addendum.md` — body-file string hygiene rule
