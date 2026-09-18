# Launch ownership and approvals

The first delegated launch request remained pending host approval and was canceled before execution. Readback immediately afterward found both attempt-001 directories sealed, with no started.json, process.json, or result.json. No actor was running from that delegated request.

The root agent then obtained direct host approval for both exact guarded launch commands and launched the same predeclared attempt-001 directories. Readback confirms ledger-c started at `2026-09-15T00:16:22.223901+00:00` and ledger-d at `2026-09-15T00:18:09.315820+00:00`.

This was transfer of an unstarted authorized launch, not a native retry. The plans, prompts, fixture/evaluator identities and 600-second limits were not changed. Root owns process polling and lifecycle. This evaluator only reads the resulting evidence and independently adjudicates it.
