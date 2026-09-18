# Dev QA Root Cause Analysis and Remediation Plan

Approved for implementation by the user's "Implement the plan." instruction. Original planning review selected permanent fixes for both causes.

## Assessment and confirmed causes

The selected QA report is docs/plan/skill-validations/dev/20260913T2310456388212Z/validation-report.md (SHA-256 88297dbba18fdc04f31f1d9b3d56e817d0f71ccc9ce0fde8ad2a0dbab6726c64). It reports 16 PASS, 1 FAIL, 1 NOT_RUN / 18 = 88.89%.

DV-17: the cold task replaced the explicit custom receipts/ with receipts/ in its context/output mapping. Its completion audit checked hashes, tests, preservation, and absence of evidence/, but never compared actual destinations to the original selection. Internal consistency of an incorrect mapping led to false VERIFIED/COMPLETE. The model-internal reason for dropping the word is unknown.

DV-16: builder retains the contract's forward-slash target_root but emits native str(Path(...)) in records/request. Strict validator intake rejects the inconsistent strings. Existing regression fixtures use native str(Path(...)) and miss this valid alternative input spelling.

Original dev package digest: 7b8bb8f34a691e8d4f186d2c688501e370cae072238b52e587d10455c35b1aae. Read-only provenance review verified the authored baseline and eleven matching current files. The old packet remains rejected; no adoption or history rewrite is needed.

## Builder correction

Owner: skill-creator for development builder maintenance; a separate skill-validator stage owns regressions.

- Preserve original supplied contract bytes/digest in the fresh run.
- After existing path checks, generate an effective contract using native absolute project_root and target_root. Store original/resolved identity. Normalize separators and absolute location only, without renaming components, indiscriminate case folding, substituting Windows/WSL roots, or following prohibited links.
- Bind the effective contract bytes in custody records; retain the original source reference for drift detection.
- Emit identical effective identities in contract, record, baseline, and request. Preflight consistency before publication writes. Stop previously staged inconsistent runs with a fresh-run requirement rather than silently rewriting them.
- Preserve schemas, historical records/readers, write checks, and partial failure semantics. Keep validator production intake unchanged and do not make builder invoke it automatically.
- Add regressions to the existing validator-owned authoring integration suite.

## Dev correction

Owner: skill-builder, using the verified prior authored baseline and the explicit proposal:
docs/plan/skill-validations/dev/20260913T2310456388212Z/revision-spec.md
SHA-256 d4fdb404ebf3e869d4d2b6f99756cf70d54a460a369a74bd3f645f5cb9cfe1b9.

Implement REV-001 through REV-004:
- Preserve selected_evidence_value, original selection source, resolved root, and logical output mapping before the first evidence write.
- Preserve complete literal multiword paths and compare with original inputs rather than paraphrases.
- Retain destination identity in checkpoints and detect resume drift.
- Read back all promised outputs at their required locations before VERIFIED/COMPLETE.
- On mismatch report required/actual locations and PARTIAL/BLOCKED; preserve erroneous attempts.
- Focus edits on entrypoint, context/evidence/delivery references and relevant templates. Preserve implementation/TDD, execution fields, portability and unaffected requirements. No runtime helper or fixed product root is needed.

## Verification

Builder red -> green -> refactor -> QA:
Execute a failing forward-slash Windows producer-to-intake case before code changes. Verify native/forward/mixed spelling, literal spaces/Unicode/brackets/dollar signs, retained raw input and drift, effective-contract tampering, stale digests/wrong targets, traversal/protected roots/links, later edits from new and old valid baselines, and interrupted publication.
Run applicable custody/legacy regressions. Declare full selected supporting-Python source denominator/exclusions before coverage; require >=95% executed-line coverage and required-case pass rate, every mandatory case passing. Supporting Python coverage is not Rust framework qualification. Missing coverage remains NOT_RUN/BLOCKED.

Dev independent stage:
Publish fresh custody/readback then separately invoke skill-validator against new package/request. Rebind the mandatory external evaluation bundle. Require accepted DV-16 intake; rerun DV-01 through DV-18 and RV-01 through RV-06. RV-01 overlaps DV-17 and must not inflate unique-case counts. Use fresh disposable roots, retained attempts, 360-second cold budgets and no automatic retries or model overrides. All mandatory cases must pass; report static/semantic/deterministic/native limitations separately.

## Order and preservation

Sequence: builder maintenance/QA; dev authoring; independent dev assessment. Use qualified development builder directly, without installation. Reverify baseline, use fresh disjoint evidence, and publish authoring record/baseline/manual request only after readback. Preserve original specification, old packet, failed trials and reports. Add a fresh provenance supplement, never edit old handoff readiness.

Allowed changes: selected development skills, validator-owned regression resources and fresh evidence. Operational skills, installation, hooks, CI, startup, plugin work, and application builds remain out of scope. Python supplies evidence only; framework acceptance remains NOT_EVALUATED.

