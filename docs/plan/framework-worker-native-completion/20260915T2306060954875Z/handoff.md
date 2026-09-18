# Development and independent-retest handoff

## Current disposition

**FAIL — mandatory coverage floor.** Frozen candidate manifest `809a8beb50f8b57198a963725fd0d2ccd5e586a1243e177284bff3d6dfa471dd`; independent complete measurement 2,852/3,103 = 91.91105381888495%. The 89/89 passing Rust functions and successful fmt/Clippy do not waive the 95% coverage requirement. Preserve this failure and its raw report; no repairs or coverage-improving reruns were made after the stop.

## Next development assignment

1. Start from the exact frozen 48-file candidate and selected three worker contracts. Read the independent QA report and uncovered-line analysis. Preserve both manifests, source snapshot, old command attempts, fixtures, coverage JSON and raw profiles.
2. Add meaningful requirement-derived tests for unexecuted behavior, especially effective-profile validation, source inventory and runner/preflight orchestration. Use actual compiled CLI/process boundaries where required. Cover failures/recovery with independent expected results; do not copy product logic into the oracle, exclude uncovered production lines or lower the 95% threshold.
3. If those tests reproduce a product defect, retain the valid Red and implement the minimum authorized repair through Red → Green → refactor. A test-coverage gap alone does not establish a product defect.
4. Freeze changed bytes and publish a new manifest, source denominator and evidence directory. Request a fresh independent QA campaign covering all 20 WF parents/subfixtures, F-01/F-02, new preflight requirements, complete locked/offline regression, formatting, Clippy and all first-party executed-line coverage. The current 91.91105381888495% measurement remains historical evidence.

## Native prerequisites remain separate

After the quality gate passes, resolve the strict plugin-cache reparse prerequisite through an explicitly selected change; no operational link/configuration edit or inventory exception is authorized by this handoff. Then collect complete source identities, obtain actual compiled preflight observations, review the source-bound profile, and execute the existing one-shot WN-01/WN-02 selection. See [native-prerequisite.md](native-prerequisite.md) for exact ordering and limits.

Final-candidate live source collection, native preflight and both trials were NOT_RUN after the mandatory QA stop. The earlier evolving-candidate source denial must not be relabeled as final-candidate native evidence. Zero model-trial attempts were consumed.

The separate operator-attested protected acceptance authority remains deferred. Its implementation, independent qualification and provisioning require their own selected scope. Framework acceptance is NOT_EVALUATED and is not established.
