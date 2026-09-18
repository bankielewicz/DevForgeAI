# Independent helper regressions

Final retained attempt `attempt-003` passed all 34 unittest methods, with 62 helper CLI subprocesses and no skipped tests. Runtime was 9.530 seconds on Windows with Python 3.10.11. The symlink omission fixture executed successfully.

The independently authored tests exercise exact raw bytes and Unicode paths, canonical package digest accounting, changed/added/removed source files, snapshot boundaries, existing/overlapping outputs, file and byte ceilings, metadata parsing and types, ordinary Markdown links and anchors, duplicate/non-finite JSON, evidence references, finding identity/deduplication, status reduction, incomplete coverage, origin history limits, and authorization bound to the actual proposal and target digests.

Run command from project root:

```powershell
python -B -X utf8 docs/plan/skill-builds/skill-validator/20260912T155029Z/helper-tests/run-regressions.py attempt-003
```

That directory already exists and must not be reused. A later authorized rerun must select a new attempt name. The runner freezes the exact helper and test files before executing them. Every CLI execution preserves its disposable input snapshot, input manifest, command, expected exit, stdout, stderr, and actual exit under the attempt's `cases/` directory. `command.json` records the actual interpreter and environment, with TEMP/TMP/TMPDIR confined to the attempt.

`attempt-001` retained a failed positive control: the test's purported READY record lacked the actual source manifest and used a placeholder target digest. The helper correctly rejected it. The test was corrected to construct a digest from retained source bytes independently. `attempt-002` then passed all 33 tests. The implementation author subsequently fixed strict JSON numeric overflow; the independent test author added five non-finite inputs and executed all 34 tests in `attempt-003`.

The current helper was read back after the final run and matched the frozen SHA-256 `ddc7ed1c07ccbadc652dd58749a35be179a234544ad21c9a02ee7a143c761d5f`. Test SHA-256: `b61e8592f82ca70cc4f9ac787db8dd9c2ab2bc6bb5a69cb0c3fc75d70e8ca3ef`.

These are deterministic helper regressions. They do not establish semantic fidelity, native invocation, genuine baseline history, successful operational adoption, Rust qualification, or complete build verification. The synthetic READY control observes mechanical reference/digest consistency; its baseline text is explicitly not a real builder baseline.
