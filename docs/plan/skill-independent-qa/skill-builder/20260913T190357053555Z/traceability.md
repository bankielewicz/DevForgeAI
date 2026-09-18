# Requirement and BAT traceability

Target: `7715f8b80a9b089a4349f6bbb3b502a52d55a03bb2eb2ec65f861ea4be77ff3a`. PASS applies only to a named executed subcase. NOT_RUN includes reviewed requirements with incomplete behavioral evidence.

| Requirement | Status | Source locators | Required BATs |
| --- | --- | --- | --- |
| BA-001 | NOT_RUN | SKILL.md:9, references/authoring.md:7, references/validation-handoff.md:3, scripts/authoring.py:419 | BAT-01, BAT-12 |
| BA-002 | NOT_RUN | references/adaptation.md:7, references/adaptation.md:9, references/adaptation.md:11, scripts/adaptive.py:225 | BAT-02, BAT-03 |
| BA-003 | NOT_RUN | references/adaptation.md:15, references/adaptive-contracts.md:23, scripts/adaptive.py:237 | BAT-04, BAT-05 |
| BA-004 | NOT_RUN | SKILL.md:25, references/project-binding.md:3, assets/adaptive-runtime/check_project_binding.py:246 | BAT-06, BAT-07 |
| BA-005 | NOT_RUN | references/adaptive-contracts.md:17, scripts/record_schema.py:15, scripts/adaptive.py:44, scripts/adaptive.py:97, scripts/adaptive.py:129 | BAT-08, BAT-09 |
| BA-006 | NOT_RUN | references/adaptation.md:23, scripts/adaptive.py:321, scripts/adaptive.py:381, scripts/adaptive.py:444 | BAT-10, BAT-11 |
| BA-007 | NOT_RUN | references/adaptive-contracts.md:25, scripts/adaptive.py:152, scripts/adaptive.py:264 | BAT-05, BAT-13 |
| BA-008 | NOT_RUN | references/adaptation.md:15, scripts/adaptive.py:291 | BAT-04, BAT-14 |
| BA-009 | NOT_RUN | references/adaptive-contracts.md:31, references/project-binding.md:5, assets/adaptive-runtime/check_project_binding.py:158 | BAT-06, BAT-07, BAT-15 |
| BA-010 | NOT_RUN | references/adaptation.md:45, scripts/adaptive.py:307 | BAT-13, BAT-16 |
| BA-011 | NOT_RUN | references/regeneration.md:3, scripts/authoring.py:148, scripts/custody.py:159, scripts/build_evidence.py:204 | BAT-09, BAT-11, BAT-17 |
| BA-012 | NOT_RUN | references/adaptation.md:7, references/project-binding.md:13, scripts/authoring.py:459, assets/adaptive-runtime/check_project_binding.py:309 | BAT-03, BAT-15 |
| BA-013 | NOT_RUN | SKILL.md:3, SKILL.md:17, references/adaptation.md:3 | BAT-12, BAT-14 |
| BA-014 | NOT_RUN | SKILL.md:43, references/evidence-format.md:32, scripts/authoring.py:406, scripts/adaptive.py:69 | BAT-01, BAT-10, BAT-17 |

| Parent BAT | Windows (passes/required) | Linux (passes/required) | Overall |
| --- | --- | --- | --- |
| BAT-01 | NOT_RUN (1/4) | NOT_RUN (1/4) | NOT_RUN |
| BAT-02 | NOT_RUN (0/5) | NOT_RUN (0/5) | NOT_RUN |
| BAT-03 | NOT_RUN (0/7) | NOT_RUN (0/7) | NOT_RUN |
| BAT-04 | NOT_RUN (0/4) | NOT_RUN (0/4) | NOT_RUN |
| BAT-05 | PASS (4/4) | PASS (4/4) | PASS |
| BAT-06 | NOT_RUN (0/4) | NOT_RUN (0/4) | NOT_RUN |
| BAT-07 | NOT_RUN (13/14) | NOT_RUN (12/14) | NOT_RUN |
| BAT-08 | NOT_RUN (7/10) | NOT_RUN (7/10) | NOT_RUN |
| BAT-09 | NOT_RUN (3/4) | NOT_RUN (3/4) | NOT_RUN |
| BAT-10 | NOT_RUN (2/6) | NOT_RUN (2/6) | NOT_RUN |
| BAT-11 | NOT_RUN (4/6) | NOT_RUN (4/6) | NOT_RUN |
| BAT-12 | NOT_RUN (5/7) | NOT_RUN (0/7) | NOT_RUN |
| BAT-13 | NOT_RUN (0/5) | NOT_RUN (0/5) | NOT_RUN |
| BAT-14 | NOT_RUN (0/4) | NOT_RUN (0/4) | NOT_RUN |
| BAT-15 | NOT_RUN (3/6) | NOT_RUN (0/6) | NOT_RUN |
| BAT-16 | NOT_RUN (1/3) | NOT_RUN (1/3) | NOT_RUN |
| BAT-17 | NOT_RUN (3/7) | NOT_RUN (3/7) | NOT_RUN |

| Subcase | Windows | Linux | Independent test |
| --- | --- | --- | --- |
| BAT-01-cold-create | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-01-focused-edit | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-01-manual-handoff-byte-binding | PASS | PASS | test_ordinary_create_manual_request |
| BAT-01-no-quality-process | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-02-two-languages | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-02-unknown-manifest | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-02-dependency-exclusion | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-02-junction-exclusion | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-02-no-project-script | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-2000-file-boundary | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-2001-file-limit | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-32MiB-boundary | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-32MiB-plus-one-limit | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-missing-python | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-missing-rust-enforcement | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-03-independent-proposal-retained | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-04-http-retained | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-04-storage-evidence | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-04-no-redundant-persona | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-04-supporting-locators | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-05-missing-disposition | PASS | PASS | test_extra_lineage_missing_row |
| BAT-05-unauthorized-removal | PASS | PASS | test_extra_lineage_unauthorized_removed |
| BAT-05-complete-three-row-lineage | PASS | PASS | test_extra_lineage_complete |
| BAT-05-core-preserved | PASS | PASS | test_extra_lineage_modified |
| BAT-06-adaptive-authoring | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-06-relocation | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-06-no-concrete-identity | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-06-relative-runtime-paths | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-07-bound | PASS | PASS | test_binding_bound |
| BAT-07-missing | PASS | PASS | test_binding_missing |
| BAT-07-invalid | PASS | PASS | test_binding_bad_descriptor |
| BAT-07-root-mismatch | PASS | PASS | test_binding_wrong_root |
| BAT-07-unbound | PASS | PASS | test_binding_unbound |
| BAT-07-package-changed | PASS | PASS | test_binding_changed |
| BAT-07-role-mismatch | PASS | PASS | test_binding_role_mismatch |
| BAT-07-not-selected | PASS | PASS | test_binding_inactive |
| BAT-07-ambiguous-role | PASS | PASS | test_binding_ambiguous |
| BAT-07-unsafe-path | PASS | PASS | test_binding_unsafe_argument |
| BAT-07-capture-limit | PASS | PASS | test_binding_2001_limit |
| BAT-07-io-error | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-07-duplicate-name | PASS | PASS | test_binding_duplicate |
| BAT-07-no-product-effects | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-08-all-valid-record-families | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-08-duplicate-key | PASS | PASS | test_records_duplicate_and_nonfinite |
| BAT-08-extra-field | PASS | PASS | test_records_extra_field |
| BAT-08-unknown-version | PASS | PASS | test_records_unknown_version |
| BAT-08-malformed-reference | PASS | PASS | test_records_wrong_locator |
| BAT-08-malformed-digest | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-08-unresolved-id | PASS | PASS | test_records_unresolved_requirement |
| BAT-08-boolean-integer | PASS | PASS | test_records_boolean_integer |
| BAT-08-nonfinite-number | PASS | PASS | test_records_duplicate_and_nonfinite |
| BAT-08-misleading-lineage-text | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-09-legacy-authoring-contract | PASS | PASS | test_legacy_arbitrary_requirements |
| BAT-09-legacy-validation-request | PASS | PASS | test_ordinary_create_manual_request |
| BAT-09-closed-top-level | PASS | PASS | test_legacy_closed_contract |
| BAT-09-legacy-reference-base | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-10-a-fails | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-10-b-dependency-blocked | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-10-c-authored | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-10-aggregate-partial | PASS | PASS | test_records_partial_reduction |
| BAT-10-eligible-subset | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-10-subset-dependency-closure | PASS | PASS | test_extra_subset_dependency_rejected |
| BAT-11-cycle | PASS | PASS | test_records_cycle |
| BAT-11-missing-dependency | PASS | PASS | test_records_missing_dependency |
| BAT-11-occupied-target | PASS | PASS | test_records_occupied_target |
| BAT-11-user-edited-obsolete | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-11-concurrent-drift | PASS | PASS | test_extra_concurrent_drift_preserved |
| BAT-11-partial-paths | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-positive-propose | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-positive-author-set | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-positive-review-updates | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-negative-install | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-negative-test-only | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-explicit-native | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-12-implicit-discovery | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-13-no-change | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-13-equal-semantics-changed-bytes | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-13-removed-required-contract | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-13-missing-parent | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-13-no-auto-rebase | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-14-python-tdd | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-14-rust-implementation-first | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-14-typescript-monorepo | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-14-documentation-only | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-15-spaces | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-15-non-ascii | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-15-shell-significant | PASS | NOT_RUN | Native/semantic campaign incomplete |
| BAT-15-missing-interpreter | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-15-offline | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-15-no-install | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-16-evidence-drift | PASS | PASS | test_records_stale_reference |
| BAT-16-fresh-linked-proposal | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-16-no-stale-approval | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-17-claude-import | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-17-observed-first-edit | PASS | PASS | test_observed_edit_preserves_unrelated |
| BAT-17-authored-baseline | PASS | PASS | test_extra_authored_baseline_edit |
| BAT-17-legacy-generated | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-17-legacy-adopted | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
| BAT-17-corrupt-history | PASS | PASS | test_known_corrupt_history_blocks |
| BAT-17-no-fake-complete | NOT_RUN | NOT_RUN | Native/semantic campaign incomplete |
