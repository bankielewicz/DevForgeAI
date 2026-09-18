# Dependency-ordered implementation

1. S1 admission/oracle: strict closed request and review parsing, identities, disjoint fixture/run roots, expected result outside worker input. Tests exercise invalid schema, duplicate fields, IDs, hashes, paths, and exact output including unknown/duplicate keys (WF-17/18 components).
2. S2 journal/inspection: exclusive run admission, durable append-before-effects, strict bounded read-only pagination and incomplete/corrupt distinction (WF-09..12).
3. S3 owned process: atomic Job Object assignment, explicit inherited pipes, bounded concurrent readers, held-handle teardown and crash lifetime (WF-13..16 components).
4. S4 one-turn protocol: preflight, correlated events, permission refusal, final-item oracle, cancellation, usage, deadlines and terminal precedence. External peer independently checks full outbound trace (WF-01..08, WF-13..20 integration).
5. S5 frozen Windows QA: all 20 cases/subfixtures, formatting, Clippy, full src executed-line coverage and independent retest handoff. No native model trial.

Each slice first establishes a compiling seam and executes behavioral Red; setup errors are recorded separately. New implementation is selected because section 3 prohibits index workspace coupling and scoped source searches found no compatible existing worker implementation. Production files stay under the isolated package. Evidence stays under the bound implementation directory. Existing index Cargo files are hashed for preservation.

## Final execution lineage

- S1: 003/004 oracle and 005/007 admission Red/Green; strict profile and boundary repairs in 023/024, 034..036, 043/044. Setup errors are classified in development-notes.md.
- S2: 008/010 journal Red/Green, actual crash/lost stdout/junction integration in 025, expanded corruption and evidence failure checks retained in subsequent campaigns.
- S3: 011/012 owned process Red/Green, actual Ctrl+C and killed harness tests, production watchdog in full suites. 048/050 repaired pre-ID cooperative grace after a valid Red.
- S4: 013/015 protocol Red/Green, external negative stimuli and strict oracle; 040/041 repaired buffered correlation and usage sanitization. Completion duplicates/nonzero exit characterization expanded in 061 without runtime changes.
- S5: final frozen source/test manifest SHA256 177b5894a236a02c7d322df7f04d647632094a4a3f3998e7f2a150db246e1604. 063 Clippy, 064 format, 065 full coverage and 066 normal full suite PASS. Required 20/20 and supplemental 26/26 in each final suite; executed src lines 1310/1374 = 95.34206695778748%. All earlier evidence retained.

Delivery and independent handoff are complete for the selected offline development scope. WN-01/WN-02 and protected acceptance remain unperformed; no native capability is inferred.
