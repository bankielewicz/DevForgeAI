# Integrated developer QA contract

Declared after candidate freeze and enumeration, before complete execution or coverage collection. Candidate manifest: `c27d8ce1742ba7cd0955f0bd18aded8de5f14c898c989654d7298835c3256f9e`, 53 files. Windows x64, default configuration; no optional package features. Selected contracts and their unchanged hashes are in `inputs-manifest.json`.

## Requirements and expected results

| Required group | Requirement and expected result | Cases / level | Evidence and initial status |
| --- | --- | --- | --- |
| Original WF-01 through WF-20 and F-01/F-02 | Feasibility sections 4–8: exact lifecycle, errors, cancellation/timeout, typed evidence, cleanup and fixture immutability. Every original parent and subfixture must pass; full pipes cannot delay cancellation and private error payload fields must be absent. | Existing contract/protocol/process/admission/oracle/regression cases; real Windows peers and process trees | `full-tests`, `full-coverage`; NOT_RUN |
| Original native readiness and preflight offline cases | Native readiness NI-T01–NI-T12 and preflight PF contracts: typed restrictive policy, identity and source drift rejection, fail-closed effect inventories. Synthetic checks qualify offline behavior only. | Existing identity/profile/policy/preflight tests; unit and real process integration | `full-tests`, `full-coverage`; NOT_RUN |
| Effective-profile edge cases | Eight case functions and their expected positive/negative subfixtures declared in `effective-dev/case-map.md`; reject malformed, incomplete, active or unknown state; project only approved typed fields. | New public-library tests | `full-tests`, `full-coverage`; NOT_RUN |
| Source-inventory edge cases | Eight functions, declared in `sources-dev/matrix.md`: literal schema, entry/byte/member/depth bounds, types, credential names, plugin grammar and freshness, with real files. | New private unit and filesystem tests | `full-tests`, `full-coverage`; NOT_RUN |
| Protocol PE-01–PE-09 | Nine cases in four functions, declared in `protocol-dev/traceability.md`: captured denial replies, no work, bounded pagination, sanitized stderr and explicit unavailable quota. | New real compiled peer/process/IPC tests | `full-tests`, `full-coverage`; NOT_RUN |
| Runtime RT-01–RT-05 | Five functions declared in `root-cases.md`: missing fixture, evidence-write failures, CLI diagnostics and both review entrypoints must reject unqualified evidence without work. | Library/filesystem/compiled CLI | `full-tests`, `full-coverage`; NOT_RUN |
| Build and static checks | Cargo lockfile unchanged, build offline and locked; rustfmt clean; Clippy all targets with warnings denied; applicable doctests | Native toolchain | `full-tests`, `final-fmt`, `final-clippy`, `doc-tests`; NOT_RUN |
| QA-F-COV-01 | All first-party executable lines >=95%; complete raw LLVM JSON and profiles; no removed source or per-file exclusions | Full instrumented all-target run | `source-denominator.json`, `full-coverage/coverage.json`, `coverage-analysis.json`; NOT_RUN |

`required-cases.json` enumerates 114 unique required executable functions: 28 unit and 86 integration functions. The 20 WF parent cases are a subset, not 20 extra passes. All nested fixtures must succeed. The 25 new functions are characterization tests of requirements already implemented; no functional Red or runtime repair is claimed. Instrumented repetitions and focused attempts remain separate records and do not increase the denominator.

Coverage source denominator: all 12 Rust files under `src/`, recursively resolved and hash-bound before measurement. `lib.rs` may contribute zero executable lines if LLVM reports only module declarations. Tests, test-support programs and third-party dependencies are excluded by ownership, never by result. Branch coverage is separately NOT_RUN unless supported raw branch records exist.

Minimum pass rate: exact passing required functions /114 >=95%, with no mandatory-case failure, unresolved regression or authority/security failure waived. Minimum executed-line coverage: >=95%, no rounding. A valid subthreshold metric, established result manipulation or confirmed critical security/data-loss defect stops this assignment; preserve evidence and deliver a failure handoff without automatic repairs or retries.

Native WN-01/WN-02 are outside this defect-retest denominator. Both remain separately required for native readiness and blocked by the unresolved source/profile prerequisites, with zero new attempts. Native profile collection/launch and protected authority provisioning are not actions in this coverage remediation.
