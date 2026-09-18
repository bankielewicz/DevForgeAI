# Legacy assessment interface (validator-owned)

These profiles assess legacy validated-build records without changing their meanings. New authoring records use authoring-intake.md. This resource is executed by validator, never by the enhanced builder.

# Evaluator machine contracts

These UTF-8 JSON interfaces produce deterministic observations. They do not authorize framework transitions or mutations. All paths below are forward-slash paths relative to the selected `--candidate-root`; original absolute paths are informational only. All SHA-256 values are lowercase raw-byte hashes. JSON objects reject duplicate keys and non-finite values. Unknown or missing structural fields are errors; well-formed records that disagree with observed bytes fail their case.

## Profiles and output

`scripts/run_evaluation.py` accepts `--profile`. Omission selects `legacy-import-v1`; enhanced workflows explicitly select their profile. `evals/profiles.json` is the bound profile registry. Each suite must contain exactly the profile's grader set, with one or more unique case IDs per grader. Every JSONL case retains `{case_id,grader_id,params,expected}`, where expected is `PASS` or `FAIL`. All results use evidence schema `2`, including `profile` and `profile_version`. Exit 0 means all expected observations matched, 1 means a mismatch, and 2 means a configuration/execution error. None means acceptance.

## Build traceability

Params: `{"evidence":"evidence","destination":"destination"}`. Both are disjoint directories. The grader reads `build-contract.json` and `build-provenance.json` in evidence and reads referenced snapshots inside candidate-root. A source path and its baseline may be outside these two directories but must remain inside candidate-root.

Contract schema `1` contains `mode` (`import` or `spec_build`), `target_name`, `inputs`, `authorization`, `purpose`, `activation`, `requirements`, `artifacts`, `workers`, and `dependencies`.

- Input: `{id,path,resolved_path,role,bytes,sha256}`. `path` locates the bounded evaluation copy; `resolved_path` records the original resolved input. Both are required. `bytes` is a nonnegative integer.
- Authorization: `{instruction,inputs:[{id,sha256}]}`. Input identities and hashes must exactly cover contract inputs.
- Activation: `{positive:[string],excluded:[string]}`. Positive examples are nonempty.
- Requirement: `{id,origin,text,source_refs,artifact_paths,verification,rationale?}`. `origin` is `source` or `derived`; source requirements require references; derived requirements require nonempty rationale. Each reference is `{input_id,start_byte,end_byte,sha256}` with a zero-based end-exclusive byte interval. Verification is a nonempty list of `{method,expected}` strings. Every requirement maps to at least one artifact.
- Artifact: `{path,role,requirement_ids,purpose}`. Paths and requirement IDs are unique; the two-way requirement/artifact mappings must agree.
- Workers and dependencies are arrays of objects holding the domain contracts described in the specification-build reference. The byte grader observes their recording; a forward trial assesses their meaning.

Provenance schema `1` contains:

```text
run_id, mode, target_name, builder_manifest_sha256, contract_sha256,
inputs:[{id,sha256}], dependencies:[],
outputs:[{path,sha256,ownership,baseline_path,baseline_sha256}],
mappings:[{requirement_id,artifact_paths,evidence_ids}],
evidence:[{id,path,sha256}], prior_build, result
```

`result` is `COMPLETE` or `INCOMPLETE`. `ownership` is `generated` or `retained_user`. Generated rows require a real baseline path and its digest. Retained user rows require null baseline fields. Outputs exactly cover the observed destination. The baseline stores generated candidate bytes; it may differ from delivered user-edited bytes. A prior build is null for a first build, otherwise `{path,sha256}` referencing the preceding successful provenance. Dependency records match the contract's records; the grader does not invent verification results.

Mappings exactly cover requirement IDs and their declared artifact paths, and each mapping cites at least one evidence ID. A cited evidence file is a JSON object with `schema_version:"1"`, `run_id`, `target_name`, and `outputs:[{path,sha256}]`, plus actual command/observation fields. Those identity fields bind preceding structural/script observations to the run and measured artifacts. All mapped artifact paths must be covered by the mapping's cited evidence. Output digests in cited evidence must match current delivered output. The final evaluator JSONL is written outside candidate-root and is linked from the final report; do not cite that not-yet-written file from the input provenance. These checks establish byte accounting, not completeness or semantic correctness of model interpretation.

## Revision consistency

Params: `{"path":"evidence/revision-plan.json"}`. The plan has schema `1` and fields:

```text
run_id, status, baseline, current, candidate, after,
required_paths, owned_paths, rows, applied_paths,
baseline_advanced, readback_passed, evaluation_passed,
prior_build, baseline_before, baseline_after
```

`baseline`, `current`, `candidate`, and `after` identify four distinct, nonoverlapping snapshot directories. Baseline B and candidate N contain generated files; current C and after contain the entire destination including unrelated user files. `owned_paths` is the previous generated ownership set; it must equal B's file set. The prior build reference is `{path,sha256}` to a JSON object declaring `result:"COMPLETE"` and `baseline:[{path,sha256}]` equal to B. This projection contains `provenance:{path,sha256}` referencing the preceding successful provenance. That JSON's `result` is `COMPLETE`, its `run_id` matches the projection, and its generated `outputs` baseline digests exactly cover B. A projection never replaces the full provenance.

The preceding provenance must contain the full schema-1 fields and exact input/output/mapping/evidence row shapes defined above, valid digests and target identity, unique IDs, and coherent mapping references to its generated outputs and evidence IDs. Generated baseline digests are compared with the actual B snapshot; delivered digests may differ when an earlier build retained user edits. Its historical builder digest need not equal the current builder's digest. The current projection's locator and digest bind the captured provenance bytes. Internal paths in those unchanged historical bytes still refer to the preceding snapshot: schema 1 has no historical snapshot-root locator or explicit contract path, so the grader checks their syntax without rebasing them, discovering a contract by filename, or following older history. It does not thereby verify the historical contract or cited observation contents. The revision plan/projection also has no target-name comparison field; target syntax is checked, while build traceability compares a supplied prior provenance with the current contract target. These are finite development observations, not independent verification of protected history.

`baseline_before` and `baseline_after` are `{path,sha256}` references to captured active-baseline pointer JSON files. The grader compares their actual bytes. An advanced pointer must identify this run through `run_id` and contain `baseline:[{path,sha256}]` matching N. The previous pointer and prior-build projection identify the preceding successful run with the same `run_id` and baseline entries matching B.

Each row is `{path,ownership,b_sha256,c_sha256,n_sha256,action,reason}`. Hashes use null for absence. Rows exactly cover the union of all B/C/N paths. Ownership is `generated` for prior owned or newly proposed paths and `retained_user` for unrelated paths. Required paths must exist in N. Actions are `USE_NEW`, `KEEP_CURRENT`, or `CONFLICT`. The grader recomputes ordered B/C/N rules, including unowned occupied paths and missing required output; reason is descriptive evidence, not the decision input.

`status` is `CONFLICT`, `PLANNED`, `APPLIED`, or `PARTIAL`. A conflict or a planned preview requires no destination delta and no baseline advancement. APPLIED requires the after snapshot to equal the complete computed result and requires readback/evaluation success. PARTIAL allows only proposed mutations and records the exact changed path set; it does not advance the baseline or claim successful readback. `applied_paths` must equal the actual C/after delta for every status. Baseline advancement is permitted only for APPLIED with successful readback and evaluation. APPLIED with no advancement is valid intermediate evidence. A later published observation must supply the advanced pointer. Recheck event ordering itself requires command evidence/forward testing; static snapshots cannot prove wall-clock ordering.

For a retry following partial application, add `retry_of:{path,sha256}` to the new plan. It references the retained prior `PARTIAL` revision plan, which must have `baseline_advanced:false` and the same `prior_build.sha256`. The new B still comes from that successful build, while C is captured from the actual destination after the partial attempt.

## Routing outcomes

### Adoption extensions

[adoption.md](adoption.md) defines the additional record, pointer, handoff and schema-2 lineage contracts; [adoption-evidence.schema.json](../evals/adoption-evidence.schema.json) supplies their structural schemas. Existing contract/provenance/revision schema-1 meanings remain unchanged. `build_traceability_v2` retains `{evidence,destination}` params and reads the schema-2 plan alongside provenance. It checks published-before origin, adoption metadata, contract justification of generated ownership and delivered/after equality. `revision_consistency_v2` retains `{path}` params and shares the three-way/delta checks with schema 1, adding typed prior/after origins. References stay inside the selected bounded candidate root with historical relative layouts preserved; absolute origin metadata is never followed.

`adoption_consistency` takes `{evidence,destination}` and compares complete snapshot/after byte sets, manifest partitions, authorization digests and preceding readback. `routing_outcomes_v2` uses the legacy routing interface below with only `adoption` added to its allowed route values; validation-only requests use the existing `unrelated` class. The legacy grader rejects the new value. Source chronology, real user authorization, publication and application ordering still require task/command receipts; static byte agreement does not prove them.

Params: `{"expected":"expected.jsonl","observed":"observed.jsonl"}`. Each file has 1–1000 JSONL records, at most 1 MiB. A record has `case_id`, `route`, and optional `request`. IDs must be unique and equal across both files. Route values are `import`, `spec_build`, `revision`, `explanation`, `specification_authoring`, `installation`, and `unrelated`. A route difference fails; absent, duplicate, or unknown IDs/routes are errors. Observed results come from an independent routing task. These classifications do not establish native implicit activation.
