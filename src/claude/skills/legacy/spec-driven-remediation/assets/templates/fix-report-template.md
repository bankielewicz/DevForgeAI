# Fix Session Report Template

Use this template to generate the fix report in Phase 05.

---

## Fix Session Report

**Audit Source:** {AUDIT_FILE}
**Session Date:** {CURRENT_DATE}
**Mode:** {MODE_LABEL}

### Results Summary

| Outcome | Count |
|---------|-------|
| Applied (automated) | {COUNT_AUTO_APPLIED} |
| Applied (interactive) | {COUNT_INTERACTIVE_APPLIED} |
| Deferred | {COUNT_DEFERRED} |
| Skipped | {COUNT_SKIPPED} |
| Failed verification | {COUNT_FAILED} |
| Previously fixed | {COUNT_PREVIOUSLY_FIXED} |

### Applied Fixes

{FOR_EACH_APPLIED}
- [x] {FINDING_ID} ({TYPE}): {CHANGE_SUMMARY} -- verified
{END_FOR_EACH}

### Deferred Items

{FOR_EACH_DEFERRED}
- [ ] {FINDING_ID} ({SEVERITY}): {REASON}
{END_FOR_EACH}

### Remaining Findings

{FOR_EACH_REMAINING}
- {FINDING_ID} ({SEVERITY}): {SUMMARY}
{END_FOR_EACH}

### Next Steps

{NEXT_STEPS}

---

## Template Variables

| Variable | Source | Description |
|----------|--------|-------------|
| `AUDIT_FILE` | Context marker | Path to audit file |
| `CURRENT_DATE` | Runtime | Today's date (YYYY-MM-DD) |
| `MODE_LABEL` | DRY_RUN/AUTO_ONLY flags | "Dry Run", "Auto Only", or "Full" |
| `COUNT_*` | Findings list | Counts by status/classification |
| `FOR_EACH_APPLIED` | Findings WHERE status=applied AND verification=passed | Applied fix details |
| `FOR_EACH_DEFERRED` | Findings WHERE status=deferred | Deferred item details |
| `FOR_EACH_REMAINING` | Findings WHERE status=pending OR status=skipped | Unprocessed findings |
| `NEXT_STEPS` | Conditional logic | Guidance based on remaining work |

### Next Steps Logic

```
IF all findings resolved (no pending, no skipped, no failed):
    NEXT_STEPS = "All findings resolved. Run `/validate-stories` to confirm clean audit."
ELIF remaining findings exist:
    NEXT_STEPS = "Re-run `/fix-story` to address remaining findings."
IF deferred items exist:
    NEXT_STEPS += "\nAddress deferred items in a future session."
```
