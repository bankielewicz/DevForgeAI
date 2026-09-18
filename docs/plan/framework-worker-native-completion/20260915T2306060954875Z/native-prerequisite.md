# Native prerequisite and unchanged trial selection

## Observed prerequisite denial

The development command in `native-source-inspection-001/receipt.json` ran the compiled `profile-sources` operation against the contract-layout fixture at `docs/plan/framework-worker-trials/20260915T2306060954875Z-preflight/fixture`. It exited 3 in 0.031 seconds, with empty stdout and this stderr diagnostic:

```json
{"error":"profile_source_reparse:\\\\?\\C:\\Users\\bryan\\.codex\\plugins\\cache\\openai-bundled\\chrome\\latest"}
```

This is an expected fail-closed prerequisite outcome under DFF-WORKER-PREFLIGHT-01, not a reproduced Codex execution failure. It occurred on the evolving development candidate recorded in that receipt; final independent QA evidence must be distinguished from this earlier observation. The command launched no Codex child, thread or turn. Its source and executable hashes, exact argv, cwd, native status, timing and separate streams remain in that attempt directory.

No source call-chain was established proving that all cached plugin control files become irrelevant when plugins are disabled. The implementation therefore retains cache inventory and strict reparse rejection. Source hashes alone cannot establish effective inactivity. No operational cache link, configuration, credentials, startup settings or skill installation was changed.

## Required sequence after offline qualification

1. Resolve the source-inventory prerequisite through a separately selected, reviewable change. Do not silently omit the cache, follow the link, remove it, substitute a home directory or relax the current contract. If executable/configuration source bytes change, rebind them and repeat the affected independent QA.
2. Collect the complete source inventory using the compiled terminal operation. Bind the exact physical Codex 0.154.0 identity, compiled policy, sources, model and effort in a closed review v2 record.
3. Run one bounded compiled `preflight` inspection. The review may contain false findings for this inspection; those findings cannot authorize model work. Require actual effective configuration, feature, hook, plugin, installed-app, MCP, account/model/effort and sandbox evidence, with source rechecks and verified cleanup.
4. Have the selected operator review the concrete source-bound observations. Native `run` requires all four findings true and repeats its own inspection before a turn. No model-authored report can supply operator or protected framework authority.
5. Execute the already-selected WN-01 completion and WN-02 cancellation trials once each only after every prerequisite is satisfied. Preserve their outcomes, including denial, failure or a cancellation/completion race, without automatic retry.

The selection remains Codex 0.154.0, `gpt-6-astra`, `high`, native Windows x64, immutable fixture, dispatch 120 seconds, RPC 10 seconds, interrupt grace 5 seconds, teardown 5 seconds and external supervision 145 seconds. Keep harness stdin open until the intended cancellation/completion; EOF requests cancellation. Actual trial attempts consumed in this assignment: zero of two.

## Authority boundary

Protected acceptance authority implementation/provisioning is deferred and outside this worker scope. Worker observations, passing Rust tests, operator profile review and this handoff cannot issue protected framework acceptance. Framework acceptance is `NOT_EVALUATED` and is not established.
