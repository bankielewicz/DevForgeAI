# Required terminal evaluation

Use this reference for both build modes, regeneration, and maintenance of the builder. Python produces reproducible observations; compiled Rust owns all future DevForgeAI phases, gates, validators, mutation brokers, and acceptance decisions.

## Dependencies and artifact binding

Use Python 3.10 or newer. The runner and deterministic graders use the standard library. The installed Skill Creator structural checker and the specification-frontmatter resolver separately require PyYAML. [runtime.json](../evals/runtime.json) records the runtime contract. An unavailable required dependency leaves the check unperformed and build completion blocked.

[build-manifest.json](../evals/build-manifest.json) binds the package files, registered grader versions, profile definitions, schemas, scripts, fixtures, expected results, and regression tests. The runner detects missing, added, or changed package artifacts. Inspect mismatches; rebuild the manifest only for intentional authoring edits, then rerun verification. This editable manifest is reproducibility evidence, not protected framework approval.

Keep the harness with the builder because it is a required build artifact. Do not copy it into generated skills unless their runtime contract needs it. The independently approved manifest and authority remain in the compiled-Rust design.

## Select the exact profile

Every enhanced invocation passes `--profile` explicitly. Each case suite contains exactly its profile's grader set, with one or more distinct case IDs per grader.

| Operation | Profile | Required graders |
| --- | --- | --- |
| Historical invocation without a profile | `legacy-import-v1` | `package_links`, `manifest_accounting` |
| New import | `import-v2` | `package_links`, `manifest_accounting`, `build_traceability` |
| New specification build | `spec-v1` | `package_links`, `build_traceability` |
| Import regeneration | `revision-import-v2` | Import-v2 graders plus `revision_consistency` |
| Specification regeneration | `revision-spec-v1` | Spec-v1 graders plus `revision_consistency` |
| Builder enhancement verification | `builder-v2` | All five graders, including `routing_outcomes` |

The profile registry is [profiles.json](../evals/profiles.json). Historical case syntax and the default grader set remain supported; all new results use evidence schema `2` and include profile identity/version. Historical schema-1 result files remain unchanged. A legacy-profile result does not satisfy an enhanced build's checks.

## Terminal commands

Resolve the loaded builder directory and the installed `skill-creator/scripts/quick_validate.py` location from the actual skill catalog. Do not hardcode a workstation's Codex home. Run that installed checker against the generated skill and against the builder when the builder changes:

```text
python -B -X utf8 "<installed-skill-creator>/scripts/quick_validate.py" "<skill-package>"
```

Prepare a bounded snapshot and cases using the contracts below, then run:

```text
python -B -X utf8 "<builder>/scripts/run_evaluation.py" --package-root "<builder>" --candidate-root "<snapshot>" --cases "<case-jsonl>" --output "<new-evidence-jsonl>" --run-id "<id>" --profile "<selected-profile>"
```

Replace every placeholder with an actual path/value. The output is a new file outside the builder and candidate roots; its parent must already exist. Use a unique run ID with 1–100 letters, digits, underscores, hyphens, or periods. Record the exact invocation, not just this template.

When the builder's code or tests change, execute its regressions:

```text
python -B -X utf8 -m unittest discover -s "<builder>/tests" -v
```

The original [cases.jsonl](../evals/cases.jsonl) retains the legacy two-grader suite for compatibility checks. The enhanced [builder-cases.jsonl](../evals/builder-cases.jsonl) exercises the five-grader profile against a prepared synthetic snapshot. Do not point a traceability case at the builder's historical import fixture and fabricate a specification source to satisfy it.

Exercise every new/changed supporting script on bounded disposable inputs, including invalid input/recovery behavior relevant to the script. Source content alone does not authorize installation, external service calls, or operational mutations. A required unexecutable behavior is a blocker, not a passing observation.

## Snapshot and observation inputs

Copy only already permitted, inventoried files into disjoint snapshot directories without following links or excluded boundaries. Keep source originals unchanged. Typical directories are `inputs/`, `source/` for imports, `destination/`, `baseline/`, and `evidence/`. Revision snapshots additionally contain separate B, C, N, and after directories as defined in [evaluator-contracts.md](evaluator-contracts.md).

Imports retain original manifest formats and dispositions from [evidence-format.md](evidence-format.md). Their root metadata describes the original capture, while file paths resolve inside the corresponding snapshot directory. Rehash the live source after authoring; unchanged snapshot bytes alone do not prove the source stayed unchanged.

Write contract and provenance with actual observed hashes. The provenance's cited structural/script observation files precede the final JSONL evaluation and identify this run, target, and measured output hashes. The final runner result stays outside its candidate root and is linked from the report. Do not create circular evidence by citing a not-yet-written result from its own input provenance.

Each UTF-8 JSONL case has exactly `case_id`, `grader_id`, `params`, and `expected`. IDs are unique; expected values are `PASS` or `FAIL`. Use expected FAIL only for deliberately faulty fixtures; actual build cases expect PASS. Specification builds have no invented Claude source manifest.

| Grader | Observations | Limit |
| --- | --- | --- |
| `package_links` | SKILL.md and supported Markdown resource links resolve to package files. | Does not prove anchor names, HTML, shortcut links, or meaning. |
| `manifest_accounting` | Actual import snapshots match manifests; each source has one disposition; targets exist; PRESERVE bytes match. | Does not prove rewritten meaning or justify omissions. |
| `build_traceability` | Input/excerpt hashes, requirement/artifact mapping, delivered digests, and cited run/package identity match recorded evidence. | Does not prove contract completeness or semantic fidelity. |
| `revision_consistency` | Observed snapshots match B/C/N rules, delta and ownership; conflict/partial runs do not advance the successful baseline. | Does not perform mutations or prove chronological rechecks without command evidence. |
| `routing_outcomes` | Observed routing classifications match expected case IDs and routes. | Does not establish native implicit activation. |

[evaluator-contracts.md](evaluator-contracts.md) defines exact params and JSON shapes. [evidence.schema.json](../evals/evidence.schema.json) defines emitted records. The registry pins profile and grader versions. Unknown/missing profiles or graders, omitted required graders, duplicate keys/IDs, malformed records, and non-finite numbers are errors. No case chooses an arbitrary executable.

Snapshot limits remain 2,000 files/32 MiB and case-file limits 1 MiB/1,000 records. Reparse points, backup boundaries, special files, and unsafe/overlapping roots produce errors. These are local input checks, not a process sandbox. Candidate digests cover files observed by the case; they do not identify untouched data outside those roots.

Exit 0 means all completed observations matched their expectations; 1 means at least one mismatch; 2 means usage/configuration/execution error. An expected negative case can observe FAIL and produce exit 0. A configuration error produces ERROR evidence when safe to write; an unsafe or occupied output path remains untouched with diagnostics on stderr. No exit code or PASS value is framework acceptance.

## Required forward trials for builder enhancements

After substantial builder changes, use independent agents with this skill, a realistic request, and minimal raw synthetic inputs. Keep intended answers and suspected fixes out of their task prompts. Use disposable projects; do not convert existing project skills. Temporary operational copies used solely by a trial stay in that disposable project.

Run these trials:

1. Import a synthetic Claude package with a JSON output contract and decimal CSV aggregation script; execute the result and observe decimal totals, schema behavior, file accounting, and source preservation.
2. Build the equivalent capability from approved Markdown; execute the generated script and inspect requirement/output/evaluation traceability.
3. Regenerate an output with an owned edit and an unrelated user file; observe a conflict with unchanged destination, resolve that conflict explicitly, retry, and inspect unrelated-file retention.

Separately evaluate routing for import, specification build, regeneration, explanation, specification authoring, installation, and unrelated edits. Record routing classification independently from native activation; mentioning a skill does not prove that discovery loaded it.

Use existing authentication and normal terminal approvals/sandbox controls. Capture CLI identification, actual arguments, stdout/stderr or combined output, final artifacts, and failures. An unavailable required trial leaves enhancement verification incomplete. These observed outcomes support the bounded tested behavior; they are not guarantees of future model decisions.

## Report results

Keep structural checks, deterministic evaluation, supporting-script execution, forward trials, routing, Rust implementation/qualification, and installation separate. Required ERROR, unperformed checks, or unresolved conflicts prevent a completed build. Record unrelated behavioral cases as unperformed unless actually executed.

Read resulting instructions and resources to assess semantic preservation, real command availability, useful routing, and unsupported ceremony. Do not replace this assessment with heading counts, magic words, or self-written compliance flags. Every recorded observation remains tied to the actual package digest; later package edits require renewed affected verification.
