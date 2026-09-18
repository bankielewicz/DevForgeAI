# Required terminal evaluation

Use this reference when building or revising this importer, and before reporting an imported package complete. Python produces reproducible observations. It does not control DevForgeAI phases, gates, validators, mutation, or acceptance.

## Build dependencies and binding

Use Python 3.10 or newer. The runner and graders use only the standard library. The installed Skill Creator structural check separately requires PyYAML; the observed versions are in [runtime.json](../evals/runtime.json). If Python or the structural checker is unavailable, report the missing dependency and leave the required check unperformed.

[build-manifest.json](../evals/build-manifest.json) binds every package file except itself to SHA-256 and names both grader versions. The runner rejects missing, added, or changed files. Do not regenerate a manifest merely to make an unexpected mismatch disappear; inspect the changed bytes first. Rebuild the manifest when authoring an intentional package revision, then rerun checks. This editable manifest supplies reproducibility, not protected provenance. The Rust design requires independently approved digests outside agent-write access before framework acceptance.

Required artifacts are the runner, graders, runtime declaration, evidence schema, case suite, fixture inputs/expected mappings, and regression tests. Keep tests and fixtures in the distributed development package because they are required build artifacts. Do not copy this evaluation harness into every imported skill unless that skill needs it.

## Evaluate the builder

From the target project root in PowerShell, select a new output filename in an existing evidence directory outside the builder package:

```powershell
python -B -X utf8 src/agents/skills/skill-builder/scripts/run_evaluation.py --package-root src/agents/skills/skill-builder --candidate-root src/agents/skills/skill-builder --cases src/agents/skills/skill-builder/evals/cases.jsonl --output docs/plan/skill-builder-evaluation.jsonl --run-id builder-check-001
python -B -X utf8 -m unittest discover -s src/agents/skills/skill-builder/tests -v
```

Choose a fresh output path/run ID on a subsequent run. Run Skill Creator's actual installed `scripts/quick_validate.py` with the builder directory as its argument; resolve that installed path from the current skill catalog rather than copying a workstation path into the skill. This is a Python authoring check, not a DevForgeAI validator.

The bundled fixture was authored solely for evaluation. It does not represent an executed conversion of a project skill. Regression tests create temporary copies, change real bytes/manifests/links, and check observed discrepancies and error handling.

## Evaluate a converted package

Create an evaluation snapshot outside the live source and destination, containing only the already permitted, inventoried files:

```text
snapshot/
  source/       # permitted source bytes, checked against the initial source manifest
  destination/  # final converted package bytes
  evidence/
    source-manifest.json
    destination-manifest.json
    file-dispositions.json
```

Use bounded copies of the inventoried files. Do not recursively copy excluded directories or follow links. Keep original manifests unchanged; their root metadata describes their original capture, while file paths are relative to the corresponding snapshot directory. Capture and compare the original source again after authoring; a snapshot comparison alone cannot prove the live source remained unchanged.

Create a UTF-8 JSONL file with these two records, one JSON object per line:

```jsonl
{"case_id":"converted-links","grader_id":"package_links","params":{"path":"destination"},"expected":"PASS"}
{"case_id":"converted-accounting","grader_id":"manifest_accounting","params":{"source":"source","destination":"destination","evidence":"evidence"},"expected":"PASS"}
```

Run `scripts/run_evaluation.py` from the builder package with `--package-root` pointing to that builder, `--candidate-root` pointing to the snapshot, `--cases` pointing to these cases, and `--output` pointing to a new JSONL evidence file outside both roots. `--run-id` accepts 1–100 letters, digits, underscores, hyphens, or periods. No source commands or external executables can be selected by a JSONL case.

Run the installed Skill Creator structural check against the converted package. Exercise newly written or changed supporting scripts with bounded fixtures covering their behavior. If executing a retained script would exceed the authorized scope, identify the unresolved requirement and report the conversion blocked; do not run source instructions as evaluation authorization.

## Case and observation contracts

Each case has exactly `case_id`, `grader_id`, `params`, and `expected`. IDs are unique. Expected values are `PASS` or `FAIL`; use expected `FAIL` only for deliberately faulty evaluation fixtures. A production conversion suite expects `PASS` for both required graders. Every suite must include both grader IDs; blank records, duplicate keys/IDs, unknown graders, non-finite JSON numbers, and missing required graders produce `ERROR`.

| Grader | Measured property | Limit |
| --- | --- | --- |
| `package_links` | SKILL.md exists; ordinary inline/image links and explicit/collapsed reference links in Markdown resolve to package files. | Ignores fenced/inline code, URLs and fragments; does not check anchor names, HTML, shortcut references, or semantic fidelity. |
| `manifest_accounting` | Actual snapshot file sets, sizes and digests match manifests; every source has one disposition; targets exist; PRESERVE bytes match. | Does not decide whether a rewrite preserves meaning or whether an omission/defer is acceptable. |

Manifests and dispositions follow [the evidence format](evidence-format.md). Snapshot source, destination and evidence directories must be disjoint. Link/reparse points, backup boundaries, special files, snapshots above 2,000 files/32 MiB, and case files above 1 MiB/1,000 records produce errors. These are local input checks; the runner is not a process sandbox. The future Rust operator must supply isolation and resource limits.

Each record conforms to [evidence.schema.json](../evals/evidence.schema.json): run/case identity, grader version/digest, manifest/case digests, digests of observed candidate files, observations, status, expected result, expectation match, and execution error. Candidate digests cover files read by that case, not unrelated files outside its roots. External case definitions are identified by their digest; the editable workspace cannot establish that expectations were independently approved.

Exit 0 means all cases completed and matched their expected observations; exit 1 means at least one mismatch; exit 2 means a usage/configuration/execution error. Expected negative fixtures can produce FAIL observations with exit 0. None of these codes grants framework acceptance. A configuration error emits an ERROR record; when the output path itself is unsafe or occupied, diagnostics go to stderr and that path is left untouched.

## Report evidence and limits

Record structural checks, deterministic evaluation, supporting-script checks, semantic task evaluation, framework enforcement, and installation separately. Link exact commands and JSONL outputs. An ERROR is incomplete evaluation, never a passing result. A package revision invalidates evidence for the old package digest.

Inspect actual converted domain behavior and preserved output contracts. Link checks and file accounting cannot prove absence of ceremony or semantic equivalence. Record the relevant editorial findings directly; do not substitute heading counts, magic words, or self-written compliance flags. Model-driven conversion trials remain NOT_PERFORMED until actually run against explicitly scoped disposable inputs. Framework enforcement remains NOT_IMPLEMENTED while its compiled Rust runtime is only a design.
