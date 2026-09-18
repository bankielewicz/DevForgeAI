# Independent implementation probes

Executed on native Windows using Python, against the development helpers only. No native model task was launched. `probe_runner.py` is the reproducible fixture generator; it intentionally requires fresh directories and will not overwrite previous attempts. `cases.json` predates interface execution. Detailed observations are in `probe-results.json`.

## Confirmed defects

1. **Receipt validation accepts malformed and incomplete evidence.** After a valid delivered-output attempt, replacing `streams` with `[]`, setting `timeout_seconds` to 999 instead of the sealed 5, setting `schema_version` to `invalid`, setting `exit_code` to Boolean false, or setting elapsed time to -999 each still produces PASS from `check_attempt`. These changes were tested separately. Evidence: `correct-output/tamper-*.json`, baseline restored in `correct-output/attempt/result.json`, result rows `IND-RECEIPT-*`. This violates evidence completeness/type and selected-limit binding requirements; ordinary editable evidence still needs internal consistency checks.

2. **Summary can drop a sealed prerequisite.** The sealed `dependent` plan declares `correct-output` as a prerequisite and binds its attempt. Supplying summary inventory with only `dependent` and an empty dependency list returns PASS with required_total=1. Evidence: `dependent/plan.json`, `dependent/omitted-dependency-summary.json`, row `IND-SUMMARY-OMITTED-DEPENDENCY`. Summary must compare caller dependency lists with sealed plans and require selected prerequisites to remain in inventory.

3. **Input-root separation is unenforced.** A plan with its protected input script inside `permitted_write_root` seals successfully. The selected SVE-04 explicitly places inputs outside that root. Evidence: `inside-input/plan.json`, `inside-input/attempt/seal.json`, row `IND-INPUT-BOUNDARY`. Either enforce the selected requirement or explicitly justify a spec correction; this cannot be silently marked implemented.

4. **Unlisted side effects are unobserved.** A synthetic command creates `unexpected.txt` inside its disposable project. The result records PASS with empty artifact/check arrays and no before/after observation. Evidence: `unexpected-side-effect/project/unexpected.txt`, `unexpected-side-effect/attempt/result.json`, row `IND-SIDE-EFFECT-OBSERVATION`. The approved plan requires before/after side-effect observations, distinct from a claim of OS-wide isolation. A bounded disposable-root inventory would establish what changed without elevating observations to policy authority.

## Successful observations

- Shared metadata parsing accepted valid optional fields and rejected numeric metadata values, allowed-tools sequences, duplicate keys, and mixed non-string keys.
- Zero exit plus completion prose did not qualify an absent required file.
- JSON output with the wrong total failed; correct content passed.
- A real command spawned a sleeping descendant, printed a marker, and exceeded its explicit 1.5-second limit. The result retained timeout status and stdout; Windows Job cleanup reported VERIFIED; an independent process-handle check found the recorded descendant no longer alive.

## Limits

These are focused independent helper probes, not complete validation of the skill or framework acceptance. Frozen cases not represented in the results remain unperformed. No retry erased an earlier result. The scripts and tampered receipt copies are retained for separately authorized corrections/retests.
