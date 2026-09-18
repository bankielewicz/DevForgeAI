# Findings ledger

Target digest: `338c70995e72637e0ce84991be110d6a371ab6965faf4009d570156ea0e13cf2`. No corrections applied.

## F-01 — HIGH — implementation defect

Source: `src/agents/skills/skill-builder/scripts/adaptive.py:389-400,435-449`. Clauses: 5.1, 5.3, 9: closed legacy records and exact member custody/request bindings. BA-005, BA-006, BA-014, BAT-08, BAT-10.

Expected: Reject malformed referenced authoring/request records and requests whose target identity or manifest disagrees with the delivered member.

Actual: inspect returned VALID/exit 0 separately for PASS quality statuses, wrong record_kind, wrong request target name/root, boolean changed_paths, and an empty unrelated target_manifest, after all reference hashes and publication references were refreshed.

Minimal reproductions: `commands/ext2-linked-quality/command.json`, `commands/ext2-linked-kind/command.json`, `commands/ext2-linked-request-identity/command.json`, `commands/ext2-linked-request-type/command.json`, `commands/ext2-linked-request-manifest/command.json`. Each directory preserves stdout, stderr and exit; corresponding independently constructed input paths are in the argv. Execute a fresh copy for mutating begin cases.

Impact: The set packet can appear custody-valid while carrying invalid quality claims and a request for another target. No protected authority bypass is claimed.
Confidence: HIGH. Counterevidence: The valid control is accepted; correct partial/subset packets and false-full/omission negatives behaved correctly. This is not a claim that the normal publisher fabricates these fields.

Proposed correction: Validate every legacy field against its unchanged family schema and cross-bind target name/root, manifest rows/digest, run identity and changed paths to actual publication. Preserve legacy version semantics.

## F-02 — MEDIUM — implementation defect, inherited from preserved baseline

Source: `src/agents/skills/skill-builder/scripts/authoring.py:241-247; schemas/authoring-contract.schema.json:113`. Clauses: 5.1 and 9: preserve closed legacy schemas and actual parser behavior. BA-005, BA-011, BAT-08, BAT-09.

Expected: An unlisted top-level authoring-contract-v1 field is rejected before staging.

Actual: begin accepted unlisted_field: true and returned STAGED/exit 0. The shipped schema has additionalProperties: false; begin only checks the required-key subset.

Minimal reproductions: `commands/v2-author-extra-contract-field/command.json`. Each directory preserves stdout, stderr and exit; corresponding independently constructed input paths are in the argv. Execute a fresh copy for mutating begin cases.

Impact: Unsupported contract fields can enter custody evidence instead of failing closed. Valid arbitrary objects inside the legacy requirements array remain supported and must stay supported.
Confidence: HIGH. Counterevidence: Duplicate-key parsing and selected required-field/type checks exist. Historical byte comparison confirms this helper was preserved, so this is not newly introduced by adaptation.

Proposed correction: Enforce the closed top-level schema and declared optional fields without tightening legacy requirement object contents.

## F-03 — HIGH — implementation defect

Source: `src/agents/skills/skill-builder/assets/adaptive-runtime/check_project_binding.py:110-111,142-157`. Clauses: 4.2 exclusions and 6.2 refusal of excluded files in exact runtime capture. BA-002, BA-009, BAT-07, BAT-15.

Expected: Reject recognized private-key/certificate-container filenames before reading/hashing; do not return MATCH for a package containing excluded key material.

Actual: Synthetic id_rsa and identity.pfx package files were inventoried and returned MATCH/BOUND on both Windows and Linux. Only a small suffix list is checked.

Minimal reproductions: `commands/windows-private-key-name/command.json`, `commands/windows-pfx-name/command.json`, `commands/linux-private-key-name/command.json`, `commands/linux-pfx-name/command.json`. Each directory preserves stdout, stderr and exit; corresponding independently constructed input paths are in the argv. Execute a fresh copy for mutating begin cases.

Impact: The helper reads/hashes files the selected contract excludes, and can bind such a package as complete. No real credentials were used or exposed.
Confidence: HIGH. Counterevidence: node_modules and symlink/junction negatives were rejected; .pem and .key suffixes are already rejected. Stdout did not expose a UUID or file contents.

Proposed correction: Define and share a complete conservative private-key exclusion policy (including standard private-key basenames and credential containers), apply it before file reads, and retain explicit omission/rejection reasons.

## F-04 — HIGH — implementation defect, inherited from preserved baseline

Source: `src/agents/skills/skill-builder/scripts/authoring.py:221-238; scripts/custody.py:367-379`. Clauses: 1.1 and 9 preserved legacy identity; known conflicting history blocks. BA-011, BAT-11, BAT-17.

Expected: A selected schema-2 adoption pointer must identify the same skill and run as its adopted origin.

Actual: begin accepted a pointer with target_name wrong-skill and run_id wrong-run while its origin describes sample/old1. It returned STAGED/exit 0. The adopted record and baseline checks passed but pointer identity was never checked.

Minimal reproductions: `commands/ext2-legacy-wrong-pointer/command.json`. Each directory preserves stdout, stderr and exit; corresponding independently constructed input paths are in the argv. Execute a fresh copy for mutating begin cases.

Impact: Conflicting known custody history can establish an edit base. The existing custody.pointer_record check is not called on this source-to-effect branch.
Confidence: HIGH. Counterevidence: Independently constructed valid generated/adopted histories staged successfully; corrupt generated baseline bytes were rejected.

Proposed correction: Validate the entire selected pointer and bind its run/name/origin/baseline to the adopted record before beginning an edit; preserve old bytes and fail conflicting history.

## D-01 — LOW — status/contract ambiguity

`authoring.py:409-417` reports PARTIAL when a concurrent actor changes user.txt before the first builder write, even though applied_paths is empty. v2-author-drift-publish retains the external edit and stops. This is not an overwrite defect. Clarify whether PARTIAL means builder-applied effects or any observed live delta, and distinguish the actor in the receipt. This observation is not counted as a confirmed implementation defect.

## E-01 — audit evidence limitations

Initial second-edit/B/C/N fixtures had an invalid run-root layout; their setup errors are not valid defect reproductions. Fresh followup fixtures corrected the harness only. The first coverage wrapper altered Python import semantics; its ModuleNotFoundError observations are instrumentation failures, not builder defects. The fresh coverage driver restores direct-script imports. All attempts remain. Timeout rows are NOT_RUN, including Linux count-limit commands.

Some initial commands retained argv/oracle/raw output but lacked an explicit per-case pre-execution input manifest and complete effect inventory. Fixture source and in-place inputs support reproduction, but this does not meet the entire requested receipt contract for those cases. No retrospective hash is labeled as a pre-execution hash. Cold execution inherited host context, including a memory lookup in cold-create-02; it is an explicit child task, not fully held-out context or implicit-discovery proof.
