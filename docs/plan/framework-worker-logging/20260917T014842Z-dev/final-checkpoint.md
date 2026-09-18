# Final development checkpoint

The selected fresh candidate is implemented and offline development verification is complete. Source and output locations are unchanged from context.md. Final candidate-manifest.json, suite-summary.json, binary-manifest.json, artifact-index.json and post-seal-readback.json bind delivery; delivery.md reports the scope and metrics, and qa-handoff.md selects the next independent assessment.

The final package campaign passes all 152 required cases (49 units); a supplemental real Windows malformed-byte child passes one additional required case. Coverage is 3858/4041 lines (95.47141796585004%) with all executable source files included. Formatting, all-target Clippy and binary build pass. Runtime query_failed is exercised with a real access-denied Windows query. The original source, snapshot, selected inputs and earlier evidence indexes passed hash readback. Failed attempts and their raw coverage data remain.

Development result: COMPLETE for this scoped implementation and offline Windows verification. Independent product QA and native Codex execution: NOT_RUN. Framework acceptance: NOT_EVALUATED. Continue by independently assessing the sealed candidate in a fresh QA evidence directory; only after that passes prepare a separately authorized native diagnostic. No user approval is inferred from elapsed time or these development observations.
