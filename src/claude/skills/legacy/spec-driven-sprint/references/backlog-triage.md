# Backlog Triage Reference

Defines the selector grammar, `backlog-manifest-v1` schema, idempotency rules, and W3 statement for the `/spec-sprint --backlog <selector>` triage sub-route.

---

## Selector Grammar

`$BACKLOG_SELECTOR` is passed to `/spec-sprint` as `--backlog <selector>`. Three supported forms:

| Form | Syntax | Example | Resolves to |
|------|--------|---------|-------------|
| Issue range | `NNN-MMM` | `399-430` | gh issue list filtered to issue numbers NNN..MMM inclusive |
| Label filter | `label:<name>` | `label:bug` | gh issue list with `--label <name>` |
| gh search query | any string | `is:open milestone:v1.2` | gh issue list with `--search '<query>'` |

Unknown forms → HALT → ask the user in Phase T00.

---

## backlog-manifest-v1 Schema

```json
{
  "schema": "backlog-manifest-v1",
  "issues": [
    {
      "number": 401,
      "title": "...",
      "url": "https://...",
      "labels": ["bug"],
      "class": 0,
      "files": ["src/a.py", "src/b.py"],
      "files_parse": "OK",
      "readiness_status": "execute-existing-issue",
      "resolution_path": "run one supervised spec-sprint for this issue",
      "readiness_evidence": ["issue body ACs verified", "no active claim found"],
      "manual_preflight_required": false,
      "priority_rank": 1,
      "priority_rationale": "..."
    }
  ],
  "overlap_matrix": [
    {"a": 401, "b": 402, "shared_files": ["src/a.py"]}
  ],
  "clusters": [[401, 402]],
  "waves": [[401, 402], [403]],
  "parallelism": {
    "metric": 2,
    "max_width": 2,
    "degraded_serial": [404]
  }
}
```

**`files_parse`:** `"OK"` when `## Files to change` was found and parsed; `"UNPARSEABLE"` when the section was absent (issue body does not conform to the incident template). UNPARSEABLE issues are placed in trailing serial waves.

**`readiness_status`:** manual preflight classification from `tmp/${TRIAGE_ID}/readiness.json`. Allowed values:
- `execute-existing-issue`
- `complete-partial-issue`
- `close-as-implemented`
- `close-as-superseded`
- `blocked-by-dependency`
- `needs-user-decision`

**`manual_preflight_required`:** `true` means the issue is excluded from executable sprint prompts until a human resolves the classification. T03 executable wave output includes only `execute-existing-issue` and `complete-partial-issue` entries with `manual_preflight_required == false`.

**Exit codes of `devforgeai-validate triage-backlog`:**
- `0`: manifest written
- `1`: zero OPEN issues (manifest written with empty arrays — degenerate-but-valid)
- `2`: missing or malformed input JSON or malformed readiness JSON

---

## Idempotency Rules

1. Running triage again with the same `issues.json` produces byte-identical wave assignments (deterministic algorithm, no random state).
2. `TRIAGE_ID` includes a UTC timestamp — each `/spec-sprint --backlog` run gets a fresh id and fresh artifacts. Previous triage runs are never overwritten.
3. The manifest is self-contained: it can be re-read by a cold session without re-running T01/T02.

---

## W3 Statement

The triage route NEVER auto-invokes `/spec-sprint` per issue. The `session-prompt.md` artifact instructs the user to paste the prompt into 1..N sessions manually. Automating that step is a W3 (auto-skill-chaining) violation. See the W3 prohibition in `phases/triage-03-emit.md`.

---

## References

- `phases/triage-00-init.md` — T00 Init
- `phases/triage-01-fetch-prioritize.md` — T01 Fetch + Prioritize
- `phases/triage-02-overlap.md` — T02 Compute Overlap
- `phases/triage-03-emit.md` — T03 Emit + STOP
- `assets/session-prompt-template.md` — fill-token template for the session prompt
- `src/codex/scripts/devforgeai_cli/commands/triage_backlog.py` — CLI implementation
