# Repaired candidate final campaign

The final candidate is `057-final-clippy/candidate.json`, SHA256 `bd90e1161015553b7325bfa65ee64f8a04b57938894ee9aa68b4b4855a02384c`. It supersedes the prematurely named source-test-manifest.json, which is retained as an intermediate candidate and failed compilation in attempt 055 because a new test closure needed an explicit argument type. That was a test compilation ERROR, not Red. No production behavior was changed to resolve it.

The all-src denominator, exclusions and thresholds from qa-declaration-03.md remain unchanged. Execute all targets, all 20 mandatory WF cases with subfixtures and all supplemental tests. Collect coverage-04.json and run the normal noninstrumented all-target suite on the same candidate. Count mandatory cases once per candidate; do not aggregate retries. Native WN-01/WN-02 remain NOT_RUN and independent QA remains separately selected.

048 reproduces immediate forced termination before IDs (exit 1 of a cooperative peer). 050 passes after the cooperative EOF grace repair. The same grace also applies when interrupt transport is lost or recording server_started fails. A supplemental held-process test exercises the lost transport branch. 049 exercised only WF-15 due its command filter; 050 executed the named requirement, protocol and negative suites.

047 measured 1294/1362 (95.00734214390602%) on the previous candidate, with all 20 required and 22 supplemental tests passing. It is retained evidence, not qualification of the repaired candidate.
