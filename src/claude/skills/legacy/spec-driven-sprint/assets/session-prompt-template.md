# Session Prompt Template — Backlog Triage

Fill contract: 6 tokens (${TRIAGE_ID}, ${MANIFEST_PATH}, ${READINESS_SUMMARY}, ${WAVE_SUMMARY}, ${ISSUE_COUNT}, ${DEGRADED_COUNT}).
Output file: `tmp/${TRIAGE_ID}/session-prompt.md`.

---

## Template

```
=== BACKLOG TRIAGE SESSION PROMPT ===
Triage ID:     ${TRIAGE_ID}
Manifest:      ${MANIFEST_PATH}
Open issues:   ${ISSUE_COUNT} (${DEGRADED_COUNT} UNPARSEABLE → serial)

READINESS STATUS
${READINESS_SUMMARY}

EXECUTABLE WAVE PLAN
${WAVE_SUMMARY}

HOW TO USE
----------
1. Read the readiness status and executable wave plan above.
2. Choose an issue only from EXECUTABLE WAVE PLAN, using the earliest available wave.
   If EXECUTABLE WAVE PLAN is empty, stop and ask the user which non-executable status to resolve first.
3. Check the live issue state:
   gh issue view <number> --json state,comments
4. Look for an active /claim comment (no later /release + no merged PR).
   - If claimed: pick a different issue or wait.
   - If unclaimed: run /spec-sprint <number>.
5. /spec-sprint will post a /claim comment automatically (Phase 00 Step 5).
6. When your PR merges, /release is posted automatically (Phase 06 Step 2).
7. Re-read this prompt each session — live gh state supersedes the manifest wave
   plan (some issues may have been claimed, completed, or deprioritized since
   the manifest was generated).

IMPORTANT: Do NOT auto-invoke /spec-sprint for all issues in a loop.
The user pastes this prompt into each parallel session manually.
Each session claims ONE issue and runs /spec-sprint for that issue only.

Manifest path for re-reading: ${MANIFEST_PATH}
```

---

## Fill Rules

1. HTML-escape is NOT required — this is a plaintext Markdown file, not HTML.
2. Empty `${READINESS_SUMMARY}` → substitute `"(manifest contains 0 open issues)"`.
3. Empty `${WAVE_SUMMARY}` → substitute `"(no executable issues; resolve readiness statuses first)"`.
4. `${WAVE_SUMMARY}` must exclude `close-as-implemented`, `close-as-superseded`, `blocked-by-dependency`, `needs-user-decision`, and any issue with `manual_preflight_required: true`.
5. `${MANIFEST_PATH}` must be repo-relative (e.g., `tmp/TRIAGE-20260612-100000/backlog-manifest.json`), never an absolute path.
6. Verify: no unfilled `${...}` tokens remain after substitution.
7. Idempotent: re-running T03 with the same manifest overwrites `session-prompt.md` with identical content (deterministic fill).
