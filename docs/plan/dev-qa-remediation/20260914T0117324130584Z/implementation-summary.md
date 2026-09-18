# Implemented Dev QA remediation

Approved plan: [dev-qa-remediation-plan.md](../../dev-qa-remediation-plan.md).

## Changes

- Development skill-builder now retains supplied-contract.json byte-for-byte, writes a safe host-resolved effective contract.json, records supplied/resolved project and target values in contract-paths.json, and pins all three representations before publication. Older noncanonical staged contracts require a fresh run. Validator production intake is unchanged.
- Development dev now preserves the complete literal evidence destination, binds outputs before writes, rechecks original selection and actual outputs before VERIFIED/COMPLETE, and carries selection identity through resume checkpoints.
- Validator-owned regression tests cover alternate Windows path spellings, original/effective contract integrity, publication failures, concurrent writers, legacy provenance, retained baselines and source limits. The evaluation manifest was updated only for the changed and added test artifacts.

## Retained results

- red-001: native path works; forward/mixed spellings fail unchanged intake with authoring contract/request mismatch. This is the expected behavioral red.
- green-001: new path cases pass; an existing malformed-array test asserts obsolete error text and fails.
- baseline-malformed-001: same assertion failure reproduced against untouched before/skill-builder. Assertion updated to the current field-qualified schema error, retaining rejection and strengthening no-write observation.
- coverage-001: 36/36 authoring cases pass; 354/453 executed lines, below the floor.
- builder-qa/attempt-001: 67/67 pass; 427/453 lines, below the floor.
- builder-qa/attempt-002: 71/71 pass; 435/453 executed lines = 96.02649006622516%, no exclusions. Branch arcs 225/244 = 92.21311475409836%.
- regression-001: full selected validator regression suite 292/292 PASS, no failures/errors/skips, 72.423 seconds.
- builder-structure-001: installed Skill Creator structural checker passed; this is limited format evidence.
- builder-qa/evaluation-bundle: a separately owned Python JSONL evidence runner, deterministic reducer, fixtures, expected outputs, schema, runtime description, and manifest bind the actual helper results. Final manifest-v2.json SHA-256 is 1fe87bc375d32a8c3e02080f1790d63f73bcb705db3b175ec02d70604f47a0dd. Reduction-002 exited 0 with three PASS results; eight reducer tests passed. Earlier reducer failures remain retained. This reduces retained execution evidence and does not qualify native skill behavior.
- dev publication: AUTHORED/PUBLISHED, eight applied paths, eleven delivered files read back. Package digest 8ad8c94b862a2e68a1d6e3064978bb654ded484da2e8adf0317f23dd7583924c.

The initial evidence capture had a locator setup error before creating snapshots or changing production files; capture-attempt-001.md retains it. It is not behavioral red.

## Custody and boundaries

Authoring run: ../../skill-authorings/dev/20260914T0117324130584Z.
Manual request SHA-256: 034887a39a8b5f12e0ca3bb27e2f87cba48b4f0f74335071ef2baf6b77d525af.
Verified prior authored baseline retained; no adoption, original-packet repair, or historical QA rewriting.
Original specification remains b9783ca08d86fa734c89ce76623ff6c45b2640781d3955f16ea54ea659c7b265.

Implementation readback confirms only three development builder paths, three validator evaluation paths, and eight dev paths changed. Operational validator and dev still match pre-change development bytes. Operational builder contains additional legacy evaluator resources absent from development source; all shared files match the pre-change source. That installation difference was preserved, not synchronized.

No installation, hooks, CI, startup, plugin or application build performed. Framework acceptance remains NOT_EVALUATED.
The separate fresh dev assessment has its own run and final report; these implementation observations do not predeclare its verdict.
