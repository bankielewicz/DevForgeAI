# Closed review-v2 request slice

Status: **COMPLETE for the selected review intake and verification slice**. Runner/protocol integration, native preflight, native trials, full-suite coverage, independent QA, and framework acceptance remain parent-scope work.

## Delivered behavior

- Review v2 is a distinct closed deserialization contract. It retains every v1 field and requires `launch_policy_id`, `launch_policy_sha256`, `source_inventory_ref`, and `source_inventory_sha256` with their exact types.
- `Request::verify_preflight_review() -> Result<Vec<PathBuf>>` accepts false operator findings for bootstrap inspection while enforcing every request, review, policy, model, effort, inventory, and source binding.
- `Request::verify_review()` preserves peer and review-v1 behavior. For review v2 it requires all four operator findings true in addition to the complete preflight validation.
- Both request profile and review must select `gpt-6-astra` / `high`, the pinned native adapter, request schema 2, the compiled launch-policy ID, and the exact compiled policy digest.
- The referenced source inventory must have a valid exact digest, deserialize through the closed inventory schema, identify the request checkout, and pass fixed-root live `Inventory::verify()` freshness checking.
- Review `profile_sources` must exactly equal the inventory file bindings after strict path resolution. Missing, duplicate, extra, changed, invalid-digest, forbidden credential-named, inaccessible, or reparse sources prevent qualification.
- The returned paths come only from `Inventory::file_paths()`. There is no public source-collector override. The private collector-verification seam exists only under `cfg(test)`.

## Verification

| Attempt | Result | Evidence |
| --- | --- | --- |
| Red before behavior | Expected Cargo exit 101: missing review-v2 API; concurrent protocol also referenced that missing API | `01-red/` |
| Initial green | PASS, 5/5 review-v2 test functions | `02-green/` |
| Owned rustfmt before formatting correction | Expected diff, retained | `03-format-check/` |
| Owned rustfmt after correction | PASS | `04-owned-rustfmt/` |
| Refactor review-v2 tests | PASS, 5/5 | `05-refactor-test/` |
| Legacy profile regression | PASS, 3/3 | `06-legacy-profile/` |
| Initial library Clippy | FAIL only in concurrently owned `profile_sources.rs`; reported to its owner | `07-lib-clippy/` |
| Expanded closed-schema and exact-coverage tests | PASS, 5/5 with missing/null/wrong/duplicate/unknown subcases | `08-expanded-test/` |
| Expanded owned rustfmt | PASS | `09-expanded-format/` |
| Library Clippy after the profile-source owner corrected its finding | PASS with warnings denied | `10-lib-clippy/` |
| Explicit v1 review error-contract preservation | PASS, 3/3 legacy profile tests | `11-v1-error-contract/` |
| Final expanded review-v2 tests | PASS, 5/5 | `12-v2-final/` |
| Final library Clippy | PASS with warnings denied | `13-final-clippy/` |
| Final owned rustfmt | PASS | `14-final-rustfmt/` |
| Review-v2 binding after the selected 35-feature policy digest changed | PASS, 5/5 | `15-policy-rebind/` |

Every attempt retains raw stdout/stderr, exact argv and cwd, native exit, UTC start/end, duration, tool digest, and package candidate manifest. No Codex process or configuration mutation occurred.

## Source readback

The two owned files and exact final hashes are recorded in `source-readback.json`. The `request.rs` change also includes the cfg(test) path to the owned review-v2 cases.

Framework acceptance: **NOT_EVALUATED**.
