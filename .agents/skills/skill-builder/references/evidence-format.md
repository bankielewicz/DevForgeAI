# Authoring records and write custody

Use fresh project docs/plan/skill-authorings/name/run-id directories. Never overwrite older attempts. JSON is UTF-8 with unique keys and finite numbers. A file reference is `{path, sha256}` where path is an actual absolute local locator and sha256 hashes raw bytes. Original paths remain identity data, not portable runtime constants. Manifest rows are sorted `{path, bytes, sha256}`. The package digest is SHA-256 of compact UTF-8 JSON of these rows (unescaped Unicode, key order path/bytes/sha256); it excludes root and timestamps. Relative package paths use forward slashes, with no traversal or links.

## Contract before candidate generation

Required authoring-contract-v1 fields:

```json
{
  "schema_version": "authoring-contract-v1",
  "run_id": "unique-run",
  "project_root": "<resolved selected project>",
  "target_root": "<resolved final development skill directory>",
  "target_name": "selected-name",
  "operation": "create",
  "authorization": "<actual current instruction and authorized effects>",
  "history_review": "no_known_history",
  "change_paths": ["SKILL.md"],
  "requirements": [{"origin": "user", "outcome": "<task contract>", "artifacts": ["SKILL.md"]}],
  "capabilities": [],
  "expected_outputs": [],
  "side_effects": [],
  "inputs": [],
  "known_issues": []
}
```

Operation is create, edit, import, spec_build or adopt. For existing known history set history_review to a description of the verified review and provide prior as a digest-bound reference. Legacy records additionally need legacy_root identifying their existing bounded snapshot root (relative record paths retain their original base). An authored prior names authoring-baseline.json; do not use a PARTIAL or unpublished run. Known corrupt history blocks rather than selecting observed editing. Inputs include supplied specifications, conversational task capture, imported source bytes and selected external reports; preserve the input files before execution. Side effects describe the authored skill, never permission invented by a handoff.

## Output families

Enhanced create/edit/import/specification authoring includes the external [workflow design](workflow-design.md) reference in `inputs` and supplies the same file through `begin --design`. Its version is `authoring-design-v1`; do not add design fields to the closed authoring contract or validation-request-v1. The capture record has exactly `schema_version: authoring-design-capture-v1`, `run_id`, `target_name`, `source_ref` and `snapshot_ref`. Both references use `{path, sha256}`. Snapshot points to the existing `inputs/<index>` copy, and internal origin metadata adds `design_capture_ref`. Original, snapshot, capture and bindings are read back before STAGED and rechecked at publication. The design input and referenced inputs share the bounded capture rules; a design-enabled input capture counts the contract within the 2,000-file/32-MiB ceiling.

The completed design remains in the selected disjoint input area. A new design requires a fresh linked run after staging. Capture failure prevents publication; never remove design evidence to downgrade a run. Calls without --design and existing legacy stages keep their original contract. Custody-only adoption/proposal/update-review needs no mandatory design. CLI exit codes remain 0 for success, 1 for recorded BLOCKED/PARTIAL, and 2 for rejected input or handled command errors. Retained errors describe actual effects, not rollback.

New internal origins record the boolean `design_capture_requested` to distinguish explicit --design selection from a legacy call that happens to reference a design-shaped file as ordinary input. Design-enabled origins also require `design_capture_ref`; a false mode cannot coexist with a capture record/binding. This internal marker changes neither supplied contract bytes nor validator packet fields.

Before returning STAGED, begin writes and reads back `stage-integrity.json` with exactly `schema_version: authoring-stage-integrity-v1`, `run_id`, `target_name`, `origin_ref: {path, sha256}` and boolean `design_capture_requested`. The reference binds the original origin.json bytes, including mode and design binding. Publication validates this receipt before legacy/design dispatch, before each changed path, after delivery and at baseline/handoff publication boundaries. Missing or inconsistent evidence blocks dependent writes; changes detected after delivery retain actual deltas as PARTIAL. A receipt write/readback failure retains capture-failure.json and cannot yield STAGED.

Canonical historical stages without the mode marker or design evidence retain legacy handling. Pre-revision stages containing the mode marker but no receipt require a fresh linked run; never manufacture a receipt after staging. New no-design runs also carry a receipt and may reference design-shaped JSON as ordinary input. Published historical baselines keep their original meaning. These are editable consistency records, not protected authority: coordinated rewriting of all evidence is outside their protection.

New captures preserve the supplied contract byte-for-byte as supplied-contract.json and bind its original source in contract-source.json. contract.json is the effective contract: project_root and target_root use the same safe host-native absolute spelling emitted in the record, baseline and request. contract-paths.json retains each field's supplied and resolved values. origin.json binds the effective contract, supplied snapshot and path-resolution bytes independently. No other supplied contract values are changed. Host resolution does not rename path components, case-fold identity, follow links or translate checkouts.

Before publication, recheck the source, both contract representations and their resolution mapping. A previously staged contract with noncanonical project/target spelling cannot be published by this writer: retain it and start a fresh linked run. Existing canonical stages and published historical baselines remain readable; never rewrite their contracts or reinterpret their quality states. This producer-side consistency safeguard does not invoke validator or relax its exact identity and digest comparisons.

authoring-v1 / record_kind authoring records project, target, name, operation, run, authorization, inputs, prior_origin (observed, adopted, legacy_generated or authored), managed_paths, retained_user_paths, before/candidate/delivered manifests, applied_paths and comparison rows. States are AUTHORED, PARTIAL or BLOCKED. validation_status and testing_status default to NOT_PERFORMED. Unresolved issues remain explicit.

authoring-baseline-v1 / record_kind authoring_baseline binds the exact AUTHORED record and separate baseline manifest/root. Baseline bytes represent the managed candidate, not retained user edits. Publication-readback.json confirms actual publication; publication-failure.json or absent readback prevents use as the next baseline. Untested AUTHORED runs can be revised. Old results remain separate, exact-byte history; never rewrite the original record to attach a later validation.

`authoring.py read --record <file>` distinguishes the new family from legacy schema-1 and schema-2. The retained build_evidence.py and custody.py are legacy input and B/C/N readers, not evaluators; no graders import is required. Legacy readers retain old field meanings, including historical evaluated completion. New runs use authoring-v1 rather than emitting a fake COMPLETE build record.

Snapshots, candidate, baseline, command receipts and reports remain external to the authored package. Publication failure retains all artifacts. Do not claim protected admission, package-wide atomicity, automatic rollback or OS-enforced isolation.
